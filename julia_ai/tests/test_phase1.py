"""
JULIA AI - Phase 1 Test Suite.

This module contains tests to verify the Phase 1 skeleton is functional.
Tests check:
- Module imports work correctly
- Settings load properly
- Orchestrator initializes and starts
- Required directories exist

Run with: python tests/test_phase1.py
Expected output: "TEST PHASE 1: PASSED"
"""

import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


def test_imports():
    """Test that all core modules can be imported."""
    try:
        from config.settings import Settings, MODEL_ROUTING
        from core.orchestrator import Orchestrator
        return True
    except ImportError as e:
        print(f"  [FAIL] Import error: {e}")
        return False


def test_settings():
    """Test that Settings class works correctly."""
    try:
        from config.settings import Settings, MODEL_ROUTING
        
        settings = Settings()
        
        # Check BASE_DIR is set
        if not settings.BASE_DIR.exists():
            print(f"  [FAIL] BASE_DIR does not exist: {settings.BASE_DIR}")
            return False
        
        # Check LOGS_DIR exists (created on init)
        if not settings.LOGS_DIR.exists():
            print(f"  [FAIL] LOGS_DIR was not created: {settings.LOGS_DIR}")
            return False
        
        # Check MODEL_ROUTING has expected keys
        required_keys = ["reasoning", "coding", "fast"]
        for key in required_keys:
            if key not in MODEL_ROUTING:
                print(f"  [FAIL] MODEL_ROUTING missing key: {key}")
                return False
        
        return True
    except Exception as e:
        print(f"  [FAIL] Settings error: {e}")
        return False


def test_orchestrator():
    """Test that Orchestrator initializes and starts."""
    try:
        from config.settings import Settings
        from core.orchestrator import Orchestrator
        
        settings = Settings()
        orchestrator = Orchestrator(settings)
        
        # Test initialization
        if orchestrator.version != "0.1.0":
            print(f"  [FAIL] Wrong version: {orchestrator.version}")
            return False
        
        if orchestrator.status != "initialized":
            print(f"  [FAIL] Wrong initial status: {orchestrator.status}")
            return False
        
        # Test start
        success = orchestrator.start()
        if not success:
            print(f"  [FAIL] Orchestrator failed to start")
            return False
        
        if orchestrator.status != "online":
            print(f"  [FAIL] Wrong status after start: {orchestrator.status}")
            return False
        
        # Test get_status
        status = orchestrator.get_status()
        if "version" not in status or "status" not in status:
            print(f"  [FAIL] get_status() missing required fields")
            return False
        
        # Test stop
        orchestrator.stop()
        if orchestrator.status != "stopped":
            print(f"  [FAIL] Wrong status after stop: {orchestrator.status}")
            return False
        
        return True
    except Exception as e:
        print(f"  [FAIL] Orchestrator error: {e}")
        return False


def test_directories():
    """Test that required directories exist."""
    from config.settings import Settings
    
    settings = Settings()
    
    # Check BASE_DIR
    if not settings.BASE_DIR.exists():
        print(f"  [FAIL] BASE_DIR missing: {settings.BASE_DIR}")
        return False
    
    # Check LOGS_DIR
    if not settings.LOGS_DIR.exists():
        print(f"  [FAIL] LOGS_DIR missing: {settings.LOGS_DIR}")
        return False
    
    # Check config directory
    config_dir = settings.BASE_DIR / "config"
    if not config_dir.exists():
        print(f"  [FAIL] config/ directory missing")
        return False
    
    # Check core directory
    core_dir = settings.BASE_DIR / "core"
    if not core_dir.exists():
        print(f"  [FAIL] core/ directory missing")
        return False
    
    return True


def run_all_tests():
    """Run all Phase 1 tests and report results."""
    print("Running JULIA AI Phase 1 Tests...")
    print("-" * 40)
    
    tests = [
        ("Imports", test_imports),
        ("Settings", test_settings),
        ("Orchestrator", test_orchestrator),
        ("Directories", test_directories),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"- [{name}] ", end="")
        result = test_func()
        results.append(result)
        if result:
            print("PASS")
        else:
            print("FAIL")
    
    print("-" * 40)
    
    if all(results):
        print("TEST PHASE 1: PASSED")
        return 0
    else:
        print("TEST PHASE 1: FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
