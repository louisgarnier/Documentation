"""
Database models and setup for Test Case Documentation Tool.

This module handles SQLite database initialization and provides
functions for managing test cases, steps, and screenshots.
"""

import sqlite3
import os
from datetime import datetime
from typing import Optional, List, Dict, Tuple


# Database file path - relative to shared directory
DB_DIR = os.path.join(os.path.dirname(__file__), "database")
DB_FILE = os.path.join(DB_DIR, "test_cases.db")


def get_db_connection():
    """Create and return a database connection."""
    # Ensure database directory exists
    os.makedirs(DB_DIR, exist_ok=True)
    return sqlite3.connect(DB_FILE)


def init_database():
    """
    Initialize the database with all required tables.
    Creates tables if they don't exist.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create projects table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create test_cases table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_number TEXT NOT NULL UNIQUE,
            description TEXT NOT NULL,
            project_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL
        )
    """)
    
    # Migration: Add project_id column to existing test_cases table if it doesn't exist
    try:
        cursor.execute("ALTER TABLE test_cases ADD COLUMN project_id INTEGER")
    except sqlite3.OperationalError:
        # Column already exists, ignore
        pass
    
    # Migration: Create default "Unassigned" project and assign existing test cases
    # This runs after all tables are created, so projects table should exist
    try:
        # Check if default project exists
        cursor.execute("SELECT id FROM projects WHERE name = 'Unassigned'")
        default_project = cursor.fetchone()
        
        if not default_project:
            # Create default project
            cursor.execute("""
                INSERT INTO projects (name, description)
                VALUES ('Unassigned', 'Default project for existing test cases')
            """)
            default_project_id = cursor.lastrowid
        else:
            default_project_id = default_project[0]
        
        # Assign all test cases without project_id to default project
        cursor.execute("""
            UPDATE test_cases
            SET project_id = ?
            WHERE project_id IS NULL
        """, (default_project_id,))
    except sqlite3.OperationalError as e:
        # If something goes wrong, continue (migration will happen on next run)
        print(f"Migration note: {e}")
        pass
    
    # Create test_steps table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_steps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_case_id INTEGER NOT NULL,
            step_number INTEGER NOT NULL,
            description TEXT NOT NULL,
            modules TEXT,
            calculation_logic TEXT,
            configuration TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (test_case_id) REFERENCES test_cases(id) ON DELETE CASCADE,
            UNIQUE(test_case_id, step_number)
        )
    """)
    
    # Create step_screenshots table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS step_screenshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            step_id INTEGER NOT NULL,
            file_path TEXT NOT NULL,
            screenshot_name TEXT,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (step_id) REFERENCES test_steps(id) ON DELETE CASCADE
        )
    """)
    
    # Add screenshot_name column if it doesn't exist (migration for existing databases)
    try:
        cursor.execute("ALTER TABLE step_screenshots ADD COLUMN screenshot_name TEXT")
    except sqlite3.OperationalError:
        # Column already exists, ignore
        pass
    
    # Create index on project_id for better query performance
    try:
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_test_cases_project_id ON test_cases(project_id)")
    except sqlite3.OperationalError:
        pass
    
    conn.commit()
    conn.close()
    print(f"Database initialized successfully at: {DB_FILE}")


# Test Case Functions
def create_test_case(test_number: str, description: str, project_id: Optional[int] = None) -> int:
    """Create a new test case and return its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO test_cases (test_number, description, project_id)
        VALUES (?, ?, ?)
    """, (test_number, description, project_id))
    test_case_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return test_case_id


def get_all_test_cases(project_id: Optional[int] = None) -> List[Dict]:
    """Get all test cases, optionally filtered by project_id."""
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    if project_id is not None:
        cursor.execute("SELECT * FROM test_cases WHERE project_id = ? ORDER BY created_at DESC", (project_id,))
    else:
        cursor.execute("SELECT * FROM test_cases ORDER BY created_at DESC")
    
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_test_case_by_id(test_case_id: int) -> Optional[Dict]:
    """Get a test case by ID."""
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM test_cases WHERE id = ?", (test_case_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def update_test_case(test_case_id: int, test_number: str, description: str, project_id: Optional[int] = None) -> bool:
    """Update an existing test case."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if project_id is not None:
        cursor.execute("""
            UPDATE test_cases
            SET test_number = ?, description = ?, project_id = ?
            WHERE id = ?
        """, (test_number, description, project_id, test_case_id))
    else:
        cursor.execute("""
            UPDATE test_cases
            SET test_number = ?, description = ?
            WHERE id = ?
        """, (test_number, description, test_case_id))
    
    success = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return success


def move_test_case_to_project(test_case_id: int, project_id: Optional[int]) -> bool:
    """Move a test case to another project."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE test_cases
            SET project_id = ?
            WHERE id = ?
        """, (project_id, test_case_id))
        success = cursor.rowcount > 0
        conn.commit()
        return success
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def duplicate_test_case(test_case_id: int, new_test_number: str, target_project_id: Optional[int] = None) -> Optional[int]:
    """
    Duplicate a test case with all its steps and screenshots.
    Returns the ID of the new test case, or None if failed.
    """
    conn = get_db_connection()
    try:
        # Get original test case (using the same connection to avoid locking)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM test_cases WHERE id = ?", (test_case_id,))
        row = cursor.fetchone()
        if not row:
            return None
        
        original = dict(row)
        
        # Use target_project_id if provided, otherwise use original's project_id
        project_id = target_project_id if target_project_id is not None else original.get('project_id')
        
        # Check if new_test_number already exists, if so, make it unique
        cursor.execute("SELECT COUNT(*) as count FROM test_cases WHERE test_number = ?", (new_test_number,))
        count = cursor.fetchone()['count']
        if count > 0:
            # Generate unique test number by appending a number
            base_number = new_test_number
            counter = 1
            while True:
                unique_number = f"{base_number}_{counter}"
                cursor.execute("SELECT COUNT(*) as count FROM test_cases WHERE test_number = ?", (unique_number,))
                if cursor.fetchone()['count'] == 0:
                    new_test_number = unique_number
                    break
                counter += 1
        
        # Create new test case
        cursor.execute("""
            INSERT INTO test_cases (test_number, description, project_id)
            VALUES (?, ?, ?)
        """, (new_test_number, original['description'], project_id))
        new_test_case_id = cursor.lastrowid
        
        # Get all steps from original (using same connection)
        cursor.execute("SELECT * FROM steps WHERE test_case_id = ? ORDER BY step_number", (test_case_id,))
        original_steps = [dict(row) for row in cursor.fetchall()]
        
        # Duplicate each step
        for step in original_steps:
            cursor.execute("""
                INSERT INTO steps (test_case_id, step_number, description, modules, calculation_logic, configuration)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                new_test_case_id,
                step['step_number'],
                step['description'],
                step.get('modules'),
                step.get('calculation_logic'),
                step.get('configuration')
            ))
            new_step_id = cursor.lastrowid
            
            # Duplicate screenshots for this step
            cursor.execute("SELECT * FROM screenshots WHERE step_id = ?", (step['id'],))
            screenshots = [dict(row) for row in cursor.fetchall()]
            for screenshot in screenshots:
                cursor.execute("""
                    INSERT INTO screenshots (step_id, file_path, screenshot_name)
                    VALUES (?, ?, ?)
                """, (
                    new_step_id,
                    screenshot['file_path'],
                    screenshot.get('screenshot_name')
                ))
        
        conn.commit()
        return new_test_case_id
    except Exception as e:
        conn.rollback()
        print(f"Error duplicating test case: {e}")
        return None
    finally:
        conn.close()


def delete_test_case(test_case_id: int) -> bool:
    """Delete a test case and all its related steps and screenshots."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM test_cases WHERE id = ?", (test_case_id,))
    success = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return success


# Test Step Functions
def create_test_step(test_case_id: int, step_number: int, description: str,
                     modules: Optional[str] = None,
                     calculation_logic: Optional[str] = None,
                     configuration: Optional[str] = None) -> int:
    """Create a new test step and return its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO test_steps (test_case_id, step_number, description, 
                               modules, calculation_logic, configuration)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (test_case_id, step_number, description, modules, calculation_logic, configuration))
    step_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return step_id


def get_steps_by_test_case(test_case_id: int) -> List[Dict]:
    """Get all steps for a test case, ordered by step number."""
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM test_steps
        WHERE test_case_id = ?
        ORDER BY step_number
    """, (test_case_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_step_by_id(step_id: int) -> Optional[Dict]:
    """Get a step by ID."""
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM test_steps WHERE id = ?", (step_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def update_test_step(step_id: int, step_number: int, description: str,
                    modules: Optional[str] = None,
                    calculation_logic: Optional[str] = None,
                    configuration: Optional[str] = None) -> bool:
    """Update an existing test step."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE test_steps
        SET step_number = ?, description = ?, modules = ?,
            calculation_logic = ?, configuration = ?
        WHERE id = ?
    """, (step_number, description, modules, calculation_logic, configuration, step_id))
    success = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return success


def delete_test_step(step_id: int) -> bool:
    """Delete a test step and all its screenshots."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM test_steps WHERE id = ?", (step_id,))
    success = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return success


def swap_step_numbers(test_case_id: int, step_id_1: int, step_id_2: int) -> bool:
    """Swap the step numbers of two steps within the same test case."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get current step numbers
    cursor.execute("SELECT step_number FROM test_steps WHERE id = ?", (step_id_1,))
    step_1 = cursor.fetchone()
    cursor.execute("SELECT step_number FROM test_steps WHERE id = ?", (step_id_2,))
    step_2 = cursor.fetchone()
    
    if not step_1 or not step_2:
        conn.close()
        return False
    
    step_num_1 = step_1[0]
    step_num_2 = step_2[0]
    
    # Use a temporary value to avoid unique constraint violation
    temp_step_num = 99999
    
    try:
        # Set first step to temporary number
        cursor.execute("""
            UPDATE test_steps
            SET step_number = ?
            WHERE id = ?
        """, (temp_step_num, step_id_1))
        
        # Set second step to first step's number
        cursor.execute("""
            UPDATE test_steps
            SET step_number = ?
            WHERE id = ?
        """, (step_num_1, step_id_2))
        
        # Set first step to second step's number
        cursor.execute("""
            UPDATE test_steps
            SET step_number = ?
            WHERE id = ?
        """, (step_num_2, step_id_1))
        
        conn.commit()
        success = True
    except Exception as e:
        conn.rollback()
        success = False
    finally:
        conn.close()
    
    return success


def reorder_steps(test_case_id: int, step_order: List[int]) -> bool:
    """
    Reorder steps by providing a list of step IDs in the desired order.
    Step numbers will be reassigned sequentially starting from 1.
    
    Args:
        test_case_id: The test case ID
        step_order: List of step IDs in the desired order
    
    Returns:
        True if successful, False otherwise
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # First, set all step numbers to temporary values to avoid unique constraint
        temp_start = 10000
        for idx, step_id in enumerate(step_order):
            cursor.execute("""
                UPDATE test_steps
                SET step_number = ?
                WHERE id = ? AND test_case_id = ?
            """, (temp_start + idx, step_id, test_case_id))
        
        # Now assign the correct sequential numbers
        for idx, step_id in enumerate(step_order, start=1):
            cursor.execute("""
                UPDATE test_steps
                SET step_number = ?
                WHERE id = ? AND test_case_id = ?
            """, (idx, step_id, test_case_id))
        
        conn.commit()
        success = True
    except Exception as e:
        conn.rollback()
        success = False
    finally:
        conn.close()
    
    return success


# Screenshot Functions
def add_screenshot_to_step(step_id: int, file_path: str, screenshot_name: Optional[str] = None) -> int:
    """Add a screenshot to a step and return the screenshot ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO step_screenshots (step_id, file_path, screenshot_name)
        VALUES (?, ?, ?)
    """, (step_id, file_path, screenshot_name))
    screenshot_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return screenshot_id


def get_screenshots_by_step(step_id: int) -> List[Dict]:
    """Get all screenshots for a step."""
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM step_screenshots
        WHERE step_id = ?
        ORDER BY uploaded_at
    """, (step_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def update_screenshot_name(screenshot_id: int, screenshot_name: Optional[str]) -> bool:
    """Update the name of a screenshot."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE step_screenshots
        SET screenshot_name = ?
        WHERE id = ?
    """, (screenshot_name, screenshot_id))
    success = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return success


def delete_screenshot(screenshot_id: int) -> bool:
    """Delete a screenshot record."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM step_screenshots WHERE id = ?", (screenshot_id,))
    success = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return success


# Project Functions
def create_project(name: str, description: Optional[str] = None) -> int:
    """Create a new project and return its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO projects (name, description, updated_at)
        VALUES (?, ?, CURRENT_TIMESTAMP)
    """, (name, description))
    project_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return project_id


def get_all_projects() -> List[Dict]:
    """Get all projects with test case counts."""
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.*, 
               COUNT(tc.id) as test_case_count
        FROM projects p
        LEFT JOIN test_cases tc ON p.id = tc.project_id
        GROUP BY p.id
        ORDER BY p.created_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_project_by_id(project_id: int) -> Optional[Dict]:
    """Get a project by ID with test case count."""
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.*, 
               COUNT(tc.id) as test_case_count
        FROM projects p
        LEFT JOIN test_cases tc ON p.id = tc.project_id
        WHERE p.id = ?
        GROUP BY p.id
    """, (project_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def update_project(project_id: int, name: str, description: Optional[str] = None) -> bool:
    """Update an existing project."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE projects
        SET name = ?, description = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (name, description, project_id))
    success = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return success


def delete_project(project_id: int, move_to_project_id: Optional[int] = None) -> bool:
    """
    Delete a project. If move_to_project_id is provided, move test cases to that project.
    Otherwise, set test cases' project_id to NULL (they will be assigned to default project on next init).
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if move_to_project_id:
            # Move test cases to another project
            cursor.execute("""
                UPDATE test_cases
                SET project_id = ?
                WHERE project_id = ?
            """, (move_to_project_id, project_id))
        else:
            # Set project_id to NULL (will be handled by migration)
            cursor.execute("""
                UPDATE test_cases
                SET project_id = NULL
                WHERE project_id = ?
            """, (project_id,))
        
        # Delete the project
        cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        success = cursor.rowcount > 0
        conn.commit()
    except Exception as e:
        conn.rollback()
        success = False
    finally:
        conn.close()
    
    return success


def get_test_cases_by_project(project_id: int) -> List[Dict]:
    """Get all test cases for a project."""
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM test_cases
        WHERE project_id = ?
        ORDER BY created_at DESC
    """, (project_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


if __name__ == "__main__":
    # Initialize database when run directly
    print("Initializing database...")
    init_database()
    print("Database initialization complete!")
    
    # Test database operations
    print("\nTesting database operations...")
    
    # Create a test case
    test_id = create_test_case("TC-001", "Test Case 1 Description")
    print(f"Created test case with ID: {test_id}")
    
    # Get all test cases
    test_cases = get_all_test_cases()
    print(f"Total test cases: {len(test_cases)}")
    
    # Create a step
    step_id = create_test_step(test_id, 1, "Step 1: Do something", 
                               modules="Module A", 
                               calculation_logic="Formula X",
                               configuration="Config Y")
    print(f"Created step with ID: {step_id}")
    
    # Get steps for test case
    steps = get_steps_by_test_case(test_id)
    print(f"Total steps for test case: {len(steps)}")
    
    print("\nDatabase test completed successfully!")

