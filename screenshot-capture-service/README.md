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

## 📖 Utilisation

Voir [USAGE.md](USAGE.md) pour le guide d'utilisation complet.

### Démarrage rapide

```bash
# Démarrer le service
python3 screenshot-capture-service/start-service.py

# Ou en arrière-plan
python3 screenshot-capture-service/screenshot-service.py &

# Activer le mode capture (depuis un autre terminal)
curl -X POST http://localhost:5001/start

# Prendre une capture (Shift+Cmd+4)
# Le popup apparaîtra automatiquement

# Désactiver le mode
curl -X POST http://localhost:5001/stop

# Arrêter le service
python3 screenshot-capture-service/stop-service.py
```

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

✅ **Phase 1-5 complétées** :
- ✅ Configuration et structure
- ✅ Service API Flask
- ✅ Watcher Desktop
- ✅ Popup de saisie unifié
- ✅ Scripts de gestion avec logging
- ✅ Tests complets

🚧 **En cours** :
- Phase 6 : Documentation (ce fichier)
- Phase 7 : Intégration Interface Web
- Phase 8 : Tests finaux

## 📄 Licence

Ce projet fait partie du Test Case Manager.

## 🤝 Contribution

Pour signaler un problème ou suggérer une amélioration, voir les issues du projet.
