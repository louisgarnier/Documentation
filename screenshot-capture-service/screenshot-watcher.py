"""
Screenshot Capture Watcher
Surveille le Desktop pour détecter les nouvelles captures d'écran et affiche un popup pour nommer et décrire
"""
import time
import re
import shutil
import tempfile
import os
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
        
        # Attendre un peu pour s'assurer que le fichier est complètement écrit
        time.sleep(0.5)
        
        # Vérifier que le fichier existe toujours et est une capture
        if not file_path.exists():
            self.logger.debug(f"File no longer exists: {file_path.name}")
            return
        
        # Vérifier si c'est une capture d'écran
        is_screenshot = self.is_screenshot_file(file_path)
        self.logger.debug(f"File {file_path.name} is screenshot: {is_screenshot}")
        
        if not is_screenshot:
            return
        
        # Marquer comme traité
        processed_files.add(str(file_path))
        
        self.logger.info(f"Screenshot detected: {file_path.name}")
        
        # Afficher popup pour nom et description
        self.show_naming_popup(file_path)
    
    def on_moved(self, event):
        """Appelé quand un fichier est déplacé/renommé (macOS crée d'abord un fichier temporaire puis le renomme)"""
        if event.is_directory:
            return
        
        dest_path = Path(event.dest_path)
        
        # Si le fichier source était temporaire et que la destination est une capture
        if event.src_path and Path(event.src_path).name.startswith('.'):
            if self.is_screenshot_file(dest_path):
                self.logger.info(f"Screenshot file moved from temp: {dest_path.name}")
                # Traiter comme une création (mais sans passer par on_created pour éviter la double détection)
                if str(dest_path) not in processed_files:
                    processed_files.add(str(dest_path))
                    self.logger.info(f"Screenshot detected: {dest_path.name}")
                    self.show_naming_popup(dest_path)
    
    def show_naming_popup(self, screenshot_path):
        """Affiche un popup natif macOS pour nommer et décrire la capture"""
        self.logger.info("Popup opened for screenshot naming")
        
        # Popup pour le nom (utilise osascript pour popup natif macOS)
        applescript_name = f'''
        tell application "System Events"
            activate
            set theAnswer to text returned of (display dialog "Enter a name for this screenshot (without extension):" & return & return & "File: {screenshot_path.name}" default answer "" buttons {{"Cancel", "OK"}} default button "OK" with title "Screenshot Name")
        end tell
        '''
        
        try:
            result = subprocess.run(
                ['osascript', '-e', applescript_name],
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            
            if result.returncode != 0:
                self.logger.info("Popup cancelled by user or error occurred")
                return
            
            filename = result.stdout.strip()
            
            if not filename:
                # Afficher warning et quitter
                applescript_warning = '''
                tell application "System Events"
                    activate
                    display dialog "Name cannot be empty. Screenshot will not be processed." buttons {{"OK"}} default button "OK" with title "Warning" with icon caution
                end tell
                '''
                subprocess.run(['osascript', '-e', applescript_warning], timeout=10)
                self.logger.warning("Empty name provided, skipping")
                return
            
        except subprocess.TimeoutExpired:
            self.logger.warning("Popup timeout - user did not respond")
            return
        except Exception as e:
            self.logger.error(f"Error showing name popup: {str(e)}", exc_info=True)
            return
        
        # Popup pour la description (avec vrai textarea multiligne via tkinter)
        self.logger.info("Opening description input dialog (multiline textarea)")
        
        # Utiliser le script Python avec tkinter qui s'exécute dans un processus séparé
        script_dir = Path(__file__).parent.resolve()
        dialog_script = script_dir / "description_dialog.py"
        
        if not dialog_script.exists():
            self.logger.error(f"Description dialog script not found: {dialog_script}")
            return
        
        try:
            # Exécuter le script Python dans un processus séparé qui peut afficher une fenêtre GUI
            # Utiliser le chemin absolu pour éviter les problèmes avec les espaces
            result = subprocess.run(
                ['python3', str(dialog_script.resolve()), filename],
                capture_output=True,
                text=True,
                timeout=600,
                # Important: ne pas capturer stdin pour permettre l'interaction GUI
                stdin=subprocess.DEVNULL
            )
            
            if result.returncode != 0:
                self.logger.info("Description popup cancelled by user")
                return
            
            description = result.stdout.strip()
            
            if not description:
                self.logger.info("Empty description provided")
                return
            
        except subprocess.TimeoutExpired:
            self.logger.warning("Description popup timeout - user did not respond")
            return
        except Exception as e:
            self.logger.error(f"Error showing description popup: {str(e)}", exc_info=True)
            return
        
        # Logger les données saisies
        self.logger.info("Step 1: User input received - Name and description collected")
        self.logger.info(
            "User input details",
            extra={'data': {
                'name': filename,
                'description_length': len(description) if description else 0,
                'description_preview': (description[:50] + '...') if description and len(description) > 50 else (description if description else '(empty)')
            }}
        )
        
        # Sauvegarder les fichiers
        self.logger.info(f"Step 2: Starting file save process for '{filename}'")
        self.save_screenshot(screenshot_path, filename.strip(), description.strip() if description else "")
    
    def save_screenshot(self, screenshot_path, name, description):
        """Sauvegarde la capture et sa description dans le dossier dédié"""
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
            
            # Créer le fichier de description
            self.logger.info(f"Step 2.8: Creating description file: {dest_description}")
            with open(dest_description, 'w', encoding='utf-8') as f:
                f.write(description)
            self.logger.info(f"Step 2.9: Description file created with {len(description)} characters")
            
            self.logger.info(
                "Step 3: Files saved successfully - Process complete",
                extra={'data': {
                    'image': str(dest_image),
                    'description': str(dest_description),
                    'image_size_bytes': dest_image.stat().st_size if dest_image.exists() else 0,
                    'description_size_bytes': dest_description.stat().st_size if dest_description.exists() else 0
                }}
            )
            
        except Exception as e:
            self.logger.error(
                f"Failed to save screenshot: {str(e)}",
                exc_info=True
            )


def main():
    """Point d'entrée principal du watcher"""
    logger.info("Starting screenshot watcher")
    
    # Vérifier que le dossier Desktop existe
    if not config.DESKTOP_DIR.exists():
        logger.error(f"Desktop directory not found: {config.DESKTOP_DIR}")
        return
    
    # Créer l'observer
    event_handler = ScreenshotHandler()
    observer = Observer()
    observer.schedule(event_handler, str(config.DESKTOP_DIR), recursive=False)
    
    # Démarrer l'observation
    observer.start()
    logger.info(f"Watching directory: {config.DESKTOP_DIR}")
    
    try:
        # Garder le script actif
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Watcher stopped by user")
        observer.stop()
    
    observer.join()
    logger.info("Watcher shutdown complete")


if __name__ == "__main__":
    main()

