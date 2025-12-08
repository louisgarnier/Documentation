# Guide de Test - Screenshot Capture Service

## Tests à Effectuer

### Phase 2 : Service API Flask

#### Test 1 : Démarrer le service
```bash
cd screenshot-capture-service
python3 start-service.py
```

**À vérifier :**
- [ ] Le service démarre sans erreur
- [ ] Message "Starting Screenshot Capture Service on localhost:5001" apparaît
- [ ] Le service reste actif

#### Test 2 : Health Check
Dans un autre terminal :
```bash
curl http://localhost:5001/health
```

**Résultat attendu :**
```json
{"status": "healthy", "service": "screenshot-capture-service"}
```

**À vérifier :**
- [ ] Réponse JSON correcte
- [ ] Status "healthy"

#### Test 3 : Status (avant activation)
```bash
curl http://localhost:5001/status
```

**Résultat attendu :**
```json
{"watcher_running": false, "watcher_pid": null}
```

**À vérifier :**
- [ ] `watcher_running` est `false`
- [ ] `watcher_pid` est `null`

#### Test 4 : Activer le watcher
```bash
curl -X POST http://localhost:5001/start
```

**Résultat attendu :**
```json
{"status": "started", "message": "Watcher started with PID XXXX"}
```

**À vérifier :**
- [ ] Réponse indique "started"
- [ ] Un PID est retourné
- [ ] Le processus watcher est visible dans Activity Monitor

#### Test 5 : Status (après activation)
```bash
curl http://localhost:5001/status
```

**Résultat attendu :**
```json
{"watcher_running": true, "watcher_pid": XXXX}
```

**À vérifier :**
- [ ] `watcher_running` est `true`
- [ ] `watcher_pid` correspond au processus

#### Test 6 : Désactiver le watcher
```bash
curl -X POST http://localhost:5001/stop
```

**Résultat attendu :**
```json
{"status": "stopped", "message": "Watcher stopped successfully"}
```

**À vérifier :**
- [ ] Réponse indique "stopped"
- [ ] Le processus watcher s'arrête
- [ ] Status retourne `watcher_running: false`

#### Test 7 : Arrêter le service
Dans le terminal où le service tourne, appuyer sur `Ctrl+C`

**À vérifier :**
- [ ] Le service s'arrête proprement
- [ ] Message "Service stopped by user" apparaît

---

### Phase 3 : Système de Logging

#### Test 1 : Vérifier création du fichier de log
```bash
ls -lh ~/Documents/TestCaseScreenshots/screenshot-capture.log
```

**À vérifier :**
- [ ] Le fichier de log existe
- [ ] Le fichier est créé dans le bon dossier

#### Test 2 : Vérifier format des logs
```bash
tail -5 ~/Documents/TestCaseScreenshots/screenshot-capture.log
```

**Format attendu :**
```
[2025-01-18 10:30:45] [INFO] [SERVICE] Service started on port 5001
[2025-01-18 10:31:12] [INFO] [API] Mode activated via /start endpoint
```

**À vérifier :**
- [ ] Format avec timestamp, niveau, composant, message
- [ ] Les logs sont lisibles

#### Test 3 : Tester rotation (optionnel - nécessite gros volume)
- Générer beaucoup de logs pour atteindre 10MB
- Vérifier que les fichiers de backup sont créés

---

### Phase 4 : Script de Surveillance

#### Test 1 : Démarrer le watcher manuellement
```bash
cd screenshot-capture-service
python3 screenshot-watcher.py
```

**À vérifier :**
- [ ] Le watcher démarre sans erreur
- [ ] Message "Watching directory: ~/Desktop" apparaît
- [ ] Le watcher reste actif

#### Test 2 : Faire une capture d'écran
1. Avec le watcher actif, faire Shift+Cmd+4
2. Capturer une zone de l'écran

**À vérifier :**
- [ ] Un popup apparaît pour nommer la capture
- [ ] Le popup demande un nom
- [ ] Un deuxième popup demande une description

#### Test 3 : Nommer et décrire
1. Entrer un nom (ex: "test-capture")
2. Entrer une description (ex: "Test de la fonctionnalité")

**À vérifier :**
- [ ] Les popups se ferment après validation
- [ ] Les fichiers sont sauvegardés dans `~/Documents/TestCaseScreenshots/`
- [ ] Fichier image : `test-capture.png`
- [ ] Fichier description : `test-capture.txt`
- [ ] La capture originale est supprimée du Desktop

#### Test 4 : Vérifier les logs
```bash
tail -10 ~/Documents/TestCaseScreenshots/screenshot-capture.log
```

**À vérifier :**
- [ ] Log de détection de capture
- [ ] Log d'ouverture du popup
- [ ] Log avec nom et description saisis
- [ ] Log de sauvegarde réussie

#### Test 5 : Test avec fichier dupliqué
1. Faire une autre capture avec le même nom
2. Vérifier qu'un suffixe numérique est ajouté

**À vérifier :**
- [ ] Fichier sauvegardé comme `test-capture_1.png`
- [ ] Pas d'erreur de fichier existant

---

### Tests d'Intégration

#### Test 1 : Workflow complet
1. Démarrer le service : `python3 start-service.py`
2. Activer le mode : `curl -X POST http://localhost:5001/start`
3. Faire une capture d'écran (Shift+Cmd+4)
4. Nommer et décrire dans le popup
5. Vérifier les fichiers sauvegardés
6. Désactiver le mode : `curl -X POST http://localhost:5001/stop`
7. Arrêter le service (Ctrl+C)

**À vérifier :**
- [ ] Tout le workflow fonctionne sans erreur
- [ ] Les logs montrent toutes les étapes
- [ ] Les fichiers sont correctement sauvegardés

#### Test 2 : Gestion d'erreurs
1. Essayer d'activer le watcher deux fois
2. Essayer d'arrêter le watcher quand il n'est pas actif

**À vérifier :**
- [ ] Messages d'erreur appropriés
- [ ] Pas de crash

---

## Checklist de Validation

Avant de marquer une phase comme complète :

- [ ] Tous les tests de la phase passent
- [ ] Les logs sont créés correctement
- [ ] Pas d'erreurs dans les logs
- [ ] Le comportement correspond aux attentes
- [ ] L'utilisateur a validé manuellement

---

## Notes

- Les tests doivent être effectués **manuellement** par l'utilisateur
- Documenter tout problème rencontré
- Ajuster les tests si nécessaire

