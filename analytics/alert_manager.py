#!/usr/bin/env python3
"""
Alert Manager - Threshold-Based Alerting

Monitors metrics and triggers alerts when thresholds are breached.
- Configurable alert rules per metric
- Severity levels (info, warning, critical, emergency)
- Alert deduplication and suppression
- Notification routing to departments/governor
"""

import json
import time
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field, asdict
from enum import Enum
from collections import defaultdict, deque


class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class AlertStatus(Enum):
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
    SUPPRESSED = "suppressed"


@dataclass
class AlertRule:
    """Alert trigger rule."""
    rule_id: str
    metric_name: str
    comparison: str  # >, >=, <, <=, ==, !=
    threshold: float
    severity: AlertSeverity
    message: str
    enabled: bool = True
    tags: Dict[str, str] = field(default_factory=dict)
    conditions: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AlertNotification:
    """Notification for a triggered alert."""
    alert_id: str
    rule_id: str
    metric_name: str
    metric_value: float
    threshold: float
    severity: AlertSeverity
    message: str
    timestamp: str
    tags: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AlertRecord:
    """Persistent alert record."""
    alert_id: str
    rule_id: str
    metric_name: str
    metric_value: float
    threshold: float
    severity: AlertSeverity
    message: str
    timestamp: str
    status: AlertStatus
    resolved_at: Optional[str] = None
    resolved_reason: Optional[str] = None
    tags: Dict[str, str] = field(default_factory=dict)


class AlertManager:
    """Manages alerts and notifications."""

    def __init__(self):
        self.manager_id = "alert-manager@vjsos-ai"
        self.rules: Dict[str, AlertRule] = {}
        self.active_alerts: Dict[str, AlertNotification] = {}  # rule_id -> alert
        self.alert_history: deque = deque(maxlen=10000)
        self.resolved_alerts: List[AlertRecord] = []
        self.suppression_rules: Dict[str, Dict[str, Any]] = {}
        self.acknowledgements: Dict[str, bool] = {}
        self.rate_limiters: Dict[str, float] = {}  # rule_id -> last alert time
        self.alert_channels = {
            "console": self._console_notify,
            "file": self._file_notify,
            "event_bus": self._event_bus_notify
        }
        self.active_notifications = []
        self._alert_cooldown = 60  # Minimum seconds between alerts

    def add_rule(self, rule: AlertRule) -> Dict[str, Any]:
        """Add an alert rule. Accepts an AlertRule or a rule dict."""
        if isinstance(rule, dict):
            rule = AlertRule(**rule)
        self.rules[rule.rule_id] = rule
        return {"success": True, "rule_id": rule.rule_id}

    def remove_rule(self, rule_id: str) -> Dict[str, Any]:
        """Remove an alert rule."""
        if rule_id in self.rules:
            del self.rules[rule_id]
            return {"success": True, "rule_id": rule_id}
        return {"success": False, "error": "Rule not found"}

    def update_rule(self, rule_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update an alert rule."""
        rule = self.rules.get(rule_id)
        if not rule:
            return {"success": False, "error": "Rule not found"}

        for key, value in updates.items():
            if hasattr(rule, key):
                setattr(rule, key, value)

        return {"success": True, "rule_id": rule_id}

    def evaluate_metric(self, metric_name: str, value: float,
                       tags: Optional[Dict[str, str]] = None) -> List[AlertNotification]:
        """Evaluate a metric against all alert rules."""
        triggered = []
        tags = tags or {}

        for rule_id, rule in self.rules.items():
            if not rule.enabled:
                continue

            # Check if rule applies to this metric
            if rule.metric_name != metric_name:
                continue

            # Check if rule applies to tags
            if rule.tags and not all(tags.get(k) == v for k, v in rule.tags.items()):
                continue

            # Check comparison
            if self._evaluate_comparison(rule.comparison, value, rule.threshold):
                # Check cooldown
                if self._is_in_cooldown(rule_id):
                    continue

                # Create alert notification
                alert = AlertNotification(
                    alert_id=f"alert_{int(time.time())}_{rule_id}",
                    rule_id=rule_id,
                    metric_name=metric_name,
                    metric_value=value,
                    threshold=rule.threshold,
                    severity=rule.severity,
                    message=rule.message,
                    timestamp=datetime.utcnow().isoformat() + "Z",
                    tags=tags or {},
                    metadata=rule.conditions
                )

                # Check if alert already active
                existing = self.active_alerts.get(rule_id)
                if existing and existing.metric_value == value:
                    continue

                self.active_alerts[rule_id] = alert
                self.alert_history.append(asdict(alert))
                self.rate_limiters[rule_id] = time.time()

                # Send notifications
                self._send_notification(alert)

                triggered.append(alert)

        return triggered

    def _evaluate_comparison(self, operator: str, value: float, threshold: float) -> bool:
        """Evaluate a comparison operator."""
        if operator == ">":
            return value > threshold
        elif operator == ">=":
            return value >= threshold
        elif operator == "<":
            return value < threshold
        elif operator == "<=":
            return value <= threshold
        elif operator == "==":
            return value == threshold
        elif operator == "!=":
            return value != threshold
        return False

    def _is_in_cooldown(self, rule_id: str) -> bool:
        """Check if a rule is in cooldown period."""
        last_alert = self.rate_limiters.get(rule_id, 0)
        return (time.time() - last_alert) < self._alert_cooldown

    def _send_notification(self, alert: AlertNotification):
        """Send alert notification to configured channels."""
        for channel_name, channel_fn in self.alert_channels.items():
            try:
                channel_fn(alert)
            except Exception as e:
                print(f"Alert channel {channel_name} failed: {e}")

    def _console_notify(self, alert: AlertNotification):
        """Send alert to console."""
        print(f"[{alert.severity.value.upper()}] {alert.message} (metric: {alert.metric_name} = {alert.metric_value} vs threshold {alert.threshold})")

    def _file_notify(self, alert: AlertNotification):
        """Write alert to file."""
        log_path = Path("logs/alerts.log")
        log_path.parent.mkdir(parents=True, exist_ok=True)

        with open(log_path, "a") as f:
            f.write(json.dumps(asdict(alert)) + "\n")

    def _event_bus_notify(self, alert: AlertNotification):
        """Publish alert to event bus."""
        # In a real implementation, this would publish via the message bus
        pass

    def acknowledge_alert(self, alert_id: str, acknowledged_by: str) -> Dict[str, Any]:
        """Acknowledge an active alert."""
        found = None
        for rule_id, alert in self.active_alerts.items():
            if alert.alert_id == alert_id:
                found = alert
                del self.active_alerts[rule_id]
                self.acknowledgements[alert_id] = True
                break

        if not found:
            return {"success": False, "error": "Alert not found or already resolved"}

        record = AlertRecord(
            alert_id=found.alert_id,
            rule_id=found.rule_id,
            metric_name=found.metric_name,
            metric_value=found.metric_value,
            threshold=found.threshold,
            severity=found.severity,
            message=found.message,
            timestamp=found.timestamp,
            status=AlertStatus.ACKNOWLEDGED,
            tags=found.tags,
            resolved_at=datetime.utcnow().isoformat() + "Z",
            resolved_reason=f"Acknowledged by {acknowledged_by}"
        )
        self.alert_history.append(asdict(record))

        return {"success": True, "alert_id": alert_id}

    def resolve_alert(self, alert_id: str, reason: str = "") -> Dict[str, Any]:
        """Resolve an active alert."""
        found = False
        for rule_id, alert in self.active_alerts.items():
            if alert.alert_id == alert_id:
                record = AlertRecord(
                    alert_id=alert.alert_id,
                    rule_id=alert.rule_id,
                    metric_name=alert.metric_name,
                    metric_value=alert.metric_value,
                    threshold=alert.threshold,
                    severity=alert.severity,
                    message=alert.message,
                    timestamp=alert.timestamp,
                    status=AlertStatus.RESOLVED,
                    tags=alert.tags,
                    resolved_at=datetime.utcnow().isoformat() + "Z",
                    resolved_reason=reason
                )
                self.alert_history.append(asdict(record))
                del self.active_alerts[rule_id]
                found = True

        return {"success": found, "alert_id": alert_id if found else ""}

    def resolve_all_for_metric(self, metric_name: str, reason: str = "") -> Dict[str, Any]:
        """Resolve all active alerts for a metric."""
        to_resolve = [
            alert_id for rule_id, alert in self.active_alerts.items()
            if alert.metric_name == metric_name
        ]

        resolved = []
        for alert_id in to_resolve:
            result = self.resolve_alert(alert_id, reason)
            if result["success"]:
                resolved.append(alert_id)

        return {"success": True, "resolved": resolved, "count": len(resolved)}

    def suppress_rule(self, rule_id: str, duration_seconds: int = 300) -> Dict[str, Any]:
        """Suppress a rule for a period of time."""
        self.suppression_rules[rule_id] = {
            "until": time.time() + duration_seconds,
            "duration": duration_seconds
        }
        return {"success": True, "rule_id": rule_id, "suppressed_until": self.suppression_rules[rule_id]["until"]}

    def unsuppress_rule(self, rule_id: str) -> Dict[str, Any]:
        """Remove suppression from a rule."""
        if rule_id in self.suppression_rules:
            del self.suppression_rules[rule_id]
            return {"success": True, "rule_id": rule_id}
        return {"success": False, "error": "Rule not suppressed"}

    def get_active_alerts(self, severity: Optional[AlertSeverity] = None) -> List[Dict[str, Any]]:
        """Get active alerts with optional severity filter."""
        alerts = list(self.active_alerts.values())
        if severity:
            alerts = [a for a in alerts if a.severity == severity]
        return [asdict(a) for a in alerts]

    def get_alert_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get alert history."""
        return [history for history in self.alert_history][-limit:]

    def get_stats(self) -> Dict[str, Any]:
        """Get alert manager statistics."""
        return {
            "total_rules": len(self.rules),
            "enabled_rules": len([r for r in self.rules.values() if r.enabled]),
            "active_alerts": len(self.active_alerts),
            "total_alerts": len(self.alert_history),
            "suppressed_rules": len(self.suppression_rules),
            "alerts_by_severity": {
                severity.value: len([a for a in self.alert_history if a.get("severity") == severity.value])
                for severity in AlertSeverity
            },
            "last_alert_at": self.alert_history[-1].get("timestamp") if self.alert_history else None
        }


def main():
    """Test the Alert Manager."""
    manager = AlertManager()
    print("Testing Alert Manager...")

    # Add some alert rules
    manager.add_rule(AlertRule(
        rule_id="rules.error_rate_high",
        metric_name="error_rate",
        comparison=">",
        threshold=0.10,
        severity=AlertSeverity.WARNING,
        message="Error rate exceeds threshold"
    ))

    manager.add_rule(AlertRule(
        rule_id="rules.response_time_slow",
        metric_name="response_time",
        comparison=">",
        threshold=30.0,
        severity=AlertSeverity.CRITICAL,
        message="Response time exceeds threshold"
    ))

    # Evaluate metrics
    triggered = manager.evaluate_metric("error_rate", 0.15, {"department": "engineering"})
    print(f"Triggered alerts for error_rate: {len(triggered)}")

    triggered = manager.evaluate_metric("response_time", 60.0, {"department": "engineering"})
    print(f"Triggered alerts for response_time: {len(triggered)}")

    # Get stats
    print(f"Stats: {json.dumps(manager.get_stats(), indent=2)}")

    # Get active alerts
    active = manager.get_active_alerts()
    print(f"Active alerts: {json.dumps(active, indent=2)}")

    print("\nAlert Manager test completed!")


if __name__ == "__main__":
    main()