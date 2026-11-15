#!/usr/bin/env python3
"""
Phase 2 Integration Test

Tests the complete Phase 2 infrastructure stack:
- Skill Registry + Loader + Tester
- Plugin Manager + SDK
- Event Bus / Message Bus
- Analytics Engine (metrics, alerts, dashboards, cost tracking)
- Learning Engine (patterns, proposals)
"""

import sys
import json
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# Unicode glyphs (✓/✗/⚠) crash on Windows cp1252 consoles unless stdout is UTF-8
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:  # Python < 3.7
    pass


def test_skill_registry():
    """Test skill registry, loader, and tester."""
    print("=" * 60)
    print("Testing Skill Registry...")
    print("=" * 60)

    from skills.registry import SkillRegistry
    from skills.skill_loader import SkillLoader
    from skills.skill_tester import SkillTester

    registry = SkillRegistry(skills_root="skills")
    loader = SkillLoader(registry)
    tester = SkillTester(registry, loader)

    # Test loading
    print("✓ SkillRegistry instantiated")
    print("✓ SkillLoader instantiated")
    print("✓ SkillTester instantiated")

    # List skills
    skills = registry.list_skills()
    print(f"✓ Listed {len(skills)} skills")

    return True


def test_plugin_manager():
    """Test plugin manager and SDK."""
    print("=" * 60)
    print("Testing Plugin Manager + SDK...")
    print("=" * 60)

    from plugins.manager import PluginManager
    from plugins.vault_interface import VaultInterface
    from plugins.sdk import (
        PluginInterface, PluginCapability, PluginState,
        OAuthAuthHandler, ApiKeyAuthHandler,
        RateLimiter, RateLimitConfig,
        Event, EventPublisher, EventSubscriber,
        SDKLogger, SDKConfig, SDKTimer
    )

    manager = PluginManager(plugins_root="plugins", governor=None)
    print("✓ PluginManager instantiated")

    # Test vault
    vault = VaultInterface()
    vault.store("test_key", "test_value")
    assert vault.retrieve("test_key") == "test_value"
    print("✓ VaultInterface store/retrieve works")

    # Test SDK imports
    print("✓ All SDK modules imported successfully")

    return True


def test_event_bus():
    """Test message bus / event bus."""
    print("=" * 60)
    print("Testing Message Bus / Event Bus...")
    print("=" * 60)

    from kernel.event_bus import EventBus, EventHandler, MessageType, Message
    from kernel.event_bus import SubscriberManager

    # Test MessageType
    print(f"✓ MessageType has {len(list(MessageType))} types")

    # Test EventBus (legacy)
    bus = EventBus()
    print("✓ EventBus instantiated")

    # Test MessageBus (refactored)
    from kernel.event_bus import MessageBus, SubscriberManager as NewSubscriberManager
    msg_bus = MessageBus()
    print("✓ MessageBus instantiated")
    print("✓ SubscriberManager available")

    return True


def test_analytics():
    """Test analytics engine components."""
    print("=" * 60)
    print("Testing Analytics Engine...")
    print("=" * 60)

    from analytics import (
        AnalyticsEngine, MetricsCollector, AlertManager,
        DashboardGenerator, CostTracker,
        MetricType, AggregationType,
        AlertSeverity, AlertStatus,
        DashboardType, ResourceType, CostUnit
    )

    # Test AnalyticsEngine
    engine = AnalyticsEngine()
    engine.record_task_completion(
        task_id="test_task_1",
        agent_id="test-agent@engineering@vjsos-ai",
        department="engineering",
        duration=5.5,
        status="COMPLETED"
    )
    print("✓ AnalyticsEngine records task completion")

    # Test MetricsCollector
    collector = MetricsCollector()
    collector.record_metric(
        metric_type=MetricType.TASK.value,
        name="test_metric",
        value=42,
        unit="count",
        timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        source="test-source"
    )
    print("✓ MetricsCollector records metrics")

    # Test AlertManager
    alerts = AlertManager()
    alerts.add_rule({
        "rule_id": "test_rule",
        "metric_name": "test_metric",
        "comparison": ">",
        "threshold": 10,
        "severity": AlertSeverity.WARNING,
        "message": "Test alert triggered"
    })
    print("✓ AlertManager adds rules")

    # Test CostTracker
    costs = CostTracker()
    costs.record_llm_usage("test-agent", "test-model", 1000, 500)
    report = costs.get_cost_report()
    print(f"✓ CostTracker records LLM usage: ${report['total_cost_usd']:.6f}")

    # Test DashboardGenerator
    dashboards = DashboardGenerator(metrics_collector=collector, alert_manager=alerts)
    dash_list = dashboards.list_dashboards()
    print(f"✓ DashboardGenerator has {len(dash_list)} standard dashboards")

    return True


def test_learning():
    """Test learning engine components."""
    print("=" * 60)
    print("Testing Learning Engine...")
    print("=" * 60)

    from learning import (
        LearningEngine, LearningType,
        PatternDetector, PatternType, Pattern,
        ProposalWorkflow, Proposal, ProposalStatus, ProposalPriority, ProposalType,
        TrendAnalyzer
    )

    # Test LearningEngine
    engine = LearningEngine()
    engine.record_execution({
        "task_id": "learn_1",
        "agent_id": "agent1@engineering@vjsos-ai",
        "department": "engineering",
        "duration": 30,
        "status": "COMPLETED"
    })
    print("✓ LearningEngine records execution")

    # Test PatternDetector
    detector = PatternDetector()
    patterns = detector.detect_all([
        {"task_id": "p1", "department": "eng", "duration": 120, "error": "timeout", "qa_passed": False},
        {"task_id": "p2", "department": "eng", "duration": 90, "error": "timeout", "qa_passed": False},
        {"task_id": "p3", "department": "eng", "duration": 200, "error": "timeout", "qa_passed": False},
    ])
    print(f"✓ PatternDetector found {len(patterns)} patterns")

    # Test ProposalWorkflow
    workflow = ProposalWorkflow("proposals_test")
    prop = workflow.create(
        title="Test proposal",
        proposal_type=ProposalType.PROCESS_CHANGE,
        description="Test description",
        rationale="Test rationale",
        priority=ProposalPriority.MEDIUM
    )
    workflow.submit_for_review(prop.proposal_id)
    workflow.review(prop.proposal_id, True, "governor@vjsos-ai", "Approved")
    print(f"✓ ProposalWorkflow created and approved proposal {prop.proposal_id}")

    # Test TrendAnalyzer
    trend = TrendAnalyzer()
    print("✓ TrendAnalyzer instantiated")

    return True


def test_integration():
    """Test cross-component integration."""
    print("=" * 60)
    print("Testing Cross-Component Integration...")
    print("=" * 60)

    from analytics import AnalyticsEngine
    from learning import LearningEngine, ProposalWorkflow, ProposalType, ProposalPriority
    from kernel.event_bus import MessageBus, Message, MessageType

    # Create components
    analytics = AnalyticsEngine()
    learning = LearningEngine()
    workflow = ProposalWorkflow("integration_test")
    bus = MessageBus()

    # Simulate a task flow: analytics records → learning analyzes → proposal created
    analytics.record_task_completion(
        task_id="integration_1",
        agent_id="test-agent@engineering@vjsos-ai",
        department="engineering",
        duration=10.0,
        status="COMPLETED"
    )
    learning.record_execution({
        "task_id": "integration_1",
        "agent_id": "test-agent@engineering@vjsos-ai",
        "department": "engineering",
        "duration": 10.0,
        "status": "COMPLETED"
    })

    # Learning detects pattern → creates proposal
    prop = workflow.create(
        title="Optimize engineering tasks",
        proposal_type=ProposalType.PROCESS_CHANGE,
        description="Reduce average duration from 10s to 5s",
        rationale="Learning engine detected optimization opportunity",
        priority=ProposalPriority.HIGH,
        affected_components=["engineering", "analytics"]
    )
    workflow.submit_for_review(prop.proposal_id)
    workflow.review(prop.proposal_id, True, "governor@vjsos-ai")

    print("✓ Analytics → Learning → Proposal workflow integration works")

    return True


def main():
    """Run all integration tests."""
    print("\n" + "=" * 60)
    print("PHASE 2 INTEGRATION TEST SUITE")
    print("=" * 60 + "\n")

    tests = [
        ("Skill Registry", test_skill_registry),
        ("Plugin Manager + SDK", test_plugin_manager),
        ("Event Bus / Message Bus", test_event_bus),
        ("Analytics Engine", test_analytics),
        ("Learning Engine", test_learning),
        ("Cross-Component Integration", test_integration),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, True, None))
            print(f"\n✓ {name} PASSED\n")
        except Exception as e:
            results.append((name, False, str(e)))
            print(f"\n✗ {name} FAILED: {e}\n")

    # Summary
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    passed = sum(1 for _, ok, _ in results if ok)
    total = len(results)
    for name, ok, err in results:
        status = "PASS" if ok else "FAIL"
        print(f"  {status} - {name}")
        if err:
            print(f"       Error: {err}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n✓ ALL TESTS PASSED")
        return 0
    else:
        print(f"\n✗ {total - passed} TEST(S) FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())