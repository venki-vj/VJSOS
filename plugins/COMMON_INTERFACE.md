# VJSOS-AI Plugin System

## Common Interface Specification

**Interface Version:** `vjsos-ai-plugin-v1`
**Status:** Active
**Governed by:** System Governor + Infrastructure Director

---

## 1. Plugin Manifest (`manifest.json`)

Every plugin must provide a `manifest.json` at its root:

```json
{
  "plugin_id": "github@v1.2.0",
  "name": "GitHub Integration",
  "version": "1.2.0",
  "type": "api_integration",
  "description": "GitHub API integration for repository management, CI/CD, and analytics",
  "author": "Infrastructure Department",
  "license": "MIT",
  "interface_version": "vjsos-ai-plugin-v1",
  "auth_method": "oauth",
  "auth_config": {
    "oauth_scopes": ["repo", "admin:repo_hook", "read:org"],
    "token_refresh_endpoint": "https://github.com/login/oauth/access_token"
  },
  "capabilities": [
    "read_repositories",
    "create_issues",
    "manage_pull_requests",
    "trigger_workflows",
    "read_analytics",
    "manage_releases",
    "read_audit_log"
  ],
  "rate_limits": {
    "calls_per_minute": 5000,
    "calls_per_hour": 50000,
    "per_ip": true,
    "per_token": true
  },
  "required_permissions": [
    "admin:repo_hook",
    "repo"
  ],
  "events_subscribed": [
    "task.created",
    "task.completed",
    "deployment.requested"
  ],
  "events_published": [
    "github.workflow.triggered",
    "github.pr.created",
    "github.issue.created"
  ],
  "endpoints": [
    {
      "path": "/repos",
      "method": "GET",
      "description": "List repositories"
    },
    {
      "path": "/repos/{owner}/{repo}/issues",
      "method": "POST",
      "description": "Create issue"
    }
  ],
  "governor_approval": true,
  "qa_status": "verified",
  "last_audited": "2026-08-05",
  "dependencies": [],
  "configuration_schema": {
    "type": "object",
    "properties": {
      "organization": {"type": "string"},
      "default_repo": {"type": "string"},
      "webhook_secret": {"type": "string", "format": "secret"}
    },
    "required": ["organization"]
  }
}
```

---

## 2. Required Interface Methods

Plugins must implement these handlers:

### `on_init(config: dict) -> dict`
Called once on plugin load. Returns initialization status.

```python
async def on_init(self, config: dict) -> dict:
    """Initialize plugin with validated configuration."""
    self.client = GitHubClient(config["organization"], config["token"])
    await self.client.verify_auth()
    return {"status": "initialized", "version": self.manifest["version"]}
```

### `on_event(event_type: str, payload: dict) -> dict`
Handle system events the plugin subscribed to.

```python
async def on_event(self, event_type: str, payload: dict) -> dict:
    """React to system events."""
    if event_type == "deployment.requested":
        return await self.trigger_deployment_workflow(payload)
    return {"status": "ignored"}
```

### `on_schedule(cron: str) -> dict`
Handle scheduled recurring tasks.

```python
async def on_schedule(self, cron: str) -> dict:
    """Run scheduled tasks (e.g., sync analytics)."""
    if cron == "0 * * * *":  # hourly
        return await self.sync_repository_metrics()
    return {"status": "no_matching_schedule"}
```

### `on_request(endpoint: str, params: dict) -> dict`
Handle internal API requests from agents/orchestrator.

```python
async def on_request(self, endpoint: str, params: dict) -> dict:
    """Expose plugin capabilities to agents."""
    if endpoint == "repos.list":
        return await self.client.list_repos(params)
    elif endpoint == "issues.create":
        return await self.client.create_issue(params)
    raise NotImplementedError(f"Endpoint {endpoint} not implemented")
```

### `on_stream(source: str) -> AsyncIterator[dict]`
Consume external data streams.

```python
async def on_stream(self, source: str) -> AsyncIterator[dict]:
    """Stream events from external source."""
    if source == "github.webhooks":
        async for event in self.client.webhook_stream():
            yield self._normalize_event(event)
```

### `on_shutdown() -> dict`
Cleanup on plugin unload.

```python
async def on_shutdown(self) -> dict:
    """Graceful shutdown."""
    await self.client.close()
    return {"status": "shutdown_complete"}
```

---

## 3. Plugin SDK Base Class

```python
# plugins/sdk/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any, AsyncIterator
import asyncio

class PluginBase(ABC):
    """Base class for all VJSOS-AI plugins."""
    
    def __init__(self, manifest: dict):
        self.manifest = manifest
        self.config = {}
        self._running = False
    
    @abstractmethod
    async def on_init(self, config: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def on_event(self, event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    async def on_schedule(self, cron: str) -> Dict[str, Any]:
        return {"status": "no_schedule_handler"}
    
    @abstractmethod
    async def on_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    async def on_stream(self, source: str) -> AsyncIterator[Dict[str, Any]]:
        return
        yield  # makes it an async generator
    
    async def on_shutdown(self) -> Dict[str, Any]:
        return {"status": "shutdown"}
    
    async def run(self):
        """Main plugin loop."""
        self._running = True
        while self._running:
            await asyncio.sleep(1)
    
    def stop(self):
        self._running = False
```

---

## 4. Authentication Methods

### OAuth 2.0
```json
{
  "auth_method": "oauth",
  "auth_config": {
    "authorization_url": "https://github.com/login/oauth/authorize",
    "token_url": "https://github.com/login/oauth/access_token",
    "scopes": ["repo", "admin:repo_hook"],
    "refresh_token": true
  }
}
```

### API Key
```json
{
  "auth_method": "api_key",
  "auth_config": {
    "header_name": "Authorization",
    "header_prefix": "Bearer ",
    "key_rotation_days": 90
  }
}
```

### SSH
```json
{
  "auth_method": "ssh",
  "auth_config": {
    "private_key_path": "/vault/ssh/plugin_key",
    "known_hosts_path": "/vault/ssh/known_hosts",
    "passphrase": "vault:plugin_ssh_passphrase"
  }
}
```

---

## 5. Rate Limiting

Plugins declare rate limits in manifest. Plugin Manager enforces:

```python
# Applied per plugin instance
class RateLimiter:
    def __init__(self, calls_per_minute: int, calls_per_hour: int):
        self.minute_bucket = TokenBucket(calls_per_minute, 60)
        self.hour_bucket = TokenBucket(calls_per_hour, 3600)
    
    async def acquire(self) -> bool:
        return await self.minute_bucket.take() and await self.hour_bucket.take()
```

---

## 6. Plugin Lifecycle

```
INSTALLED
    │
    ▼
GOVERNOR_REVIEW  ←── Governor validates manifest, security, constitution compliance
    │
    ▼
QA_VERIFICATION  ←── QA tests plugin against rubric (security, reliability, interface)
    │
    ▼
APPROVED
    │
    ▼
ACTIVE  ←── Plugin Manager loads, runs on_init, registers event handlers
    │
    ├── on_event()  ←── System events
    ├── on_schedule()  ←── Cron triggers
    ├── on_request()  ←── Agent requests
    └── on_stream()  ←── External streams
    │
    ▼
SUPERSEDED/DEPRECATED  ←── New version or removal
    │
    ▼
SHUTDOWN  ←── on_shutdown(), cleanup
```

---

## 7. Security Requirements

1. **No credentials in code** — All secrets via Vault
2. **Governor approval required** — `governor_approval: true` in manifest
3. **Audit trail** — All plugin actions logged to `logs/audit.log`
4. **Isolation** — Plugins run in sandboxed processes
5. **Rate limits enforced** — Cannot exceed declared limits
6. **Capability scoping** — Plugins only access declared capabilities

---

## 8. Example Plugin Structure

```
plugins/github/
├── manifest.json
├── src/
│   ├── __init__.py
│   ├── plugin.py           # Implements PluginBase
│   ├── client.py           # GitHub API client
│   ├── models.py           # Data models
│   └── handlers/
│       ├── events.py       # on_event handlers
│       ├── requests.py     # on_request handlers
│       └── streams.py      # on_stream handlers
├── tests/
│   ├── test_plugin.py
│   ├── test_client.py
│   └── fixtures/
├── requirements.txt
└── README.md
```

---

## 9. Plugin Registry

Located at `plugins/registry/index.json`:

```json
{
  "plugins": {
    "github@v1.2.0": {
      "path": "github/",
      "status": "active",
      "installed_at": "2026-08-05T10:00:00Z",
      "approved_by": "governor@vjsos-ai",
      "qa_verified": true
    },
    "obsidian@v1.0.0": {
      "path": "obsidian/",
      "status": "active",
      "installed_at": "2026-08-05T10:00:00Z"
    },
    "youtube@v1.1.0": {
      "path": "youtube/",
      "status": "pending_review",
      "installed_at": "2026-08-06T14:00:00Z"
    }
  }
}
```

---

## 10. CLI Commands

```bash
# Install plugin
python -m plugins.manager install plugins/github/

# Governor review
python -m plugins.manager review --plugin github@v1.2.0

# Enable/disable
python -m plugins.manager enable github@v1.2.0
python -m plugins.manager disable github@v1.2.0

# List plugins
python -m plugins.manager list

# Test plugin
python -m plugins.manager test github@v1.2.0

# View logs
python -m plugins.manager logs github@v1.2.0
```

---

## 11. Governance

- **Infrastructure Director** owns plugin system
- **System Governor** approves all plugins
- **QA Infrastructure** verifies before activation
- **Security audit** required for new auth methods
- **Deprecation policy** — 6 months notice, migration path required

---

**End of Plugin Interface Specification**

*See `plugins/registry/` for available plugins. All changes require Governor approval.*