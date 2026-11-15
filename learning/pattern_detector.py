#!/usr/bin/env python3
"""
Pattern Detector - Advanced Pattern Recognition for Learning Engine

Detects recurring patterns in task executions, failures, and performance data.
Provides the pattern-recognition layer used by the Learning Engine to produce
improvement suggestions and post-mortem analysis.

Separate module from `learning/engine.py` for:
- Memory efficiency (lazy loading of detection logic)
- Testability (pure functions over structured data)
- Extensibility (register custom detectors without touching engine)
"""

import time
import statistics
import hashlib
from collections import defaultdict, Counter
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional, List


class PatternType(Enum):
    PERFORMANCE = "performance"
    FAILURE = "failure"
    FREQUENCY = "frequency"
    CORRELATION = "correlation"
    REGRESSION = "regression"
    ANOMALY = "anomaly"
    CUSTOM = "custom"


@dataclass
class Pattern:
    """A detected pattern in execution data."""
    pattern_id: str
    type: PatternType
    name: str
    description: str
    confidence: float
    detection_method: str
    affected_areas: List[str] = field(default_factory=list)
    examples: List[Dict[str, Any]] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    detected_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class PatternDetector:
    """Detects recurring patterns across multiple dimensions of execution data.

    Operators are stateless: each `detect_*` method consumes raw records and
    returns a list of ``Pattern`` objects. This keeps detection reproducible
    and testable independent of the Learning Engine's internal state.
    """

    def __init__(self, min_samples: int = 3):
        self.detector_id = "pattern-detector@vjsos-ai"
        self.min_samples = min_samples
        self.custom_detectors: Dict[str, callable] = {}

    # ---------- Performance patterns ----------

    def detect_performance(self, executions: List[Dict[str, Any]]) -> List[Pattern]:
        """Detect performance issues (high latency, slow departments/agents)."""
        patterns = []

        # Group by department and agent
        deque_over_slow_depts = defaultdict(list)
        for execution in executions:
            dept = execution.get("department", "unknown")
            deque_over_slow_depts[dept].append(execution)

        for dept, dept_executions in deque_over_slow_depts.items():
            self._analyze_group_performance(dept, dept_executions, patterns)

        return patterns

    def _analyze_group_performance(self, key: str, executions: List[Dict[str, Any]],
                                   patterns: List[Pattern]):
        """Analyze performance of a single department/agent group."""
        if len(executions) < self.min_samples:
            return

        durations = [e.get("duration", 0) for e in executions if e.get("duration")]
        if not durations:
            return

        avg_duration = statistics.mean(durations)
        max_duration = max(durations)

        if avg_duration > 60:
            patterns.append(Pattern(
                pattern_id=f"perf_{key}_{int(time.time())}_{len(patterns)}",
                type=PatternType.PERFORMANCE,
                name=f"High latency in {key}",
                description=f"Average task duration {avg_duration:.1f}s exceeds 60s targets",
                confidence=0.8,
                detection_method="threshold_avg",
                affected_areas=[key],
                examples=[{"task_id": e.get("task_id"), "duration": e.get("duration")} for e in executions[:3]],
                metrics={"avg_duration": avg_duration, "max_duration": max_duration, "samples": len(durations)}
            ))

        if max_duration > 5 * avg_duration and len(durations) >= 3:
            patterns.append(Pattern(
                pattern_id=f"outlier_{key}_{time.time()}",
                type=PatternType.ANOMALY,
                name=f"Duration outlier in {key}",
                description=f"Max duration {max_duration:.1f}s is >5x the average",
                confidence=0.9,
                detection_method="outlier_ratio",
                affected_areas=[key],
                examples=[{"task_id": e.get("task_id"), "duration": e.get("duration")} for e in executions[:3]],
                metrics={"avg_duration": avg_duration, "max_duration": max_duration}
            ))

    # ────────────── Failure patterns ──────────────

    def detect_failures(self, executions: List[Dict[str, Any]]) -> List[Pattern]:
        """Detect recurring failures and common error signatures."""
        patterns = []

        errors = [e.get("error") for e in executions if e.get("error")]
        if not errors:
            return patterns

        common = Counter(errors).most_common(1)[0]
        if common[1] >= self.min_samples:
            error_message, count = common
            patterns.append(Pattern(
                pattern_id=f"failure_{int(time.time())}",
                type=PatternType.FAILURE,
                name="Recurring error",
                description=f"'{error_message}' occurred {count} times",
                confidence=0.85,
                detection_method="frequency_counter",
                affected_areas=["error_handling", "input_validation"],
                examples=[{"order": i, "error": msg} for i, msg in enumerate(errors[:5])],
                metrics={"count": count, "unique_errors": len(set(errors))}
            ))

        return patterns

    # ────────────── Quality patterns ──────────────

    def detect_quality_loss(self, executions: List[Dict[str, Any]]) -> List[Pattern]:
        """Detect quality regressions (QA rejections / feedback cycles)."""
        patterns = []

        qa_failed = [e for e in executions if e.get("qa_passed") is False]
        if len(qa_failed) >= self.min_samples:
            patterns.append(Pattern(
                pattern_id=f"quality_{int(time.time())}",
                type=PatternType.REGRESSION,
                name="QA regression trend",
                description=f"{len(qa_failed)} executions failed QA",
                confidence=0.7,
                detection_method="qa_failure_count",
                affected_areas=["qa_gate", "quality"],
                examples=[{"task_id": e.get("task_id"), "qa_feedback": e.get("qa_feedback")} for e in qa_failed[:3]]
            ))

        return patterns

    # ────────────── Correlation patterns ──────────────

    def detect_correlations(self, executions: List[Dict[str, Any]]) -> List[Pattern]:
        """Detect relationships between fields (e.g. error types per dept)."""
        patterns = []

        error_to_dept = defaultdict(set)
        for e in executions:
            if e.get("error"):
                error_to_dept[e["error"]].add(e.get("department", "unknown"))

        for error, depts in error_to_dept.items():
            if len(depts) >= 2:
                patterns.append(Pattern(
                    pattern_id=f"corr_{int(time.time())}_{error[:12]}",
                    type=PatternType.CORRELATION,
                    name=f"Error affectmultiple departments",
                    description=f"'{error}' affects {sorted(depts)}",
                    confidence=0.75,
                    detection_method="error_dept_crossing",
                    affected_areas=list(depts),
                    examples=[{"error": error, "departments": sorted(depts)}]
                ))

        return patterns

    # ────────────── Meta / helpers ──────────────

    def register_custom_detector(self, name: str, detector: callable):
        """Register a custom detector function for domain-specific patterns."""
        self.custom_detectors[name] = detector

    def detect_all(self, executions: List[Dict[str, Any]]) -> List[Pattern]:
        """Run all built-in detectors against a dataset."""
        all_patterns = []
        all_patterns.extend(self.detect_performance(executions))
        all_patterns.extend(self.detect_failures(executions))
        all_patterns.extend(self.detect_quality_loss(executions))
        all_patterns.extend(self.detect_correlations(executions))
        return all_patterns

    @staticmethod
    def deduplicate(patterns: List[Pattern], by: str = "name") -> List[Pattern]:
        """Deduplicate patterns by a field, keeping the highest confidence."""
        ranked = defaultdict(list)
        for pattern in patterns:
            key = getattr(pattern, by, str(pattern.pattern_id))
            ranked[key].append(pattern)

        result = []
        for _, group in ranked.items():
            result.append(max(group, key=lambda p: p.confidence))
        return result


def main():
    """Test the Pattern Detector."""
    detector = PatternDetector()
    sample = [
        {"task_id": "t1", "department": "engineering", "duration": 120, "error": "timeout", "qa_passed": False},
        {"task_id": "t2", "department": "engineering", "duration": 90, "error": "timeout", "qa_passed": False},
        {"task_id": "t3", "department": "engineering", "duration": 200, "error": "timeout", "qa_passed": False},
        {"task_id": "t4", "department": "media", "duration": 15, "qa_passed": True},
    ]
    for pattern in detector.detect_all(sample):
        print(pattern.to_dict())


if __name__ == "__main__":
    main()