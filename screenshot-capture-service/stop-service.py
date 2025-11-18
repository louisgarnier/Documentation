#!/usr/bin/env python3
"""
Stop the Screenshot Capture Service
"""
import sys
import signal
import psutil
from logger import get_logger

# Initialize logger
logger = get_logger("STOP-SCRIPT")

def find_service_process():
    """Find the screenshot-service.py process"""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info.get('cmdline', [])
            if cmdline and 'screenshot-service.py' in ' '.join(cmdline):
                return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return None

def stop_service():
    """Stop the screenshot capture service"""
    logger.info("Attempting to stop Screenshot Capture Service")
    proc = find_service_process()
    
    if proc is None:
        logger.warning("Service is not running")
        print("Service is not running")
        return False
    
    try:
        pid = proc.pid
        logger.info(f"Stopping service (PID: {pid})")
        print(f"Stopping service (PID: {pid})...")
        proc.terminate()
        
        # Wait for graceful shutdown (5 seconds max)
        try:
            proc.wait(timeout=5)
            logger.info("Service stopped successfully", extra={'data': {"pid": pid, "method": "graceful"}})
            print("Service stopped successfully")
            return True
        except psutil.TimeoutExpired:
            # Force kill if it doesn't stop
            logger.warning("Service didn't stop gracefully, forcing kill", extra={'data': {"pid": pid}})
            print("Service didn't stop gracefully, forcing kill...")
            proc.kill()
            proc.wait()
            logger.info("Service stopped (forced)", extra={'data': {"pid": pid, "method": "forced"}})
            print("Service stopped (forced)")
            return True
    except psutil.NoSuchProcess:
        logger.warning("Service process not found (already stopped?)", extra={'data': {"pid": pid if 'pid' in locals() else None}})
        print("Service process not found (already stopped?)")
        return False
    except Exception as e:
        logger.error("Error stopping service", extra={'data': {"error": str(e)}}, exc_info=True)
        print(f"Error stopping service: {e}")
        return False

if __name__ == "__main__":
    success = stop_service()
    sys.exit(0 if success else 1)

