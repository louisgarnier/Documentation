# Test Case Documentation Tool

A Streamlit-based web application for creating and managing SimCorp Dimension test case documentation with Excel export capability.

## Features

- Create and manage test cases with descriptions and numbers
- Add multiple steps to each test case
- Attach screenshots to steps
- Add metadata: modules used, calculation logic, configuration elements
- Export all test cases to Excel workbook (summary + individual test sheets)

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
streamlit run app.py
```

3. Open your browser to `http://localhost:8501`

## Project Structure

```
Documentation/
├── app.py              # Main Streamlit application
├── models.py           # Database models and setup
├── excel_export.py     # Excel generation functions
├── uploads/            # Screenshot storage
└── database/           # SQLite database (auto-created)
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

