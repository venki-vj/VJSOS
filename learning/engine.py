#!/usr/bin/env python3
"""
Learning Engine - Post-Mortem Analysis and Continuous Improvement

Collects, analyzes, and learns from past execution:
- Task outcome analysis and pattern recognition
- Performance trend detection and optimization recommendations
- Knowledge base updates and skill refinement
- Root cause analysis for failures
- Continuous improvement recommendations

Analyzes all processed events and results to improve future performance.
"""

import json
import time
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple, Set
from collections import defaultdict, Counter, deque
from dataclasses import dataclass, asdict
from enum import Enum
import statistics
import re
from itertools import combinations


class LearningType(Enum):
    PERFORMANCE_OPTIMIZATION = "performance_optimization"
    SKILL_REFLECTION = "skill_reflection"
    PROCESS_IMPROVEMENT = "process_improvement"
    KNOWLEDGE_UPDATING = "knowledge_updating"
    FAILURE_ANALYSIS = "failure_analysis"
    PATTERN_RECOGNITION = "pattern_recognition"


@dataclass
class LearningPattern:
    """Identified learning pattern from past executions."""
    pattern_id: str
    type: str
    description: str
    correlation_score: float  # 0.0 - 1.0
    examples: List[Dict[str, Any]]
    confidence: float
    recommendations: List[str]
    affected_areas: List[str]


@dataclass
class ImprovementSuggestion:
    """Suggestion for improvement based on learning."""
    suggestion_id: str
    type: str
    priority: str  # low, medium, high, critical
    title: str
    description: str
    affected_components: List[str]
    expected_impact: Dict[str, Any]
    implementation_effort: str  # simple, moderate, complex
    confidence: float
    status: str = "pending"  # pending, in_progress, implemented, tested, rejected


@dataclass
class PostMortemAnalysis:
    """Analysis of a failed or problematic task."""
    analysis_id: str
    task_id: str
    timestamp: str
    root_causes: List[str]
    contributing_factors: Dict[str, float]
    recovery_actions: List[str]
    lessons_learned: List[str]
    prevention_strategies: List[str]
    knowledge_base_updates: List[str]


class LearningEngine:
    """Learning engine for continuous improvement and knowledge accumulation."""

    def __init__(self):
        self.engine_id = "learning-engine@vjsos-ai"
        self.patterns: Dict[str, LearningPattern] = {}
        self.improvements: Dict[str, ImprovementSuggestion] = {}
        self.postmortems: List[PostMortemAnalysis] = []
        self.knowledge_base: Dict[str, Any] = {
            "successful_patterns": [],
            "common_failures": [],
            "optimization_opportunities": [],
            "skill_improvements": []
        }
        self.execution_history: deque = deque(maxlen=10000)
        self.trend_analyzer = TrendAnalyzer()
        self.pattern_detector = PatternDetector()

    def record_execution(self, execution_data: Dict[str, Any]):
        """Record execution for learning analysis."""
        self.execution_history.append({
            **execution_data,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })

    def analyze_performance(self, time_window_hours: int = 24) -> Dict[str, Any]:
        """Analyze performance trends and identify improvement opportunities."""
        cutoff_time = datetime.utcnow() - timedelta(hours=time_window_hours)
        cutoff_timestamp = cutoff_time.isoformat() + "Z"

        recent_executions = [
            exec_data for exec_data in self.execution_history
            if exec_data.get("timestamp", "") >= cutoff_timestamp
        ]

        if not recent_executions:
            return {
                "analysis_id": f"perf_analysis_{int(time.time())}",
                "status": "no_data",
                "message": "No execution data available for analysis"
            }

        # Analyze trends
        trend_analysis = self.trend_analyzer.analyze(recent_executions)

        # Detect performance patterns
        patterns = self.pattern_detector.detect_performance_patterns(recent_executions)

        # Generate improvement suggestions
        suggestions = self._generate_improvement_suggestions(recent_executions, patterns)

        # Update knowledge base
        self._update_knowledge_base(recent_executions, patterns, suggestions)

        return {
            "analysis_id": f"perf_analysis_{int(time.time())}",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "time_window_hours": time_window_hours,
            "status": "completed",
            "executions_analyzed": len(recent_executions),
            "trends": trend_analysis,
            "patterns": [asdict(p) for p in patterns],
            "improvements": [asdict(i) for i in suggestions],
            "summary": self._generate_summary(trend_analysis, patterns, suggestions)
        }

    def analyze_failures(self, time_window_hours: int = 72) -> Dict[str, Any]:
        """Analyze failures and conduct root cause analysis."""
        cutoff_time = datetime.utcnow() - timedelta(hours=time_window_hours)
        cutoff_timestamp = cutoff_time.isoformat() + "Z"

        failed_executions = [
            exec_data for exec_data in self.execution_history
            if exec_data.get("timestamp", "") >= cutoff_timestamp
            and exec_data.get("status") not in ["COMPLETED", "APPROVED"]
        ]

        if not failed_executions:
            return {
                "analysis_id": f"failure_analysis_{int(time.time())}",
                "status": "no_failures",
                "message": "No failed executions in the specified time window"
            }

        # Conduct post-mortem analysis for each failure
        postmortems = []
        for execution in failed_executions:
            analysis = self._conduct_post_mortem(execution)
            postmortems.append(analysis)

        # Aggregate failure patterns
        failure_patterns = self.pattern_detector.detect_failure_patterns(failed_executions)

        # Generate prevention strategies
        prevention_strategies = self._generate_prevention_strategies(failure_patterns)

        return {
            "analysis_id": f"failure_analysis_{int(time.time())}",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "time_window_hours": time_window_hours,
            "status": "completed",
            "failed_executions": len(failed_executions),
            "postmortems": [asdict(p) for p in postmortems],
            "failure_patterns": [asdict(p) for p in failure_patterns],
            "prevention_strategies": prevention_strategies,
            "root_causes": self._aggregate_root_causes(postmortems)
        }

    def reflect_on_skills(self, department: Optional[str] = None) -> Dict[str, Any]:
        """Analyze skill performance and provide reflection insights."""
        recent_executions = [
            exec_data for exec_data in self.execution_history
            if exec_data.get("department") == department or not department
        ]

        if not recent_executions:
            return {
                "analysis_id": f"skill_reflection_{int(time.time())}",
                "status": "no_data",
                "message": "No skill execution data available"
            }

        # Analyze skill performance by department
        skill_performance = self._analyze_skill_performance(recent_executions, department)

        # Identify skill improvement opportunities
        improvement_opportunities = self._identify_skill_improvements(recent_executions, department)

        # Generate skill refinement recommendations
        skill_refinements = self._generate_skill_refinements(skill_performance, improvement_opportunities)

        return {
            "analysis_id": f"skill_reflection_{int(time.time())}",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "department": department,
            "status": "completed",
            "executions_analyzed": len(recent_executions),
            "skill_performance": skill_performance,
            "improvement_opportunities": improvement_opportunities,
            "skill_refinements": skill_refinements,
            "recommendations": self._generate_skill_recommendations(skill_performance, improvement_opportunities)
        }

    def update_knowledge_base(self, execution_data: Dict[str, Any]):
        """Update the knowledge base with new learnings."""
        self.record_execution(execution_data)

        # Extract knowledge from successful executions
        if execution_data.get("status") == "COMPLETED":
            self._extract_success_patterns(execution_data)

        # Extract knowledge from failed executions
        elif execution_data.get("status") not in ["COMPLETED", "APPROVED"]:
            self._extract_failure_patterns(execution_data)

        # Extract optimization opportunities
        self._extract_optimization_opportunities(execution_data)

        # Generate and store improvement suggestions
        self._generate_and_store_improvements(execution_data)

    def get_knowledge_base(self) -> Dict[str, Any]:
        """Get the current knowledge base."""
        return {
            "knowledge_base": self.knowledge_base,
            "patterns_count": len(self.patterns),
            "improvements_count": len(self.improvements),
            "postmortems_count": len(self.postmortems),
            "last_updated": datetime.utcnow().isoformat() + "Z"
        }

    def get_improvements(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get improvement suggestions with optional status filter."""
        improvements = list(self.improvements.values())

        if status:
            improvements = [i for i in improvements if i.status == status]

        return [asdict(i) for i in improvements]

    def update_improvement_status(self, suggestion_id: str, status: str) -> Dict[str, Any]:
        """Update the status of an improvement suggestion."""
        if suggestion_id in self.improvements:
            self.improvements[suggestion_id].status = status
            return {
                "success": True,
                "suggestion_id": suggestion_id,
                "new_status": status,
                "updated_at": datetime.utcnow().isoformat() + "Z"
            }

        return {
            "success": False,
            "error": f"Improvement suggestion not found: {suggestion_id}"
        }

    # === Internal Analysis Methods ===

    def _conduct_post_mortem(self, execution: Dict[str, Any]) -> PostMortemAnalysis:
        """Conduct detailed post-mortem analysis for a failed execution."""
        analysis_id = f"pm_{execution.get('task_id', 'unknown')}_{int(time.time())}"

        # Extract contributing factors
        contributing_factors = self._extract_contributing_factors(execution)

        # Identify root causes
        root_causes = self._identify_root_causes(execution, contributing_factors)

        # Determine recovery actions that were taken
        recovery_actions = self._extract_recovery_actions(execution)

        # Derive lessons learned
        lessons_learned = self._derive_lessons_learned(execution, root_causes)

        # Formulate prevention strategies
        prevention_strategies = self._formulate_prevention_strategies(root_causes, lessons_learned)

        # Identify knowledge base updates
        knowledge_base_updates = self._identify_knowledge_base_updates(execution, root_causes)

        return PostMortemAnalysis(
            analysis_id=analysis_id,
            task_id=execution.get("task_id", "unknown"),
            timestamp=datetime.utcnow().isoformat() + "Z",
            root_causes=root_causes,
            contributing_factors=contributing_factors,
            recovery_actions=recovery_actions,
            lessons_learned=lessons_learned,
            prevention_strategies=prevention_strategies,
            knowledge_base_updates=knowledge_base_updates
        )

    def _extract_contributing_factors(self, execution: Dict[str, Any]) -> Dict[str, float]:
        """Extract factors that contributed to execution outcome."""
        factors = {}

        # Analyze execution data for contributing factors
        duration = execution.get("duration", 0)
        department = execution.get("department")
        status = execution.get("status")

        # Time-based factors
        if duration > 60:  # > 1 minute
            factors["long_duration"] = min(duration / 60, 1.0)

        # Department-specific factors
        if department:
            factors["department_specific_issues"] = 0.5  # Placeholder

        # Error factors
        if "error" in execution:
            factors["error_impact"] = 0.8

        return factors

    def _identify_root_causes(self, execution: Dict[str, Any], contributing_factors: Dict[str, float]) -> List[str]:
        """Identify root causes from execution data."""
        root_causes = []

        if execution.get("status") not in ["COMPLETED", "APPROVED"]:
            root_causes.extend([
                "Execution constraints not met",
                "Quality thresholds not achieved"
            ])

        if execution.get("duration", 0) > 30:
            root_causes.append("Performance bottleneck - slow execution")

        if "error" in execution:
            root_causes.append(f"Error: {execution['error']}")

        if not root_causes:
            root_causes.append("Unknown factors - requires deeper investigation")

        return root_causes

    def _extract_recovery_actions(self, execution: Dict[str, Any]) -> List[str]:
        """Extract recovery actions taken during execution."""
        actions = []

        if execution.get("feedback_cycles", 0) > 0:
            actions.append(f"Applied {execution['feedback_cycles']} feedback cycles")

        if "recovery_actions" in execution:
            actions.extend(execution["recovery_actions"])

        if not actions:
            actions.append("No explicit recovery actions recorded")

        return actions

    def _derive_lessons_learned(self, execution: Dict[str, Any], root_causes: List[str]) -> List[str]:
        """Derive lessons learned from execution analysis."""
        lessons = []

        for cause in root_causes:
            if "performance" in cause.lower():
                lessons.append("Performance optimization needed for similar tasks")
            elif "error" in cause.lower():
                lessons.append("Error handling needs improvement")
            elif "constraint" in cause.lower():
                lessons.append("Task constraints need better definition")

        if not lessons:
            lessons.append("Execute again with improved parameters")

        return lessons

    def _formulate_prevention_strategies(self, root_causes: List[str], lessons_learned: List[str]) -> List[str]:
        """Formulate strategies to prevent similar issues."""
        strategies = []

        for cause in root_causes:
            if "performance" in cause.lower():
                strategies.append("Add performance monitoring and early warnings")
            elif "error" in cause.lower():
                strategies.append("Implement better error handling and recovery")

        for lesson in lessons_learned:
            if "constraint" in lesson.lower():
                strategies.append("Improve task definition and parameter validation")

        if not strategies:
            strategies.append("Review and improve execution parameters")

        return strategies

    def _identify_knowledge_base_updates(self, execution: Dict[str, Any], root_causes: List[str]) -> List[str]:
        """Identify what needs to be updated in the knowledge base."""
        updates = []

        for cause in root_causes:
            if "performance" in cause.lower():
                updates.append("performance_benchmarks")
            elif "error" in cause.lower():
                updates.append("error_handling_procedures")
            elif "constraint" in cause.lower():
                updates.append("task_parameter_validation")

        if not updates:
            updates.append("general_execution_patterns")

        return updates

    def _analyze_skill_performance(self, executions: List[Dict[str, Any]], department: Optional[str]) -> Dict[str, Any]:
        """Analyze skill performance across executions."""
        performance_by_dept = defaultdict(list)

        for execution in executions:
            if not department or execution.get("department") == department:
                performance_by_dept[execution.get("department", "unknown")].append(execution)

        skill_performance = {}

        for dept, dept_executions in performance_by_dept.items():
            if dept_executions:
                completed = [e for e in dept_executions if e.get("status") == "COMPLETED"]
                avg_duration = statistics.mean([e.get("duration", 0) for e in dept_executions])
                success_rate = len(completed) / len(dept_executions) if dept_executions else 0

                skill_performance[dept] = {
                    "total_executions": len(dept_executions),
                    "successful_executions": len(completed),
                    "success_rate": success_rate,
                    "average_duration": avg_duration,
                    "average_feedback_cycles": statistics.mean([e.get("feedback_cycles", 0) for e in dept_executions]) if dept_executions else 0
                }

        return skill_performance

    def _identify_skill_improvements(self, executions: List[Dict[str, Any]], department: Optional[str]) -> List[Dict[str, Any]]:
        """Identify opportunities for skill improvement."""
        improvements = []

        # Analyze patterns of low performance
        for execution in executions:
            if execution.get("duration", 0) > 60 and execution.get("status") == "COMPLETED":
                improvements.append({
                    "type": "performance",
                    "description": f"Task took {execution.get('duration', 0)} seconds - performance optimization needed",
                    "department": execution.get("department"),
                    "severity": "medium"
                })

        return improvements

    def _generate_skill_refinements(self, skill_performance: Dict[str, Any], improvement_opportunities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate specific skill refinement recommendations."""
        refinements = []

        for dept, perf in skill_performance.items():
            if perf["success_rate"] < 0.8:
                refinements.append({
                    "department": dept,
                    "recommendation": "Improve success rate through better input validation",
                    "expected_improvement": "+15% success rate",
                    "effort": "moderate"
                })

            if perf["average_duration"] > 30:
                refinements.append({
                    "department": dept,
                    "recommendation": "Optimize execution time for better performance",
                    "expected_improvement": "-30% execution time",
                    "effort": "high"
                })

        return refinements

    def _generate_skill_recommendations(self, skill_performance: Dict[str, Any], improvement_opportunities: List[Dict[str, Any]]) -> List[str]:
        """Generate high-level skill recommendations."""
        recommendations = []

        for dept, perf in skill_performance.items():
            if perf["success_rate"] < 0.7:
                recommendations.append(f"{dept}: Focus on improving success rate through better error handling")

            if perf["average_feedback_cycles"] > 2:
                recommendations.append(f"{dept}: Reduce feedback cycles by improving initial quality")

        if not recommendations:
            recommendations.append("All departments performing well - focus on continuous optimization")

        return recommendations

    def _extract_success_patterns(self, execution: Dict[str, Any]):
        """Extract patterns from successful executions."""
        success_pattern = {
            "task_id": execution.get("task_id"),
            "department": execution.get("department"),
            "duration": execution.get("duration", 0),
            "feedback_cycles": execution.get("feedback_cycles", 0),
            "timestamp": execution.get("timestamp"),
            "success_factors": self._identify_success_factors(execution)
        }
        self.knowledge_base["successful_patterns"].append(success_pattern)

        # Keep only recent patterns
        if len(self.knowledge_base["successful_patterns"]) > 100:
            self.knowledge_base["successful_patterns"] = self.knowledge_base["successful_patterns"][-50:]

    def _extract_failure_patterns(self, execution: Dict[str, Any]):
        """Extract patterns from failed executions."""
        failure_pattern = {
            "task_id": execution.get("task_id"),
            "department": execution.get("department"),
            "error": execution.get("error", ""),
            "timestamp": execution.get("timestamp"),
            "failure_indicators": self._identify_failure_indicators(execution)
        }
        self.knowledge_base["common_failures"].append(failure_pattern)

        # Keep only recent patterns
        if len(self.knowledge_base["common_failures"]) > 50:
            self.knowledge_base["common_failures"] = self.knowledge_base["common_failures"][-25:]

    def _extract_optimization_opportunities(self, execution: Dict[str, Any]):
        """Extract optimization opportunities from executions."""
        if execution.get("duration", 0) > 30:
            opportunity = {
                "type": "performance",
                "task_id": execution.get("task_id"),
                "current_duration": execution.get("duration", 0),
                "potential_improvement": "significant",
                "timestamp": execution.get("timestamp")
            }
            self.knowledge_base["optimization_opportunities"].append(opportunity)

        # Keep only recent opportunities
        if len(self.knowledge_base["optimization_opportunities"]) > 20:
            self.knowledge_base["optimization_opportunities"] = self.knowledge_base["optimization_opportunities"][-10:]

    def _generate_improvement_suggestions(self, executions: List[Dict[str, Any]], patterns: List[LearningPattern]) -> List[ImprovementSuggestion]:
        """Generate improvement suggestions based on analysis."""
        suggestions = []

        # Check for common performance issues
        slow_executions = [e for e in executions if e.get("duration", 0) > 60]
        if len(slow_executions) / len(executions) > 0.2:  # > 20% slow
            suggestion_id = f"imp_{int(time.time())}_performance"
            suggestions.append(ImprovementSuggestion(
                suggestion_id=suggestion_id,
                type="performance_optimization",
                priority="high",
                title="Optimize Slow Task Performance",
                description=f"Analysis shows {len(slow_executions) / len(executions) * 100:.0f}% of tasks exceed 60 seconds",
                affected_components=["orchestrator", "agent_execution"],
                expected_impact={"performance_improvement": "30-50% reduction in execution time"},
                implementation_effort="complex",
                confidence=0.8,
                status="pending"
            ))

        # Check for high feedback cycles
        high_feedback_executions = [e for e in executions if e.get("feedback_cycles", 0) > 2]
        if len(high_feedback_executions) / len(executions) > 0.3:  # > 30% need multiple feedback cycles
            suggestion_id = f"imp_{int(time.time())}_quality"
            suggestions.append(ImprovementSuggestion(
                suggestion_id=suggestion_id,
                type="quality_improvement",
                priority="medium",
                title="Improve Initial Task Quality",
                description=f"{len(high_feedback_executions) / len(executions) * 100:.0f}% of tasks require multiple feedback cycles",
                affected_components=["qa_engine", "agent_initialization"],
                expected_impact={"quality_improvement": "40% reduction in feedback cycles"},
                implementation_effort="moderate",
                confidence=0.7,
                status="pending"
            ))

        return suggestions

    def _update_knowledge_base(self, executions: List[Dict[str, Any]], patterns: List[LearningPattern], suggestions: List[ImprovementSuggestion]):
        """Update knowledge base with new learnings."""
        # Add new patterns
        for pattern in patterns:
            if pattern.pattern_id not in self.patterns:
                self.patterns[pattern.pattern_id] = pattern

        # Add new improvement suggestions
        for suggestion in suggestions:
            if suggestion.suggestion_id not in self.improvements:
                self.improvements[suggestion.suggestion_id] = suggestion

        # Keep knowledge base manageable
        if len(self.patterns) > 50:
            # Remove oldest patterns
            oldest_keys = sorted(self.patterns.keys())[:10]
            for key in oldest_keys:
                del self.patterns[key]

        if len(self.improvements) > 30:
            # Remove pending suggestions
            pending_keys = [k for k, v in self.improvements.items() if v.status == "pending"]
            for key in pending_keys[:10]:
                del self.improvements[key]

    def _generate_and_store_improvements(self, execution: Dict[str, Any]):
        """Generate and store improvements from a single execution."""
        # Simple heuristic-based improvement generation
        if execution.get("duration", 0) > 45:
            suggestion = ImprovementSuggestion(
                suggestion_id=f"imp_{execution.get('task_id', 'unknown')}_{int(time.time())}",
                type="performance_optimization",
                priority="medium",
                title="Reduce Task Execution Time",
                description=f"Task {execution.get('task_id', 'unknown')} took {execution.get('duration', 0)} seconds",
                affected_components=["agent_execution"],
                expected_impact={"performance_improvement": "25% reduction in execution time"},
                implementation_effort="simple",
                confidence=0.6,
                status="pending"
            )
            self.improvements[suggestion.suggestion_id] = suggestion

    def _generate_summary(self, trends: Dict[str, Any], patterns: List[LearningPattern], suggestions: List[ImprovementSuggestion]) -> str:
        """Generate human-readable analysis summary."""
        total_executions = sum(trend.get("count", 0) for trend in trends.get("trends", []))
        success_rate = trends.get("success_rate", 0)
        avg_duration = trends.get("average_duration", 0)

        summary = f"Analysis of {total_executions} executions: "

        if success_rate > 0.9:
            summary += "High success rate, "
        elif success_rate > 0.7:
            summary += "Moderate success rate, "
        else:
            summary += "Low success rate, "

        summary += f"average duration {avg_duration:.1f}s, "

        if len(patterns) > 0:
            summary += f"identified {len(patterns)} patterns. "

        if len(suggestions) > 0:
            critical_suggestions = [s for s in suggestions if s.priority == "critical"]
            if critical_suggestions:
                summary += f"{len(critical_suggestions)} critical improvement suggestions."
            else:
                summary += f"{len(suggestions)} improvement suggestions."
        else:
            summary += "No immediate improvement opportunities identified."

        return summary

    def _identify_success_factors(self, execution: Dict[str, Any]) -> List[str]:
        """Identify success factors from execution."""
        factors = []

        if execution.get("feedback_cycles", 0) <= 2:
            factors.append("Efficient feedback loop")

        if execution.get("duration", 0) < 30:
            factors.append("Fast execution")

        if execution.get("qa_status", "") == "APPROVED":
            factors.append("Quality approval achieved")

        return factors

    def _identify_failure_indicators(self, execution: Dict[str, Any]) -> List[str]:
        """Identify failure indicators from execution."""
        indicators = []

        if "error" in execution:
            indicators.append(f"Error: {execution['error']}")

        if execution.get("duration", 0) > 60:
            indicators.append("Slow execution")

        if execution.get("status") not in ["COMPLETED", "APPROVED"]:
            indicators.append("Failed quality check")

        return indicators

    def _aggregate_root_causes(self, postmortems: List[PostMortemAnalysis]) -> List[str]:
        """Aggregate root causes from multiple postmortems."""
        all_causes = []
        for postmortem in postmortems:
            all_causes.extend(postmortem.root_causes)

        # Count occurrences
        cause_counts = Counter(all_causes)

        # Return most common causes
        return [cause for cause, count in cause_counts.most_common(5)]

    def _generate_prevention_strategies(self, failure_patterns: List[LearningPattern]) -> List[str]:
        """Generate prevention strategies from failure patterns."""
        strategies = []

        for pattern in failure_patterns:
            if "performance" in pattern.type:
                strategies.append(f"Monitor and optimize for {pattern.description}")
            elif "quality" in pattern.type:
                strategies.append(f"Enhance quality checks to address {pattern.description}")

        if not strategies:
            strategies.append("Implement comprehensive testing for all new changes")

        return strategies


class TrendAnalyzer:
    """Analyze execution trends over time."""

    def analyze(self, executions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze execution trends."""
        if not executions:
            return {"status": "no_data"}

        # Calculate basic metrics
        success_rate = len([e for e in executions if e.get("status") == "COMPLETED"]) / len(executions)
        durations = [e.get("duration", 0) for e in executions if e.get("duration")]

        # Calculate trend (simplified linear regression)
        trend = self._calculate_trend([e.get("timestamp", "") for e in executions if e.get("timestamp")], durations)

        return {
            "success_rate": success_rate,
            "average_duration": statistics.mean(durations) if durations else 0,
            "duration_variance": statistics.variance(durations) if len(durations) > 1 else 0,
            "trend": trend,
            "total_executions": len(executions),
            "time_span_hours": self._calculate_time_span(executions)
        }

    def _calculate_trend(self, timestamps: List[str], durations: List[float]) -> str:
        """Calculate performance trend."""
        if len(durations) < 3:
            return "stable"

        # Simple trend calculation
        first_half = durations[:len(durations)//2]
        second_half = durations[len(durations)//2:]

        avg_first = statistics.mean(first_half) if first_half else 0
        avg_second = statistics.mean(second_half) if second_half else 0

        if avg_second < avg_first * 0.9:
            return "improving"
        elif avg_second > avg_first * 1.1:
            return "degrading"
        else:
            return "stable"

    def _calculate_time_span(self, executions: List[Dict[str, Any]]) -> float:
        """Calculate time span of executions."""
        if not executions:
            return 0

        timestamps = []
        for exec_data in executions:
            if "timestamp" in exec_data:
                try:
                    timestamp = datetime.fromisoformat(exec_data["timestamp"].replace("Z", "+00:00"))
                    timestamps.append(timestamp)
                except:
                    pass

        if not timestamps:
            return 0

        return (max(timestamps) - min(timestamps)).total_seconds() / 3600


class PatternDetector:
    """Detect patterns in execution data."""

    def detect_performance_patterns(self, executions: List[Dict[str, Any]]) -> List[LearningPattern]:
        """Detect performance-related patterns."""
        patterns = []

        # Group by department
        by_department = defaultdict(list)
        for execution in executions:
            dept = execution.get("department", "unknown")
            by_department[dept].append(execution)

        # Analyze each department
        for dept, dept_executions in by_department.items():
            if len(dept_executions) >= 3:
                durations = [e.get("duration", 0) for e in dept_executions if e.get("duration")]
                if durations and statistics.mean(durations) > 60:
                    pattern = LearningPattern(
                        pattern_id=f"perf_dept_{dept}_{int(time.time())}",
                        type="performance_optimization",
                        description=f"Department {dept} has high execution times",
                        correlation_score=0.7,
                        examples=[{"task_id": e.get("task_id"), "duration": e.get("duration")} for e in dept_executions[:3]],
                        confidence=0.8,
                        recommendations=["Optimize task execution", "Monitor slow tasks"],
                        affected_areas=[dept]
                    )
                    patterns.append(pattern)

        return patterns

    def detect_failure_patterns(self, executions: List[Dict[str, Any]]) -> List[LearningPattern]:
        """Detect failure patterns."""
        patterns = []

        # Look for common error patterns
        error_messages = [e.get("error", "") for e in executions if e.get("error")]
        if error_messages:
            common_errors = Counter(error_messages)
            most_common_error = common_errors.most_common(1)[0] if common_errors else None

            if most_common_error and most_common_error[1] >= 3:
                pattern = LearningPattern(
                    pattern_id=f"failure_error_{int(time.time())}",
                    type="failure_analysis",
                    description=f"Common error: {most_common_error[0]}",
                    correlation_score=0.9,
                    examples=[{"execution": i, "error": error} for i, error in enumerate(error_messages[:5])],
                    confidence=0.85,
                    recommendations=[f"Fix error: {most_common_error[0]}", "Add error handling"],
                    affected_areas=["error_handling", "input_validation"]
                )
                patterns.append(pattern)

        return patterns


def main():
    """Test the Learning Engine."""
    engine = LearningEngine()
    print("Testing Learning Engine...")

    # Record some test executions
    engine.record_execution({
        "task_id": "test_task_001",
        "department": "engineering",
        "duration": 5.2,
        "status": "COMPLETED",
        "feedback_cycles": 1,
        "qa_status": "APPROVED"
    })

    engine.record_execution({
        "task_id": "test_task_002",
        "department": "media",
        "duration": 45.8,
        "status": "COMPLETED",
        "feedback_cycles": 2,
        "qa_status": "APPROVED",
        "error": "timeout"
    })

    engine.record_execution({
        "task_id": "test_task_003",
        "department": "engineering",
        "duration": 120.5,
        "status": "FAILED",
        "feedback_cycles": 5,
        "qa_status": "REJECTED",
        "error": "resource_limit"
    })

    # Analyze performance
    perf_analysis = engine.analyze_performance(24)
    print(f"Performance Analysis: {json.dumps(perf_analysis, indent=2)}")

    # Analyze failures
    failure_analysis = engine.analyze_failures(72)
    print(f"\nFailure Analysis: {json.dumps(failure_analysis, indent=2)}")

    # Skill reflection
    skill_reflection = engine.reflect_on_skills("engineering")
    print(f"\nSkill Reflection: {json.dumps(skill_reflection, indent=2)}")

    # Knowledge base
    knowledge_base = engine.get_knowledge_base()
    print(f"\nKnowledge Base: {json.dumps(knowledge_base, indent=2)}")

    print("\nLearning Engine test completed!")


if __name__ == "__main__":
    main()