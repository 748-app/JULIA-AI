"""
Core module for JULIA AI.

This module contains the central orchestration logic:
- Orchestrator: The brain of the system that coordinates all agents and tasks

The core module is the heart of JULIA AI's multi-agent architecture.
In Phase 1, it contains only the Orchestrator as a minimal skeleton.
Future phases will add agent coordination, workflow management, and task execution.
"""

from core.orchestrator import Orchestrator

__all__ = ["Orchestrator"]
