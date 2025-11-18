# Backend API

Python API backend for the Test Case Documentation Tool.

## Status

🚧 **Under Development**

This backend will provide REST API endpoints for:
- Test case CRUD operations
- Test step management
- Screenshot handling
- Excel export

## Technology

- **Framework**: FastAPI or Flask (TBD)
- **Database**: SQLite (via shared/models.py)
- **Python Version**: 3.10+

## Planned Endpoints

- `GET /api/test-cases` - List all test cases
- `GET /api/test-cases/{id}` - Get test case details
- `POST /api/test-cases` - Create new test case
- `PUT /api/test-cases/{id}` - Update test case
- `DELETE /api/test-cases/{id}` - Delete test case
- `GET /api/test-cases/{id}/steps` - Get steps for a test case
- `POST /api/test-cases/{id}/steps` - Add step to test case
- `POST /api/export` - Export test cases to Excel

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run the API server
python -m api.main
```

