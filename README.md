# Test Case Documentation Tool

A modern web application for creating and managing SimCorp Dimension test case documentation with Excel export capability and integrated screenshot capture.

## 🎯 Features

- **Test Case Management**: Create, edit, and organize test cases with unique numbers and descriptions
- **Step Management**: Add multiple steps to each test case with detailed descriptions
- **Screenshot Integration**: Attach screenshots to steps with drag-and-drop support
- **Metadata Support**: Add modules used, calculation logic, and configuration elements
- **Excel Export**: Export selected test cases to professional Excel workbooks (summary + individual test sheets)
- **Screenshot Capture Mode**: Integrated macOS screenshot capture with automatic naming and description
- **Load Step Feature**: Quickly load steps from pre-captured screenshots in Capture_TC/ directory
- **Bulk Operations**: Select and export or delete multiple test cases at once

## 🏗️ Architecture

The application consists of three main components:

1. **Frontend** (Next.js + React)
   - Modern, responsive web interface
   - Real-time updates and drag-and-drop functionality
   - Dark mode support

2. **Backend API** (FastAPI + Python)
   - RESTful API for all operations
   - SQLite database for data persistence
   - Excel generation and file handling

3. **Screenshot Capture Service** (Python + Flask)
   - macOS screenshot interception
   - Automatic file organization
   - Integration with Test Case Manager

## 📋 Prerequisites

- **macOS** 12+ (for screenshot capture service)
- **Python** 3.10+
- **Node.js** 18+ and npm
- **Git**

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/louisgarnier/Documentation.git
cd Documentation
```

### 2. Backend Setup

```bash
# Install Python dependencies
cd backend
pip install -r requirements.txt

# Initialize database (automatic on first run)
# Database will be created at: shared/database/test_cases.db

# Start the API server
python3 -m uvicorn api.main:app --reload --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 3. Frontend Setup

```bash
# Install Node.js dependencies
cd frontend
npm install

# Start the development server
npm run dev
```

The frontend will be available at: http://localhost:3000

### 4. Screenshot Capture Service (Optional)

The screenshot capture service is automatically managed from the web interface. No manual setup required!

See [USER_GUIDE.md](USER_GUIDE.md) for detailed configuration instructions.

## 📁 Project Structure

```
Documentation/
├── backend/                    # FastAPI backend
│   ├── api/                   # API routes and models
│   ├── requirements.txt       # Python dependencies
│   └── README.md              # Backend documentation
├── frontend/                   # Next.js frontend
│   ├── src/                   # Source code
│   │   ├── components/        # React components
│   │   ├── api/               # API client
│   │   └── types/             # TypeScript types
│   ├── package.json           # Node.js dependencies
│   └── README.md              # Frontend documentation
├── screenshot-capture-service/ # Screenshot capture service
│   ├── config.py              # Service configuration
│   ├── screenshot-service.py  # Flask API service
│   ├── screenshot-watcher.py  # Desktop file watcher
│   └── README.md              # Service documentation
├── shared/                     # Shared components
│   ├── models.py              # Database models
│   ├── excel_export.py        # Excel generation
│   └── database/              # SQLite database
├── uploads/                    # Screenshot storage
├── docs/                       # Documentation files
├── README.md                   # This file
└── USER_GUIDE.md              # User guide and configuration
```

## 🎮 Usage

### Basic Workflow

1. **Start the Application**
   ```bash
   # Terminal 1 - Backend
   cd backend && uvicorn api.main:app --reload --port 8000
   
   # Terminal 2 - Frontend
   cd frontend && npm run dev
   ```

2. **Create a Test Case**
   - Open http://localhost:3000
   - Click "Create New Test Case"
   - Enter test number and description

3. **Add Steps**
   - Open a test case
   - Click "Add New Step" or use "Load Step" to load from Capture_TC/
   - Fill in step details

4. **Add Screenshots**
   - Click "Add Screenshot" on any step
   - Upload from computer or select from Capture_TC/
   - Drag and drop images directly

5. **Export to Excel**
   - Select test cases using checkboxes
   - Click "Export to Excel"
   - Download the generated workbook

### Screenshot Capture Mode

1. **Activate Capture Mode**
   - Open any test case page
   - Click "Capture Mode: OFF" button
   - Service starts automatically

2. **Take Screenshots**
   - Press `Shift+Cmd+4` (macOS screenshot)
   - Popup appears automatically
   - Enter screenshot name and description
   - Files saved to `~/Desktop/Capture_TC/`

3. **Load Steps from Captures**
   - Click "Load Step" button
   - Select images and description file
   - Step created automatically with screenshots

See [USER_GUIDE.md](USER_GUIDE.md) for detailed instructions.

## 🔧 Configuration

### Backend Configuration

- **Port**: 8000 (default)
- **Database**: `shared/database/test_cases.db` (auto-created)
- **Uploads**: `uploads/` directory (auto-created)

### Frontend Configuration

- **Port**: 3000 (default)
- **API URL**: `http://localhost:8000` (configured in `src/api/client.ts`)

### Screenshot Capture Service

See [screenshot-capture-service/README.md](screenshot-capture-service/README.md) and [USER_GUIDE.md](USER_GUIDE.md) for complete configuration details.

**Key Settings** (in `screenshot-capture-service/config.py`):
- **Capture Directory**: `~/Desktop/Capture_TC/` (default)
- **Service API Port**: 5001 (default)
- **Log File**: `~/Documents/TestCaseScreenshots/screenshot-capture.log`

## 📚 Documentation

- **[USER_GUIDE.md](USER_GUIDE.md)** - Complete user guide and configuration instructions
- **[backend/README.md](backend/README.md)** - Backend API documentation
- **[screenshot-capture-service/README.md](screenshot-capture-service/README.md)** - Screenshot capture service documentation
- **[GIT_WORKFLOW.md](GIT_WORKFLOW.md)** - Git workflow instructions

## 🧪 Testing

### Backend Tests

```bash
cd backend
python3 test_all.py
```

### Frontend

The frontend runs in development mode with hot reload. Open http://localhost:3000 to test.

### Screenshot Capture Service

```bash
cd screenshot-capture-service
python3 test_all_phases.py
```

## 🐛 Troubleshooting

### Backend Issues

- **Port 8000 already in use**: Change port in `uvicorn` command or stop conflicting service
- **Database errors**: Check `shared/database/` permissions
- **Import errors**: Ensure all dependencies are installed: `pip install -r requirements.txt`

### Frontend Issues

- **Port 3000 already in use**: Change port: `npm run dev -- -p 3001`
- **API connection errors**: Verify backend is running on port 8000
- **Build errors**: Clear cache: `rm -rf .next node_modules && npm install`

### Screenshot Capture Service Issues

See [USER_GUIDE.md](USER_GUIDE.md#troubleshooting) for detailed troubleshooting.

## 🔐 Security Notes

- The application is designed for local development use
- CORS is enabled for all origins (restrict in production)
- Database and uploads are stored locally
- Screenshot capture service requires macOS permissions

## 📝 License

This project is part of the Test Case Documentation Tool.

## 🤝 Contributing

For issues, feature requests, or contributions, please use the GitHub issue tracker.

## 📊 Status

✅ **Production Ready**

- ✅ Backend API (FastAPI)
- ✅ Frontend (Next.js)
- ✅ Screenshot Capture Service
- ✅ Excel Export
- ✅ Load Step Feature
- ✅ Bulk Operations

## 🔗 Repository

https://github.com/louisgarnier/Documentation.git
