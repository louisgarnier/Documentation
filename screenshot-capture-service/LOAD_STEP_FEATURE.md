# Fonctionnalité "Load Step" - Auto-load de Steps depuis Capture_TC/

## 🎯 Objectif

Permettre de charger automatiquement un step dans un test case à partir de fichiers (images PNG et description texte) déjà présents dans le dossier `Capture_TC/`.

## 📋 Spécifications

### 1. Emplacement du Bouton

**Position** : Dans la page de détail d'un test case
- **À droite de** : "Capture Mode: OFF, Service API: OFF, Capture Mode: INACTIVE"
- **À gauche de** : Le bouton "Edit"

**Label** : "Load Step"

### 2. Fonctionnalité

#### 2.1 Ouverture de l'Interface

Au clic sur "Load Step" :
- Ouvrir une modal/interface de sélection similaire a "add new step"
- Afficher les fichiers disponibles dans `~/Desktop/Capture_TC/`
- Interface similaire à celle de "Add Screenshot" mais avec sélection multiple

#### 2.2 Sélection des Fichiers

**Images PNG** :
- Sélection multiple possible (checkbox ou multi-select)
- Afficher les miniatures des PNG disponibles
- Tous les PNG sélectionnés seront associés au même step

**Fichier Texte (Description)** :
- Sélection d'un seul fichier `.txt` parmi ceux disponibles dans `Capture_TC/`
- Afficher le contenu du fichier texte dans un éditeur
- Permettre la modification du texte avant sauvegarde

#### 2.3 Création du Step

**Champs automatiques** :
- **Step Number** : Automatique (prochain numéro dans le test case)
- **Description** : Contenu du fichier texte sélectionné (modifiable)

**Champs optionnels** (vides pour l'instant) :
- Modules
- Calculation Logic
- Configuration

**Screenshots** :
- Tous les PNG sélectionnés sont uploadés et associés au step

### 3. Workflow Utilisateur

1. Utilisateur clique sur "Load Step"
2. Modal s'ouvre avec la liste des fichiers de `Capture_TC/`
3. Utilisateur sélectionne un ou plusieurs PNG (miniatures avec checkboxes)
4. Utilisateur sélectionne un fichier `.txt` (description)
5. Le contenu du fichier texte s'affiche dans un éditeur
6. Utilisateur peut modifier le texte si nécessaire
7. Utilisateur clique sur "Create Step" ou "Save"
8. Le step est créé avec :
   - Le numéro suivant automatique
   - La description (texte modifié)
   - Tous les screenshots sélectionnés
9. Le step apparaît dans la liste des steps du test case

## 🔧 Implémentation Technique

### 3.1 Backend

**Nouvel endpoint** :
```
POST /api/test-cases/{test_case_id}/steps/load
```

**Request Body** :
```json
{
  "description": "string",
  "image_paths": ["path1.png", "path2.png"],
  "description_file_path": "description.txt"
}
```

**Response** :
```json
{
  "id": 123,
  "test_case_id": 1,
  "step_number": 5,
  "description": "...",
  "screenshots": [...]
}
```

**Logique** :
1. Créer le step avec le numéro suivant
2. Pour chaque image_path :
   - Lire le fichier depuis `Capture_TC/`
   - Uploader vers le système de fichiers du backend
   - Créer l'entrée screenshot dans la DB
   - Associer au step créé

### 3.2 Frontend

**Composant** : `LoadStepModal.tsx` (nouveau)

**Fonctionnalités** :
- Liste des fichiers PNG avec checkboxes
- Liste des fichiers TXT avec sélection unique
- Éditeur de texte pour la description
- Boutons : "Cancel" et "Create Step"
- Gestion des états : loading, error, success

**Intégration** :
- Ajouter le bouton "Load Step" dans `TestCaseDetail.tsx`
- Positionner à droite de "Capture Mode" et à gauche de "Edit"

### 3.3 API Client

**Nouvelle fonction** :
```typescript
loadStep: async (
  testCaseId: number,
  data: {
    description: string;
    imagePaths: string[];
    descriptionFilePath: string;
  }
): Promise<TestStep>
```

## 📊 Checklist d'Implémentation

### Phase 1 : Backend
- [ ] Créer endpoint `POST /api/test-cases/{id}/steps/load`
- [ ] Implémenter la logique de création du step
- [ ] Implémenter l'upload des images depuis `Capture_TC/`
- [ ] Tester l'endpoint avec Postman/curl

### Phase 2 : Frontend - Composant Modal
- [ ] Créer `LoadStepModal.tsx`
- [ ] Implémenter la liste des fichiers PNG avec sélection multiple
- [ ] Implémenter la liste des fichiers TXT avec sélection unique
- [ ] Implémenter l'éditeur de texte pour la description
- [ ] Ajouter les boutons Cancel/Create Step
- [ ] Gérer les états (loading, error, success)

### Phase 3 : Frontend - Intégration
- [ ] Ajouter le bouton "Load Step" dans `TestCaseDetail.tsx`
- [ ] Positionner correctement (droite de Capture Mode, gauche de Edit)
- [ ] Connecter le bouton à l'ouverture de la modal
- [ ] Implémenter le callback de rafraîchissement après création

### Phase 4 : API Client
- [ ] Ajouter fonction `loadStep()` dans `client.ts`
- [ ] Tester la connexion frontend-backend

### Phase 5 : Tests
- [ ] Tester avec un PNG
- [ ] Tester avec plusieurs PNG
- [ ] Tester avec un fichier TXT
- [ ] Tester la modification du texte
- [ ] Vérifier que le step est créé avec le bon numéro
- [ ] Vérifier que les screenshots sont bien associés
- [ ] Vérifier le rafraîchissement de la liste des steps

## ⚠️ Points d'Attention

1. **Gestion des erreurs** :
   - Fichier PNG introuvable
   - Fichier TXT introuvable
   - Erreur lors de l'upload
   - Erreur lors de la création du step

2. **Validation** :
   - Au moins un PNG doit être sélectionné
   - Un fichier TXT doit être sélectionné
   - La description ne doit pas être vide

3. **Performance** :
   - Charger les miniatures de manière optimisée
   - Limiter le nombre de fichiers affichés si nécessaire
   - Pagination si beaucoup de fichiers

4. **UX** :
   - Afficher un loader pendant la création
   - Message de succès après création
   - Fermer la modal automatiquement après succès
   - Rafraîchir la liste des steps

## 📝 Notes

- Pour l'instant, seuls les champs `step_number` et `description` sont gérés
- Les champs `modules`, `calculation_logic`, `configuration` restent vides
- Extension future possible : pré-remplir ces champs depuis le fichier TXT si format spécifique

## ✅ Validation

Une fois implémenté, valider :

1. ✅ Le bouton "Load Step" apparaît au bon endroit
2. ✅ La modal s'ouvre avec la liste des fichiers
3. ✅ Sélection multiple de PNG fonctionne
4. ✅ Sélection unique de TXT fonctionne
5. ✅ L'éditeur de texte permet la modification
6. ✅ Le step est créé avec le bon numéro
7. ✅ Tous les screenshots sont associés
8. ✅ La description est correcte
9. ✅ La liste des steps se rafraîchit automatiquement

## 🎉 Implémentation Complétée

### Fonctionnalités Implémentées

1. **Backend Endpoint** (`POST /api/test-cases/{test_case_id}/steps/load`)
   - Calcul automatique du prochain step_number
   - Lecture de la description depuis fichier texte si fourni
   - Upload et copie des images depuis Capture_TC/ vers uploads/
   - Association automatique des screenshots au step créé
   - Validation de sécurité (fichiers doivent être dans Capture_TC/)

2. **Backend Upload Endpoint** (`POST /api/capture-service/upload-file`)
   - Upload de fichiers depuis l'ordinateur vers Capture_TC/
   - Génération de noms uniques avec timestamp
   - Support images (PNG, JPG, JPEG, GIF, BMP) et fichiers texte (TXT)

3. **Frontend Modal** (`LoadStepModal.tsx`)
   - Affichage des images depuis Capture_TC/ en grille
   - Sélection multiple d'images avec checkboxes visuelles
   - Sélection de fichier texte avec chargement automatique du contenu
   - Option "Or select from computer" pour uploader depuis l'ordinateur
   - Éditeur de description avec pré-remplissage depuis fichier texte
   - Validation et gestion d'erreurs
   - Rafraîchissement automatique après upload

4. **Intégration dans TestCaseDetail**
   - Bouton "Load Step" (vert) à côté du bouton "Edit"
   - Callback de rafraîchissement automatique après création
   - Gestion d'état du modal

### Fichiers Modifiés/Créés

- `backend/api/models.py` - Ajout du modèle `LoadStepRequest`
- `backend/api/routes/steps.py` - Nouvel endpoint `load_step`
- `backend/api/routes/capture_service.py` - Nouvel endpoint `upload_file` et support fichiers texte
- `frontend/src/api/client.ts` - Ajout fonction `stepsAPI.load()`
- `frontend/src/components/LoadStepModal.tsx` - **NOUVEAU** composant modal complet
- `frontend/src/components/TestCaseDetail.tsx` - Intégration du bouton et modal

