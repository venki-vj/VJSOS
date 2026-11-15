#!/usr/bin/env python3
"""
Dashboard Generator - Per-Department Analytics Dashboards

Generates real-time and historical dashboards for departments and the organization.
- Department performance dashboards
- System health dashboards
- Executive summary dashboards
- Custom dashboard definitions
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field, asdict
from enum import Enum
from collections import defaultdict


class DashboardType(Enum):
    DEPARTMENT = "department"
    SYSTEM = "system"
    EXECUTIVE = "executive"
    AGENT = "agent"
    CUSTOM = "custom"


@dataclass
class DashboardWidget:
    """A single dashboard widget."""
    widget_id: str
    type: str  # metric, chart, table, alert, status
    title: str
    metric_names: List[str]
    time_range: str  # 1h, 24h, 7d, 30d
    visualization: str  # line, bar, gauge, table, text
    config: Dict[str, Any] = field(default_factory=dict)
    refresh_interval: int = 60  # seconds


@dataclass
class Dashboard:
    """Dashboard definition."""
    dashboard_id: str
    name: str
    type: DashboardType
    owner: str  # department_id or "global"
    widgets: List[DashboardWidget]
    layout: Dict[str, Any] = field(default_factory=dict)
    auto_refresh: bool = True
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


class DashboardGenerator:
    """Generates dashboards from metrics data."""

    def __init__(self, metrics_collector=None, alert_manager=None):
        self.generator_id = "dashboard-generator@vjsos-ai"
        self.metrics_collector = metrics_collector
        self.alert_manager = alert_manager
        self.dashboards: Dict[str, Dashboard] = {}
        self.standard_dashboards = self._create_standard_dashboards()
        self.custom_widgets: Dict[str, Dict[str, Any]] = {}

        # Register standard dashboards
        for dash in self.standard_dashboards.values():
            self.dashboards[dash.dashboard_id] = dash

    def _create_standard_dashboards(self) -> Dict[str, Dashboard]:
        """Create standard department and system dashboards."""
        dashboards = {}

        # Department performance dashboard
        dashboards["dept_performance"] = Dashboard(
            dashboard_id="dept_performance",
            name="Department Performance",
            type=DashboardType.DEPARTMENT,
            owner="department",
            widgets=[
                DashboardWidget(
                    widget_id="task_throughput",
                    type="metric",
                    title="Task Throughput",
                    metric_names=["task_completed_count", "task_failed_count"],
                    time_range="1h",
                    visualization="line",
                    config={"unit": "tasks/hour", "colors": {"completed": "green", "failed": "red"}}
                ),
                DashboardWidget(
                    widget_id="avg_response_time",
                    type="metric",
                    title="Average Response Time",
                    metric_names=["task_duration_seconds"],
                    time_range="1h",
                    visualization="gauge",
                    config={"unit": "seconds", "thresholds": [10, 30, 60]}
                ),
                DashboardWidget(
                    widget_id="success_rate",
                    type="metric",
                    title="Success Rate",
                    metric_names=["task_success_rate"],
                    time_range="24h",
                    visualization="gauge",
                    config={"unit": "percent", "target": 95}
                ),
                DashboardWidget(
                    widget_id="agent_utilization",
                    type="metric",
                    title="Agent Utilization",
                    metric_names=["agent_utilization_ratio"],
                    time_range="1h",
                    visualization="bar",
                    config={"unit": "ratio", "max": 1.0}
                ),
                DashboardWidget(
                    widget_id="active_alerts",
                    type="alert",
                    title="Active Alerts",
                    metric_names=["alert_count"],
                    time_range="1h",
                    visualization="table",
                    config={"max_rows": 10, "sort_by": "severity"}
                )
            ]
        )

        # System health dashboard
        dashboards["system_health"] = Dashboard(
            dashboard_id="system_health",
            name="System Health",
            type=DashboardType.SYSTEM,
            owner="global",
            widgets=[
                DashboardWidget(
                    widget_id="cpu_usage",
                    type="metric",
                    title="CPU Usage",
                    metric_names=["system_cpu_usage_gauge"],
                    time_range="1h",
                    visualization="gauge",
                    config={"unit": "percent", "thresholds": [70, 85, 95]}
                ),
                DashboardWidget(
                    widget_id="memory_usage",
                    type="metric",
                    title="Memory Usage",
                    metric_names=["system_memory_usage_gauge"],
                    time_range="1h",
                    visualization="gauge",
                    config={"unit": "percent", "thresholds": [70, 85, 95]}
                ),
                DashboardWidget(
                    widget_id="disk_usage",
                    type="metric",
                    title="Disk Usage",
                    metric_names=["system_disk_usage_gauge"],
                    time_range="24h",
                    visualization="gauge",
                    config={"unit": "percent", "thresholds": [70, 85, 95]}
                ),
                DashboardWidget(
                    widget_id="active_agents",
                    type="metric",
                    title="Active Agents",
                    metric_names=["active_agent_count"],
                    time_range="1h",
                    visualization="number",
                    config={}
                ),
                DashboardWidget(
                    widget_id="error_rate",
                    type="metric",
                    title="System Error Rate",
                    metric_names=["system_error_rate"],
                    time_range="1h",
                    visualization="line",
                    config={"unit": "percent"}
                )
            ]
        )

        # Executive summary dashboard
        dashboards["executive_summary"] = Dashboard(
            dashboard_id="executive_summary",
            name="Executive Summary",
            type=DashboardType.EXECUTIVE,
            owner="global",
            widgets=[
                DashboardWidget(
                    widget_id="total_tasks_today",
                    type="metric",
                    title="Tasks Completed Today",
                    metric_names=["daily_completed_tasks"],
                    time_range="24h",
                    visualization="number",
                    config={}
                ),
                DashboardWidget(
                    widget_id="overall_success_rate",
                    type="metric",
                    title="Overall Success Rate",
                    metric_names=["overall_success_rate"],
                    time_range="7d",
                    visualization="gauge",
                    config={"unit": "percent", "target": 90}
                ),
                DashboardWidget(
                    widget_id="avg_time_to_complete",
                    type="metric",
                    title="Avg Time to Complete",
                    metric_names=["avg_task_duration"],
                    time_range="24h",
                    visualization="number",
                    config={"unit": "seconds"}
                ),
                DashboardWidget(
                    widget_id="cost_per_task",
                    type="metric",
                    title="Cost per Task",
                    metric_names=["cost_per_task"],
                    time_range="30d",
                    visualization="line",
                    config={"unit": "USD"}
                ),
                DashboardWidget(
                    widget_id="department_comparison",
                    type="metric",
                    title="Department Comparison",
                    metric_names=["dept_task_count", "dept_success_rate"],
                    time_range="24h",
                    visualization="table",
                    config={"departments": ["engineering", "media", "business", "research", "animation", "operations", "knowledge", "infrastructure", "improvement"]}
                )
            ]
        )

        # Agent performance dashboard
        dashboards["agent_performance"] = Dashboard(
            dashboard_id="agent_performance",
            name="Agent Performance",
            type=DashboardType.AGENT,
            owner="agent",
            widgets=[
                DashboardWidget(
                    widget_id="agent_task_count",
                    type="metric",
                    title="Tasks Completed",
                    metric_names=["agent_task_count"],
                    time_range="24h",
                    visualization="bar",
                    config={"group_by": "agent_id"}
                ),
                DashboardWidget(
                    widget_id="agent_avg_duration",
                    type="metric",
                    title="Avg Task Duration",
                    metric_names=["agent_avg_duration"],
                    time_range="24h",
                    visualization="bar",
                    config={"group_by": "agent_id", "unit": "seconds"}
                ),
                DashboardWidget(
                    widget_id="agent_success_rate",
                    type="metric",
                    title="Success Rate by Agent",
                    metric_names=["agent_success_rate"],
                    time_range="24h",
                    visualization="table",
                    config={"group_by": "agent_id"}
                ),
                DashboardWidget(
                    widget_id="agent_feedback_cycles",
                    type="metric",
                    title="Avg Feedback Cycles",
                    metric_names=["agent_feedback_cycles"],
                    time_range="24h",
                    visualization="bar",
                    config={"group_by": "agent_id"}
                )
            ]
        )

        return dashboards

    def generate_dashboard(self, dashboard_id: str, time_range: str = "1h") -> Dict[str, Any]:
        """Generate a dashboard with current data."""
        dashboard = self.dashboards.get(dashboard_id)
        if not dashboard:
            return {"error": f"Dashboard not found: {dashboard_id}"}

        widget_data = {}
        for widget in dashboard.widgets:
            widget_data[widget.widget_id] = self._generate_widget_data(widget, time_range)

        return {
            "dashboard_id": dashboard_id,
            "name": dashboard.name,
            "type": dashboard.type.value,
            "owner": dashboard.owner,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "time_range": time_range,
            "widgets": widget_data
        }

    def _generate_widget_data(self, widget: DashboardWidget, time_range: str) -> Dict[str, Any]:
        """Generate data for a single widget."""
        if not self.metrics_collector:
            return {"error": "No metrics collector configured", "widget": widget.widget_id}

        # Convert time_range to datetime range
        end_time = datetime.utcnow()
        start_time = end_time - self._parse_time_range(time_range)

        # Query metrics for this widget
        results = {}
        for metric_name in widget.metric_names:
            query = self._build_query(metric_name, start_time, end_time, widget.visualization)
            try:
                result = self.metrics_collector.query_metrics(query)
                results[metric_name] = result
            except Exception as e:
                results[metric_name] = {"error": str(e)}

        # Format based on visualization type
        return self._format_widget_data(widget, results)

    def _build_query(self, metric_name: str, start_time: datetime, end_time: datetime, visualization: str):
        """Build an aggregation query from the metrics collector."""
        from analytics.metrics_collector import AggregationQuery, AggregationType
        return AggregationQuery(
            metric_names=[metric_name],
            start_time=start_time.isoformat() + "Z",
            end_time=end_time.isoformat() + "Z",
            aggregation_type=AggregationType.AVERAGE if visualization in ["line", "gauge", "number"] else AggregationType.COUNT
        )

    def _format_widget_data(self, widget: DashboardWidget, results: Dict[str, Any]) -> Dict[str, Any]:
        """Format widget data for frontend consumption."""
        formatted = {
            "widget_id": widget.widget_id,
            "title": widget.title,
            "type": widget.visualization,
            "config": widget.config,
            "data": results
        }

        # Special formatting for certain types
        if widget.visualization == "number":
            # Extract single value for number display
            for metric_name, result in results.items():
                if "aggregated_values" in result and result["aggregated_values"]:
                    formatted["value"] = result["aggregated_values"][0].get("value", 0)
                    break

        elif widget.visualization == "gauge":
            # Extract value and thresholds for gauge
            for metric_name, result in results.items():
                if "aggregated_values" in result and result["aggregated_values"]:
                    formatted["value"] = result["aggregated_values"][0].get("value", 0)
                    formatted["thresholds"] = widget.config.get("thresholds", [])
                    break

        elif widget.visualization in ["line", "bar"]:
            # Format time series for charts
            for metric_name, result in results.items():
                if "aggregated_values" in result and result["aggregated_values"]:
                    formatted["series"] = [
                        {"metric": metric_name, "values": result["aggregated_values"]}
                    ]
                    break

        elif widget.visualization == "table":
            # Format for table display
            formatted["rows"] = []
            for metric_name, result in results.items():
                if "aggregated_values" in result and result["aggregated_values"]:
                    for val in result["aggregated_values"]:
                        formatted["rows"].append({
                            "metric": metric_name,
                            "value": val.get("value", 0),
                            "count": val.get("count", 0)
                        })

        return formatted

    def _parse_time_range(self, time_range: str) -> timedelta:
        """Parse time range string to timedelta."""
        ranges = {
            "1m": timedelta(minutes=1),
            "5m": timedelta(minutes=5),
            "15m": timedelta(minutes=15),
            "30m": timedelta(minutes=30),
            "1h": timedelta(hours=1),
            "6h": timedelta(hours=6),
            "12h": timedelta(hours=12),
            "24h": timedelta(hours=24),
            "7d": timedelta(days=7),
            "30d": timedelta(days=30)
        }
        return ranges.get(time_range, timedelta(hours=1))

    def register_dashboard(self, dashboard: Dashboard):
        """Register a custom dashboard."""
        self.dashboards[dashboard.dashboard_id] = dashboard

    def list_dashboards(self, dashboard_type: Optional[DashboardType] = None) -> List[Dict[str, Any]]:
        """List all available dashboards."""
        dashboards = []
        for dash in self.dashboards.values():
            if dashboard_type and dash.type != dashboard_type:
                continue
            dashboards.append({
                "dashboard_id": dash.dashboard_id,
                "name": dash.name,
                "type": dash.type.value,
                "owner": dash.owner,
                "widget_count": len(dash.widgets),
                "auto_refresh": dash.auto_refresh
            })
        return dashboards

    def get_dashboard_config(self, dashboard_id: str) -> Optional[Dict[str, Any]]:
        """Get dashboard configuration without data."""
        dashboard = self.dashboards.get(dashboard_id)
        if not dashboard:
            return None

        return {
            "dashboard_id": dashboard.dashboard_id,
            "name": dashboard.name,
            "type": dashboard.type.value,
            "owner": dashboard.owner,
            "widgets": [
                {
                    "widget_id": w.widget_id,
                    "type": w.type,
                    "title": w.title,
                    "metric_names": w.metric_names,
                    "time_range": w.time_range,
                    "visualization": w.visualization,
                    "config": w.config
                }
                for w in dashboard.widgets
            ]
        }

    def create_custom_widget(self, widget_id: str, widget_type: str,
                           query_func: callable) -> Dict[str, Any]:
        """Register a custom widget with a query function."""
        self.custom_widgets[widget_id] = {
            "type": widget_type,
            "query_func": query_func
        }
        return {"success": True, "widget_id": widget_id}


def main():
    """Test the Dashboard Generator."""
    from analytics.metrics_collector import MetricsCollector, MetricPoint, MetricType, AggregationType, AggregationQuery
    from analytics.alert_manager import AlertManager

    metrics_collector = MetricsCollector()
    alert_manager = AlertManager()

    generator = DashboardGenerator(metrics_collector=metrics_collector, alert_manager=alert_manager)
    print("Testing Dashboard Generator...")

    # List dashboards
    dashboards = generator.list_dashboards()
    print(f"Available dashboards: {len(dashboards)}")
    for d in dashboards:
        print(f"  - {d['dashboard_id']}: {d['name']} ({d['type']})")

    # Generate a sample dashboard
    sample = generator.generate_dashboard("dept_performance")
    print(f"\nDepartment Performance Dashboard:")
    print(json.dumps(sample, indent=2)[:500] + "...")

    print("\nDashboard Generator test completed!")


if __name__ == "__main__":
    main()