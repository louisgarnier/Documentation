#!/usr/bin/env python3
"""
Start the Screenshot Capture Service
"""
import subprocess
import sys
import os
from pathlib import Path
from logger import get_logger

# Initialize logger
logger = get_logger("START-SCRIPT")

# Get the directory where this script is located
script_dir = Path(__file__).parent
service_script = script_dir / "screenshot-service.py"

# Check if service is already running
service_running = False
running_pid = None

try:
    import psutil
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info.get('cmdline', [])
            if cmdline and 'screenshot-service.py' in ' '.join(cmdline):
                service_running = True
                running_pid = proc.info['pid']
                logger.info(f"Service is already running (PID: {running_pid})")
                print(f"Service is already running (PID: {running_pid})")
                sys.exit(0)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
except ImportError:
    # psutil not available, try basic check
    logger.warning("psutil not available, cannot check for running service")
    pass

# Start the service
logger.info("Starting Screenshot Capture Service", extra={'data': {
    "service_script": str(service_script),
    "python_executable": sys.executable
}})
print(f"Starting Screenshot Capture Service...")
print(f"Service will run on http://localhost:5001")
print(f"Press Ctrl+C to stop the service")

try:
    logger.info("Launching service process")
    subprocess.run([sys.executable, str(service_script)], check=True)
except KeyboardInterrupt:
    logger.info("Service stopped by user (KeyboardInterrupt)")
    print("\nService stopped by user")
except Exception as e:
    logger.error("Error starting service", extra={'data': {"error": str(e)}}, exc_info=True)
    print(f"Error starting service: {e}")
    sys.exit(1)

