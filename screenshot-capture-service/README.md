# Screenshot Capture Service

Service macOS pour intercepter et organiser les captures d'écran lors de la création de test cases.

## Vue d'ensemble

Ce service permet de :
- Activer un mode "test case" depuis l'interface web
- Intercepter automatiquement les captures d'écran (Shift+Cmd+4)
- Afficher un popup pour nommer et décrire la capture
- Sauvegarder les captures organisées dans un dossier dédié
- Intégrer facilement les captures dans le Test Case Manager

## Architecture

- **Service API** : API Flask légère sur `localhost:5001`
- **Watcher** : Surveille le Desktop pour nouvelles captures
- **Logging** : Système de logs complet pour traçabilité

## Installation

Voir `INSTALL.md` pour les instructions détaillées.

## Utilisation

Voir `USAGE.md` pour le guide d'utilisation.

## Structure

```
screenshot-capture-service/
├── screenshot-service.py    # API Flask
├── screenshot-watcher.py    # Surveillance Desktop
├── logger.py                # Système de logging
├── start-service.py         # Démarrage service
├── stop-service.py          # Arrêt service
├── config.py               # Configuration
└── tests/                  # Tests
```

## Status

🚧 **En développement** - Phase 1 complétée

