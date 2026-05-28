"""
JULIA AI Orchestrator - The Central Brain.

This module implements the Orchestrator, which is the single decision-making
entity in the JULIA AI multi-agent system. The Orchestrator:

- Understands user requests and identifies task types
- Plans workflows and decomposes complex tasks
- Selects appropriate agents (in future phases)
- Coordinates execution and validates results
- Manages context and memory access

Phase 1 Status:
    This is a minimal skeleton implementation. The Orchestrator:
    - Initializes with configuration settings
    - Provides basic status reporting
    - Logs system state for debugging
    
    Actual orchestration logic (agent selection, workflow execution,
    task planning) will be implemented in Phases 2-3.

Architecture Principle:
    NO agent decides independently. All decisions flow through the Orchestrator.
    This ensures coherent behavior and prevents conflicting actions.
"""

import logging
from pathlib import Path
from datetime import datetime
from config.settings import Settings, MODEL_ROUTING
from memory.short_term import ShortTermMemory
from memory.long_term import LongTermMemory
from memory.vector_store import VectorStore


class Orchestrator:
    """
    Central orchestrator for JULIA AI multi-agent system.
    
    The Orchestrator is the brain of the system. It receives user requests,
    analyzes them, plans execution strategies, and coordinates specialized
    agents to complete tasks.
    
    In Phase 1, this class provides:
    - Initialization and configuration loading
    - Logging setup
    - Status reporting
    - Basic readiness checks
    
    Future phases will add:
    - Task analysis and classification
    - Workflow planning
    - Agent selection and coordination
    - Result validation and synthesis
    """
    
    def __init__(self, settings: Settings = None):
        """
        Initialize the Orchestrator.
        
        Args:
            settings: Optional Settings instance. If not provided, creates new one.
        """
        self.settings = settings or Settings()
        self.version = "0.2.0"
        self.status = "initialized"
        self.started_at = None
        
        # Initialize memory systems
        self.short_term = ShortTermMemory(ttl_seconds=300)
        self.long_term = LongTermMemory(self.settings.DATA_DIR / "memory.db")
        self.vector_store = VectorStore(self.settings.DATA_DIR / "vector_store")
        
        # Setup logging
        self._setup_logging()
        
        self.logger.info(f"Orchestrator v{self.version} initialized")
        self.logger.info(f"Debug mode: {self.settings.DEBUG}")
        self.logger.info(f"Log level: {self.settings.LOG_LEVEL}")
    
    def _setup_logging(self):
        """
        Configure Python's standard logging module.
        
        Creates a log file in the logs/ directory with timestamp.
        Also sets up console logging if DEBUG mode is enabled.
        
        Windows Compatibility:
            Uses pathlib.Path for all file operations.
            Explicit UTF-8 encoding for cross-platform consistency.
        """
        self.logger = logging.getLogger("julia_ai.orchestrator")
        self.logger.setLevel(getattr(logging, self.settings.LOG_LEVEL))
        
        # Clear existing handlers to avoid duplicates
        self.logger.handlers.clear()
        
        # Create formatter
        formatter = logging.Formatter(
            "[%(levelname)s] %(asctime)s - %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # File handler - logs to logs/julia_YYYYMMDD.log
        log_file = self.settings.LOGS_DIR / f"julia_{datetime.now().strftime('%Y%m%d')}.log"
        try:
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setLevel(logging.DEBUG)  # Log everything to file
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        except Exception as e:
            # Fallback: skip file logging if directory not writable
            pass
        
        # Console handler - only if DEBUG mode
        if self.settings.DEBUG:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
    
    def start(self):
        """
        Start the Orchestrator and bring the system online.
        
        This method initializes all subsystems and marks the Orchestrator
        as ready to accept tasks.
        
        Returns:
            True if startup successful, False otherwise
        """
        try:
            self.started_at = datetime.now()
            self.status = "online"
            
            self.logger.info("=" * 60)
            self.logger.info("JULIA AI System Starting")
            self.logger.info("=" * 60)
            self.logger.info(f"Version: {self.version}")
            self.logger.info(f"Base directory: {self.settings.BASE_DIR}")
            self.logger.info(f"Logs directory: {self.settings.LOGS_DIR}")
            
            # Log model routing configuration
            self.logger.info("Model routing configured:")
            for task_type, model in MODEL_ROUTING.items():
                self.logger.info(f"  - {task_type}: {model}")
            
            # Check API keys availability (informational only)
            for provider in ["deepseek", "mistral", "tavily"]:
                if self.settings.is_api_key_set(provider):
                    self.logger.info(f"API key configured: {provider.upper()}")
                else:
                    self.logger.warning(f"API key NOT configured: {provider.upper()}")
            
            self.logger.info("=" * 60)
            self.logger.info("JULIA AI Ready")
            self.logger.info("=" * 60)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start Orchestrator: {e}")
            self.status = "error"
            return False
    
    def get_status(self) -> dict:
        """
        Get current system status.
        
        Returns:
            Dictionary containing:
            - version: JULIA AI version string
            - status: Current status (initialized, online, error)
            - started_at: Startup timestamp (if started)
            - debug_mode: Debug mode flag
            - models_configured: Number of model routes configured
        """
        return {
            "version": self.version,
            "status": self.status,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "debug_mode": self.settings.DEBUG,
            "models_configured": len(MODEL_ROUTING),
        }
    
    def stop(self):
        """
        Gracefully shutdown the Orchestrator.
        
        Logs shutdown event and updates status.
        Future phases will add cleanup of agents, connections, etc.
        """
        self.logger.info("Shutting down JULIA AI...")
        # Close long-term memory connection
        self.long_term.close()
        self.status = "stopped"
        self.logger.info("Orchestrator stopped")

    def dispatch_memory(self, action: str, data: dict) -> any:
        """
        Dispatch memory operations to appropriate memory system.
        
        Args:
            action: Type of action (store, retrieve, delete, search).
            data: Dictionary containing operation parameters.
        
        Returns:
            Result of the memory operation.
        """
        if action == "store_short":
            key = data.get("key")
            value = data.get("value")
            ttl = data.get("ttl")
            self.short_term.set(key, value, ttl)
            return True
        
        elif action == "retrieve_short":
            key = data.get("key")
            return self.short_term.get(key)
        
        elif action == "store_long":
            key = data.get("key")
            value = data.get("value")
            project_id = data.get("project_id", "default")
            return self.long_term.store(key, value, project_id)
        
        elif action == "retrieve_long":
            key = data.get("key")
            project_id = data.get("project_id")
            return self.long_term.retrieve(key, project_id)
        
        elif action == "vector_add":
            doc_id = data.get("id")
            text = data.get("text")
            metadata = data.get("metadata")
            return self.vector_store.add(doc_id, text, metadata)
        
        elif action == "vector_search":
            query = data.get("query")
            n_results = data.get("n_results", 5)
            return self.vector_store.search(query, n_results)
        
        else:
            self.logger.warning(f"Unknown memory action: {action}")
            return None

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"<Orchestrator v{self.version} status={self.status}>"
