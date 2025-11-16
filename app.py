"""
Test Case Documentation Tool - Main Streamlit Application

A web application for creating and managing SimCorp Dimension test case documentation.
"""

import streamlit as st
from models import (
    init_database, 
    get_all_test_cases, 
    create_test_case,
    get_test_case_by_id,
    update_test_case,
    delete_test_case,
    get_steps_by_test_case,
    create_test_step,
    get_step_by_id,
    update_test_step,
    delete_test_step,
    add_screenshot_to_step,
    get_screenshots_by_step,
    delete_screenshot
)
import pandas as pd
import os
import re
from pathlib import Path
from PIL import Image as PILImage
from excel_export import create_excel_export

# Page configuration
st.set_page_config(
    page_title="Test Case Documentation Tool",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database on startup
@st.cache_resource
def initialize_db():
    """Initialize database (cached to run only once)"""
    init_database()
    return True

# Initialize database
initialize_db()

# Helper function to save uploaded screenshot
def save_screenshot(uploaded_file, test_case_id, step_id):
    """Save uploaded screenshot to the appropriate directory and return the file path."""
    # Create directory structure: uploads/test_{id}/step_{id}/
    upload_dir = Path(f"uploads/test_{test_case_id}/step_{step_id}")
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate unique filename
    file_extension = Path(uploaded_file.name).suffix
    timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}{file_extension}"
    file_path = upload_dir / filename
    
    # Save the file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Return relative path for database storage
    return str(file_path)

# Sidebar navigation
st.sidebar.title("📋 Test Case Documentation")
st.sidebar.markdown("---")

# Navigation options
# If force_details_page is set, automatically switch to Test Case Details page
if 'force_details_page' in st.session_state and st.session_state['force_details_page']:
    # Set the page to Test Case Details
    if 'page' not in st.session_state or st.session_state['page'] != "Test Case Details":
        st.session_state['page'] = "Test Case Details"
    # Clear the force flag
    del st.session_state['force_details_page']

# If force_create_page is set, automatically switch to Create New Test Case page
if 'force_create_page' in st.session_state and st.session_state['force_create_page']:
    # Set the page to Create New Test Case
    st.session_state['page'] = "Create New Test Case"
    # Clear the force flag
    del st.session_state['force_create_page']

# Initialize page in session state if not exists
if 'page' not in st.session_state:
    st.session_state['page'] = "All Test Cases"

# If somehow on Edit Test Case page, redirect to Test Case Details
if st.session_state.get('page') == "Edit Test Case":
    st.session_state['page'] = "Test Case Details"

# Navigation radio button
# Determine the index based on current page
page_options = ["All Test Cases", "Test Case Details"]
current_page = st.session_state.get('page', "All Test Cases")
# Redirect old page names (but allow Create New Test Case to work)
if current_page == "Edit Test Case" or current_page == "View Test Cases":
    if current_page == "View Test Cases":
        current_page = "All Test Cases"
    elif current_page == "Edit Test Case":
        current_page = "Test Case Details"
    st.session_state['page'] = current_page

try:
    default_index = page_options.index(current_page) if current_page in page_options else 0
except ValueError:
    default_index = 0

page_selection = st.sidebar.radio(
    "Navigation",
    page_options,
    index=default_index,
    label_visibility="collapsed"
)

# Always use session state page for routing to support programmatic navigation
# But update session state if user manually changed the radio button
# Only update if the current page is one of the radio button options
current_session_page = st.session_state.get('page', "All Test Cases")
if page_selection != current_session_page and current_session_page in page_options:
    st.session_state['page'] = page_selection

# Use session state for routing (this allows programmatic navigation to work)
# If page is "Create New Test Case", use it directly (not in radio options)
page = st.session_state.get('page', page_selection)

# Main content area
st.title("📋 Test Case Documentation Tool")
st.markdown("Manage your SimCorp Dimension test cases and documentation")

st.markdown("---")

# Page routing
if page == "All Test Cases" or page == "View Test Cases":  # Support both for backward compatibility
    # Header with Create and Export buttons
    col_header_title, col_header_btn1, col_header_btn2 = st.columns([2, 1, 1])
    with col_header_title:
        st.header("📊 All Test Cases")
    with col_header_btn1:
        # Export button
        if st.button("📥 Export to Excel", key="export_excel", use_container_width=True):
            try:
                # Generate Excel file
                timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
                filename = f"test_cases_export_{timestamp}.xlsx"
                file_path = create_excel_export(filename)
                
                # Read file data and store in session state
                with open(file_path, "rb") as f:
                    st.session_state['excel_file_data'] = f.read()
                    st.session_state['excel_filename'] = filename
                
                st.success(f"✅ Excel file generated! Click download button below.")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error generating Excel file: {str(e)}")
        
        # Download button (shown if file is ready)
        if 'excel_file_data' in st.session_state and 'excel_filename' in st.session_state:
            st.download_button(
                label="⬇️ Download Excel File",
                data=st.session_state['excel_file_data'],
                file_name=st.session_state['excel_filename'],
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="download_excel",
                use_container_width=True
            )
    with col_header_btn2:
        if st.button("➕ Create New Test Case", type="primary", use_container_width=True, key="create_new_tc_btn"):
            st.session_state['page'] = "Create New Test Case"
            st.session_state['force_create_page'] = True
            st.rerun()
    
    # Get all test cases
    test_cases = get_all_test_cases()
    
    if len(test_cases) == 0:
        st.info("📝 No test cases yet. Click 'Create New Test Case' above to get started!")
        st.markdown("""
        ### Getting Started
        1. Click **"➕ Create New Test Case"** button above
        2. Fill in the test case details
        3. Start adding steps and documentation
        """)
    else:
        # Create custom clickable table
        st.markdown("**Click on any row to view test case details**")
        st.markdown("---")
        
        # Table header
        col_header1, col_header2, col_header3, col_header4 = st.columns([2, 4, 2, 1])
        with col_header1:
            st.markdown("**Test Number**")
        with col_header2:
            st.markdown("**Description**")
        with col_header3:
            st.markdown("**Created**")
        with col_header4:
            st.markdown("**Actions**")
        
        st.markdown("---")
        
        # Display each test case as a clickable row
        for tc in test_cases:
            col1, col2, col3, col4 = st.columns([2, 4, 2, 1])
            
            # Make the row clickable - use button that spans most of the row
            with col1:
                if st.button(tc['test_number'], key=f"row_{tc['id']}_1", use_container_width=True):
                    st.session_state['view_test_case_id'] = tc['id']
                    st.session_state['page'] = "Test Case Details"
                    st.session_state['force_details_page'] = True
                    st.rerun()
            
            with col2:
                description = tc['description'][:80] + "..." if len(tc['description']) > 80 else tc['description']
                if st.button(description, key=f"row_{tc['id']}_2", use_container_width=True):
                    st.session_state['view_test_case_id'] = tc['id']
                    st.session_state['page'] = "Test Case Details"
                    st.session_state['force_details_page'] = True
                    st.rerun()
            
            with col3:
                created_date = tc['created_at'][:10] if tc['created_at'] else "N/A"
                if st.button(created_date, key=f"row_{tc['id']}_3", use_container_width=True):
                    st.session_state['view_test_case_id'] = tc['id']
                    st.session_state['page'] = "Test Case Details"
                    st.session_state['force_details_page'] = True
                    st.rerun()
            
            with col4:
                # Delete button
                if st.button("🗑️", key=f"delete_{tc['id']}", help=f"Delete {tc['test_number']}"):
                    st.session_state['delete_test_case_id'] = tc['id']
                    st.session_state['delete_test_case_number'] = tc['test_number']
            
            st.markdown("---")
        
        # Handle delete confirmation
        if 'delete_test_case_id' in st.session_state and 'delete_test_case_number' in st.session_state:
            st.warning(f"⚠️ Are you sure you want to delete test case '{st.session_state['delete_test_case_number']}'?")
            col_confirm, col_cancel = st.columns(2)
            with col_confirm:
                if st.button("✅ Confirm Delete", key="confirm_delete", type="primary", use_container_width=True):
                    try:
                        success = delete_test_case(st.session_state['delete_test_case_id'])
                        if success:
                            st.success(f"✅ Test case '{st.session_state['delete_test_case_number']}' deleted successfully!")
                            # Clear session state
                            del st.session_state['delete_test_case_id']
                            del st.session_state['delete_test_case_number']
                            st.cache_data.clear()
                            st.rerun()
                        else:
                            st.error("❌ Failed to delete test case.")
                    except Exception as e:
                        st.error(f"❌ Error deleting test case: {str(e)}")
            with col_cancel:
                if st.button("❌ Cancel", key="cancel_delete", use_container_width=True):
                    del st.session_state['delete_test_case_id']
                    del st.session_state['delete_test_case_number']
                    st.rerun()

elif page == "Create New Test Case":
    # Back button
    if st.button("← Back to All Test Cases", key="back_from_create"):
        st.session_state['page'] = "All Test Cases"
        st.rerun()
    
    st.header("➕ Create New Test Case")
    st.markdown("Fill in the details below to create a new test case.")
    
    # Suggest next test number
    def suggest_next_test_number():
        """Suggest the next test number based on existing test cases."""
        test_cases = get_all_test_cases()
        if not test_cases:
            return "TC001"  # Default if no test cases exist
        
        # Extract numbers from test case numbers
        numbers = []
        for tc in test_cases:
            # Try to find numeric patterns (e.g., "TC001", "TC-001", "001", etc.)
            match = re.search(r'(\d+)', tc['test_number'])
            if match:
                numbers.append(int(match.group(1)))
        
        if numbers:
            next_num = max(numbers) + 1
            # Try to preserve the format of the most common pattern
            # Check if most test cases use a prefix
            prefixes = {}
            for tc in test_cases:
                match = re.match(r'^([A-Za-z\-]+)', tc['test_number'])
                if match:
                    prefix = match.group(1)
                    prefixes[prefix] = prefixes.get(prefix, 0) + 1
            
            if prefixes:
                # Use the most common prefix
                most_common_prefix = max(prefixes, key=prefixes.get)
                # Check if they use dashes or not
                if '-' in most_common_prefix:
                    return f"{most_common_prefix.split('-')[0]}-{next_num:03d}"
                else:
                    return f"{most_common_prefix}{next_num:03d}"
            else:
                # Default format
                return f"TC{next_num:03d}"
        else:
            # No numbers found, use default
            return "TC001"
    
    suggested_number = suggest_next_test_number()
    
    # Create form
    with st.form("create_test_case_form", clear_on_submit=True):
        test_number = st.text_input(
            "Test Number *",
            value=suggested_number,
            placeholder="e.g., TC-001, TC-IMPL-001",
            help=f"Suggested: {suggested_number} (based on existing test cases)"
        )
        
        description = st.text_area(
            "Description *",
            placeholder="Enter a detailed description of the test case...",
            help="Describe what this test case validates",
            height=100
        )
        
        submitted = st.form_submit_button("Create Test Case", type="primary", use_container_width=True)
        
        if submitted:
            # Validation
            if not test_number.strip():
                st.error("❌ Test Number is required!")
            elif not description.strip():
                st.error("❌ Description is required!")
            else:
                try:
                    # Create test case
                    test_case_id = create_test_case(
                        test_number=test_number.strip(),
                        description=description.strip()
                    )
                    
                    if test_case_id:
                        st.success(f"✅ Test case '{test_number}' created successfully!")
                        st.balloons()
                        
                        # Clear cache to refresh the list
                        st.cache_data.clear()
                        # Redirect to All Test Cases
                        st.session_state['page'] = "All Test Cases"
                        st.rerun()
                except Exception as e:
                    if "UNIQUE constraint failed" in str(e):
                        st.error(f"❌ Test case number '{test_number}' already exists! Please use a different number.")
                    else:
                        st.error(f"❌ Error creating test case: {str(e)}")
    
    st.markdown("---")
    st.markdown("### 📝 Notes")
    st.markdown("""
    - **Test Number**: Must be unique. Use a consistent naming convention (e.g., TC-001, TC-IMPL-001)
    - **Description**: Provide a clear description of what this test case validates
    - After creating, you can add steps, screenshots, and metadata to the test case
    """)

elif page == "Test Case Details":
    st.header("📝 Test Case Details")
    
    # Get all test cases for selection
    test_cases = get_all_test_cases()
    
    if len(test_cases) == 0:
        st.info("📝 No test cases available. Create a test case first!")
        st.markdown("""
        ### Getting Started
        1. Go to **"Create New Test Case"** to create your first test case
        2. Then come back here to add steps to it
        """)
        # Back button (no unsaved changes to check)
        if st.button("← Back to All Test Cases", key="back_to_all_empty"):
            st.session_state['page'] = "All Test Cases"
            st.rerun()
    else:
        # Test case selection
        test_cases_dict = {
            (f"{tc['test_number']} - {tc['description'][:50]}..." if len(tc['description']) > 50 
             else f"{tc['test_number']} - {tc['description']}"): tc['id'] 
            for tc in test_cases
        }
        
        # If test case was selected from All Test Cases page, use it
        if 'view_test_case_id' in st.session_state:
            # Find the test case in the dict
            selected_id = st.session_state['view_test_case_id']
            selected_tc_key = next((key for key, val in test_cases_dict.items() if val == selected_id), None)
            if selected_tc_key:
                default_index = list(test_cases_dict.keys()).index(selected_tc_key)
            else:
                default_index = 0
        else:
            default_index = 0
        
        selected_tc = st.selectbox(
            "Select Test Case:",
            options=list(test_cases_dict.keys()),
            index=default_index,
            key="details_test_case_select"
        )
        
        test_case_id = test_cases_dict[selected_tc]
        test_case = get_test_case_by_id(test_case_id)
        
        # Check for unsaved changes function
        def has_unsaved_changes(tc_id):
            """Check if there are unsaved changes in the current test case."""
            edit_mode_key = f'edit_test_case_details_{tc_id}'
            return st.session_state.get(edit_mode_key, False)
        
        # Back button with unsaved changes check (placed after test case is selected)
        if st.button("← Back to All Test Cases", key="back_to_all"):
            # Check for unsaved changes
            if has_unsaved_changes(test_case_id):
                # Set flag to show warning
                st.session_state['show_unsaved_warning'] = True
                st.session_state['pending_navigation'] = True
                st.session_state['warning_test_case_id'] = test_case_id
                st.rerun()
            else:
                # No unsaved changes, proceed with navigation
                if 'view_test_case_id' in st.session_state:
                    del st.session_state['view_test_case_id']
                if 'show_unsaved_warning' in st.session_state:
                    del st.session_state['show_unsaved_warning']
                if 'pending_navigation' in st.session_state:
                    del st.session_state['pending_navigation']
                if 'warning_test_case_id' in st.session_state:
                    del st.session_state['warning_test_case_id']
                st.session_state['page'] = "All Test Cases"
                st.rerun()
        
        # Show unsaved changes warning if needed
        if st.session_state.get('show_unsaved_warning', False) and st.session_state.get('pending_navigation', False):
            warning_tc_id = st.session_state.get('warning_test_case_id', test_case_id)
            st.warning("⚠️ **You have unsaved changes!** Please save or cancel your edits before leaving this page.")
            col_save, col_discard, col_cancel = st.columns(3)
            with col_save:
                if st.button("💾 Save & Go Back", key="save_and_back", type="primary", use_container_width=True):
                    st.info("💡 Please click '💾 Save Changes' in the edit form below, then click '← Back to All Test Cases' again.")
            with col_discard:
                if st.button("🗑️ Discard Changes", key="discard_and_back", use_container_width=True):
                    # Exit edit mode
                    if warning_tc_id:
                        edit_mode_key = f'edit_test_case_details_{warning_tc_id}'
                        st.session_state[edit_mode_key] = False
                    
                    # Clear warning and navigate
                    del st.session_state['show_unsaved_warning']
                    del st.session_state['pending_navigation']
                    if 'warning_test_case_id' in st.session_state:
                        del st.session_state['warning_test_case_id']
                    if 'view_test_case_id' in st.session_state:
                        del st.session_state['view_test_case_id']
                    st.session_state['page'] = "All Test Cases"
                    st.rerun()
            with col_cancel:
                if st.button("❌ Stay on Page", key="stay_on_page", use_container_width=True):
                    del st.session_state['show_unsaved_warning']
                    del st.session_state['pending_navigation']
                    if 'warning_test_case_id' in st.session_state:
                        del st.session_state['warning_test_case_id']
                    st.rerun()
            st.markdown("---")
        
        if test_case:
            st.markdown("---")
            
            # Check if we're in edit mode
            edit_mode_key = f'edit_test_case_details_{test_case_id}'
            is_editing = st.session_state.get(edit_mode_key, False)
            
            if not is_editing:
                # Display test case info (view mode)
                col1, col2 = st.columns([3, 1])
                with col1:
                    col_info1, col_info2 = st.columns(2)
                    with col_info1:
                        st.markdown(f"**Test Number:** {test_case['test_number']}")
                    with col_info2:
                        st.markdown(f"**Created:** {test_case['created_at'][:10] if test_case['created_at'] else 'N/A'}")
                    st.markdown(f"**Description:** {test_case['description']}")
                with col2:
                    if st.button("✏️ Edit Test Case", key=f"edit_tc_{test_case_id}", use_container_width=True):
                        st.session_state[edit_mode_key] = True
                        st.rerun()
            else:
                # Edit mode
                st.markdown("### ✏️ Edit Test Case")
                
                with st.form(f"edit_test_case_form_{test_case_id}", clear_on_submit=False):
                    test_number = st.text_input(
                        "Test Number *",
                        value=test_case['test_number'],
                        key=f"edit_tc_num_{test_case_id}",
                        help="Enter a unique test case number"
                    )
                    
                    description = st.text_area(
                        "Description *",
                        value=test_case['description'],
                        key=f"edit_tc_desc_{test_case_id}",
                        help="Describe what this test case validates",
                        height=100
                    )
                    
                    st.markdown(f"**Created:** {test_case['created_at'][:10] if test_case['created_at'] else 'N/A'} *(cannot be changed)*")
                    
                    col_save, col_cancel = st.columns(2)
                    with col_save:
                        submitted = st.form_submit_button("💾 Save Changes", type="primary", use_container_width=True)
                    with col_cancel:
                        cancelled = st.form_submit_button("❌ Cancel", use_container_width=True)
                    
                    if submitted:
                        # Validation
                        if not test_number.strip():
                            st.error("❌ Test Number is required!")
                        elif not description.strip():
                            st.error("❌ Description is required!")
                        else:
                            try:
                                # Update test case
                                success = update_test_case(
                                    test_case_id=test_case_id,
                                    test_number=test_number.strip(),
                                    description=description.strip()
                                )
                                
                                if success:
                                    st.success(f"✅ Test case '{test_number}' updated successfully!")
                                    st.session_state[edit_mode_key] = False
                                    st.cache_data.clear()
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to update test case.")
                            except Exception as e:
                                if "UNIQUE constraint failed" in str(e):
                                    st.error(f"❌ Test case number '{test_number}' already exists! Please use a different number.")
                                else:
                                    st.error(f"❌ Error updating test case: {str(e)}")
                    
                    if cancelled:
                        st.session_state[edit_mode_key] = False
                        st.rerun()
            
            st.markdown("---")
            
            # Get and display steps
            steps = get_steps_by_test_case(test_case_id)
            
            st.subheader(f"📋 Steps ({len(steps)})")
            
            if len(steps) == 0:
                st.info("No steps added yet. Use the form below to add your first step.")
            else:
                # Display steps with inline editing
                for idx, step in enumerate(steps, 1):
                    step_key = f"step_{step['id']}"
                    
                    with st.expander(f"Step {step['step_number']}", expanded=False):
                        with st.form(f"step_form_{step['id']}", clear_on_submit=False):
                            # Editable step number
                            col_num, col_del = st.columns([3, 1])
                            with col_num:
                                edit_step_number = st.number_input(
                                    "Step Number",
                                    min_value=1,
                                    value=step['step_number'],
                                    key=f"step_num_{step['id']}"
                                )
                            with col_del:
                                st.write("")  # Spacing
                                st.write("")  # Spacing
                                delete_checkbox = st.checkbox("🗑️ Delete", key=f"delete_{step['id']}")
                            
                            # Editable description
                            edit_description = st.text_area(
                                "Description",
                                value=step['description'],
                                key=f"desc_{step['id']}",
                                height=80
                            )
                            
                            # Editable notes
                            edit_notes = st.text_area(
                                "Notes",
                                value=step['modules'] if step['modules'] else "",
                                key=f"notes_{step['id']}",
                                height=100
                            )
                            
                            # Display screenshots
                            screenshots = get_screenshots_by_step(step['id'])
                            screenshots_to_delete = []
                            
                            if screenshots:
                                st.markdown("**Screenshots:**")
                                for i in range(0, len(screenshots), 3):
                                    cols = st.columns(3)
                                    for j, col in enumerate(cols):
                                        if i + j < len(screenshots):
                                            screenshot = screenshots[i + j]
                                            with col:
                                                if os.path.exists(screenshot['file_path']):
                                                    upload_date = screenshot['uploaded_at'][:10] if screenshot['uploaded_at'] else 'N/A'
                                                    st.image(screenshot['file_path'], caption=upload_date, width=120)
                                                    if st.checkbox("🗑️", key=f"del_ss_{screenshot['id']}", help="Delete screenshot"):
                                                        screenshots_to_delete.append(screenshot)
                                                else:
                                                    st.warning(f"⚠️ File not found")
                            
                            # Upload new screenshot
                            st.markdown("**Upload New Screenshot:**")
                            uploaded_screenshot = st.file_uploader(
                                "Choose an image",
                                type=['png', 'jpg', 'jpeg', 'gif', 'bmp'],
                                key=f"upload_{step['id']}"
                            )
                            
                            # Save changes button
                            submitted = st.form_submit_button("💾 Save Changes", type="primary", use_container_width=True)
                            
                            # Handle form submission
                            if submitted:
                                # If delete is checked, delete the step
                                if delete_checkbox:
                                    try:
                                        success = delete_test_step(step['id'])
                                        if success:
                                            st.success(f"✅ Step {step['step_number']} deleted successfully!")
                                            st.cache_data.clear()
                                            st.rerun()
                                        else:
                                            st.error("❌ Failed to delete step.")
                                    except Exception as e:
                                        st.error(f"❌ Error deleting step: {str(e)}")
                                else:
                                    # Update the step
                                    try:
                                        success = update_test_step(
                                            step_id=step['id'],
                                            step_number=int(edit_step_number),
                                            description=edit_description.strip(),
                                            modules=edit_notes.strip() if edit_notes.strip() else None,
                                            calculation_logic=None,
                                            configuration=None
                                        )
                                        
                                        if success:
                                            # Delete marked screenshots
                                            for screenshot in screenshots_to_delete:
                                                try:
                                                    if os.path.exists(screenshot['file_path']):
                                                        os.remove(screenshot['file_path'])
                                                    delete_screenshot(screenshot['id'])
                                                except Exception as e:
                                                    st.warning(f"⚠️ Error deleting screenshot: {str(e)}")
                                            
                                            # Upload new screenshot if provided
                                            if uploaded_screenshot is not None:
                                                try:
                                                    screenshot_path = save_screenshot(uploaded_screenshot, test_case_id, step['id'])
                                                    add_screenshot_to_step(step['id'], screenshot_path)
                                                    st.success(f"✅ Step {edit_step_number} updated successfully!")
                                                except Exception as e:
                                                    st.warning(f"⚠️ Step updated but screenshot upload failed: {str(e)}")
                                            else:
                                                st.success(f"✅ Step {edit_step_number} updated successfully!")
                                            
                                            st.cache_data.clear()
                                            st.rerun()
                                        else:
                                            st.error("❌ Failed to update step.")
                                    except Exception as e:
                                        if "UNIQUE constraint failed" in str(e):
                                            st.error(f"❌ Step number {edit_step_number} already exists!")
                                        else:
                                            st.error(f"❌ Error updating step: {str(e)}")
            
            st.markdown("---")
            
            # Add Step Form
            st.subheader("➕ Add New Step")
            
            with st.form("add_step_form", clear_on_submit=True):
                col_step_num, col_desc = st.columns([1, 3])
                
                with col_step_num:
                    step_number = st.number_input(
                        "Step Number *",
                        min_value=1,
                        value=len(steps) + 1 if steps else 1,
                        help="Step number in sequence"
                    )
                
                with col_desc:
                    step_description = st.text_area(
                        "Step Description *",
                        placeholder="Describe what this step validates...",
                        help="Detailed description of the step",
                        height=80
                    )
                
                st.markdown("**Additional Information (Optional):**")
                
                step_notes = st.text_area(
                    "Notes",
                    placeholder="Add any notes, modules used, calculation logic, configuration details, etc.",
                    help="Add any additional details about this step",
                    height=120
                )
                
                # Screenshot upload
                st.markdown("**Upload Screenshot (Optional):**")
                uploaded_screenshot = st.file_uploader(
                    "Choose an image file",
                    type=['png', 'jpg', 'jpeg', 'gif', 'bmp'],
                    key=f"add_screenshot_{test_case_id}",
                    help="Upload a screenshot for this step"
                )
                
                submitted = st.form_submit_button("Add Step", type="primary", use_container_width=True)
                
                if submitted:
                    # Validation
                    if not step_description.strip():
                        st.error("❌ Step description is required!")
                    else:
                        try:
                            # Check if step number already exists
                            existing_step_numbers = [s['step_number'] for s in steps]
                            if step_number in existing_step_numbers:
                                st.warning(f"⚠️ Step number {step_number} already exists. Consider using a different number.")
                            else:
                                # Create step
                                step_id = create_test_step(
                                    test_case_id=test_case_id,
                                    step_number=int(step_number),
                                    description=step_description.strip(),
                                    modules=step_notes.strip() if step_notes.strip() else None,
                                    calculation_logic=None,
                                    configuration=None
                                )
                                
                                if step_id:
                                    # Handle screenshot upload if provided
                                    if uploaded_screenshot is not None:
                                        try:
                                            screenshot_path = save_screenshot(uploaded_screenshot, test_case_id, step_id)
                                            add_screenshot_to_step(step_id, screenshot_path)
                                            st.success(f"✅ Step {step_number} added with screenshot successfully!")
                                        except Exception as e:
                                            st.warning(f"⚠️ Step added but screenshot upload failed: {str(e)}")
                                    else:
                                        st.success(f"✅ Step {step_number} added successfully!")
                                    
                                    st.balloons()
                                    st.cache_data.clear()
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to add step.")
                        except Exception as e:
                            if "UNIQUE constraint failed" in str(e):
                                st.error(f"❌ Step number {step_number} already exists for this test case!")
                            else:
                                st.error(f"❌ Error adding step: {str(e)}")
            
            st.markdown("---")
            st.markdown("💡 **Tip**: Steps are displayed in order by step number. Open any step to edit it directly, then click '💾 Save Changes' to update.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>Test Case Documentation Tool v1.0</div>",
    unsafe_allow_html=True
)

