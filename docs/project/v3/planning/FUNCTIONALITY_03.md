# Functionality 3: Test Case Pass/Fail Status

## Overview

Add a pass/fail status toggle for each test case that can be set and updated from multiple locations in the application. This allows users to track the execution status of test cases.

## Current Behavior

- Test cases do not have a pass/fail status
- No way to track which test cases have been executed and their results
- Excel export shows default "Pass" status for all test cases

## New Behavior

### Project Detail Page (Test Cases List)
- Each test case card/item displays a pass/fail dropdown
- Dropdown shows current status (default: "Pass" or empty)
- User can toggle between "Pass" and "Fail" directly from the list
- Status is saved immediately when changed
- Visual indicator (color coding) to show status at a glance

### Test Case Detail Page
- Pass/fail dropdown displayed next to the test case number (e.g., "TC005 [Pass ▼]")
- Located in the top left area, next to the test case number
- Same functionality as project detail page
- Status persists and is visible when viewing the test case

### Excel Export
- Export uses the actual pass/fail status from the database
- "Outcome" column in summary sheet reflects the saved status
- Default to "Pass" if status is not set

## Implementation Details

### Step 1: Database Schema Update
- [ ] Add `status` column to `test_cases` table
  - Type: TEXT (values: "Pass", "Fail", or NULL)
  - Default: NULL (or "Pass")
  - Migration: Add column to existing table

### Step 2: Backend API Updates
- [ ] Update `TestCaseResponse` model to include `status` field
- [ ] Update `TestCaseUpdate` model to accept `status` field
- [ ] Update `update_test_case` function in `shared/models.py` to handle status
- [ ] Add endpoint or update existing endpoint to update status only (for quick toggles)
- [ ] Update `get_all_test_cases` and `get_test_case_by_id` to return status

### Step 3: Frontend Types & API Client
- [ ] Update `TestCase` interface to include `status?: "Pass" | "Fail" | null`
- [ ] Update `UpdateTestCaseRequest` to include `status`
- [ ] Add API method for quick status update (optional, can use existing update method)

### Step 4: Frontend - Project Detail Page
- [ ] Add pass/fail dropdown to `TestCaseItem` component
- [ ] Display dropdown with current status
- [ ] Handle status change and call API to update
- [ ] Show loading state during update
- [ ] Handle errors gracefully
- [ ] Add visual styling (green for Pass, red for Fail, gray for unset)

### Step 5: Frontend - Test Case Detail Page
- [ ] Add pass/fail dropdown next to test case number in header
- [ ] Position it in the top left area, next to "TC005" text
- [ ] Use same component/logic as project detail page
- [ ] Update status when changed
- [ ] Refresh test case data after update

### Step 6: Excel Export Update
- [ ] Update `excel_export.py` to use actual status from database
- [ ] Replace hardcoded "Pass" with `test_case.get('status', 'Pass')`
- [ ] Default to "Pass" if status is NULL or not set

## Testing Checklist

### Step 1: Database Schema
- [ ] Run database initialization
- [ ] Verify `status` column exists in `test_cases` table
- [ ] Verify existing test cases have NULL or default status
- [ ] Test creating new test case (should have NULL or default status)

### Step 2: Backend API
- [ ] Test updating test case status via API
- [ ] Test getting test case with status field
- [ ] Test updating status to "Pass"
- [ ] Test updating status to "Fail"
- [ ] Test updating status to NULL (if supported)
- [ ] Verify status is returned in all test case endpoints

### Step 3: Frontend - Project Detail Page
- [ ] Start frontend and backend
- [ ] Navigate to a project detail page
- [ ] Verify dropdown appears on each test case card
- [ ] Verify dropdown shows current status (or default)
- [ ] Test changing status from "Pass" to "Fail"
- [ ] Test changing status from "Fail" to "Pass"
- [ ] Verify status persists after page refresh
- [ ] Verify visual styling (colors) work correctly
- [ ] Test error handling (stop backend, try to update)

### Step 4: Frontend - Test Case Detail Page
- [ ] Open a test case detail page
- [ ] Verify dropdown appears next to test case number (e.g., "TC005 [Pass ▼]")
- [ ] Verify dropdown shows current status
- [ ] Test changing status
- [ ] Verify status persists after page refresh
- [ ] Navigate back to project page and verify status matches

### Step 5: Excel Export
- [ ] Set some test cases to "Pass" and some to "Fail"
- [ ] Export test cases to Excel
- [ ] Open Excel file
- [ ] Verify "Outcome" column shows correct status for each test case
- [ ] Verify test cases with no status default to "Pass"

### Integration Tests
- [ ] Change status on project detail page → verify it updates on test case detail page
- [ ] Change status on test case detail page → verify it updates on project detail page
- [ ] Export Excel → verify all statuses are correct
- [ ] Create new test case → verify it has default status
- [ ] Test with multiple projects → verify status is per test case, not per project

## Benefits

- **Status Tracking**: Users can track which test cases have been executed and their results
- **Quick Updates**: Easy to toggle status from multiple locations
- **Accurate Reporting**: Excel exports reflect actual test execution status
- **Visual Feedback**: Color coding makes it easy to see test case status at a glance

## Status
⏳ **Planned** - Ready for implementation

