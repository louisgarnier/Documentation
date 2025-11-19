"""
Routes for capture service management (start/stop/status).
"""

from fastapi import APIRouter, HTTPException
import sys
import subprocess
import psutil
import requests
from pathlib import Path
from typing import Dict, Any

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

