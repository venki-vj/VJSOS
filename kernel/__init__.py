"""
VJSOS-AI Kernel - Core System Components

This package provides the foundational components for the AI Operating System:

- SystemGovernor: Constitutional authority, singleton decision-maker
- Orchestrator: Task coordination and agent management
- ContextEngine: Minimal context assembly with relevance scoring
- MemoryEngine: 4-tier memory architecture
- QAEngine: Multi-check verification framework
- EventBus: Structured message passing
"""

from kernel.governor import SystemGovernor
from kernel.orchestrator import Orchestrator
from kernel.context_engine import ContextEngine
from kernel.memory_engine import MemoryEngine, MemoryTier, MemoryObject
from kernel.qa_engine import QAEngine
from kernel.event_bus import EventBus, MessageBus

__all__ = [
    "SystemGovernor",
    "Orchestrator",
    "ContextEngine",
    "MemoryEngine",
    "MemoryTier",
    "MemoryObject",
    "QAEngine",
    "EventBus",
    "MessageBus",
]

__version__ = "1.0.0"