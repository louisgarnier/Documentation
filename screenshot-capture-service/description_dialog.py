#!/usr/bin/env python3
"""
Dialog pour saisir une description multiligne
S'exécute dans un processus séparé pour pouvoir afficher une fenêtre GUI
"""
import sys
import tkinter as tk
from tkinter import scrolledtext, messagebox

def get_description(filename):
    """Affiche une fenêtre avec textarea pour saisir la description"""
    root = tk.Tk()
    root.title("Screenshot Description")
    root.geometry("600x400")
    root.attributes('-topmost', True)
    
    # Label
    label = tk.Label(root, text=f"Enter a description for '{filename}':", font=("Arial", 12))
    label.pack(pady=10)
    
    # Textarea avec scrollbar
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=15, font=("Arial", 11))
    text_area.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
    text_area.focus()
    
    result = {"description": None, "cancelled": False}
    
    def on_ok():
        result["description"] = text_area.get("1.0", tk.END).strip()
        root.destroy()
    
    def on_cancel():
        result["cancelled"] = True
        root.destroy()
    
    # Boutons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    
    ok_button = tk.Button(button_frame, text="OK", command=on_ok, width=10, font=("Arial", 11))
    ok_button.pack(side=tk.LEFT, padx=5)
    
    cancel_button = tk.Button(button_frame, text="Cancel", command=on_cancel, width=10, font=("Arial", 11))
    cancel_button.pack(side=tk.LEFT, padx=5)
    
    # Bind Enter (Cmd+Enter pour OK, Enter seul pour nouvelle ligne)
    root.bind('<Command-Return>', lambda e: on_ok())
    root.bind('<Escape>', lambda e: on_cancel())
    
    # Centrer la fenêtre
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()
    
    if result["cancelled"]:
        return None
    return result["description"]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: description_dialog.py <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    description = get_description(filename)
    
    if description is not None:
        print(description)
        sys.exit(0)
    else:
        sys.exit(1)

