# Guide d'utilisation - Screenshot Capture Service

Guide complet pour utiliser le Screenshot Capture Service.

## 🚀 Démarrage rapide

### 1. Démarrer le service

```bash
# Option 1 : Démarrer en mode interactif (recommandé pour débuter)
python3 screenshot-capture-service/start-service.py

# Option 2 : Démarrer en arrière-plan
python3 screenshot-capture-service/screenshot-service.py &
```

Le service démarre sur `http://localhost:5001`.

### 2. Activer le mode capture

```bash
# Depuis un terminal
curl -X POST http://localhost:5001/start

# Ou depuis l'interface web (Phase 7)
# Cliquer sur "Enable Capture Mode"
```

### 3. Prendre une capture

1. Utiliser le raccourci macOS standard : **Shift+Cmd+4**
2. Sélectionner la zone à capturer
3. Le popup apparaîtra automatiquement

### 4. Remplir le popup

- **Screenshot Name** : Nom de la capture (ex: `orderinput`)
- **Test Case** : Numéro du test case (ex: `TC05`)
- **Step #** : Numéro de l'étape (ex: `1`)
- **Description** : Description détaillée de la capture

### 5. Sauvegarde automatique

Les fichiers sont automatiquement sauvegardés dans :
- **Image** : `~/Documents/TestCaseScreenshots/TC05_step1_orderinput.png`
- **Description** : `~/Documents/TestCaseScreenshots/TC05_step1_orderinput.txt`

## 📋 Commandes Terminal

### Gestion du service

```bash
# Démarrer le service
python3 screenshot-capture-service/start-service.py

# Arrêter le service
python3 screenshot-capture-service/stop-service.py

# Vérifier si le service tourne
ps aux | grep screenshot-service.py
```

### API Endpoints

```bash
# Vérifier le statut
curl http://localhost:5001/status

# Activer le mode capture
curl -X POST http://localhost:5001/start

# Désactiver le mode capture
curl -X POST http://localhost:5001/stop

# Health check
curl http://localhost:5001/health
```

### Visualisation des logs

```bash
# Dernières 50 lignes
python3 screenshot-capture-service/view-logs.py -n 50

# Résumé des logs
python3 screenshot-capture-service/view-logs.py --summary

# Filtrer par composant
python3 screenshot-capture-service/view-logs.py -c SERVICE
python3 screenshot-capture-service/view-logs.py -c WATCHER

# Filtrer par niveau
python3 screenshot-capture-service/view-logs.py -l ERROR

# Suivre les logs en temps réel (comme tail -f)
python3 screenshot-capture-service/view-logs.py -f

# Voir toutes les lignes
python3 screenshot-capture-service/view-logs.py -n 0
```

### Tests

```bash
# Exécuter tous les tests
python3 screenshot-capture-service/test_all_phases.py
```

## 🔄 Workflow complet

### Scénario 1 : Création d'un nouveau test case

1. **Démarrer le service**
   ```bash
   python3 screenshot-capture-service/start-service.py &
   ```

2. **Ouvrir le Test Case Manager** dans le navigateur

3. **Créer ou ouvrir un test case** (ex: TC05)

4. **Activer le mode capture** (bouton dans l'interface ou API)

5. **Prendre des captures** pour chaque étape :
   - Shift+Cmd+4
   - Remplir le popup avec TC05, Step #, nom, description
   - Répéter pour chaque étape

6. **Importer les captures** dans le Test Case Manager :
   - Cliquer sur "Add Screenshot" dans l'étape
   - Sélectionner les fichiers depuis `~/Documents/TestCaseScreenshots/`

7. **Désactiver le mode capture** quand terminé

### Scénario 2 : Ajout de captures à un test existant

1. **Service déjà démarré** (vérifier avec `curl http://localhost:5001/status`)

2. **Ouvrir le test case** dans le Test Case Manager

3. **Activer le mode capture**

4. **Prendre les captures** nécessaires

5. **Importer** via "Add Screenshot"

6. **Désactiver** le mode capture

## 🎯 Utilisation avancée

### Mode capture persistant

Le mode capture reste actif même après avoir fermé la page web. Pour le désactiver :

```bash
curl -X POST http://localhost:5001/stop
```

### Plusieurs captures rapides

1. Activer le mode une fois
2. Prendre plusieurs captures successives
3. Remplir chaque popup
4. Désactiver le mode à la fin

### Organisation des fichiers

Les fichiers sont nommés automatiquement :
- Format : `{test_case}_step{step_number}_{screenshot_name}.png`
- Exemple : `TC05_step1_orderinput.png`

Les descriptions sont dans des fichiers `.txt` correspondants.

### Logs et débogage

Pour activer les logs détaillés, éditer `config.py` :

```python
LOG_LEVEL = "DEBUG"  # Au lieu de "INFO"
```

Puis redémarrer le service.

## 🐛 Dépannage

### Le popup n'apparaît pas

**Symptômes** : Capture prise mais aucun popup

**Solutions** :
1. Vérifier que le mode est activé :
   ```bash
   curl http://localhost:5001/status
   ```
   Doit afficher `"watcher_running": true`

2. Vérifier les logs :
   ```bash
   python3 screenshot-capture-service/view-logs.py -n 20
   ```

3. Vérifier les permissions macOS :
   - Système Préférences → Sécurité → Accessibilité
   - Autoriser Python ou Terminal

4. Redémarrer le service :
   ```bash
   python3 screenshot-capture-service/stop-service.py
   python3 screenshot-capture-service/start-service.py
   ```

### Le service ne démarre pas

**Symptômes** : Erreur au démarrage

**Solutions** :
1. Vérifier que le port 5001 est libre :
   ```bash
   lsof -i :5001
   ```

2. Vérifier les dépendances :
   ```bash
   python3 -c "import flask, flask_cors, watchdog, psutil"
   ```

3. Vérifier les logs d'erreur :
   ```bash
   python3 screenshot-capture-service/view-logs.py -l ERROR
   ```

### Les fichiers ne sont pas sauvegardés

**Symptômes** : Popup rempli mais fichiers absents

**Solutions** :
1. Vérifier les permissions du dossier :
   ```bash
   ls -la ~/Documents/TestCaseScreenshots/
   ```

2. Vérifier l'espace disque disponible

3. Vérifier les logs pour erreurs :
   ```bash
   python3 screenshot-capture-service/view-logs.py -l ERROR
   ```

### Le watcher ne démarre pas

**Symptômes** : Mode activé mais pas de surveillance

**Solutions** :
1. Vérifier les logs du watcher :
   ```bash
   python3 screenshot-capture-service/view-logs.py -c WATCHER
   ```

2. Vérifier que le processus watcher tourne :
   ```bash
   ps aux | grep screenshot-watcher
   ```

3. Redémarrer le service

### Erreur "Address already in use"

**Symptômes** : Port 5001 déjà utilisé

**Solutions** :
1. Trouver le processus :
   ```bash
   lsof -i :5001
   ```

2. Arrêter le processus ou changer le port dans `config.py`

### Les logs ne se mettent pas à jour

**Symptômes** : Logs anciens après redémarrage

**Solutions** :
1. Vérifier que le logger a été corrigé (Phase 5)
2. Redémarrer le service proprement
3. Vérifier les permissions du fichier de log

## 📊 Monitoring

### Vérifier l'état du service

```bash
# Statut API
curl http://localhost:5001/status | python3 -m json.tool

# Processus en cours
ps aux | grep screenshot

# Logs récents
python3 screenshot-capture-service/view-logs.py -n 10
```

### Statistiques des captures

```bash
# Compter les captures
ls -1 ~/Documents/TestCaseScreenshots/*.png | wc -l

# Taille totale
du -sh ~/Documents/TestCaseScreenshots/
```

## 🔧 Configuration

### Changer le port API

Éditer `config.py` :
```python
API_PORT = 5002  # Changer de 5001
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

## 💡 Conseils et bonnes pratiques

1. **Toujours vérifier le statut** avant de prendre des captures
2. **Désactiver le mode** quand vous n'en avez plus besoin
3. **Consulter les logs** en cas de problème
4. **Nommer clairement** les captures dans le popup
5. **Organiser par test case** : utiliser le même Test Case # pour toutes les captures d'un test
6. **Sauvegarder régulièrement** : les fichiers sont locaux, pensez à les sauvegarder

## 📞 Support

En cas de problème :

1. Consulter les logs : `python3 screenshot-capture-service/view-logs.py`
2. Vérifier la section Dépannage ci-dessus
3. Exécuter les tests : `python3 screenshot-capture-service/test_all_phases.py`
4. Vérifier la documentation : [README.md](README.md) et [INSTALL.md](INSTALL.md)

## 🔗 Liens utiles

- [README.md](README.md) - Vue d'ensemble
- [INSTALL.md](INSTALL.md) - Instructions d'installation
- [SCREENSHOT_CAPTURE_PLAN.md](../docs/SCREENSHOT_CAPTURE_PLAN.md) - Plan de développement

