# Test Phase 7 : Intégration Interface Web

Plan de test pour valider l'intégration du bouton "Enable/Disable Capture Mode" dans l'interface web.

## 📋 Prérequis

1. **Service démarré** :
   ```bash
   python3 screenshot-capture-service/start-service.py &
   ```

2. **Frontend démarré** :
   ```bash
   cd frontend
   npm run dev
   ```

3. **Ouvrir le navigateur** sur `http://localhost:3000`

4. **Ouvrir un test case** (ex: TC05)

## 🧪 Plan de Test

### Test 1 : Désactiver Capture Mode (si actif)

**Objectif** : Vérifier que le mode capture peut être désactivé depuis l'interface web.

**Étapes** :
1. Ouvrir une page de test case dans le navigateur
2. Vérifier l'état du bouton "Capture Mode"
3. Si le bouton affiche "Capture Mode: ON" (vert), cliquer dessus pour désactiver
4. Vérifier que le bouton passe à "Capture Mode: OFF" (gris)
5. Vérifier dans les logs du service :
   ```bash
   python3 screenshot-capture-service/view-logs.py -n 5
   ```
   - Doit contenir : `[SERVICE] Stop endpoint called`
   - Doit contenir : `[SERVICE] Mode deactivated successfully`

**Résultat attendu** :
- ✅ Bouton passe à "OFF" (gris)
- ✅ Logs montrent la désactivation
- ✅ Watcher arrêté

---

### Test 2 : Capture sans mode actif (pas de popup)

**Objectif** : Vérifier qu'une capture prise sans mode actif ne déclenche pas de popup.

**Étapes** :
1. S'assurer que "Capture Mode: OFF" est affiché
2. Prendre une capture macOS : **Shift+Cmd+4**
3. Sélectionner une zone à capturer
4. **Vérifier** : Aucun popup ne doit apparaître
5. Vérifier dans les logs :
   ```bash
   python3 screenshot-capture-service/view-logs.py -n 10
   ```
   - Ne doit **PAS** contenir de log de détection de capture
   - Ne doit **PAS** contenir : `[WATCHER] Screenshot detected`

6. Vérifier sur le Desktop :
   ```bash
   ls -lt ~/Desktop/*.png | head -1
   ```
   - La capture doit être présente sur le Desktop avec le nom par défaut macOS
   - Format : `Screenshot YYYY-MM-DD at HH.MM.SS AM/PM.png`

**Résultat attendu** :
- ✅ Pas de popup
- ✅ Pas de logs de détection
- ✅ Capture sauvegardée sur Desktop avec nom par défaut

---

### Test 3 : Activer Capture Mode depuis l'interface

**Objectif** : Vérifier que le mode capture peut être activé depuis l'interface web.

**Étapes** :
1. Dans l'interface web, cliquer sur le bouton "Capture Mode: OFF"
2. Vérifier que le bouton passe à "Capture Mode: ON" (vert)
3. Vérifier l'indicateur visuel : point vert visible
4. Vérifier le message d'information vert qui apparaît :
   - "Capture Mode Active: Take a screenshot (Shift+Cmd+4) and a popup will appear..."
5. Vérifier dans les logs :
   ```bash
   python3 screenshot-capture-service/view-logs.py -n 5
   ```
   - Doit contenir : `[SERVICE] Start endpoint called`
   - Doit contenir : `[SERVICE] Mode activated successfully`
   - Doit contenir : `[WATCHER] Starting screenshot watcher`
   - Doit contenir : `[WATCHER] Watching directory: /Users/.../Desktop`

6. Vérifier que le watcher est actif :
   ```bash
   ps aux | grep screenshot-watcher
   ```
   - Un processus `screenshot-watcher.py` doit être en cours d'exécution

**Résultat attendu** :
- ✅ Bouton passe à "ON" (vert)
- ✅ Message d'information affiché
- ✅ Logs montrent l'activation
- ✅ Watcher processus en cours d'exécution

---

### Test 4 : Capture avec mode actif (popup et traitement)

**Objectif** : Vérifier qu'une capture prise avec mode actif déclenche le popup et le traitement.

**Étapes** :
1. S'assurer que "Capture Mode: ON" est affiché (vert)
2. Prendre une capture macOS : **Shift+Cmd+4**
3. Sélectionner une zone à capturer
4. **Vérifier** : Un popup doit apparaître automatiquement
5. Dans le popup, remplir :
   - **Screenshot Name** : `test-phase7`
   - **Test Case** : `TC05` (ou le numéro du test case ouvert)
   - **Step #** : `1`
   - **Description** : `Test de la Phase 7 - Intégration Interface Web`
6. Cliquer sur "Save" dans le popup
7. Vérifier dans les logs :
   ```bash
   python3 screenshot-capture-service/view-logs.py -n 20
   ```
   - Doit contenir : `[WATCHER] File created event: ...`
   - Doit contenir : `[WATCHER] Screenshot detected: ...`
   - Doit contenir : `[WATCHER] Opening unified screenshot information dialog`
   - Doit contenir : `[WATCHER] Step 1: User input received - All fields collected`
   - Doit contenir : `[WATCHER] User input details` avec les données du popup
   - Doit contenir : `[WATCHER] Step 2: Starting file save process`
   - Doit contenir : `[WATCHER] Step 3: Files saved successfully`

8. Vérifier les fichiers créés :
   ```bash
   ls -lh ~/Documents/TestCaseScreenshots/TC05_step1_test-phase7.*
   ```
   - Doit exister : `TC05_step1_test-phase7.png` (image)
   - Doit exister : `TC05_step1_test-phase7.txt` (description)

9. Vérifier le contenu du fichier de description :
   ```bash
   cat ~/Documents/TestCaseScreenshots/TC05_step1_test-phase7.txt
   ```
   - Doit contenir : Test Case, Step #, Screenshot Name, Description

10. Vérifier que la capture n'est plus sur le Desktop :
    ```bash
    ls ~/Desktop/Screenshot*.png | grep -v "Screen Shot" || echo "No screenshots on Desktop"
    ```
    - La capture originale ne doit plus être sur le Desktop

**Résultat attendu** :
- ✅ Popup apparaît automatiquement
- ✅ Logs montrent la détection et le traitement
- ✅ Fichiers renommés et déplacés dans `~/Documents/TestCaseScreenshots/`
- ✅ Format de nommage correct : `{test_case}_step{step_number}_{screenshot_name}.png`
- ✅ Fichier de description créé avec toutes les informations
- ✅ Capture originale supprimée du Desktop

---

### Test 5 : Vérification de l'état dans l'interface

**Objectif** : Vérifier que l'interface affiche correctement l'état du service.

**Étapes** :
1. Rafraîchir la page du test case
2. Vérifier que le bouton affiche toujours "Capture Mode: ON" (si activé)
3. Vérifier que le message d'information est toujours affiché
4. Vérifier dans la console du navigateur (F12) :
   - Doit contenir : `Capture mode activated` ou `Capture mode deactivated`
   - Pas d'erreurs liées au service

**Résultat attendu** :
- ✅ État persiste après rafraîchissement
- ✅ Pas d'erreurs dans la console

---

### Test 6 : Gestion des erreurs (service non démarré)

**Objectif** : Vérifier que l'interface gère correctement l'absence du service.

**Étapes** :
1. Arrêter le service :
   ```bash
   python3 screenshot-capture-service/stop-service.py
   ```
2. Rafraîchir la page du test case
3. Vérifier que le bouton est désactivé (gris, non cliquable)
4. Vérifier qu'un message d'erreur jaune apparaît :
   - "Capture Service: Capture service is not available. Make sure the service is running on localhost:5001"
5. Vérifier dans la console du navigateur :
   - Doit contenir : `Failed to check capture service status: ...`
6. Redémarrer le service :
   ```bash
   python3 screenshot-capture-service/start-service.py &
   ```
7. Attendre quelques secondes (vérification automatique toutes les 5 secondes)
8. Vérifier que le message d'erreur disparaît
9. Vérifier que le bouton redevient cliquable

**Résultat attendu** :
- ✅ Bouton désactivé quand service indisponible
- ✅ Message d'erreur clair affiché
- ✅ Détection automatique de la récupération du service
- ✅ Bouton redevient fonctionnel automatiquement

---

## ✅ Checklist de Validation

- [ ] Test 1 : Désactivation depuis interface ✅
- [ ] Test 2 : Capture sans mode = pas de popup ✅
- [ ] Test 3 : Activation depuis interface ✅
- [ ] Test 4 : Capture avec mode = popup + traitement ✅
- [ ] Test 5 : État persiste après rafraîchissement ✅
- [ ] Test 6 : Gestion erreurs service indisponible ✅

## 📝 Notes de Test

**Date du test** : _______________

**Testeur** : _______________

**Résultats** :
- Tests réussis : ___ / 6
- Problèmes rencontrés :
  - 
  - 
  - 

**Logs à vérifier** :
```bash
# Voir tous les logs de la session
python3 screenshot-capture-service/view-logs.py -n 50

# Filtrer par composant
python3 screenshot-capture-service/view-logs.py -c SERVICE
python3 screenshot-capture-service/view-logs.py -c WATCHER
```

## 🔍 Commandes Utiles

```bash
# Vérifier le statut du service
curl http://localhost:5001/status | python3 -m json.tool

# Vérifier les processus
ps aux | grep screenshot

# Voir les fichiers créés
ls -lh ~/Documents/TestCaseScreenshots/

# Voir les captures sur Desktop
ls -lt ~/Desktop/*.png | head -5
```

