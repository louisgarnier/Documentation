# Phase 2: API Backend - Plan d'Implémentation Étape par Étape

## Objectif
Créer une API REST avec FastAPI qui expose les fonctionnalités de l'app Streamlit.

## Approche
**Une étape à la fois, avec test après chaque étape.**

---

## Étape 1: Setup FastAPI ⏭️

### Ce que je vais faire:
1. Créer `backend/requirements.txt` avec les dépendances FastAPI
2. Installer les dépendances
3. Vérifier l'installation

### Test proposé:
```bash
cd backend
pip install -r requirements.txt
python3 -c "import fastapi; print('FastAPI OK')"
python3 -c "import uvicorn; print('Uvicorn OK')"
```

### Validation:
- [ ] Dépendances installées sans erreur
- [ ] FastAPI et Uvicorn importables

---

## Étape 2: Structure de base + Premier endpoint minimal ⏭️

### Ce que je vais faire:
1. Créer `backend/api/__init__.py`
2. Créer `backend/api/main.py` avec FastAPI app basique
3. Ajouter CORS (pour le frontend React)
4. Créer un endpoint de test: `GET /` qui retourne `{"status": "ok"}`

### Test proposé:
```bash
# Démarrer le serveur
cd backend
python3 -m uvicorn api.main:app --reload --port 8000

# Dans un autre terminal, tester:
curl http://localhost:8000/
# Devrait retourner: {"status":"ok"}

# Ouvrir dans le navigateur:
# http://localhost:8000/docs
# Devrait afficher la documentation Swagger automatique
```

### Validation:
- [ ] Serveur démarre sans erreur
- [ ] `GET /` retourne `{"status": "ok"}`
- [ ] Documentation Swagger accessible à `/docs`

---

## Étape 3: Premier endpoint réel - GET /api/test-cases ⏭️

### Ce que je vais faire:
1. Créer `backend/api/models.py` avec modèles Pydantic
2. Créer `backend/api/routes/__init__.py`
3. Créer `backend/api/routes/test_cases.py` avec `GET /api/test-cases`
4. Importer et utiliser `shared.models.get_all_test_cases()`
5. Retourner la liste des test cases en JSON

### Test proposé:
```bash
# Serveur déjà lancé (étape 2)

# Tester l'endpoint:
curl http://localhost:8000/api/test-cases

# Devrait retourner un JSON avec la liste des test cases
# Exemple: [{"id": 1, "test_number": "TC01", "description": "...", ...}]

# Ou via Swagger UI: http://localhost:8000/docs
# Cliquer sur GET /api/test-cases → Try it out → Execute
```

### Validation:
- [ ] Endpoint retourne la liste des test cases
- [ ] Format JSON correct
- [ ] Données correspondent à la base de données

---

## Étape 4: Endpoints Test Cases complets ⏭️

### Ce que je vais faire:
1. Ajouter `GET /api/test-cases/{id}` - Détails d'un test case
2. Ajouter `POST /api/test-cases` - Créer un test case
3. Ajouter `PUT /api/test-cases/{id}` - Modifier un test case
4. Ajouter `DELETE /api/test-cases/{id}` - Supprimer un test case

### Test proposé:
```bash
# 1. GET /api/test-cases/{id}
curl http://localhost:8000/api/test-cases/1
# Devrait retourner les détails du test case 1

# 2. POST /api/test-cases
curl -X POST http://localhost:8000/api/test-cases \
  -H "Content-Type: application/json" \
  -d '{"test_number": "TC99", "description": "Test API"}'
# Devrait créer un nouveau test case et retourner ses détails

# 3. PUT /api/test-cases/{id}
curl -X PUT http://localhost:8000/api/test-cases/1 \
  -H "Content-Type: application/json" \
  -d '{"test_number": "TC01", "description": "Description modifiée"}'
# Devrait modifier le test case 1

# 4. DELETE /api/test-cases/{id}
curl -X DELETE http://localhost:8000/api/test-cases/99
# Devrait supprimer le test case 99

# Vérifier dans Streamlit que les changements sont visibles
```

### Validation:
- [ ] Tous les endpoints CRUD fonctionnent
- [ ] Les données sont persistées dans la base
- [ ] Les changements sont visibles dans l'app Streamlit (même DB)

---

## Étape 5: Endpoints Steps ⏭️

### Ce que je vais faire:
1. Créer `backend/api/routes/steps.py`
2. Ajouter `GET /api/test-cases/{id}/steps` - Liste des steps
3. Ajouter `POST /api/test-cases/{id}/steps` - Créer un step
4. Ajouter `GET /api/steps/{id}` - Détails d'un step
5. Ajouter `PUT /api/steps/{id}` - Modifier un step
6. Ajouter `DELETE /api/steps/{id}` - Supprimer un step
7. Ajouter `POST /api/steps/{id}/reorder` - Réordonner les steps

### Test proposé:
```bash
# 1. GET /api/test-cases/1/steps
curl http://localhost:8000/api/test-cases/1/steps
# Devrait retourner la liste des steps du test case 1

# 2. POST /api/test-cases/1/steps
curl -X POST http://localhost:8000/api/test-cases/1/steps \
  -H "Content-Type: application/json" \
  -d '{"step_number": 1, "description": "Nouveau step", "notes": "..."}'
# Devrait créer un nouveau step

# 3. GET /api/steps/1
curl http://localhost:8000/api/steps/1
# Devrait retourner les détails du step 1

# 4. PUT /api/steps/1
curl -X PUT http://localhost:8000/api/steps/1 \
  -H "Content-Type: application/json" \
  -d '{"description": "Description modifiée"}'
# Devrait modifier le step 1

# 5. POST /api/steps/1/reorder
curl -X POST http://localhost:8000/api/steps/1/reorder \
  -H "Content-Type: application/json" \
  -d '{"new_position": 2}'
# Devrait réordonner le step

# 6. DELETE /api/steps/1
curl -X DELETE http://localhost:8000/api/steps/1
# Devrait supprimer le step 1
```

### Validation:
- [ ] Tous les endpoints steps fonctionnent
- [ ] Les steps sont visibles dans Streamlit
- [ ] Le reordering fonctionne

---

## Étape 6: Endpoints Screenshots ⏭️

### Ce que je vais faire:
1. Créer `backend/api/routes/screenshots.py`
2. Ajouter `POST /api/steps/{id}/screenshots` - Upload screenshot
3. Ajouter `GET /api/steps/{id}/screenshots` - Liste des screenshots
4. Ajouter `DELETE /api/screenshots/{id}` - Supprimer screenshot

### Test proposé:
```bash
# 1. POST /api/steps/1/screenshots (upload)
curl -X POST http://localhost:8000/api/steps/1/screenshots \
  -F "file=@/path/to/image.png"
# Devrait uploader l'image et retourner les détails

# 2. GET /api/steps/1/screenshots
curl http://localhost:8000/api/steps/1/screenshots
# Devrait retourner la liste des screenshots

# 3. DELETE /api/screenshots/1
curl -X DELETE http://localhost:8000/api/screenshots/1
# Devrait supprimer le screenshot
```

### Validation:
- [ ] Upload fonctionne
- [ ] Images sauvegardées dans `uploads/`
- [ ] Images visibles dans Streamlit
- [ ] Suppression fonctionne

---

## Étape 7: Endpoint Export Excel ⏭️

### Ce que je vais faire:
1. Créer `backend/api/routes/export.py`
2. Ajouter `POST /api/export` - Export Excel
3. Utiliser `shared.excel_export.create_excel_export()`
4. Retourner le fichier Excel en téléchargement

### Test proposé:
```bash
# POST /api/export
curl -X POST http://localhost:8000/api/export \
  -H "Content-Type: application/json" \
  -d '{"test_case_ids": [1, 2, 3]}' \
  --output test_export.xlsx

# Vérifier que le fichier est créé
ls -lh test_export.xlsx

# Ouvrir le fichier Excel et vérifier le contenu
```

### Validation:
- [ ] Export fonctionne
- [ ] Fichier Excel généré correctement
- [ ] Contenu identique à l'export Streamlit

---

## Étape 8: Tests finaux et documentation ⏭️

### Ce que je vais faire:
1. Tester tous les endpoints ensemble
2. Vérifier la documentation Swagger
3. Mettre à jour `backend/README.md`
4. Créer un script de test simple

### Test proposé:
```bash
# Lancer tous les tests via Swagger UI
# http://localhost:8000/docs

# Ou créer un script de test automatisé
python3 backend/test_api.py
```

### Validation:
- [ ] Tous les endpoints fonctionnent
- [ ] Documentation complète
- [ ] README mis à jour

---

## Résumé des étapes

1. ⏭️ Setup FastAPI
2. ⏭️ Structure de base + Premier endpoint
3. ⏭️ GET /api/test-cases
4. ⏭️ Endpoints Test Cases complets
5. ⏭️ Endpoints Steps
6. ⏭️ Endpoints Screenshots
7. ⏭️ Endpoint Export
8. ⏭️ Tests finaux

**Chaque étape sera testée avant de passer à la suivante.**

