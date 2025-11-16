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
- [x] Create `requirements.txt` with dependencies
- [x] Create `.gitignore`
- [x] Create `README.md`
- [x] Initialize git repo and connect to remote

**Validation**:
- [x] Run `pip install -r requirements.txt` successfully
- [x] Git remote configured correctly
- [x] Project structure created

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
- [x] Add "Create Test Case" form in Streamlit
- [x] Form fields: Test Number, Description
- [x] Save to database on submit
- [x] Show success message and refresh list

**Additional Work Completed**:
- [x] **Form Validation**: Added client-side validation for required fields with clear error messages
- [x] **Duplicate Prevention**: Implemented error handling for duplicate test case numbers with user-friendly messages
- [x] **User Experience**: Added form auto-clear on successful submission, success animations (balloons), and helpful tips
- [x] **Form Design**: Used Streamlit form component with proper styling, placeholders, and help text

**Validation**:
- [x] Can create a new test case with valid data
- [x] Test case appears in list after creation (verified by user)
- [x] Data persists in database correctly
- [x] Form validation works (empty fields, duplicate numbers)
- [x] Success messages and user feedback working

**Commit**: `[Frontend] Add test case creation form`

---

### Step 5: Edit Test Case ✅
**Goal**: Allow editing existing test cases

**Tasks**:
- [x] Add edit button for each test case in list
- [x] Create edit form (pre-filled with existing data)
- [x] Update database on save
- [x] Add delete functionality

**Additional Work Completed**:
- [x] **Navigation Enhancement**: Implemented automatic page navigation when clicking "Edit Selected" button
  - **Why**: Improves user experience by automatically switching to edit page instead of requiring manual navigation
  - **Implementation**: Added session state management for page routing with force navigation flag
- [x] **Delete Confirmation**: Added confirmation dialog before deletion to prevent accidental deletions
- [x] **Dual Edit Access**: Users can edit from View Test Cases page or directly from Edit Test Case page
- [x] **Form Validation**: Added validation for edit form with duplicate number checking

**Validation**:
- [x] Can edit test case description/number (verified by user)
- [x] Changes persist in database correctly
- [x] Can delete test case with confirmation
- [x] Navigation automatically switches to edit page when "Edit Selected" is clicked (verified by user)
- [x] Edit form pre-fills with existing data correctly

**Commit**: `[Frontend] Add test case edit and delete functionality`

---

### Step 6: Add Steps to Test Case ✅
**Goal**: Allow adding steps to a test case

**Tasks**:
- [x] Create "View Test Case Details" page
- [x] Display steps for selected test case
- [x] Add "Add Step" form with: step number, description
- [x] Save step to database linked to test case

**Additional Work Completed**:
- [x] **Step Display**: Steps displayed in expandable sections showing all metadata fields
- [x] **Auto-numbering**: Step number auto-suggests next available number
- [x] **Duplicate Prevention**: Validation to prevent duplicate step numbers
- [x] **Test Data**: Created TC04 test case with 7 steps for testing purposes

**Validation**:
- [x] Can view test case with its steps (verified with TC04)
- [x] Can add new step to test case
- [x] Steps display in correct order by step number
- [x] Step form validation works correctly

**Commit**: `[Frontend] Add step management for test cases`

---

### Step 7: Edit Steps & Add Metadata ✅
**Goal**: Allow editing steps and adding metadata fields

**Tasks**:
- [x] Add edit button for each step
- [x] Expand step form to include: modules, calculation_logic, configuration (text areas)
- [x] Update step edit form with all fields
- [x] Display metadata in step view

**Validation**:
- [x] Can edit step description
- [x] Can add/edit modules, calculation logic, configuration
- [x] All metadata displays correctly

**Commit**: `[Frontend] Add metadata fields to steps (modules, logic, config)`

---

### Step 8: Screenshot Upload ✅
**Goal**: Attach screenshots to steps

**Tasks**:
- [x] Create `uploads/` directory structure
- [x] Add file uploader to step form
- [x] Save uploaded images to `uploads/test_{id}/step_{id}/`
- [x] Store file path in database
- [x] Display screenshots in step view

**Validation**:
- [x] Can upload image file
- [x] Image saved to correct location
- [x] Image displays in step details
- [x] Multiple screenshots per step work

**Commit**: `[Frontend] Add screenshot upload and display functionality`

---

### Step 9: Excel Export - Basic Structure ✅
**Goal**: Create Excel export function

**Tasks**:
- [x] Create `excel_export.py` module
- [x] Use openpyxl to create workbook
- [x] Create summary sheet with test case list
- [x] Create one sheet per test case
- [x] Add basic formatting (headers, borders)

**Validation**:
- [x] Can generate Excel file
- [x] Summary sheet shows all test cases
- [x] Each test case has its own sheet
- [x] File downloads correctly

**Commit**: `[Backend] Add Excel export functionality`

---

### Step 10: Excel Export - Complete Data ✅
**Goal**: Export all test case data to Excel

**Tasks**:
- [x] Export test case details to each sheet
- [x] Export steps with all metadata
- [x] Add screenshot file paths/links to Excel (embedded as images)
- [x] Format Excel with proper columns and styling
- [x] Add export button in Streamlit UI

**Validation**:
- [x] Excel contains all test case data
- [x] Steps are properly formatted
- [x] Metadata (modules, logic, config) included
- [x] Screenshots embedded as images in Excel

**Commit**: `[Backend] Complete Excel export with all data and screenshots`

---

### Step 10.5: Selective Excel Export ✅
**Goal**: Allow users to select which test cases to export

**Tasks**:
- [x] Add "Export" column with checkboxes to "All Test Cases" table
- [x] Track selected test cases in session state
- [x] Modify Excel export function to accept list of test case IDs
- [x] Update export button to only export selected test cases
- [ ] Add "Select All" / "Deselect All" functionality (optional)

**Validation**:
- [x] Checkboxes appear in "All Test Cases" table
- [x] Can select/deselect individual test cases
- [x] Export only includes selected test cases
- [x] Excel file contains only selected test cases

**Commit**: `[Frontend] Add selective export with checkboxes for test cases`

---

### Step 11: UI Polish & Navigation ✅
**Goal**: Improve user experience

**Tasks**:
- [x] Improve navigation between pages
- [x] Add confirmation dialogs for delete actions
- [ ] Add search/filter for test cases
- [x] Improve styling and layout
- [x] Add page titles and headers
- [x] Add unsaved changes warning when navigating away
- [x] Add full-size screenshot viewing
- [x] Add auto-suggestion for test numbers

**Validation**:
- [x] Navigation is intuitive
- [x] All features accessible easily
- [x] UI is clean and professional

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

