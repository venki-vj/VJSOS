"""
Plugin SDK - Utility Classes

Provides common utilities used across plugins:
- SDKLogger: Structured logging for plugins
- SDKError: Error hierarchy for SDK operations
- SDKConfig: Configuration management for plugins
"""

import logging
import json
import time
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path
from enum import Enum


class SDKError(Exception):
    """Base exception for SDK errors."""

    def __init__(self, message: str, error_code: str = "UNKNOWN", details: Dict[str, Any] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error": self.message,
            "error_code": self.error_code,
            "details": self.details
        }


class SDKValidationError(SDKError):
    """Raised when validation fails."""

    def __init__(self, message: str, details: Dict[str, Any] = None):
        super().__init__(message, error_code="VALIDATION_ERROR", details=details)


class SDKAuthError(SDKError):
    """Raised when authentication fails."""

    def __init__(self, message: str, details: Dict[str, Any] = None):
        super().__init__(message, error_code="AUTH_ERROR", details=details)


class SDKRateLimitError(SDKError):
    """Raised when rate limit is exceeded."""

    def __init__(self, message: str, retry_after: float = None, details: Dict[str, Any] = None):
        super().__init__(message, error_code="RATE_LIMIT_ERROR", details=details)
        self.retry_after = retry_after


class SDKTimeoutError(SDKError):
    """Raised when an operation times out."""

    def __init__(self, message: str, timeout: float = None, details: Dict[str, Any] = None):
        super().__init__(message, error_code="TIMEOUT_ERROR", details=details)
        self.timeout = timeout


class SDKErrorCodes:
    """Standard error codes."""
    UNKNOWN = "UNKNOWN"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    AUTH_ERROR = "AUTH_ERROR"
    RATE_LIMIT_ERROR = "RATE_LIMIT_ERROR"
    TIMEOUT_ERROR = "TIMEOUT_ERROR"
    CONNECTION_ERROR = "CONNECTION_ERROR"
    PLUGIN_ERROR = "PLUGIN_ERROR"
    CONFIG_ERROR = "CONFIG_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"


class SDKLogLevel(Enum):
    """Log levels for SDK logger."""
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class SDKLogger:
    """Structured logger for plugins."""

    def __init__(self, plugin_id: str, level: SDKLogLevel = SDKLogLevel.INFO):
        self.plugin_id = plugin_id
        self.level = level
        self.logs: List[Dict[str, Any]] = []

        # Set up Python logging
        self.logger = logging.getLogger(f"vjsos.plugin.{plugin_id}")
        self.logger.setLevel(level.value)

        # Add handler if not already present
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                f'%(asctime)s [{plugin_id}] [%(levelname)s] %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def _log(self, level: SDKLogLevel, message: str, context: Dict[str, Any] = None):
        """Internal log method."""
        if level.value < self.level.value:
            return

        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "plugin_id": self.plugin_id,
            "level": level.name,
            "message": message,
            "context": context or {}
        }
        self.logs.append(log_entry)

        # Log to Python logger
        if level == SDKLogLevel.DEBUG:
            self.logger.debug(json.dumps(context or {}))
        elif level == SDKLogLevel.INFO:
            self.logger.info(message)
        elif level == SDKLogLevel.WARNING:
            self.logger.warning(message)
        elif level == SDKLogLevel.ERROR:
            self.logger.error(message)
        elif level == SDKLogLevel.CRITICAL:
            self.logger.critical(message)

    def debug(self, message: str, context: Dict[str, Any] = None):
        self._log(SDKLogLevel.DEBUG, message, context)

    def info(self, message: str, context: Dict[str, Any] = None):
        self._log(SDKLogLevel.INFO, message, context)

    def warning(self, message: str, context: Dict[str, Any] = None):
        self._log(SDKLogLevel.WARNING, message, context)

    def error(self, message: str, context: Dict[str, Any] = None):
        self._log(SDKLogLevel.ERROR, message, context)

    def critical(self, message: str, context: Dict[str, Any] = None):
        self._log(SDKLogLevel.CRITICAL, message, context)

    def get_logs(self, level: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get logs, optionally filtered by level."""
        if level:
            logs = [log for log in self.logs if log["level"].lower() == level.lower()]
        else:
            logs = self.logs

        return logs[-limit:]

    def save_logs(self, path: str):
        """Save logs to file."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w") as f:
            for log in self.logs:
                f.write(json.dumps(log) + "\n")


class SDKConfig:
    """Configuration manager for plugins."""

    def __init__(self, plugin_id: str, config: Dict[str, Any] = None):
        self.plugin_id = plugin_id
        self._config = config or {}
        self._config_path = Path(f"plugins/{plugin_id}/config.json")
        self._load_persistent_config()

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        keys = key.split(".")
        value = self._config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    def set(self, key: str, value: Any, persistent: bool = False):
        """Set a configuration value."""
        keys = key.split(".")
        config = self._config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value

        if persistent:
            self._save_persistent_config()

    def merge(self, config: Dict[str, Any], overwrite: bool = True):
        """Merge a configuration dict."""
        self._deep_merge(self._config, config, overwrite)

    def to_dict(self) -> Dict[str, Any]:
        """Get full configuration as dict."""
        return dict(self._config)

    def _load_persistent_config(self):
        """Load persistent config from disk."""
        if self._config_path.exists():
            try:
                with open(self._config_path, "r") as f:
                    self._config.update(json.load(f))
            except (json.JSONDecodeError, IOError):
                pass

    def _save_persistent_config(self):
        """Save persistent config to disk."""
        self._config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self._config_path, "w") as f:
            json.dump(self._config, f, indent=2)

    def _deep_merge(self, base: Dict[str, Any], override: Dict[str, Any], overwrite: bool):
        """Deep merge two config dicts."""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value, overwrite)
            elif overwrite or key not in base:
                base[key] = value


class SDKTimer:
    """Timer utility for measuring execution time."""

    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.lap_times: List[float] = []

    def start(self):
        """Start the timer."""
        self.start_time = time.time()
        return self

    def stop(self) -> float:
        """Stop the timer and return elapsed time."""
        if self.start_time is None:
            raise SDKError("Timer not started")
        self.end_time = time.time()
        elapsed = self.end_time - self.start_time
        self.lap_times.append(elapsed)
        return elapsed

    def lap(self) -> float:
        """Record a lap time."""
        if self.start_time is None:
            raise SDKError("Timer not started")
        elapsed = time.time() - self.start_time
        self.lap_times.append(elapsed)
        return elapsed

    def reset(self):
        """Reset the timer."""
        self.start_time = None
        self.end_time = None
        self.lap_times.clear()


class SDKMetrics:
    """Metrics collector for plugins."""

    def __init__(self, plugin_id: str):
        self.plugin_id = plugin_id
        self.metrics: Dict[str, List[float]] = {}
        self.counters: Dict[str, int] = {}

    def gauge(self, name: str, value: float):
        """Record a gauge value."""
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append(value)

    def counter(self, name: str, value: int = 1):
        """Increment a counter."""
        self.counters[name] = self.counters.get(name, 0) + value

    def timer(self, name: str, duration: float):
        """Record a timing."""
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append(duration)

    def get_stats(self) -> Dict[str, Any]:
        """Get metrics statistics."""
        stats = {}
        for name, values in self.metrics.items():
            if values:
                stats[name] = {
                    "count": len(values),
                    "min": min(values),
                    "max": max(values),
                    "avg": sum(values) / len(values),
                    "latest": values[-1]
                }
        stats.update({f"counter_{k}": v for k, v in self.counters.items()})
        return stats