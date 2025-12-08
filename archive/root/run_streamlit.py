#!/usr/bin/env python3
"""
Launcher script for Streamlit app.
Run this from the project root: python3 run_streamlit.py
"""

import subprocess
import sys
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent
streamlit_app = project_root / "streamlit" / "app.py"

# Change to project root to ensure relative paths work
import os
os.chdir(project_root)

# Run streamlit
subprocess.run([sys.executable, "-m", "streamlit", "run", str(streamlit_app)] + sys.argv[1:])

