# Architecture - Screenshot Capture Service

## 🏗️ Vue d'ensemble

Le système est composé de **2 composants principaux** qui fonctionnent ensemble :

### 1. **Service API** (`screenshot-service.py`)
- **Rôle** : API Flask qui écoute sur `localhost:5001`
- **Fonction** : Gère l'activation/désactivation du mode capture
- **Endpoints** :
  - `GET /status` : Vérifier l'état
  - `POST /start` : Activer le mode capture (démarre le watcher)
  - `POST /stop` : Désactiver le mode capture (arrête le watcher)
  - `GET /health` : Health check

### 2. **Watcher** (`screenshot-watcher.py`)
- **Rôle** : Surveille le Desktop pour détecter les nouvelles captures
- **Fonction** : Détecte les captures et affiche le popup
- **État** : Démarre/arrête selon l'activation du mode

## 🔄 Workflow (Mode Unifié)

```
┌─────────────────────────────────────────────────────────┐
│ 1. CLICKER SUR "CAPTURE MODE: OFF" (interface web)     │
│    → Service API démarre automatiquement                │
│    → Voyant: 🟡 Starting...                             │
│    → Service API prêt (voyant: 🟢 ON)                    │
│    → Watcher démarre automatiquement                     │
│    → Voyant: 🟢 ACTIVE                                  │
│    → Bouton devient "Capture Mode: ON" (vert)           │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ 2. PRENDRE UNE CAPTURE (Shift+Cmd+4)                    │
│    → Watcher détecte la capture                         │
│    → Popup apparaît                                     │
│    → Fichiers sauvegardés                               │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ 3. CLICKER SUR "CAPTURE MODE: ON" (interface web)      │
│    → Watcher s'arrête (voyant: 🔴 INACTIVE)             │
│    → Service API s'arrête (voyant: 🔴 OFF)               │
│    → Bouton devient "Capture Mode: OFF" (gris)          │
│    → Plus de popup même si capture prise                │
└─────────────────────────────────────────────────────────┘
```

## 📋 États du système (Mode Unifié)

### État 1 : Mode INACTIF (Initial)
```
Service API : ❌ Arrêté
Watcher     : ❌ Arrêté
Popup       : ❌ N'apparaîtra PAS
Bouton      : "Capture Mode: OFF" (gris)
```

### État 2 : Mode ACTIF
```
Service API : ✅ En cours d'exécution (localhost:5001)
Watcher     : ✅ En cours d'exécution (surveille Desktop)
Popup       : ✅ Apparaîtra lors des captures
Bouton      : "Capture Mode: ON" (vert)
Voyants     : 🟢 Service API: ON | 🟢 Capture Mode: ACTIVE
```

### État 3 : Démarrage en cours
```
Service API : 🟡 Démarrage en cours...
Watcher     : ❌ Arrêté (en attente)
Popup       : ❌ N'apparaîtra PAS encore
Bouton      : "Capture Mode: OFF" (gris, disabled)
Voyants     : 🟡 Service API: Starting... | 🔴 Capture Mode: INACTIVE
```

## 🚀 Démarrage (Mode Unifié)

### ⚠️ IMPORTANT : Mode Capture Unifié

**Le système fonctionne maintenant avec un seul bouton** qui contrôle Service API + Watcher :

- **Bouton "Capture Mode: OFF"** → Démarre automatiquement Service API + Watcher
- **Bouton "Capture Mode: ON"** → Arrête automatiquement Watcher + Service API

**Plus besoin de démarrer le Service API manuellement !**

### Workflow Simplifié

```
1. Ouvrir une page de test case dans l'interface web
2. Cliquer sur "Capture Mode: OFF"
   → Service API démarre automatiquement (voyant: 🟡 Starting...)
   → Service API prêt (voyant: 🟢 ON)
   → Watcher démarre (voyant: 🟢 ACTIVE)
   → Bouton devient "Capture Mode: ON" (vert)
3. Prendre des captures (Shift+Cmd+4)
   → Popup apparaît automatiquement
4. Cliquer sur "Capture Mode: ON" pour désactiver
   → Watcher s'arrête
   → Service API s'arrête
   → Bouton devient "Capture Mode: OFF" (gris)
```

### Gestion Manuelle (Optionnel)

Si vous devez gérer le service manuellement (dépannage) :

```bash
# Démarrer le service manuellement
python3 screenshot-capture-service/start-service.py

# Arrêter le service manuellement
python3 screenshot-capture-service/stop-service.py
```

## ⚠️ Important

### Service API vs Watcher (Mode Unifié)

| Composant | Démarrage/Arrêt | Contrôle |
|-----------|----------------|----------|
| **Service API** | Automatique (bouton "Capture Mode ON/OFF") | Démarre/arrête avec le mode |
| **Watcher** | Automatique (bouton "Capture Mode ON/OFF") | Démarre/arrête avec le mode |

**Nouveau comportement** :
- **Le bouton "Capture Mode ON/OFF"** contrôle **Service API + Watcher** ensemble
- **Service API ne tourne plus en continu** : seulement quand le mode est actif
- **Un seul bouton** pour tout activer/désactiver
- **Voyants visuels** pour voir l'état du Service API et du Mode Capture
- **Un seul Watcher** doit tourner à la fois (le système nettoie automatiquement)

## 🔍 Vérification

```bash
# Vérifier que le Service API tourne
curl http://localhost:5001/status

# Vérifier les processus
ps aux | grep screenshot-service  # Service API
ps aux | grep screenshot-watcher  # Watcher (seulement si mode actif)
```

## 🐛 Dépannage

**Problème** : "Capture service is not available" ou voyant "Error"
- **Solution** : 
  1. Vérifier que le backend est démarré (`cd backend && uvicorn api.main:app --reload`)
  2. Cliquer à nouveau sur "Capture Mode: OFF"
  3. Si le problème persiste, démarrer manuellement : `python3 screenshot-capture-service/start-service.py`

**Problème** : Service API reste en "Starting..." indéfiniment
- **Solution** : 
  1. Vérifier les logs : `python3 screenshot-capture-service/view-logs.py -n 20`
  2. Arrêter manuellement : `python3 screenshot-capture-service/stop-service.py`
  3. Réessayer depuis l'interface

**Problème** : Popup apparaît même quand mode OFF
- **Solution** : Vérifier qu'il n'y a qu'un seul watcher, redémarrer le service

**Problème** : Plusieurs watchers qui tournent
- **Solution** : Le système nettoie automatiquement maintenant, mais on peut forcer :
  ```bash
  pkill -f screenshot-watcher
  ```

**Problème** : Le bouton ne répond pas
- **Solution** : 
  1. Vérifier que le backend est accessible
  2. Rafraîchir la page
  3. Vérifier la console du navigateur pour les erreurs

