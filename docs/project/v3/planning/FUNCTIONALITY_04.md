# Functionality 4: Test Case Reordering within Projects

## Overview

Add drag-and-drop functionality to reorder test cases within a project, similar to the existing step reordering feature. This allows users to organize test cases in their preferred order within each project.

## Current Behavior

- Test cases are displayed in the order they were created (by `created_at` timestamp)
- No way to change the order of test cases within a project
- Order is fixed and cannot be customized

## New Behavior

### Project Detail Page
- Test case cards can be dragged and dropped to reorder them
- Visual feedback during drag (opacity change, drag handle indicator)
- Order is saved automatically when dropped
- Test cases maintain their custom order within the project
- Order is project-specific (each project has its own test case order)

### Visual Indicators
- Drag handle icon/area on each test case card
- Visual feedback when dragging (card becomes semi-transparent)
- Drop zone indicator when hovering over valid drop targets
- Loading state during reorder operation

## Implementation Details

### Step 1: Database Schema Update ✅
- [x] Add `display_order` column to `test_cases` table
  - Type: INTEGER
  - Default: NULL (or auto-increment based on creation order)
  - Migration: Add column to existing table
  - Set initial values: assign order based on current `created_at` or `id`

### Step 2: Backend API Updates ✅
- [x] Update `TestCaseResponse` model to include `display_order` field
- [x] Update `get_all_test_cases` to order by `display_order` (with fallback to `created_at`)
- [x] Create `reorder_test_cases` function in `shared/models.py`
  - Similar to `reorder_steps` function
  - Takes project_id and list of test case IDs in desired order
  - Updates `display_order` for each test case
- [x] Add endpoint `POST /api/projects/{project_id}/test-cases/reorder`
  - Accepts list of test case IDs in new order
  - Updates display_order for all test cases in the project

### Step 3: Frontend Types & API Client ✅
- [x] Update `TestCase` interface to include `display_order?: number | null`
- [x] Add `reorderTestCases` method to `projectsAPI` or `testCasesAPI`
  - Takes project_id and array of test case IDs in new order

### Step 4: Frontend - Sortable Test Case Component ✅
- [x] Create `SortableTestCaseItem.tsx` component (similar to `SortableStepCard.tsx`)
  - Wrap existing `TestCaseItem` with drag-and-drop functionality
  - Use `@dnd-kit/sortable` (already installed)
  - Add drag handle visual indicator (vertical dots ⋮)
  - Handle drag state (opacity, cursor changes)

### Step 5: Frontend - Project Detail Page Integration ✅
- [x] Update `TestCaseList` component to use `DndContext` and `SortableContext`
  - Similar to how `TestCaseDetail` handles step reordering
  - Wrap test case items in sortable context
- [x] Implement `handleDragEnd` function
  - Calculate new order based on drag position
  - Call API to reorder test cases
  - Update local state optimistically
  - Handle errors and rollback if needed
- [x] Add loading state during reorder operation
- [x] Ensure test cases are displayed in `display_order` (with fallback)
- [x] Add `handleReorderTestCases` function in project detail page

### Step 6: Initial Order Assignment (Migration) ✅
- [x] Migration script to set initial `display_order` for all existing test cases
  - Sets display_order based on created_at, grouped by project_id
- [x] Ensure new test cases get appropriate `display_order` when created
  - New test cases get next display_order in their project

## Testing Checklist

### Step 1: Database Schema
- [ ] Run database initialization
- [ ] Verify `display_order` column exists in `test_cases` table
- [ ] Verify existing test cases have `display_order` values (or NULL)
- [ ] Test creating new test case (should get appropriate display_order)

### Step 2: Backend API
- [ ] Test reordering test cases via API endpoint
- [ ] Test with test cases in same project
- [ ] Test with test cases in different projects (should not affect each other)
- [ ] Test getting test cases ordered by display_order
- [ ] Test edge cases (single test case, empty project, etc.)

### Step 3: Frontend - Drag and Drop
- [ ] Start frontend and backend
- [ ] Navigate to a project detail page with multiple test cases
- [ ] Verify drag handle appears on test case cards
- [ ] Test dragging a test case up (move earlier in list)
- [ ] Test dragging a test case down (move later in list)
- [ ] Verify visual feedback during drag (opacity, cursor)
- [ ] Verify order persists after page refresh
- [ ] Test reordering multiple times
- [ ] Test error handling (stop backend, try to reorder)

### Step 4: Cross-Project Isolation
- [ ] Create test cases in Project A and Project B
- [ ] Reorder test cases in Project A
- [ ] Verify Project B's test case order is unchanged
- [ ] Verify each project maintains its own order

### Step 5: New Test Case Creation
- [ ] Create a new test case in a project
- [ ] Verify it appears at the end (or appropriate position)
- [ ] Verify it can be reordered like existing test cases

### Integration Tests
- [ ] Reorder test cases → refresh page → verify order persists
- [ ] Reorder test cases → navigate away → come back → verify order
- [ ] Reorder test cases → export to Excel → verify order in export (if applicable)
- [ ] Test with projects that have many test cases (10+)
- [ ] Test rapid reordering (multiple drags in quick succession)

## Technical Notes

### Similar to Step Reordering
- Uses same `@dnd-kit` library (already installed)
- Similar pattern: `DndContext` → `SortableContext` → `SortableTestCaseItem`
- Backend function similar to `reorder_steps` but for test cases
- Order is project-scoped (unlike steps which are test-case-scoped)

### Order Management
- `display_order` is an integer (1, 2, 3, ...)
- When reordering, reassign all display_order values sequentially
- Use temporary values during update to avoid unique constraint issues (similar to step reordering)
- NULL values should be treated as "unset" and ordered by `created_at` as fallback

### Performance Considerations
- Reordering updates all test cases in the project (similar to step reordering)
- For projects with many test cases, consider batching or optimization
- Frontend should update optimistically for better UX

## Benefits

- **Custom Organization**: Users can organize test cases in their preferred order
- **Intuitive Interface**: Drag-and-drop is familiar and easy to use
- **Project-Specific**: Each project maintains its own test case order
- **Consistent UX**: Same interaction pattern as step reordering

## Status
✅ **Implemented** - All steps complete, ready for testing

