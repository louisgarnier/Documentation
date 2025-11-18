"""
Screenshot Capture Watcher
Surveille le Desktop pour détecter les nouvelles captures d'écran et affiche un popup pour nommer et décrire
"""
import time
import re
import shutil
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import tkinter as tk
from tkinter import simpledialog, messagebox
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
        pattern = r"Screen Shot \d{4}-\d{2}-\d{2} at \d{1,2}\.\d{2}\.\d{2} (AM|PM)\.png"
        
        # Pattern alternatif (format plus récent)
        pattern_alt = r"Screen Shot \d{4}-\d{2}-\d{2} at \d{1,2}\.\d{2}\.\d{2}\.png"
        
        return bool(re.match(pattern, filename, re.IGNORECASE) or 
                   re.match(pattern_alt, filename, re.IGNORECASE))
    
    def on_created(self, event):
        """Appelé quand un nouveau fichier est créé"""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        # Ignorer si déjà traité
        if str(file_path) in processed_files:
            return
        
        # Attendre un peu pour s'assurer que le fichier est complètement écrit
        time.sleep(0.5)
        
        # Vérifier que le fichier existe toujours et est une capture
        if not file_path.exists():
            return
        
        if not self.is_screenshot_file(file_path):
            return
        
        # Marquer comme traité
        processed_files.add(str(file_path))
        
        self.logger.info(f"Screenshot detected: {file_path.name}")
        
        # Afficher popup pour nom et description
        self.show_naming_popup(file_path)
    
    def show_naming_popup(self, screenshot_path):
        """Affiche un popup pour nommer et décrire la capture"""
        self.logger.info("Popup opened for screenshot naming")
        
        # Créer fenêtre popup
        root = tk.Tk()
        root.withdraw()  # Cacher la fenêtre principale
        root.attributes('-topmost', True)  # Garder au-dessus
        
        # Popup pour le nom
        filename = simpledialog.askstring(
            "Screenshot Name",
            "Enter a name for this screenshot (without extension):\n\n"
            f"File: {screenshot_path.name}",
            parent=root
        )
        
        if filename is None:  # Utilisateur a annulé
            self.logger.info("Popup cancelled by user")
            root.destroy()
            return
        
        if not filename.strip():
            messagebox.showwarning("Warning", "Name cannot be empty. Screenshot will not be processed.")
            self.logger.warning("Empty name provided, skipping")
            root.destroy()
            return
        
        # Popup pour la description
        description = simpledialog.askstring(
            "Screenshot Description",
            f"Enter a description for '{filename}':",
            parent=root
        )
        
        if description is None:  # Utilisateur a annulé
            self.logger.info("Description popup cancelled by user")
            root.destroy()
            return
        
        root.destroy()
        
        # Logger les données saisies
        self.logger.info(
            "User input received",
            extra={'data': {
                'name': filename,
                'description': description if description else '(empty)'
            }}
        )
        
        # Sauvegarder les fichiers
        self.save_screenshot(screenshot_path, filename.strip(), description.strip() if description else "")
    
    def save_screenshot(self, screenshot_path, name, description):
        """Sauvegarde la capture et sa description dans le dossier dédié"""
        try:
            # Créer les noms de fichiers
            image_name = f"{name}.png"
            description_name = f"{name}{config.DESCRIPTION_FILE_EXTENSION}"
            
            # Chemins de destination
            dest_image = config.SCREENSHOTS_DIR / image_name
            dest_description = config.SCREENSHOTS_DIR / description_name
            
            # Vérifier si les fichiers existent déjà
            if dest_image.exists():
                # Ajouter un suffixe numérique
                counter = 1
                while dest_image.exists():
                    image_name = f"{name}_{counter}.png"
                    dest_image = config.SCREENSHOTS_DIR / image_name
                    counter += 1
                description_name = f"{Path(image_name).stem}{config.DESCRIPTION_FILE_EXTENSION}"
                dest_description = config.SCREENSHOTS_DIR / description_name
            
            # Déplacer/copier l'image
            shutil.move(str(screenshot_path), str(dest_image))
            
            # Créer le fichier de description
            with open(dest_description, 'w', encoding='utf-8') as f:
                f.write(description)
            
            self.logger.info(
                "Files saved successfully",
                extra={'data': {
                    'image': image_name,
                    'description': description_name
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

