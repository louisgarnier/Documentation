#!/usr/bin/env python3
"""
Test script for Step 3: GET /api/test-cases endpoint
Run this to verify the endpoint returns test cases from the database.
"""

import subprocess
import sys
import time
import requests
import json

def test_api():
    """Test that GET /api/test-cases returns test cases."""
    print("=" * 60)
    print("TEST: GET /api/test-cases Endpoint")
    print("=" * 60)
    
    # Start server in background
    print("\n1. Starting FastAPI server...")
    server_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "api.main:app", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to start
    print("   Waiting for server to start...")
    time.sleep(3)
    
    try:
        # Test GET /api/test-cases
        print("\n2. Testing GET /api/test-cases endpoint...")
        response = requests.get("http://localhost:8000/api/test-cases", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {response.status_code}")
            print(f"   ✅ Response type: {type(data)}")
            print(f"   ✅ Number of test cases: {len(data)}")
            
            if len(data) > 0:
                print(f"\n   First test case:")
                first = data[0]
                print(f"   - ID: {first.get('id')}")
                print(f"   - Test Number: {first.get('test_number')}")
                print(f"   - Description: {first.get('description')[:50]}...")
                print("   ✅ Endpoint returns test cases!")
            else:
                print("   ⚠️  No test cases found (database might be empty)")
            
            # Test GET /api/test-cases/{id}
            if len(data) > 0:
                test_case_id = data[0]['id']
                print(f"\n3. Testing GET /api/test-cases/{test_case_id} endpoint...")
                response = requests.get(f"http://localhost:8000/api/test-cases/{test_case_id}", timeout=5)
                
                if response.status_code == 200:
                    test_case = response.json()
                    print(f"   ✅ Status: {response.status_code}")
                    print(f"   ✅ Test Case ID: {test_case.get('id')}")
                    print(f"   ✅ Test Number: {test_case.get('test_number')}")
                    print("   ✅ Get by ID works!")
                else:
                    print(f"   ❌ Status: {response.status_code}")
                    print(f"   Response: {response.text}")
                    return False
            
            print("\n" + "=" * 60)
            print("✅ ALL TESTS PASSED!")
            print("=" * 60)
            print("\nNext steps:")
            print("1. Open http://localhost:8000/docs in your browser")
            print("2. Find 'GET /api/test-cases' endpoint")
            print("3. Click 'Try it out' and 'Execute'")
            print("4. Verify you see your test cases")
            
            return True
        else:
            print(f"   ❌ Status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
    except requests.exceptions.ConnectionError:
        print("   ❌ Could not connect to server")
        print("   Make sure the server started correctly")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Stop server
        print("\n4. Stopping server...")
        server_process.terminate()
        server_process.wait()
        print("   ✅ Server stopped")

if __name__ == "__main__":
    try:
        import requests
    except ImportError:
        print("❌ 'requests' library not found. Install it with: pip install requests")
        sys.exit(1)
    
    success = test_api()
    sys.exit(0 if success else 1)

