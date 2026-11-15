"""
Plugin SDK - Base Plugin Class

Defines the abstract base class all VJSOS-AI plugins must implement.
Interface version: vjsos-ai-plugin-v1
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List, AsyncIterator
from enum import Enum


class PluginCapability(Enum):
    """Capabilities a plugin can declare."""
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    STREAM = "stream"
    AUTH = "auth"
    WEBHOOK = "webhook"
    FILE_IO = "file_io"
    NETWORK = "network"
    DATABASE = "database"
    AI_MODEL = "ai_model"
    CODE_EXECUTION = "code_execution"


class PluginState(Enum):
    """Plugin lifecycle states."""
    INSTALLED = "installed"
    PENDING_GOVERNOR_REVIEW = "pending_governor_review"
    PENDING_QA = "pending_qa"
    APPROVED = "approved"
    ACTIVE = "active"
    INACTIVE = "inactive"
    REJECTED = "rejected"
    DEPRECATED = "deprecated"


class PluginInterface(ABC):
    """Abstract interface all plugins must implement."""

    # Required metadata - overridden by concrete plugins
    plugin_id: str = ""
    name: str = ""
    version: str = "0.0.0"
    description: str = ""
    plugin_type: str = "generic"
    interface_version: str = "vjsos-ai-plugin-v1"

    # Capabilities
    capabilities: List[str] = []
    required_permissions: List[str] = []
    rate_limits: Dict[str, Any] = {"calls_per_minute": 1000, "calls_per_hour": 100000}

    # Governance
    governor_approval: bool = True
    qa_status: str = "pending"
    last_audited: str = ""
    configuration_schema: Dict[str, Any] = {}

    # Auth
    auth_method: str = "api_key"
    auth_config: Dict[str, Any] = {}

    # Events
    events_subscribed: List[str] = []
    events_published: List[str] = []

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.state = PluginState.INSTALLED
        self._handlers: Dict[str, Any] = {}

    # === Lifecycle Methods ===

    async def on_install(self) -> Dict[str, Any]:
        """Called when plugin is installed. Override for custom logic."""
        return {"status": "installed"}

    async def on_activate(self) -> Dict[str, Any]:
        """Called when plugin is activated. Override for custom logic."""
        self.state = PluginState.ACTIVE
        return {"status": "activated"}

    async def on_deactivate(self) -> Dict[str, Any]:
        """Called when plugin is deactivated. Override for custom logic."""
        self.state = PluginState.INACTIVE
        return {"status": "deactivated"}

    async def on_uninstall(self) -> Dict[str, Any]:
        """Called when plugin is uninstalled. Override for custom logic."""
        return {"status": "uninstalled"}

    # === Core Execution Methods ===

    @abstractmethod
    async def execute(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a plugin endpoint. Must be implemented by concrete plugins."""
        raise NotImplementedError

    # === Event Methods ===

    async def on_event(self, event_type: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Handle a subscribed event. Override for custom event handling."""
        return None

    async def stream(self, endpoint: str, params: Dict[str, Any]) -> AsyncIterator[Dict[str, Any]]:
        """Stream data from the plugin. Override for streaming endpoints."""
        if False:
            yield {}
        raise NotImplementedError("Streaming not supported")

    # === Health & Status ===

    async def health_check(self) -> Dict[str, Any]:
        """Check plugin health. Override for custom health checks."""
        return {
            "status": "healthy",
            "plugin_id": self.plugin_id,
            "version": self.version,
            "state": self.state.value
        }

    def get_manifest(self) -> Dict[str, Any]:
        """Get the plugin manifest."""
        return {
            "plugin_id": self.plugin_id,
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "type": self.plugin_type,
            "interface_version": self.interface_version,
            "capabilities": self.capabilities,
            "required_permissions": self.required_permissions,
            "rate_limits": self.rate_limits,
            "governor_approval": self.governor_approval,
            "qa_status": self.qa_status,
            "last_audited": self.last_audited,
            "auth_method": self.auth_method,
            "auth_config": self.auth_config,
            "events_subscribed": self.events_subscribed,
            "events_published": self.events_published,
            "configuration_schema": self.configuration_schema
        }

    def validate_manifest(self) -> Dict[str, Any]:
        """Validate the plugin manifest against the interface spec."""
        required_fields = [
            "plugin_id", "name", "version", "description", "type",
            "interface_version", "auth_method", "auth_config",
            "capabilities", "rate_limits", "required_permissions",
            "governor_approval", "qa_status", "last_audited",
            "configuration_schema"
        ]

        manifest = self.get_manifest()

        for field in required_fields:
            if field not in manifest or manifest[field] is None:
                return {"valid": False, "error": f"Missing required field: {field}"}

        if self.interface_version != "vjsos-ai-plugin-v1":
            return {"valid": False, "error": "Unsupported interface version"}

        return {"valid": True}


# Export for backwards compatibility
VjsosPlugin = PluginInterface