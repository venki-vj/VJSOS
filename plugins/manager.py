#!/usr/bin/env python3
"""
Plugin Manager - External Tool Integration

Manages plugin lifecycle:
- Manifest validation
- Authentication method handling
- Rate limit enforcement
- Governor approval workflow
- QA verification

Plugin Interface: vjsos-ai-plugin-v1
"""

import json
import time
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, AsyncIterator
from dataclasses import dataclass, field, fields
from enum import Enum
import aiohttp
import hashlib
import hmac


class PluginStatus(Enum):
    INSTALLED = "installed"
    PENDING_GOVERNOR_REVIEW = "pending_governor_review"
    PENDING_QA = "pending_qa"
    APPROVED = "approved"
    ACTIVE = "active"
    INACTIVE = "inactive"
    REJECTED = "rejected"
    DEPRECATED = "deprecated"


class AuthMethod(Enum):
    OAUTH = "oauth"
    API_KEY = "api_key"
    SSH = "ssh"
    VAULT = "vault"
    TOKEN = "token"


@dataclass
class PluginManifest:
    """Plugin manifest - matches plugins/COMMON_INTERFACE.md spec."""
    plugin_id: str
    name: str
    version: str
    description: str
    type: str
    interface_version: str
    auth_method: str
    auth_config: Dict[str, Any]
    capabilities: List[str]
    rate_limits: Dict[str, Any]
    required_permissions: List[str]
    governor_approval: bool
    qa_status: str
    last_audited: str
    configuration_schema: Dict[str, Any]
    author: Optional[str] = None
    license: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    events_subscribed: List[str] = field(default_factory=list)
    events_published: List[str] = field(default_factory=list)
    endpoints: List[Dict[str, str]] = field(default_factory=list)
    config: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PluginManifest":
        """Create PluginManifest from dict."""
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class RateLimit:
    """Rate limiter state for a plugin."""
    calls_per_minute: int
    calls_per_hour: int
    minute_bucket: int = 0
    hour_bucket: int = 0
    last_minute_reset: float = field(default_factory=time.time)
    last_hour_reset: float = field(default_factory=time.time)


class PluginManager:
    """Manages plugin lifecycle and integration."""

    def __init__(self, plugins_root: str = "plugins", governor=None):
        self.manager_id = "plugin-manager@vjsos-ai"
        self.plugins_root = Path(plugins_root)
        self.plugins_root.mkdir(parents=True, exist_ok=True)

        self.registry_path = self.plugins_root / "registry" / "index.json"
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)

        self.governor = governor
        self.plugins: Dict[str, PluginEntry] = {}  # plugin_id@version -> entry
        self.rate_limiters: Dict[str, RateLimit] = {}

        self._load_registry()

    def _load_registry(self):
        """Load plugin registry from disk."""
        if self.registry_path.exists():
            with open(self.registry_path, 'r') as f:
                data = json.load(f)
            # Only pass fields that PluginEntry understands; the registry may
            # carry extra metadata (name, type, auth_method, capabilities,
            # description, ...) that belongs in the manifest, not the entry.
            known_fields = {f.name for f in fields(PluginEntry)}
            for plugin_id, entry_data in data.get("plugins", {}).items():
                # The registry key IS the plugin_id; the entry dict carries the
                # rest (name, path, status, auth_method, capabilities, ...).
                filtered = {k: v for k, v in entry_data.items() if k in known_fields}
                filtered.setdefault("plugin_id", plugin_id)
                self.plugins[plugin_id] = PluginEntry(**filtered)

    def _save_registry(self):
        """Save plugin registry to disk."""
        registry_data = {
            "version": "1.0.0",
            "updated_at": datetime.utcnow().isoformat() + "Z",
            "plugins": {
                plugin_id: {
                    "plugin_id": entry.plugin_id,
                    "name": entry.name,
                    "path": str(entry.path),
                    "status": entry.status.value if isinstance(entry.status, PluginStatus) else entry.status,
                    "manifest": entry.manifest or {},
                    "installed_at": entry.installed_at,
                    "approved_by": entry.approved_by,
                    "last_used": entry.last_used,
                    "config": entry.config
                }
                for plugin_id, entry in self.plugins.items()
            }
        }
        with open(self.registry_path, 'w') as f:
            json.dump(registry_data, f, indent=2)

    def install_plugin(self, plugin_path: str, skip_governor: bool = False) -> Dict[str, Any]:
        """Install a plugin package."""
        path = Path(plugin_path)
        if not path.exists():
            return {"success": False, "error": f"Plugin path not found: {plugin_path}"}

        # Find manifest.json
        manifest_path = path / "manifest.json"
        if not manifest_path.exists():
            return {"success": False, "error": "manifest.json not found in plugin directory"}

        # Parse and validate manifest
        try:
            manifest_data = json.loads(manifest_path.read_text())
        except json.JSONDecodeError as e:
            return {"success": False, "error": f"Invalid manifest.json: {e}"}

        # Validate manifest
        validation = self._validate_manifest(manifest_data)
        if not validation["valid"]:
            return {"success": False, "error": validation["error"]}

        manifest = PluginManifest.from_dict(manifest_data)

        # Governor approval required
        if manifest.governor_approval and not skip_governor:
            # Submit to Governor for review
            if self.governor:
                decision_id = self.governor.make_decision(
                    type_="PLUGIN_APPROVAL",
                    title=f"Plugin approval: {manifest.plugin_id}",
                    rationale=manifest.description,
                    impact={"plugin_id": manifest.plugin_id, "capabilities": manifest.capabilities},
                    proposed_by="plugin_manager"
                )
                status = PluginStatus.PENDING_GOVERNOR_REVIEW
            else:
                return {"success": False, "error": "Governor approval required but no governor configured"}
        else:
            status = PluginStatus.PENDING_QA

        # Create plugin entry
        plugin_key = f"{manifest.plugin_id}@{manifest.version}"
        entry = PluginEntry(
            plugin_id=plugin_key,
            path=path,
            manifest=manifest,
            status=status.value,
            installed_at=datetime.utcnow().isoformat() + "Z"
        )

        self.plugins[plugin_key] = entry
        self._save_registry()

        return {
            "success": True,
            "plugin_key": plugin_key,
            "status": status.value,
            "message": f"Plugin {plugin_key} installed. Awaiting {'Governor review' if manifest.governor_approval else 'QA verification'}"
        }

    def activate_plugin(self, plugin_key: str) -> Dict[str, Any]:
        """Activate an approved plugin."""
        entry = self.plugins.get(plugin_key)
        if not entry:
            return {"success": False, "error": "Plugin not found"}

        if entry.status != PluginStatus.APPROVED.value:
            return {"success": False, "error": f"Plugin not approved (status: {entry.status})"}

        entry.status = PluginStatus.ACTIVE.value
        entry.last_used = datetime.utcnow().isoformat() + "Z"
        self._save_registry()

        # Initialize auth
        auth_result = self._initialize_auth(entry)
        if not auth_result["success"]:
            return {"success": False, "error": f"Auth failed: {auth_result['error']}"}

        # Initialize rate limiter
        self._initialize_rate_limiter(entry)

        return {"success": True, "message": f"Plugin {plugin_key} activated"}

    async def execute(self, plugin_key: str, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a plugin endpoint with rate limiting."""
        entry = self.plugins.get(plugin_key)
        if not entry or entry.status != PluginStatus.ACTIVE.value:
            return {"success": False, "error": "Plugin not active"}

        # Rate limit check
        rl_result = self._check_rate_limit(plugin_key, entry)
        if not rl_result["allowed"]:
            return {"success": False, "error": f"Rate limit exceeded: {rl_result['reason']}"}

        # In real implementation, this would call the plugin's handler
        return {
            "success": True,
            "plugin": plugin_key,
            "endpoint": endpoint,
            "result": {"message": "Plugin call successful (simulated)"}
        }

    async def stream_events(self, plugin_key: str) -> AsyncIterator[Dict[str, Any]]:
        """Stream events from a plugin (if supported)."""
        entry = self.plugins.get(plugin_key)
        if not entry or entry.status != PluginStatus.ACTIVE.value:
            return

        # In real implementation, this would connect to plugin's event stream
        while True:
            yield {"event": "heartbeat", "timestamp": datetime.utcnow().isoformat() + "Z"}
            await asyncio.sleep(1)

    def handle_event(self, plugin_key: str, event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle a system event for a plugin."""
        entry = self.plugins.get(plugin_key)
        if not entry or entry.status != PluginStatus.ACTIVE.value:
            return {"success": False, "error": "Plugin not active"}

        if event_type not in entry.manifest.events_subscribed:
            return {"success": False, "error": f"Event {event_type} not subscribed"}

        # In real implementation, this would call plugin.on_event
        return {"success": True, "event": event_type, "processed": True}

    def list_plugins(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all plugins with optional status filter."""
        results = []
        for key, entry in self.plugins.items():
            if status and entry.status != status:
                continue
            manifest = entry.manifest
            name = manifest.name if manifest else (entry.name or entry.plugin_id)
            version = manifest.version if manifest else "1.0.0"
            ptype = manifest.type if manifest else "api_integration"
            caps = manifest.capabilities if manifest else []
            auth = manifest.auth_method if manifest else "unknown"
            desc = manifest.description if manifest else ""
            results.append({
                "plugin_key": entry.plugin_id,
                "plugin_id": entry.plugin_id,
                "name": name,
                "version": version,
                "type": ptype,
                "status": entry.status,
                "capabilities": caps,
                "auth_method": auth,
                "last_used": entry.last_used,
                "installed_at": entry.installed_at,
                "manifest": {
                    "name": name,
                    "version": version,
                    "description": desc,
                    "capabilities": caps,
                    "auth_method": auth,
                }
            })
        return results

    def get_audit_log(self, plugin_key: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get audit log for plugins."""
        audit_path = self.plugins_root / "audit_log.json"
        if not audit_path.exists():
            return []

        with open(audit_path, 'r') as f:
            logs = json.load(f)

        if plugin_key:
            logs = [log for log in logs if log.get("plugin_id") == plugin_key]

        return logs

    def _validate_manifest(self, manifest_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate plugin manifest against specification."""
        required_fields = [
            "plugin_id", "name", "version", "type", "interface_version",
            "auth_method", "auth_config", "capabilities", "rate_limits",
            "required_permissions", "governor_approval", "qa_status",
            "last_audited", "configuration_schema"
        ]

        for field_name in required_fields:
            if field_name not in manifest_data:
                return {"valid": False, "error": f"Missing required field: {field_name}"}

        # Validate interface version
        if manifest_data["interface_version"] != "vjsos-ai-plugin-v1":
            return {"valid": False, "error": "Unsupported interface version"}

        # Validate auth method
        try:
            AuthMethod(manifest_data["auth_method"])
        except ValueError:
            return {"valid": False, "error": f"Invalid auth_method: {manifest_data['auth_method']}"}

        # Validate version format
        parts = manifest_data["version"].split(".")
        if len(parts) != 3:
            return {"valid": False, "error": "Version must be semantic (MAJOR.MINOR.PATCH)"}

        # Validate rate limits
        rate_limits = manifest_data.get("rate_limits", {})
        if not isinstance(rate_limits, dict):
            return {"valid": False, "error": "rate_limits must be an object"}

        if "calls_per_minute" not in rate_limits and "calls_per_hour" not in rate_limits:
            return {"valid": False, "error": "rate_limits must include calls_per_minute or calls_per_hour"}

        return {"valid": True}

    def _initialize_auth(self, entry: "PluginEntry") -> Dict[str, Any]:
        """Initialize authentication for a plugin."""
        auth_method = entry.manifest.auth_method
        config = entry.manifest.auth_config

        if auth_method == AuthMethod.OAUTH.value:
            # OAuth flow handled by Vault
            return {"success": True, "method": "oauth", "vault_path": config.get("token_url", "vault:/plugins/oauth")}
        elif auth_method == AuthMethod.API_KEY.value:
            return {"success": True, "method": "api_key", "vault_path": "vault:/plugins/api_keys"}
        elif auth_method == AuthMethod.SSH.value:
            return {"success": True, "method": "ssh", "key_path": config.get("private_key_path", "~/.ssh/plugin_key")}
        elif auth_method == AuthMethod.VAULT.value:
            return {"success": True, "method": "vault"}
        else:
            return {"success": False, "error": f"Unsupported auth method: {auth_method}"}

    def _initialize_rate_limiter(self, entry: "PluginEntry"):
        """Initialize rate limiter for a plugin."""
        rate_limits = entry.manifest.rate_limits
        self.rate_limiters[entry.plugin_id] = RateLimit(
            calls_per_minute=rate_limits.get("calls_per_minute", 1000),
            calls_per_hour=rate_limits.get("calls_per_hour", 100000)
        )

    def _check_rate_limit(self, plugin_key: str, entry: "PluginEntry") -> Dict[str, Any]:
        """Check and update rate limits."""
        limiter = self.rate_limiters.get(plugin_key)
        if not limiter:
            return {"allowed": True}  # No rate limiting

        now = time.time()

        # Reset minute bucket if needed
        if now - limiter.last_minute_reset >= 60:
            limiter.minute_bucket = 0
            limiter.last_minute_reset = now

        # Reset hour bucket if needed
        if now - limiter.last_hour_reset >= 3600:
            limiter.hour_bucket = 0
            limiter.last_hour_reset = now

        # Check limits
        if limiter.minute_bucket >= limiter.calls_per_minute:
            return {"allowed": False, "reason": "Rate limit exceeded for minute"}
        if limiter.hour_bucket >= limiter.calls_per_hour:
            return {"allowed": False, "reason": "Rate limit exceeded for hour"}

        # Increment counters
        limiter.minute_bucket += 1
        limiter.hour_bucket += 1

        return {"allowed": True}

    def _log_audit_event(self, event: Dict[str, Any]):
        """Log audit event."""
        Path(self.plugins_root).mkdir(parents=True, exist_ok=True)
        audit_path = self.plugins_root / "audit_log.json"

        logs = []
        if audit_path.exists():
            with open(audit_path, 'r') as f:
                logs = json.load(f)

        logs.append(event)

        with open(audit_path, 'w') as f:
            json.dump(logs, f, indent=2)


@dataclass
class PluginEntry:
    """A plugin entry in the registry.

    The registry doubles as both an availability listing (plugins/registry/
    index.json) and an installation record. Fields that only make sense once
    a plugin is installed (manifest, installed_at) are therefore optional so a
    bare listing entry can be loaded without them.
    """
    plugin_id: str
    path: Any  # pathlib.Path
    manifest: Optional[Dict[str, Any]] = None
    status: str = "available"
    installed_at: Optional[str] = None
    name: str = ""
    approved_by: Optional[str] = None
    last_used: Optional[str] = None
    config: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        # Handle Path serialization
        if isinstance(self.path, str):
            self.path = Path(self.path)


def main():
    """Test the Plugin Manager."""
    manager = PluginManager()

    # List existing plugins
    print("Installed plugins:", manager.list_plugins())

    # Create test plugin manifest
    test_plugin_path = Path("plugins/test_plugin")
    test_plugin_path.mkdir(parents=True, exist_ok=True)

    manifest = {
        "plugin_id": "test@v1.0.0",
        "name": "Test Plugin",
        "version": "1.0.0",
        "description": "Test plugin for validation",
        "type": "api_integration",
        "interface_version": "vjsos-ai-plugin-v1",
        "auth_method": "api_key",
        "auth_config": {"header_name": "Authorization", "header_prefix": "Bearer "},
        "capabilities": ["read_test", "write_test"],
        "rate_limits": {"calls_per_minute": 60, "calls_per_hour": 1000},
        "required_permissions": ["test:read"],
        "governor_approval": False,
        "qa_status": "verified",
        "last_audited": "2026-08-07",
        "configuration_schema": {"type": "object", "properties": {"endpoint": {"type": "string"}}}
    }

    (test_plugin_path / "manifest.json").write_text(json.dumps(manifest, indent=2))

    # Install
    result = manager.install_plugin(str(test_plugin_path))
    print(f"Install: {result}")

    # List again
    print(f"Plugins: {manager.list_plugins()}")

    print("Plugin Manager test completed!")


if __name__ == "__main__":
    main()