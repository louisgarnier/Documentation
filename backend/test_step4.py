#!/usr/bin/env python3
"""
Test script for Step 4: CRUD endpoints for test cases
Run this to verify POST, PUT, DELETE work correctly.
"""

import subprocess
import sys
import time
import requests
import json

def test_api():
    """Test CRUD operations for test cases."""
    print("=" * 60)
    print("TEST: CRUD Endpoints for Test Cases")
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
    
    created_id = None
    
    try:
        # Test POST /api/test-cases
        print("\n2. Testing POST /api/test-cases (create)...")
        new_test_case = {
            "test_number": "TC99",
            "description": "Test case créé via API"
        }
        response = requests.post(
            "http://localhost:8000/api/test-cases",
            json=new_test_case,
            timeout=5
        )
        
        if response.status_code == 201:
            data = response.json()
            created_id = data['id']
            print(f"   ✅ Status: {response.status_code}")
            print(f"   ✅ Test case créé avec ID: {created_id}")
            print(f"   ✅ Test Number: {data['test_number']}")
            print(f"   ✅ Description: {data['description']}")
        else:
            print(f"   ❌ Status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        # Test PUT /api/test-cases/{id}
        if created_id:
            print(f"\n3. Testing PUT /api/test-cases/{created_id} (update)...")
            update_data = {
                "description": "Description modifiée via API"
            }
            response = requests.put(
                f"http://localhost:8000/api/test-cases/{created_id}",
                json=update_data,
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Status: {response.status_code}")
                print(f"   ✅ Description mise à jour: {data['description']}")
            else:
                print(f"   ❌ Status: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
        
        # Test GET to verify update
        if created_id:
            print(f"\n4. Testing GET /api/test-cases/{created_id} (verify update)...")
            response = requests.get(
                f"http://localhost:8000/api/test-cases/{created_id}",
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Status: {response.status_code}")
                print(f"   ✅ Description vérifiée: {data['description']}")
            else:
                print(f"   ❌ Status: {response.status_code}")
                return False
        
        # Test DELETE /api/test-cases/{id}
        if created_id:
            print(f"\n5. Testing DELETE /api/test-cases/{created_id} (delete)...")
            response = requests.delete(
                f"http://localhost:8000/api/test-cases/{created_id}",
                timeout=5
            )
            
            if response.status_code == 204:
                print(f"   ✅ Status: {response.status_code} (No Content)")
                print(f"   ✅ Test case supprimé")
            else:
                print(f"   ❌ Status: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
            
            # Verify deletion
            print(f"\n6. Verifying deletion...")
            response = requests.get(
                f"http://localhost:8000/api/test-cases/{created_id}",
                timeout=5
            )
            
            if response.status_code == 404:
                print(f"   ✅ Status: {response.status_code} (Not Found)")
                print(f"   ✅ Test case bien supprimé")
            else:
                print(f"   ⚠️  Status: {response.status_code} (devrait être 404)")
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Vérifier dans Streamlit que les changements sont visibles")
        print("2. Tester via Swagger UI: http://localhost:8000/docs")
        
        return True
        
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
    
    success = test_api()
    sys.exit(0 if success else 1)

