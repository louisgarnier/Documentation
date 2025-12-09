#!/usr/bin/env python3
"""
Test script for Test Cases API endpoints (Step 3 of Functionality 2)
Tests all test case endpoints with project support.
"""
import requests
import json

API_URL = "http://localhost:8000"

def print_section(title):
    """Print a section header"""
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

def print_success(message):
    """Print success message"""
    print(f"✅ {message}")

def print_error(message):
    """Print error message"""
    print(f"❌ {message}")

def test_health():
    """Test API health"""
    print_section("TEST: API Health Check")
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        if response.status_code == 200:
            print_success("API is running")
            return True
        else:
            print_error(f"API returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to API. Is the backend running?")
        print("   Start with: cd backend && python3 -m uvicorn api.main:app --reload --port 8000")
        return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_list_all_test_cases():
    """Test GET /api/test-cases"""
    print_section("TEST: List All Test Cases")
    try:
        response = requests.get(f"{API_URL}/api/test-cases", timeout=2)
        if response.status_code == 200:
            test_cases = response.json()
            print_success(f"Found {len(test_cases)} test case(s)")
            for tc in test_cases[:3]:  # Show first 3
                print(f"   - {tc['test_number']}: {tc['description']} (Project ID: {tc.get('project_id', 'None')})")
            return test_cases
        else:
            print_error(f"Status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print_error(f"Error: {e}")
        return None

def test_list_test_cases_by_project(project_id):
    """Test GET /api/test-cases?project_id={id}"""
    print_section(f"TEST: List Test Cases by Project {project_id}")
    try:
        response = requests.get(f"{API_URL}/api/test-cases", params={"project_id": project_id}, timeout=2)
        if response.status_code == 200:
            test_cases = response.json()
            print_success(f"Found {len(test_cases)} test case(s) in project {project_id}")
            for tc in test_cases:
                print(f"   - {tc['test_number']}: {tc['description']}")
            return test_cases
        else:
            print_error(f"Status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print_error(f"Error: {e}")
        return None

def test_create_test_case_with_project(project_id):
    """Test POST /api/test-cases with project_id"""
    print_section(f"TEST: Create Test Case with Project {project_id}")
    try:
        data = {
            "test_number": "TC_API_TEST_001",
            "description": "Test case created via API with project",
            "project_id": project_id
        }
        response = requests.post(f"{API_URL}/api/test-cases", json=data, timeout=2)
        if response.status_code == 201:
            test_case = response.json()
            print_success(f"Created test case: {test_case['test_number']} (ID: {test_case['id']}, Project: {test_case.get('project_id')})")
            return test_case
        else:
            print_error(f"Status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print_error(f"Error: {e}")
        return None

def test_update_test_case_project(test_case_id, new_project_id):
    """Test PUT /api/test-cases/{id} with project_id"""
    print_section(f"TEST: Update Test Case {test_case_id} Project to {new_project_id}")
    try:
        data = {
            "project_id": new_project_id
        }
        response = requests.put(f"{API_URL}/api/test-cases/{test_case_id}", json=data, timeout=2)
        if response.status_code == 200:
            test_case = response.json()
            print_success(f"Updated test case project: {test_case['test_number']} (Project: {test_case.get('project_id')})")
            return test_case
        else:
            print_error(f"Status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print_error(f"Error: {e}")
        return None

def test_move_test_case(test_case_id, target_project_id):
    """Test PUT /api/test-cases/{id}/move"""
    print_section(f"TEST: Move Test Case {test_case_id} to Project {target_project_id}")
    try:
        data = {
            "target_project_id": target_project_id
        }
        response = requests.put(f"{API_URL}/api/test-cases/{test_case_id}/move", json=data, timeout=2)
        if response.status_code == 200:
            test_case = response.json()
            print_success(f"Moved test case: {test_case['test_number']} (Project: {test_case.get('project_id')})")
            return test_case
        else:
            print_error(f"Status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print_error(f"Error: {e}")
        return None

def test_duplicate_test_case(test_case_id, new_test_number, target_project_id=None):
    """Test POST /api/test-cases/{id}/duplicate"""
    print_section(f"TEST: Duplicate Test Case {test_case_id}")
    try:
        data = {
            "new_test_number": new_test_number
        }
        if target_project_id is not None:
            data["target_project_id"] = target_project_id
        
        response = requests.post(f"{API_URL}/api/test-cases/{test_case_id}/duplicate", json=data, timeout=2)
        if response.status_code == 201:
            test_case = response.json()
            print_success(f"Duplicated test case: {test_case['test_number']} (ID: {test_case['id']}, Project: {test_case.get('project_id')})")
            return test_case
        else:
            print_error(f"Status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print_error(f"Error: {e}")
        return None

def test_delete_test_case(test_case_id):
    """Test DELETE /api/test-cases/{id}"""
    print_section(f"TEST: Delete Test Case {test_case_id}")
    try:
        response = requests.delete(f"{API_URL}/api/test-cases/{test_case_id}", timeout=2)
        if response.status_code == 204:
            print_success(f"Deleted test case {test_case_id}")
            return True
        else:
            print_error(f"Status {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def get_first_project():
    """Get the first project for testing"""
    try:
        response = requests.get(f"{API_URL}/api/projects", timeout=2)
        if response.status_code == 200:
            projects = response.json()
            if projects:
                return projects[0]['id']
        return None
    except:
        return None

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("TEST CASES API TEST SUITE")
    print("Step 3: Backend API - Test Cases Updates")
    print("=" * 60)
    
    results = []
    
    # Test 1: Health check
    if not test_health():
        print("\n❌ Cannot continue - API is not running")
        print("   Please start the backend: cd backend && python3 -m uvicorn api.main:app --reload --port 8000")
        return 1
    
    # Test 2: List all test cases
    all_test_cases = test_list_all_test_cases()
    results.append(("List All Test Cases", all_test_cases is not None))
    
    if not all_test_cases:
        print("\n❌ Cannot continue - failed to list test cases")
        return 1
    
    # Get a project for testing
    project_id = get_first_project()
    if not project_id:
        print("\n❌ Cannot continue - no projects found")
        return 1
    
    # Test 3: List test cases by project
    project_test_cases = test_list_test_cases_by_project(project_id)
    results.append(("List Test Cases by Project", project_test_cases is not None))
    
    # Test 4: Create test case with project
    new_test_case = test_create_test_case_with_project(project_id)
    results.append(("Create Test Case with Project", new_test_case is not None))
    
    if not new_test_case:
        print("\n❌ Cannot continue - failed to create test case")
        return 1
    
    test_case_id = new_test_case['id']
    
    # Test 5: Update test case project
    updated = test_update_test_case_project(test_case_id, project_id)
    results.append(("Update Test Case Project", updated is not None))
    
    # Test 6: Move test case
    moved = test_move_test_case(test_case_id, project_id)
    results.append(("Move Test Case", moved is not None))
    
    # Test 7: Duplicate test case
    duplicated = test_duplicate_test_case(test_case_id, "TC_API_TEST_001_DUP", project_id)
    results.append(("Duplicate Test Case", duplicated is not None))
    
    # Clean up: Delete test cases
    if duplicated:
        test_delete_test_case(duplicated['id'])
    test_delete_test_case(test_case_id)
    
    # Summary
    print_section("TEST SUMMARY")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✅ All tests passed! Step 3 is complete.")
        return 0
    else:
        print("\n❌ Some tests failed. Please review the errors above.")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())

