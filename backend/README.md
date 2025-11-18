# Backend API

Python API backend for the Test Case Documentation Tool.

## Status

✅ **Phase 2 Complete**

This backend provides REST API endpoints for:
- Test case CRUD operations
- Test step management
- Screenshot handling
- Excel export

## Technology

- **Framework**: FastAPI
- **Database**: SQLite (via shared/models.py)
- **Python Version**: 3.10+

## API Endpoints

### Test Cases
- `GET /api/test-cases` - List all test cases
- `GET /api/test-cases/{id}` - Get test case details
- `POST /api/test-cases` - Create new test case
- `PUT /api/test-cases/{id}` - Update test case
- `DELETE /api/test-cases/{id}` - Delete test case

### Steps
- `GET /api/test-cases/{id}/steps` - Get all steps for a test case
- `POST /api/test-cases/{id}/steps` - Create a new step
- `GET /api/steps/{id}` - Get step details
- `PUT /api/steps/{id}` - Update step
- `DELETE /api/steps/{id}` - Delete step
- `POST /api/steps/{id}/reorder` - Reorder step to new position

### Screenshots
- `POST /api/steps/{id}/screenshots` - Upload screenshot
- `GET /api/steps/{id}/screenshots` - Get all screenshots for a step
- `GET /api/screenshots/{id}/file` - Download screenshot file
- `DELETE /api/screenshots/{id}` - Delete screenshot

### Export
- `POST /api/export` - Export selected test cases to Excel
  - Request body: `{"test_case_ids": [1, 2, 3]}`
  - Returns: Excel file download

## Setup

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run the API server
python3 -m uvicorn api.main:app --reload --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs (Interactive API documentation)
- **ReDoc**: http://localhost:8000/redoc (Alternative documentation)

## Testing

### Quick Test
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test getting test cases
curl http://localhost:8000/api/test-cases
```

### Comprehensive Tests
```bash
# Run all tests
python3 test_all.py

# Or run individual test scripts
python3 test_step2.py  # Basic structure
python3 test_step3.py  # GET endpoints
python3 test_step4.py  # CRUD test cases
python3 test_step5.py  # CRUD steps
python3 test_step6.py  # Screenshots
python3 test_step7.py  # Export
```

## Project Structure

```
backend/
├── api/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── models.py            # Pydantic models
│   └── routes/
│       ├── __init__.py
│       ├── test_cases.py    # Test case endpoints
│       ├── steps.py         # Step endpoints
│       ├── screenshots.py   # Screenshot endpoints
│       └── export.py        # Export endpoint
├── requirements.txt
├── README.md
└── test_*.py                # Test scripts
```

## Usage Examples

### Create a test case
```bash
curl -X POST http://localhost:8000/api/test-cases \
  -H "Content-Type: application/json" \
  -d '{"test_number": "TC01", "description": "My test case"}'
```

### Add a step
```bash
curl -X POST http://localhost:8000/api/test-cases/1/steps \
  -H "Content-Type: application/json" \
  -d '{"step_number": 1, "description": "First step"}'
```

### Upload a screenshot
```bash
curl -X POST http://localhost:8000/api/steps/1/screenshots \
  -F "file=@/path/to/image.png"
```

### Export to Excel
```bash
curl -X POST http://localhost:8000/api/export \
  -H "Content-Type: application/json" \
  -d '{"test_case_ids": [1, 2, 3]}' \
  --output export.xlsx
```

## Notes

- The API uses the same database as the Streamlit app (`shared/database/test_cases.db`)
- Screenshots are stored in `uploads/` directory (project root)
- All endpoints return JSON except `/api/export` and `/api/screenshots/{id}/file` which return files
- CORS is enabled for all origins (configure in production)

