"""
Screenshot Capture Watcher
Surveille le Desktop pour détecter les nouvelles captures d'écran et affiche un popup pour nommer et décrire
"""
import time
import re
import shutil
import tempfile
import os
import json
import signal
import sys
import threading
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent
import subprocess
import config
from logger import get_logger

# Initialize logger
logger = get_logger("WATCHER")

# Track processed files to avoid duplicates
processed_files = set()

# Global flag to check if watcher should be active
# This will be set by the service when starting/stopping
# Using threading.Lock for thread-safe access
watcher_active = True
watcher_lock = threading.Lock()


class ScreenshotHandler(FileSystemEventHandler):
    """Handler pour détecter les nouvelles captures d'écran"""
    
    def __init__(self):
        self.logger = get_logger("WATCHER")
    
    def is_screenshot_file(self, file_path):
        """Vérifie si le fichier est une capture d'écran macOS"""
        path = Path(file_path)
        
        # Vérifier extension
        if path.suffix.lower() not in config.SCREENSHOT_EXTENSIONS:
            return False
        
        # Vérifier pattern de nom macOS
        filename = path.name
        
        # Pattern 1: "Screen Shot" (deux mots) avec format 12h (AM/PM)
        pattern1 = r"Screen Shot \d{4}-\d{2}-\d{2} at \d{1,2}\.\d{2}\.\d{2} (AM|PM)\.png"
        
        # Pattern 2: "Screen Shot" (deux mots) avec format 24h
        pattern2 = r"Screen Shot \d{4}-\d{2}-\d{2} at \d{1,2}\.\d{2}\.\d{2}\.png"
        
        # Pattern 3: "Screenshot" (un mot) avec format 24h (format moderne macOS)
        pattern3 = r"Screenshot \d{4}-\d{2}-\d{2} at \d{1,2}\.\d{2}\.\d{2}\.png"
        
        return bool(re.match(pattern1, filename, re.IGNORECASE) or 
                   re.match(pattern2, filename, re.IGNORECASE) or
                   re.match(pattern3, filename, re.IGNORECASE))
    
    def on_created(self, event):
        """Appelé quand un nouveau fichier est créé"""
        global watcher_active, watcher_lock
        
        # Vérifier si le watcher est actif (thread-safe)
        with watcher_lock:
            active = watcher_active
        if not active:
            self.logger.debug("Watcher is inactive, ignoring file creation event")
            return
        
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        # Logger tous les fichiers créés pour déboguer
        self.logger.info(f"File created event: {file_path.name}")
        
        # Ignorer les fichiers temporaires macOS (commencent par un point)
        if file_path.name.startswith('.'):
            self.logger.debug(f"Ignoring temporary file: {file_path.name}")
            return
        
        # Ignorer si déjà traité
        if str(file_path) in processed_files:
            self.logger.debug(f"File already processed: {file_path.name}")
            return
        
        # Vérifier IMMÉDIATEMENT si le watcher est toujours actif (thread-safe)
        with watcher_lock:
            active = watcher_active
        if not active:
            self.logger.debug("Watcher is inactive, ignoring file creation event (early check)")
            return
        
        # Attendre un peu pour s'assurer que le fichier est complètement écrit
        time.sleep(0.5)
        
        # Vérifier à nouveau après l'attente (le watcher peut avoir été arrêté pendant l'attente)
        with watcher_lock:
            active = watcher_active
        if not active:
            self.logger.info("Watcher was deactivated during file processing, ignoring")
            return
        
        # Vérifier que le fichier existe toujours et est une capture
        if not file_path.exists():
            self.logger.debug(f"File no longer exists: {file_path.name}")
            return
        
        # Vérifier si c'est une capture d'écran
        is_screenshot = self.is_screenshot_file(file_path)
        self.logger.debug(f"File {file_path.name} is screenshot: {is_screenshot}")
        
        if not is_screenshot:
            return
        
        # Vérifier une dernière fois avant de traiter (thread-safe)
        with watcher_lock:
            active = watcher_active
        if not active:
            self.logger.info("Watcher was deactivated before processing screenshot, ignoring")
            return
        
        # Marquer comme traité AVANT d'afficher le popup pour éviter les doublons
        processed_files.add(str(file_path))
        
        self.logger.info(f"Screenshot detected: {file_path.name}")
        
        # Vérifier à nouveau que le watcher est actif (au cas où il a été désactivé entre temps)
        with watcher_lock:
            active = watcher_active
        if not active:
            self.logger.info("Watcher was deactivated, ignoring screenshot")
            return
        
        # Afficher popup pour nom et description
        self.show_naming_popup(file_path)
    
    def on_moved(self, event):
        """Appelé quand un fichier est déplacé/renommé (macOS crée d'abord un fichier temporaire puis le renomme)"""
        global watcher_active, watcher_lock
        
        # Vérifier si le watcher est actif (thread-safe)
        with watcher_lock:
            active = watcher_active
        if not active:
            self.logger.debug("Watcher is inactive, ignoring file move event")
            return
        
        if event.is_directory:
            return
        
        dest_path = Path(event.dest_path)
        
        # Si le fichier source était temporaire et que la destination est une capture
        if event.src_path and Path(event.src_path).name.startswith('.'):
            if self.is_screenshot_file(dest_path):
                self.logger.info(f"Screenshot file moved from temp: {dest_path.name}")
                
                # Ignorer si déjà traité
                if str(dest_path) in processed_files:
                    self.logger.debug(f"File already processed: {dest_path.name}")
                    return
                
                # Vérifier à nouveau que le watcher est actif
                with watcher_lock:
                    active = watcher_active
                if not active:
                    self.logger.debug("Watcher is inactive, ignoring file move event")
                    return
                
                # Attendre un peu pour s'assurer que le fichier est complètement écrit
                time.sleep(0.5)
                
                # Vérifier à nouveau après l'attente
                with watcher_lock:
                    active = watcher_active
                if not active:
                    self.logger.info("Watcher was deactivated during file processing, ignoring")
                    return
                
                # Vérifier que le fichier existe toujours
                if not dest_path.exists():
                    self.logger.debug(f"File no longer exists: {dest_path.name}")
                    return
                
                # Marquer comme traité AVANT d'afficher le popup pour éviter les doublons
                processed_files.add(str(dest_path))
                
                # Vérifier une dernière fois avant de traiter
                with watcher_lock:
                    active = watcher_active
                if not active:
                    self.logger.info("Watcher was deactivated before processing screenshot, ignoring")
                    return
                
                self.logger.info(f"Screenshot detected (from move): {dest_path.name}")
                
                # Afficher popup pour nom et description
                self.show_naming_popup(dest_path)
    
    def show_naming_popup(self, screenshot_path):
        """Affiche un popup unifié pour saisir toutes les informations de la capture"""
        global watcher_active, watcher_lock
        
        # Vérifier une dernière fois que le watcher est actif avant d'afficher le popup (thread-safe)
        with watcher_lock:
            active = watcher_active
        if not active:
            self.logger.info("Watcher was deactivated, cancelling popup")
            return
        
        self.logger.info("Opening unified screenshot information dialog")
        
        # Utiliser le script Python avec tkinter qui s'exécute dans un processus séparé
        script_dir = Path(__file__).parent.resolve()
        dialog_script = script_dir / "description_dialog.py"
        
        if not dialog_script.exists():
            self.logger.error(f"Description dialog script not found: {dialog_script}")
            return
        
        try:
            # Exécuter le script Python dans un processus séparé qui peut afficher une fenêtre GUI
            result = subprocess.run(
                ['python3', str(dialog_script.resolve()), screenshot_path.name],
                capture_output=True,
                text=True,
                timeout=600,
                stdin=subprocess.DEVNULL
            )
            
            if result.returncode != 0:
                self.logger.info("Screenshot info popup cancelled by user")
                return
            
            # Parser le JSON retourné
            if not result.stdout:
                self.logger.error("Dialog returned empty output")
                return
                
            stdout_text = result.stdout.strip()
            if not stdout_text:
                self.logger.error("Dialog returned empty output after stripping")
                return
                
            try:
                info = json.loads(stdout_text)
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to parse dialog response: {str(e)}")
                self.logger.error(f"Dialog stdout was: {result.stdout}")
                return
            
            # Safely extract values, handling None and empty strings
            screenshot_name = str(info.get("screenshot_name") or "").strip()
            test_case = str(info.get("test_case") or "").strip()
            step_number = info.get("step_number")  # Will be None, step numbers are auto-generated
            long_description = str(info.get("long_description") or "").strip()
            
            # Générer le nom de fichier (step number is auto-generated, not included in filename)
            # Format: TC05_customname or TC05
            if test_case and test_case != "Backend not available":
                # Use Test Case as base
                if screenshot_name:
                    filename = f"{test_case}_{screenshot_name}"
                else:
                    filename = test_case
            elif screenshot_name:
                # Si seulement screenshot_name
                filename = screenshot_name
            else:
                # Fallback: utiliser le nom original sans extension
                filename = screenshot_path.stem
            
            # Ensure filename is never empty
            if not filename or filename.strip() == "":
                filename = screenshot_path.stem
            
            # Logger les données saisies
            self.logger.info("Step 1: User input received - All fields collected")
            self.logger.info(
                "User input details",
                extra={'data': {
                    'screenshot_name': screenshot_name,
                    'test_case': test_case,
                    'step_number': step_number,
                    'long_description_length': len(long_description),
                    'generated_filename': filename
                }}
            )
            
            # Sauvegarder les fichiers
            self.logger.info(f"Step 2: Starting file save process for '{filename}'")
            self.save_screenshot(
                screenshot_path, 
                filename,
                test_case,
                step_number,
                long_description
            )
            
        except subprocess.TimeoutExpired:
            self.logger.warning("Screenshot info popup timeout - user did not respond")
            return
        except Exception as e:
            self.logger.error(f"Error showing screenshot info popup: {str(e)}", exc_info=True)
            return
    
    def save_screenshot(self, screenshot_path, name, test_case, step_number, long_description):
        """Sauvegarde la capture et toutes les informations dans le dossier dédié"""
        try:
            self.logger.info(f"Step 2.1: Preparing to save files - Source: {screenshot_path}")
            
            # Créer les noms de fichiers
            image_name = f"{name}.png"
            description_name = f"{name}{config.DESCRIPTION_FILE_EXTENSION}"
            
            # Chemins de destination
            dest_image = config.SCREENSHOTS_DIR / image_name
            dest_description = config.SCREENSHOTS_DIR / description_name
            
            self.logger.info(f"Step 2.2: Destination directory: {config.SCREENSHOTS_DIR}")
            
            # Vérifier si les fichiers existent déjà
            if dest_image.exists():
                self.logger.info(f"Step 2.3: File {image_name} already exists, adding suffix")
                # Ajouter un suffixe numérique
                counter = 1
                while dest_image.exists():
                    image_name = f"{name}_{counter}.png"
                    dest_image = config.SCREENSHOTS_DIR / image_name
                    counter += 1
                description_name = f"{Path(image_name).stem}{config.DESCRIPTION_FILE_EXTENSION}"
                dest_description = config.SCREENSHOTS_DIR / description_name
                self.logger.info(f"Step 2.4: Using new names - Image: {image_name}, Description: {description_name}")
            
            # Vérifier que le fichier source existe toujours
            if not screenshot_path.exists():
                self.logger.error(f"Step 2.5 ERROR: Source file no longer exists: {screenshot_path}")
                return
            
            # Déplacer l'image du Desktop vers le dossier de destination
            self.logger.info(f"Step 2.6: Moving image from Desktop to {dest_image}")
            shutil.move(str(screenshot_path), str(dest_image))
            self.logger.info(f"Step 2.7: Image moved successfully to {dest_image}")
            
            # Créer le fichier de description avec seulement le texte de description
            self.logger.info(f"Step 2.8: Creating description file: {dest_description}")
            with open(dest_description, 'w', encoding='utf-8') as f:
                f.write(long_description)
            
            total_chars = len(long_description)
            self.logger.info(f"Step 2.9: Description file created with {total_chars} characters")
            
            self.logger.info(
                "Step 3: Files saved successfully - Process complete",
                extra={'data': {
                    'image': str(dest_image),
                    'description': str(dest_description),
                    'test_case': test_case,
                    'step_number': step_number,
                    'image_size_bytes': dest_image.stat().st_size if dest_image.exists() else 0,
                    'description_size_bytes': dest_description.stat().st_size if dest_description.exists() else 0
                }}
            )
            
        except Exception as e:
            self.logger.error(
                f"Failed to save screenshot: {str(e)}",
                exc_info=True
            )


# Global observer reference for signal handler
observer_instance = None

def signal_handler(signum, frame):
    """Handler pour les signaux d'arrêt"""
    global watcher_active, observer_instance, watcher_lock
    logger.info(f"Received signal {signum}, stopping watcher immediately...")
    
    # Désactiver IMMÉDIATEMENT pour empêcher tout traitement (thread-safe)
    with watcher_lock:
        watcher_active = False
    
    # Arrêter l'observer immédiatement pour éviter de traiter de nouveaux événements
    if observer_instance:
        try:
            logger.info("Stopping observer from signal handler...")
            observer_instance.stop()
            observer_instance.join(timeout=0.5)
        except Exception as e:
            logger.error(f"Error stopping observer: {e}")
    
    # Sortir immédiatement avec os._exit pour forcer l'arrêt (ne déclenche pas les handlers finally)
    logger.info("Exiting watcher process immediately")
    os._exit(0)

def main():
    """Point d'entrée principal du watcher"""
    global watcher_active, observer_instance, watcher_lock
    
    # Enregistrer les handlers de signaux pour arrêt propre
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    with watcher_lock:
        watcher_active = True
    logger.info("Starting screenshot watcher")
    
    # Vérifier que le dossier Desktop existe
    if not config.DESKTOP_DIR.exists():
        logger.error(f"Desktop directory not found: {config.DESKTOP_DIR}")
        return
    
    # Créer l'observer
    event_handler = ScreenshotHandler()
    observer = Observer()
    observer.schedule(event_handler, str(config.DESKTOP_DIR), recursive=False)
    observer_instance = observer  # Garder une référence globale
    
    # Démarrer l'observation
    observer.start()
    logger.info(f"Watching directory: {config.DESKTOP_DIR}")
    
    try:
        # Garder le script actif
        while True:
            with watcher_lock:
                active = watcher_active
            if not active:
                logger.info("Watcher active flag set to False, stopping...")
                break
            time.sleep(0.5)
    except KeyboardInterrupt:
        logger.info("Watcher stopped by user (KeyboardInterrupt)")
        with watcher_lock:
            watcher_active = False
    finally:
        # Arrêter l'observer proprement
        logger.info("Stopping observer...")
        with watcher_lock:
            watcher_active = False  # Désactiver IMMÉDIATEMENT pour éviter de traiter de nouveaux événements
        # Arrêter l'observer avant de continuer
        observer.stop()
        # Attendre un peu pour que les événements en cours se terminent
        observer.join(timeout=1)
        logger.info("Watcher shutdown complete")


if __name__ == "__main__":
    main()

