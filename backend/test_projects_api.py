#!/usr/bin/env python3
"""
Test script for Projects API endpoints (Step 2 of Functionality 2)
Tests all project API endpoints.
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

def test_list_projects():
    """Test GET /api/projects"""
    print_section("TEST: List All Projects")
    try:
        response = requests.get(f"{API_URL}/api/projects", timeout=2)
        if response.status_code == 200:
            projects = response.json()
            print_success(f"Found {len(projects)} projects")
            for project in projects:
                print(f"   - {project['name']} (ID: {project['id']}, Test Cases: {project.get('test_case_count', 0)})")
            return projects
        else:
            print_error(f"Status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print_error(f"Error: {e}")
        return None

def test_get_project(project_id):
    """Test GET /api/projects/{id}"""
    print_section(f"TEST: Get Project {project_id}")
    try:
        response = requests.get(f"{API_URL}/api/projects/{project_id}", timeout=2)
        if response.status_code == 200:
            project = response.json()
            print_success(f"Found project: {project['name']}")
            print(f"   Description: {project.get('description', 'None')}")
            print(f"   Test Cases: {project.get('test_case_count', 0)}")
            return project
        elif response.status_code == 404:
            print_error(f"Project {project_id} not found")
            return None
        else:
            print_error(f"Status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print_error(f"Error: {e}")
        return None

def test_create_project():
    """Test POST /api/projects"""
    print_section("TEST: Create Project")
    try:
        data = {
            "name": "API Test Project",
            "description": "Test project created via API"
        }
        response = requests.post(f"{API_URL}/api/projects", json=data, timeout=2)
        if response.status_code == 201:
            project = response.json()
            print_success(f"Created project: {project['name']} (ID: {project['id']})")
            return project
        else:
            print_error(f"Status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print_error(f"Error: {e}")
        return None

def test_update_project(project_id):
    """Test PUT /api/projects/{id}"""
    print_section(f"TEST: Update Project {project_id}")
    try:
        data = {
            "name": "Updated API Test Project",
            "description": "Updated description"
        }
        response = requests.put(f"{API_URL}/api/projects/{project_id}", json=data, timeout=2)
        if response.status_code == 200:
            project = response.json()
            print_success(f"Updated project: {project['name']}")
            return project
        else:
            print_error(f"Status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print_error(f"Error: {e}")
        return None

def test_get_project_test_cases(project_id):
    """Test GET /api/projects/{id}/test-cases"""
    print_section(f"TEST: Get Test Cases for Project {project_id}")
    try:
        response = requests.get(f"{API_URL}/api/projects/{project_id}/test-cases", timeout=2)
        if response.status_code == 200:
            test_cases = response.json()
            print_success(f"Found {len(test_cases)} test case(s) in project")
            for tc in test_cases:
                print(f"   - {tc['test_number']}: {tc['description']}")
            return test_cases
        else:
            print_error(f"Status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print_error(f"Error: {e}")
        return None

def test_delete_project(project_id):
    """Test DELETE /api/projects/{id}"""
    print_section(f"TEST: Delete Project {project_id}")
    try:
        response = requests.delete(f"{API_URL}/api/projects/{project_id}", timeout=2)
        if response.status_code == 204:
            print_success(f"Deleted project {project_id}")
            return True
        else:
            print_error(f"Status {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("PROJECTS API TEST SUITE")
    print("Step 2: Backend API - Projects Routes")
    print("=" * 60)
    
    results = []
    
    # Test 1: Health check
    if not test_health():
        print("\n❌ Cannot continue - API is not running")
        print("   Please start the backend: cd backend && python3 -m uvicorn api.main:app --reload --port 8000")
        return 1
    
    # Test 2: List projects
    projects = test_list_projects()
    results.append(("List Projects", projects is not None))
    
    if not projects:
        print("\n❌ Cannot continue - failed to list projects")
        return 1
    
    # Test 3: Get project by ID (use first project)
    if projects:
        first_project = projects[0]
        project = test_get_project(first_project['id'])
        results.append(("Get Project by ID", project is not None))
    
    # Test 4: Create project
    new_project = test_create_project()
    results.append(("Create Project", new_project is not None))
    
    if not new_project:
        print("\n❌ Cannot continue - failed to create project")
        return 1
    
    project_id = new_project['id']
    
    # Test 5: Get project test cases (should be empty)
    test_cases = test_get_project_test_cases(project_id)
    results.append(("Get Project Test Cases", test_cases is not None))
    
    # Test 6: Update project
    updated = test_update_project(project_id)
    results.append(("Update Project", updated is not None))
    
    # Test 7: Delete project
    deleted = test_delete_project(project_id)
    results.append(("Delete Project", deleted))
    
    # Summary
    print_section("TEST SUMMARY")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✅ All tests passed! Step 2 is complete.")
        return 0
    else:
        print("\n❌ Some tests failed. Please review the errors above.")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())

