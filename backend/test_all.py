#!/usr/bin/env python3
"""
Comprehensive test script for all API endpoints.
Run this to verify all endpoints work correctly.
"""

import subprocess
import sys
import time
import requests

def test_endpoint(name, method, url, expected_status=200, json_data=None, files=None):
    """Test a single endpoint."""
    try:
        if method == "GET":
            response = requests.get(url, timeout=5)
        elif method == "POST":
            if files:
                response = requests.post(url, files=files, timeout=10)
            else:
                response = requests.post(url, json=json_data, timeout=5)
        elif method == "PUT":
            response = requests.put(url, json=json_data, timeout=5)
        elif method == "DELETE":
            response = requests.delete(url, timeout=5)
        else:
            return False, f"Unknown method: {method}"
        
        if response.status_code == expected_status:
            return True, f"✅ {name}: {response.status_code}"
        else:
            return False, f"❌ {name}: Expected {expected_status}, got {response.status_code}"
    except Exception as e:
        return False, f"❌ {name}: Error - {str(e)}"

def run_all_tests():
    """Run all endpoint tests."""
    print("=" * 60)
    print("COMPREHENSIVE API TESTS")
    print("=" * 60)
    
    # Start server
    print("\n1. Starting FastAPI server...")
    server_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "api.main:app", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    time.sleep(3)
    
    results = []
    created_ids = {}
    
    try:
        # Health checks
        print("\n2. Health Check Endpoints")
        print("-" * 60)
        success, msg = test_endpoint("GET /", "GET", "http://localhost:8000/")
        results.append(("GET /", success))
        print(f"   {msg}")
        
        success, msg = test_endpoint("GET /health", "GET", "http://localhost:8000/health")
        results.append(("GET /health", success))
        print(f"   {msg}")
        
        # Test Cases
        print("\n3. Test Cases Endpoints")
        print("-" * 60)
        success, msg = test_endpoint("GET /api/test-cases", "GET", "http://localhost:8000/api/test-cases")
        results.append(("GET /api/test-cases", success))
        print(f"   {msg}")
        
        if success:
            # Get a test case ID
            response = requests.get("http://localhost:8000/api/test-cases", timeout=5)
            test_cases = response.json()
            if test_cases:
                test_case_id = test_cases[0]['id']
                created_ids['test_case'] = test_case_id
                
                success, msg = test_endpoint(
                    f"GET /api/test-cases/{test_case_id}",
                    "GET",
                    f"http://localhost:8000/api/test-cases/{test_case_id}"
                )
                results.append((f"GET /api/test-cases/{test_case_id}", success))
                print(f"   {msg}")
        
        # Create test case
        success, msg = test_endpoint(
            "POST /api/test-cases",
            "POST",
            "http://localhost:8000/api/test-cases",
            expected_status=201,
            json_data={"test_number": "TC_TEST", "description": "Test API"}
        )
        results.append(("POST /api/test-cases", success))
        print(f"   {msg}")
        
        if success:
            response = requests.post(
                "http://localhost:8000/api/test-cases",
                json={"test_number": "TC_TEST2", "description": "Test API 2"},
                timeout=5
            )
            if response.status_code == 201:
                created_ids['test_case_new'] = response.json()['id']
        
        # Steps
        print("\n4. Steps Endpoints")
        print("-" * 60)
        if created_ids.get('test_case'):
            test_case_id = created_ids['test_case']
            
            success, msg = test_endpoint(
                f"GET /api/test-cases/{test_case_id}/steps",
                "GET",
                f"http://localhost:8000/api/test-cases/{test_case_id}/steps"
            )
            results.append((f"GET /api/test-cases/{test_case_id}/steps", success))
            print(f"   {msg}")
            
            # Create step
            success, msg = test_endpoint(
                f"POST /api/test-cases/{test_case_id}/steps",
                "POST",
                f"http://localhost:8000/api/test-cases/{test_case_id}/steps",
                expected_status=201,
                json_data={"step_number": 999, "description": "Test step"}
            )
            results.append((f"POST /api/test-cases/{test_case_id}/steps", success))
            print(f"   {msg}")
            
            if success:
                response = requests.post(
                    f"http://localhost:8000/api/test-cases/{test_case_id}/steps",
                    json={"step_number": 998, "description": "Test step 2"},
                    timeout=5
                )
                if response.status_code == 201:
                    created_ids['step'] = response.json()['id']
        
        # Screenshots
        print("\n5. Screenshots Endpoints")
        print("-" * 60)
        if created_ids.get('step'):
            step_id = created_ids['step']
            
            success, msg = test_endpoint(
                f"GET /api/steps/{step_id}/screenshots",
                "GET",
                f"http://localhost:8000/api/steps/{step_id}/screenshots"
            )
            results.append((f"GET /api/steps/{step_id}/screenshots", success))
            print(f"   {msg}")
        
        # Export
        print("\n6. Export Endpoint")
        print("-" * 60)
        if created_ids.get('test_case'):
            test_case_id = created_ids['test_case']
            success, msg = test_endpoint(
                "POST /api/export",
                "POST",
                "http://localhost:8000/api/export",
                json_data={"test_case_ids": [test_case_id]}
            )
            results.append(("POST /api/export", success))
            print(f"   {msg}")
        
        # Summary
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        total = len(results)
        passed = sum(1 for _, success in results if success)
        failed = total - passed
        
        print(f"\nTotal tests: {total}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        
        if failed > 0:
            print("\nFailed tests:")
            for name, success in results:
                if not success:
                    print(f"   ❌ {name}")
        
        print("\n" + "=" * 60)
        if failed == 0:
            print("✅ ALL TESTS PASSED!")
        else:
            print(f"⚠️  {failed} test(s) failed")
        print("=" * 60)
        
        return failed == 0
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Cleanup created resources
        if created_ids.get('test_case_new'):
            try:
                requests.delete(
                    f"http://localhost:8000/api/test-cases/{created_ids['test_case_new']}",
                    timeout=5
                )
            except:
                pass
        
        # Stop server
        print("\n7. Stopping server...")
        server_process.terminate()
        server_process.wait()
        print("   ✅ Server stopped")

if __name__ == "__main__":
    try:
        import requests
    except ImportError:
        print("❌ 'requests' library not found. Install it with: pip install requests")
        sys.exit(1)
    
    success = run_all_tests()
    sys.exit(0 if success else 1)

