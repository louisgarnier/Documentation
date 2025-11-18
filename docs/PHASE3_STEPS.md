# Phase 3: React Frontend - Plan d'Implémentation Étape par Étape

## Objectif
Créer un frontend React/Next.js moderne qui se connecte à l'API backend et correspond au design de `test-case-manager/`.

## Approche
**Une étape à la fois, avec test après chaque étape.**

---

## Étape 1: Setup Next.js ⏭️

### Ce que je vais faire:
1. Initialiser le projet Next.js dans `frontend/`
2. Configurer TypeScript et Tailwind CSS
3. Installer les dépendances (axios, lucide-react)
4. Vérifier que le projet démarre

### Test proposé:
```bash
cd frontend
npm install
npm run dev
# Devrait démarrer sur http://localhost:3000
# Page par défaut Next.js devrait s'afficher
# Pas d'erreurs dans la console
```

### Validation attendue:
- [ ] Next.js projet initialisé
- [ ] TypeScript configuré
- [ ] Tailwind CSS configuré
- [ ] Serveur démarre sans erreur
- [ ] Page par défaut visible sur http://localhost:3000
- [ ] Pas d'erreurs dans la console du navigateur

**Je vais lancer les tests et vous donner les résultats avant de continuer.**

---

## Étape 2: Structure de base + API Client ⏭️

### Ce que je vais faire:
1. Créer la structure de dossiers (`src/app/`, `src/components/`, `src/api/`, `src/types/`)
2. Créer `src/api/client.ts` avec toutes les fonctions API
3. Créer `src/types/index.ts` avec les types TypeScript
4. Tester la connexion à l'API backend

### Test proposé:
```bash
# Backend doit être lancé sur port 8000
cd frontend
npm run dev

# Dans le navigateur, ouvrir la console
# Tester: fetch('http://localhost:8000/api/test-cases')
# Devrait retourner la liste des test cases
```

### Validation attendue:
- [ ] Structure de dossiers créée
- [ ] API client créé avec toutes les fonctions
- [ ] Types TypeScript définis
- [ ] Connexion à l'API fonctionne (backend doit être lancé sur port 8000)
- [ ] Test dans la console du navigateur: `fetch('http://localhost:8000/api/test-cases')` retourne des données

**Je vais lancer les tests et vous donner les résultats avant de continuer.**

---

## Étape 3: Header Component ✅

### Ce que j'ai fait:
1. ✅ Créé `src/components/Header.tsx` avec le design du test-case-manager
2. ✅ Adapté les styles Tailwind pour Next.js (dark mode support)
3. ✅ Intégré dans `app/page.tsx` (page principale)
4. ✅ Mis à jour `app/layout.tsx` avec les métadonnées

### Test proposé:
```bash
cd frontend
npm run dev
# Ouvrir http://localhost:3000 (ou le port indiqué par Next.js)
# Vérifier que le header s'affiche correctement
# Vérifier le style (sticky, backdrop blur, etc.)
```

### Validation attendue:
- [x] Header component créé (`src/components/Header.tsx`)
- [x] Page principale créée avec Header intégré
- [x] Styles Tailwind configurés (dark mode)
- [x] Layout mis à jour avec métadonnées
- [ ] **À tester**: Header s'affiche en haut de la page
- [ ] **À tester**: Style correspond au design (sticky, backdrop blur, etc.)
- [ ] **À tester**: Sticky positioning fonctionne (reste en haut au scroll)
- [ ] **À tester**: Titre et sous-titre visibles

**Note**: Le port 3000 peut être occupé par une autre app. Next.js utilisera automatiquement le port suivant (3001, 3002, etc.) ou vous pouvez spécifier un port avec `npm run dev -- -p 3001`

---

## Étape 4: Test Case List Page ✅

### Ce que j'ai fait:
1. ✅ Créé `CheckIcon.tsx` component (icône de checkbox)
2. ✅ Créé `TestCaseItem.tsx` component (card individuelle)
3. ✅ Créé `TestCaseList.tsx` component (liste avec gestion d'état vide)
4. ✅ Mis à jour `app/page.tsx` pour charger les test cases depuis l'API
5. ✅ Implémenté les checkboxes de sélection (state management)
6. ✅ Ajouté loading et error states

### Test proposé:
```bash
cd frontend
npm run dev
# Backend doit être lancé sur port 8000
# Ouvrir http://localhost:3000 (ou le port indiqué)
# Vérifier que les test cases s'affichent en cards
# Vérifier que les checkboxes fonctionnent
# Vérifier le style (hover, shadows, etc.)
```

### Validation attendue:
- [x] Composants créés (TestCaseItem, TestCaseList, CheckIcon)
- [x] Page principale mise à jour avec API integration
- [x] Checkboxes fonctionnelles (state management)
- [x] Design correspond à test-case-manager (cards, hover effects)
- [x] Loading et error states gérés
- [ ] **À tester**: Liste des test cases affichée (chargée depuis l'API)
- [ ] **À tester**: Cards avec le bon style (hover, shadows, etc.)
- [ ] **À tester**: Test cases visibles depuis la base de données
- [ ] **À tester**: Backend API accessible sur port 8000

**Note**: Pour tester, le backend doit être lancé: `cd backend && uvicorn api.main:app --reload`

---

## Étape 5: Test Case Detail Page ✅

### Ce que j'ai fait:
1. ✅ Créé `ChevronLeftIcon.tsx` component (icône pour le bouton retour)
2. ✅ Créé `TestCaseDetail.tsx` component (affichage des détails)
3. ✅ Créé la page dynamique `src/app/test-case/[id]/page.tsx`
4. ✅ Implémenté le chargement des données (test case + steps)
5. ✅ Implémenté le bouton "Back to List" avec navigation
6. ✅ Mis à jour la navigation dans la page principale (router.push)

### Test proposé:
```bash
npm run dev
# Backend doit être lancé sur port 8000
# Cliquer sur une card de test case
# Vérifier que la page de détail s'affiche
# Vérifier que les steps sont affichés
# Vérifier que le bouton "Back" fonctionne
```

### Validation attendue:
- [x] Composants créés (TestCaseDetail, ChevronLeftIcon)
- [x] Page dynamique créée avec route `/test-case/[id]`
- [x] Chargement des données (test case + steps) depuis l'API
- [x] Navigation mise à jour (router.push au lieu de window.location)
- [x] Gestion des états (loading, error)
- [x] **Testé**: Page de détail s'affiche au clic sur une card ✅
- [x] **Testé**: Détails du test case visibles (test_number, description, created_at) ✅
- [x] **Testé**: Steps affichés (liste des steps du test case) ✅
- [x] **Testé**: Bouton "Back to List" fonctionne (retour à la liste) ✅
- [x] **Testé**: URL change correctement (/test-case/[id]) ✅

**Note**: Page déplacée de `src/app/` vers `app/` (Next.js utilise `app/` à la racine)

**Je vais lancer les tests et vous donner les résultats avant de continuer.**

---

## Étape 6: Create/Edit Test Case ✅

### Ce que j'ai fait:
1. ✅ Créé `TestCaseForm.tsx` component (formulaire réutilisable)
2. ✅ Créé page `/test-case/new` pour créer un nouveau test case
3. ✅ Implémenté édition inline dans `TestCaseDetail` component
4. ✅ Connecté aux endpoints API (POST pour créer, PUT pour éditer)
5. ✅ Ajouté bouton "Create New Test Case" sur la page principale
6. ✅ Gestion des erreurs et états de chargement

### Test proposé:
```bash
npm run dev
# Backend doit être lancé sur port 8000
# Cliquer sur "Create New Test Case"
# Créer un nouveau test case
# Vérifier qu'il apparaît dans la liste
# Cliquer sur un test case et cliquer "Edit"
# Éditer le test case
# Vérifier que les changements sont sauvegardés
```

### Validation attendue:
- [x] Formulaire de création accessible (`/test-case/new`)
- [x] Création fonctionne (POST API)
- [x] Redirection vers page de détail après création
- [x] Édition inline dans page de détail
- [x] Édition fonctionne (PUT API)
- [x] Messages d'erreur/succès affichés
- [ ] **À tester**: Nouveau test case apparaît dans la liste
- [ ] **À tester**: Données persistées dans la DB (vérifier dans Streamlit)

---

## Étape 7: Steps Management ✅

### Ce que j'ai fait:
1. ✅ Créé `StepCard.tsx` component (affichage et édition d'un step)
2. ✅ Créé `AddStepForm.tsx` component (formulaire pour ajouter un step)
3. ✅ Intégré dans `TestCaseDetail` component
4. ✅ Implémenté création de step (POST API)
5. ✅ Implémenté édition de step (PUT API)
6. ✅ Implémenté suppression de step (DELETE API avec confirmation)
7. ✅ Implémenté réordonnement de steps (POST reorder API avec dropdown)
8. ✅ Gestion des champs optionnels (modules, calculation_logic, configuration)

### Test proposé:
```bash
npm run dev
# Backend doit être lancé sur port 8000
# Ouvrir un test case
# Ajouter un step avec "Add New Step"
# Éditer un step existant
# Réordonner les steps avec le dropdown
# Supprimer un step
# Vérifier que tout fonctionne
```

### Validation attendue:
- [x] Composants créés (StepCard, AddStepForm)
- [x] Formulaire pour créer un step accessible
- [x] Création de step fonctionne (POST API)
- [x] Formulaire pour éditer un step accessible (mode édition dans StepCard)
- [x] Édition de step fonctionne (PUT API)
- [x] Reordering fonctionne (POST reorder API avec dropdown)
- [x] Suppression fonctionne (DELETE API avec confirmation)
- [x] Champs optionnels gérés (modules, calculation_logic, configuration)
- [ ] **À tester**: Step apparaît dans la liste après création
- [ ] **À tester**: Données persistées dans la DB

---

## Étape 8: Screenshots Management ✅

### Ce que j'ai fait:
1. ✅ Créé `ScreenshotGallery.tsx` component (affichage des screenshots en grille)
2. ✅ Créé `ScreenshotUpload.tsx` component (upload avec drag & drop)
3. ✅ Intégré dans `StepCard` component (section screenshots en bas de chaque step)
4. ✅ Implémenté upload de screenshot (POST avec FormData)
5. ✅ Implémenté affichage des images (GET file URL)
6. ✅ Implémenté suppression de screenshot (DELETE API avec confirmation)
7. ✅ Gestion du rechargement automatique après upload/suppression
8. ✅ Validation des types de fichiers et taille (200MB max)
9. ✅ Drag & drop support

### Test proposé:
```bash
npm run dev
# Backend doit être lancé sur port 8000
# Ouvrir un test case avec des steps
# Uploader un screenshot (click ou drag & drop)
# Vérifier qu'il s'affiche dans la galerie
# Supprimer un screenshot (hover sur l'image)
# Vérifier qu'il disparaît
```

### Validation attendue:
- [x] Composants créés (ScreenshotGallery, ScreenshotUpload)
- [x] Upload de screenshot fonctionne (POST avec FormData)
- [x] Affichage des images fonctionne (GET file URL)
- [x] Images visibles dans StepCard (thumbnails 64x64px)
- [x] Modal pour afficher l'image en taille normale
- [x] Suppression fonctionne (DELETE API avec confirmation dans modal)
- [x] Drag & drop support
- [x] Validation des types de fichiers
- [x] Layout optimisé (thumbnails à gauche, upload à droite, 50% de largeur)
- [x] **Testé**: Upload fonctionne ✅
- [x] **Testé**: Affichage thumbnails fonctionne ✅
- [x] **Testé**: Modal pour voir l'image en grand ✅
- [x] **Testé**: Suppression fonctionne ✅

---

## Étape 9: Export Excel + Footer ✅

### Ce que j'ai fait:
1. ✅ Créé `Footer.tsx` component (sticky footer avec compteur et bouton Export)
2. ✅ Intégré le Footer dans la page principale (affiché uniquement si des items sont sélectionnés)
3. ✅ Implémenté l'export Excel (appel API `/api/export` avec IDs sélectionnés)
4. ✅ Géré le téléchargement automatique du fichier Excel (Blob → download link)
5. ✅ Utilisé le même format Excel que Streamlit (via `shared/excel_export.py`)

### Test proposé:
```bash
npm run dev
# Backend doit être lancé sur port 8000
# Sélectionner plusieurs test cases (checkboxes)
# Vérifier que le Footer apparaît avec le compteur
# Cliquer sur "Export to Excel"
# Vérifier que le fichier Excel se télécharge
# Ouvrir le fichier et vérifier le contenu (même format que Streamlit)
```

### Validation attendue:
- [x] Footer s'affiche quand des items sont sélectionnés ✅
- [x] Compteur de sélection correct ✅
- [x] Sélection multiple fonctionne (plusieurs checkboxes) ✅
- [x] Bouton Export visible et fonctionnel ✅
- [x] Export génère un fichier Excel (POST export API) ✅
- [x] Fichier se télécharge automatiquement ✅
- [x] **Testé**: Fichier contient les bonnes données (ouvrir dans Excel) ✅
- [x] **Testé**: Format Excel identique à celui de Streamlit ✅

---

## Étape 10: Polish & Testing ⏭️

### Ce que je vais faire:
1. Ajuster les styles pour correspondre exactement au design
2. Tester toutes les fonctionnalités
3. Vérifier la responsivité
4. Corriger les bugs éventuels
5. Mettre à jour la documentation

### Test proposé:
```bash
npm run dev
# Tester toutes les fonctionnalités end-to-end
# Vérifier sur différentes tailles d'écran
# Vérifier que tout fonctionne avec l'API
```

### Validation attendue:
- [ ] Toutes les fonctionnalités fonctionnent end-to-end
- [ ] Design correspond à test-case-manager (couleurs, spacing, typography)
- [ ] Responsive design fonctionne (mobile, tablet, desktop)
- [ ] Pas d'erreurs dans la console
- [ ] Performance acceptable
- [ ] Pas de bugs majeurs

**Je vais lancer les tests et vous donner les résultats avant de continuer.**

---

## Résumé des étapes

1. ⏭️ Setup Next.js
2. ⏭️ Structure de base + API Client
3. ⏭️ Header Component
4. ⏭️ Test Case List Page
5. ⏭️ Test Case Detail Page
6. ⏭️ Create/Edit Test Case
7. ⏭️ Steps Management
8. ✅ Screenshots Management
9. ✅ Export Excel + Footer
10. ⏭️ Polish & Testing

**Chaque étape sera testée avant de passer à la suivante.**

