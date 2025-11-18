#!/usr/bin/env python3
"""
Start the Screenshot Capture Service
"""
import subprocess
import sys
import os
from pathlib import Path

# Get the directory where this script is located
script_dir = Path(__file__).parent
service_script = script_dir / "screenshot-service.py"

# Check if service is already running
try:
    import psutil
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info.get('cmdline', [])
            if cmdline and 'screenshot-service.py' in ' '.join(cmdline):
                print(f"Service is already running (PID: {proc.info['pid']})")
                sys.exit(0)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
except ImportError:
    # psutil not available, try basic check
    pass

# Start the service
print(f"Starting Screenshot Capture Service...")
print(f"Service will run on http://localhost:5001")
print(f"Press Ctrl+C to stop the service")

try:
    subprocess.run([sys.executable, str(service_script)], check=True)
except KeyboardInterrupt:
    print("\nService stopped by user")
except Exception as e:
    print(f"Error starting service: {e}")
    sys.exit(1)

