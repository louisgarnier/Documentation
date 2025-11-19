#!/usr/bin/env python3
"""
Script de test interactif pour valider le workflow complet
du Screenshot Capture Service étape par étape.
"""

import requests
import time
import subprocess
import sys
import os
from pathlib import Path

# Configuration
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

def check_service_running():
    """Vérifie si le service est en cours d'exécution"""
    try:
        response = requests.get(f"{SERVICE_URL}/status", timeout=2)
        if response.status_code == 200:
            return True, response.json()
        return False, None
    except requests.exceptions.RequestException:
        return False, None

def get_service_status():
    """Récupère le statut du service"""
    try:
        response = requests.get(f"{SERVICE_URL}/status", timeout=2)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException:
        return None

def start_service():
    """Démarre le service API"""
    print_info("Démarrage du service API...")
    try:
        # Vérifier si le service tourne déjà
        is_running, status = check_service_running()
        if is_running:
            print_warning("Le service est déjà en cours d'exécution")
            return True
        
        # Démarrer le service en arrière-plan
        service_script = SERVICE_DIR / "screenshot-service.py"
        if not service_script.exists():
            print_error(f"Fichier service introuvable: {service_script}")
            return False
        
        print_info(f"Exécution de: python3 {service_script}")
        subprocess.Popen(
            [sys.executable, str(service_script)],
            cwd=str(SERVICE_DIR),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        # Attendre que le service démarre
        print_info("Attente du démarrage du service (5 secondes)...")
        time.sleep(5)
        
        # Vérifier que le service a démarré
        is_running, status = check_service_running()
        if is_running:
            print_success("Service démarré avec succès")
            return True
        else:
            print_error("Le service n'a pas démarré correctement")
            return False
            
    except Exception as e:
        print_error(f"Erreur lors du démarrage: {e}")
        return False

def test_step_1():
    """Étape 1: Démarrer le Service API"""
    print_step(1, "Démarrer le Service API")
    
    print_info("Vérification de l'état actuel du service...")
    is_running, status = check_service_running()
    
    if is_running:
        print_success("Le service est déjà en cours d'exécution")
        print_info(f"Statut: {status}")
    else:
        print_warning("Le service n'est pas en cours d'exécution")
        response = input("\nVoulez-vous démarrer le service maintenant? (o/n): ")
        if response.lower() == 'o':
            if not start_service():
                print_error("Impossible de démarrer le service")
                return False
        else:
            print_warning("Veuillez démarrer le service manuellement:")
            print_info("  python3 screenshot-service.py")
            wait_for_user()
    
    # Vérification finale
    is_running, status = check_service_running()
    if is_running:
        print_success(f"Service API actif sur {SERVICE_URL}")
        print_info(f"Mode capture: {'ACTIF' if status.get('watcher_running', False) else 'INACTIF'}")
        print_info(f"Watcher: {'ACTIF' if status.get('watcher_running', False) else 'ARRÊTÉ'}")
        if status.get('watcher_pid'):
            print_info(f"Watcher PID: {status.get('watcher_pid')}")
        return True
    else:
        print_error("Le service n'est pas accessible")
        return False

def test_step_2():
    """Étape 2: Activer le Mode Capture"""
    print_step(2, "Activer le Mode Capture")
    
    # Vérifier l'état actuel
    status = get_service_status()
    if not status:
        print_error("Impossible de récupérer le statut du service")
        return False
    
    if status.get('watcher_running', False):
        print_warning("Le mode capture est déjà actif")
        print_info("Voulez-vous le désactiver puis le réactiver pour tester? (o/n): ")
        response = input()
        if response.lower() == 'o':
            print_info("Désactivation du mode...")
            requests.post(f"{SERVICE_URL}/stop")
            time.sleep(2)
        else:
            print_info("Test de l'activation ignoré (déjà actif)")
            return True
    
    print_info("Activation du mode capture...")
    print_info(f"POST {SERVICE_URL}/start")
    
    try:
        response = requests.post(f"{SERVICE_URL}/start", timeout=5)
        if response.status_code == 200:
            result = response.json()
            print_success("Mode capture activé")
            print_info(f"Réponse: {result}")
        else:
            print_error(f"Erreur HTTP {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Erreur lors de l'activation: {e}")
        return False
    
    # Vérification
    time.sleep(2)
    status = get_service_status()
    if status and status.get('watcher_running', False):
        print_success("✓ Mode capture: ACTIF")
        print_success("✓ Watcher: ACTIF")
        if status.get('watcher_pid'):
            print_info(f"Watcher PID: {status.get('watcher_pid')}")
        return True
    else:
        print_error("Le mode n'a pas été activé correctement")
        if status:
            print_info(f"Statut reçu: {status}")
        return False

def test_step_3():
    """Étape 3: Prendre une capture (vérification manuelle)"""
    print_step(3, "Prendre une Capture d'écran (Vérification Manuelle)")
    
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
    print("  ✓ Les fichiers sont sauvegardés dans le dossier configuré")
    
    wait_for_user()
    
    # Vérifier les fichiers créés
    config_path = SERVICE_DIR / "config.py"
    if config_path.exists():
        import importlib.util
        spec = importlib.util.spec_from_file_location("config", config_path)
        config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config)
        
        capture_dir = Path(config.SCREENSHOTS_DIR)
        if capture_dir.exists():
            print_info(f"\nVérification du dossier: {capture_dir}")
            files = list(capture_dir.glob("*.png"))
            txt_files = list(capture_dir.glob("*.txt"))
            
            if files:
                print_success(f"✓ {len(files)} fichier(s) image trouvé(s)")
                for f in files[-3:]:  # Afficher les 3 derniers
                    print_info(f"  - {f.name}")
            else:
                print_warning("Aucun fichier image trouvé")
            
            if txt_files:
                print_success(f"✓ {len(txt_files)} fichier(s) description trouvé(s)")
                for f in txt_files[-3:]:  # Afficher les 3 derniers
                    print_info(f"  - {f.name}")
            else:
                print_warning("Aucun fichier description trouvé")
    
    response = input("\nLe popup est-il apparu et avez-vous pu sauvegarder? (o/n): ")
    if response.lower() == 'o':
        print_success("✓ Étape 3 validée")
        return True
    else:
        print_error("✗ Étape 3 échouée - le popup n'est pas apparu")
        return False

def test_step_4():
    """Étape 4: Désactiver le Mode Capture"""
    print_step(4, "Désactiver le Mode Capture")
    
    # Vérifier l'état actuel
    status = get_service_status()
    if not status:
        print_error("Impossible de récupérer le statut du service")
        return False
    
    if not status.get('active', False):
        print_warning("Le mode capture est déjà inactif")
        return True
    
    print_info("Désactivation du mode capture...")
    print_info(f"POST {SERVICE_URL}/stop")
    
    try:
        response = requests.post(f"{SERVICE_URL}/stop", timeout=5)
        if response.status_code == 200:
            result = response.json()
            print_success("Mode capture désactivé")
            print_info(f"Réponse: {result}")
        else:
            print_error(f"Erreur HTTP {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Erreur lors de la désactivation: {e}")
        return False
    
    # Vérification
    time.sleep(2)
    status = get_service_status()
    if status and not status.get('watcher_running', False):
        print_success("✓ Mode capture: INACTIF")
        print_success("✓ Watcher: ARRÊTÉ")
        return True
    else:
        print_error("Le mode n'a pas été désactivé correctement")
        if status:
            print_info(f"Statut reçu: {status}")
        return False

def test_step_5():
    """Étape 5: Vérifier que le popup n'apparaît plus"""
    print_step(5, "Vérifier que le Popup n'Apparaît Plus")
    
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
        print_success("✓ Étape 5 validée - le popup n'apparaît plus")
        return True
    else:
        print_error("✗ Étape 5 échouée - le popup est encore apparu")
        return False

def main():
    """Fonction principale"""
    print_header("TEST DU WORKFLOW - Screenshot Capture Service")
    
    print_info("Ce script teste toutes les étapes du workflow:")
    print("  1. Démarrer le Service API")
    print("  2. Activer le Mode Capture")
    print("  3. Prendre une capture (vérification manuelle)")
    print("  4. Désactiver le Mode Capture")
    print("  5. Vérifier que le popup n'apparaît plus")
    
    wait_for_user()
    
    results = []
    
    # Étape 1
    results.append(("Étape 1: Démarrer le Service", test_step_1()))
    wait_for_user()
    
    # Étape 2
    results.append(("Étape 2: Activer le Mode Capture", test_step_2()))
    wait_for_user()
    
    # Étape 3
    results.append(("Étape 3: Prendre une Capture", test_step_3()))
    wait_for_user()
    
    # Étape 4
    results.append(("Étape 4: Désactiver le Mode Capture", test_step_4()))
    wait_for_user()
    
    # Étape 5
    results.append(("Étape 5: Vérifier Popup Désactivé", test_step_5()))
    
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

