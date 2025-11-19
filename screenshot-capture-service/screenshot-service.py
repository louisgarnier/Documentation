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
import time
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
    
    # Vérifier d'abord le processus global
    if watcher_process is not None:
        if watcher_process.poll() is None:
            return True
        else:
            # Processus mort, nettoyer
            watcher_process = None
    
    # Vérifier aussi s'il y a d'autres watchers qui tournent (au cas où)
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = proc.info.get('cmdline', [])
                if cmdline and 'screenshot-watcher.py' in ' '.join(cmdline):
                    # Trouvé un watcher qui tourne
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    except Exception:
        pass
    
    return False


def stop_all_watchers():
    """Stop ALL watcher processes (robust cleanup)"""
    global watcher_process
    
    stopped_count = 0
    
    # Arrêter le watcher global d'abord
    if watcher_process is not None:
        try:
            if watcher_process.poll() is None:
                logger.info(f"Stopping global watcher process (PID: {watcher_process.pid})")
                watcher_process.terminate()
                try:
                    watcher_process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    watcher_process.kill()
                    watcher_process.wait()
                stopped_count += 1
        except Exception as e:
            logger.warning(f"Error stopping global watcher: {e}")
        finally:
            watcher_process = None
    
    # Chercher et arrêter TOUS les autres watchers
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = proc.info.get('cmdline', [])
                if cmdline and 'screenshot-watcher.py' in ' '.join(cmdline):
                    pid = proc.info['pid']
                    logger.info(f"Found additional watcher process (PID: {pid}), stopping it...")
                    try:
                        proc.terminate()
                        try:
                            proc.wait(timeout=2)
                        except psutil.TimeoutExpired:
                            proc.kill()
                            proc.wait()
                        stopped_count += 1
                        logger.info(f"Stopped watcher process (PID: {pid})")
                    except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                        logger.debug(f"Could not stop process {pid}: {e}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    except Exception as e:
        logger.warning(f"Error finding/stopping watchers: {e}")
    
    if stopped_count > 0:
        logger.info(f"Stopped {stopped_count} watcher process(es)")
        # Attendre un peu pour s'assurer que les processus sont bien arrêtés
        time.sleep(0.5)
    
    return stopped_count

def start_watcher():
    """Start the screenshot watcher process"""
    global watcher_process
    
    # D'abord, arrêter TOUS les watchers existants (nettoyage robuste)
    logger.info("Checking for existing watchers and cleaning up...")
    stopped_count = stop_all_watchers()
    if stopped_count > 0:
        logger.info(f"Cleaned up {stopped_count} existing watcher(s) before starting new one")
    
    # Vérifier qu'il n'y a plus de watchers
    if is_watcher_running():
        logger.error("Watchers still running after cleanup, cannot start new watcher")
        return False, "Cannot start watcher: existing watchers could not be stopped"
    
    try:
        # Get the directory where this script is located
        script_dir = Path(__file__).parent
        watcher_script = script_dir / "screenshot-watcher.py"
        
        logger.info("Starting new watcher process")
        
        # Start watcher as subprocess
        watcher_process = subprocess.Popen(
            ["python3", str(watcher_script)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Attendre un peu pour vérifier que le processus démarre correctement
        time.sleep(0.5)
        
        if watcher_process.poll() is not None:
            # Le processus s'est arrêté immédiatement (erreur)
            error_output = watcher_process.stderr.read().decode() if watcher_process.stderr else "Unknown error"
            logger.error(f"Watcher process exited immediately: {error_output}")
            watcher_process = None
            return False, f"Watcher failed to start: {error_output}"
        
        logger.info(f"Watcher started successfully", extra={'data': {'pid': watcher_process.pid}})
        return True, f"Watcher started with PID {watcher_process.pid}"
    except Exception as e:
        logger.error(f"Failed to start watcher: {str(e)}", exc_info=True)
        watcher_process = None
        return False, f"Failed to start watcher: {str(e)}"


def stop_watcher():
    """Stop the screenshot watcher process (stops ALL watchers)"""
    global watcher_process
    
    if not is_watcher_running():
        logger.info("No watchers running")
        return True, "No watchers to stop"
    
    logger.info("Stopping all watcher processes...")
    
    # Utiliser la fonction robuste pour arrêter TOUS les watchers
    stopped_count = stop_all_watchers()
    
    if stopped_count > 0:
        logger.info(f"Successfully stopped {stopped_count} watcher process(es)")
        return True, f"Stopped {stopped_count} watcher process(es)"
    else:
        logger.warning("No watchers were stopped (they may have already stopped)")
        return True, "No active watchers found"


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
        return jsonify({"status": "stopped", "message": message}), 200
    else:
        logger.warning(f"Failed to deactivate mode: {message}")
        return jsonify({"status": "error", "message": message}), 400


if __name__ == "__main__":
    logger.info(f"Starting Screenshot Capture Service on {config.API_HOST}:{config.API_PORT}")
    print(f"Starting Screenshot Capture Service on {config.API_HOST}:{config.API_PORT}")
    app.run(host=config.API_HOST, port=config.API_PORT, debug=False)

