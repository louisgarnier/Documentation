# Changement du Dossier de Sauvegarde des Captures

## 🎯 Objectif

Modifier le dossier de sauvegarde des captures d'écran pour une meilleure accessibilité et organisation.

## 📋 Modifications Requises

### 1. Changement du Dossier de Sauvegarde du Service

**Actuel** :
- Dossier : `/Users/louisgarnier/Library/Mobile Documents/com~apple~CloudDocs/Documents/TestCaseScreenshots/`
- Utilisé par : `screenshot-watcher.py` pour sauvegarder les captures et descriptions

**Nouveau** :
- Dossier : `/Users/louisgarnier/Library/Mobile Documents/com~apple~CloudDocs/Desktop/Capture_TC/`
- Avantages :
  - Plus accessible (sur le Desktop)
  - Plus facile à trouver
  - Meilleure organisation visuelle

### 2. Dossier par Défaut dans le Sélecteur de Fichiers

**Actuel** :
- Le sélecteur de fichiers "Add Screenshot" ouvre probablement le dossier par défaut du système

**Nouveau** :
- Le sélecteur de fichiers "Add Screenshot" doit ouvrir par défaut : `/Users/louisgarnier/Library/Mobile Documents/com~apple~CloudDocs/Desktop/Capture_TC/`
- Cela permet de sélectionner facilement les captures récemment prises

## 🔧 Fichiers à Modifier

### Backend / Service

1. **`screenshot-capture-service/config.py`**
   - Modifier `SCREENSHOTS_DIR` pour pointer vers `~/Desktop/Capture_TC/`
   - Mettre à jour `LOG_FILE` si nécessaire (peut rester dans Documents ou être déplacé)

2. **`screenshot-capture-service/screenshot-watcher.py`**
   - Vérifier que le code utilise bien `config.SCREENSHOTS_DIR`
   - S'assurer que le dossier est créé automatiquement s'il n'existe pas

### Frontend

3. **`frontend/src/components/ScreenshotUpload.tsx`** (ou composant similaire)
   - Modifier le sélecteur de fichiers pour ouvrir par défaut `~/Desktop/Capture_TC/`
   - Utiliser l'API File System Access ou un input file avec le bon chemin

4. **`frontend/src/components/TestCaseDetail.tsx`** (si le sélecteur est là)
   - Vérifier où se trouve le bouton "Add Screenshot"
   - Modifier le chemin par défaut du sélecteur

## 📝 Détails Techniques

### Configuration du Dossier

**Fichier** : `screenshot-capture-service/config.py`

```python
# Ancien
SCREENSHOTS_DIR = HOME_DIR / "Documents" / "TestCaseScreenshots"

# Nouveau
SCREENSHOTS_DIR = HOME_DIR / "Desktop" / "Capture_TC"
```

**Note** : Le dossier sera créé automatiquement par `config.py` avec `SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)`

### Sélecteur de Fichiers Frontend

**Options d'implémentation** :

1. **Option A : Input file HTML avec accept**
   - Limitation : Ne peut pas définir le dossier par défaut directement
   - Solution : Utiliser un chemin relatif ou documenter le chemin

2. **Option B : API File System Access (si supportée)**
   - Permet d'ouvrir un dossier spécifique
   - Limitation : Support navigateur limité

3. **Option C : Backend endpoint pour lister les fichiers**
   - Le backend liste les fichiers du dossier
   - L'utilisateur sélectionne depuis une liste
   - Plus de contrôle mais moins natif

4. **Option D : Input file avec accept + documentation**
   - Utiliser un input file standard
   - Afficher le chemin attendu à côté du bouton
   - L'utilisateur navigue manuellement vers le dossier

**Recommandation** : Option D (simple et fonctionnelle) ou Option C (meilleure UX)

## 🧪 Tests à Effectuer

- [ ] Vérifier que le dossier `~/Desktop/Capture_TC/` est créé automatiquement
- [ ] Prendre une capture et vérifier qu'elle est sauvegardée dans le nouveau dossier
- [ ] Vérifier que le fichier `.txt` de description est aussi dans le nouveau dossier
- [ ] Tester le sélecteur de fichiers "Add Screenshot" (ouvre le bon dossier)
- [ ] Vérifier que les anciennes captures dans l'ancien dossier ne sont pas affectées
- [ ] Tester la migration (si nécessaire) des captures existantes

## ⚠️ Points d'Attention

1. **Migration des captures existantes** :
   - Les captures déjà sauvegardées restent dans l'ancien dossier
   - Pas de migration automatique nécessaire (les anciennes captures restent accessibles)
   - Documenter le changement dans les logs

2. **Logs** :
   - Le fichier de log peut rester dans `~/Documents/TestCaseScreenshots/` ou être déplacé
   - À décider selon les préférences

3. **Permissions** :
   - Vérifier que l'écriture est possible dans `~/Desktop/Capture_TC/`
   - macOS peut avoir des restrictions sur le Desktop

4. **Chemin absolu vs relatif** :
   - Utiliser `Path.home()` pour éviter les chemins hardcodés
   - S'assurer que ça fonctionne avec le chemin iCloud Drive

## 📊 Checklist d'Implémentation

- [x] Modifier `config.py` : `SCREENSHOTS_DIR` ✅
- [x] Vérifier que `screenshot-watcher.py` utilise bien `config.SCREENSHOTS_DIR` ✅
- [x] Tester la création automatique du dossier ✅
- [x] Ajouter endpoint backend pour obtenir le chemin du dossier ✅
- [x] Ajouter endpoint backend pour lister les fichiers du dossier ✅
- [x] Ajouter endpoint backend pour récupérer un fichier ✅
- [x] Modifier le composant frontend pour afficher la liste des fichiers ✅
- [x] Implémenter la sélection directe depuis la liste ✅
- [ ] Tester le workflow complet (capture → sauvegarde → sélection)
- [ ] Mettre à jour la documentation (README.md, USAGE.md)
- [x] Mettre à jour les logs si nécessaire ✅

## 🔄 Migration (Optionnel)

Si on veut migrer les captures existantes :

```python
# Script de migration (optionnel)
import shutil
from pathlib import Path

old_dir = Path.home() / "Documents" / "TestCaseScreenshots"
new_dir = Path.home() / "Desktop" / "Capture_TC"

if old_dir.exists():
    for file in old_dir.glob("*.png"):
        shutil.move(str(file), str(new_dir / file.name))
    for file in old_dir.glob("*.txt"):
        shutil.move(str(file), str(new_dir / file.name))
```

**Note** : Migration non nécessaire si on garde les deux dossiers accessibles.

## 📝 Documentation à Mettre à Jour

- [ ] `README.md` : Mettre à jour le chemin du dossier de destination
- [ ] `USAGE.md` : Mettre à jour les exemples de chemins
- [ ] `ARCHITECTURE.md` : Mettre à jour la configuration
- [ ] `config.py` : Commentaires dans le fichier

## ✅ Validation

Une fois les modifications effectuées, valider :

1. ✅ Capture sauvegardée dans `~/Desktop/Capture_TC/`
2. ✅ Description sauvegardée dans `~/Desktop/Capture_TC/`
3. ✅ Clic sur "Click or drag" → affiche la liste des fichiers de `Capture_TC/`
4. ✅ Miniatures affichées avec aperçu des images
5. ✅ Clic sur une miniature → upload direct du fichier
6. ✅ Dossier créé automatiquement si absent
7. ✅ Logs fonctionnent correctement (restent dans Documents)
8. ⏳ Documentation à jour (en cours)

## ✅ Implémentation Complétée

**Date d'implémentation** : 2025-11-19

### Fichiers Modifiés

1. **`screenshot-capture-service/config.py`**
   - `SCREENSHOTS_DIR` changé vers `~/Desktop/Capture_TC/`
   - `LOG_FILE` reste dans `~/Documents/TestCaseScreenshots/` (pour éviter d'encombrer le Desktop)
   - Création automatique des dossiers

2. **`backend/api/routes/capture_service.py`**
   - Nouvel endpoint `GET /api/capture-service/capture-directory` : retourne le chemin du dossier
   - Nouvel endpoint `GET /api/capture-service/capture-files` : liste les fichiers du dossier Capture_TC/
   - Nouvel endpoint `GET /api/capture-service/get-file` : récupère un fichier (avec vérification de sécurité)
   - Nouvel endpoint `POST /api/capture-service/open-folder` : ouvre le dossier dans Finder (macOS)

3. **`frontend/src/api/client.ts`**
   - Nouvelle fonction `getCaptureDirectory()` pour récupérer le chemin
   - Nouvelle fonction `listCaptureFiles()` pour lister les fichiers du dossier

4. **`frontend/src/components/ScreenshotUpload.tsx`**
   - **Solution principale** : Clic sur "Click or drag" → affiche directement la liste des fichiers de `Capture_TC/` dans une grille de miniatures
   - Affichage des miniatures avec aperçu des images
   - Tri par date (plus récent en premier)
   - Clic sur une miniature → upload direct du fichier
   - Drag & drop toujours disponible
   - Lien "Or select from computer" pour le sélecteur de fichiers classique (fallback)
   - Affichage du chemin du dossier

### Solution Implémentée pour Contourner la Limitation

**Problème** : Les navigateurs ne permettent pas de définir directement le dossier par défaut pour un input file HTML pour des raisons de sécurité.

**Solution** : Au lieu d'essayer d'ouvrir le sélecteur de fichiers dans un dossier spécifique, on affiche directement la liste des fichiers du dossier `Capture_TC/` dans l'interface web.

**Avantages** :
- ✅ Accès direct aux fichiers sans navigation
- ✅ Aperçu visuel avec miniatures
- ✅ Tri automatique par date (plus récent en premier)
- ✅ Upload en un clic
- ✅ Pas besoin de chercher le dossier à chaque fois

**Workflow** :
1. Utilisateur clique sur "Click or drag"
2. La liste des fichiers de `Capture_TC/` s'affiche automatiquement
3. Utilisateur clique sur une miniature
4. Le fichier est uploadé directement

