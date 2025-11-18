#!/usr/bin/env python3
"""
Script to clean base64-encoded XLSX data from calculation_logic field.

This script identifies and removes base64-encoded XLSX data that was stored
during the Excel editor testing phase, replacing it with empty strings.
"""

import sqlite3
import sys
import os
from pathlib import Path

# Add shared to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "shared"))

from models import get_db_connection

def is_base64_xlsx(data: str) -> bool:
    """Check if a string looks like base64-encoded XLSX data."""
    if not data or len(data) < 100:
        return False
    
    # Base64 XLSX files typically start with "UEsDB" (PK header encoded)
    # and are usually very long (>1000 chars)
    if data.startswith("UEsDB") and len(data) > 1000:
        return True
    
    # Also check for other base64 patterns
    if len(data) > 5000 and all(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=" for c in data[:100]):
        return True
    
    return False

def clean_base64_data():
    """Clean base64-encoded XLSX data from calculation_logic field."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get all steps with calculation_logic
    cursor.execute("""
        SELECT id, step_number, test_case_id, calculation_logic 
        FROM test_steps 
        WHERE calculation_logic IS NOT NULL AND calculation_logic != ''
    """)
    
    steps = cursor.fetchall()
    cleaned_count = 0
    
    print(f"Found {len(steps)} steps with calculation_logic data")
    print("\nChecking for base64-encoded XLSX data...\n")
    
    for step_id, step_number, test_case_id, calc_logic in steps:
        if is_base64_xlsx(calc_logic):
            print(f"  Step {step_id} (test_case_id={test_case_id}, step_number={step_number}): BASE64 detected (length={len(calc_logic)})")
            # Clear the base64 data
            cursor.execute("""
                UPDATE test_steps 
                SET calculation_logic = NULL 
                WHERE id = ?
            """, (step_id,))
            cleaned_count += 1
        else:
            print(f"  Step {step_id} (test_case_id={test_case_id}, step_number={step_number}): Text data (length={len(calc_logic)}, preview={calc_logic[:50]}...)")
    
    if cleaned_count > 0:
        conn.commit()
        print(f"\n✅ Cleaned {cleaned_count} steps with base64-encoded XLSX data")
    else:
        print("\n✅ No base64 data found to clean")
    
    conn.close()
    return cleaned_count

if __name__ == "__main__":
    print("=" * 60)
    print("Cleaning base64-encoded XLSX data from calculation_logic")
    print("=" * 60)
    print()
    
    try:
        cleaned = clean_base64_data()
        print(f"\n{'=' * 60}")
        print(f"Cleanup complete! {cleaned} steps cleaned.")
        print(f"{'=' * 60}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

