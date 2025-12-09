# Functionality 2: Projects Organization

## Overview
Add a project layer to organize test cases. The home page will display projects instead of test cases directly. Each project can contain one or multiple test cases, providing better organization and management.

## Current Behavior

### Home Page
- Displays all test cases directly
- No grouping or organization layer
- Test cases are shown in a flat list

### Test Case Management
- Test cases exist independently
- No way to group related test cases together
- No way to duplicate or move test cases between groups

## New Behavior

### Home Page Changes
- **Display Projects** instead of test cases directly
- Each project shows:
  - Project name
  - Number of test cases in the project
  - Optionally: project description or metadata
- Click on a project to view its test cases

### Project Management
- **Create Project**: Add new projects with name and optional description
- **Delete Project**: Remove projects (with confirmation)
- **Edit Project**: Update project name/description
- **View Project**: Click to see all test cases within that project

### Test Case Management within Projects
- When viewing a project, see all test cases in that project
- **Create Test Case**: Add new test cases to the current project
- **Duplicate Test Case**: Copy a test case (within same project or to another project)
- **Move Test Case**: Transfer test case to another project
- **Delete Test Case**: Remove test case from project

### Export Functionality
- **Project Level Export** (existing):
  - Export all test cases within a project
  - Summary page shows test cases from that project
  - Each test case in separate tab
  
- **Home Page Level Export** (new):
  - Select multiple projects to export
  - Export includes all test cases from selected projects
  - **Summary Page Format**:
    - Projects displayed one below the other
    - Separator/divider between each project section
    - Each project section shows its test cases
    - Clear indication of which project each test case belongs to
  - **Test Case Tabs**:
    - Each test case still in separate tab (as currently)
    - Test case tabs include project name/identifier for clarity

## Implementation Details

### Step 1: Database Schema Updates (`shared/models.py`) ✅
- Create `projects` table:
  - `id` (primary key)
  - `name` (required)
  - `description` (optional)
  - `created_at`
  - `updated_at`
- Update `test_cases` table:
  - Add `project_id` (foreign key to projects table)
  - Make it nullable initially (for migration)
  - Add index on `project_id`
- Migration: Create default "Unassigned" project and assign existing test cases

### Step 2: Backend API - Projects Routes (`backend/api/routes/projects.py`) ✅
- `GET /api/projects` - List all projects
- `GET /api/projects/{id}` - Get project details with test cases
- `GET /api/projects/{id}/test-cases` - Get test cases in project
- `POST /api/projects` - Create new project
- `PUT /api/projects/{id}` - Update project
- `DELETE /api/projects/{id}` - Delete project (with validation)

### Step 3: Backend API - Test Cases Updates (`backend/api/routes/test_cases.py`) ✅
- Update `POST /api/test-cases` to accept `project_id`
- Add `PUT /api/test-cases/{id}/move` - Move test case to another project
- Add `POST /api/test-cases/{id}/duplicate` - Duplicate test case
- Update `GET /api/test-cases` to filter by `project_id` (optional query param)
- Update `PUT /api/test-cases/{id}` to accept `project_id`

### Step 4: Frontend - Types & API Client (`frontend/src/`) ✅
- Add Project type to `types/index.ts`
- Add projects API functions to `api/client.ts`
- Update TestCase type to include project_id
- Update CreateTestCaseRequest and UpdateTestCaseRequest to include project_id
- Add MoveTestCaseRequest and DuplicateTestCaseRequest types
- Update testCasesAPI.getAll to support project_id filtering
- Add testCasesAPI.move and testCasesAPI.duplicate methods

### Step 5: Frontend - Home Page (`frontend/src/app/page.tsx`) ✅
- Change to display projects list instead of test cases
- Add "Create New Project" button
- Show project cards with test case count
- Click project to navigate to project detail page
- Created ProjectItem component for project cards
- Updated Header to show "Create New Project" button

### Step 6: Frontend - Project Detail Page (`frontend/app/project/[id]/page.tsx`) ✅
- Display all test cases in the project
- Add "Create Test Case" button
- Show project name/description at top
- Add "Back to Projects" navigation
- Uses existing TestCaseList component
- Fetches project details and test cases via API

### Step 7: Frontend - Project Components ✅
- Create `components/ProjectForm.tsx` - Form to create/edit projects
- Add "Duplicate" button to test case cards
- Add "Move to Project" dropdown/button
- Update test case creation to assign to current project
- Created project creation page at `app/project/new/page.tsx`
- Added edit/delete functionality to project detail page
- Updated TestCaseItem to show duplicate and move buttons
- Updated test case creation to accept project_id from query params
- **FIXED**: Duplicate function now generates unique test numbers
- **FIXED**: Database connection handling improved (single connection, proper cleanup)

### Step 8: Excel Export Updates (`shared/excel_export.py`) ⏳
- **Project Level Export** (enhance existing):
  - Export all test cases from a single project
  - Summary page shows project name as header
  - Test cases listed under that project
  
- **Multi-Project Export** (new):
  - Accept multiple project IDs
  - Summary page structure:
    - Project 1 section with separator line
    - Test cases from Project 1
    - Separator/divider (visual separator)
    - Project 2 section with separator line
    - Test cases from Project 2
    - Continue for all selected projects
  - Each test case sheet includes project name in title or metadata
  - Maintain existing tab structure (one tab per test case)

## Benefits
- ✅ Better organization of test cases
- ✅ Logical grouping of related test cases
- ✅ Easier navigation and management
- ✅ Ability to duplicate test cases for reuse
- ✅ Flexibility to reorganize test cases between projects

## Testing Checklist

### Step 1: Database Schema ✅
- [x] Database schema updated (projects table created)
- [x] project_id column added to test_cases table
- [x] Migration script works correctly for existing data
- [x] Default "Unassigned" project created
- [x] Existing test cases assigned to default project
- [x] Project functions work (create, get, update, delete)
- [x] Test case functions support project_id
- [x] Move test case function works
- [x] Duplicate test case function works

### Step 2: Backend API - Projects Routes ✅
- [x] GET /api/projects - List all projects
- [x] GET /api/projects/{id} - Get project details with test cases
- [x] GET /api/projects/{id}/test-cases - Get test cases in project
- [x] POST /api/projects - Create project
- [x] PUT /api/projects/{id} - Update project
- [x] DELETE /api/projects/{id} - Delete project (with validation)
- [x] Projects router included in main.py
- [x] Project models added to api/models.py
- [x] Test suite created and passing (6/6 tests)

### Step 3: Backend API - Test Cases Updates ✅
- [x] POST /api/test-cases accepts project_id
- [x] GET /api/test-cases filters by project_id (optional query param)
- [x] PUT /api/test-cases/{id} accepts project_id
- [x] PUT /api/test-cases/{id}/move - Move test case to another project
- [x] POST /api/test-cases/{id}/duplicate - Duplicate test case
- [x] TestCaseCreate, TestCaseUpdate, TestCaseResponse models updated
- [x] TestCaseMoveRequest and TestCaseDuplicateRequest models created
- [x] Test suite created and passing (6/6 tests)

### Step 4: Frontend - Types & API Client ✅
- [x] Project type added to types/index.ts
- [x] Projects API functions added to api/client.ts
- [x] TestCase type updated to include project_id
- [x] CreateTestCaseRequest and UpdateTestCaseRequest updated to include project_id
- [x] MoveTestCaseRequest and DuplicateTestCaseRequest types added
- [x] testCasesAPI.getAll updated to support project_id filtering
- [x] testCasesAPI.move and testCasesAPI.duplicate methods added

### Step 5: Frontend - Home Page ✅
- [x] Home page displays projects instead of test cases
- [x] "Create New Project" button works
- [x] Project cards show test case count
- [x] Clicking project navigates to project detail page
- [x] Created ProjectItem component
- [x] Updated Header component
- [x] Added loading and error states

**Testing Checklist for Step 5 (Home Page = Projects View):**
- [x] Start frontend: `cd frontend && npm run dev`
- [x] Open http://localhost:3000 in browser
- [x] **Verify the home page now shows PROJECTS (not test cases)**
- [x] Verify you see at least one project: "Unassigned" (created during migration)
- [x] Verify projects are displayed in a grid layout (1 column mobile, 2 tablet, 3 desktop)
- [x] Verify each project card shows:
  - Project name (e.g., "Unassigned")
  - Test case count badge (e.g., "5 test cases")
  - Description (if available)
  - Created date
- [x] Verify "Create New Project" button appears in header and main content
- [x] Verify clicking a project card tries to navigate to `/project/[id]` (will show 404 until Step 6 is done - this is expected)
- [x] Verify loading state appears briefly when fetching projects
- [ ] Test error state: stop backend → should show error message with retry button (optional)
- [ ] Verify empty state: if no projects exist, shows message with "Create New Project" button (optional)

**What you should see:**
- **Home page**: List of projects (currently shows "Unassigned" project with 5 test cases)
- **NOT test cases** - those will appear in Step 6 when you click into a project
- The old home page view (test cases list) will become the project detail page in Step 6

**Status:** ✅ Step 5 tested and working!

### Step 6: Frontend - Project Detail Page ✅
- [x] Project detail page displays all test cases in project
- [x] "Create Test Case" button works
- [x] Project name/description displayed at top
- [x] "Back to Projects" navigation works
- [x] Created project detail page at `app/project/[id]/page.tsx`
- [x] Integrated with existing TestCaseList component
- [x] Loading and error states implemented
- [x] **Tested and verified** - Test cases visible under "Unassigned" project

### Step 7: Frontend - Project Components ✅
- [x] ProjectForm component created and works
- [x] Can create a new project with name and description
- [x] Can edit project name and description
- [x] Can delete a project (with confirmation)
- [x] "Duplicate" button on test case cards works
- [x] "Move to Project" dropdown/button works
- [x] Test cases are automatically assigned to current project
- [x] **FIXED**: Duplicate generates unique test numbers (was causing UNIQUE constraint errors)
- [x] **FIXED**: Database connection handling in duplicate/move functions (was causing "database is locked" errors)
- [x] **FIXED**: Removed hardcoded "Unassigned" option from move dropdown (was confusing)
- [x] **FIXED**: Added validation to prevent moving to non-existent projects
- [x] **FIXED**: Added auto-refresh of projects list (every 5 seconds and on move menu open)
- [x] Created project creation page
- [x] Added edit/delete UI to project detail page
- [x] **Tested and verified**: Duplicate and move work without errors

### Step 8: Excel Export Updates ⏳
- [ ] Project level export works (export all test cases in a project)
- [ ] Home page level export allows selecting multiple projects
- [ ] Multi-project export includes all test cases from selected projects
- [ ] Summary page shows projects one below the other with separators
- [ ] Separators clearly indicate project boundaries
- [ ] Each project section shows its test cases correctly
- [ ] Test case tabs include project identifier/name
- [ ] Excel export maintains one tab per test case structure
- [ ] Summary page clearly shows which test case belongs to which project

## Implementation Progress

### ✅ Step 1: Database Schema (Complete)
- Projects table created
- project_id column added to test_cases
- Migration logic implemented
- Default "Unassigned" project created
- All project functions implemented
- Test suite created and passing (9/9 tests)

### ✅ Step 2: Backend API - Projects Routes (Complete)
- Created projects routes file
- Implemented all project endpoints
- Added project models
- Test suite created and passing (6/6 tests)

### ✅ Step 3: Backend API - Test Cases Updates (Complete)
- Updated test cases routes
- Added move/duplicate endpoints
- Updated models to support project_id
- Test suite created and passing (6/6 tests)

### ⏳ Step 4: Frontend - Types & API Client
- Add Project type
- Add projects API functions

### ⏳ Step 5: Frontend - Home Page
- Display projects instead of test cases

### ⏳ Step 6: Frontend - Project Detail Page
- Create project detail view

### ⏳ Step 7: Frontend - Project Components
- Create project forms and components

### ⏳ Step 8: Excel Export Updates
- Multi-project export functionality

## Status
🚧 **In Progress** - Step 1 complete ✅, Step 2 complete ✅, Step 3 complete ✅, Step 4 complete ✅, Step 5 complete ✅, Step 6 complete ✅, Step 7 complete ✅, Step 8 next 🚧
