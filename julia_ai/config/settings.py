"""
JULIA AI Configuration Settings.

This module contains all configuration for the JULIA AI system:
- API keys loaded from environment variables (.env file)
- Model routing map for dynamic LLM selection based on task type
- Application settings (debug mode, log level, paths)

Model Routing Strategy (Phase 1 - Configuration Only):
    The MODEL_ROUTING dictionary defines which model to use for each task type.
    Actual routing logic will be implemented in Phase 3 when agents are added.
    
    - reasoning: DeepSeek v4-pro (deep reasoning, planning, architecture)
    - coding: Codestral (code generation, completion, infilling)
    - fast: Mistral small (quick responses, simple tasks)
    - analysis: Mistral large (text analysis, document understanding)
    - fallback: Mistral medium (backup when primary fails)

Windows Compatibility:
    All paths use pathlib.Path for cross-platform compatibility.
    No hardcoded slashes (/ or \\) anywhere in this module.
"""

import os
from pathlib import Path
from dotenv import load_dotenv


class Settings:
    """
    Central configuration class for JULIA AI.
    
    Loads environment variables from .env file if present,
    otherwise uses system environment variables.
    
    Attributes:
        DEEPSEEK_API_KEY: API key for DeepSeek models
        MISTRAL_API_KEY: API key for Mistral AI models (includes Codestral)
        TAVILY_API_KEY: API key for Tavily web search
        DEBUG: Debug mode flag (enables verbose logging)
        LOG_LEVEL: Logging level (DEBUG, INFO, WARNING, ERROR)
        BASE_DIR: Root directory of the JULIA AI project
        LOGS_DIR: Directory for log files
    """
    
    def __init__(self):
        """Initialize settings by loading environment variables."""
        # Get the base directory (parent of config/)
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        
        # Load .env file if it exists (silent failure if not found)
        env_path = self.BASE_DIR / ".env"
        load_dotenv(dotenv_path=env_path, verbose=False)
        
        # API Keys (None if not set - will cause runtime error if used)
        self.DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
        self.MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
        self.TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
        
        # Application settings
        self.DEBUG = os.getenv("JULIA_DEBUG", "false").lower() == "true"
        self.LOG_LEVEL = os.getenv("JULIA_LOG_LEVEL", "INFO").upper()
        
        # Paths (using pathlib for Windows compatibility)
        self.LOGS_DIR = self.BASE_DIR / "logs"
        self.DATA_DIR = self.BASE_DIR / "data"
        
        # Ensure directories exist
        self.LOGS_DIR.mkdir(parents=True, exist_ok=True)
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    def is_api_key_set(self, provider: str) -> bool:
        """
        Check if an API key is configured for a provider.
        
        Args:
            provider: One of 'deepseek', 'mistral', 'tavily'
            
        Returns:
            True if API key is set and non-empty, False otherwise
        """
        key_map = {
            "deepseek": self.DEEPSEEK_API_KEY,
            "mistral": self.MISTRAL_API_KEY,
            "tavily": self.TAVILY_API_KEY,
        }
        key = key_map.get(provider.lower())
        return key is not None and len(key.strip()) > 0
    
    def get_api_endpoint(self, provider: str) -> str:
        """
        Get the API endpoint URL for a provider.
        
        Args:
            provider: One of 'deepseek', 'mistral', 'codestral'
            
        Returns:
            Base URL for the provider's API
        """
        endpoints = {
            "deepseek": "https://api.deepseek.com/v1",
            "mistral": "https://api.mistral.ai/v1",
            "codestral": "https://codestral.mistral.ai/v1",
        }
        return endpoints.get(provider.lower(), "")


# Model Routing Map (Phase 1: Configuration only)
# This defines the strategy for selecting models based on task type.
# Actual implementation of dynamic routing will happen in Phase 3.
MODEL_ROUTING = {
    "reasoning": "deepseek-v4-pro",      # Deep reasoning, planning, architecture
    "coding": "codestral-latest",         # Code generation, completion, FIM
    "fast": "mistral-small",              # Quick responses, simple tasks
    "analysis": "mistral-large-latest",   # Text analysis, document understanding
    "fallback": "mistral-medium",         # Backup when primary model fails
}

# Default model to use when no specific task type is specified
DEFAULT_MODEL = MODEL_ROUTING["fast"]

# Available providers (for future multi-provider support)
AVAILABLE_PROVIDERS = ["deepseek", "mistral", "codestral"]
