# Phase 4: Enhancements - Drag & Drop Steps + Calculation Logic Field

**Status**: ✅ **COMPLÉTÉ**

## Status: ⏭️ Planning Phase

Cette phase ajoute deux améliorations majeures à l'interface de gestion des test cases.

---

## Changement 1: Drag & Drop pour réordonner les Steps ✅

**Status**: ✅ **COMPLÉTÉ**

### Objectif
Remplacer le dropdown "Move to position" par un système de drag & drop pour réordonner les steps de manière plus intuitive.

### Comportement attendu
- Les cards de steps peuvent être glissées (drag) et déposées (drop) au-dessus ou en dessous d'autres steps
- Quand une card est déplacée, les numéros de step (Step 1, Step 2, etc.) se mettent à jour automatiquement
- L'ordre est sauvegardé via l'API de reordering existante
- Feedback visuel pendant le drag (highlight, preview de position)

### Checklist d'implémentation

#### 1.1 Recherche et sélection de la bibliothèque
- [ ] Rechercher les bibliothèques React pour drag & drop (react-beautiful-dnd, @dnd-kit, react-sortable-hoc)
- [ ] Choisir la bibliothèque la plus adaptée (recommandation: @dnd-kit pour Next.js 14+)
- [ ] Vérifier la compatibilité avec Next.js App Router et React Server Components
- [ ] **Important** : Support desktop uniquement (pas besoin de support mobile/touch si trop compliqué)
- [ ] Documenter le choix et la raison

#### 1.2 Installation et configuration
- [ ] Installer la bibliothèque choisie (`npm install @dnd-kit/core @dnd-kit/sortable @dnd-kit/utilities`)
- [ ] Configurer la bibliothèque dans le projet
- [ ] Créer un composant wrapper si nécessaire

#### 1.3 Implémentation du drag & drop
- [ ] Modifier `StepCard.tsx` pour rendre les cards draggable
- [ ] Créer un conteneur `SortableStepsList` dans `TestCaseDetail.tsx`
- [ ] Implémenter la logique de drag & drop (onDragStart, onDragEnd, onDragOver)
- [ ] Gérer la mise à jour visuelle pendant le drag (highlight, preview)

#### 1.4 Mise à jour automatique des numéros
- [ ] Détecter le changement de position après le drop
- [ ] Appeler l'API de reordering (`POST /api/steps/{id}/reorder`)
- [ ] Mettre à jour l'état local pour refléter les nouveaux numéros
- [ ] Gérer les erreurs (rollback visuel si l'API échoue)

#### 1.5 Feedback visuel
- [ ] Ajouter un style "dragging" à la card en cours de déplacement
- [ ] Ajouter un indicateur de position de drop (ligne ou zone highlight)
- [ ] Ajouter une animation de transition lors du réordonnement
- [ ] Gérer les états de chargement pendant la sauvegarde

#### 1.6 Tests
- [ ] Tester le drag & drop sur desktop (mouse) - **Priorité principale**
- [ ] Tester avec plusieurs steps (2, 5, 10+)
- [ ] Tester les cas limites (déplacer le premier, le dernier, au milieu)
- [ ] Vérifier que les numéros se mettent à jour correctement
- [ ] Vérifier que l'ordre est persisté après rechargement
- [ ] **Note** : Tests mobile/tablet non prioritaires (desktop uniquement)

---

## Changement 2: Calculation Logic Field (Simplifié) ✅

**Status**: ✅ **COMPLÉTÉ**

### Objectif
Fournir un champ texte simple pour la logique de calcul, formules ou descriptions. L'éditeur Excel complexe a été remplacé par un simple textarea pour une meilleure simplicité d'utilisation.

### Comportement attendu
- Champ texte libre (textarea) pour "Calculation Logic"
- Les utilisateurs peuvent entrer du texte, des formules, ou coller des descriptions
- Champ optionnel sur la carte de step
- Peut inclure des descriptions de screenshots ou références
- Affichage formaté dans le mode lecture

### Checklist d'implémentation

#### 2.1 Remplacement par textarea simple
- [x] Remplacer l'éditeur Excel par un simple textarea
- [x] Textarea avec 6 lignes
- [x] Texte placeholder suggérant l'utilisation
- [x] Interface propre et simple

#### 2.2 Mise à jour du composant StepCard
- [x] Supprimer la checkbox et le composant Excel editor
- [x] Utiliser un textarea standard pour calculation logic
- [x] Mettre à jour l'affichage en mode lecture

**Note** : L'éditeur Excel a été reporté. Voir `NICETOHAVE.md` pour les détails des tentatives d'implémentation.

---

## Résumé de la Phase 4

### ✅ Changement 1: Drag & Drop pour réordonner les Steps
- **Status**: ✅ **COMPLÉTÉ**
- **Implémentation**: Utilisation de `@dnd-kit` pour le drag & drop
- **Fonctionnalités**:
  - Drag & drop des steps avec handle visuel
  - Mise à jour automatique des numéros de step
  - Sauvegarde via API de reordering
  - Feedback visuel pendant le drag

### ✅ Changement 2: Calculation Logic Field (Simplifié)
- **Status**: ✅ **COMPLÉTÉ**
- **Implémentation**: Textarea simple remplaçant l'éditeur Excel complexe
- **Fonctionnalités**:
  - Champ texte libre pour calculation logic
  - Affichage formaté en mode lecture
  - Support des descriptions et références

### 📝 Notes
- L'éditeur Excel a été reporté (voir `NICETOHAVE.md`)
- Le composant `ExcelCalculationEditor.tsx` est conservé mais non utilisé

---

## Sections obsolètes (référence uniquement)

### ~~Anciennes tâches Excel Editor (ABANDONNÉES)~~
- [ ] Évaluer les options :
  - Support des formules Excel de base (=SUM(), =ABS(), =AVG(), =MAX(), =MIN())
  - Calcul automatique des formules
  - Export/Import XLSX
  - Taille fixe : 15 lignes × 10 colonnes
  - Performance acceptable
  - Compatibilité avec Next.js
- [ ] Choisir la bibliothèque la plus adaptée
- [ ] Documenter le choix et la raison

#### 2.2 Installation et configuration
- [ ] Installer la bibliothèque choisie
- [ ] Configurer la bibliothèque dans le projet
- [ ] Créer un composant wrapper `ExcelCalculationEditor.tsx`

#### 2.3 Implémentation du tableur
- [ ] Créer le composant `ExcelCalculationEditor` avec :
  - Mode édition (quand on clique "Edit" ET que la checkbox est cochée)
  - Mode lecture (affichage non-éditable quand checkbox cochée mais pas en édition)
  - Support des formules Excel de base (=SUM, =ABS, =AVG, =MAX, =MIN, opérateurs arithmétiques)
  - Calcul automatique des formules
  - Taille fixe : 15 lignes × 10 colonnes
- [ ] Ajouter une checkbox "Enable Calculation Table" dans `StepCard.tsx` (dans le formulaire d'édition)
- [ ] Afficher le tableur uniquement si la checkbox est cochée
- [ ] Remplacer le champ texte "Calculation Logic" par le tableur (conditionnel à la checkbox)
- [ ] Gérer le scroll si nécessaire pour le tableur

#### 2.4 Gestion des données
- [ ] Format de stockage : XLSX (format Excel binaire)
- [ ] Implémenter la sérialisation (tableur → XLSX)
  - Utiliser une bibliothèque pour générer le fichier XLSX (ex: `xlsx` ou `exceljs`)
  - Convertir les données du tableur en format XLSX
  - Encoder en base64 ou stocker directement
- [ ] Implémenter la désérialisation (XLSX → tableur)
  - Charger le fichier XLSX depuis la base de données
  - Parser le fichier et remplir le tableur
- [ ] Sauvegarder dans le champ `calculation_logic` de la base de données (format XLSX encodé en base64 ou stocké comme BLOB)
- [ ] Charger depuis la base de données au chargement du step
- [ ] Gérer le cas où `calculation_logic` est vide (tableur vide par défaut)

#### 2.5 Support des formules Excel
- [ ] Implémenter le support des formules de base uniquement :
  - `=SUM(range)` - Somme d'une plage (ex: =SUM(A1:A5))
  - `=ABS(value)` - Valeur absolue (ex: =ABS(A1))
  - `=AVG(range)` - Moyenne (ex: =AVG(A1:A5))
  - `=MAX(range)` - Maximum (ex: =MAX(A1:A5))
  - `=MIN(range)` - Minimum (ex: =MIN(A1:A5))
  - Opérateurs arithmétiques (+, -, *, /) - ex: =A1+B2, =A1*B2
  - Références de cellules (A1, B2, C3, etc.)
  - Références de plages (A1:B5, A1:A10, etc.)
  - Combinaisons (ex: =SUM(A1:A5)+B1, =ABS(A1)+ABS(B1))
- [ ] Gérer les erreurs de formule (#N/A, #REF!, #DIV/0!, etc.)
- [ ] Afficher les erreurs de manière claire dans les cellules
- [ ] Ne pas implémenter de formules avancées (VLOOKUP, IF, etc.) pour cette phase

#### 2.6 Interface utilisateur
- [ ] Ajouter une checkbox "Enable Calculation Table" dans le formulaire d'édition du step
- [ ] Afficher le tableur uniquement si la checkbox est cochée
- [ ] Mode édition : tableur éditable avec barre de formule (quand en mode édition ET checkbox cochée)
- [ ] Mode lecture : tableur en lecture seule (affichage formaté quand checkbox cochée mais pas en édition)
- [ ] Taille fixe : 15 lignes × 10 colonnes (avec scroll si nécessaire)
- [ ] Indicateur visuel pour les cellules avec formules (couleur différente, icône, etc.)
- [ ] Tooltip ou aide pour les formules disponibles
- [ ] Gérer l'affichage responsive (le tableur doit rester utilisable sur desktop)

#### 2.7 Tests
- [ ] Tester la création d'un tableur avec formules
- [ ] Tester le calcul automatique des formules (formules de base uniquement)
- [ ] Tester la sauvegarde et le chargement (format XLSX)
- [ ] Tester avec l'exemple fourni (GrossLeverageFI)
- [ ] Tester les erreurs de formule (#N/A, #REF!, etc.)
- [ ] Tester la checkbox (activation/désactivation du tableur)
- [ ] Tester la taille fixe (15 lignes × 10 colonnes)
- [ ] Vérifier que les données sont persistées correctement en XLSX
- [ ] **Note** : Tests responsivité non prioritaires (desktop principalement)

---

## Clarifications apportées

### Pour le Changement 1 (Drag & Drop)
- ✅ **Support mobile/touch** : Non nécessaire - Desktop/ordinateur uniquement (si trop compliqué pour tablette/mobile, on peut s'en passer)
- [ ] Animation de transition souhaitée ? (oui/non, type d'animation) - À déterminer lors de l'implémentation

### Pour le Changement 2 (Calculation Logic - Simplifié)
- ✅ **Solution simplifiée** : Textarea simple au lieu d'éditeur Excel complexe
- ✅ **Format de stockage** : Texte libre dans le champ `calculation_logic`
- ✅ **Interface** : Textarea standard avec 6 lignes, champ optionnel
- ✅ **Utilisation** : Les utilisateurs peuvent entrer du texte, formules, ou descriptions de screenshots
- ✅ **Affichage** : Formaté en mode lecture avec préservation des sauts de ligne

---

## Ordre d'implémentation recommandé

1. **Changement 1 (Drag & Drop)** - Plus simple, impact UX immédiat
2. **Changement 2 (Calculation Logic)** - ✅ Simplifié en textarea pour meilleure utilisabilité

---

## Dépendances

### Changement 1
- Bibliothèque drag & drop (à déterminer)
- API de reordering existante (déjà implémentée)

### Changement 2
- Bibliothèque tableur Excel (à déterminer)
- Parser de formules Excel (peut être inclus dans la bibliothèque)
- Format de stockage à définir

---

## Notes

- Les deux changements sont indépendants et peuvent être implémentés séparément
- Chaque changement doit être testé individuellement avant de passer au suivant
- La documentation doit être mise à jour après chaque changement

---

## Prochaines étapes

1. ✅ Création du document Phase 4
2. ✅ Révision du document par l'utilisateur
3. ✅ Clarification des questions ouvertes
4. ✅ Push sur Git
5. ✅ Implémentation du Changement 1 (Drag & Drop)
6. ✅ Tests et validation du Changement 1
7. ✅ Implémentation du Changement 2 (Calculation Logic - Simplifié)
8. ✅ Tests et validation du Changement 2
9. ✅ Documentation finale
10. ⏭️ Tests finaux et validation utilisateur
11. ⏭️ Déploiement si nécessaire

