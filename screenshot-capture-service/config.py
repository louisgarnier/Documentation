"""
Configuration for Screenshot Capture Service
"""
import os
from pathlib import Path

# API Configuration
API_PORT = 5001
API_HOST = "localhost"

# Directories
HOME_DIR = Path.home()
DESKTOP_DIR = HOME_DIR / "Desktop"
SCREENSHOTS_DIR = HOME_DIR / "Desktop" / "Capture_TC"
# Keep log file in Documents to avoid cluttering Desktop
LOG_FILE = (HOME_DIR / "Documents" / "TestCaseScreenshots" / "screenshot-capture.log")

# Logging Configuration
LOG_MAX_SIZE = 10 * 1024 * 1024  # 10 MB
LOG_BACKUP_COUNT = 5
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR

# Screenshot Detection
SCREENSHOT_PATTERN = r"Screen Shot \d{4}-\d{2}-\d{2} at \d{1,2}\.\d{2}\.\d{2} (AM|PM)\.png"
SCREENSHOT_EXTENSIONS = [".png"]

# File Naming
DESCRIPTION_FILE_EXTENSION = ".txt"

# Ensure directories exist
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
# Ensure log directory exists
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

