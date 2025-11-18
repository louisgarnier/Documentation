# Plan : Screenshot Capture Service pour Test Case Manager

## Objectif

Créer un service qui intercepte les captures d'écran macOS (Shift+Cmd+4) quand un mode "test case" est activé depuis l'interface web, permettant de nommer et décrire automatiquement les captures pour les intégrer facilement dans les test cases.

## Contexte

- **Projet principal** : Test Case Documentation Tool (React/Next.js frontend + FastAPI backend)
- **Nouveau projet** : Service de capture d'écran macOS (projet parallèle)
- **Branche Git** : Nouvelle branche dédiée (ex: `feature/screenshot-capture-service`)

---

## Architecture

### Composants

1. **Service API léger** (`screenshot-service.py`)
   - API Flask sur `localhost:5001`
   - Endpoints : `/start`, `/stop`, `/status`
   - Gère le démarrage/arrêt du watcher
   - Très léger (~5-10 MB RAM)

2. **Script de surveillance** (`screenshot-watcher.py`)
   - Surveille le dossier Desktop pour nouvelles captures
   - Affiche popup natif macOS pour nom/description
   - Déplace et organise les captures dans dossier dédié
   - Ne tourne que quand activé

3. **Scripts de gestion** 
   - `start-service.py` : Démarre le service API
   - `stop-service.py` : Arrête le service API

4. **Système de logging**
   - Fichier de log : `~/Documents/TestCaseScreenshots/screenshot-capture.log`
   - Log toutes les activités : activations, captures, popups, erreurs
   - Format structuré avec timestamps
   - Rotation automatique des logs

5. **Intégration interface web**
   - Bouton "Enable/Disable Capture Mode" sur pages de test case
   - Appels API pour activer/désactiver le mode

---

## Structure du Projet

```
screenshot-capture-service/
├── README.md                    # Documentation principale
├── INSTALL.md                   # Instructions d'installation
├── USAGE.md                     # Guide d'utilisation
├── screenshot-service.py         # API Flask (service léger)
├── screenshot-watcher.py         # Script de surveillance Desktop
├── start-service.py              # Script de démarrage
├── stop-service.py               # Script d'arrêt
├── logger.py                     # Module de logging centralisé
├── requirements.txt              # Dépendances Python
├── config.py                     # Configuration (dossiers, ports, etc.)
└── tests/                        # Tests unitaires
    └── test_screenshot_service.py
```

---

## Workflow Utilisateur

### 1. Installation (une fois)
- Installer les dépendances Python
- Configurer le démarrage automatique (optionnel)
- Tester le service

### 2. Utilisation quotidienne
- Démarrer le service (si pas en auto-start)
- Ouvrir l'interface web du Test Case Manager
- Sur une page de test case → Cliquer "Enable Capture Mode"
- Faire des captures d'écran (Shift+Cmd+4)
- Popup apparaît → Entrer nom + description
- Capture sauvegardée dans dossier dédié
- Dans l'interface → "Add Screenshot" → Sélectionner depuis le dossier

### 3. Désactivation
- Cliquer "Disable Capture Mode" dans l'interface
- Ou arrêter le service manuellement

---

## Étapes d'Implémentation

### Phase 1 : Setup et Structure ✅
- [x] Créer nouvelle branche Git `feature/screenshot-capture-service`
- [x] Créer structure de dossiers
- [x] Créer `requirements.txt` avec dépendances
- [x] Créer `config.py` pour configuration
- [x] **Validation** : Structure créée, prête pour développement

### Phase 2 : Service API Flask
- [x] Créer `screenshot-service.py` avec API Flask
- [x] Implémenter endpoint `/start` (démarre watcher)
- [x] Implémenter endpoint `/stop` (arrête watcher)
- [x] Implémenter endpoint `/status` (vérifie état)
- [x] Implémenter endpoint `/health` (health check)
- [x] Gestion des processus (démarrage/arrêt du watcher)
- [x] Créer `start-service.py` (script de démarrage)
- [x] Créer `stop-service.py` (script d'arrêt)
- [x] **Tests** : Tester API avec curl/Postman ✅
- [x] **Validation** : API fonctionne, peut démarrer/arrêter le watcher ✅

### Phase 3 : Système de Logging
- [x] Créer `logger.py` avec configuration logging
- [x] Définir format de log (timestamp, niveau, message, données)
- [x] Configurer rotation automatique des logs
- [x] Implémenter fonctions de logging (info, warning, error, debug)
- [x] Implémenter StructuredFormatter pour format personnalisé
- [x] Implémenter ComponentAdapter pour composants (SERVICE, WATCHER, API)
- [x] **Tests** : Vérifier écriture logs, rotation ✅
- [x] **Validation** : Logs créés correctement, format cohérent ✅

### Phase 4 : Script de Surveillance
- [x] Créer `screenshot-watcher.py`
- [x] Surveiller dossier Desktop pour nouveaux fichiers `.png`
- [x] Détecter captures d'écran (pattern de nom macOS)
- [x] Gérer fichiers temporaires macOS (commencent par `.`)
- [x] Logger détection de capture
- [x] Afficher popup natif macOS (tkinter)
- [x] Logger ouverture popup
- [x] Récupérer nom de fichier et description
- [x] Logger nom et description saisis
- [x] Créer fichier texte avec description
- [x] Déplacer capture + description dans dossier dédié
- [x] Logger sauvegarde réussie
- [x] Gérer fichiers dupliqués (suffixe numérique)
- [x] **Tests** : Tester détection, popup, sauvegarde ✅
- [x] **Validation** : Capture détectée → popup → fichiers sauvegardés → tout loggé ✅
- [x] **Popup multiligne** : Textarea tkinter fonctionnel ✅
- [x] **Déplacement fichiers** : Images déplacées du Desktop vers `~/Documents/TestCaseScreenshots/` ✅

### Phase 4.4 : Amélioration UX du Popup (Un seul popup avec tous les champs)

**Objectif** : Remplacer les deux popups (nom + description) par un seul popup unifié avec tous les champs nécessaires.

**Tâches d'implémentation** :
- [x] Modifier `description_dialog.py` pour inclure tous les champs dans un seul popup ✅
- [x] Conserver la zone de texte libre pour la screenshot name (une ligne de texte) ✅
- [x] Ajouter champ "Test Case" (tag/projet) - input texte en haut à droite de screenshot name ✅
- [x] Ajouter champ "Step #" (numéro d'étape) - input numérique en haut à droite de Test case ✅
- [x] Conserver la zone de texte libre pour la description (textarea multiligne) en dessous ✅
- [x] Améliorer le layout (labels clairs, espacement, taille fenêtre 700x500) ✅
- [x] Modifier `screenshot-watcher.py` pour utiliser le nouveau popup unifié ✅
- [x] Supprimer le popup de nom séparé (AppleScript `simpledialog.askstring`) ✅
- [x] Adapter la logique de sauvegarde pour utiliser les nouveaux champs ✅
  - [x] Générer nom de fichier avec Test Case et Step # en priorité : `TC05_step1.png` ✅
  - [x] Format: `{test_case}_step{step_number}` ou `{test_case}_step{step_number}_{screenshot_name}` ✅
  - [x] Sauvegarder Test Case, Step #, et Description dans le fichier .txt ✅
- [x] Logger les nouvelles données (test_case, step_number, long_description) ✅
- [x] Gérer cas où Test Case ou Step # sont vides (génération de nom avec fallback) ✅
- [x] Supprimer champ "Short Description" (garder seulement Description multiligne) ✅

**Tests à effectuer** :
- [x] **Test 1 - Popup unique** : ✅
  - [x] Faire une capture d'écran (`Shift+Cmd+4`) ✅
  - [x] Vérifier qu'un seul popup apparaît (pas deux) ✅
  - [x] Vérifier que le popup contient : Screenshot Name, Test Case, Step #, Description ✅
  
- [x] **Test 2 - Saisie des champs** : ✅
  - [x] Saisir "TC05" dans Test Case ✅
  - [x] Saisir "1" dans Step # ✅
  - [x] Saisir une description multiligne avec bullet points ✅
  - [x] Cliquer OK ✅
  - [x] Vérifier que tous les champs sont bien capturés ✅
  
- [x] **Test 3 - Sauvegarde des fichiers** : ✅
  - [x] Vérifier que l'image est sauvegardée avec le bon nom (ex: `TC05_step1.png`) ✅
  - [x] Vérifier que le fichier .txt contient Test Case, Step #, et description ✅
  - [x] Vérifier que les fichiers sont dans `~/Documents/TestCaseScreenshots/` ✅
  
- [x] **Test 4 - Logs** : ✅
  - [x] Vérifier les logs contiennent : test_case, step_number, long_description ✅
  - [x] Vérifier le format des logs est cohérent ✅
  
- [x] **Test 5 - Cas limites** : ✅
  - [x] Tester avec Test Case vide (fallback sur screenshot_name ou nom original) ✅
  - [x] Tester avec Step # vide (fallback sur test_case seul ou screenshot_name) ✅
  - [x] Tester avec description vide (accepté, peut être vide) ✅
  - [x] Tester annulation (Cancel) - ne doit rien sauvegarder ✅

**Validation** : ✅ **COMPLÉTÉE**
- [x] Un seul popup user-friendly avec tous les champs ✅
- [x] Workflow simplifié (une seule interaction au lieu de deux) ✅
- [x] Fichiers sauvegardés avec noms cohérents incluant Test Case + Step # (ex: `TC05_step1.png`) ✅
- [x] Toutes les informations sont loggées correctement ✅
- [x] Nom de fichier inclut toujours Test Case et Step # pour référence rapide ✅

### Phase 4.5 : Tests d'Activation/Désactivation du Service

**Objectif** : Vérifier que le service peut être activé/désactivé et que le popup ne s'affiche que quand le service est actif.

**Tests à effectuer** :
- [x] **Test 1 - Vérifier l'état du service** : ✅
  - [x] Exécuter `curl http://localhost:5001/status` ✅
  - [x] Vérifier la réponse JSON avec `watcher_running` et `watcher_pid` ✅
  - [x] Vérifier que le processus est visible avec `ps aux | grep screenshot-watcher` ✅
  
- [x] **Test 2 - Désactiver le service** : ✅
  - [x] Exécuter `curl -X POST http://localhost:5001/stop` ✅
  - [x] Vérifier la réponse indique "stopped" ✅
  - [x] Vérifier que le processus watcher n'existe plus (`ps aux | grep screenshot-watcher`) ✅
  - [x] Vérifier le status avec `curl http://localhost:5001/status` → `watcher_running: false` ✅
  
- [x] **Test 3 - Test capture sans service actif** : ✅
  - [x] Avec le service désactivé, faire une capture d'écran (`Shift+Cmd+4`) ✅
  - [x] Vérifier qu'**aucun popup n'apparaît** ✅
  - [x] Vérifier que la capture reste sur le Desktop (non traitée) ✅
  - [x] Vérifier les logs ne montrent pas de détection de capture ✅
  
- [x] **Test 4 - Réactiver le service** : ✅
  - [x] Exécuter `curl -X POST http://localhost:5001/start` ✅
  - [x] Vérifier la réponse indique "started" avec un PID ✅
  - [x] Vérifier que le processus watcher existe (`ps aux | grep screenshot-watcher`) ✅
  - [x] Vérifier le status avec `curl http://localhost:5001/status` → `watcher_running: true` ✅
  
- [x] **Test 5 - Test capture avec service actif** : ✅
  - [x] Avec le service activé, faire une capture d'écran (`Shift+Cmd+4`) ✅
  - [x] Vérifier que le **popup apparaît** avec tous les champs ✅
  - [x] Remplir les champs et valider ✅
  - [x] Vérifier que les fichiers sont sauvegardés correctement ✅
  - [x] Vérifier les logs montrent la détection et le traitement ✅

**Validation** : ✅ **COMPLÉTÉE**
- [x] Le service peut être activé/désactivé via l'API ✅
- [x] Le popup ne s'affiche que quand le service est actif ✅
- [x] Les captures ne sont pas traitées quand le service est désactivé ✅
- [x] Le workflow complet fonctionne après réactivation ✅

### Phase 5 : Scripts de Gestion
- [x] Créer `start-service.py` (démarre service API) ✅
- [ ] Logger démarrage du service
- [x] Créer `stop-service.py` (arrête service API) ✅
- [ ] Logger arrêt du service
- [x] Gestion des processus en arrière-plan ✅
- [ ] **Tests** : Démarrer/arrêter le service avec les scripts ⚠️ **NON TESTÉ**
- [ ] **Validation** : Scripts fonctionnent correctement, logs créés ⚠️ **NON TESTÉ**

**Note** : Les scripts existent mais n'ont pas encore été testés. Les tests seront effectués après la Phase 4.5.

### Phase 6 : Documentation
- [ ] Créer `README.md` (vue d'ensemble)
- [ ] Créer `INSTALL.md` (instructions d'installation)
- [ ] Créer `USAGE.md` (guide d'utilisation)
- [ ] Documenter commandes terminal
- [ ] Documenter dépannage
- [ ] **Validation** : Documentation complète et claire

### Phase 7 : Intégration Interface Web
- [ ] Ajouter bouton "Enable/Disable Capture Mode" dans `TestCaseDetail.tsx`
- [ ] Créer fonction API dans `client.ts` pour appeler service local
- [ ] Logger activation/désactivation depuis interface web
- [ ] Gérer état actif/inactif (indicateur visuel)
- [ ] Gérer erreurs (service non démarré, etc.)
- [ ] Logger erreurs API
- [ ] **Tests** : Tester depuis l'interface web
- [ ] **Validation** : Bouton fonctionne, active/désactive le mode, logs créés

### Phase 8 : Tests Finaux
- [ ] Test complet du workflow
- [ ] Test avec plusieurs captures
- [ ] Test activation/désactivation
- [ ] Test intégration avec "Add Screenshot"
- [ ] **Validation** : Tout fonctionne end-to-end

---

## Détails Techniques

### Dépendances Python
```
flask>=2.3.0
watchdog>=3.0.0  # Pour surveiller le Desktop
tkinter          # Pour popup natif (inclus avec Python)
# ou PyObjC pour popup macOS natif
logging          # Pour système de logs (inclus avec Python)
```

### Configuration
- **Port API** : `5001` (configurable)
- **Dossier Desktop** : `~/Desktop` (détection automatique)
- **Dossier de destination** : `~/Documents/TestCaseScreenshots/` (configurable)
- **Fichier de log** : `~/Documents/TestCaseScreenshots/screenshot-capture.log`
- **Rotation logs** : Taille max 10MB, garder 5 fichiers de backup
- **Format fichiers** : 
  - Image : `{nom}.png`
  - Description : `{nom}.txt`

### Détection des captures
- Pattern de nom macOS : `Screen Shot YYYY-MM-DD at HH.MM.SS.png`
- Surveiller nouveaux fichiers dans `~/Desktop`
- Filtrer par extension `.png` et pattern de nom

### Popup natif macOS
- Utiliser `tkinter` (simple, inclus avec Python)
- Ou `PyObjC` pour popup macOS plus natif (optionnel)

---

## Tests et Validations

### Tests Unitaires
- [ ] Test détection nouvelle capture
- [ ] Test popup et récupération données
- [ ] Test sauvegarde fichiers
- [ ] Test API endpoints

### Tests d'Intégration
- [ ] Test workflow complet (activation → capture → popup → sauvegarde)
- [ ] Test activation/désactivation depuis interface web
- [ ] Test avec plusieurs captures successives
- [ ] Test gestion erreurs (service non démarré, etc.)

### Validations Utilisateur
- [ ] Installation simple et claire
- [ ] Activation/désactivation intuitive
- [ ] Popup fonctionne correctement
- [ ] Intégration avec "Add Screenshot" fluide

---

## Système de Logging

### Éléments à Logger

1. **Service API** :
   - Démarrage du service
   - Arrêt du service
   - Démarrage du watcher (activation mode)
   - Arrêt du watcher (désactivation mode)
   - Appels API (start/stop/status)
   - Erreurs API

2. **Watcher (Surveillance)** :
   - Détection nouvelle capture sur Desktop
   - Nom du fichier détecté
   - Ouverture du popup
   - Nom saisi par l'utilisateur
   - Description saisie par l'utilisateur
   - Annulation du popup (si applicable)
   - Sauvegarde réussie (fichiers créés/déplacés)
   - Erreurs de sauvegarde

3. **Interface Web** :
   - Activation mode depuis interface
   - Désactivation mode depuis interface
   - Erreurs de connexion au service

4. **Général** :
   - Erreurs système
   - Warnings (ex: service déjà démarré)
   - Debug (optionnel, pour développement)

### Format de Log

```
[YYYY-MM-DD HH:MM:SS] [LEVEL] [COMPONENT] Message | Data: {key: value}
```

Exemples :
```
[2025-01-18 10:30:45] [INFO] [SERVICE] Service started on port 5001
[2025-01-18 10:31:12] [INFO] [API] Mode activated via /start endpoint
[2025-01-18 10:32:05] [INFO] [WATCHER] Screenshot detected: Screen Shot 2025-01-18 at 10.32.05.png
[2025-01-18 10:32:15] [INFO] [WATCHER] Popup opened for screenshot naming
[2025-01-18 10:32:45] [INFO] [WATCHER] User input received | Name: step1-orderinput | Description: Order entry form validation
[2025-01-18 10:32:46] [INFO] [WATCHER] Files saved successfully | Image: step1-orderinput.png | Description: step1-orderinput.txt
[2025-01-18 10:33:20] [INFO] [API] Mode deactivated via /stop endpoint
[2025-01-18 10:35:00] [ERROR] [WATCHER] Failed to move file: Permission denied
```

### Rotation des Logs

- **Taille max** : 10 MB par fichier
- **Backups** : Garder 5 fichiers de backup maximum
- **Nommage** : `screenshot-capture.log`, `screenshot-capture.log.1`, etc.

## Questions à Résoudre

1. **Popup natif** : `tkinter` ou `PyObjC` ? ✅ **Résolu** : Utilisation de `osascript` (AppleScript) car tkinter ne fonctionne pas depuis un processus en arrière-plan sur macOS
2. **Dossier destination** : Dans le projet ou `~/Documents/` ? (à décider)
3. **Format description** : Fichier `.txt` séparé ou métadonnées ? (fichier .txt recommandé)
4. **Démarrage automatique** : Au démarrage du Mac ou manuel ? (manuel pour commencer)
5. **Gestion erreurs** : Que faire si service non démarré ? (message clair dans interface)
6. **Niveau de log par défaut** : INFO (production) ou DEBUG (développement) ? (INFO recommandé)

---

## Prochaines Étapes

1. **Créer branche Git** : `feature/screenshot-capture-service`
2. **Valider ce plan** avec l'utilisateur
3. **Commencer Phase 1** : Setup et structure
4. **Itérer** : Implémenter, tester, valider chaque phase

---

## Notes

- Ce projet est **indépendant** du projet principal
- Peut être développé en parallèle
- Doit être simple à installer et utiliser
- Doit avoir un impact minimal sur le système

---

**Date de création** : 2025-01-XX
**Status** : 📝 Planification - En attente de validation

