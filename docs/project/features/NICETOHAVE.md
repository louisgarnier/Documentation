# Nice to Have - Features Futures

Ce document contient les fonctionnalités qui ont été envisagées mais reportées pour une version future, ainsi que les tentatives d'implémentation et les leçons apprises.

---

## Excel Calculation Editor (Reporté)

### Contexte
Initialement, il était prévu de remplacer le champ texte libre "Calculation Logic" par un tableur Excel intégré permettant de faire des calculs et formules directement dans l'interface.

### Objectif Initial
- Remplacer le champ texte libre "Calculation Logic" par un tableur Excel intégré
- Permettre d'entrer des valeurs, formules Excel (=SUM(), =ABS(), etc.)
- Calculer automatiquement les formules
- Sauvegarder le contenu en format XLSX

### Tentatives d'Implémentation

#### Tentative 1: Bibliothèque `x-data-spreadsheet`
- **Problème rencontré** : Incompatibilité avec Next.js 16
- **Erreur** : `Unknown module type ./node_modules/x-data-spreadsheet/src/index.less`
- **Raison** : La bibliothèque utilise des fichiers `.less` qui ne sont pas supportés nativement par Next.js 16
- **Solution envisagée** : Configuration complexe avec `next-less` ou migration vers une autre bibliothèque

#### Tentative 2: Implémentation Custom
- **Approche** : Création d'un éditeur Excel custom avec HTML table et JavaScript
- **Bibliothèques utilisées** :
  - `xlsx` pour la sérialisation/désérialisation XLSX
  - HTML table avec gestion d'état React
  - Parser de formules custom
- **Fonctionnalités implémentées** :
  - ✅ Table 15x10 avec cellules éditables
  - ✅ Support des formules de base (=A1, =A1+B2, =SUM(A1:A5), =ABS(A1), etc.)
  - ✅ Calcul automatique des formules
  - ✅ Sauvegarde en format XLSX (base64)
  - ✅ Chargement depuis XLSX
  - ✅ Insertion de références de cellules par clic
- **Problèmes rencontrés** :
  - Parsing de formules complexe et fragile
  - Gestion des dépendances entre cellules difficile
  - Bugs avec les formules contenant des parenthèses
  - Expérience utilisateur pas aussi fluide qu'Excel
  - Complexité de maintenance élevée

### Décision
**Abandon de la fonctionnalité** - Remplacement par un simple textarea pour :
- ✅ Simplicité d'utilisation
- ✅ Moins de bugs potentiels
- ✅ Maintenance plus facile
- ✅ Les utilisateurs peuvent coller des screenshots ou descriptions
- ✅ Possibilité de revenir à cette fonctionnalité plus tard si nécessaire

### Code Conservé
Le composant `ExcelCalculationEditor.tsx` a été conservé dans le code mais n'est plus utilisé. Il peut servir de référence pour une implémentation future.

**Emplacement** : `frontend/src/components/ExcelCalculationEditor.tsx`

### Recommandations pour le Futur

Si cette fonctionnalité est réintroduite, considérer :

1. **Bibliothèques alternatives** :
   - `react-spreadsheet` - Plus léger, meilleure compatibilité Next.js
   - `handsontable` - Plus complet mais plus lourd
   - `react-data-grid` - Bon compromis performance/fonctionnalités

2. **Approche hybride** :
   - Garder le textarea comme option principale
   - Ajouter un bouton "Ouvrir dans Excel" qui exporte vers Excel
   - Permettre l'import depuis Excel

3. **Simplification** :
   - Limiter aux formules vraiment nécessaires
   - Utiliser une bibliothèque éprouvée plutôt qu'une implémentation custom
   - Tester intensivement avant de déployer

### Exemple de Données Attendues
```
GrossLeverageFI		#N/A
MV of all Long positions (excluding derivatives)	152 160 852,39	=J3+J4+J5+J7+J8+J10+J12+J13
ABS(MV of all Short Positions excluding derivatives)	2 123 775,62	=ABS(J9+J11+J14)
Notional value of all Derivatives	50 000 000,00	=I2+I6
NAV	150 037 076,77	=SUM(J2:J14)
GrossLeverageFI:	1,36	=(B17+B18+B19)/B20
```

Ces données peuvent être entrées dans le textarea actuel avec des descriptions ou références aux screenshots.

---

## Autres Fonctionnalités Futures

### À documenter ici au fur et à mesure...

