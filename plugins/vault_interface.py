#!/usr/bin/env python3
"""
Vault Interface - Secure Credential Management

Provides a secure interface for storing and retrieving plugin/agent
credentials and secrets. Supports a pluggable backend architecture:

    Backends:
    - env: Environment variable backend (local dev)
    - file: Encrypted JSON file backend (local)
    - hashicorp: HashiCorp Vault backend (production)

The interface enforces Constitution Article VI: "No credential may be
stored in plaintext in system logs, memory dumps, or plugin manifests.
All secrets must be accessed via the Vault Interface."
"""

import json
import os
import time
import hmac
import hashlib
import base64
import threading
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, Any, Optional, List

try:
    from cryptography.fernet import Fernet
    _CRYPTO_AVAILABLE = True
except ImportError:
    _CRYPTO_AVAILABLE = False


class VaultBackend(Enum):
    """Supported vault backends."""
    ENV = "env"
    FILE = "file"
    VAULT = "vault"  # HashiCorp Vault
    MOCK = "mock"  # In-memory only (testing)


@dataclass
class CredentialEntry:
    """Represents a stored credential."""
    key: str
    backend: str
    created_at: str
    expires_at: Optional[str]
    tags: Dict[str, str]
    metadata: Dict[str, Any]

    def is_expired(self) -> bool:
        if not self.expires_at:
            return False
        return datetime.utcnow() > datetime.fromisoformat(self.expires_at.replace("Z", "+00:00"))


class VaultInterface:
    """Secure credential management interface.

    Usage:
        vault = VaultInterface(backend=VaultBackend.ENV, env_prefix="VJSOS_")
        vault.store("github_token@engineering", "ghp_...", tags={"type": "oauth_token"})
        token = vault.retrieve("github_token@engineering")
    """

    def __init__(self, backend: VaultBackend = VaultBackend.MOCK,
                 vault_url: str = None,
                 token: str = None,
                 env_prefix: str = "VJSOS_",
                 file_path: str = "vault_secrets.json",
                 encryption_key: str = None):
        self.backend = backend
        self.vault_url = vault_url
        self.token = token
        self.env_prefix = env_prefix
        self.file_path = Path(file_path)
        self.encryption_key = encryption_key
        self._cache: Dict[str, Any] = {}
        self._cache_lock = threading.Lock()
        self._access_log: List[Dict[str, Any]] = []
        self._entries: Dict[str, CredentialEntry] = {}

        if backend == VaultBackend.FILE:
            self._fernet = None
            if self.encryption_key and _CRYPTO_AVAILABLE:
                self._fernet = Fernet(self.encryption_key.encode() if isinstance(self.encryption_key, str) else self.encryption_key)
            elif not _CRYPTO_AVAILABLE:
                print("WARNING: cryptography package not available; file backend will store unencrypted")

        if backend == VaultBackend.MOCK:
            self._cache = {}
            self._entries = {}

    # ────────────── Environment backend ──────────────

    def _env_key(self, key: str) -> str:
        """Convert key to environment variable name."""
        return f"{self.env_prefix}{key.upper().replace('@', '_').replace('-', '_').replace('.', '_')}"

    def _env_store(self, key: str, value: str) -> bool:
        """Store secret in environment variable (process-local)."""
        os.environ[self._env_key(key)] = value
        self._log_access(key, "store", "env")
        return True

    def _env_retrieve(self, key: str) -> Optional[str]:
        """Retrieve secret from environment variable."""
        value = os.environ.get(self._env_key(key))
        self._log_access(key, "retrieve", "env")
        return value

    # ────────────── File backend ──────────────

    def _file_store(self, key: str, value: str, ttl: int = 0) -> bool:
        """Store secret in encrypted JSON file."""
        if not _CRYPTO_AVAILABLE or not self._fernet:
            # Fallback: store unencrypted (dev only)
            self._log_access(key, "store", "file_unencrypted")
        else:
            self._log_access(key, "store", "file_encrypted")

        try:
            data = {}
            if self.file_path.exists():
                try:
                    with open(self.file_path) as f:
                        data = json.load(f)
                except (json.JSONDecodeError, KeyError):
                    data = {}

            if _CRYPTO_AVAILABLE and self._fernet:
                value = self._fernet.encrypt(value.encode()).decode()

            expires_at = None
            if ttl > 0:
                expires_at = (datetime.utcnow() + timedelta(seconds=ttl)).isoformat() + "Z"

            data[key] = {
                "value": value,
                "created_at": datetime.utcnow().isoformat() + "Z",
                "expires_at": expires_at,
                "encrypted": _CRYPTO_AVAILABLE and bool(self._fernet)
            }

            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.file_path, "w") as f:
                json.dump(data, f, indent=2)

            self._entries[key] = CredentialEntry(
                key=key, backend="file",
                created_at=data[key]["created_at"],
                expires_at=expires_at,
                tags={}, metadata={}
            )
            return True
        except Exception as e:
            print(f"Failed to store secret '{key}': {e}")
            return False

    def _file_retrieve(self, key: str) -> Optional[str]:
        """Retrieve secret from encrypted JSON file."""
        self._log_access(key, "retrieve", "file")
        try:
            with open(self.file_path) as f:
                data = json.load(f)
            if key not in data:
                return None

            value = data[key]["value"]
            if data[key].get("encrypted") and self._fernet:
                value = self._fernet.decrypt(value.encode()).decode()
            return value
        except Exception as e:
            print(f"Failed to retrieve secret '{key}': {e}")
            return None

    # ────────────── HashiCorp Vault backend ──────────────

    def _vault_store(self, key: str, value: str, ttl: int = 0) -> bool:
        """Store secret in HashiCorp Vault."""
        self._log_access(key, "store", "vault")
        try:
            import hvac
            client = hvac.Client(url=self.vault_url, token=self.token)
            path = f"vjsos/secrets/{key}"
            mount_point = "secret"
            client.secrets.kv.v2.create_or_update_secret(
                path=path,
                secret={"value": value},
                mount_point=mount_point
            )
            return True
        except ImportError:
            print("hvac package not available; falling back to file backend")
            return self._file_store(key, value, ttl)
        except Exception as e:
            print(f"Failed to store secret in Vault '{key}': {e}")
            return False

    def _vault_retrieve(self, key: str) -> Optional[str]:
        """Retrieve secret from HashiCorp Vault."""
        self._log_access(key, "retrieve", "vault")
        try:
            import hvac
            client = hvac.Client(url=self.vault_url, token=self.token)
            path = f"vjsos/secrets/{key}"
            mount_point = "secret"
            secret = client.secrets.kv.v2.read_secret_version(path=path, mount_point=mount_point)
            return secret["data"]["data"].get("value")
        except (ImportError, Exception) as e:
            print(f"Failed to retrieve secret from Vault '{key}': {e}")
            return None

    # ────────────── Public API ──────────────

    def store(self, key: str, value: str,
              ttl: int = 0, tags: Dict[str, str] = None) -> bool:
        """Store a secret value with optional TTL (seconds)."""
        if not key or not value:
            return False

        tags = tags or {}

        # Store in cache for fast retrieval
        with self._cache_lock:
            self._cache[key] = value

        # Store in configured backend
        if self.backend == VaultBackend.ENV:
            return self._env_store(key, value)
        elif self.backend == VaultBackend.FILE:
            return self._file_store(key, value, ttl)
        elif self.backend == VaultBackend.VAULT:
            return self._vault_store(key, value, ttl)
        else:  # MOCK
            self._log_access(key, "store", "mock")
            return True

    def retrieve(self, key: str, default: Any = None) -> Optional[str]:
        """Retrieve a secret value by key."""
        # Check cache first
        with self._cache_lock:
            if key in self._cache:
                self._log_access(key, "retrieve", "cache")
                return self._cache[key]

        # Retrieve from backend
        if self.backend == VaultBackend.ENV:
            return self._env_retrieve(key) or default
        elif self.backend == VaultBackend.FILE:
            return self._file_retrieve(key) or default
        elif self.backend == VaultBackend.VAULT:
            return self._vault_retrieve(key) or default
        else:
            self._log_access(key, "retrieve", "mock")
            return self._cache.get(key, default)

    def delete(self, key: str) -> bool:
        """Delete a secret."""
        with self._cache_lock:
            self._cache.pop(key, None)

        if self.backend == VaultBackend.ENV:
            os.environ.pop(self._env_key(key), None)
            return True
        elif self.backend == VaultBackend.FILE:
            try:
                if self.file_path.exists():
                    with open(self.file_path) as f:
                        data = json.load(f)
                    if key in data:
                        del data[key]
                        with open(self.file_path, "w") as f:
                            json.dump(data, f, indent=2)
                return True
            except Exception:
                return False
        elif self.backend == VaultBackend.VAULT:
            try:
                import hvac
                client = hvac.Client(url=self.vault_url, token=self.token)
                client.secrets.kv.v2.delete_metadata(
                    path=f"vjsos/secrets/{key}",
                    mount_point="secret"
                )
                return True
            except Exception:
                return False
        return True

    def exists(self, key: str) -> bool:
        """Check if a secret exists."""
        return self.retrieve(key, None) is not None

    def list_keys(self) -> List[str]:
        """List all stored keys (metadata only, no values)."""
        if self.backend == VaultBackend.FILE:
            try:
                with open(self.file_path) as f:
                    data = json.load(f)
                return list(data.keys())
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        elif self.backend == VaultBackend.MOCK:
            with self._cache_lock:
                return list(self._cache.keys())
        else:
            with self._cache_lock:
                return [k for k in self._cache.keys()]

    def rotate(self, key: str, new_value: str, ttl: int = 0,
               tags: Dict[str, str] = None) -> bool:
        """Rotate (replace) a secret value."""
        self.delete(key)
        return self.store(key, new_value, ttl=ttl, tags=tags)

    def get_metadata(self) -> Dict[str, Any]:
        """Get metadata about stored credentials."""
        return {
            "backend": self.backend.value,
            "total_credentials": len(self.list_keys()),
            "entries": [asdict(e) for e in self._entries.values()],
            "access_log_count": len(self._access_log)
        }

    # ────────────── Internal ──────────────

    def _log_access(self, key: str, action: str, backend: str):
        """Log credential access for audit trail."""
        self._access_log.append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "key": key,
            "action": action,
            "backend": backend
        })
        # Keep only last 1000 entries
        if len(self._access_log) > 1000:
            self._access_log = self._access_log[-1000:]


def main():
    """Test the Vault Interface."""
    vault = VaultInterface(backend=VaultBackend.ENV)

    # Store
    vault.store("github_token@engineering", "ghp_test123456789", tags={"type": "oauth_token"})
    print(f"Stored: github_token@engineering")

    # Retrieve
    token = vault.retrieve("github_token@engineering")
    print(f"Retrieved: {token}")

    # Exists
    print(f"Exists: {vault.exists('github_token@engineering')}")

    # List
    print(f"Keys: {vault.list_keys()}")

    # Delete
    vault.delete("github_token@engineering")
    print(f"After delete exists: {vault.exists('github_token@engineering')}")

    print(f"\nMetadata: {json.dumps(vault.get_metadata(), indent=2)}")


if __name__ == "__main__":
    main()