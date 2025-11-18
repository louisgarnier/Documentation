#!/usr/bin/env python3
"""
Stop the Screenshot Capture Service
"""
import sys
import signal
import psutil

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
    proc = find_service_process()
    
    if proc is None:
        print("Service is not running")
        return False
    
    try:
        print(f"Stopping service (PID: {proc.pid})...")
        proc.terminate()
        
        # Wait for graceful shutdown (5 seconds max)
        try:
            proc.wait(timeout=5)
            print("Service stopped successfully")
            return True
        except psutil.TimeoutExpired:
            # Force kill if it doesn't stop
            print("Service didn't stop gracefully, forcing kill...")
            proc.kill()
            proc.wait()
            print("Service stopped (forced)")
            return True
    except psutil.NoSuchProcess:
        print("Service process not found (already stopped?)")
        return False
    except Exception as e:
        print(f"Error stopping service: {e}")
        return False

if __name__ == "__main__":
    success = stop_service()
    sys.exit(0 if success else 1)

