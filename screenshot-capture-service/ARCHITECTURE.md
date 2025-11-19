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

## 🔄 Workflow

```
┌─────────────────────────────────────────────────────────┐
│ 1. DÉMARRER LE SERVICE API                              │
│    python3 screenshot-service.py                        │
│    → Service écoute sur localhost:5001                  │
│    → Watcher = ARRÊTÉ (pas encore actif)                │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ 2. ACTIVER LE MODE CAPTURE (depuis interface web)       │
│    POST http://localhost:5001/start                     │
│    → Service démarre le Watcher                         │
│    → Watcher surveille le Desktop                       │
│    → Mode = ACTIF ✅                                     │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ 3. PRENDRE UNE CAPTURE (Shift+Cmd+4)                    │
│    → Watcher détecte la capture                         │
│    → Popup apparaît                                     │
│    → Fichiers sauvegardés                               │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ 4. DÉSACTIVER LE MODE CAPTURE                           │
│    POST http://localhost:5001/stop                      │
│    → Service arrête le Watcher                          │
│    → Watcher = ARRÊTÉ                                   │
│    → Mode = INACTIF ❌                                   │
│    → Plus de popup même si capture prise                │
└─────────────────────────────────────────────────────────┘
```

## 📋 États du système

### État 1 : Service démarré, Mode INACTIF
```
Service API : ✅ En cours d'exécution (localhost:5001)
Watcher     : ❌ Arrêté
Popup       : ❌ N'apparaîtra PAS
```

### État 2 : Service démarré, Mode ACTIF
```
Service API : ✅ En cours d'exécution (localhost:5001)
Watcher     : ✅ En cours d'exécution (surveille Desktop)
Popup       : ✅ Apparaîtra lors des captures
```

## 🚀 Démarrage

### ⚠️ IMPORTANT : Deux composants indépendants

**Service API** et **Watcher** sont deux processus séparés :

- **Service API** : Doit être démarré/arrêté **manuellement** avec les scripts
- **Watcher** : Démarre/arrête automatiquement via le bouton "Capture Mode ON/OFF"

### Étape 1 : Démarrer le Service API (une seule fois)
```bash
# Option 1 : Avec le script (recommandé)
python3 screenshot-capture-service/start-service.py

# Option 2 : En arrière-plan
python3 screenshot-capture-service/screenshot-service.py &
```

**Résultat** : Le service API tourne sur `localhost:5001`, mais le watcher est **ARRÊTÉ**.

### Arrêter le Service API (si nécessaire)
```bash
# Utiliser le script d'arrêt
python3 screenshot-capture-service/stop-service.py
```

**Note** : Le Service API tourne en continu une fois démarré. Il ne s'arrête que si vous l'arrêtez manuellement.

### Étape 2 : Activer le Mode Capture (depuis l'interface web)
- Cliquer sur le bouton "Capture Mode: OFF" dans l'interface
- Ou utiliser : `curl -X POST http://localhost:5001/start`

**Résultat** : Le watcher démarre et surveille le Desktop.

### Étape 3 : Prendre des captures
- Utiliser Shift+Cmd+4
- Le popup apparaît automatiquement

### Étape 4 : Désactiver le Mode Capture
- Cliquer sur le bouton "Capture Mode: ON" dans l'interface
- Ou utiliser : `curl -X POST http://localhost:5001/stop`

**Résultat** : Le watcher s'arrête, plus de popup.

## ⚠️ Important

### Service API vs Watcher

| Composant | Démarrage/Arrêt | Contrôle |
|-----------|----------------|----------|
| **Service API** | Manuel (scripts `start-service.py` / `stop-service.py`) | Tourne en continu une fois démarré |
| **Watcher** | Automatique (bouton "Capture Mode ON/OFF") | Démarre/arrête selon le mode |

- **Le Service API doit TOUJOURS être démarré** pour que l'interface web fonctionne
- **Le bouton "Capture Mode ON/OFF"** contrôle uniquement le Watcher, pas le Service API
- **Le Watcher démarre/arrête** selon l'activation du mode
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

**Problème** : "Capture service is not available"
- **Solution** : Démarrer le Service API (`screenshot-service.py`)

**Problème** : Popup apparaît même quand mode OFF
- **Solution** : Vérifier qu'il n'y a qu'un seul watcher, redémarrer le service

**Problème** : Plusieurs watchers qui tournent
- **Solution** : Le système nettoie automatiquement maintenant, mais on peut forcer :
  ```bash
  pkill -f screenshot-watcher
  ```

