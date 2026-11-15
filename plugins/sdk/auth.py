"""
Plugin SDK - Authentication Handlers

Provides authentication mechanisms for plugin integration:
- OAuth 2.0 flow
- API Key authentication
- Token-based authentication
- Vault integration

All auth handlers follow the same interface and can be
mixed and matched based on the plugin's requirements.
"""

import abc
import time
import hashlib
import hmac
from typing import Dict, Any, Optional
from pathlib import Path
from urllib.parse import urlencode


class AuthHandler(abc.ABC):
    """Abstract base class for authentication handlers."""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.credentials = None
        self.authenticated = False
        self.token_expiry = None

    @abc.abstractmethod
    async def authenticate(self) -> Dict[str, Any]:
        """Authenticate with the service."""
        raise NotImplementedError

    @abc.abstractmethod
    async def refresh(self) -> Dict[str, Any]:
        """Refresh authentication credentials."""
        raise NotImplementedError

    @abc.abstractmethod
    async def revoke(self) -> Dict[str, Any]:
        """Revoke authentication credentials."""
        raise NotImplementedError

    def is_valid(self) -> bool:
        """Check if current credentials are still valid."""
        if not self.credentials or not self.authenticated:
            return False

        if self.token_expiry:
            return time.time() < self.token_expiry

        return True


class OAuthAuthHandler(AuthHandler):
    """OAuth 2.0 authentication handler."""

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.client_id = config.get("client_id", "")
        self.token_url = config.get("token_url", "")
        self.auth_url = config.get("auth_url", "")
        self.redirect_uri = config.get("redirect_uri", "urn:ietf:wg:oauth:2.0:oob")
        self.scopes = config.get("scopes", ["read"])
        self.access_token = None
        self.refresh_token = None

    async def authenticate(self) -> Dict[str, Any]:
        """Perform OAuth authentication flow."""
        # In a real implementation, this would:
        # 1. Redirect user to auth_url
        # 2. Handle auth callback
        # 3. Exchange auth code for tokens
        # 4. Store tokens securely via Vault

        auth_params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": " ".join(self.scopes)
        }
        auth_url = f"{self.auth_url}?{urlencode(auth_params)}"

        # Simulate token getting (placeholder)
        self.access_token = "test_access_token"
        self.refresh_token = "test_refresh_token"
        self.authenticated = True
        self.token_expiry = time.time() + 3600  # 1 hour

        self._store_credentials({
            "access_token": self.access_token,
            "refresh_token": self.refresh_token
        })

        return {
            "success": True,
            "method": "oauth",
            "auth_url": auth_url,
            "token_expiry": self.token_expiry
        }

    async def refresh(self) -> Dict[str, Any]:
        """Refresh access token."""
        if not self.refresh_token:
            return {"success": False, "error": "No refresh token available"}

        # In a real implementation, this would call token_url
        self.access_token = "refreshed_access_token"
        self.token_expiry = time.time() + 3600
        self.authenticated = True

        return {"success": True, "token_expiry": self.token_expiry}

    async def revoke(self) -> Dict[str, Any]:
        """Revoke tokens."""
        self.access_token = None
        self.refresh_token = None
        self.authenticated = False
        self.token_expiry = None
        return {"success": True, "message": "Tokens revoked"}

    def _store_credentials(self):
        """Store credentials securely via Vault."""
        # In a real implementation, this would store in Vault
        pass

    def get_headers(self) -> Dict[str, str]:
        """Get authentication headers for API calls."""
        if not self.access_token:
            return {}
        return {"Authorization": f"Bearer {self.access_token}"}


class ApiKeyAuthHandler(AuthHandler):
    """API Key authentication handler."""

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.api_key = config.get("api_key", "")
        self.header_name = config.get("header_name", "X-API-Key")
        self.header_prefix = config.get("header_prefix", "")
        self.vault_path = config.get("vault_path", "vault:/plugins/api_keys")

    async def authenticate(self) -> Dict[str, Any]:
        """Use API key for authentication."""
        if not self.api_key:
            # In a real implementation, this would retrieve from Vault
            self.api_key = "retrieved_from_vault"

        self.credentials = {"api_key": self.api_key}
        self.authenticated = True

        return {"success": True, "method": "api_key"}

    async def refresh(self) -> Dict[str, Any]:
        """Refresh API key (no-op, just re-authenticate)."""
        return await self.authenticate()

    async def revoke(self) -> Dict[str, Any]:
        """Revoke API key."""
        self.api_key = ""
        self.authenticated = False
        return {"success": True}

    def get_headers(self) -> Dict[str, str]:
        """Build API key headers for requests."""
        header_value = f"{self.header_prefix} {self.api_key}".strip() if self.header_prefix else self.api_key
        return {self.header_name: header_value}


class VaultAuthHandler(AuthHandler):
    """HashiCorp Vault-based auth handler."""

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.vault_url = config.get("vault_url", "")
        self.role_id = config.get("role_id", "")
        self.secret_id = config.get("secret_id", "")
        self.vault_path = config.get("vault_path", "")

    async def authenticate(self) -> Dict[str, Any]:
        """Authenticate via Vault."""
        # In a real implementation, this would:
        # - Request a Vault token using role_id/secret_id
        # - Use the token to retrieve plugin secrets
        self.credentials = {"vault_token": "test_vault_token"}
        self.authenticated = True
        return {"success": True, "method": "vault"}

    async def refresh(self) -> Dict[str, Any]:
        """Refresh Vault token."""
        return await self.authenticate()

    async def revoke(self) -> Dict[str, Any]:
        """Revoke Vault token."""
        self.authenticated = False
        return {"success": True}


class SSHKeyAuthHandler(AuthHandler):
    """SSH key-based auth handler."""

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.private_key_path = config.get("private_key_path", "~/.ssh/plugin_key")
        self.public_key_path = config.get("public_key_path", "~/.ssh/plugin_key.pub")
        self.key_passphrase = config.get("key_passphrase", "")

    async def authenticate(self) -> Dict[str, Any]:
        """Authenticate via SSH key."""
        key_path = Path(self.private_key_path).expanduser()
        if not key_path.exists():
            return {"success": False, "error": f"SSH key not found: {key_path}"}

        # In a real implementation, this would load the key and connect
        self.authenticated = True
        return {"success": True, "method": "ssh", "key_path": str(key_path)}

    async def refresh(self) -> Dict[str, Any]:
        """Refresh SSH authentication."""
        return await self.authenticate()

    async def revoke(self) -> Dict[str, Any]:
        """Revoke SSH authentication."""
        self.authenticated = False
        return {"success": True}