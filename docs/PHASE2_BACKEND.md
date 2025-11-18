# Phase 2: API Backend Development

## Status: ⏭️ Next Phase

This phase will create a Python API backend (FastAPI or Flask) that provides REST endpoints for the React frontend.

## Objectives

1. Choose backend framework (FastAPI recommended)
2. Create API structure
3. Implement REST endpoints
4. Connect to shared components
5. Test API endpoints

## Framework Choice

### FastAPI (Recommended)
- **Pros**: Modern, fast, automatic API docs, type hints
- **Cons**: None significant for this project

### Flask
- **Pros**: Simple, well-known
- **Cons**: More manual setup, no automatic docs

**Decision**: FastAPI

## API Endpoints to Implement

### Test Cases
- `GET /api/test-cases` - List all test cases
- `GET /api/test-cases/{id}` - Get test case details
- `POST /api/test-cases` - Create new test case
- `PUT /api/test-cases/{id}` - Update test case
- `DELETE /api/test-cases/{id}` - Delete test case

### Test Steps
- `GET /api/test-cases/{id}/steps` - Get all steps for a test case
- `POST /api/test-cases/{id}/steps` - Add step to test case
- `GET /api/steps/{id}` - Get step details
- `PUT /api/steps/{id}` - Update step
- `DELETE /api/steps/{id}` - Delete step
- `POST /api/steps/{id}/reorder` - Reorder steps

### Screenshots
- `POST /api/steps/{id}/screenshots` - Upload screenshot
- `GET /api/steps/{id}/screenshots` - Get screenshots for step
- `DELETE /api/screenshots/{id}` - Delete screenshot

### Export
- `POST /api/export` - Export selected test cases to Excel
  - Request body: `{ "test_case_ids": [1, 2, 3] }`
  - Response: Excel file download

## Implementation Steps

1. **Setup FastAPI project**
   ```bash
   cd backend
   pip install fastapi uvicorn python-multipart
   ```

2. **Create main API file**
   - `backend/api/main.py`
   - FastAPI app initialization
   - CORS configuration
   - Route registration

3. **Create route modules**
   - `backend/api/routes/test_cases.py`
   - `backend/api/routes/steps.py`
   - `backend/api/routes/screenshots.py`
   - `backend/api/routes/export.py`

4. **Implement endpoints**
   - Use shared/models.py functions
   - Handle request/response models
   - Error handling

5. **File upload handling**
   - Use FastAPI's `UploadFile` for screenshots
   - Save to `uploads/` directory (project root)

6. **Testing**
   - Test each endpoint
   - Use FastAPI's automatic docs at `/docs`

## File Structure

```
backend/
├── api/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── test_cases.py
│   │   ├── steps.py
│   │   ├── screenshots.py
│   │   └── export.py
│   └── models.py            # Pydantic models for request/response
├── requirements.txt
└── README.md
```

## Dependencies

```txt
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
python-multipart>=0.0.6
pydantic>=2.0.0
```

## Testing

Use FastAPI's automatic interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

Or use curl/Postman for manual testing.

## Next Steps

After Phase 2 completion:
- ✅ Phase 2: API Backend Development
- ⏭️ Phase 3: React Frontend Development

