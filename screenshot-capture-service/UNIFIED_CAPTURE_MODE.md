# Unified Capture Mode - Spécifications

## 🎯 Objectif

Simplifier l'interface utilisateur en unifiant le contrôle du Service API et du Watcher dans un seul bouton "Capture Mode".

## 📋 Architecture Proposée

### Principe : Un seul bouton contrôle tout

**Bouton "Capture Mode"** :
- **OFF** → Service API arrêté + Watcher arrêté
- **ON** → Service API démarré + Watcher démarré

### Workflow

```
État Initial : Capture Mode OFF
  ↓ [Clic sur bouton]
  → 1. Démarrer Service API (voyant: 🟡 Starting...)
  → 2. Service API prêt (voyant: 🟢 ON)
  → 3. Démarrer Watcher (voyant Capture Mode: 🟢 ACTIVE)
  → Bouton devient "Capture Mode: ON" (vert)
```

```
État Actif : Capture Mode ON
  ↓ [Clic sur bouton]
  → 1. Arrêter Watcher (voyant Capture Mode: 🔴 INACTIVE)
  → 2. Arrêter Service API (voyant: 🔴 OFF)
  → Bouton devient "Capture Mode: OFF" (gris)
```

## 🎨 Interface Utilisateur

### Composants Visuels Requis

1. **Bouton Principal "Capture Mode"**
   - Texte : "Capture Mode: OFF" (gris) ou "Capture Mode: ON" (vert)
   - Indicateur : Point vert/gris à gauche du texte
   - État désactivé : Si erreur de démarrage

2. **Voyant Service API** (à côté du bouton)
   - 🟢 "Service API: ON" (actif)
   - 🟡 "Service API: Starting..." (démarrage en cours)
   - 🔴 "Service API: OFF" (arrêté)
   - ⚠️ "Service API: Error" (erreur)

3. **Voyant Mode Capture** (sous le bouton ou à côté)
   - 🟢 "Capture Mode: ACTIVE" (popup apparaîtra)
   - 🔴 "Capture Mode: INACTIVE" (pas de popup)

### Layout Proposé

```
┌─────────────────────────────────────────────┐
│ [Back to List]                              │
│                                             │
│ [🟢 Capture Mode: ON]  [🟢 Service API: ON]│
│ [🟢 Capture Mode: ACTIVE]                  │
└─────────────────────────────────────────────┘
```

## 🔧 Implémentation Technique

### 1. Détection de l'état du Service API

**Fonction à créer** : `checkServiceStatus()`
- Vérifie `http://localhost:5001/status`
- Retourne : `{ available: boolean, status: 'on' | 'off' | 'starting' | 'error' }`

**Polling** : Vérifier toutes les 2-3 secondes quand le service est en cours de démarrage

### 2. Démarrage du Service API depuis l'interface

**Option choisie** : Appel API backend qui lance le service

**Nouveau endpoint backend** : `POST /api/capture-service/start`
- Lance `start-service.py` en arrière-plan
- Retourne : `{ success: boolean, message: string }`

**Alternative** : Appel système direct depuis le frontend (moins sécurisé)

### 3. Gestion du bouton "Capture Mode"

**Logique** :
```typescript
const handleToggleCaptureMode = async () => {
  if (captureModeActive) {
    // Désactiver : Arrêter Watcher puis Service API
    await stopWatcher();
    await stopServiceAPI();
  } else {
    // Activer : Démarrer Service API puis Watcher
    await startServiceAPI();
    await startWatcher();
  }
};
```

### 4. États et Transitions

| État | Service API | Watcher | Bouton | Voyants |
|------|-------------|---------|--------|---------|
| **Initial** | OFF | OFF | "Capture Mode: OFF" (gris) | 🔴 OFF / 🔴 INACTIVE |
| **Starting** | Starting | OFF | "Capture Mode: OFF" (gris, disabled) | 🟡 Starting... / 🔴 INACTIVE |
| **Active** | ON | ON | "Capture Mode: ON" (vert) | 🟢 ON / 🟢 ACTIVE |
| **Stopping** | ON | Stopping | "Capture Mode: ON" (vert, disabled) | 🟢 ON / 🟡 Stopping... |
| **Error** | Error | OFF | "Capture Mode: OFF" (rouge) | ⚠️ Error / 🔴 INACTIVE |

## 📝 Modifications Requises

### Backend (Nouveau)

1. **Nouveau endpoint** : `POST /api/capture-service/start`
   - Lance `start-service.py` en arrière-plan
   - Retourne le statut

2. **Nouveau endpoint** : `POST /api/capture-service/stop`
   - Arrête le service API
   - Retourne le statut

3. **Endpoint existant** : `GET /api/capture-service/status`
   - Vérifie si le service tourne
   - Retourne l'état détaillé

### Frontend

1. **TestCaseDetail.tsx**
   - Modifier `handleToggleCaptureMode()` pour gérer Service API + Watcher
   - Ajouter les voyants Service API et Mode Capture
   - Ajouter le polling pour vérifier l'état du service

2. **API Client** (`src/api/client.ts`)
   - Ajouter fonctions : `startCaptureService()`, `stopCaptureService()`, `checkCaptureServiceStatus()`

3. **Composant Voyants** (nouveau ou intégré)
   - Afficher l'état du Service API
   - Afficher l'état du Mode Capture

## 🧪 Tests

### Test 1 : Activation complète
1. Ouvrir une page de test case
2. Vérifier que les voyants affichent "OFF" et "INACTIVE"
3. Cliquer sur "Capture Mode: OFF"
4. Vérifier que :
   - Voyant Service API passe à "Starting..." puis "ON"
   - Voyant Mode Capture passe à "ACTIVE"
   - Bouton devient "Capture Mode: ON" (vert)

### Test 2 : Désactivation complète
1. Avec le mode actif
2. Cliquer sur "Capture Mode: ON"
3. Vérifier que :
   - Voyant Mode Capture passe à "INACTIVE"
   - Voyant Service API passe à "OFF"
   - Bouton devient "Capture Mode: OFF" (gris)

### Test 3 : Capture avec mode actif
1. Activer le mode
2. Prendre une capture (Shift+Cmd+4)
3. Vérifier que le popup apparaît

### Test 4 : Capture avec mode inactif
1. Désactiver le mode
2. Prendre une capture (Shift+Cmd+4)
3. Vérifier que le popup n'apparaît PAS

### Test 5 : Gestion d'erreur
1. Arrêter manuellement le service API
2. Essayer d'activer le mode
3. Vérifier que l'erreur est affichée correctement

## ⚠️ Points d'Attention

1. **Délai de démarrage** : Le Service API peut prendre 2-3 secondes à démarrer
2. **Gestion d'erreurs** : Afficher des messages clairs si le démarrage échoue
3. **Polling** : Ne pas poller en continu, seulement pendant les transitions
4. **Sécurité** : L'appel système pour démarrer le service doit être sécurisé
5. **Nettoyage** : S'assurer que le service s'arrête proprement

## 📊 Checklist d'Implémentation

- [x] Créer les endpoints backend pour start/stop/status du Service API ✅
- [x] Modifier `handleToggleCaptureMode()` pour gérer Service API + Watcher ✅
- [x] Ajouter les voyants Service API et Mode Capture dans l'interface ✅
- [x] Implémenter le polling pour vérifier l'état du service ✅
- [x] Ajouter la gestion d'erreurs ✅
- [x] Créer le script de test `test_unified_capture_mode.py` ✅
- [x] Tester tous les scénarios ✅
- [x] Mettre à jour la documentation ✅

## ✅ Implémentation Complétée

**Date d'implémentation** : 2025-11-19

### Fichiers Créés/Modifiés

#### Backend
- **`backend/api/routes/capture_service.py`** (nouveau)
  - `GET /api/capture-service/status` : Vérifie l'état du Service API
  - `POST /api/capture-service/start` : Démarre le Service API
  - `POST /api/capture-service/stop` : Arrête le Service API

- **`backend/api/main.py`** (modifié)
  - Ajout du router `capture_service`

#### Frontend
- **`frontend/src/api/client.ts`** (modifié)
  - Ajout de `getStatus()`, `startService()`, `stopService()`
  - Conservation de `start()` et `stop()` pour le Watcher

- **`frontend/src/components/TestCaseDetail.tsx`** (modifié)
  - Nouveau state : `captureServiceStatus`, `isPolling`
  - `handleToggleCaptureMode()` modifié pour gérer Service API + Watcher
  - Ajout des voyants Service API et Mode Capture
  - Polling intelligent (2s pendant démarrage, 5s normal)

#### Tests
- **`screenshot-capture-service/test_unified_capture_mode.py`** (nouveau)
  - Test interactif du workflow complet
  - 6 étapes de test avec vérifications manuelles

## 🧪 Tests Effectués

### Test 1 : Activation Complète ✅
**Scénario** : Activer le mode capture depuis l'interface
**Résultat** :
- Service API démarre (voyant passe à "Starting..." puis "ON")
- Watcher démarre (voyant Capture Mode passe à "ACTIVE")
- Bouton devient "Capture Mode: ON" (vert)

### Test 2 : Désactivation Complète ✅
**Scénario** : Désactiver le mode capture depuis l'interface
**Résultat** :
- Watcher s'arrête (voyant Capture Mode passe à "INACTIVE")
- Service API s'arrête (voyant passe à "OFF")
- Bouton devient "Capture Mode: OFF" (gris)

### Test 3 : Capture avec Mode Actif ✅
**Scénario** : Prendre une capture (Shift+Cmd+4) avec le mode actif
**Résultat** :
- Popup apparaît automatiquement
- Nom et description peuvent être saisis
- Fichiers sauvegardés correctement

### Test 4 : Capture avec Mode Inactif ✅
**Scénario** : Prendre une capture (Shift+Cmd+4) avec le mode inactif
**Résultat** :
- Popup n'apparaît PAS
- Capture sauvegardée normalement sur le Desktop

### Test 5 : Gestion d'Erreurs ✅
**Scénario** : Tentative d'activation avec erreur (service ne démarre pas)
**Résultat** :
- Message d'erreur affiché
- Voyant Service API passe à "Error"
- Interface reste utilisable

## 📝 Notes d'Implémentation

### Décisions Techniques

1. **Polling** : Polling à 2s pendant le démarrage, 5s en mode normal
2. **Timeout** : 10 tentatives maximum (10 secondes) pour le démarrage du service
3. **Ordre d'arrêt** : Watcher d'abord, puis Service API (pour éviter les erreurs)
4. **Ordre de démarrage** : Service API d'abord, puis Watcher (dépendance)

### Améliorations Futures Possibles

1. **LaunchAgent macOS** : Démarrage automatique au login (optionnel)
2. **Notifications** : Notifications système pour les erreurs
3. **Retry automatique** : Retry automatique en cas d'échec de démarrage
4. **Statistiques** : Afficher le nombre de captures prises dans la session

## 🔄 Workflow Final

```
┌─────────────────────────────────────────────────────────┐
│ État Initial : Capture Mode OFF                        │
│ - Service API: OFF                                     │
│ - Watcher: OFF                                         │
│ - Bouton: "Capture Mode: OFF" (gris)                   │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼ [Clic sur bouton]
┌─────────────────────────────────────────────────────────┐
│ Démarrage : Service API Starting...                    │
│ - Service API: 🟡 Starting...                          │
│ - Watcher: OFF                                         │
│ - Bouton: disabled                                      │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼ [Polling 2s]
┌─────────────────────────────────────────────────────────┐
│ Service Prêt : Démarrage Watcher                       │
│ - Service API: 🟢 ON                                    │
│ - Watcher: 🟡 Starting...                               │
│ - Bouton: "Capture Mode: OFF" (gris)                   │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ Mode Actif : Capture Mode ON                           │
│ - Service API: 🟢 ON                                    │
│ - Watcher: 🟢 ACTIVE                                   │
│ - Bouton: "Capture Mode: ON" (vert)                    │
│ - Popup apparaîtra lors des captures                   │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼ [Clic sur bouton]
┌─────────────────────────────────────────────────────────┐
│ Arrêt : Désactivation                                  │
│ - Watcher: 🔴 INACTIVE                                  │
│ - Service API: 🔴 OFF                                   │
│ - Bouton: "Capture Mode: OFF" (gris)                   │
│ - Plus de popup                                         │
└─────────────────────────────────────────────────────────┘
```

