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

## Étape 6: Create/Edit Test Case ⏭️

### Ce que je vais faire:
1. Créer un formulaire pour créer un test case
2. Créer un formulaire pour éditer un test case
3. Connecter aux endpoints API (POST, PUT)
4. Gérer les erreurs et succès

### Test proposé:
```bash
npm run dev
# Créer un nouveau test case
# Vérifier qu'il apparaît dans la liste
# Éditer un test case
# Vérifier que les changements sont sauvegardés
```

### Validation attendue:
- [ ] Formulaire de création accessible
- [ ] Création fonctionne (POST API)
- [ ] Nouveau test case apparaît dans la liste
- [ ] Formulaire d'édition accessible
- [ ] Édition fonctionne (PUT API)
- [ ] Données persistées dans la DB (vérifier dans Streamlit)
- [ ] Messages d'erreur/succès affichés

**Je vais lancer les tests et vous donner les résultats avant de continuer.**

---

## Étape 7: Steps Management ⏭️

### Ce que je vais faire:
1. Ajouter formulaire pour créer un step
2. Ajouter formulaire pour éditer un step
3. Implémenter la suppression de step
4. Implémenter le reordering de steps

### Test proposé:
```bash
npm run dev
# Ajouter un step à un test case
# Éditer un step
# Réordonner les steps
# Supprimer un step
# Vérifier que tout fonctionne
```

### Validation attendue:
- [ ] Formulaire pour créer un step accessible
- [ ] Création de step fonctionne (POST API)
- [ ] Step apparaît dans la liste
- [ ] Formulaire pour éditer un step accessible
- [ ] Édition de step fonctionne (PUT API)
- [ ] Reordering fonctionne (POST reorder API)
- [ ] Suppression fonctionne (DELETE API)
- [ ] Données persistées dans la DB

**Je vais lancer les tests et vous donner les résultats avant de continuer.**

---

## Étape 8: Screenshots Management ⏭️

### Ce que je vais faire:
1. Implémenter l'upload de screenshots
2. Afficher les screenshots dans la page de détail
3. Implémenter la suppression de screenshots
4. Gérer l'affichage des images

### Test proposé:
```bash
npm run dev
# Uploader un screenshot
# Vérifier qu'il s'affiche
# Supprimer un screenshot
# Vérifier qu'il disparaît
```

### Validation attendue:
- [ ] Upload de screenshot fonctionne (POST avec file)
- [ ] Image sauvegardée sur le serveur
- [ ] Affichage des images fonctionne (GET file)
- [ ] Images visibles dans la page de détail
- [ ] Suppression fonctionne (DELETE API)
- [ ] Image supprimée du serveur

**Je vais lancer les tests et vous donner les résultats avant de continuer.**

---

## Étape 9: Export Excel + Footer ⏭️

### Ce que je vais faire:
1. Créer `Footer.tsx` component
2. Implémenter la sélection multiple
3. Implémenter l'export Excel
4. Gérer le téléchargement du fichier

### Test proposé:
```bash
npm run dev
# Sélectionner plusieurs test cases
# Cliquer sur Export
# Vérifier que le fichier Excel se télécharge
# Ouvrir le fichier et vérifier le contenu
```

### Validation attendue:
- [ ] Footer s'affiche quand des items sont sélectionnés
- [ ] Compteur de sélection correct
- [ ] Sélection multiple fonctionne (plusieurs checkboxes)
- [ ] Bouton Export visible et fonctionnel
- [ ] Export génère un fichier Excel (POST export API)
- [ ] Fichier se télécharge automatiquement
- [ ] Fichier contient les bonnes données (ouvrir dans Excel)

**Je vais lancer les tests et vous donner les résultats avant de continuer.**

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
8. ⏭️ Screenshots Management
9. ⏭️ Export Excel + Footer
10. ⏭️ Polish & Testing

**Chaque étape sera testée avant de passer à la suivante.**

