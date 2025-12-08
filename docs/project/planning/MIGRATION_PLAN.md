# Migration Plan: Streamlit to Next.js/Nuxt.js

## Overview
This document outlines the plan to migrate from Streamlit to a modern React-based frontend (Next.js or Nuxt.js) while preserving all existing work and maintaining the ability to roll back if needed.

## Repository
**Remote**: https://github.com/louisgarnier/Documentation.git

---

## Project Structure

### Recommended Structure
```
doc/
├── streamlit/                    # Streamlit version (preserved)
│   ├── app.py                   # Current Streamlit app
│   ├── models.py                # Database models (shared)
│   ├── excel_export.py          # Excel export (shared)
│   ├── requirements.txt
│   └── README.md
│
├── backend/                     # New Python API backend
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI/Flask app
│   │   ├── routes/
│   │   │   ├── test_cases.py
│   │   │   ├── steps.py
│   │   │   └── export.py
│   │   └── models.py            # Import from ../shared
│   ├── requirements.txt
│   └── README.md
│
├── frontend/                    # New React/Next.js frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.tsx
│   │   │   ├── TestCaseList.tsx
│   │   │   ├── TestCaseItem.tsx
│   │   │   ├── TestCaseDetail.tsx
│   │   │   └── Footer.tsx
│   │   ├── pages/
│   │   ├── api/                 # API client
│   │   └── types.ts
│   ├── package.json
│   └── README.md
│
├── shared/                      # Shared components (reusable)
│   ├── models.py                # Database models (from streamlit/)
│   ├── excel_export.py          # Excel export logic (from streamlit/)
│   └── database/                # Database files
│
├── docs/                        # Documentation
│   ├── PLAN.md
│   ├── V2.md
│   ├── Layout.md
│   ├── GIT_WORKFLOW.md
│   └── MIGRATION_PLAN.md        # This file
│
├── .gitignore
└── README.md                    # Main project README
```

---

## Git Branch Strategy

### Recommended Approach: Feature Branch

1. **Main branch (`main`)**:
   - Keep current Streamlit version
   - Always stable and working
   - Can roll back here anytime

2. **New branch (`feature/react-frontend`)**:
   - Develop new React frontend
   - Develop new API backend
   - Keep Streamlit code intact in `streamlit/` folder

3. **Merge strategy**:
   - When React version is ready and tested
   - Merge to `main` but keep `streamlit/` folder
   - Can switch between versions easily

### Branch Commands
```bash
# Create new branch from current main
git checkout -b feature/react-frontend

# Work on new branch
# ... development ...

# When ready, merge back to main (keeping both versions)
git checkout main
git merge feature/react-frontend
```

---

## Component Reuse Strategy

### Components to Reuse (Move to `shared/`)

1. **`models.py`**:
   - Database schema
   - CRUD operations
   - Database connection
   - **Action**: Move to `shared/models.py`
   - **Usage**: Imported by both Streamlit and API backend

2. **`excel_export.py`**:
   - Excel generation logic
   - Formatting functions
   - **Action**: Move to `shared/excel_export.py`
   - **Usage**: Called by API endpoint for export

3. **Database files**:
   - `database/test_cases.db`
   - **Action**: Keep in `shared/database/`
   - **Usage**: Shared by both versions

### Components to Keep Separate

1. **`app.py`** (Streamlit):
   - Keep in `streamlit/app.py`
   - UI logic specific to Streamlit
   - Can be deprecated later or kept as backup

2. **New API Backend**:
   - `backend/api/main.py`
   - REST API endpoints
   - Request/response handling

3. **New Frontend**:
   - `frontend/src/`
   - React components
   - UI logic

---

## Migration Steps

### Phase 1: Project Restructuring (Preserve Current Work)
1. Create new branch: `feature/react-frontend`
2. Create folder structure:
   - `streamlit/` - Move current app.py here
   - `shared/` - Move models.py and excel_export.py here
   - `backend/` - New API backend (empty for now)
   - `frontend/` - New React frontend (empty for now)
3. Update imports in Streamlit app to use `shared/`
4. Test that Streamlit still works
5. Commit and push

### Phase 2: API Backend Development
1. Create FastAPI/Flask backend in `backend/`
2. Import shared components (`models.py`, `excel_export.py`)
3. Create API endpoints:
   - GET /api/test-cases
   - GET /api/test-cases/{id}
   - POST /api/test-cases
   - PUT /api/test-cases/{id}
   - DELETE /api/test-cases/{id}
   - GET /api/test-cases/{id}/steps
   - POST /api/test-cases/{id}/steps
   - POST /api/export
4. Test API endpoints
5. Commit and push

### Phase 3: React Frontend Development
1. Initialize Next.js/Nuxt.js project in `frontend/`
2. Copy and adapt components from `test-case-manager/`
3. Create API client to call backend
4. Implement all features:
   - Test case list with cards
   - Test case detail view
   - Create/edit/delete operations
   - Excel export
5. Test frontend
6. Commit and push

### Phase 4: Integration & Testing
1. Connect frontend to backend
2. End-to-end testing
3. Performance testing
4. Bug fixes
5. Commit and push

### Phase 5: Deployment Decision
1. Option A: Replace Streamlit with React version
2. Option B: Keep both versions (Streamlit as backup)
3. Option C: Roll back to Streamlit if issues

---

## File Organization Details

### `shared/models.py`
- All database operations
- CRUD functions
- Database initialization
- **No UI dependencies**

### `shared/excel_export.py`
- Excel generation functions
- Formatting logic
- **No UI dependencies**

### `streamlit/app.py`
- Streamlit-specific UI
- Imports from `shared/`
- Can be kept as backup

### `backend/api/main.py`
- FastAPI/Flask application
- API routes
- Imports from `shared/`
- Handles HTTP requests/responses

### `frontend/src/`
- React components
- API client
- UI logic
- Calls backend API

---

## Benefits of This Structure

1. **Preservation**: Streamlit version always available
2. **Reusability**: Shared components used by both versions
3. **Flexibility**: Can switch between versions easily
4. **Traceability**: All changes tracked in Git
5. **Rollback**: Easy to revert if needed
6. **Testing**: Can test both versions side-by-side

---

## Git Workflow

### Initial Setup
```bash
# Create new branch
git checkout -b feature/react-frontend

# Create folder structure
mkdir -p streamlit shared backend frontend

# Move files
git mv app.py streamlit/
git mv models.py shared/
git mv excel_export.py shared/
git mv database/ shared/

# Update imports in streamlit/app.py
# Commit changes
git add .
git commit -m "refactor: Restructure project for React migration"
git push origin feature/react-frontend
```

### Development Workflow
```bash
# Work on backend
cd backend/
# ... develop API ...

# Work on frontend
cd frontend/
# ... develop React app ...

# Commit regularly
git add .
git commit -m "feat: Add API endpoint for test cases"
git push origin feature/react-frontend
```

### When Ready to Merge
```bash
# Test everything works
# Merge to main
git checkout main
git merge feature/react-frontend

# Keep branch for reference
# Or delete if no longer needed
git branch -d feature/react-frontend
```

---

## Rollback Plan

If React version has issues:

1. **Quick Rollback**:
   ```bash
   git checkout main
   cd streamlit/
   streamlit run app.py
   ```

2. **Keep Both Versions**:
   - Run Streamlit: `cd streamlit && streamlit run app.py`
   - Run React: `cd frontend && npm run dev`
   - Run API: `cd backend && python -m uvicorn api.main:app`

3. **Database Safety**:
   - Database in `shared/database/`
   - Both versions use same database
   - No data loss

---

## Next Steps

1. Review and approve this structure
2. Create Git branch
3. Restructure project
4. Start Phase 1

---

## Status

**Status**: 📋 Planning
**Priority**: High
**Estimated Effort**: High (but preserves existing work)

