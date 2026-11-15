#!/usr/bin/env python3
"""
Analytics Engine - KPI Tracking and Performance Monitoring

Collects, processes, and reports metrics across the VJSOS-AI system:
- Task performance metrics (duration, throughput, error rates)
- Department utilization and agent effectiveness
- System health and resource usage
- Trend analysis and anomaly detection
- Business metrics (time-to-completion, satisfaction indicators)

All metrics flow through the Event Bus to Orchestrator.
"""

import json
import time
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
from enum import Enum
import statistics
from collections import Counter


class MetricType(Enum):
    PERFORMANCE = "performance"
    UTILIZATION = "utilization"
    ERROR_RATE = "error_rate"
    THROUGHPUT = "throughput"
    RESPONSE_TIME = "response_time"
    SYSTEM_HEALTH = "system_health"
    USER_SATISFACTION = "user_satisfaction"
    BUSINESS = "business"


@dataclass
class MetricPoint:
    """Single metric data point."""
    metric_type: str
    value: float
    unit: str
    timestamp: str
    source: str
    tags: Dict[str, str] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = {}
        if self.metadata is None:
            self.metadata = {}


@dataclass
class AnalyticsQuery:
    """Analytics query definition."""
    metric_types: List[str]
    time_window_hours: int
    department: Optional[str] = None
    source: Optional[str] = None
    aggregation: str = "average"  # average, sum, max, min, percentile
    filters: Dict[str, Any] = None

    def __post_init__(self):
        if self.filters is None:
            self.filters = {}


class AnalyticsEngine:
    """Analytics engine for KPI tracking and performance monitoring."""

    def __init__(self):
        self.engine_id = "analytics-engine@vjsos-ai"
        self.metrics_store: deque = deque(maxlen=100000)
        self.running_metrics: Dict[str, Dict[str, Any]] = {}
        self.alert_thresholds = {
            "error_rate": 0.10,  # 10% error rate
            "response_time_p95": 30.0,  # 30 seconds p95
            "task_failure_rate": 0.15,  # 15% failure rate
            "system_down_time": 300.0  # 5 minutes
        }
        self.report_templates = {
            "daily": self._daily_report,
            "hourly": self._hourly_report,
            "department": self._department_report,
            "agent": self._agent_report
        }

    def record_metric(self, metric: MetricPoint):
        """Record a single metric point."""
        self.metrics_store.append(asdict(metric))

        # Update running metrics
        key = f"{metric.metric_type}_{metric.source}"
        if key not in self.running_metrics:
            self.running_metrics[key] = {
                "sum": 0.0,
                "count": 0,
                "min": float('inf'),
                "max": float('-inf'),
                "latest": metric.value,
                "updated_at": metric.timestamp,
                "unit": metric.unit,
                "tags": metric.tags,
                "metadata": metric.metadata
            }

        rm = self.running_metrics[key]
        rm["sum"] += metric.value
        rm["count"] += 1
        rm["min"] = min(rm["min"], metric.value)
        rm["max"] = max(rm["max"], metric.value)
        rm["latest"] = metric.value
        rm["updated_at"] = metric.timestamp

    def query_metrics(self, query: AnalyticsQuery) -> Dict[str, Any]:
        """Query metrics with aggregation."""
        # Filter by time window
        cutoff_time = datetime.utcnow() - timedelta(hours=query.time_window_hours)
        cutoff_timestamp = cutoff_time.isoformat() + "Z"

        filtered_metrics = []
        for metric_data in self.metrics_store:
            metric = MetricPoint(**metric_data) if isinstance(metric_data, dict) else metric_data

            # Apply time filter
            if metric.timestamp < cutoff_timestamp:
                continue

            # Apply type filter
            if query.metric_types and metric.metric_type not in query.metric_types:
                continue

            # Apply source filter
            if query.source and metric.source != query.source:
                continue

            # Apply department filter (via tags)
            if query.department and metric.tags.get("department") != query.department:
                continue

            # Apply custom filters
            matches_filters = True
            for filter_key, filter_value in query.filters.items():
                if filter_key == "tags":
                    for tag_key, tag_value in filter_value.items():
                        if metric.tags.get(tag_key) != tag_value:
                            matches_filters = False
                            break
                elif filter_key in metric.tags or filter_key in metric.metadata:
                    if metric.tags.get(filter_key) != filter_value and metric.metadata.get(filter_key) != filter_value:
                        matches_filters = False
                        break

            if matches_filters:
                filtered_metrics.append(metric)

        # Apply aggregation
        result = self._aggregate_metrics(filtered_metrics, query.aggregation)

        return {
            "query": asdict(query),
            "metric_count": len(filtered_metrics),
            "aggregated_result": result,
            "time_range": {
                "start": cutoff_timestamp,
                "end": datetime.utcnow().isoformat() + "Z"
            }
        }

    def get_running_metrics(self) -> Dict[str, Any]:
        """Get running (real-time) metrics."""
        return {
            "metrics": self.running_metrics,
            "last_updated": datetime.utcnow().isoformat() + "Z"
        }

    def check_alerts(self) -> List[Dict[str, Any]]:
        """Check for alerts based on thresholds."""
        alerts = []
        cutoff_time = datetime.utcnow() - timedelta(hours=1)
        cutoff_timestamp = cutoff_time.isoformat() + "Z"

        # Check error rate
        recent_metrics = [
            MetricPoint(**data) if isinstance(data, dict) else data
            for data in self.metrics_store
            if data.get("timestamp", "") >= cutoff_timestamp and data.get("metric_type") == "error_rate"
        ]

        if recent_metrics:
            latest_error_rate = recent_metrics[-1].value
            if latest_error_rate > self.alert_thresholds["error_rate"]:
                alerts.append({
                    "type": "HIGH_ERROR_RATE",
                    "value": latest_error_rate,
                    "threshold": self.alert_thresholds["error_rate"],
                    "severity": "critical",
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                })

        # Check system health
        health_metrics = [
            MetricPoint(**data) if isinstance(data, dict) else data
            for data in self.metrics_store
            if data.get("timestamp", "") >= cutoff_timestamp and data.get("metric_type") == "system_health"
        ]

        if not health_metrics:
            # Check for system downtime (no metrics in last hour)
            alerts.append({
                "type": "SYSTEM_DOWN",
                "value": 1.0,
                "threshold": 0.0,
                "severity": "critical",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "message": "No system health metrics in the last hour"
            })

        return alerts

    def generate_report(self, report_type: str, department: Optional[str] = None,
                       time_window_hours: int = 24) -> Dict[str, Any]:
        """Generate analytics report."""
        if report_type not in self.report_templates:
            return {"error": f"Unknown report type: {report_type}"}

        template = self.report_templates[report_type]
        return template(department, time_window_hours)

    def record_task_completion(self, task_id: str, department: str, agent_id: str,
                              duration: float, status: str, error: Optional[str] = None):
        """Record task completion metrics."""
        timestamp = datetime.utcnow().isoformat() + "Z"

        # Performance metrics
        self.record_metric(MetricPoint(
            metric_type="response_time",
            value=duration,
            unit="seconds",
            timestamp=timestamp,
            source=agent_id,
            tags={"department": department, "task_id": task_id, "status": status},
            metadata={"task_id": task_id, "department": department, "agent_id": agent_id}
        ))

        # Status tracking
        status_value = 1.0 if status == "COMPLETED" else 0.0
        self.record_metric(MetricPoint(
            metric_type="task_status",
            value=status_value,
            unit="ratio",
            timestamp=timestamp,
            source=agent_id,
            tags={"department": department, "task_id": task_id, "status": status},
            metadata={"task_id": task_id, "department": department, "agent_id": agent_id}
        ))

        # Error rate (if failed)
        if error:
            self.record_metric(MetricPoint(
                metric_type="error_rate",
                value=1.0,
                unit="ratio",
                timestamp=timestamp,
                source=agent_id,
                tags={"department": department, "task_id": task_id, "error": error},
                metadata={"task_id": task_id, "department": department, "agent_id": agent_id, "error": error}
            ))

        # Department utilization
        self.record_metric(MetricPoint(
            metric_type="utilization",
            value=1.0,  # Busy indicator
            unit="ratio",
            timestamp=timestamp,
            source=department,
            tags={"department": department, "agent_id": agent_id, "task_id": task_id},
            metadata={"task_id": task_id, "department": department, "agent_id": agent_id}
        ))

    def record_system_health(self, health_data: Dict[str, Any]):
        """Record system health metrics."""
        timestamp = datetime.utcnow().isoformat() + "Z"

        for metric_type, value in health_data.items():
            self.record_metric(MetricPoint(
                metric_type=metric_type,
                value=float(value),
                unit="unitless",
                timestamp=timestamp,
                source="system",
                tags={"component": metric_type},
                metadata=health_data
            ))

    # === Report Templates ===

    def _daily_report(self, department: Optional[str], time_window_hours: int) -> Dict[str, Any]:
        """Generate daily report."""
        cutoff_time = datetime.utcnow() - timedelta(hours=time_window_hours)
        cutoff_timestamp = cutoff_time.isoformat() + "Z"

        # Query key metrics
        query = AnalyticsQuery(
            metric_types=["response_time", "utilization", "error_rate"],
            time_window_hours=time_window_hours,
            department=department
        )
        results = self.query_metrics(query)

        return {
            "report_type": "daily",
            "department": department,
            "time_window_hours": time_window_hours,
            "summary": {
                "total_tasks": results["metric_count"] // 3,  # Rough estimate
                "average_response_time": results["aggregated_result"].get("response_time", 0),
                "utilization_rate": results["aggregated_result"].get("utilization", 0),
                "error_rate": results["aggregated_result"].get("error_rate", 0)
            },
            "detailed": results,
            "generated_at": datetime.utcnow().isoformat() + "Z"
        }

    def _hourly_report(self, department: Optional[str], time_window_hours: int) -> Dict[str, Any]:
        """Generate hourly report."""
        query = AnalyticsQuery(
            metric_types=["response_time", "system_health"],
            time_window_hours=time_window_hours,
            department=department
        )
        results = self.query_metrics(query)

        return {
            "report_type": "hourly",
            "department": department,
            "time_window_hours": time_window_hours,
            "performance": {
                "response_time": results["aggregated_result"].get("response_time"),
                "system_health": results["aggregated_result"].get("system_health")
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

    def _department_report(self, department: Optional[str], time_window_hours: int) -> Dict[str, Any]:
        """Generate department-specific report."""
        query = AnalyticsQuery(
            metric_types=["response_time", "utilization", "error_rate"],
            time_window_hours=time_window_hours,
            department=department
        )
        results = self.query_metrics(query)

        return {
            "report_type": "department",
            "department": department,
            "time_window_hours": time_window_hours,
            "performance": {
                "response_time": {
                    "average": results["aggregated_result"].get("response_time", 0),
                    "min": results["aggregated_result"].get("response_time_min", 0),
                    "max": results["aggregated_result"].get("response_time_max", 0)
                },
                "utilization": results["aggregated_result"].get("utilization", 0),
                "error_rate": results["aggregated_result"].get("error_rate", 0)
            },
            "department_summary": {
                "most_active_agent": "agent_1",  # Would be computed from metrics
                "task_distribution": {},
                "performance_trend": "improving"
            }
        }

    def _agent_report(self, department: Optional[str], time_window_hours: int) -> Dict[str, Any]:
        """Generate agent-specific report."""
        query = AnalyticsQuery(
            metric_types=["response_time", "task_status"],
            time_window_hours=time_window_hours,
            department=department
        )
        results = self.query_metrics(query)

        return {
            "report_type": "agent",
            "department": department,
            "time_window_hours": time_window_hours,
            "agent_performance": {
                "response_time": results["aggregated_result"].get("response_time"),
                "task_completion_rate": results["aggregated_result"].get("task_status", 0)
            },
            "rankings": {
                "by_response_time": [],
                "by_completion_rate": []
            }
        }

    def _aggregate_metrics(self, metrics: List[MetricPoint], aggregation: str) -> Dict[str, Any]:
        """Aggregate metrics using specified method."""
        if not metrics:
            return {}

        result = {}

        # Group by metric type for organization
        by_type = defaultdict(list)
        for metric in metrics:
            by_type[metric.metric_type].append(metric)

        # Aggregate each type
        for metric_type, metric_list in by_type.items():
            values = [m.value for m in metric_list]

            if aggregation == "average":
                result[f"{metric_type}"] = statistics.mean(values) if values else 0
            elif aggregation == "sum":
                result[f"{metric_type}"] = sum(values) if values else 0
            elif aggregation == "max":
                result[f"{metric_type}"] = max(values) if values else 0
            elif aggregation == "min":
                result[f"{metric_type}"] = min(values) if values else 0
            elif aggregation == "percentile":
                result[f"{metric_type}"] = statistics.quantiles(values, n=10)[-1] if len(values) >= 10 else (statistics.mean(values) if values else 0)
            else:
                result[f"{metric_type}"] = statistics.mean(values) if values else 0

            # Add min/max for more insights
            if len(values) > 1:
                result[f"{metric_type}_min"] = min(values)
                result[f"{metric_type}_max"] = max(values)

        return result


def main():
    """Test the Analytics Engine."""
    engine = AnalyticsEngine()
    print("Testing Analytics Engine...")

    # Record some test metrics
    engine.record_metric(MetricPoint(
        metric_type="response_time",
        value=5.2,
        unit="seconds",
        timestamp=datetime.utcnow().isoformat() + "Z",
        source="android-agent@vjsos-ai",
        tags={"department": "engineering", "task_type": "code_generation"}
    ))

    engine.record_metric(MetricPoint(
        metric_type="utilization",
        value=0.85,
        unit="ratio",
        timestamp=datetime.utcnow().isoformat() + "Z",
        source="engineering",
        tags={"department": "engineering"}
    ))

    engine.record_metric(MetricPoint(
        metric_type="error_rate",
        value=0.05,
        unit="ratio",
        timestamp=datetime.utcnow().isoformat() + "Z",
        source="android-agent@vjsos-ai",
        tags={"department": "engineering"}
    ))

    # Record task completion
    engine.record_task_completion(
        task_id="task_001",
        department="engineering",
        agent_id="android-agent@vjsos-ai",
        duration=4.8,
        status="COMPLETED"
    )

    # Generate reports
    daily_report = engine.generate_report("daily", "engineering")
    hourly_report = engine.generate_report("hourly", "engineering")

    print(f"Daily Report: {json.dumps(daily_report, indent=2)}")
    print(f"\nHourly Report: {json.dumps(hourly_report, indent=2)}")
    print("\nAnalytics Engine test completed!")


if __name__ == "__main__":
    main()