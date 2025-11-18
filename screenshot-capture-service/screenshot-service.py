"""
Screenshot Capture Service - API Flask
Service léger pour gérer l'activation/désactivation du mode capture d'écran
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import os
import signal
import psutil
from pathlib import Path
import config
from logger import get_logger

# Initialize logger
logger = get_logger("SERVICE")

app = Flask(__name__)
CORS(app)  # Allow requests from web interface

# Global variable to track watcher process
watcher_process = None


def is_watcher_running():
    """Check if watcher process is running"""
    global watcher_process
    if watcher_process is None:
        return False
    return watcher_process.poll() is None


def start_watcher():
    """Start the screenshot watcher process"""
    global watcher_process
    
    if is_watcher_running():
        logger.warning("Attempted to start watcher but it's already running")
        return False, "Watcher is already running"
    
    try:
        # Get the directory where this script is located
        script_dir = Path(__file__).parent
        watcher_script = script_dir / "screenshot-watcher.py"
        
        logger.info("Starting watcher process")
        
        # Start watcher as subprocess
        watcher_process = subprocess.Popen(
            ["python3", str(watcher_script)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        logger.info(f"Watcher started successfully", extra={'data': {'pid': watcher_process.pid}})
        return True, f"Watcher started with PID {watcher_process.pid}"
    except Exception as e:
        logger.error(f"Failed to start watcher: {str(e)}", exc_info=True)
        return False, f"Failed to start watcher: {str(e)}"


def stop_watcher():
    """Stop the screenshot watcher process"""
    global watcher_process
    
    if not is_watcher_running():
        logger.warning("Attempted to stop watcher but it's not running")
        return False, "Watcher is not running"
    
    try:
        pid = watcher_process.pid
        logger.info(f"Stopping watcher process", extra={'data': {'pid': pid}})
        
        # Terminate the process
        watcher_process.terminate()
        
        # Wait for graceful shutdown (5 seconds max)
        try:
            watcher_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            # Force kill if it doesn't stop
            logger.warning("Watcher didn't stop gracefully, forcing kill")
            watcher_process.kill()
            watcher_process.wait()
        
        watcher_process = None
        logger.info("Watcher stopped successfully")
        return True, "Watcher stopped successfully"
    except Exception as e:
        logger.error(f"Failed to stop watcher: {str(e)}", exc_info=True)
        return False, f"Failed to stop watcher: {str(e)}"


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    logger.debug("Health check requested")
    return jsonify({"status": "healthy", "service": "screenshot-capture-service"})


@app.route("/status", methods=["GET"])
def status():
    """Get current status of the service"""
    watcher_running = is_watcher_running()
    status_data = {
        "watcher_running": watcher_running,
        "watcher_pid": watcher_process.pid if watcher_running and watcher_process else None
    }
    logger.debug("Status requested", extra={'data': status_data})
    return jsonify(status_data)


@app.route("/start", methods=["POST"])
def start():
    """Start the screenshot watcher"""
    logger.info("Start endpoint called")
    success, message = start_watcher()
    
    if success:
        logger.info("Mode activated successfully")
        return jsonify({"status": "started", "message": message}), 200
    else:
        logger.warning(f"Failed to activate mode: {message}")
        return jsonify({"status": "error", "message": message}), 400


@app.route("/stop", methods=["POST"])
def stop():
    """Stop the screenshot watcher"""
    logger.info("Stop endpoint called")
    success, message = stop_watcher()
    
    if success:
        logger.info("Mode deactivated successfully")
        return jsonify({"status": "stopped", "message": message}), 400
    else:
        logger.warning(f"Failed to deactivate mode: {message}")
        return jsonify({"status": "error", "message": message}), 400


if __name__ == "__main__":
    logger.info(f"Starting Screenshot Capture Service on {config.API_HOST}:{config.API_PORT}")
    print(f"Starting Screenshot Capture Service on {config.API_HOST}:{config.API_PORT}")
    app.run(host=config.API_HOST, port=config.API_PORT, debug=False)

