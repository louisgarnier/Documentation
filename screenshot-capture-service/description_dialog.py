#!/usr/bin/env python3
"""
Dialog unifié pour saisir toutes les informations de la capture
S'exécute dans un processus séparé pour pouvoir afficher une fenêtre GUI
"""
import sys
import json
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import requests

def fetch_test_cases(backend_url="http://localhost:8000"):
    """Fetch test cases from the backend API"""
    try:
        response = requests.get(f"{backend_url}/api/test-cases", timeout=2)
        if response.status_code == 200:
            test_cases = response.json()
            # Return list of test case numbers for the dropdown
            return [tc.get("test_number", "") for tc in test_cases if tc.get("test_number")]
        else:
            return []
    except (requests.exceptions.RequestException, requests.exceptions.Timeout):
        # Backend not available or connection error
        return []


def get_screenshot_info(screenshot_filename):
    """Affiche une fenêtre avec tous les champs pour saisir les infos de la capture"""
    root = tk.Tk()
    root.title("Screenshot Information")
    root.geometry("700x500")
    root.attributes('-topmost', True)
    
    result = {
        "screenshot_name": None,
        "test_case": None,
        "step_number": None,
        "long_description": None,
        "cancelled": False
    }
    
    # Frame principal avec padding
    main_frame = tk.Frame(root, padx=20, pady=15)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Label titre
    title_label = tk.Label(main_frame, text=f"Screenshot: {screenshot_filename}", font=("Arial", 11, "bold"))
    title_label.pack(pady=(0, 15))
    
    # Fetch test cases from backend
    test_cases_list = fetch_test_cases()
    
    # Ligne 1: Screenshot Name, Test Case
    row1_frame = tk.Frame(main_frame)
    row1_frame.pack(fill=tk.X, pady=(0, 10))
    
    # Screenshot Name
    name_label = tk.Label(row1_frame, text="Screenshot Name:", font=("Arial", 10))
    name_label.pack(side=tk.LEFT, padx=(0, 5))
    name_entry = tk.Entry(row1_frame, width=20, font=("Arial", 10))
    name_entry.pack(side=tk.LEFT, padx=(0, 15))
    
    # Test Case (Dropdown)
    testcase_label = tk.Label(row1_frame, text="Test Case:", font=("Arial", 10))
    testcase_label.pack(side=tk.LEFT, padx=(0, 5))
    testcase_combo = ttk.Combobox(row1_frame, width=15, font=("Arial", 10), values=test_cases_list)
    testcase_combo.pack(side=tk.LEFT, padx=(0, 15))
    if test_cases_list:
        testcase_combo.set(test_cases_list[0])  # Set first test case as default
    else:
        # Show warning if backend is not available
        testcase_combo.set("Backend not available")
        testcase_combo.config(state="disabled")
    
    # Ligne 2: Long Description (textarea)
    long_desc_label = tk.Label(main_frame, text="Long Description:", font=("Arial", 10))
    long_desc_label.pack(anchor=tk.W, pady=(10, 5))
    long_desc_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=80, height=12, font=("Arial", 10))
    long_desc_text.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
    
    # Focus sur le premier champ
    name_entry.focus()
    
    def on_ok():
        result["screenshot_name"] = name_entry.get().strip() or ""
        # Get test case from combobox (handle disabled state)
        if testcase_combo.cget("state") == "disabled":
            result["test_case"] = ""
        else:
            test_case_value = testcase_combo.get()
            if test_case_value:
                test_case_value = test_case_value.strip()
            else:
                test_case_value = ""
            # Don't use "Backend not available" as test case value
            if test_case_value == "Backend not available":
                result["test_case"] = ""
            else:
                result["test_case"] = test_case_value
        # Step number is no longer collected - will be auto-generated
        result["step_number"] = None
        result["long_description"] = long_desc_text.get("1.0", tk.END).strip() or ""
        root.destroy()
    
    def on_cancel():
        result["cancelled"] = True
        root.destroy()
    
    # Boutons
    button_frame = tk.Frame(main_frame)
    button_frame.pack(pady=(10, 0))
    
    ok_button = tk.Button(button_frame, text="OK", command=on_ok, width=12, font=("Arial", 11))
    ok_button.pack(side=tk.LEFT, padx=5)
    
    cancel_button = tk.Button(button_frame, text="Cancel", command=on_cancel, width=12, font=("Arial", 11))
    cancel_button.pack(side=tk.LEFT, padx=5)
    
    # Bind Enter (Cmd+Enter pour OK, Enter seul pour nouvelle ligne dans textarea)
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
    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: description_dialog.py <screenshot_filename>")
        sys.exit(1)
    
    screenshot_filename = sys.argv[1]
    info = get_screenshot_info(screenshot_filename)
    
    if info is not None:
        # Retourner les données en JSON pour faciliter le parsing
        print(json.dumps(info))
        sys.exit(0)
    else:
        sys.exit(1)

