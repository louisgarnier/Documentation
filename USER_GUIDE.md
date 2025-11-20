# User Guide - Test Case Documentation Tool

Complete guide for setting up and using the Test Case Documentation Tool, including all configuration requirements.

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Screenshot Capture Service Setup](#screenshot-capture-service-setup)
5. [Daily Usage](#daily-usage)
6. [Troubleshooting](#troubleshooting)

## 🖥️ System Requirements

### Operating System
- **macOS 12+** (required for screenshot capture service)
- Full disk access permissions for Desktop folder monitoring

### Software Requirements
- **Python 3.10+**
- **Node.js 18+** and npm
- **Git**

### Python Dependencies
- FastAPI
- SQLite3 (included with Python)
- openpyxl (Excel generation)
- flask, flask-cors (screenshot service)
- watchdog, psutil (file monitoring)

### Node.js Dependencies
- Next.js 14+
- React 18+
- TypeScript

## 📦 Installation

### 1. Clone Repository

```bash
git clone https://github.com/louisgarnier/Documentation.git
cd Documentation
```

### 2. Backend Installation

```bash
cd backend
pip install -r requirements.txt
```

**Verify installation:**
```bash
python3 -m pip list | grep -E "fastapi|uvicorn|openpyxl"
```

### 3. Frontend Installation

```bash
cd frontend
npm install
```

**Verify installation:**
```bash
npm list next react
```

### 4. Screenshot Capture Service Installation

```bash
cd screenshot-capture-service
pip install -r requirements.txt
```

**Verify installation:**
```bash
python3 -m pip list | grep -E "flask|watchdog|psutil"
```

## ⚙️ Configuration

### Backend Configuration

#### Port Configuration

The backend runs on **port 8000** by default. To change:

```bash
# In backend directory
python3 -m uvicorn api.main:app --reload --port 8001
```

Update frontend API URL in `frontend/src/api/client.ts`:
```typescript
const API_BASE_URL = 'http://localhost:8001';
```

#### Database Location

- **Default**: `shared/database/test_cases.db`
- **Auto-created** on first run
- **Backups**: Stored in `backups/` directory

#### Upload Directory

- **Default**: `uploads/` (project root)
- **Structure**: `uploads/test_{id}/step_{id}/screenshot_*.png`
- **Auto-created** when needed

### Frontend Configuration

#### Port Configuration

The frontend runs on **port 3000** by default. To change:

```bash
# In frontend directory
npm run dev -- -p 3001
```

#### API URL Configuration

Edit `frontend/src/api/client.ts`:

```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
```

Or set environment variable:
```bash
export NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Screenshot Capture Service Configuration

#### Configuration File

Edit `screenshot-capture-service/config.py`:

```python
# API Configuration
API_PORT = 5001  # Change if port is in use
API_HOST = "localhost"

# Directories
HOME_DIR = Path.home()
DESKTOP_DIR = HOME_DIR / "Desktop"
SCREENSHOTS_DIR = HOME_DIR / "Desktop" / "Capture_TC"  # ⚠️ IMPORTANT: This is where screenshots are saved

# Logging
LOG_FILE = (HOME_DIR / "Documents" / "TestCaseScreenshots" / "screenshot-capture.log")
LOG_MAX_SIZE = 10 * 1024 * 1024  # 10 MB
LOG_BACKUP_COUNT = 5
```

#### ⚠️ Critical Configuration: Capture_TC/ Directory

**Default Location**: `~/Desktop/Capture_TC/`

**To Change Location**:

1. Edit `screenshot-capture-service/config.py`:
   ```python
   SCREENSHOTS_DIR = Path("/path/to/your/capture/directory")
   ```

2. **Important**: The directory must:
   - Exist (or be auto-creatable)
   - Be writable by your user
   - Be accessible from the Desktop (for macOS screenshot detection)

3. **Verify Configuration**:
   ```bash
   python3 -c "from screenshot-capture-service.config import SCREENSHOTS_DIR; print(SCREENSHOTS_DIR)"
   ```

#### Service API Port

- **Default**: 5001
- **Check if port is available**:
  ```bash
  lsof -i :5001
  ```
- **Change port** in `config.py` if needed:
  ```python
  API_PORT = 5002  # Use different port
  ```

## 🎥 Screenshot Capture Service Setup

### Initial Setup Checklist

Before using the screenshot capture service, verify:

- [ ] **Python 3.10+ installed**: `python3 --version`
- [ ] **Dependencies installed**: `pip3 list | grep -E "flask|watchdog|psutil"`
- [ ] **Capture_TC/ directory exists**: `ls ~/Desktop/Capture_TC/`
- [ ] **Desktop folder accessible**: `ls ~/Desktop`
- [ ] **Backend running**: `curl http://localhost:8000/health`
- [ ] **Frontend running**: `curl http://localhost:3000`
- [ ] **Port 5001 available**: `lsof -i :5001 || echo "Port available"`

### macOS Permissions

The screenshot capture service requires:

1. **Full Disk Access** (for Desktop folder monitoring):
   - System Settings → Privacy & Security → Full Disk Access
   - Add Terminal (or your IDE) to allowed apps

2. **Accessibility** (if using automation):
   - System Settings → Privacy & Security → Accessibility
   - Add Terminal (or your IDE) to allowed apps

### Service Startup

**The service starts automatically from the web interface!**

1. Open any test case page
2. Click "Capture Mode: OFF" button
3. Service API starts automatically
4. Watcher starts automatically
5. Status indicators show "ON" / "ACTIVE"

**Manual Startup** (if needed):

```bash
cd screenshot-capture-service
python3 start-service.py
```

### Service Verification

**Check Service Status**:
```bash
curl http://localhost:5001/status
```

**Check Backend Integration**:
```bash
curl http://localhost:8000/api/capture-service/status
```

**View Logs**:
```bash
python3 screenshot-capture-service/view-logs.py -n 50
```

## 📖 Daily Usage

### Starting the Application

**Terminal 1 - Backend**:
```bash
cd backend
python3 -m uvicorn api.main:app --reload --port 8000
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm run dev
```

**Open Browser**: http://localhost:3000

### Using Screenshot Capture Mode

1. **Navigate to Test Case**
   - Open any test case from the home page

2. **Activate Capture Mode**
   - Click "Capture Mode: OFF" button (top right)
   - Wait for status to show "ON" / "ACTIVE"

3. **Take Screenshots**
   - Press `Shift+Cmd+4` (macOS screenshot shortcut)
   - Popup appears automatically
   - Enter:
     - Test Case Number (e.g., "TC05")
     - Step Number (e.g., "1")
     - Screenshot Name (e.g., "orderinput")
     - Description (optional)
   - Click "Save"

4. **Files Saved**
   - Image: `~/Desktop/Capture_TC/TC05_step1_orderinput.png`
   - Description: `~/Desktop/Capture_TC/TC05_step1_orderinput.txt`

5. **Load Step from Captures**
   - Click "Load Step" button
   - Select images from Capture_TC/
   - Select description file (optional)
   - Edit description if needed
   - Click "Create Step"

6. **Deactivate Capture Mode**
   - Click "Capture Mode: ON" button
   - Service stops automatically

### Using Load Step Feature

1. **Prepare Files**
   - Ensure images are in `~/Desktop/Capture_TC/`
   - Optionally create `.txt` description files

2. **Open Test Case**
   - Navigate to the test case where you want to add a step

3. **Click "Load Step"**
   - Modal opens showing files from Capture_TC/

4. **Select Images**
   - Click on image thumbnails to select (multiple selection)
   - Selected images show checkmark

5. **Select Description File** (optional)
   - Click on a `.txt` file to load its content
   - Description auto-fills in the editor
   - You can edit the description

6. **Or Upload from Computer**
   - Click "Browse Files" under "Or select from computer"
   - Select images and/or text files
   - Files are automatically copied to Capture_TC/

7. **Create Step**
   - Verify description is correct
   - Click "Create Step"
   - Step is created with automatic step number
   - Screenshots are associated automatically

### Exporting to Excel

1. **Select Test Cases**
   - Check boxes next to test cases on home page
   - Footer shows count of selected cases

2. **Export**
   - Click "Export to Excel" button
   - File downloads automatically
   - Filename: `test_cases_export_YYYYMMDD_HHMMSS.xlsx`

3. **Excel Structure**
   - **Summary Sheet**: Overview of all exported test cases
   - **Individual Sheets**: One sheet per test case with all steps and screenshots

### Deleting Test Cases

1. **Select Test Cases**
   - Check boxes next to test cases on home page

2. **Delete**
   - Click "Delete" button (red, next to Export button)
   - Confirm deletion in dialog
   - Test cases are permanently deleted
   - List refreshes automatically

## 🔍 Troubleshooting

### Backend Issues

#### Port 8000 Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill process (replace PID)
kill -9 <PID>

# Or use different port
python3 -m uvicorn api.main:app --reload --port 8001
```

#### Database Errors

```bash
# Check database file exists
ls -la shared/database/test_cases.db

# Check permissions
chmod 644 shared/database/test_cases.db

# Backup and recreate if corrupted
cp shared/database/test_cases.db backups/backup_$(date +%Y%m%d_%H%M%S).db
rm shared/database/test_cases.db
# Database will be recreated on next API call
```

#### Import Errors

```bash
# Reinstall dependencies
cd backend
pip install --upgrade -r requirements.txt
```

### Frontend Issues

#### Port 3000 Already in Use

```bash
# Use different port
npm run dev -- -p 3001
```

#### API Connection Errors

1. **Verify backend is running**:
   ```bash
   curl http://localhost:8000/health
   ```

2. **Check API URL** in `frontend/src/api/client.ts`

3. **Check CORS** in backend (should allow localhost:3000)

#### Build Errors

```bash
# Clear cache and reinstall
cd frontend
rm -rf .next node_modules package-lock.json
npm install
npm run dev
```

### Screenshot Capture Service Issues

#### Service Won't Start

1. **Check port 5001**:
   ```bash
   lsof -i :5001
   # If in use, change API_PORT in config.py
   ```

2. **Check Python dependencies**:
   ```bash
   pip3 list | grep -E "flask|watchdog|psutil"
   ```

3. **Check logs**:
   ```bash
   python3 screenshot-capture-service/view-logs.py -n 100
   ```

#### Popup Doesn't Appear

1. **Verify service is active**:
   - Check status in web interface
   - Should show "Capture Mode: ACTIVE"

2. **Check watcher is running**:
   ```bash
   ps aux | grep screenshot-watcher
   ```

3. **Check Desktop permissions**:
   - System Settings → Privacy & Security → Full Disk Access
   - Ensure Terminal/IDE has access

4. **Check logs**:
   ```bash
   python3 screenshot-capture-service/view-logs.py -f
   # Take a screenshot and watch logs
   ```

#### Files Not Saving to Capture_TC/

1. **Verify directory exists**:
   ```bash
   ls -la ~/Desktop/Capture_TC/
   ```

2. **Check permissions**:
   ```bash
   chmod 755 ~/Desktop/Capture_TC/
   ```

3. **Verify config.py**:
   ```python
   SCREENSHOTS_DIR = HOME_DIR / "Desktop" / "Capture_TC"
   ```

4. **Test write access**:
   ```bash
   touch ~/Desktop/Capture_TC/test.txt && rm ~/Desktop/Capture_TC/test.txt
   ```

#### Load Step Feature Issues

1. **No files showing in modal**:
   - Verify files are in `~/Desktop/Capture_TC/`
   - Check file extensions (.png, .jpg, .txt)
   - Refresh modal (close and reopen)

2. **Upload from computer fails**:
   - Check backend is running
   - Verify `uploads/` directory is writable
   - Check backend logs for errors

3. **Step creation fails**:
   - Verify at least one image is selected
   - Check description is not empty
   - Check backend logs: `tail -f backend/logs/*.log`

### General Issues

#### Application Won't Start

1. **Check all services are running**:
   ```bash
   # Backend
   curl http://localhost:8000/health
   
   # Frontend
   curl http://localhost:3000
   
   # Capture Service (if activated)
   curl http://localhost:5001/status
   ```

2. **Check logs**:
   - Backend: Check terminal output
   - Frontend: Check browser console (F12)
   - Capture Service: `python3 screenshot-capture-service/view-logs.py`

#### Database Locked Errors

```bash
# Close all connections
pkill -f uvicorn
pkill -f python

# Wait a few seconds
sleep 2

# Restart backend
cd backend && python3 -m uvicorn api.main:app --reload
```

## 📝 Configuration Summary

### Required Directories

- `shared/database/` - Database storage
- `uploads/` - Screenshot storage
- `~/Desktop/Capture_TC/` - Capture directory (auto-created)
- `~/Documents/TestCaseScreenshots/` - Log files (auto-created)

### Required Ports

- **8000**: Backend API (FastAPI)
- **3000**: Frontend (Next.js)
- **5001**: Screenshot Capture Service API (Flask, optional)

### Environment Variables

**Frontend** (optional):
```bash
export NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Backend** (optional):
```bash
export DATABASE_PATH=shared/database/test_cases.db
export UPLOAD_DIR=uploads/
```

## 🔗 Additional Resources

- [Backend API Documentation](backend/README.md)
- [Screenshot Capture Service Documentation](screenshot-capture-service/README.md)
- [Git Workflow](GIT_WORKFLOW.md)

## 💡 Tips

1. **Keep Capture_TC/ organized**: Regularly clean up old screenshots
2. **Use descriptive names**: When capturing, use clear names like "orderinput" not "screenshot1"
3. **Backup database**: Regularly backup `shared/database/test_cases.db`
4. **Monitor logs**: Check logs if something doesn't work: `python3 screenshot-capture-service/view-logs.py`
5. **Test in order**: Always start backend before frontend
6. **Check ports**: If something doesn't connect, verify ports aren't in use

## ❓ Getting Help

1. Check this guide first
2. Review logs: `python3 screenshot-capture-service/view-logs.py`
3. Check browser console (F12) for frontend errors
4. Verify all services are running
5. Check GitHub issues for known problems

