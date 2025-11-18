# TODO - Séparation des Versions Streamlit et React

## Objectif

Séparer la version Streamlit originale sur une branche dédiée, en gardant uniquement la version React/Next.js sur la branche `main`.

## Situation Actuelle

- **Branche `main`** : Contient les deux versions
  - `streamlit/` - Version Streamlit originale
  - `frontend/` - Version React/Next.js
  - `backend/` - API FastAPI
  - `shared/` - Composants partagés (models, excel_export, database)

## Plan de Séparation

### Option 1: Créer une branche `streamlit-only` depuis un commit antérieur

Cette option crée une branche propre avec uniquement la version Streamlit, en remontant à un commit avant la migration React.

#### Étapes :

1. **Identifier le dernier commit avec uniquement Streamlit**
   ```bash
   git log --oneline --all | grep -i streamlit
   # Chercher le commit juste avant la restructuration (5058158)
   # Probablement autour de 4820ad6 ou avant
   ```

2. **Créer la branche `streamlit-only` depuis ce commit**
   ```bash
   git checkout -b streamlit-only <commit-hash-avant-restructuration>
   # Exemple: git checkout -b streamlit-only 4820ad6
   ```

3. **Nettoyer la branche `streamlit-only`**
   - Supprimer les dossiers `frontend/` et `backend/`
   - Garder uniquement `streamlit/`, `shared/`, et les fichiers racine nécessaires
   - Mettre à jour `README.md` pour refléter la version Streamlit uniquement

4. **Pousser la branche**
   ```bash
   git push origin streamlit-only
   ```

### Option 2: Créer une branche `streamlit-only` depuis `main` actuel

Cette option part de l'état actuel et supprime les parties React.

#### Étapes :

1. **Créer la branche depuis `main`**
   ```bash
   git checkout main
   git checkout -b streamlit-only
   ```

2. **Supprimer les dossiers React/Backend**
   ```bash
   git rm -r frontend/
   git rm -r backend/
   git rm -r test-case-manager/  # Si présent
   ```

3. **Nettoyer les fichiers de configuration**
   - Supprimer `frontend/.gitignore` si présent
   - Garder `streamlit/requirements.txt`
   - Mettre à jour `.gitignore` pour supprimer les références React

4. **Mettre à jour `README.md`**
   - Supprimer les sections sur React/Next.js
   - Garder uniquement les instructions Streamlit
   - Mettre à jour la structure du projet

5. **Mettre à jour `docs/`**
   - Déplacer ou supprimer `PHASE2_*.md`, `PHASE3_*.md`, `PHASE4_*.md`
   - Garder uniquement la documentation Streamlit
   - Créer un `README.md` dans `docs/` expliquant la séparation

6. **Commit et push**
   ```bash
   git add -A
   git commit -m "Separate Streamlit-only version: Remove React/Next.js and backend code"
   git push origin streamlit-only
   ```

### Option 3: Créer une branche `react-only` et garder Streamlit sur `main`

Cette option inverse la logique : garder Streamlit sur `main` et créer une branche pour React.

#### Étapes :

1. **Créer la branche `react-only` depuis `main`**
   ```bash
   git checkout main
   git checkout -b react-only
   ```

2. **Supprimer Streamlit de `react-only`**
   ```bash
   git rm -r streamlit/
   git rm run_streamlit.py
   ```

3. **Nettoyer `main` pour garder uniquement Streamlit**
   ```bash
   git checkout main
   git rm -r frontend/
   git rm -r backend/
   # Mettre à jour README.md, etc.
   ```

## Recommandation

**Option 2** est recommandée car :
- ✅ Part de l'état actuel (plus simple)
- ✅ Préserve l'historique Git
- ✅ Permet de garder `shared/` si nécessaire
- ✅ Plus facile à maintenir

## Structure Cible

### Branche `streamlit-only`
```
Documentation/
├── streamlit/          # Application Streamlit
│   ├── app.py
│   └── requirements.txt
├── shared/             # Composants partagés
│   ├── models.py
│   ├── excel_export.py
│   └── database/
├── uploads/            # Screenshots
├── backups/            # Database backups
├── docs/               # Documentation Streamlit
├── run_streamlit.py    # Launcher
├── app.py              # Compatibility placeholder
├── README.md           # Instructions Streamlit uniquement
└── .gitignore
```

### Branche `main` (après séparation)
```
Documentation/
├── frontend/           # Application React/Next.js
├── backend/            # API FastAPI
├── shared/             # Composants partagés
│   ├── models.py
│   ├── excel_export.py
│   └── database/
├── uploads/            # Screenshots
├── backups/            # Database backups
├── docs/               # Documentation React/Backend
├── README.md           # Instructions React/Backend
└── .gitignore
```

## Points d'Attention

### 1. Base de données partagée
- Les deux versions utilisent `shared/database/test_cases.db`
- **Décision nécessaire** : 
  - Option A : Garder la même base de données (les deux versions peuvent lire/écrire)
  - Option B : Séparer les bases de données (une par version)

### 2. Dossier `shared/`
- Contient `models.py` et `excel_export.py` utilisés par les deux versions
- **Décision nécessaire** :
  - Option A : Garder `shared/` sur les deux branches
  - Option B : Dupliquer le code dans chaque version

### 3. Dossier `uploads/`
- Contient les screenshots
- **Décision nécessaire** : Garder partagé ou séparer ?

### 4. Documentation
- `docs/PHASE2_*.md`, `PHASE3_*.md`, `PHASE4_*.md` sont spécifiques à React
- `docs/PLAN.md` et autres docs peuvent être partagés
- **Action** : Organiser la documentation par version

## Checklist de Séparation

### Avant de commencer
- [ ] Décider quelle option utiliser (1, 2, ou 3)
- [ ] Décider le sort de `shared/` (garder ou dupliquer)
- [ ] Décider le sort de la base de données (partagée ou séparée)
- [ ] Décider le sort de `uploads/` (partagé ou séparé)
- [ ] Faire un backup de la base de données
- [ ] S'assurer que tout est commité et poussé

### Pendant la séparation
- [ ] Créer la nouvelle branche
- [ ] Supprimer les fichiers/dossiers non nécessaires
- [ ] Mettre à jour `README.md`
- [ ] Mettre à jour `.gitignore`
- [ ] Organiser la documentation
- [ ] Tester que chaque version fonctionne indépendamment

### Après la séparation
- [ ] Tester la version Streamlit sur `streamlit-only`
- [ ] Tester la version React sur `main` (ou `react-only`)
- [ ] Mettre à jour la documentation principale
- [ ] Pousser les branches
- [ ] Documenter dans `README.md` principal comment choisir entre les versions

## Commandes Git de Référence

```bash
# Voir toutes les branches
git branch -a

# Créer une branche depuis un commit spécifique
git checkout -b streamlit-only <commit-hash>

# Créer une branche depuis main actuel
git checkout main
git checkout -b streamlit-only

# Supprimer un dossier
git rm -r frontend/

# Voir l'historique d'un fichier
git log --follow -- streamlit/app.py

# Comparer deux branches
git diff main..streamlit-only

# Pousser une nouvelle branche
git push origin streamlit-only
```

## Notes

- Cette séparation est **réversible** : on peut toujours merger les branches plus tard
- Les deux versions peuvent coexister sur `main` si nécessaire
- La séparation permet de :
  - Simplifier chaque version
  - Éviter la confusion
  - Faciliter la maintenance
  - Permettre des évolutions indépendantes

## Date de Création

Document créé le : 2025-01-XX (après Phase 4)
**Status** : 📝 Planification - Non implémenté

