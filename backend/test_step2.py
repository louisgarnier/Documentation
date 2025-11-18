#!/usr/bin/env python3
"""
Test script for Step 2: Basic API structure
Run this to verify the API starts correctly.
"""

import subprocess
import sys
import time
import requests

def test_api():
    """Test that the API starts and responds correctly."""
    print("=" * 60)
    print("TEST: API Basic Structure")
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
        # Test root endpoint
        print("\n2. Testing GET / endpoint...")
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {response.status_code}")
            print(f"   ✅ Response: {data}")
            if data.get("status") == "ok":
                print("   ✅ Root endpoint works!")
            else:
                print("   ❌ Unexpected response format")
                return False
        else:
            print(f"   ❌ Status: {response.status_code}")
            return False
        
        # Test health endpoint
        print("\n3. Testing GET /health endpoint...")
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {response.status_code}")
            print(f"   ✅ Response: {data}")
            print("   ✅ Health endpoint works!")
        else:
            print(f"   ❌ Status: {response.status_code}")
            return False
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Open http://localhost:8000/docs in your browser")
        print("2. You should see the Swagger UI documentation")
        print("3. Test the endpoints interactively")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("   ❌ Could not connect to server")
        print("   Make sure the server started correctly")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
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

