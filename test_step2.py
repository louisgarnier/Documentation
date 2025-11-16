"""
Test script for Step 2: Database Schema & Models

Run this script to validate the database setup:
    python3 test_step2.py
"""

import os
import sqlite3
from models import (
    init_database, 
    create_test_case, 
    get_all_test_cases,
    get_test_case_by_id,
    update_test_case,
    create_test_step,
    get_steps_by_test_case,
    update_test_step,
    add_screenshot_to_step,
    get_screenshots_by_step,
    delete_test_case
)

def test_database_initialization():
    """Test 1: Database initialization"""
    print("=" * 60)
    print("TEST 1: Database Initialization")
    print("=" * 60)
    
    # Remove existing database if it exists (for clean test)
    if os.path.exists("database/test_cases.db"):
        os.remove("database/test_cases.db")
        print("✓ Removed existing database for clean test")
    
    # Initialize database
    init_database()
    print("✓ Database initialized")
    
    # Verify database file exists
    assert os.path.exists("database/test_cases.db"), "Database file not created!"
    print("✓ Database file created at: database/test_cases.db")
    
    # Verify tables exist
    conn = sqlite3.connect("database/test_cases.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    expected_tables = ['test_cases', 'test_steps', 'step_screenshots']
    
    for table in expected_tables:
        assert table in tables, f"Table '{table}' not found!"
        print(f"✓ Table '{table}' exists")
    
    conn.close()
    print("\n✅ TEST 1 PASSED: Database initialization successful\n")


def test_test_case_crud():
    """Test 2: Test Case CRUD operations"""
    print("=" * 60)
    print("TEST 2: Test Case CRUD Operations")
    print("=" * 60)
    
    # Create test case
    test_id = create_test_case("TC-TEST-001", "Test Case for Validation")
    print(f"✓ Created test case with ID: {test_id}")
    assert test_id > 0, "Test case ID should be positive!"
    
    # Get all test cases
    all_cases = get_all_test_cases()
    print(f"✓ Retrieved {len(all_cases)} test case(s)")
    assert len(all_cases) >= 1, "Should have at least 1 test case!"
    
    # Get test case by ID
    test_case = get_test_case_by_id(test_id)
    assert test_case is not None, "Test case not found!"
    assert test_case['test_number'] == "TC-TEST-001", "Test number mismatch!"
    assert test_case['description'] == "Test Case for Validation", "Description mismatch!"
    print(f"✓ Retrieved test case: {test_case['test_number']} - {test_case['description']}")
    
    # Update test case
    success = update_test_case(test_id, "TC-TEST-001-UPDATED", "Updated Description")
    assert success, "Update failed!"
    updated_case = get_test_case_by_id(test_id)
    assert updated_case['test_number'] == "TC-TEST-001-UPDATED", "Update didn't work!"
    print(f"✓ Updated test case: {updated_case['test_number']}")
    
    # Clean up - delete test case
    delete_test_case(test_id)
    deleted_case = get_test_case_by_id(test_id)
    assert deleted_case is None, "Test case should be deleted!"
    print(f"✓ Deleted test case (ID: {test_id})")
    
    print("\n✅ TEST 2 PASSED: Test Case CRUD operations working\n")
    return test_id


def test_step_crud():
    """Test 3: Test Step CRUD operations"""
    print("=" * 60)
    print("TEST 3: Test Step CRUD Operations")
    print("=" * 60)
    
    # Create a test case first
    test_id = create_test_case("TC-TEST-002", "Test Case for Step Testing")
    print(f"✓ Created test case (ID: {test_id})")
    
    # Create test step
    step_id = create_test_step(
        test_case_id=test_id,
        step_number=1,
        description="Step 1: Perform initial validation",
        modules="Module A, Module B",
        calculation_logic="Formula: X = Y + Z",
        configuration="Config setting: enabled"
    )
    print(f"✓ Created step with ID: {step_id}")
    assert step_id > 0, "Step ID should be positive!"
    
    # Get steps for test case
    steps = get_steps_by_test_case(test_id)
    print(f"✓ Retrieved {len(steps)} step(s) for test case")
    assert len(steps) == 1, "Should have 1 step!"
    assert steps[0]['step_number'] == 1, "Step number mismatch!"
    assert steps[0]['modules'] == "Module A, Module B", "Modules mismatch!"
    print(f"✓ Step details: Step {steps[0]['step_number']} - {steps[0]['description']}")
    print(f"  Modules: {steps[0]['modules']}")
    print(f"  Calculation Logic: {steps[0]['calculation_logic']}")
    print(f"  Configuration: {steps[0]['configuration']}")
    
    # Update step
    success = update_test_step(
        step_id=step_id,
        step_number=1,
        description="Step 1: Updated description",
        modules="Module A, Module B, Module C",
        calculation_logic="Updated Formula: X = Y + Z + W",
        configuration="Config setting: disabled"
    )
    assert success, "Step update failed!"
    updated_steps = get_steps_by_test_case(test_id)
    assert updated_steps[0]['description'] == "Step 1: Updated description", "Update didn't work!"
    print(f"✓ Updated step successfully")
    
    # Clean up
    delete_test_case(test_id)
    print(f"✓ Cleaned up test case and steps")
    
    print("\n✅ TEST 3 PASSED: Test Step CRUD operations working\n")


def test_screenshot_operations():
    """Test 4: Screenshot operations"""
    print("=" * 60)
    print("TEST 4: Screenshot Operations")
    print("=" * 60)
    
    # Create test case and step
    test_id = create_test_case("TC-TEST-003", "Test Case for Screenshot Testing")
    step_id = create_test_step(test_id, 1, "Step with screenshot")
    print(f"✓ Created test case (ID: {test_id}) and step (ID: {step_id})")
    
    # Create uploads directory structure (simulating screenshot path)
    os.makedirs("uploads/test_1/step_1", exist_ok=True)
    screenshot_path = "uploads/test_1/step_1/screenshot1.png"
    
    # Add screenshot (even though file doesn't exist, we're testing the DB operation)
    screenshot_id = add_screenshot_to_step(step_id, screenshot_path)
    print(f"✓ Added screenshot record with ID: {screenshot_id}")
    assert screenshot_id > 0, "Screenshot ID should be positive!"
    
    # Get screenshots for step
    screenshots = get_screenshots_by_step(step_id)
    print(f"✓ Retrieved {len(screenshots)} screenshot(s) for step")
    assert len(screenshots) == 1, "Should have 1 screenshot!"
    assert screenshots[0]['file_path'] == screenshot_path, "Screenshot path mismatch!"
    print(f"✓ Screenshot path: {screenshots[0]['file_path']}")
    
    # Clean up
    delete_test_case(test_id)
    print(f"✓ Cleaned up test case, steps, and screenshots")
    
    print("\n✅ TEST 4 PASSED: Screenshot operations working\n")


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("STEP 2 VALIDATION: Database Schema & Models")
    print("=" * 60 + "\n")
    
    try:
        test_database_initialization()
        test_test_case_crud()
        test_step_crud()
        test_screenshot_operations()
        
        print("=" * 60)
        print("🎉 ALL TESTS PASSED! Step 2 validation complete.")
        print("=" * 60)
        print("\nDatabase is ready for use in the Streamlit application.")
        print("You can now proceed to Step 3: Basic Streamlit UI\n")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        print("Please review the error and fix the issue before proceeding.\n")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

