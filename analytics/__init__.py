"""
Analytics Engine - KPI tracking and performance monitoring.

Components:
- engine.py: Core analytics engine with KPI tracking
- metrics_collector.py: Metrics collection and aggregation
- alert_manager.py: Threshold-based alerting system
- dashboard_generator.py: Dashboard generation for departments
- cost_tracker.py: Resource usage and cost tracking

Usage:
    from analytics import AnalyticsEngine, MetricsCollector
    engine = AnalyticsEngine()
    collector = MetricsCollector()
"""

from .engine import AnalyticsEngine
from .metrics_collector import MetricsCollector, MetricPoint, MetricType, AggregationType, AggregationQuery
from .alert_manager import AlertManager, AlertRule, AlertSeverity, AlertStatus
from .dashboard_generator import DashboardGenerator, Dashboard, DashboardType, DashboardWidget
from .cost_tracker import CostTracker, CostEntry, CostModel, ResourceType, CostUnit

__all__ = [
    # Core
    "AnalyticsEngine",

    # Metrics
    "MetricsCollector",
    "MetricPoint",
    "MetricType",
    "AggregationType",
    "AggregationQuery",

    # Alerts
    "AlertManager",
    "AlertRule",
    "AlertSeverity",
    "AlertStatus",

    # Dashboards
    "DashboardGenerator",
    "Dashboard",
    "DashboardType",
    "DashboardWidget",

    # Costs
    "CostTracker",
    "CostEntry",
    "CostModel",
    "ResourceType",
    "CostUnit"
]
