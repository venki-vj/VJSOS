#!/usr/bin/env python3
"""
Metrics Collector - KPI Aggregation and Storage

Collects and aggregates metrics from across the VJSOS system:
- Task execution metrics (duration, throughput, success rates)
- System resource metrics
- Agent performance metrics
- Department utilization metrics
- Error and failure tracking

All metrics flow through the Event Bus and are stored for analysis.
"""

import json
import time
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from collections import defaultdict, deque, Counter
from dataclasses import dataclass, asdict
from enum import Enum
import statistics
from collections import defaultdict


class MetricType(Enum):
    TASK = "task"
    SYSTEM = "system"
    AGENT = "agent"
    DEPARTMENT = "department"
    PERFORMANCE = "performance"
    ERROR = "error"
    CUSTOM = "custom"


class AggregationType(Enum):
    COUNT = "count"
    SUM = "sum"
    AVERAGE = "average"
    MINIMUM = "minimum"
    MAXIMUM = "maximum"
    MEDIAN = "median"
    PERCENTILE = "percentile"
    RATE = "rate"


@dataclass
class MetricPoint:
    """Single metric data point."""
    metric_type: str
    name: str
    value: float
    unit: str
    timestamp: str
    source: str
    tags: Dict[str, str] = None
    metadata: Dict[str, Any] = None
    aggregation_window: str = "raw"  # raw, minute, hour, day

    def __post_init__(self):
        if self.tags is None:
            self.tags = {}
        if self.metadata is None:
            self.metadata = {}


@dataclass
class AggregationQuery:
    """Query for metric aggregation."""
    metric_names: List[str]
    start_time: str
    end_time: str
    metric_type: Optional[MetricType] = None
    tags: Optional[Dict[str, str]] = None
    aggregation_type: AggregationType = AggregationType.AVERAGE
    group_by: Optional[List[str]] = None
    filters: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if self.filters is None:
            self.filters = {}


@dataclass
class AggregatedValue:
    """Aggregated metric value."""
    name: str
    value: float
    unit: str
    count: int
    timestamp: str
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class MetricsCollector:
    """Collects, stores, and aggregates metrics for VJSOS."""

    def __init__(self):
        self.collector_id = "metrics-collector@vjsos-ai"
        self.raw_metrics: deque = deque(maxlen=1000000)
        self.aggregated_metrics: Dict[str, deque] = defaultdict(lambda: deque(maxlen=10000))
        self.counters: Dict[str, int] = defaultdict(int)
        self.gauges: Dict[str, List[float]] = defaultdict(list)
        self.histograms: Dict[str, List[float]] = defaultdict(list)
        self.tags_index: Dict[str, Dict[str, List[MetricPoint]]] = defaultdict(lambda: defaultdict(list))
        self.metric_definitions: Dict[str, Dict[str, Any]] = {}
        self.alert_rules: Dict[str, Dict[str, Any]] = {}
        self.custom_aggregators: Dict[str, Callable] = {}

    def record_metric(self, metric: Optional[MetricPoint] = None, **kwargs):
        """Record a single metric point.

        Accepts either a MetricPoint object or keyword args:
            record_metric(MetricPoint(metric_type=..., name=..., ...))
            record_metric(metric_type="task", name="...", value=42, unit="count", ...)
        """
        if metric is None:
            metric = MetricPoint(
                metric_type=kwargs.pop("metric_type", "custom"),
                name=kwargs.pop("name", "unnamed"),
                value=kwargs.pop("value", 0.0),
                unit=kwargs.pop("unit", ""),
                timestamp=kwargs.pop("timestamp",
                                     time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())),
                source=kwargs.pop("source", "unknown"),
                tags=kwargs.pop("tags", {}),
                metadata=kwargs.pop("metadata", {}),
            )

        # Add to raw metrics
        self.raw_metrics.append(asdict(metric))

        # Update aggregates based on metric type and name
        metric_key = f"{metric.metric_type}.{metric.name}"

        # Store in appropriate structure based on metric type
        if metric.name.endswith("_count"):
            self.counters[metric.name] += int(metric.value)
        elif metric.name.endswith("_gauge"):
            self._update_gauge(metric.name, metric.value)
        elif metric.name.endswith("_histogram"):
            self._update_histogram(metric.name, metric.value)
        else:
            self._update_timeseries(metric_key, metric)

        # Update tags index
        for tag_key, tag_value in metric.tags.items():
            tag_composite_key = f"{metric.name}.{tag_key}={tag_value}"
            self.tags_index[tag_composite_key].append(metric)

        # Check for alerts
        self._check_alerts(metric)

    def _update_gauge(self, name: str, value: float):
        """Update gauge value."""
        values = self.gauges[name]
        # Keep last 1000 values for rolling average
        if len(values) >= 1000:
            values.pop(0)
        values.append(value)

    def _update_histogram(self, name: str, value: float):
        """Update histogram data."""
        values = self.histograms[name]
        # Keep last 10000 values
        if len(values) >= 10000:
            values.pop(0)
        values.append(value)

    def _update_timeseries(self, key: str, metric: MetricPoint):
        """Update time series data."""
        # Keep last 10000 data points per metric
        series = self.aggregated_metrics[key]
        if len(series) >= 10000:
            series.popleft()
        series.append(asdict(metric))

    def query_metrics(self, query: AggregationQuery) -> Dict[str, Any]:
        """Query metrics with aggregation."""
        # Convert query to internal format
        start_time = datetime.fromisoformat(query.start_time.replace("Z", "+00:00"))
        end_time = datetime.fromisoformat(query.end_time.replace("Z", "+00:00"))

        # Filter metrics by time range
        filtered_metrics = self._filter_metrics_by_time(start_time, end_time, query)

        # Apply tags filtering
        if query.tags:
            filtered_metrics = self._filter_by_tags(filtered_metrics, query.tags)

        # Apply metrics name filtering
        filtered_metrics = [
            MetricPoint(**m) for m in filtered_metrics
            if any(name in m.get("name", "") for name in query.metric_names)
        ]

        # Apply aggregation
        result = self._aggregate_metrics(filtered_metrics, query)

        return {
            "query": asdict(query),
            "metrics_count": len(filtered_metrics),
            "aggregated_values": result,
            "time_range": {
                "start": query.start_time,
                "end": query.end_time
            }
        }

    def _filter_metrics_by_time(self, start_time: datetime, end_time: datetime,
                               query: AggregationQuery) -> List[Dict[str, Any]]:
        """Filter metrics by time range."""
        filtered = []
        for metric_data in self.raw_metrics:
            try:
                metric_time = datetime.fromisoformat(metric_data.get("timestamp", "").replace("Z", "+00:00"))
                if start_time <= metric_time <= end_time:
                    # Apply metric type filter
                    if query.metric_type:
                        if metric_data.get("metric_type") != query.metric_type.value:
                            continue
                    filtered.append(metric_data)
            except (ValueError, KeyError):
                continue
        return filtered

    def _filter_by_tags(self, metrics: List[Dict[str, Any]], tags: Dict[str, str]) -> List[Dict[str, Any]]:
        """Filter metrics by tags."""
        return [
            metric for metric in metrics
            if all(metric.get("tags", {}).get(k) == v for k, v in tags.items())
        ]

    def _aggregate_metrics(self, metrics: List[Dict[str, Any]], query: AggregationQuery) -> List[Dict[str, Any]]:
        """Aggregate metrics using specified aggregation type."""
        if not metrics:
            return []

        # Group by group_by fields if specified
        if query.group_by:
            return self._aggregate_with_grouping(metrics, query)
        else:
            return self._aggregate_single_metrics(metrics, query)

    def _aggregate_single_metrics(self, metrics: List[Dict[str, Any]], query: AggregationQuery) -> List[Dict[str, Any]]:
        """Aggregate metrics without grouping."""
        # Group by metric name
        grouped = defaultdict(list)
        for metric_data in metrics:
            name = metric_data.get("name")
            if name:
                grouped[name].append(metric_data)

        results = []
        for metric_name, metric_data in grouped.items():
            aggregated = self._aggregate_metric_set(metric_data, query.aggregation_type)
            results.append(asdict(aggregated))

        return results

    def _aggregate_with_grouping(self, metrics: List[Dict[str, Any]], query: AggregationQuery) -> List[Dict[str, Any]]:
        """Aggregate metrics with grouping."""
        # This would group by specified fields (department, agent, etc.)
        # For now, implement simple grouping
        results = []

        for group_key, metric_data in self._group_metrics(metrics, query.group_by).items():
            aggregated = self._aggregate_metric_set(metric_data, query.aggregation_type)
            results.append(asdict(aggregated))

        return results

    def _group_metrics(self, metrics: List[Dict[str, Any]], group_by: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """Group metrics by specified fields."""
        # Simple implementation - group by source for now
        grouped = defaultdict(list)
        for metric_data in metrics:
            source = metric_data.get("source", "unknown")
            if source:
                grouped[source].append(metric_data)
        return grouped

    def _aggregate_metric_set(self, metrics: List[Dict[str, Any]], aggregation_type: AggregationType) -> AggregatedValue:
        """Aggregate a set of metric data points."""
        if not metrics:
            return AggregatedValue(
                name="",
                value=0.0,
                unit="",
                count=0,
                timestamp=datetime.utcnow().isoformat() + "Z"
            )

        values = []
        for metric_data in metrics:
            try:
                value = float(metric_data.get("value", 0))
                values.append(value)
            except (ValueError, TypeError):
                continue

        if not values:
            return AggregatedValue(
                name=metrics[0].get("name", ""),
                value=0.0,
                unit=metrics[0].get("unit", ""),
                count=0,
                timestamp=datetime.utcnow().isoformat() + "Z"
            )

        # Calculate aggregation
        if aggregation_type == AggregationType.COUNT:
            result_value = len(values)
        elif aggregation_type == AggregationType.SUM:
            result_value = sum(values)
        elif aggregation_type == AggregationType.AVERAGE:
            result_value = statistics.mean(values)
        elif aggregation_type == AggregationType.MINIMUM:
            result_value = min(values)
        elif aggregation_type == AggregationType.MAXIMUM:
            result_value = max(values)
        elif aggregation_type == AggregationType.MEDIAN:
            result_value = statistics.median(values)
        elif aggregation_type == AggregationType.PERCENTILE:
            result_value = statistics.quantiles(values, n=10)[-1]
        elif aggregation_type == AggregationType.RATE:
            # Calculate rate per second
            time_span = self._calculate_time_span([m.get("timestamp") for m in metrics])
            result_value = len(values) / time_span if time_span > 0 else 0
        else:
            result_value = statistics.mean(values)

        return AggregatedValue(
            name=metrics[0].get("name", ""),
            value=result_value,
            unit=metrics[0].get("unit", ""),
            count=len(values),
            timestamp=datetime.utcnow().isoformat() + "Z",
            metadata={"aggregation_type": aggregation_type.value}
        )

    def _calculate_time_span(self, timestamps: List[str]) -> float:
        """Calculate time span in seconds from timestamps."""
        if len(timestamps) < 2:
            return 0.0

        try:
            times = [datetime.fromisoformat(ts.replace("Z", "+00:00")) for ts in timestamps if ts]
            if times:
                return (max(times) - min(times)).total_seconds()
        except (ValueError, AttributeError):
            pass

        return 0.0

    def get_gauge(self, name: str) -> Dict[str, Any]:
        """Get current gauge value."""
        values = self.gauges.get(name, [])
        if not values:
            return {"name": name, "value": 0.0, "count": 0}

        return {
            "name": name,
            "value": values[-1],  # Latest value
            "count": len(values),
            "average": statistics.mean(values)
        }

    def get_counter(self, name: str) -> Dict[str, Any]:
        """Get current counter value."""
        return {
            "name": name,
            "value": self.counters.get(name, 0)
        }

    def get_histogram(self, name: str, percentile: float = 0.95) -> Dict[str, Any]:
        """Get histogram statistics."""
        values = self.histograms.get(name, [])
        if not values:
            return {"name": name, "count": 0}

        return {
            "name": name,
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "average": statistics.mean(values),
            f"p_{int(percentile * 100)}": statistics.quantiles(values, n=100)[int(percentile * 100) - 1] if len(values) >= 100 else statistics.mean(values)
        }

    def get_time_series(self, metric_name: str, start_time: str, end_time: str, aggregation: str = "average") -> List[Dict[str, Any]]:
        """Get time series data for a metric."""
        start = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
        end = datetime.fromisoformat(end_time.replace("Z", "+00:00"))

        metrics = []
        for metric_data in self.aggregated_metrics.get(metric_name, []):
            try:
                metric_time = datetime.fromisoformat(metric_data.get("timestamp", "").replace("Z", "+00:00"))
                if start <= metric_time <= end:
                    metrics.append(metric_data)
            except (ValueError, KeyError):
                continue

        # Apply aggregation
        if aggregation == "sum":
            # Group by time bucket and sum
            return self._bucket_and_aggregate(metrics, "sum", "hour")
        elif aggregation == "average":
            return self._bucket_and_aggregate(metrics, "average", "hour")
        else:
            return [asdict(MetricPoint(**m)) for m in metrics]

    def _bucket_and_aggregate(self, metrics: List[Dict[str, Any]], aggregation: str, bucket_size: str) -> List[Dict[str, Any]]:
        """Bucket metrics by time and aggregate."""
        # Simple implementation - bucket by hour
        buckets = defaultdict(list)
        for metric_data in metrics:
            try:
                metric_time = datetime.fromisoformat(metric_data.get("timestamp", "").replace("Z", "+00:00"))
                if bucket_size == "hour":
                    hour_bucket = metric_time.replace(minute=0, second=0, microsecond=0)
                    buckets[hour_bucket].append(metric_data)
            except (ValueError, KeyError):
                continue

        results = []
        for bucket_time, bucket_metrics in buckets.items():
            if aggregation == "sum":
                value = sum(float(m.get("value", 0)) for m in bucket_metrics)
            elif aggregation == "average":
                values = [float(m.get("value", 0)) for m in bucket_metrics]
                value = statistics.mean(values) if values else 0
            else:
                values = [float(m.get("value", 0)) for m in bucket_metrics]
                value = statistics.mean(values) if values else 0

            results.append({
                "timestamp": bucket_time.isoformat() + "Z",
                "value": value,
                "count": len(bucket_metrics)
            })

        return results

    def add_metric_definition(self, name: str, definition: Dict[str, Any]):
        """Add a metric definition."""
        self.metric_definitions[name] = definition

    def add_alert_rule(self, name: str, rule: Dict[str, Any]):
        """Add an alert rule."""
        self.alert_rules[name] = rule

    def _check_alerts(self, metric: MetricPoint):
        """Check if metric triggers any alerts."""
        for rule_name, rule in self.alert_rules.items():
            if self._metric_matches_rule(metric, rule):
                # Trigger alert
                self._trigger_alert(rule_name, metric, rule)

    def _metric_matches_rule(self, metric: MetricPoint, rule: Dict[str, Any]) -> bool:
        """Check if a metric matches an alert rule."""
        # Basic rule matching
        metric_name = metric.name
        metric_value = metric.value

        if "metric_name" in rule and rule["metric_name"] != metric_name:
            return False

        if "threshold" in rule and "comparison" in rule:
            comparison = rule["comparison"]
            threshold = rule["threshold"]

            if comparison == ">" and metric_value <= threshold:
                return False
            elif comparison == ">=" and metric_value < threshold:
                return False
            elif comparison == "<" and metric_value >= threshold:
                return False
            elif comparison == "<=" and metric_value > threshold:
                return False
            elif comparison == "==" and metric_value != threshold:
                return False
            elif comparison == "!=" and metric_value == threshold:
                return False

        if "tags" in rule:
            for tag_key, tag_value in rule["tags"].items():
                if metric.tags.get(tag_key) != tag_value:
                    return False

        return True

    def _trigger_alert(self, rule_name: str, metric: MetricPoint, rule: Dict[str, Any]):
        """Trigger an alert for a matched rule."""
        alert = {
            "rule_name": rule_name,
            "metric": asdict(metric),
            "triggered_at": datetime.utcnow().isoformat() + "Z",
            "severity": rule.get("severity", "warning")
        }

        # In a real implementation, this would publish to the event bus
        print(f"ALERT: {rule_name} triggered by metric {metric.name} = {metric.value}")


def main():
    """Test the Metrics Collector."""
    collector = MetricsCollector()
    print("Testing Metrics Collector...")

    # Record some test metrics
    collector.record_metric(MetricPoint(
        metric_type=MetricType.TASK.value,
        name="task_duration_seconds",
        value=5.2,
        unit="seconds",
        timestamp=datetime.utcnow().isoformat() + "Z",
        source="android-agent@vjsos-ai",
        tags={"department": "engineering", "agent_type": "worker"}
    ))

    collector.record_metric(MetricPoint(
        metric_type=MetricType.SYSTEM.value,
        name="system_cpu_usage_gauge",
        value=0.85,
        unit="ratio",
        timestamp=datetime.utcnow().isoformat() + "Z",
        source="system",
        tags={"component": "cpu"}
    ))

    collector.record_metric(MetricPoint(
        metric_type=MetricType.ERROR.value,
        name="task_failure_count",
        value=1,
        unit="count",
        timestamp=datetime.utcnow().isoformat() + "Z",
        source="qa-engine@vjsos-ai",
        tags={"department": "engineering", "error_type": "validation"}
    ))

    # Query metrics
    query = AggregationQuery(
        metric_names=["task_duration_seconds"],
        start_time=(datetime.utcnow() - timedelta(hours=1)).isoformat() + "Z",
        end_time=datetime.utcnow().isoformat() + "Z",
        aggregation_type=AggregationType.AVERAGE
    )

    results = collector.query_metrics(query)
    print(f"Query results: {json.dumps(results, indent=2)}")

    # Get gauge
    gauge = collector.get_gauge("system_cpu_usage_gauge")
    print(f"\nGauge: {json.dumps(gauge, indent=2)}")

    # Get counter
    counter = collector.get_counter("task_failure_count")
    print(f"\nCounter: {json.dumps(counter, indent=2)}")

    print("\nMetrics Collector test completed!")


if __name__ == "__main__":
    main()