#!/usr/bin/env python3
"""
Test Script for All Phases
Tests all functionality from Phase 1 to Phase 5
"""
import sys
import time
import requests
import subprocess
import psutil
from pathlib import Path
from logger import get_logger

logger = get_logger("TEST-ALL")

# Configuration
API_URL = "http://localhost:5001"
SCREENSHOT_DIR = Path.home() / "Documents" / "TestCaseScreenshots"
SERVICE_SCRIPT = Path(__file__).parent / "screenshot-service.py"
START_SCRIPT = Path(__file__).parent / "start-service.py"
STOP_SCRIPT = Path(__file__).parent / "stop-service.py"

# Test results
test_results = {
    "Phase 1 - Configuration": [],
    "Phase 2 - Service API": [],
    "Phase 3 - Watcher": [],
    "Phase 4 - Popup": [],
    "Phase 5 - Scripts": []
}

def test_pass(test_name):
    """Mark test as passed"""
    print(f"✅ {test_name}")
    return True

def test_fail(test_name, error=""):
    """Mark test as failed"""
    print(f"❌ {test_name}")
    if error:
        print(f"   Error: {error}")
    return False

def test_phase1():
    """Test Phase 1: Configuration"""
    print("\n" + "="*60)
    print("PHASE 1: CONFIGURATION")
    print("="*60)
    
    results = []
    
    # Test 1.1: Config file exists
    try:
        import config
        results.append(test_pass("1.1 - Config file exists and importable"))
    except Exception as e:
        results.append(test_fail("1.1 - Config file exists and importable", str(e)))
    
    # Test 1.2: Required config values
    try:
        import config
        required = ['API_PORT', 'SCREENSHOTS_DIR', 'LOG_FILE', 'LOG_LEVEL']
        missing = [attr for attr in required if not hasattr(config, attr)]
        if missing:
            results.append(test_fail("1.2 - Required config values", f"Missing: {missing}"))
        else:
            results.append(test_pass("1.2 - Required config values"))
    except Exception as e:
        results.append(test_fail("1.2 - Required config values", str(e)))
    
    # Test 1.3: Screenshot directory exists
    try:
        if SCREENSHOT_DIR.exists():
            results.append(test_pass("1.3 - Screenshot directory exists"))
        else:
            SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
            results.append(test_pass("1.3 - Screenshot directory created"))
    except Exception as e:
        results.append(test_fail("1.3 - Screenshot directory", str(e)))
    
    # Test 1.4: Logger setup
    try:
        from logger import setup_logger, get_logger
        logger_test = get_logger("TEST")
        logger_test.info("Test log message")
        results.append(test_pass("1.4 - Logger setup"))
    except Exception as e:
        results.append(test_fail("1.4 - Logger setup", str(e)))
    
    test_results["Phase 1 - Configuration"] = results
    return all(results)

def test_phase2():
    """Test Phase 2: Service API"""
    print("\n" + "="*60)
    print("PHASE 2: SERVICE API")
    print("="*60)
    
    results = []
    
    # Test 2.1: Service not running initially
    try:
        response = requests.get(f"{API_URL}/status", timeout=2)
        # If we get here, service is running (which is OK)
        results.append(test_pass("2.1 - Service accessible"))
    except requests.exceptions.ConnectionError:
        results.append(test_fail("2.1 - Service not running", "Start service first with: python3 start-service.py"))
        return False
    except Exception as e:
        results.append(test_fail("2.1 - Service check", str(e)))
        return False
    
    # Test 2.2: GET /status
    try:
        response = requests.get(f"{API_URL}/status", timeout=2)
        if response.status_code == 200:
            data = response.json()
            if 'watcher_running' in data:
                results.append(test_pass("2.2 - GET /status returns correct format"))
            else:
                results.append(test_fail("2.2 - GET /status format", "Missing 'watcher_running' field"))
        else:
            results.append(test_fail("2.2 - GET /status", f"Status code: {response.status_code}"))
    except Exception as e:
        results.append(test_fail("2.2 - GET /status", str(e)))
    
    # Test 2.3: POST /start
    try:
        response = requests.post(f"{API_URL}/start", json={}, timeout=2)
        if response.status_code == 200:
            data = response.json()
            if data.get('success') == True or data.get('watcher_running') == True:
                results.append(test_pass("2.3 - POST /start works"))
            else:
                results.append(test_fail("2.3 - POST /start", "Service not started"))
        else:
            results.append(test_fail("2.3 - POST /start", f"Status code: {response.status_code}"))
    except Exception as e:
        results.append(test_fail("2.3 - POST /start", str(e)))
    
    # Test 2.4: POST /stop
    try:
        response = requests.post(f"{API_URL}/stop", timeout=2)
        if response.status_code == 200:
            data = response.json()
            if data.get('success') == True or data.get('watcher_running') == False:
                results.append(test_pass("2.4 - POST /stop works"))
            else:
                results.append(test_fail("2.4 - POST /stop", "Service not stopped"))
        else:
            results.append(test_fail("2.4 - POST /stop", f"Status code: {response.status_code}"))
    except Exception as e:
        results.append(test_fail("2.4 - POST /stop", str(e)))
    
    # Test 2.5: Restart for next tests
    try:
        response = requests.post(f"{API_URL}/start", json={}, timeout=2)
        if response.status_code == 200:
            results.append(test_pass("2.5 - Service restarted for next tests"))
        else:
            results.append(test_fail("2.5 - Restart", f"Status code: {response.status_code}"))
    except Exception as e:
        results.append(test_fail("2.5 - Restart", str(e)))
    
    test_results["Phase 2 - Service API"] = results
    return all(results)

def test_phase3():
    """Test Phase 3: Watcher"""
    print("\n" + "="*60)
    print("PHASE 3: WATCHER")
    print("="*60)
    
    results = []
    
    # Test 3.1: Watcher process running
    try:
        watcher_found = False
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = proc.info.get('cmdline', [])
                if cmdline and 'screenshot-watcher.py' in ' '.join(cmdline):
                    watcher_found = True
                    results.append(test_pass("3.1 - Watcher process running"))
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        if not watcher_found:
            results.append(test_fail("3.1 - Watcher process not found", "Activate service first"))
    except Exception as e:
        results.append(test_fail("3.1 - Watcher check", str(e)))
    
    # Test 3.2: Watcher starts when service activated
    try:
        # Stop first
        requests.post(f"{API_URL}/stop", timeout=2)
        time.sleep(1)
        
        # Check watcher stopped
        watcher_running = False
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = proc.info.get('cmdline', [])
                if cmdline and 'screenshot-watcher.py' in ' '.join(cmdline):
                    watcher_running = True
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        if watcher_running:
            results.append(test_fail("3.2 - Watcher should stop on stop"))
        else:
            results.append(test_pass("3.2 - Watcher stops on stop"))
        
        # Restart
        requests.post(f"{API_URL}/start", json={}, timeout=2)
        time.sleep(2)
        
        # Check watcher started
        watcher_running = False
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = proc.info.get('cmdline', [])
                if cmdline and 'screenshot-watcher.py' in ' '.join(cmdline):
                    watcher_running = True
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        if watcher_running:
            results.append(test_pass("3.3 - Watcher starts on start"))
        else:
            results.append(test_fail("3.3 - Watcher should start on start"))
            
    except Exception as e:
        results.append(test_fail("3.2/3.3 - Watcher start/stop", str(e)))
    
    test_results["Phase 3 - Watcher"] = results
    return all(results)

def test_phase4():
    """Test Phase 4: Popup"""
    print("\n" + "="*60)
    print("PHASE 4: POPUP")
    print("="*60)
    
    results = []
    
    # Test 4.1: Service must be active for popup
    try:
        # Ensure service is started
        response = requests.post(f"{API_URL}/start", json={}, timeout=2)
        if response.status_code == 200:
            results.append(test_pass("4.1 - Service started for popup test"))
        else:
            results.append(test_fail("4.1 - Service start", f"Status: {response.status_code}"))
    except Exception as e:
        results.append(test_fail("4.1 - Service start", str(e)))
    
    # Test 4.2: Popup script exists
    try:
        popup_script = Path(__file__).parent / "description_dialog.py"
        if popup_script.exists():
            results.append(test_pass("4.2 - Popup script exists"))
        else:
            results.append(test_fail("4.2 - Popup script missing"))
    except Exception as e:
        results.append(test_fail("4.2 - Popup script check", str(e)))
    
    # Test 4.3: Popup can be imported
    try:
        import description_dialog
        results.append(test_pass("4.3 - Popup script importable"))
    except Exception as e:
        results.append(test_fail("4.3 - Popup script import", str(e)))
    
    # Note: Actual popup display test requires manual screenshot
    print("\n⚠️  Note: To test popup display, take a screenshot (Shift+Cmd+4)")
    print("   The popup should appear automatically if service is active")
    
    test_results["Phase 4 - Popup"] = results
    return all(results)

def test_phase5():
    """Test Phase 5: Scripts de gestion"""
    print("\n" + "="*60)
    print("PHASE 5: SCRIPTS DE GESTION")
    print("="*60)
    
    results = []
    
    # Test 5.1: start-service.py exists and is executable
    try:
        if START_SCRIPT.exists():
            results.append(test_pass("5.1 - start-service.py exists"))
        else:
            results.append(test_fail("5.1 - start-service.py missing"))
    except Exception as e:
        results.append(test_fail("5.1 - start-service.py check", str(e)))
    
    # Test 5.2: stop-service.py exists
    try:
        if STOP_SCRIPT.exists():
            results.append(test_pass("5.2 - stop-service.py exists"))
        else:
            results.append(test_fail("5.2 - stop-service.py missing"))
    except Exception as e:
        results.append(test_fail("5.2 - stop-service.py check", str(e)))
    
    # Test 5.3: stop-service.py can find and stop service
    try:
        # Check if service is running
        service_running = False
        service_pid = None
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = proc.info.get('cmdline', [])
                if cmdline and 'screenshot-service.py' in ' '.join(cmdline):
                    service_running = True
                    service_pid = proc.info['pid']
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        if service_running:
            # Try to stop it
            result = subprocess.run(
                [sys.executable, str(STOP_SCRIPT)],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                results.append(test_pass("5.3 - stop-service.py can stop service"))
            else:
                results.append(test_fail("5.3 - stop-service.py failed", result.stderr))
        else:
            results.append(test_pass("5.3 - stop-service.py (service not running)"))
    except Exception as e:
        results.append(test_fail("5.3 - stop-service.py test", str(e)))
    
    # Test 5.4: start-service.py can start service (in background)
    try:
        # Start service in background
        process = subprocess.Popen(
            [sys.executable, str(SERVICE_SCRIPT)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a bit for service to start
        time.sleep(3)
        
        # Check if service is responding
        try:
            response = requests.get(f"{API_URL}/status", timeout=2)
            if response.status_code == 200:
                results.append(test_pass("5.4 - Service can be started"))
            else:
                results.append(test_fail("5.4 - Service started but not responding"))
        except requests.exceptions.ConnectionError:
            results.append(test_fail("5.4 - Service not responding after start"))
        
        # Keep process reference for cleanup
        test_phase5.service_process = process
        
    except Exception as e:
        results.append(test_fail("5.4 - Service start test", str(e)))
    
    # Test 5.5: Logging in scripts
    try:
        import config
        log_file = Path(config.LOG_FILE)
        if log_file.exists():
            # Check if logs contain start/stop entries
            log_content = log_file.read_text()
            if "START-SCRIPT" in log_content or "STOP-SCRIPT" in log_content:
                results.append(test_pass("5.5 - Scripts log to file"))
            else:
                results.append(test_fail("5.5 - Scripts not logging", "No START/STOP entries found"))
        else:
            results.append(test_fail("5.5 - Log file not found", f"Expected: {log_file}"))
    except Exception as e:
        results.append(test_fail("5.5 - Logging check", str(e)))
    
    test_results["Phase 5 - Scripts"] = results
    return all(results)

def print_summary():
    """Print test summary"""
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    total_tests = 0
    passed_tests = 0
    
    for phase, results in test_results.items():
        phase_passed = sum(1 for r in results if r)
        phase_total = len(results)
        total_tests += phase_total
        passed_tests += phase_passed
        
        status = "✅ PASS" if phase_passed == phase_total else "⚠️  PARTIAL" if phase_passed > 0 else "❌ FAIL"
        print(f"\n{phase}: {status} ({phase_passed}/{phase_total})")
        for i, result in enumerate(results, 1):
            status_icon = "✅" if result else "❌"
            print(f"  {status_icon} Test {i}")
    
    print(f"\n{'='*60}")
    print(f"TOTAL: {passed_tests}/{total_tests} tests passed")
    print(f"{'='*60}\n")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed!")
        return True
    else:
        print("⚠️  Some tests failed. Review the output above.")
        return False

def cleanup():
    """Cleanup test processes"""
    try:
        if hasattr(test_phase5, 'service_process'):
            test_phase5.service_process.terminate()
            test_phase5.service_process.wait(timeout=5)
    except:
        pass

if __name__ == "__main__":
    print("\n" + "="*60)
    print("SCREENSHOT CAPTURE SERVICE - COMPLETE TEST SUITE")
    print("="*60)
    print("\n⚠️  IMPORTANT: Make sure the service is running before starting tests")
    print("   Start it with: python3 screenshot-capture-service/start-service.py")
    print("   Or run it in background: python3 screenshot-capture-service/screenshot-service.py &\n")
    
    input("Press Enter to start tests...")
    
    try:
        # Run all phase tests
        test_phase1()
        test_phase2()
        test_phase3()
        test_phase4()
        test_phase5()
        
        # Print summary
        all_passed = print_summary()
        
        # Cleanup
        cleanup()
        
        sys.exit(0 if all_passed else 1)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        cleanup()
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Test suite error: {e}")
        import traceback
        traceback.print_exc()
        cleanup()
        sys.exit(1)

