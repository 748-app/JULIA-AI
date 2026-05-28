"""
Configuration module for JULIA AI.

This module centralizes all configuration settings including:
- API keys for LLM providers (DeepSeek, Mistral, Tavily)
- Model routing strategy for dynamic model selection
- Application-wide settings (debug mode, log level)

Usage:
    from config.settings import Settings, MODEL_ROUTING
    settings = Settings()
"""

from config.settings import Settings, MODEL_ROUTING

__all__ = ["Settings", "MODEL_ROUTING"]
