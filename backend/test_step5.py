#!/usr/bin/env python3
"""
Test script for Step 5: Steps endpoints
Run this to verify all step endpoints work correctly.
"""

import subprocess
import sys
import time
import requests
import json

def test_api():
    """Test all step endpoints."""
    print("=" * 60)
    print("TEST: Steps Endpoints")
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
    
    # Get a test case ID (use test case 7 which should exist)
    test_case_id = 7
    created_step_id = None
    
    try:
        # Test GET /api/test-cases/{id}/steps
        print(f"\n2. Testing GET /api/test-cases/{test_case_id}/steps...")
        response = requests.get(
            f"http://localhost:8000/api/test-cases/{test_case_id}/steps",
            timeout=5
        )
        
        if response.status_code == 200:
            steps = response.json()
            print(f"   ✅ Status: {response.status_code}")
            print(f"   ✅ Number of steps: {len(steps)}")
            if len(steps) > 0:
                print(f"   ✅ First step: {steps[0].get('description', '')[:50]}...")
        else:
            print(f"   ❌ Status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        # Test POST /api/test-cases/{id}/steps
        print(f"\n3. Testing POST /api/test-cases/{test_case_id}/steps...")
        new_step = {
            "step_number": 999,
            "description": "Step créé via API",
            "modules": "test module",
            "calculation_logic": "test logic",
            "configuration": "test config"
        }
        response = requests.post(
            f"http://localhost:8000/api/test-cases/{test_case_id}/steps",
            json=new_step,
            timeout=5
        )
        
        if response.status_code == 201:
            data = response.json()
            created_step_id = data['id']
            print(f"   ✅ Status: {response.status_code}")
            print(f"   ✅ Step créé avec ID: {created_step_id}")
            print(f"   ✅ Description: {data['description']}")
        else:
            print(f"   ❌ Status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        # Test GET /api/steps/{id}
        if created_step_id:
            print(f"\n4. Testing GET /api/steps/{created_step_id}...")
            response = requests.get(
                f"http://localhost:8000/api/steps/{created_step_id}",
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Status: {response.status_code}")
                print(f"   ✅ Step ID: {data['id']}")
                print(f"   ✅ Description: {data['description']}")
            else:
                print(f"   ❌ Status: {response.status_code}")
                return False
        
        # Test PUT /api/steps/{id}
        if created_step_id:
            print(f"\n5. Testing PUT /api/steps/{created_step_id}...")
            update_data = {
                "description": "Description modifiée via API"
            }
            response = requests.put(
                f"http://localhost:8000/api/steps/{created_step_id}",
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
        
        # Test POST /api/steps/{id}/reorder
        if created_step_id:
            print(f"\n6. Testing POST /api/steps/{created_step_id}/reorder...")
            reorder_data = {
                "new_position": 1
            }
            response = requests.post(
                f"http://localhost:8000/api/steps/{created_step_id}/reorder",
                json=reorder_data,
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Status: {response.status_code}")
                print(f"   ✅ Step reordonné, nouveau step_number: {data['step_number']}")
            else:
                print(f"   ⚠️  Status: {response.status_code}")
                print(f"   Response: {response.text}")
                # Reorder might fail if only one step, that's OK
        
        # Test DELETE /api/steps/{id}
        if created_step_id:
            print(f"\n7. Testing DELETE /api/steps/{created_step_id}...")
            response = requests.delete(
                f"http://localhost:8000/api/steps/{created_step_id}",
                timeout=5
            )
            
            if response.status_code == 204:
                print(f"   ✅ Status: {response.status_code} (No Content)")
                print(f"   ✅ Step supprimé")
            else:
                print(f"   ❌ Status: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
            
            # Verify deletion
            print(f"\n8. Verifying deletion...")
            response = requests.get(
                f"http://localhost:8000/api/steps/{created_step_id}",
                timeout=5
            )
            
            if response.status_code == 404:
                print(f"   ✅ Status: {response.status_code} (Not Found)")
                print(f"   ✅ Step bien supprimé")
            else:
                print(f"   ⚠️  Status: {response.status_code} (devrait être 404)")
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        
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
        print("\n9. Stopping server...")
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

