#!/usr/bin/env python3
"""
Test script for Step 6: Screenshots endpoints
Run this to verify all screenshot endpoints work correctly.
"""

import subprocess
import sys
import time
import requests
import json
import os
from pathlib import Path

def create_test_image():
    """Create a simple test image file."""
    # Create a simple 1x1 PNG image (minimal valid PNG)
    # PNG header + minimal data
    png_data = bytes([
        0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A,  # PNG signature
        0x00, 0x00, 0x00, 0x0D, 0x49, 0x48, 0x44, 0x52,  # IHDR chunk
        0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01,  # 1x1 image
        0x08, 0x02, 0x00, 0x00, 0x00, 0x90, 0x77, 0x53, 0xDE,
        0x00, 0x00, 0x00, 0x0A, 0x49, 0x44, 0x41, 0x54,  # IDAT chunk
        0x08, 0x99, 0x01, 0x01, 0x00, 0x00, 0x00, 0xFF, 0xFF,
        0x00, 0x00, 0x00, 0x02, 0x00, 0x01, 0x00, 0x00, 0x00,
        0x00, 0x49, 0x45, 0x4E, 0x44, 0xAE, 0x42, 0x60, 0x82  # IEND
    ])
    
    test_file = Path("/tmp/test_screenshot.png")
    test_file.write_bytes(png_data)
    return test_file

def test_api():
    """Test all screenshot endpoints."""
    print("=" * 60)
    print("TEST: Screenshots Endpoints")
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
    
    # Get a step ID (use step from test case 7)
    test_case_id = 7
    step_id = None
    created_screenshot_id = None
    test_file = None
    
    try:
        # Get a step ID
        print(f"\n2. Getting steps for test case {test_case_id}...")
        response = requests.get(
            f"http://localhost:8000/api/test-cases/{test_case_id}/steps",
            timeout=5
        )
        
        if response.status_code == 200:
            steps = response.json()
            if len(steps) > 0:
                step_id = steps[0]['id']
                print(f"   ✅ Using step ID: {step_id}")
            else:
                print("   ⚠️  No steps found, creating one...")
                # Create a step first
                new_step = {
                    "step_number": 999,
                    "description": "Test step for screenshots"
                }
                response = requests.post(
                    f"http://localhost:8000/api/test-cases/{test_case_id}/steps",
                    json=new_step,
                    timeout=5
                )
                if response.status_code == 201:
                    step_id = response.json()['id']
                    print(f"   ✅ Step créé avec ID: {step_id}")
                else:
                    print(f"   ❌ Failed to create step: {response.status_code}")
                    return False
        else:
            print(f"   ❌ Failed to get steps: {response.status_code}")
            return False
        
        if not step_id:
            print("   ❌ No step ID available")
            return False
        
        # Test GET /api/steps/{id}/screenshots
        print(f"\n3. Testing GET /api/steps/{step_id}/screenshots...")
        response = requests.get(
            f"http://localhost:8000/api/steps/{step_id}/screenshots",
            timeout=5
        )
        
        if response.status_code == 200:
            screenshots = response.json()
            print(f"   ✅ Status: {response.status_code}")
            print(f"   ✅ Number of screenshots: {len(screenshots)}")
        else:
            print(f"   ❌ Status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        # Test POST /api/steps/{id}/screenshots
        print(f"\n4. Testing POST /api/steps/{step_id}/screenshots (upload)...")
        test_file = create_test_image()
        
        with open(test_file, 'rb') as f:
            files = {'file': ('test_screenshot.png', f, 'image/png')}
            response = requests.post(
                f"http://localhost:8000/api/steps/{step_id}/screenshots",
                files=files,
                timeout=10
            )
        
        if response.status_code == 201:
            data = response.json()
            created_screenshot_id = data['id']
            print(f"   ✅ Status: {response.status_code}")
            print(f"   ✅ Screenshot créé avec ID: {created_screenshot_id}")
            print(f"   ✅ File path: {data['file_path']}")
            
            # Verify file exists
            if os.path.exists(data['file_path']):
                print(f"   ✅ File exists on disk")
            else:
                print(f"   ⚠️  File not found on disk: {data['file_path']}")
        else:
            print(f"   ❌ Status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        # Test GET /api/steps/{id}/screenshots again
        print(f"\n5. Testing GET /api/steps/{step_id}/screenshots (after upload)...")
        response = requests.get(
            f"http://localhost:8000/api/steps/{step_id}/screenshots",
            timeout=5
        )
        
        if response.status_code == 200:
            screenshots = response.json()
            print(f"   ✅ Status: {response.status_code}")
            print(f"   ✅ Number of screenshots: {len(screenshots)}")
            if len(screenshots) > 0:
                print(f"   ✅ New screenshot in list: {screenshots[-1]['id']}")
        else:
            print(f"   ❌ Status: {response.status_code}")
            return False
        
        # Test GET /api/screenshots/{id}/file
        if created_screenshot_id:
            print(f"\n6. Testing GET /api/screenshots/{created_screenshot_id}/file...")
            response = requests.get(
                f"http://localhost:8000/api/screenshots/{created_screenshot_id}/file",
                timeout=5
            )
            
            if response.status_code == 200:
                print(f"   ✅ Status: {response.status_code}")
                print(f"   ✅ Content-Type: {response.headers.get('content-type')}")
                print(f"   ✅ File size: {len(response.content)} bytes")
            else:
                print(f"   ⚠️  Status: {response.status_code}")
                print(f"   Response: {response.text}")
        
        # Test DELETE /api/screenshots/{id}
        if created_screenshot_id:
            print(f"\n7. Testing DELETE /api/screenshots/{created_screenshot_id}...")
            response = requests.delete(
                f"http://localhost:8000/api/screenshots/{created_screenshot_id}",
                timeout=5
            )
            
            if response.status_code == 204:
                print(f"   ✅ Status: {response.status_code} (No Content)")
                print(f"   ✅ Screenshot supprimé")
            else:
                print(f"   ❌ Status: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
            
            # Verify deletion
            print(f"\n8. Verifying deletion...")
            response = requests.get(
                f"http://localhost:8000/api/steps/{step_id}/screenshots",
                timeout=5
            )
            
            if response.status_code == 200:
                screenshots = response.json()
                screenshot_ids = [s['id'] for s in screenshots]
                if created_screenshot_id not in screenshot_ids:
                    print(f"   ✅ Screenshot bien supprimé de la liste")
                else:
                    print(f"   ⚠️  Screenshot toujours dans la liste")
        
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
        # Cleanup
        if test_file and test_file.exists():
            test_file.unlink()
        
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

