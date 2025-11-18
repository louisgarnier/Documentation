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
        return False, "Watcher is already running"
    
    try:
        # Get the directory where this script is located
        script_dir = Path(__file__).parent
        watcher_script = script_dir / "screenshot-watcher.py"
        
        # Start watcher as subprocess
        watcher_process = subprocess.Popen(
            ["python3", str(watcher_script)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return True, f"Watcher started with PID {watcher_process.pid}"
    except Exception as e:
        return False, f"Failed to start watcher: {str(e)}"


def stop_watcher():
    """Stop the screenshot watcher process"""
    global watcher_process
    
    if not is_watcher_running():
        return False, "Watcher is not running"
    
    try:
        # Terminate the process
        watcher_process.terminate()
        
        # Wait for graceful shutdown (5 seconds max)
        try:
            watcher_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            # Force kill if it doesn't stop
            watcher_process.kill()
            watcher_process.wait()
        
        watcher_process = None
        return True, "Watcher stopped successfully"
    except Exception as e:
        return False, f"Failed to stop watcher: {str(e)}"


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "screenshot-capture-service"})


@app.route("/status", methods=["GET"])
def status():
    """Get current status of the service"""
    watcher_running = is_watcher_running()
    return jsonify({
        "watcher_running": watcher_running,
        "watcher_pid": watcher_process.pid if watcher_running and watcher_process else None
    })


@app.route("/start", methods=["POST"])
def start():
    """Start the screenshot watcher"""
    success, message = start_watcher()
    
    if success:
        return jsonify({"status": "started", "message": message}), 200
    else:
        return jsonify({"status": "error", "message": message}), 400


@app.route("/stop", methods=["POST"])
def stop():
    """Stop the screenshot watcher"""
    success, message = stop_watcher()
    
    if success:
        return jsonify({"status": "stopped", "message": message}), 200
    else:
        return jsonify({"status": "error", "message": message}), 400


if __name__ == "__main__":
    print(f"Starting Screenshot Capture Service on {config.API_HOST}:{config.API_PORT}")
    app.run(host=config.API_HOST, port=config.API_PORT, debug=False)

