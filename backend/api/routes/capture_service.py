"""
Routes for capture service management (start/stop/status).
"""

from fastapi import APIRouter, HTTPException, Body
import sys
import subprocess
import psutil
import requests
from pathlib import Path
from typing import Dict, Any
from pydantic import BaseModel

# Add project root to path to import shared modules
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

router = APIRouter(prefix="/api/capture-service", tags=["capture-service"])

# Configuration
SERVICE_URL = "http://localhost:5001"
SERVICE_SCRIPT = project_root / "screenshot-capture-service" / "screenshot-service.py"
START_SCRIPT = project_root / "screenshot-capture-service" / "start-service.py"
STOP_SCRIPT = project_root / "screenshot-capture-service" / "stop-service.py"


def is_service_running() -> bool:
    """Check if the capture service API is running."""
    try:
        response = requests.get(f"{SERVICE_URL}/status", timeout=2)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def is_service_process_running() -> bool:
    """Check if the service process is running."""
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = proc.info.get('cmdline', [])
                if cmdline and 'screenshot-service.py' in ' '.join(cmdline):
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    except Exception:
        pass
    return False


@router.get("/status")
async def get_service_status() -> Dict[str, Any]:
    """
    Get the status of the capture service.
    
    Returns:
        - service_running: bool - Whether the service API is running
        - watcher_running: bool - Whether the watcher is running
        - service_process_running: bool - Whether the service process exists
    """
    service_running = is_service_running()
    service_process_running = is_service_process_running()
    
    watcher_running = False
    if service_running:
        try:
            response = requests.get(f"{SERVICE_URL}/status", timeout=2)
            if response.status_code == 200:
                data = response.json()
                watcher_running = data.get('watcher_running', False)
        except requests.exceptions.RequestException:
            pass
    
    return {
        "service_running": service_running,
        "service_process_running": service_process_running,
        "watcher_running": watcher_running,
        "status": "on" if service_running else ("starting" if service_process_running else "off")
    }


@router.get("/capture-directory")
async def get_capture_directory() -> Dict[str, Any]:
    """
    Get the capture directory path where screenshots are saved.
    
    Returns:
        - capture_directory: str - Path to the capture directory
    """
    try:
        # Import config from screenshot-capture-service
        config_path = project_root / "screenshot-capture-service" / "config.py"
        if not config_path.exists():
            raise HTTPException(
                status_code=500,
                detail="Config file not found"
            )
        
        # Read config to get SCREENSHOTS_DIR
        import importlib.util
        spec = importlib.util.spec_from_file_location("config", config_path)
        config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config)
        
        capture_dir = config.SCREENSHOTS_DIR.expanduser()
        
        return {
            "capture_directory": str(config.SCREENSHOTS_DIR),
            "capture_directory_expanded": str(capture_dir)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get capture directory: {str(e)}"
        )


class OpenFolderRequest(BaseModel):
    path: str


@router.post("/open-folder")
async def open_folder(request: OpenFolderRequest) -> Dict[str, Any]:
    """
    Open a folder in Finder (macOS).
    
    Request body:
        - path: str - Path to the folder to open
    
    Returns:
        - success: bool
        - message: str
    """
    try:
        folder_path = request.path
        
        # Expand user path
        from pathlib import Path
        expanded_path = Path(folder_path).expanduser()
        
        if not expanded_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Folder does not exist: {expanded_path}"
            )
        
        # Open folder in Finder (macOS)
        subprocess.run(
            ['open', str(expanded_path)],
            check=True
        )
        
        return {
            "success": True,
            "message": f"Folder opened in Finder: {expanded_path}"
        }
    except subprocess.CalledProcessError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to open folder: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error opening folder: {str(e)}"
        )


@router.get("/get-file")
async def get_file(path: str, _t: str = None):
    """
    Get a file from the capture directory.
    
    Query params:
        - path: str - Path to the file
        - _t: str (optional) - Cache busting parameter (ignored)
    
    Returns:
        - File content
    """
    try:
        from pathlib import Path as PathLib
        from fastapi.responses import FileResponse
        
        # Expand user path and resolve
        file_path = PathLib(path).expanduser().resolve()
        
        if not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"File not found: {path}"
            )
        
        if not file_path.is_file():
            raise HTTPException(
                status_code=400,
                detail=f"Path is not a file: {path}"
            )
        
        # Security check: ensure file is in capture directory
        config_path = project_root / "screenshot-capture-service" / "config.py"
        if config_path.exists():
            import importlib.util
            spec = importlib.util.spec_from_file_location("config", config_path)
            config = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(config)
            capture_dir = config.SCREENSHOTS_DIR.expanduser().resolve()
            
            try:
                file_path.resolve().relative_to(capture_dir.resolve())
            except ValueError:
                raise HTTPException(
                    status_code=403,
                    detail=f"File is not in capture directory. File: {file_path}, Capture dir: {capture_dir}"
                )
        
        return FileResponse(
            str(file_path),
            media_type='image/png' if file_path.suffix.lower() == '.png' else 'image/jpeg'
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting file: {str(e)}"
        )


@router.get("/capture-files")
async def list_capture_files() -> Dict[str, Any]:
    """
    List all image files in the capture directory.
    
    Returns:
        - files: List of file information (name, path, size, modified)
    """
    try:
        # Import config from screenshot-capture-service
        config_path = project_root / "screenshot-capture-service" / "config.py"
        if not config_path.exists():
            raise HTTPException(
                status_code=500,
                detail="Config file not found"
            )
        
        # Read config to get SCREENSHOTS_DIR
        import importlib.util
        spec = importlib.util.spec_from_file_location("config", config_path)
        config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config)
        
        capture_dir = config.SCREENSHOTS_DIR.expanduser()
        
        if not capture_dir.exists():
            return {
                "files": [],
                "directory": str(capture_dir)
            }
        
        # List all image files
        image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
        files = []
        
        for file_path in capture_dir.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in image_extensions:
                stat = file_path.stat()
                files.append({
                    "name": file_path.name,
                    "path": str(file_path),
                    "size": stat.st_size,
                    "modified": stat.st_mtime
                })
        
        # Sort by modified time (newest first)
        files.sort(key=lambda x: x['modified'], reverse=True)
        
        return {
            "files": files,
            "directory": str(capture_dir)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list capture files: {str(e)}"
        )


@router.post("/start")
async def start_service() -> Dict[str, Any]:
    """
    Start the capture service API.
    
    Returns:
        - success: bool
        - message: str
    """
    # Check if already running
    if is_service_running():
        return {
            "success": True,
            "message": "Service is already running"
        }
    
    # Check if process is already starting
    if is_service_process_running():
        return {
            "success": False,
            "message": "Service process is already running but not responding. Please check manually."
        }
    
    # Start the service
    try:
        if not START_SCRIPT.exists():
            raise HTTPException(
                status_code=500,
                detail=f"Start script not found: {START_SCRIPT}"
            )
        
        # Start service in background
        subprocess.Popen(
            ["python3", str(START_SCRIPT)],
            cwd=str(START_SCRIPT.parent),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        return {
            "success": True,
            "message": "Service is starting. Please wait a few seconds and check status."
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start service: {str(e)}"
        )


@router.post("/stop")
async def stop_service() -> Dict[str, Any]:
    """
    Stop the capture service API.
    
    Returns:
        - success: bool
        - message: str
    """
    # First stop the watcher if running
    if is_service_running():
        try:
            response = requests.post(f"{SERVICE_URL}/stop", timeout=5)
            # Continue even if this fails
        except requests.exceptions.RequestException:
            pass
    
    # Stop the service process
    try:
        if not STOP_SCRIPT.exists():
            raise HTTPException(
                status_code=500,
                detail=f"Stop script not found: {STOP_SCRIPT}"
            )
        
        result = subprocess.run(
            ["python3", str(STOP_SCRIPT)],
            cwd=str(STOP_SCRIPT.parent),
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            return {
                "success": True,
                "message": "Service stopped successfully"
            }
        else:
            return {
                "success": False,
                "message": f"Stop script returned error: {result.stderr}"
            }
    except subprocess.TimeoutExpired:
        raise HTTPException(
            status_code=500,
            detail="Stop script timed out"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to stop service: {str(e)}"
        )

