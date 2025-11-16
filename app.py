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
    delete_test_case
)
import pandas as pd

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

# Sidebar navigation
st.sidebar.title("📋 Test Case Documentation")
st.sidebar.markdown("---")

# Navigation options
# If force_edit_page is set, automatically switch to Edit Test Case page
if 'force_edit_page' in st.session_state and st.session_state['force_edit_page']:
    # Set the page to Edit Test Case
    if 'page' not in st.session_state or st.session_state['page'] != "Edit Test Case":
        st.session_state['page'] = "Edit Test Case"
    # Clear the force flag
    del st.session_state['force_edit_page']

# Initialize page in session state if not exists
if 'page' not in st.session_state:
    st.session_state['page'] = "View Test Cases"

# Navigation radio button
page_selection = st.sidebar.radio(
    "Navigation",
    ["View Test Cases", "Create New Test Case", "Edit Test Case"],
    index=["View Test Cases", "Create New Test Case", "Edit Test Case"].index(st.session_state['page']),
    label_visibility="collapsed",
    key="nav_radio"
)

# Update session state when user manually changes page
if page_selection != st.session_state['page']:
    st.session_state['page'] = page_selection

# Use session state page for routing
page = st.session_state['page']

# Main content area
st.title("📋 Test Case Documentation Tool")
st.markdown("Manage your SimCorp Dimension test cases and documentation")

st.markdown("---")

# Page routing
if page == "View Test Cases":
    st.header("📊 All Test Cases")
    
    # Get all test cases
    test_cases = get_all_test_cases()
    
    if len(test_cases) == 0:
        st.info("📝 No test cases yet. Create your first test case using the sidebar!")
        st.markdown("""
        ### Getting Started
        1. Select **"Create New Test Case"** from the sidebar
        2. Fill in the test case details
        3. Start adding steps and documentation
        """)
    else:
        # Display test cases in a table
        st.markdown(f"**Total Test Cases: {len(test_cases)}**")
        
        # Prepare data for display
        display_data = []
        for tc in test_cases:
            display_data.append({
                "Test Number": tc['test_number'],
                "Description": tc['description'],
                "Created": tc['created_at'][:10] if tc['created_at'] else "N/A"
            })
        
        # Create DataFrame and display
        df = pd.DataFrame(display_data)
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
        
        st.markdown("---")
        st.markdown("### Actions")
        
        # Create columns for edit/delete actions
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ✏️ Edit Test Case")
            test_cases_for_edit = {
                (f"{tc['test_number']} - {tc['description'][:50]}..." if len(tc['description']) > 50 
                 else f"{tc['test_number']} - {tc['description']}"): tc['id'] 
                for tc in test_cases
            }
            selected_edit = st.selectbox(
                "Select test case to edit:",
                options=list(test_cases_for_edit.keys()),
                key="edit_select",
                label_visibility="collapsed"
            )
            if st.button("Edit Selected", key="edit_btn", use_container_width=True):
                st.session_state['edit_test_case_id'] = test_cases_for_edit[selected_edit]
                st.session_state['edit_test_case_number'] = next(tc['test_number'] for tc in test_cases if tc['id'] == test_cases_for_edit[selected_edit])
                st.session_state['force_edit_page'] = True
                st.rerun()
        
        with col2:
            st.markdown("#### 🗑️ Delete Test Case")
            test_cases_for_delete = {
                (f"{tc['test_number']} - {tc['description'][:50]}..." if len(tc['description']) > 50 
                 else f"{tc['test_number']} - {tc['description']}"): tc['id'] 
                for tc in test_cases
            }
            selected_delete = st.selectbox(
                "Select test case to delete:",
                options=list(test_cases_for_delete.keys()),
                key="delete_select",
                label_visibility="collapsed"
            )
            if st.button("Delete Selected", key="delete_btn", type="secondary", use_container_width=True):
                st.session_state['delete_test_case_id'] = test_cases_for_delete[selected_delete]
                st.session_state['delete_test_case_number'] = next(tc['test_number'] for tc in test_cases if tc['id'] == test_cases_for_delete[selected_delete])
        
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
        
        st.markdown("---")
        st.markdown("💡 **Tip**: Use the sidebar to create new test cases or edit existing ones")

elif page == "Create New Test Case":
    st.header("➕ Create New Test Case")
    st.markdown("Fill in the details below to create a new test case.")
    
    # Create form
    with st.form("create_test_case_form", clear_on_submit=True):
        test_number = st.text_input(
            "Test Number *",
            placeholder="e.g., TC-001, TC-IMPL-001",
            help="Enter a unique test case number"
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
                        st.info("💡 Switch to 'View Test Cases' to see your new test case.")
                        
                        # Clear cache to refresh the list
                        st.cache_data.clear()
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

elif page == "Edit Test Case":
    st.header("✏️ Edit Test Case")
    
    # Check if test case ID is in session state (from View Test Cases page)
    if 'edit_test_case_id' in st.session_state:
        test_case_id = st.session_state['edit_test_case_id']
        test_case = get_test_case_by_id(test_case_id)
        
        if test_case:
            st.markdown(f"Editing: **{test_case['test_number']}**")
            st.markdown("---")
            
            # Create edit form
            with st.form("edit_test_case_form", clear_on_submit=False):
                test_number = st.text_input(
                    "Test Number *",
                    value=test_case['test_number'],
                    help="Enter a unique test case number"
                )
                
                description = st.text_area(
                    "Description *",
                    value=test_case['description'],
                    help="Describe what this test case validates",
                    height=100
                )
                
                submitted = st.form_submit_button("Save Changes", type="primary", use_container_width=True)
                
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
                                st.balloons()
                                st.info("💡 Switch to 'View Test Cases' to see the updated test case.")
                                
                                # Clear session state and cache
                                del st.session_state['edit_test_case_id']
                                if 'edit_test_case_number' in st.session_state:
                                    del st.session_state['edit_test_case_number']
                                st.cache_data.clear()
                            else:
                                st.error("❌ Failed to update test case.")
                        except Exception as e:
                            if "UNIQUE constraint failed" in str(e):
                                st.error(f"❌ Test case number '{test_number}' already exists! Please use a different number.")
                            else:
                                st.error(f"❌ Error updating test case: {str(e)}")
            
            st.markdown("---")
            if st.button("❌ Cancel Editing", use_container_width=True):
                del st.session_state['edit_test_case_id']
                if 'edit_test_case_number' in st.session_state:
                    del st.session_state['edit_test_case_number']
                st.rerun()
        else:
            st.error("❌ Test case not found!")
            if st.button("Go to View Test Cases", use_container_width=True):
                del st.session_state['edit_test_case_id']
                if 'edit_test_case_number' in st.session_state:
                    del st.session_state['edit_test_case_number']
                st.rerun()
    else:
        # No test case selected
        st.info("📝 No test case selected for editing.")
        st.markdown("""
        ### How to Edit a Test Case:
        1. Go to **"View Test Cases"** page
        2. Select a test case from the "Edit Test Case" dropdown
        3. Click **"Edit Selected"** button
        4. You'll be redirected here to edit the test case
        """)
        
        # Show all test cases for quick selection
        test_cases = get_all_test_cases()
        if len(test_cases) > 0:
            st.markdown("---")
            st.markdown("### Or select a test case to edit:")
            test_cases_dict = {
                (f"{tc['test_number']} - {tc['description'][:50]}..." if len(tc['description']) > 50 
                 else f"{tc['test_number']} - {tc['description']}"): tc['id'] 
                for tc in test_cases
            }
            selected = st.selectbox(
                "Select test case:",
                options=list(test_cases_dict.keys()),
                key="direct_edit_select"
            )
            if st.button("Edit Selected Test Case", type="primary", use_container_width=True):
                st.session_state['edit_test_case_id'] = test_cases_dict[selected]
                st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>Test Case Documentation Tool v1.0</div>",
    unsafe_allow_html=True
)

