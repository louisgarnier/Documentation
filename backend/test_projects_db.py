#!/usr/bin/env python3
"""
Test script for Projects database functionality (Step 1 of Functionality 2)
Tests database schema, migration, and project functions.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from shared.models import (
    init_database,
    create_project,
    get_all_projects,
    get_project_by_id,
    update_project,
    delete_project,
    get_test_cases_by_project,
    create_test_case,
    get_all_test_cases,
    move_test_case_to_project,
    duplicate_test_case
)

def test_database_init():
    """Test database initialization"""
    print("=" * 60)
    print("TEST 1: Database Initialization")
    print("=" * 60)
    
    try:
        init_database()
        print("✅ Database initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

def test_create_project():
    """Test creating projects"""
    print("\n" + "=" * 60)
    print("TEST 2: Create Projects")
    print("=" * 60)
    
    try:
        # Create test projects
        project1_id = create_project("Test Project 1", "Description for project 1")
        print(f"✅ Created project 1 with ID: {project1_id}")
        
        project2_id = create_project("Test Project 2")
        print(f"✅ Created project 2 with ID: {project2_id} (no description)")
        
        return project1_id, project2_id
    except Exception as e:
        print(f"❌ Create project failed: {e}")
        return None, None

def test_get_projects():
    """Test getting all projects"""
    print("\n" + "=" * 60)
    print("TEST 3: Get All Projects")
    print("=" * 60)
    
    try:
        projects = get_all_projects()
        print(f"✅ Found {len(projects)} projects:")
        for project in projects:
            print(f"   - {project['name']} (ID: {project['id']}, Test Cases: {project.get('test_case_count', 0)})")
        return True
    except Exception as e:
        print(f"❌ Get projects failed: {e}")
        return False

def test_get_project_by_id(project_id):
    """Test getting project by ID"""
    print("\n" + "=" * 60)
    print("TEST 4: Get Project by ID")
    print("=" * 60)
    
    try:
        project = get_project_by_id(project_id)
        if project:
            print(f"✅ Found project: {project['name']}")
            print(f"   Description: {project.get('description', 'None')}")
            print(f"   Test Cases: {project.get('test_case_count', 0)}")
            return True
        else:
            print(f"❌ Project {project_id} not found")
            return False
    except Exception as e:
        print(f"❌ Get project by ID failed: {e}")
        return False

def test_create_test_case_in_project(project_id):
    """Test creating test case in a project"""
    print("\n" + "=" * 60)
    print("TEST 5: Create Test Case in Project")
    print("=" * 60)
    
    try:
        test_case_id = create_test_case("TC-PROJ-001", "Test case in project", project_id)
        print(f"✅ Created test case {test_case_id} in project {project_id}")
        
        # Verify it's in the project
        test_cases = get_test_cases_by_project(project_id)
        print(f"✅ Project now has {len(test_cases)} test case(s)")
        
        return test_case_id
    except Exception as e:
        print(f"❌ Create test case in project failed: {e}")
        return None

def test_get_test_cases_by_project(project_id):
    """Test getting test cases by project"""
    print("\n" + "=" * 60)
    print("TEST 6: Get Test Cases by Project")
    print("=" * 60)
    
    try:
        test_cases = get_test_cases_by_project(project_id)
        print(f"✅ Found {len(test_cases)} test case(s) in project:")
        for tc in test_cases:
            print(f"   - {tc['test_number']}: {tc['description']}")
        return True
    except Exception as e:
        print(f"❌ Get test cases by project failed: {e}")
        return False

def test_move_test_case(test_case_id, target_project_id):
    """Test moving test case to another project"""
    print("\n" + "=" * 60)
    print("TEST 7: Move Test Case to Another Project")
    print("=" * 60)
    
    try:
        success = move_test_case_to_project(test_case_id, target_project_id)
        if success:
            print(f"✅ Moved test case {test_case_id} to project {target_project_id}")
            
            # Verify move
            test_cases = get_test_cases_by_project(target_project_id)
            print(f"✅ Target project now has {len(test_cases)} test case(s)")
            return True
        else:
            print(f"❌ Failed to move test case")
            return False
    except Exception as e:
        print(f"❌ Move test case failed: {e}")
        return False

def test_update_project(project_id):
    """Test updating project"""
    print("\n" + "=" * 60)
    print("TEST 8: Update Project")
    print("=" * 60)
    
    try:
        success = update_project(project_id, "Updated Project Name", "Updated description")
        if success:
            project = get_project_by_id(project_id)
            print(f"✅ Updated project: {project['name']}")
            print(f"   New description: {project.get('description', 'None')}")
            return True
        else:
            print(f"❌ Failed to update project")
            return False
    except Exception as e:
        print(f"❌ Update project failed: {e}")
        return False

def test_get_all_test_cases_filtered():
    """Test getting test cases with project filter"""
    print("\n" + "=" * 60)
    print("TEST 9: Get Test Cases Filtered by Project")
    print("=" * 60)
    
    try:
        # Get all test cases
        all_tcs = get_all_test_cases()
        print(f"✅ Total test cases: {len(all_tcs)}")
        
        # Get test cases for a specific project (if we have one)
        projects = get_all_projects()
        if projects:
            project_id = projects[0]['id']
            filtered_tcs = get_all_test_cases(project_id=project_id)
            print(f"✅ Test cases in project {project_id}: {len(filtered_tcs)}")
        
        return True
    except Exception as e:
        print(f"❌ Get filtered test cases failed: {e}")
        return False

def cleanup_test_data(project1_id, project2_id):
    """Clean up test data"""
    print("\n" + "=" * 60)
    print("CLEANUP: Removing Test Data")
    print("=" * 60)
    
    try:
        if project1_id:
            delete_project(project1_id)
            print(f"✅ Deleted project {project1_id}")
        if project2_id:
            delete_project(project2_id)
            print(f"✅ Deleted project {project2_id}")
    except Exception as e:
        print(f"⚠️  Cleanup warning: {e}")

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("PROJECTS DATABASE TEST SUITE")
    print("Step 1: Database Schema Implementation")
    print("=" * 60 + "\n")
    
    results = []
    
    # Test 1: Database initialization
    results.append(("Database Init", test_database_init()))
    
    # Test 2: Create projects
    project1_id, project2_id = test_create_project()
    results.append(("Create Projects", project1_id is not None))
    
    if not project1_id:
        print("\n❌ Cannot continue tests - project creation failed")
        return
    
    # Test 3: Get all projects
    results.append(("Get All Projects", test_get_projects()))
    
    # Test 4: Get project by ID
    results.append(("Get Project by ID", test_get_project_by_id(project1_id)))
    
    # Test 5: Create test case in project
    test_case_id = test_create_test_case_in_project(project1_id)
    results.append(("Create Test Case in Project", test_case_id is not None))
    
    # Test 6: Get test cases by project
    results.append(("Get Test Cases by Project", test_get_test_cases_by_project(project1_id)))
    
    # Test 7: Move test case
    if test_case_id and project2_id:
        results.append(("Move Test Case", test_move_test_case(test_case_id, project2_id)))
    
    # Test 8: Update project
    results.append(("Update Project", test_update_project(project1_id)))
    
    # Test 9: Get filtered test cases
    results.append(("Get Filtered Test Cases", test_get_all_test_cases_filtered()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    # Cleanup
    cleanup_test_data(project1_id, project2_id)
    
    if passed == total:
        print("\n✅ All tests passed! Step 1 is complete.")
        return 0
    else:
        print("\n❌ Some tests failed. Please review the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

