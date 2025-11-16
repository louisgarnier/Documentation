"""
Test Case Documentation Tool - Main Streamlit Application

A web application for creating and managing SimCorp Dimension test case documentation.
"""

import streamlit as st
from models import init_database, get_all_test_cases
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
    st.info("🚧 Test case creation form will be implemented in Step 4")
    st.markdown("""
    This page will allow you to:
    - Enter test case number
    - Add test case description
    - Save the test case to the database
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>Test Case Documentation Tool v1.0</div>",
    unsafe_allow_html=True
)

