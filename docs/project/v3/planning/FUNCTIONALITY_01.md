# Functionality 1: Enhanced Screenshot Capture Process

## Overview
Improve the screenshot capture workflow by simplifying the popup dialog and streamlining the saved description file format.

## Current Behavior

### Popup Dialog
- Screenshot name input
- Test case input (text field)
- Step # input (manual entry)
- Description input

### Saved .txt File Format
```
Test Case: TC01
Step #: 1
Description: This is the step description
```

## New Behavior

### Popup Dialog Changes
- ✅ **Screenshot name input** - Keep as is
- 🔄 **Test case input** - Change from text field to **dropdown** populated with test cases from the app
- ❌ **Step # input** - **Remove** (step number will be automatically generated)
- ✅ **Description input** - Keep as is

### Saved .txt File Format
- **Only save the description text** (no headers, no metadata)
- Example:
  ```
  This is the step description
  ```

## Implementation Details

### 1. Dialog Updates (`screenshot-capture-service/description_dialog.py`)
- Remove step number input field
- Replace test case text input with dropdown/combobox
- Fetch test cases from backend API endpoint: `GET /api/test-cases`
- Populate dropdown with test case numbers/names

### 2. File Saving Logic
- Update file writing to only output description text
- Remove all metadata headers (Test Case, Step #, Description labels)

### 3. Backend Integration
- Dialog needs to call backend API to retrieve test cases list
- Handle API connection errors gracefully
- Cache test cases list if needed for offline scenarios

## Benefits
- ✅ Simpler user experience (fewer fields to fill)
- ✅ Automatic step numbering (reduces errors)
- ✅ Cleaner description files (easier to read/edit)
- ✅ Better test case selection (dropdown prevents typos)

## Testing Checklist

- [x] Popup dialog shows only: Screenshot name, Test case dropdown, Description
- [x] Step # input field is removed from dialog
- [x] Test case dropdown is populated with test cases from the app
- [x] Test case dropdown shows test case numbers/names correctly
- [x] Description input field works as expected
- [x] Saved .txt file contains only the description text (no headers)
- [x] Saved .txt file has no "Test Case:" line
- [x] Saved .txt file has no "Step #:" line
- [x] Saved .txt file has no "Description:" label
- [ ] Step number is automatically generated when loading step (to be tested when loading steps)
- [x] Backend API connection works for fetching test cases
- [x] Error handling works if backend is unavailable
- [x] Dialog gracefully handles empty test cases list
- [x] Screenshots are saved to Capture_TC folder correctly
- [x] Text files are saved to Capture_TC folder correctly
- [x] Files are renamed correctly based on test case and screenshot name

## Status
✅ **Implemented** - Functionality complete and tested

## Implementation Notes

- Updated `description_dialog.py` to use dropdown for test cases
- Removed step number input field
- Updated file saving to only write description text
- Added error handling for backend unavailability
- Fixed None value handling to prevent crashes

