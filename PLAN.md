# Test Case Documentation Tool - Implementation Plan

## Repository
**Remote**: https://github.com/louisgarnier/Documentation.git

## Project Overview
Streamlit-based web application for creating and managing SimCorp Dimension test case documentation with Excel export capability.

## Tech Stack
- **Frontend/Backend**: Streamlit
- **Database**: SQLite
- **Excel Export**: openpyxl
- **File Storage**: Local filesystem (uploads/)

## Implementation Steps

### Step 1: Project Setup ✅
**Goal**: Initialize project structure and dependencies

**Tasks**:
- [ ] Create `requirements.txt` with dependencies
- [ ] Create `.gitignore`
- [ ] Create `README.md`
- [ ] Initialize git repo and connect to remote

**Validation**:
- [ ] Run `pip install -r requirements.txt` successfully
- [ ] Git remote configured correctly
- [ ] Project structure created

**Commit**: `[Setup] Initialize project structure and dependencies`

---

### Step 2: Database Schema & Models ✅
**Goal**: Define data structure for test cases and steps

**Tasks**:
- [x] Create `models.py` with SQLite database setup
- [x] Define tables: `test_cases`, `test_steps`, `step_screenshots`
- [x] Create database initialization function

**Schema**:
- `test_cases`: id, test_number, description, created_at
- `test_steps`: id, test_case_id, step_number, description, modules, calculation_logic, configuration
- `step_screenshots`: id, step_id, file_path, uploaded_at

**Additional Work Completed**:
- [x] **Comprehensive CRUD Functions**: Created full set of database operations for all entities
  - **Why**: Having all CRUD functions ready upfront allows the frontend to be built without needing to add database logic later. This follows the "backend-first" approach and ensures data layer is complete before UI development.
  - **Functions Added**:
    - Test Cases: `create_test_case()`, `get_all_test_cases()`, `get_test_case_by_id()`, `update_test_case()`, `delete_test_case()`
    - Test Steps: `create_test_step()`, `get_steps_by_test_case()`, `get_step_by_id()`, `update_test_step()`, `delete_test_step()`
    - Screenshots: `add_screenshot_to_step()`, `get_screenshots_by_step()`, `delete_screenshot()`
- [x] **Database Connection Management**: Implemented `get_db_connection()` with automatic directory creation
- [x] **Test Script**: Added `if __name__ == "__main__"` block for direct testing and validation

**Validation**:
- [x] Database file created successfully at `database/test_cases.db`
- [x] All 3 tables created with correct schema (verified via PRAGMA table_info)
- [x] Can insert and query sample data (tested with test case and step creation)
- [x] Database operations tested and working correctly
- [x] No linting errors

**Commit**: `[Backend] Add database schema and models`

---

### Step 3: Basic Streamlit UI - Test Case List ✅
**Goal**: Display existing test cases

**Tasks**:
- [x] Create `app.py` with Streamlit structure
- [x] Add sidebar navigation
- [x] Create "View Test Cases" page showing all test cases in a table
- [x] Add "Create New Test Case" button (placeholder page)

**Additional Work Completed**:
- [x] **Streamlit Version Fix**: Upgraded Streamlit from 1.3.0 to 1.51.0 to resolve protobuf compatibility issue
  - **Why**: The installed protobuf version (5.28.2) was incompatible with older Streamlit version, causing import errors
- [x] **Database Initialization**: Added cached database initialization on app startup
- [x] **Empty State Handling**: Implemented user-friendly empty state message with getting started instructions
- [x] **Page Configuration**: Set up proper Streamlit page config with title, icon, and wide layout

**Validation**:
- [x] Run `streamlit run app.py` successfully (after Streamlit upgrade)
- [x] UI displays correctly with sidebar navigation
- [x] Can see test cases list (shows empty state when no test cases exist)
- [x] Navigation between pages works correctly
- [x] Database initializes automatically on startup

**Commit**: `[Frontend] Add basic UI with test case list view`

---

### Step 4: Create Test Case Form ✅
**Goal**: Allow users to create new test cases

**Tasks**:
- [ ] Add "Create Test Case" form in Streamlit
- [ ] Form fields: Test Number, Description
- [ ] Save to database on submit
- [ ] Show success message and refresh list

**Validation**:
- [ ] Can create a new test case
- [ ] Test case appears in list after creation
- [ ] Data persists in database

**Commit**: `[Frontend] Add test case creation form`

---

### Step 5: Edit Test Case ✅
**Goal**: Allow editing existing test cases

**Tasks**:
- [ ] Add edit button for each test case in list
- [ ] Create edit form (pre-filled with existing data)
- [ ] Update database on save
- [ ] Add delete functionality

**Validation**:
- [ ] Can edit test case description/number
- [ ] Changes persist in database
- [ ] Can delete test case

**Commit**: `[Frontend] Add test case edit and delete functionality`

---

### Step 6: Add Steps to Test Case ✅
**Goal**: Allow adding steps to a test case

**Tasks**:
- [ ] Create "View Test Case Details" page
- [ ] Display steps for selected test case
- [ ] Add "Add Step" form with: step number, description
- [ ] Save step to database linked to test case

**Validation**:
- [ ] Can view test case with its steps
- [ ] Can add new step to test case
- [ ] Steps display in correct order

**Commit**: `[Frontend] Add step management for test cases`

---

### Step 7: Edit Steps & Add Metadata ✅
**Goal**: Allow editing steps and adding metadata fields

**Tasks**:
- [ ] Add edit button for each step
- [ ] Expand step form to include: modules, calculation_logic, configuration (text areas)
- [ ] Update step edit form with all fields
- [ ] Display metadata in step view

**Validation**:
- [ ] Can edit step description
- [ ] Can add/edit modules, calculation logic, configuration
- [ ] All metadata displays correctly

**Commit**: `[Frontend] Add metadata fields to steps (modules, logic, config)`

---

### Step 8: Screenshot Upload ✅
**Goal**: Attach screenshots to steps

**Tasks**:
- [ ] Create `uploads/` directory structure
- [ ] Add file uploader to step form
- [ ] Save uploaded images to `uploads/test_{id}/step_{id}/`
- [ ] Store file path in database
- [ ] Display screenshots in step view

**Validation**:
- [ ] Can upload image file
- [ ] Image saved to correct location
- [ ] Image displays in step details
- [ ] Multiple screenshots per step work

**Commit**: `[Frontend] Add screenshot upload and display functionality`

---

### Step 9: Excel Export - Basic Structure ✅
**Goal**: Create Excel export function

**Tasks**:
- [ ] Create `excel_export.py` module
- [ ] Use openpyxl to create workbook
- [ ] Create summary sheet with test case list
- [ ] Create one sheet per test case
- [ ] Add basic formatting (headers, borders)

**Validation**:
- [ ] Can generate Excel file
- [ ] Summary sheet shows all test cases
- [ ] Each test case has its own sheet
- [ ] File downloads correctly

**Commit**: `[Backend] Add Excel export functionality`

---

### Step 10: Excel Export - Complete Data ✅
**Goal**: Export all test case data to Excel

**Tasks**:
- [ ] Export test case details to each sheet
- [ ] Export steps with all metadata
- [ ] Add screenshot file paths/links to Excel
- [ ] Format Excel with proper columns and styling
- [ ] Add export button in Streamlit UI

**Validation**:
- [ ] Excel contains all test case data
- [ ] Steps are properly formatted
- [ ] Metadata (modules, logic, config) included
- [ ] Screenshot paths are correct

**Commit**: `[Backend] Complete Excel export with all data and screenshots`

---

### Step 11: UI Polish & Navigation ✅
**Goal**: Improve user experience

**Tasks**:
- [ ] Improve navigation between pages
- [ ] Add confirmation dialogs for delete actions
- [ ] Add search/filter for test cases
- [ ] Improve styling and layout
- [ ] Add page titles and headers

**Validation**:
- [ ] Navigation is intuitive
- [ ] All features accessible easily
- [ ] UI is clean and professional

**Commit**: `[Frontend] Polish UI and improve navigation`

---

### Step 12: Testing & Documentation ✅
**Goal**: Final testing and documentation

**Tasks**:
- [ ] Test all features end-to-end
- [ ] Update README.md with usage instructions
- [ ] Add comments to code
- [ ] Test Excel export with real data
- [ ] Verify all screenshots work in Excel

**Validation**:
- [ ] All features work as expected
- [ ] Documentation is complete
- [ ] Ready for use

**Commit**: `[Docs] Complete testing and update documentation`

---

## Git Workflow
Follow the workflow defined in `GIT_WORKFLOW.md`:
- Commit after each validated step
- Use format: `[Component] Description`
- Push to: `https://github.com/louisgarnier/Documentation.git`

## Next Steps
1. ✅ Review and approve this plan
2. ⏭️ Start with Step 1: Project Setup
3. ⏭️ Validate each step before moving to next
4. ⏭️ Commit after each completed step

