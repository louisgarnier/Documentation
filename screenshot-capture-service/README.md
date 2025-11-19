# Screenshot Capture Service

Service macOS pour intercepter et organiser automatiquement les captures d'écran lors de la création de test cases.

## 🎯 Vue d'ensemble

Ce service permet de :
- **Activer un mode "test case"** depuis l'interface web ou en ligne de commande
- **Intercepter automatiquement** les captures d'écran macOS (Shift+Cmd+4)
- **Afficher un popup** pour nommer et décrire la capture avec Test Case et Step #
- **Sauvegarder organisé** : captures et descriptions dans un dossier dédié
- **Intégration facile** : fichiers prêts à être importés dans le Test Case Manager

## 🏗️ Architecture

Le service est composé de 3 composants principaux :

1. **Service API** (`screenshot-service.py`)
   - API Flask légère sur `localhost:5001`
   - Endpoints : `/status`, `/start`, `/stop`, `/health`
   - Gère l'activation/désactivation du mode capture

2. **Watcher** (`screenshot-watcher.py`)
   - Surveille le Desktop pour nouvelles captures
   - Détecte les fichiers `.png` créés
   - Lance le popup de saisie d'informations
   - Déplace et renomme les fichiers avec les métadonnées

3. **Système de Logging** (`logger.py`)
   - Logs structurés avec rotation automatique
   - Traçabilité complète de toutes les opérations
   - Logs dans `~/Documents/TestCaseScreenshots/screenshot-capture.log`

## 📋 Prérequis

- **macOS** (testé sur macOS 12+)
- **Python 3.8+**
- **Dépendances** : `flask`, `flask-cors`, `watchdog`, `psutil`

## 🚀 Installation

Voir [INSTALL.md](INSTALL.md) pour les instructions détaillées d'installation.

## ✅ Checklist de Vérification Avant Utilisation

Avant d'utiliser le Screenshot Capture Service, vérifiez que tout est correctement configuré :

### 1. Vérification de l'Environnement

- [ ] **Python 3.8+ installé** : `python3 --version`
- [ ] **Dépendances installées** : `pip3 list | grep -E "flask|watchdog|psutil"`
- [ ] **macOS compatible** : macOS 12 ou supérieur

### 2. Vérification des Répertoires

- [ ] **Dossier Desktop accessible** : `ls ~/Desktop` (doit exister)
- [ ] **Dossier de destination créé** : `ls ~/Documents/TestCaseScreenshots` (sera créé automatiquement si absent)
- [ ] **Permissions d'écriture** : Vérifier que vous pouvez créer des fichiers dans `~/Documents/`

### 3. Vérification des Services

#### Backend (FastAPI)
- [ ] **Backend démarré** : `curl http://localhost:8000/health` (doit retourner `{"status":"healthy"}`)
- [ ] **Backend accessible** : Ouvrir `http://localhost:8000` dans le navigateur

#### Frontend (Next.js)
- [ ] **Frontend démarré** : `curl http://localhost:3000` (doit retourner du HTML)
- [ ] **Frontend accessible** : Ouvrir `http://localhost:3000` dans le navigateur

#### Service API (Flask) - Optionnel
- [ ] **Service API peut démarrer** : `python3 screenshot-capture-service/start-service.py` (test rapide)
- [ ] **Port 5001 disponible** : `lsof -i :5001` (ne doit pas être utilisé par autre chose)

**Note** : Le Service API se démarre automatiquement depuis l'interface web, pas besoin de le démarrer manuellement.

### 4. Vérification de la Configuration

- [ ] **Fichier config.py existe** : `ls screenshot-capture-service/config.py`
- [ ] **Port API configuré** : Vérifier `API_PORT = 5001` dans `config.py`
- [ ] **Dossier Desktop correct** : Vérifier `DESKTOP_DIR` dans `config.py` pointe vers `~/Desktop`

### 5. Vérification de l'Intégration

- [ ] **Interface web accessible** : `http://localhost:3000`
- [ ] **Page de test case accessible** : Ouvrir un test case dans l'interface
- [ ] **Bouton "Capture Mode" visible** : Doit apparaître en haut à droite de la page de test case

### 6. Test Rapide

- [ ] **Test de connexion backend** : `curl http://localhost:8000/api/capture-service/status`
- [ ] **Test de démarrage service** : Cliquer sur "Capture Mode: OFF" dans l'interface
- [ ] **Voyants s'affichent** : Service API et Capture Mode doivent afficher leur état

### 7. Vérification des Logs

- [ ] **Dossier de logs existe** : `ls ~/Documents/TestCaseScreenshots/screenshot-capture.log` (sera créé au premier démarrage)
- [ ] **Permissions d'écriture logs** : Vérifier que les logs peuvent être créés

## 🔍 Commandes de Vérification Rapide

```bash
# Vérifier Python
python3 --version

# Vérifier dépendances
pip3 list | grep -E "flask|watchdog|psutil"

# Vérifier répertoires
ls ~/Desktop && ls ~/Documents/TestCaseScreenshots 2>/dev/null || echo "Dossier sera créé automatiquement"

# Vérifier backend
curl http://localhost:8000/health

# Vérifier frontend
curl http://localhost:3000

# Vérifier port 5001 (doit être libre)
lsof -i :5001 || echo "Port 5001 disponible"

# Vérifier configuration
cat screenshot-capture-service/config.py | grep -E "API_PORT|DESKTOP_DIR|SCREENSHOTS_DIR"
```

## ⚠️ Problèmes Courants

Si une vérification échoue :

1. **Backend non accessible** : Démarrer avec `cd backend && uvicorn api.main:app --reload`
2. **Frontend non accessible** : Démarrer avec `cd frontend && npm run dev`
3. **Port 5001 occupé** : Arrêter le processus avec `pkill -f screenshot-service`
4. **Dépendances manquantes** : Installer avec `pip3 install -r screenshot-capture-service/requirements.txt`
5. **Permissions refusées** : Vérifier les permissions des dossiers Desktop et Documents

## 📖 Utilisation

Voir [USAGE.md](USAGE.md) pour le guide d'utilisation complet.

### Démarrage rapide (Mode Unifié)

**Le service se démarre automatiquement depuis l'interface web !**

1. **Démarrer Backend et Frontend** :
   ```bash
   # Terminal 1 - Backend
   cd backend && uvicorn api.main:app --reload
   
   # Terminal 2 - Frontend
   cd frontend && npm run dev
   ```

2. **Ouvrir l'interface** : `http://localhost:3000`

3. **Activer le mode capture** :
   - Ouvrir une page de test case
   - Cliquer sur "Capture Mode: OFF"
   - Le Service API démarre automatiquement
   - Les voyants affichent l'état

4. **Prendre des captures** : `Shift+Cmd+4` → Popup apparaît automatiquement

5. **Désactiver le mode** : Cliquer sur "Capture Mode: ON" → Tout s'arrête automatiquement

**Note** : Plus besoin de démarrer le Service API manuellement, tout est géré depuis l'interface !

## 📁 Structure du projet

```
screenshot-capture-service/
├── screenshot-service.py      # API Flask principale
├── screenshot-watcher.py      # Surveillance Desktop
├── description_dialog.py      # Popup de saisie (tkinter)
├── logger.py                  # Système de logging
├── config.py                  # Configuration
├── start-service.py           # Script de démarrage
├── stop-service.py            # Script d'arrêt
├── test_all_phases.py         # Suite de tests complète
├── view-logs.py               # Visualiseur de logs
├── README.md                  # Ce fichier
├── INSTALL.md                 # Instructions d'installation
└── USAGE.md                   # Guide d'utilisation
```

## 🔧 Configuration

La configuration se trouve dans `config.py` :

- **Port API** : `5001` (configurable)
- **Dossier Desktop** : `~/Desktop` (détection automatique)
- **Dossier de destination** : `~/Documents/TestCaseScreenshots/`
- **Fichier de log** : `~/Documents/TestCaseScreenshots/screenshot-capture.log`
- **Rotation logs** : 10MB max, 5 fichiers de backup

## 📝 Format des fichiers

Les captures sont sauvegardées avec le format :
- **Image** : `{test_case}_step{step_number}_{screenshot_name}.png`
- **Description** : `{test_case}_step{step_number}_{screenshot_name}.txt`

Exemple : `TC05_step1_orderinput.png` et `TC05_step1_orderinput.txt`

## 🧪 Tests

Exécuter la suite de tests complète :

```bash
python3 screenshot-capture-service/test_all_phases.py
```

Cela teste toutes les phases (Configuration, API, Watcher, Popup, Scripts).

## 📊 Visualisation des logs

```bash
# Dernières 50 lignes
python3 screenshot-capture-service/view-logs.py -n 50

# Résumé des logs
python3 screenshot-capture-service/view-logs.py --summary

# Filtrer par composant
python3 screenshot-capture-service/view-logs.py -c SERVICE

# Suivre les logs en temps réel
python3 screenshot-capture-service/view-logs.py -f
```

## 🔗 Intégration avec Test Case Manager

Les fichiers sauvegardés peuvent être facilement importés depuis l'interface web :
1. Activer le mode capture depuis une page de test case
2. Prendre des captures (Shift+Cmd+4)
3. Remplir le popup avec Test Case, Step #, nom et description
4. Les fichiers sont sauvegardés dans `~/Documents/TestCaseScreenshots/`
5. Utiliser "Add Screenshot" dans le Test Case Manager pour sélectionner les fichiers

## 🐛 Dépannage

Voir la section [Dépannage](USAGE.md#dépannage) dans USAGE.md.

## 📈 Statut du projet

✅ **Phases 1-9 complétées** :
- ✅ Configuration et structure
- ✅ Service API Flask
- ✅ Watcher Desktop
- ✅ Popup de saisie unifié
- ✅ Scripts de gestion avec logging
- ✅ Tests complets
- ✅ Documentation complète
- ✅ Intégration Interface Web
- ✅ Mode Capture Unifié (Service API + Watcher via un seul bouton)

**Status** : ✅ **Production Ready**

## 📄 Licence

Ce projet fait partie du Test Case Manager.

## 🤝 Contribution

Pour signaler un problème ou suggérer une amélioration, voir les issues du projet.
