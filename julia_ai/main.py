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
        print(f"[SUCCESS] JULIA AI ready - Phase 1 complete")
        print(f"         Version: {status['version']}")
        print(f"         Status: {status['status']}")
        print(f"         Models configured: {status['models_configured']}")
        
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
