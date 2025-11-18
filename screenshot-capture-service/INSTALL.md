# Installation - Screenshot Capture Service

Guide d'installation complet pour le Screenshot Capture Service sur macOS.

## 📋 Prérequis

### Système
- **macOS 12.0 (Monterey)** ou supérieur
- **Python 3.8+** (vérifier avec `python3 --version`)

### Vérification Python

```bash
python3 --version
# Doit afficher Python 3.8.x ou supérieur
```

Si Python n'est pas installé, télécharger depuis [python.org](https://www.python.org/downloads/macos/).

## 📦 Installation des dépendances

### Option 1 : Installation avec pip

```bash
cd screenshot-capture-service
pip3 install flask flask-cors watchdog psutil
```

### Option 2 : Installation avec requirements.txt (si disponible)

```bash
cd screenshot-capture-service
pip3 install -r requirements.txt
```

### Vérification des dépendances

```bash
python3 -c "import flask, flask_cors, watchdog, psutil; print('✅ Toutes les dépendances sont installées')"
```

## 🔧 Configuration

### 1. Vérifier la configuration

Le fichier `config.py` contient la configuration par défaut :

```python
API_PORT = 5001
SCREENSHOTS_DIR = Path.home() / "Documents" / "TestCaseScreenshots"
LOG_FILE = SCREENSHOTS_DIR / "screenshot-capture.log"
```

### 2. Créer les répertoires nécessaires

Les répertoires sont créés automatiquement au premier démarrage, mais vous pouvez les créer manuellement :

```bash
mkdir -p ~/Documents/TestCaseScreenshots
```

### 3. Vérifier les permissions

Assurez-vous d'avoir les permissions d'écriture :

```bash
touch ~/Documents/TestCaseScreenshots/test.txt
rm ~/Documents/TestCaseScreenshots/test.txt
```

Si cela échoue, vérifiez les permissions du dossier Documents.

## 🚀 Installation des scripts

### Rendre les scripts exécutables

```bash
cd screenshot-capture-service
chmod +x start-service.py
chmod +x stop-service.py
chmod +x test_all_phases.py
chmod +x view-logs.py
```

## ✅ Vérification de l'installation

### Test 1 : Vérifier que tout fonctionne

```bash
cd screenshot-capture-service
python3 test_all_phases.py
```

Cela devrait exécuter tous les tests et afficher un résumé.

### Test 2 : Démarrer le service

```bash
python3 screenshot-capture-service/start-service.py
```

Dans un autre terminal :

```bash
curl http://localhost:5001/status
```

Vous devriez voir une réponse JSON avec le statut du service.

### Test 3 : Arrêter le service

```bash
python3 screenshot-capture-service/stop-service.py
```

## 🔐 Permissions macOS

### Permissions d'accessibilité (si nécessaire)

Si le popup ne s'affiche pas, vous devrez peut-être autoriser Python dans les paramètres macOS :

1. **Système Préférences** → **Sécurité et confidentialité** → **Accessibilité**
2. Ajouter Python ou Terminal à la liste des applications autorisées
3. Redémarrer le service

### Permissions de fichiers

Le service doit avoir accès à :
- `~/Desktop` (pour surveiller les captures)
- `~/Documents/TestCaseScreenshots/` (pour sauvegarder)

Ces permissions sont généralement accordées automatiquement.

## 🐛 Dépannage de l'installation

### Problème : ModuleNotFoundError

**Erreur** : `ModuleNotFoundError: No module named 'flask'`

**Solution** :
```bash
pip3 install flask flask-cors watchdog psutil
```

### Problème : Permission denied

**Erreur** : `PermissionError: [Errno 13] Permission denied`

**Solution** :
```bash
# Vérifier les permissions
ls -la ~/Documents/TestCaseScreenshots/

# Corriger si nécessaire
chmod 755 ~/Documents/TestCaseScreenshots/
```

### Problème : Port déjà utilisé

**Erreur** : `Address already in use` sur le port 5001

**Solution** :
```bash
# Trouver le processus utilisant le port
lsof -i :5001

# Arrêter le processus ou changer le port dans config.py
```

### Problème : Python non trouvé

**Erreur** : `python3: command not found`

**Solution** :
```bash
# Installer Python depuis python.org
# Ou utiliser Homebrew
brew install python3
```

## 📝 Configuration avancée

### Changer le port API

Éditer `config.py` :

```python
API_PORT = 5002  # Changer de 5001 à 5002
```

### Changer le dossier de destination

Éditer `config.py` :

```python
SCREENSHOTS_DIR = Path.home() / "Desktop" / "MyScreenshots"
```

### Changer le niveau de log

Éditer `config.py` :

```python
LOG_LEVEL = "DEBUG"  # DEBUG, INFO, WARNING, ERROR
```

## ✅ Installation terminée

Une fois l'installation terminée, vous pouvez :

1. **Démarrer le service** : `python3 screenshot-capture-service/start-service.py`
2. **Lire le guide d'utilisation** : Voir [USAGE.md](USAGE.md)
3. **Tester le service** : `python3 screenshot-capture-service/test_all_phases.py`

## 🔄 Mise à jour

Pour mettre à jour le service :

```bash
cd screenshot-capture-service
git pull  # Si vous utilisez Git
pip3 install --upgrade flask flask-cors watchdog psutil
```

## 📞 Support

Si vous rencontrez des problèmes lors de l'installation :

1. Vérifier les logs : `python3 screenshot-capture-service/view-logs.py`
2. Vérifier les prérequis ci-dessus
3. Consulter la section Dépannage dans [USAGE.md](USAGE.md)

