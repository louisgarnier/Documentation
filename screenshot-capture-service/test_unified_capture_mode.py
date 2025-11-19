#!/usr/bin/env python3
"""
Script de test pour valider le mode capture unifié
Teste l'intégration Service API + Watcher via un seul bouton
"""

import requests
import time
import subprocess
import sys
import os
from pathlib import Path

# Configuration
BACKEND_URL = "http://localhost:8000"
SERVICE_URL = "http://localhost:5001"
SERVICE_DIR = Path(__file__).parent

# Couleurs pour l'affichage
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"

def print_header(text):
    """Affiche un en-tête"""
    print(f"\n{BOLD}{BLUE}{'='*60}{RESET}")
    print(f"{BOLD}{BLUE}{text}{RESET}")
    print(f"{BOLD}{BLUE}{'='*60}{RESET}\n")

def print_step(step_num, description):
    """Affiche une étape"""
    print(f"\n{BOLD}Étape {step_num}: {description}{RESET}")
    print("-" * 60)

def print_success(message):
    """Affiche un message de succès"""
    print(f"{GREEN}✓ {message}{RESET}")

def print_error(message):
    """Affiche un message d'erreur"""
    print(f"{RED}✗ {message}{RESET}")

def print_warning(message):
    """Affiche un avertissement"""
    print(f"{YELLOW}⚠ {message}{RESET}")

def print_info(message):
    """Affiche une information"""
    print(f"{BLUE}ℹ {message}{RESET}")

def wait_for_user():
    """Attend que l'utilisateur appuie sur Entrée"""
    input(f"\n{YELLOW}→ Appuyez sur Entrée pour continuer...{RESET}")

def check_backend():
    """Vérifie si le backend est accessible"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=2)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def get_service_status():
    """Récupère le statut du service via le backend"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/capture-service/status", timeout=2)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException:
        return None

def test_step_1():
    """Étape 1: Vérifier que le backend est accessible"""
    print_step(1, "Vérifier que le Backend est Accessible")
    
    if check_backend():
        print_success("Backend accessible")
        return True
    else:
        print_error("Backend non accessible")
        print_warning("Démarrez le backend avec: cd backend && uvicorn api.main:app --reload")
        return False

def test_step_2():
    """Étape 2: Vérifier l'état initial (Service API OFF)"""
    print_step(2, "Vérifier l'État Initial")
    
    status = get_service_status()
    if not status:
        print_error("Impossible de récupérer le statut")
        return False
    
    print_info(f"Service API: {'ON' if status.get('service_running') else 'OFF'}")
    print_info(f"Watcher: {'ON' if status.get('watcher_running') else 'OFF'}")
    
    if not status.get('service_running') and not status.get('watcher_running'):
        print_success("État initial correct (tout est OFF)")
        return True
    else:
        print_warning("Le service ou le watcher est déjà actif")
        return True  # Pas une erreur, juste un avertissement

def test_step_3():
    """Étape 3: Activer le mode capture (Service API + Watcher)"""
    print_step(3, "Activer le Mode Capture (Service API + Watcher)")
    
    print_info("Démarrage du Service API via le backend...")
    try:
        response = requests.post(f"{BACKEND_URL}/api/capture-service/start", timeout=10)
        if response.status_code == 200:
            result = response.json()
            print_success(f"Service API: {result.get('message')}")
        else:
            print_error(f"Erreur HTTP {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Erreur: {e}")
        return False
    
    # Attendre que le service démarre
    print_info("Attente du démarrage du service (5 secondes)...")
    time.sleep(5)
    
    # Vérifier le statut
    status = get_service_status()
    if status and status.get('service_running'):
        print_success("Service API: ON")
    else:
        print_warning("Service API pas encore prêt, attente supplémentaire...")
        time.sleep(3)
        status = get_service_status()
        if not status or not status.get('service_running'):
            print_error("Service API n'a pas démarré")
            return False
    
    # Démarrer le watcher
    print_info("Démarrage du Watcher...")
    try:
        response = requests.post(f"{SERVICE_URL}/start", timeout=5)
        if response.status_code == 200:
            print_success("Watcher démarré")
        else:
            print_error(f"Erreur HTTP {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Erreur: {e}")
        return False
    
    # Vérification finale
    time.sleep(2)
    status = get_service_status()
    if status and status.get('service_running') and status.get('watcher_running'):
        print_success("✓ Service API: ON")
        print_success("✓ Watcher: ON")
        print_success("✓ Mode Capture: ACTIF")
        return True
    else:
        print_error("Le mode n'a pas été activé correctement")
        return False

def test_step_4():
    """Étape 4: Prendre une capture (vérification manuelle)"""
    print_step(4, "Prendre une Capture d'écran (Vérification Manuelle)")
    
    print_info("Le watcher surveille maintenant le Desktop")
    print_info("Instructions:")
    print("  1. Utilisez Shift+Cmd+4 pour prendre une capture")
    print("  2. Sélectionnez une zone à capturer")
    print("  3. Le popup devrait apparaître automatiquement")
    print("  4. Entrez un nom et une description")
    print("  5. Cliquez sur 'Save'")
    
    print_warning("\n⚠ VÉRIFICATION MANUELLE REQUISE")
    print("Vérifiez que:")
    print("  ✓ Le popup apparaît après la capture")
    print("  ✓ Vous pouvez entrer un nom et une description")
    print("  ✓ Les fichiers sont sauvegardés")
    
    wait_for_user()
    
    response = input("\nLe popup est-il apparu et avez-vous pu sauvegarder? (o/n): ")
    if response.lower() == 'o':
        print_success("✓ Étape 4 validée")
        return True
    else:
        print_error("✗ Étape 4 échouée")
        return False

def test_step_5():
    """Étape 5: Désactiver le mode capture (Service API + Watcher)"""
    print_step(5, "Désactiver le Mode Capture (Service API + Watcher)")
    
    # Arrêter le watcher
    print_info("Arrêt du Watcher...")
    try:
        response = requests.post(f"{SERVICE_URL}/stop", timeout=5)
        if response.status_code == 200:
            print_success("Watcher arrêté")
        else:
            print_warning(f"Erreur HTTP {response.status_code}")
    except Exception as e:
        print_warning(f"Erreur: {e}")
    
    # Arrêter le service API
    print_info("Arrêt du Service API...")
    try:
        response = requests.post(f"{BACKEND_URL}/api/capture-service/stop", timeout=10)
        if response.status_code == 200:
            result = response.json()
            print_success(f"Service API: {result.get('message')}")
        else:
            print_error(f"Erreur HTTP {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Erreur: {e}")
        return False
    
    # Vérification
    time.sleep(3)
    status = get_service_status()
    if status and not status.get('service_running') and not status.get('watcher_running'):
        print_success("✓ Service API: OFF")
        print_success("✓ Watcher: OFF")
        print_success("✓ Mode Capture: INACTIF")
        return True
    else:
        print_warning("Le mode n'a pas été complètement désactivé")
        if status:
            print_info(f"Statut: {status}")
        return False

def test_step_6():
    """Étape 6: Vérifier que le popup n'apparaît plus"""
    print_step(6, "Vérifier que le Popup n'Apparaît Plus")
    
    print_info("Le mode capture est maintenant INACTIF")
    print_info("Instructions:")
    print("  1. Utilisez Shift+Cmd+4 pour prendre une capture")
    print("  2. Sélectionnez une zone à capturer")
    print("  3. Le popup NE devrait PAS apparaître")
    
    print_warning("\n⚠ VÉRIFICATION MANUELLE REQUISE")
    print("Vérifiez que:")
    print("  ✓ Le popup N'apparaît PAS après la capture")
    print("  ✓ La capture est sauvegardée normalement sur le Desktop")
    
    wait_for_user()
    
    response = input("\nLe popup n'est-il pas apparu? (o/n): ")
    if response.lower() == 'o':
        print_success("✓ Étape 6 validée")
        return True
    else:
        print_error("✗ Étape 6 échouée")
        return False

def main():
    """Fonction principale"""
    print_header("TEST DU MODE CAPTURE UNIFIÉ")
    
    print_info("Ce script teste l'intégration Service API + Watcher:")
    print("  1. Vérifier que le backend est accessible")
    print("  2. Vérifier l'état initial")
    print("  3. Activer le mode capture (Service API + Watcher)")
    print("  4. Prendre une capture (vérification manuelle)")
    print("  5. Désactiver le mode capture (Service API + Watcher)")
    print("  6. Vérifier que le popup n'apparaît plus")
    
    wait_for_user()
    
    results = []
    
    # Étape 1
    if not test_step_1():
        print_error("Le backend n'est pas accessible. Arrêt des tests.")
        return
    wait_for_user()
    
    # Étape 2
    results.append(("Étape 2: État Initial", test_step_2()))
    wait_for_user()
    
    # Étape 3
    results.append(("Étape 3: Activer Mode Capture", test_step_3()))
    wait_for_user()
    
    # Étape 4
    results.append(("Étape 4: Prendre une Capture", test_step_4()))
    wait_for_user()
    
    # Étape 5
    results.append(("Étape 5: Désactiver Mode Capture", test_step_5()))
    wait_for_user()
    
    # Étape 6
    results.append(("Étape 6: Vérifier Popup Désactivé", test_step_6()))
    
    # Résumé
    print_header("RÉSUMÉ DES TESTS")
    
    all_passed = True
    for step_name, passed in results:
        if passed:
            print_success(f"{step_name}: ✓ RÉUSSI")
        else:
            print_error(f"{step_name}: ✗ ÉCHOUÉ")
            all_passed = False
    
    print("\n" + "="*60)
    if all_passed:
        print_success("TOUS LES TESTS SONT RÉUSSIS! 🎉")
    else:
        print_error("CERTAINS TESTS ONT ÉCHOUÉ")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Test interrompu par l'utilisateur{RESET}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

