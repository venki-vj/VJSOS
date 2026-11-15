#!/usr/bin/env python3
"""
Event Types - Standard Event Definitions for the Message Bus

Defines the canonical set of event/message types used across the
VJSOS-AI message bus. All kernel components and departments should
use these standard types rather than inventing ad-hoc ones.

Re-exported from `kernel/event_bus.py` for backwards compatibility:
    from kernel.event_types import MessageType, SYSTEM_EVENTS
"""

from enum import Enum


class MessageType(Enum):
    """Standard message types for the VJSOS message bus."""
    # Task lifecycle
    TASK_REQUEST = "task_request"
    TASK_RESULT = "task_result"
    TASK_UPDATE = "task_update"
    TASK_CANCEL = "task_cancel"

    # QA feedback
    QA_FEEDBACK = "qa_feedback"
    QA_APPROVE = "qa_approve"
    QA_REJECT = "qa_reject"
    QA_APPEAL = "qa_appeal"

    # Department messages
    DEPARTMENT_ANNOUNCEMENT = "department_announcement"
    DEPARTMENT_REQUEST = "department_request"

    # Governance
    GOVERNOR_DECISION = "governor_decision"
    GOVERNOR_APPROVAL = "governor_approval"
    GOVERNOR_APPEAL = "governor_appeal"

    # System
    SYSTEM_EVENT = "system_event"
    HEARTBEAT = "heartbeat"
    STATUS_UPDATE = "status_update"

    # Plugins & Skills
    PLUGIN_EVENT = "plugin_event"
    PLUGIN_INSTALLED = "plugin_installed"
    PLUGIN_ACTIVATED = "plugin_activated"
    PLUGIN_DEACTIVATED = "plugin_deactivated"
    SKILL_REGISTERED = "skill_registered"
    SKILL_UPDATED = "skill_updated"
    SKILL_EXECUTED = "skill_executed"

    # Analytics
    METRICS = "metrics"
    ALERT = "alert"
    DASHBOARD = "dashboard"

    # Learning
    LEARNING = "learning"
    INSIGHT = "insight"
    PROPOSAL = "proposal"

    # Errors and appeals
    ERROR = "error"
    APPEAL = "appeal"

    # Lifecycle
    LIFECYCLE = "lifecycle"
    SHUTDOWN = "shutdown"
    STARTUP = "startup"


class SystemEvents:
    """Constant reference for system-level events.

    Provides a stable, importable set of system event names used for
    audit logging and system lifecycle management.
    """
    STARTUP = "startup"
    SHUTDOWN = "shutdown"
    HEARTBEAT = "heartbeat"
    CONFIG_RELOAD = "config_reload"
    GOVERNOR_OVERRIDE = "governor_override"
    CONSTITUTION_UPDATE = "constitution_update"


class SkillEvents:
    """Constant reference for skill-related events."""
    SKILL_REGISTERED = "skill_registered"
    SKILL_UPDATED = "skill_updated"
    SKILL_EXECUTED = "skill_executed"
    SKILL_TESTED = "skill_tested"
    SKILL_DEPRECATED = "skill_deprecated"


class PluginEvents:
    """Constant reference for plugin lifecycle events."""
    PLUGIN_INSTALLED = "plugin_installed"
    PLUGIN_ACTIVATED = "plugin_activated"
    PLUGIN_DEACTIVATED = "plugin_deactivated"
    PLUGIN_UNINSTALLED = "plugin_uninstalled"
    PLUGIN_ERROR = "plugin_error"


class AnalyticsEvents:
    """Constant reference for analytics and alerting events."""
    METRIC_RECORDED = "metric_recorded"
    ALERT_TRIGGERED = "alert_triggered"
    ALERT_RESOLVED = "alert_resolved"
    REPORT_GENERATED = "report_generated"
    DASHBOARD_REFRESHED = "dashboard_refreshed"


class LearningEvents:
    """Constant reference for learning events."""
    PATTERN_DETECTED = "pattern_detected"
    IMPROVEMENT_SUGGESTED = "improvement_suggested"
    PROPOSAL_CREATED = "proposal_created"
    PROPOSAL_APPROVED = "proposal_approved"
    KNOWLEDGE_UPDATED = "knowledge_updated"


class QAEvents:
    """Constant reference for QA events."""
    QA_FEEDBACK = "qa_feedback"
    QA_APPROVE = "qa_approve"
    QA_REJECT = "qa_reject"
    QA_APPEAL = "qa_appeal"


def get_event_category(message_type: MessageType) -> str:
    """Classify a message type into a broad category.

    Useful for dashboard grouping and audit logging.
    """
    category_map = {
        # Task lifecycle
        MessageType.TASK_REQUEST: "task",
        MessageType.TASK_RESULT: "task",
        MessageType.TASK_UPDATE: "task",
        # QA
        MessageType.QA_FEEDBACK: "qa",
        MessageType.QA_APPROVE: "qa",
        MessageType.QA_REJECT: "qa",
        MessageType.QA_APPEAL: "qa",
        # System
        MessageType.SYSTEM_EVENT: "system",
        MessageType.HEARTBEAT: "system",
        MessageType.STATUS_UPDATE: "system",
        MessageType.STARTUP: "system",
        MessageType.SHUTDOWN: "system",
        # Governance
        MessageType.GOVERNOR_DECISION: "governance",
        MessageType.GOVERNOR_APPROVAL: "governance",
        MessageType.GOVERNOR_APPEAL: "governance",
        # Plugin/Skill
        MessageType.PLUGIN_EVENT: "plugin",
        MessageType.PLUGIN_INSTALLED: "plugin",
        MessageType.PLUGIN_ACTIVATED: "plugin",
        MessageType.SKILL_REGISTERED: "skill",
        MessageType.SKILL_UPDATED: "skill",
        MessageType.SKILL_EXECUTED: "skill",
        # Analytics
        MessageType.METRICS: "analytics",
        MessageType.ALERT: "analytics",
        MessageType.DASHBOARD: "analytics",
        # Learning
        MessageType.LEARNING: "learning",
        MessageType.INSIGHT: "learning",
        MessageType.PROPOSAL: "learning",
        # Error / appeal
        MessageType.ERROR: "system",
        MessageType.APPEAL: "governance",
        # Lifecycle
        MessageType.LIFECYCLE: "system",
        # Department
        MessageType.DEPARTMENT_ANNOUNCEMENT: "department",
        MessageType.DEPARTMENT_REQUEST: "department",
    }
    return category_map.get(message_type, "custom")
