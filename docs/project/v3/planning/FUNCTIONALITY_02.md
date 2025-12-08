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

### 1. Database Schema Updates (`shared/models.py`)
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

### 2. Backend API Updates (`backend/api/`)
- **Projects Routes** (`routes/projects.py`):
  - `GET /api/projects` - List all projects
  - `GET /api/projects/{id}` - Get project details with test cases
  - `POST /api/projects` - Create new project
  - `PUT /api/projects/{id}` - Update project
  - `DELETE /api/projects/{id}` - Delete project (with validation)
- **Test Cases Routes** (`routes/test_cases.py`):
  - Update `POST /api/test-cases` to accept `project_id`
  - Add `PUT /api/test-cases/{id}/move` - Move test case to another project
  - Add `POST /api/test-cases/{id}/duplicate` - Duplicate test case
  - Update `GET /api/test-cases` to filter by `project_id` (optional query param)

### 3. Frontend Updates (`frontend/src/`)
- **Home Page** (`app/page.tsx`):
  - Change to display projects list instead of test cases
  - Add "Create New Project" button
  - Show project cards with test case count
  - Click project to navigate to project detail page
- **Project Detail Page** (`app/project/[id]/page.tsx` - new):
  - Display all test cases in the project
  - Add "Create Test Case" button
  - Show project name/description at top
  - Add "Back to Projects" navigation
- **Project Form Component** (`components/ProjectForm.tsx` - new):
  - Form to create/edit projects
  - Fields: name (required), description (optional)
- **Test Case Actions**:
  - Add "Duplicate" button to test case cards
  - Add "Move to Project" dropdown/button
  - Update test case creation to assign to current project

### 4. Excel Export Updates (`shared/excel_export.py`)
- **Project Level Export** (enhance existing):
  - Export all test cases from a single project
  - Summary page shows project name as header
  - Test cases listed under that project
  
- **Multi-Project Export** (new):
  - Accept multiple project IDs
  - Summary page structure:
    - Project 1 section with separator line
    - Test cases from Project 1
    - Separator/divider (visual separator, e.g., blank row with border or text)
    - Project 2 section with separator line
    - Test cases from Project 2
    - Continue for all selected projects
  - Each test case sheet includes project name in title or metadata
  - Maintain existing tab structure (one tab per test case)

### 5. Migration Strategy
- Create migration script to:
  - Create `projects` table
  - Add `project_id` column to `test_cases`
  - Create a default "Unassigned" project
  - Assign all existing test cases to default project
  - Add foreign key constraint

## Benefits
- ✅ Better organization of test cases
- ✅ Logical grouping of related test cases
- ✅ Easier navigation and management
- ✅ Ability to duplicate test cases for reuse
- ✅ Flexibility to reorganize test cases between projects

## Testing Checklist

- [ ] Home page displays projects instead of test cases
- [ ] Can create a new project with name and description
- [ ] Can delete a project (with confirmation)
- [ ] Can edit project name and description
- [ ] Clicking a project shows all its test cases
- [ ] Can create test case within a project
- [ ] Test cases are automatically assigned to current project
- [ ] Can duplicate a test case within same project
- [ ] Can duplicate a test case to another project
- [ ] Can move a test case to another project
- [ ] Project shows correct count of test cases
- [ ] Deleting a project handles test cases correctly (move to default or delete)
- [ ] Migration script works correctly for existing data
- [ ] Backend API endpoints work correctly
- [ ] Frontend navigation works (home → project → test case)
- [ ] "Back to Projects" navigation works
- [ ] Project level export works (export all test cases in a project)
- [ ] Home page level export allows selecting multiple projects
- [ ] Multi-project export includes all test cases from selected projects
- [ ] Summary page shows projects one below the other with separators
- [ ] Separators clearly indicate project boundaries
- [ ] Each project section shows its test cases correctly
- [ ] Test case tabs include project identifier/name
- [ ] Excel export maintains one tab per test case structure
- [ ] Summary page clearly shows which test case belongs to which project

## Status
🚧 **Planned** - Ready for implementation

