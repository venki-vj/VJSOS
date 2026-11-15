#!/usr/bin/env python3
"""
Cost Tracker - Resource Usage and Cost Tracking

Tracks resource usage and costs across the VJSOS system:
- Compute costs (CPU, memory, GPU)
- API call costs (external services, LLMs)
- Storage costs
- Network costs
- Custom cost models per department/agent
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field, asdict
from enum import Enum
from collections import defaultdict


class ResourceType(Enum):
    COMPUTE = "compute"
    API_CALL = "api_call"
    STORAGE = "storage"
    NETWORK = "network"
    GPU = "gpu"
    CUSTOM = "custom"


class CostUnit(Enum):
    USD = "USD"
    CREDITS = "credits"
    TOKENS = "tokens"
    SECONDS = "seconds"
    GB_HOURS = "gb_hours"


@dataclass
class CostEntry:
    """Single cost entry."""
    entry_id: str
    resource_type: str
    cost_unit: str
    amount: float
    timestamp: str
    source: str  # agent_id, department, or "system"
    tags: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CostModel:
    """Cost model for a resource type."""
    resource_type: str
    unit: str
    rate: float  # cost per unit
    description: str
    effective_date: str


class CostTracker:
    """Tracks and aggregates costs across the VJSOS system."""

    def __init__(self):
        self.tracker_id = "cost-tracker@vjsos-ai"
        self.cost_entries: List[CostEntry] = []
        self.cost_models: Dict[str, CostModel] = {}
        self.budgets: Dict[str, Dict[str, Any]] = {}
        self._load_default_models()

    def _load_default_models(self):
        """Load default cost models."""
        default_models = {
            "llm_input_tokens": CostModel(
                resource_type="llm_input_tokens",
                unit="tokens",
                rate=0.00001,  # $0.01 per 1K tokens
                description="LLM input token cost",
                effective_date=datetime.utcnow().isoformat() + "Z"
            ),
            "llm_output_tokens": CostModel(
                resource_type="llm_output_tokens",
                unit="tokens",
                rate=0.00003,  # $0.03 per 1K tokens
                description="LLM output token cost",
                effective_date=datetime.utcnow().isoformat() + "Z"
            ),
            "cpu_seconds": CostModel(
                resource_type="cpu_seconds",
                unit="seconds",
                rate=0.0000001,  # $0.0001 per 1000 seconds
                description="CPU compute cost",
                effective_date=datetime.utcnow().isoformat() + "Z"
            ),
            "gpu_seconds": CostModel(
                resource_type="gpu_seconds",
                unit="seconds",
                rate=0.000001,  # $0.001 per 1000 seconds
                description="GPU compute cost",
                effective_date=datetime.utcnow().isoformat() + "Z"
            ),
            "storage_gb_month": CostModel(
                resource_type="storage_gb_month",
                unit="gb_months",
                rate=0.10,  # $0.10 per GB/month
                description="Storage cost",
                effective_date=datetime.utcnow().isoformat() + "Z"
            ),
            "api_call": CostModel(
                resource_type="api_call",
                unit="calls",
                rate=0.001,  # $0.001 per call
                description="External API call cost",
                effective_date=datetime.utcnow().isoformat() + "Z"
            )
        }
        self.cost_models = default_models

    def record_cost(self, entry: CostEntry):
        """Record a cost entry."""
        self.cost_entries.append(entry)

    def record_llm_usage(self, agent_id: str, model: str,
                        input_tokens: int, output_tokens: int,
                        tags: Optional[Dict[str, str]] = None):
        """Record LLM token usage."""
        tags = tags or {}
        tags["model"] = model

        self.record_cost(CostEntry(
            entry_id=f"llm_{int(time.time())}_{agent_id}",
            resource_type="llm_input_tokens",
            cost_unit="tokens",
            amount=input_tokens,
            timestamp=datetime.utcnow().isoformat() + "Z",
            source=agent_id,
            tags=tags
        ))

        self.record_cost(CostEntry(
            entry_id=f"llm_{int(time.time())}_{agent_id}_out",
            resource_type="llm_output_tokens",
            cost_unit="tokens",
            amount=output_tokens,
            timestamp=datetime.utcnow().isoformat() + "Z",
            source=agent_id,
            tags=tags
        ))

    def record_compute(self, agent_id: str, cpu_seconds: float,
                      gpu_seconds: float = 0,
                      tags: Optional[Dict[str, str]] = None):
        """Record compute usage."""
        tags = tags or {}

        if cpu_seconds > 0:
            self.record_cost(CostEntry(
                entry_id=f"cpu_{int(time.time())}_{agent_id}",
                resource_type="cpu_seconds",
                cost_unit="seconds",
                amount=cpu_seconds,
                timestamp=datetime.utcnow().isoformat() + "Z",
                source=agent_id,
                tags=tags
            ))

        if gpu_seconds > 0:
            self.record_cost(CostEntry(
                entry_id=f"gpu_{int(time.time())}_{agent_id}",
                resource_type="gpu_seconds",
                cost_unit="seconds",
                amount=gpu_seconds,
                timestamp=datetime.utcnow().isoformat() + "Z",
                source=agent_id,
                tags=tags
            ))

    def record_api_call(self, agent_id: str, api_name: str,
                       count: int = 1,
                       tags: Optional[Dict[str, str]] = None):
        """Record external API call."""
        tags = tags or {}
        tags["api"] = api_name

        self.record_cost(CostEntry(
            entry_id=f"api_{int(time.time())}_{agent_id}",
            resource_type="api_call",
            cost_unit="calls",
            amount=count,
            timestamp=datetime.utcnow().isoformat() + "Z",
            source=agent_id,
            tags=tags
        ))

    def record_storage(self, agent_id: str, gb_hours: float,
                      tags: Optional[Dict[str, str]] = None):
        """Record storage usage."""
        tags = tags or {}

        self.record_cost(CostEntry(
            entry_id=f"storage_{int(time.time())}_{agent_id}",
            resource_type="storage_gb_month",
            cost_unit="gb_months",
            amount=gb_hours / 730,  # Convert GB-hours to GB-months
            timestamp=datetime.utcnow().isoformat() + "Z",
            source=agent_id,
            tags=tags
        ))

    def get_costs(self, source: Optional[str] = None,
                 resource_type: Optional[str] = None,
                 start_time: Optional[str] = None,
                 end_time: Optional[str] = None) -> List[CostEntry]:
        """Get cost entries with filters."""
        filtered = self.cost_entries

        if source:
            filtered = [e for e in filtered if e.source == source]

        if resource_type:
            filtered = [e for e in filtered if e.resource_type == resource_type]

        if start_time:
            start = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
            filtered = [e for e in filtered if datetime.fromisoformat(e.timestamp.replace("Z", "+00:00")) >= start]

        if end_time:
            end = datetime.fromisoformat(end_time.replace("Z", "+00:00"))
            filtered = [e for e in filtered if datetime.fromisoformat(e.timestamp.replace("Z", "+00:00")) <= end]

        return filtered

    def calculate_total_cost(self, source: Optional[str] = None,
                           start_time: Optional[str] = None,
                           end_time: Optional[str] = None) -> float:
        """Calculate total cost in USD."""
        entries = self.get_costs(source=source, start_time=start_time, end_time=end_time)

        total = 0.0
        for entry in entries:
            model = self.cost_models.get(entry.resource_type)
            if model:
                total += entry.amount * model.rate

        return total

    def calculate_cost_by_resource(self, source: Optional[str] = None,
                                  start_time: Optional[str] = None,
                                  end_time: Optional[str] = None) -> Dict[str, float]:
        """Calculate cost breakdown by resource type."""
        entries = self.get_costs(source=source, start_time=start_time, end_time=end_time)

        costs = defaultdict(float)
        for entry in entries:
            model = self.cost_models.get(entry.resource_type)
            if model:
                costs[entry.resource_type] += entry.amount * model.rate

        return dict(costs)

    def calculate_cost_by_source(self, start_time: Optional[str] = None,
                                end_time: Optional[str] = None) -> Dict[str, float]:
        """Calculate cost breakdown by source (agent/department)."""
        entries = self.get_costs(start_time=start_time, end_time=end_time)

        costs = defaultdict(float)
        for entry in entries:
            model = self.cost_models.get(entry.resource_type)
            if model:
                costs[entry.source] += entry.amount * model.rate

        return dict(costs)

    def calculate_cost_by_department(self, start_time: Optional[str] = None,
                                    end_time: Optional[str] = None) -> Dict[str, float]:
        """Calculate cost breakdown by department."""
        entries = self.get_costs(start_time=start_time, end_time=end_time)

        dept_costs = defaultdict(float)
        for entry in entries:
            model = self.cost_models.get(entry.resource_type)
            if not model:
                continue

            # Extract department from tags or infer from source
            dept = entry.tags.get("department")
            if not dept:
                # Infer from source (e.g., "android-agent@engineering@vjsos-ai")
                parts = entry.source.split("@")
                if len(parts) >= 2:
                    dept = parts[1]

            if dept:
                dept_costs[dept] += entry.amount * model.rate

        return dict(dept_costs)

    def set_budget(self, budget_id: str, limit: float,
                  period: str = "monthly",  # daily, weekly, monthly
                  scope: str = "global",  # global, department, agent
                  scope_value: Optional[str] = None):
        """Set a budget limit."""
        self.budgets[budget_id] = {
            "budget_id": budget_id,
            "limit": limit,
            "period": period,
            "scope": scope,
            "scope_value": scope_value,
            "created_at": datetime.utcnow().isoformat() + "Z",
            "alerts_sent": []
        }

    def check_budgets(self, start_time: Optional[str] = None,
                     end_time: Optional[str] = None) -> List[Dict[str, Any]]:
        """Check all budgets against actual spend."""
        alerts = []

        for budget_id, budget in self.budgets.items():
            scope = budget["scope"]
            scope_value = budget.get("scope_value")

            # Calculate actual spend for this budget
            if scope == "global":
                actual = self.calculate_total_cost(start_time=start_time, end_time=end_time)
            elif scope == "department":
                dept_costs = self.calculate_cost_by_department(start_time=start_time, end_time=end_time)
                actual = dept_costs.get(scope_value, 0)
            elif scope == "agent":
                source_costs = self.calculate_cost_by_source(start_time=start_time, end_time=end_time)
                actual = source_costs.get(scope_value, 0)
            else:
                continue

            limit = budget["limit"]
            percentage = (actual / limit * 100) if limit > 0 else 0

            if percentage >= 100:
                severity = "critical"
            elif percentage >= 80:
                severity = "warning"
            elif percentage >= 50:
                severity = "info"
            else:
                severity = "ok"

            if severity != "ok" and budget_id not in budget["alerts_sent"]:
                budget["alerts_sent"].append(budget_id)
                alerts.append({
                    "budget_id": budget_id,
                    "severity": severity,
                    "actual": actual,
                    "limit": limit,
                    "percentage": percentage,
                    "message": f"Budget {budget_id} at {percentage:.1f}% (${actual:.4f}/${limit:.4f})"
                })

        return alerts

    def get_cost_report(self, start_time: Optional[str] = None,
                       end_time: Optional[str] = None,
                       group_by: str = "resource") -> Dict[str, Any]:
        """Generate a cost report."""
        total = self.calculate_total_cost(start_time=start_time, end_time=end_time)

        report = {
            "report_id": f"cost_report_{int(time.time())}",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "period": {
                "start": start_time or "inception",
                "end": end_time or "now"
            },
            "total_cost_usd": total,
            "entries_count": len(self.get_costs(start_time=start_time, end_time=end_time))
        }

        if group_by == "resource":
            report["by_resource"] = self.calculate_cost_by_resource(start_time=start_time, end_time=end_time)
        elif group_by == "source":
            report["by_source"] = self.calculate_cost_by_source(start_time=start_time, end_time=end_time)
        elif group_by == "department":
            report["by_department"] = self.calculate_cost_by_department(start_time=start_time, end_time=end_time)
        elif group_by == "all":
            report["by_resource"] = self.calculate_cost_by_resource(start_time=start_time, end_time=end_time)
            report["by_source"] = self.calculate_cost_by_source(start_time=start_time, end_time=end_time)
            report["by_department"] = self.calculate_cost_by_department(start_time=start_time, end_time=end_time)

        # Add budget status
        if self.budgets:
            report["budget_alerts"] = self.check_budgets(start_time=start_time, end_time=end_time)

        return report

    def add_cost_model(self, model: CostModel):
        """Add or update a cost model."""
        self.cost_models[model.resource_type] = model

    def get_cost_models(self) -> Dict[str, Any]:
        """Get all cost models."""
        return {
            model_id: asdict(model)
            for model_id, model in self.cost_models.items()
        }

    def export_costs(self, path: str, start_time: Optional[str] = None,
                    end_time: Optional[str] = None):
        """Export cost entries to JSON file."""
        entries = self.get_costs(start_time=start_time, end_time=end_time)
        export_data = {
            "exported_at": datetime.utcnow().isoformat() + "Z",
            "entry_count": len(entries),
            "entries": [asdict(e) for e in entries]
        }

        with open(path, "w") as f:
            json.dump(export_data, f, indent=2)


def main():
    """Test the Cost Tracker."""
    tracker = CostTracker()
    print("Testing Cost Tracker...")

    # Record some usage
    tracker.record_llm_usage("android-agent@engineering@vjsos-ai", "claude-3.5-sonnet",
                           input_tokens=5000, output_tokens=2000,
                           tags={"department": "engineering", "task": "code_generation"})

    tracker.record_compute("android-agent@engineering@vjsos-ai",
                          cpu_seconds=30.5, gpu_seconds=0,
                          tags={"department": "engineering"})

    tracker.record_api_call("android-agent@engineering@vjsos-ai",
                           "github_api", count=5,
                           tags={"department": "engineering"})

    # Record usage for another department
    tracker.record_llm_usage("script-agent@media@vjsos-ai", "claude-3.5-sonnet",
                           input_tokens=3000, output_tokens=1500,
                           tags={"department": "media", "task": "script_writing"})

    # Generate reports
    report = tracker.get_cost_report(group_by="department")
    print(f"Cost Report: {json.dumps(report, indent=2)}")

    # Set budget
    tracker.set_budget("eng_monthly", 100.0, period="monthly", scope="department", scope_value="engineering")
    tracker.set_budget("global_monthly", 500.0, period="monthly", scope="global")

    # Check budgets
    budget_alerts = tracker.check_budgets()
    print(f"\nBudget Alerts: {json.dumps(budget_alerts, indent=2)}")

    print("\nCost Tracker test completed!")


if __name__ == "__main__":
    main()