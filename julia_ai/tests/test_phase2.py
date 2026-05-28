"""Phase 2 Memory Tests.

Tests for short-term, long-term, and vector memory systems.
Run with: python tests/test_phase2.py
"""

import sys
import time
from pathlib import Path

# Ensure project root is in path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from memory.short_term import ShortTermMemory
from memory.long_term import LongTermMemory
from memory.vector_store import VectorStore
from core.orchestrator import Orchestrator
from config.settings import Settings


def test_short_term_memory():
    """Test short-term memory with TTL."""
    print("Testing short-term memory...")
    
    # Create with very short TTL for testing
    stm = ShortTermMemory(ttl_seconds=2)
    
    # Store and retrieve
    stm.set("test_key", "test_value")
    result = stm.get("test_key")
    assert result == "test_value", f"Expected 'test_value', got {result}"
    
    # Wait for expiration
    time.sleep(3)
    result = stm.get("test_key")
    assert result is None, f"Expected None (expired), got {result}"
    
    print("  [PASS] Short-term memory with TTL works correctly")
    return True


def test_long_term_memory():
    """Test long-term SQLite storage."""
    print("Testing long-term memory...")
    
    # Use temp database
    db_path = Path(__file__).parent / "test_memory.db"
    ltm = LongTermMemory(db_path)
    
    try:
        # Store a fact
        ltm.store("python", "Python is a programming language", "test_project")
        
        # Retrieve by key
        result = ltm.retrieve("python", "test_project")
        assert result is not None, "Expected to retrieve stored value"
        assert "language" in result.lower(), f"Expected 'language' in result, got: {result}"
        
        # Clean up
        ltm.delete("python", "test_project")
        
        print("  [PASS] Long-term memory stores and retrieves correctly")
        return True
        
    finally:
        ltm.close()
        # Remove test database
        if db_path.exists():
            db_path.unlink()


def test_vector_store():
    """Test vector store initialization."""
    print("Testing vector store...")
    
    # Use temp directory
    vs_dir = Path(__file__).parent / "test_vector_store"
    vs = VectorStore(vs_dir)
    
    # Check if ChromaDB is available
    if vs.is_available():
        print("  [PASS] Vector store initialized (ChromaDB available)")
        return True
    else:
        print("  [PASS] Vector store initialized (ChromaDB not installed - graceful fallback)")
        return True
    
    # Cleanup
    if vs_dir.exists():
        import shutil
        shutil.rmtree(vs_dir, ignore_errors=True)


def test_orchestrator_dispatch():
    """Test orchestrator memory dispatch."""
    print("Testing orchestrator dispatch_memory...")
    
    settings = Settings()
    orch = Orchestrator(settings)
    
    # Test short-term via orchestrator
    orch.dispatch_memory("store_short", {"key": "orch_key", "value": "orch_value"})
    result = orch.dispatch_memory("retrieve_short", {"key": "orch_key"})
    assert result == "orch_value", f"Expected 'orch_value', got {result}"
    
    # Test long-term via orchestrator
    orch.dispatch_memory("store_long", {"key": "fact1", "value": "Test fact", "project_id": "test"})
    result = orch.dispatch_memory("retrieve_long", {"key": "fact1", "project_id": "test"})
    assert result == "Test fact", f"Expected 'Test fact', got {result}"
    
    print("  [PASS] Orchestrator dispatch_memory works correctly")
    return True


def run_all_tests():
    """Run all Phase 2 tests."""
    print("=" * 60)
    print("PHASE 2 MEMORY TESTS")
    print("=" * 60)
    
    tests = [
        test_short_term_memory,
        test_long_term_memory,
        test_vector_store,
        test_orchestrator_dispatch,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  [FAIL] {test.__name__}: {e}")
            failed += 1
    
    print("=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("\nTEST PHASE 2: PASSED\n")
        return 0
    else:
        print(f"\nTEST PHASE 2: FAILED ({failed} test(s) failed)\n")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
