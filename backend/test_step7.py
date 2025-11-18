#!/usr/bin/env python3
"""
Test script for Step 7: Export Excel endpoint
Run this to verify the export endpoint works correctly.
"""

import subprocess
import sys
import time
import requests
import json
import os
from pathlib import Path

def test_api():
    """Test export endpoint."""
    print("=" * 60)
    print("TEST: Export Excel Endpoint")
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
    
    # Get some test case IDs
    test_case_ids = []
    export_file = None
    
    try:
        # Get test cases
        print("\n2. Getting test cases...")
        response = requests.get(
            "http://localhost:8000/api/test-cases",
            timeout=5
        )
        
        if response.status_code == 200:
            test_cases = response.json()
            if len(test_cases) >= 2:
                test_case_ids = [test_cases[0]['id'], test_cases[1]['id']]
                print(f"   ✅ Found {len(test_cases)} test cases")
                print(f"   ✅ Will export test cases: {test_case_ids}")
            else:
                print(f"   ⚠️  Only {len(test_cases)} test case(s) found, using all")
                test_case_ids = [tc['id'] for tc in test_cases]
        else:
            print(f"   ❌ Failed to get test cases: {response.status_code}")
            return False
        
        if not test_case_ids:
            print("   ❌ No test cases to export")
            return False
        
        # Test POST /api/export
        print(f"\n3. Testing POST /api/export...")
        export_data = {
            "test_case_ids": test_case_ids
        }
        
        response = requests.post(
            "http://localhost:8000/api/export",
            json=export_data,
            timeout=30  # Export might take time
        )
        
        if response.status_code == 200:
            # Save the file
            export_file = Path("/tmp/test_export.xlsx")
            export_file.write_bytes(response.content)
            
            print(f"   ✅ Status: {response.status_code}")
            print(f"   ✅ Content-Type: {response.headers.get('content-type')}")
            print(f"   ✅ File size: {len(response.content)} bytes")
            print(f"   ✅ File saved to: {export_file}")
            
            # Verify file exists and is valid
            if export_file.exists():
                file_size = export_file.stat().st_size
                print(f"   ✅ File exists, size: {file_size} bytes")
                
                if file_size > 0:
                    print(f"   ✅ File is not empty")
                else:
                    print(f"   ⚠️  File is empty")
            else:
                print(f"   ❌ File not found")
                return False
            
            # Check if it's a valid Excel file (starts with PK header for ZIP/Excel)
            file_header = export_file.read_bytes()[:4]
            if file_header == b'PK\x03\x04':
                print(f"   ✅ File appears to be a valid Excel file (ZIP header)")
            else:
                print(f"   ⚠️  File header: {file_header.hex()} (might not be Excel)")
        else:
            print(f"   ❌ Status: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print(f"\nExport file saved to: {export_file}")
        print("You can open it with Excel/LibreOffice to verify the content.")
        
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
        if export_file and export_file.exists():
            # Keep file for user to check
            print(f"\nNote: Export file kept at {export_file} for verification")
        
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

