"""
Plugin SDK - Validation Tools

Provides manifest validation and schema validation for plugins.
Ensures plugin compliance with the VJSOS-AI interface specification.
"""

import json
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path
from enum import Enum


class ValidationSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ValidationError:
    """Represents a validation error."""

    def __init__(self, field: str, message: str, severity: ValidationSeverity = ValidationSeverity.ERROR):
        self.field = field
        self.message = message
        self.severity = severity

    def to_dict(self) -> Dict[str, Any]:
        return {
            "field": self.field,
            "message": self.message,
            "severity": self.severity.value
        }

    def __repr__(self):
        return f"ValidationError({self.field}: {self.message} [{self.severity.value}])"


class ManifestValidator:
    """Validates plugin manifests against the VJSOS-AI plugin interface specification."""

    INTERFACE_VERSION = "vjsos-ai-plugin-v1"

    REQUIRED_FIELDS = [
        "plugin_id", "name", "version", "description", "type",
        "interface_version", "auth_method", "auth_config",
        "capabilities", "rate_limits", "required_permissions",
        "governor_approval", "qa_status", "last_audited",
        "configuration_schema"
    ]

    VALID_AUTH_METHODS = ["oauth", "api_key", "ssh", "vault", "token"]
    VALID_PLUGIN_TYPES = ["api_integration", "data_provider", "action_executor",
                          "analytics_provider", "notification_handler",
                          "scheduler", "connector", "extension"]

    def __init__(self, strict: bool = True):
        self.strict = strict
        self.errors: List[ValidationError] = []
        self.warnings: List[ValidationError] = []

    def validate(self, manifest_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a plugin manifest."""
        self.errors = []
        self.warnings = []

        # Check required fields
        for field in self.REQUIRED_FIELDS:
            if field not in manifest_data:
                self.errors.append(ValidationError(field, f"Required field '{field}' is missing"))

        if self.errors:
            return self._build_result(False)

        # Validate interface version
        interface_version = manifest_data.get("interface_version", "")
        if interface_version != self.INTERFACE_VERSION:
            self.errors.append(ValidationError(
                "interface_version",
                f"Expected '{self.INTERFACE_VERSION}', got '{interface_version}'"
            ))

        # Validate version format (semver)
        version = manifest_data.get("version", "")
        if not self._validate_semver(version):
            self.errors.append(ValidationError(
                "version",
                f"Version '{version}' is not a valid semantic version (MAJOR.MINOR.PATCH)"
            ))

        # Validate auth method
        auth_method = manifest_data.get("auth_method", "")
        if auth_method not in self.VALID_AUTH_METHODS:
            self.errors.append(ValidationError(
                "auth_method",
                f"Invalid auth method '{auth_method}'. Valid options: {self.VALID_AUTH_METHODS}"
            ))

        # Validate plugin type
        plugin_type = manifest_data.get("type", "")
        if plugin_type not in self.VALID_PLUGIN_TYPES:
            self.warnings.append(ValidationError(
                "type",
                f"Unknown plugin type '{plugin_type}'",
                severity=ValidationSeverity.WARNING
            ))

        # Validate rate limits
        self._validate_rate_limits(manifest_data.get("rate_limits", {}))

        # Validate capabilities
        self._validate_capabilities(manifest_data.get("capabilities", []))

        # Validate configuration schema
        self._validate_config_schema(manifest_data.get("configuration_schema", {}))

        # Validate events
        self._validate_events(manifest_data)

        return self._build_result(len(self.errors) == 0)

    def _validate_semver(self, version: str) -> bool:
        """Validate semantic version format."""
        parts = version.split(".")
        if len(parts) != 3:
            return False
        return all(part.isdigit() for part in parts)

    def _validate_rate_limits(self, rate_limits: Dict[str, Any]):
        """Validate rate limits configuration."""
        if not rate_limits:
            self.errors.append(ValidationError("rate_limits", "Rate limits must be specified"))
            return

        if not isinstance(rate_limits, dict):
            self.errors.append(ValidationError("rate_limits", "Rate limits must be an object"))
            return

        required_limits = ["calls_per_minute", "calls_per_hour"]
        has_required = any(limit in rate_limits for limit in required_limits)
        if not has_required:
            self.errors.append(ValidationError(
                "rate_limits",
                f"Rate limits must include at least one of: {required_limits}"
            ))

        for limit_name, value in rate_limits.items():
            if not isinstance(value, int) or value <= 0:
                self.errors.append(ValidationError(
                    f"rate_limits.{limit_name}",
                    f"Rate limit '{limit_name}' must be a positive integer, got {value}"
                ))

    def _validate_capabilities(self, capabilities: List[str]):
        """Validate capabilities list."""
        if not capabilities:
            self.warnings.append(ValidationError(
                "capabilities",
                "No capabilities declared - plugin may not be functional",
                severity=ValidationSeverity.WARNING
            ))
            return

        if not isinstance(capabilities, list):
            self.errors.append(ValidationError("capabilities", "Capabilities must be a list"))
            return

        valid_capabilities = [
            "read", "write", "execute", "stream", "auth", "webhook",
            "file_io", "network", "database", "ai_model", "code_execution"
        ]

        for cap in capabilities:
            if cap not in valid_capabilities:
                self.warnings.append(ValidationError(
                    f"capabilities.{cap}",
                    f"Unknown capability '{cap}'",
                    severity=ValidationSeverity.WARNING
                ))

    def _validate_config_schema(self, schema: Dict[str, Any]):
        """Validate configuration schema (basic JSON Schema check)."""
        if not schema:
            self.warnings.append(ValidationError(
                "configuration_schema",
                "No configuration schema provided",
                severity=ValidationSeverity.WARNING
            ))
            return

        if not isinstance(schema, dict):
            self.errors.append(ValidationError("configuration_schema", "Configuration schema must be an object"))
            return

        # Basic JSON Schema validation
        type_value = schema.get("type", "")
        if type_value and type_value != "object":
            self.warnings.append(ValidationError(
                "configuration_schema.type",
                f"Configuration schema type should be 'object', got '{type_value}'",
                severity=ValidationSeverity.WARNING
            ))

    def _validate_events(self, manifest_data: Dict[str, Any]):
        """Validate event subscription/publishing lists."""
        for event_type in ["events_subscribed", "events_published"]:
            events = manifest_data.get(event_type, [])
            if not isinstance(events, list):
                self.errors.append(ValidationError(event_type, f"{event_type} must be a list"))

    def _build_result(self, valid: bool) -> Dict[str, Any]:
        """Build validation result."""
        return {
            "valid": valid,
            "errors": [e.to_dict() for e in self.errors],
            "warnings": [e.to_dict() for e in self.warnings],
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "interface_version": self.INTERFACE_VERSION,
            "strict_mode": self.strict
        }


class SchemaValidator:
    """Validates arbitrary data against JSON schemas."""

    def __init__(self):
        self.validated_count = 0
        self.validation_errors = []

    def validate(self, data: Any, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data against a JSON schema."""
        errors = []
        valid = True

        # Basic type checking
        expected_type = schema.get("type")
        if expected_type:
            type_map = {
                "string": str,
                "number": (int, float),
                "integer": int,
                "boolean": bool,
                "array": list,
                "object": dict
            }

            expected_python_type = type_map.get(expected_type)
            if expected_python_type and not isinstance(data, expected_python_type):
                valid = False
                errors.append({
                    "field": schema.get("field", "root"),
                    "message": f"Expected type '{expected_type}', got '{type(data).__name__}'"
                })

        # Check required properties for objects
        if isinstance(data, dict) and expected_type == "object":
            required = schema.get("required", [])
            for req in required:
                if req not in data:
                    valid = False
                    errors.append({
                        "field": req,
                        "message": f"Required property '{req}' is missing"
                    })

            # Validate properties
            properties = schema.get("properties", {})
            for prop_name, prop_schema in properties.items():
                if prop_name in data:
                    prop_result = self.validate(data[prop_name], prop_schema)
                    if not prop_result["valid"]:
                        valid = False
                        for err in prop_result["errors"]:
                            err["field"] = f"{prop_name}.{err['field']}"
                            errors.append(err)

        # Check items for arrays
        if isinstance(data, list) and expected_type == "array":
            items_schema = schema.get("items", {})
            if items_schema:
                for i, item in enumerate(data):
                    item_result = self.validate(item, items_schema)
                    if not item_result["valid"]:
                        valid = False

        # Check string constraints
        if isinstance(data, str) and expected_type == "string":
            min_length = schema.get("minLength")
            max_length = schema.get("maxLength")
            pattern = schema.get("pattern")

            if min_length and len(data) < min_length:
                valid = False
                errors.append({
                    "field": schema.get("field", "root"),
                    "message": f"String must be at least {min_length} characters"
                })

            if max_length and len(data) > max_length:
                valid = False
                errors.append({
                    "field": schema.get("field", "root"),
                    "message": f"String must be at most {max_length} characters"
                })

            if pattern:
                import re
                if not re.match(pattern, data):
                    valid = False
                    errors.append({
                        "field": schema.get("field", "root"),
                        "message": f"String does not match pattern '{pattern}'"
                    })

        # Check numeric constraints
        if isinstance(data, (int, float)) and expected_type in ("number", "integer"):
            minimum = schema.get("minimum")
            maximum = schema.get("maximum")

            if minimum is not None and data < minimum:
                valid = False
                errors.append({
                    "field": schema.get("field", "root"),
                    "message": f"Value must be >= {minimum}"
                })

            if maximum is not None and data > maximum:
                valid = False
                errors.append({
                    "field": schema.get("field", "root"),
                    "message": f"Value must be <= {maximum}"
                })

        self.validated_count += 1

        return {
            "valid": valid,
            "errors": errors
        }

    def get_validation_stats(self) -> Dict[str, Any]:
        """Get validation statistics."""
        return {
            "total_validated": self.validated_count,
            "total_errors": len(self.validation_errors)
        }


class Validator:
    """Convenience class for comprehensive plugin validation."""

    @staticmethod
    def validate_plugin(plugin_path: str, strict: bool = True) -> Dict[str, Any]:
        """Validate a plugin package from its directory path."""
        path = Path(plugin_path)
        errors = []

        # Check directory exists
        if not path.exists() or not path.is_dir():
            return {"valid": False, "errors": [{"field": "plugin_path", "message": f"Plugin path not found: {plugin_path}"}]}

        # Load manifest
        manifest_path = path / "manifest.json"
        if not manifest_path.exists():
            return {"valid": False, "errors": [{"field": "manifest", "message": "manifest.json not found"}]}

        try:
            manifest_data = json.loads(manifest_path.read_text())
        except json.JSONDecodeError as e:
            return {"valid": False, "errors": [{"field": "manifest", "message": f"Invalid JSON: {e}"}]}

        # Validate manifest
        validator = ManifestValidator(strict=strict)
        manifest_result = validator.validate(manifest_data)

        errors.extend(manifest_result["errors"])

        return {
            "valid": len(errors) == 0,
            "manifest_valid": manifest_result["valid"],
            "errors": errors,
            "warnings": manifest_result["warnings"],
            "manifest": manifest_data
        }