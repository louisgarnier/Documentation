# Test Case Documentation Tool

A Streamlit-based web application for creating and managing SimCorp Dimension test case documentation with Excel export capability.

## Features

- Create and manage test cases with descriptions and numbers
- Add multiple steps to each test case
- Attach screenshots to steps
- Add metadata: modules used, calculation logic, configuration elements
- Export all test cases to Excel workbook (summary + individual test sheets)

## Setup

### Streamlit Version (Current)

1. Install dependencies:
```bash
pip install -r streamlit/requirements.txt
```

2. Run the application:
```bash
# Option 1: Use the launcher script
python3 run_streamlit.py

# Option 2: Run directly
streamlit run streamlit/app.py
```

3. Open your browser to `http://localhost:8501`

**Note**: The app has been restructured. The main file is now at `streamlit/app.py`, but you can use the launcher script for convenience.

## Project Structure

```
Documentation/
├── streamlit/          # Streamlit application (current version)
│   ├── app.py          # Main Streamlit application
│   └── requirements.txt
├── shared/             # Shared components (used by Streamlit and future API)
│   ├── models.py       # Database models and setup
│   ├── excel_export.py # Excel generation functions
│   └── database/       # SQLite database
├── backend/            # Future API backend (empty for now)
├── frontend/           # Future React frontend (empty for now)
├── uploads/            # Screenshot storage
├── backups/            # Database backups
├── docs/               # Documentation files
├── run_streamlit.py    # Launcher script for Streamlit app
└── app.py              # Compatibility placeholder
```

## Usage

1. **Create Test Case**: Use the sidebar to create a new test case
2. **Add Steps**: Open a test case and add steps with descriptions
3. **Add Metadata**: Edit steps to include modules, calculation logic, and configuration
4. **Upload Screenshots**: Attach screenshots to each step
5. **Export to Excel**: Use the export button to generate Excel workbook

## Git Workflow

See `GIT_WORKFLOW.md` for detailed git workflow instructions.

## Repository

https://github.com/louisgarnier/Documentation.git

