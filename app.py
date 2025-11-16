"""
Test Case Documentation Tool - Main Streamlit Application

A web application for creating and managing SimCorp Dimension test case documentation.
"""

import streamlit as st
from models import init_database, get_all_test_cases, create_test_case
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
page = st.sidebar.radio(
    "Navigation",
    ["View Test Cases", "Create New Test Case"],
    label_visibility="collapsed"
)

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
        st.markdown("💡 **Tip**: Use the sidebar to create new test cases or view details")

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

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>Test Case Documentation Tool v1.0</div>",
    unsafe_allow_html=True
)

