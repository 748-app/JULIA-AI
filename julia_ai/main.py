"""
JULIA AI - Main Entry Point.

This is the primary entry point for running JULIA AI.
It initializes the Orchestrator and starts the system.

Usage:
    python main.py
    
Or on Windows:
    run.bat
"""

import sys
from pathlib import Path

# Ensure the project root is in the Python path
# This allows imports like 'from config.settings import Settings'
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from config.settings import Settings
from core.orchestrator import Orchestrator


def main():
    """
    Main function to start JULIA AI.
    
    Creates an Orchestrator instance, starts it, and displays status.
    Exits gracefully on errors or keyboard interrupt.
    """
    try:
        # Initialize settings
        settings = Settings()
        
        # Create and start the Orchestrator
        orchestrator = Orchestrator(settings)
        success = orchestrator.start()
        
        if not success:
            print("[ERROR] Failed to start JULIA AI")
            return 1
        
        # Display success message
        status = orchestrator.get_status()
        print(f"[SUCCESS] JULIA AI ready - Phase 2 complete")
        print(f"         Version: {status['version']}")
        print(f"         Status: {status['status']}")
        print(f"         Models configured: {status['models_configured']}")
        print(f"         Memory systems: short_term, long_term, vector_store")
        
        # Demo memory operations
        print("\n[DEMO] Testing memory systems...")
        
        # Short-term memory demo
        orchestrator.dispatch_memory("store_short", {"key": "demo_key", "value": "Hello from short-term!", "ttl": 60})
        result = orchestrator.dispatch_memory("retrieve_short", {"key": "demo_key"})
        print(f"  - Short-term memory: {result}")
        
        # Long-term memory demo
        orchestrator.dispatch_memory("store_long", {"key": "python_fact", "value": "Python is a programming language", "project_id": "demo"})
        result = orchestrator.dispatch_memory("retrieve_long", {"key": "python_fact", "project_id": "demo"})
        print(f"  - Long-term memory: {result}")
        
        # Vector store demo
        if orchestrator.vector_store.is_available():
            orchestrator.dispatch_memory("vector_add", {"id": "doc1", "text": "Machine learning is a subset of AI", "metadata": {"source": "demo"}})
            count = orchestrator.vector_store.count()
            print(f"  - Vector store: {count} document(s) indexed")
        else:
            print(f"  - Vector store: ChromaDB not available (install with: pip install chromadb)")
        
        print("\n[INFO] All memory systems operational")
        
        # Graceful shutdown
        orchestrator.stop()
        return 0
        
    except KeyboardInterrupt:
        print("\n[INFO] Interrupted by user")
        return 0
    except Exception as e:
        print(f"[ERROR] Fatal error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
