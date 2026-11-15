#!/usr/bin/env python3
"""
VJSOS-AI Phase 2 Integration Walkthrough — Terminal Recording Script
Run each function separately, record output, then edit together per VIDEO_PRODUCTION_PACKAGE.md

REQUIREMENTS:
- Terminal: 3840×2160 (or 1920×1080 @ 2x scale)
- Font: JetBrains Mono 14pt
- Theme: One Dark Pro
- Hide: title bar, scrollbar, tabs
- Record: OBS (lossless) or ffmpeg
"""

import subprocess
import sys
import time
from pathlib import Path

# ─── CONFIG ──────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).parent.parent
PYTHON = sys.executable

def run(cmd, description="", delay_after=1.0):
    """Run command, print description, return output."""
    print(f"\n{'='*60}")
    print(f"🎬 {description}")
    print(f"$ {cmd}")
    print(f"{'='*60}\n")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=REPO_ROOT)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    time.sleep(delay_after)
    return result

# ─── SEGMENT 1: COLD OPEN ────────────────────────────────────────
def segment_cold_open():
    run("git log --oneline -5", "Cold open: recent Phase 2 commits")

# ─── SEGMENT 2: ARCHITECTURE ─────────────────────────────────────
def segment_architecture():
    run("tree -L 3 skills plugins analytics learning kernel", "Architecture: file structure overview")

# ─── SEGMENT 3: SKILL REGISTRY ───────────────────────────────────
def segment_skills():
    run("python scripts/skills_cli.py list", "Skills: list all registered")
    run('python scripts/skills_cli.py register skills/engineering/android_development/skill.md', "Skills: register android_development")
    run("python scripts/skills_cli.py test android_development", "Skills: run test suite")
    run('python scripts/skills_cli.py prompt android_development --variables task="build login screen" platform="android"', "Skills: render prompt with variables")
    run("python scripts/skills_cli.py get android_development --json", "Skills: introspect skill (JSON)")

# ─── SEGMENT 4: PLUGIN MANAGER ───────────────────────────────────
def segment_plugins():
    run("python scripts/plugins_cli.py list", "Plugins: list (empty state)")
    run("python scripts/plugins_cli.py install plugins/github_integration/manifest.json --skip-governor", "Plugins: install github_integration")
    run("python scripts/plugins_cli.py enable github_integration", "Plugins: enable plugin")
    run("python -c \"from plugins.vault_interface import VaultInterface; v=VaultInterface(); v.store('github_token', 'ghp_demo', tags={'type':'oauth','env':'prod'}); print('Stored:', v.retrieve('github_token'))\"", "Plugins: VaultInterface demo")
    run("python scripts/plugins_cli.py review github_integration --approve --reviewer governor@vjsos-ai", "Plugins: Governor approval")
    run("python scripts/plugins_cli.py get github_integration --json", "Plugins: introspect (JSON)")

# ─── SEGMENT 5: MESSAGE BUS ──────────────────────────────────────
def segment_message_bus():
    # Run in two terminals (tmux split) — record both panes
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║  MESSAGE BUS: Requires TWO terminal panes (tmux split)       ║
    ║                                                              ║
    ║  PANE 1 (Subscriber):                                        ║
    ║  python -c \"                                                 ║
    ║  from kernel.event_bus import MessageBus, MessageType,       ║
    ║       EventHandler                                           ║
    ║  bus = MessageBus()                                          ║
    ║  bus.start()                                                 ║
    ║  class Handler(EventHandler):                                ║
    ║      async def handle(self, msg):                            ║
    ║          print(f'Received {msg.type} corr={msg.correlation_id}')\n    ║
    ║          print(f'  from {msg.sender} payload={msg.payload}')\n    ║
    ║  h = Handler()                                               ║
    ║  h.subscribe([MessageType.TASK_REQUEST])                     ║
    ║  import asyncio                                              ║
    ║  asyncio.run(bus.subscribe(h, ['task']))                     ║
    ║  \"                                                            ║
    ║                                                              ║
    ║  PANE 2 (Publisher — run AFTER subscriber shows 'ready'):    ║
    ║  python -c \"                                                 ║
    ║  from kernel.event_bus import MessageBus, Message, MessageType\↴\n    ║
    ║  bus = MessageBus()                                          ║
    ║  bus.start()                                                 ║
    ║  import asyncio                                              ║
    ║  asyncio.run(bus.publish(Message(                            ║
    ║      type=MessageType.TASK_REQUEST,                          ║
    ║      correlation_id='demo-1',                                ║
    ║      sender='orchestrator',                                  ║
    ║      recipient='android-agent',                              ║
    ║      payload={'task': 'build_apk'}                           ║
    ║  )))                                                         ║
    ║  \"                                                            ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

# ─── SEGMENT 6: ANALYTICS ENGINE ─────────────────────────────────
def segment_analytics():
    run("""
python -c "
from analytics import (
    AnalyticsEngine, MetricsCollector, AlertManager,
    CostTracker, DashboardGenerator,
    MetricType, AlertSeverity
)
e = AnalyticsEngine()
e.record_task_completion('t1', 'a@eng', 'engineering', 4.2, 'COMPLETED')
print('AnalyticsEngine: task recorded')

c = MetricsCollector()
c.record_metric(MetricType.TASK.value, 'duration', 4.2, 'seconds', 'eng-agent')
print('MetricsCollector: metric recorded')

a = AlertManager()
a.add_rule({
    'rule_id': 'high_latency',
    'metric_name': 'duration',
    'comparison': '>',
    'threshold': 10,
    'severity': AlertSeverity.CRITICAL
})
print('AlertManager: rule added')

ct = CostTracker()
ct.record_llm_usage('agent1', 'claude-3.5-sonnet', 5000, 2000)
report = ct.get_cost_report()
print(f'CostTracker: \${report[\"total_cost_usd\"]:.6f}')

d = DashboardGenerator()
dash = d.generate_department_dashboard('engineering')
print(f'DashboardGenerator: {dash[\"dashboard_id\"]}')

exec_dash = d.generate_executive_summary()
print(f'Executive Summary: {exec_dash[\"summary\"][\"total_tasks\"]} tasks')
"
""", "Analytics: full component demo")

# ─── SEGMENT 7: LEARNING ENGINE ──────────────────────────────────
def segment_learning():
    run("""
python -c "
from learning import (
    LearningEngine, PatternDetector,
    ProposalWorkflow, ProposalType, ProposalPriority
)
le = LearningEngine()
le.record_execution({
    'task_id': 't1', 'agent_id': 'a@eng',
    'department': 'engineering', 'duration': 120, 'status': 'COMPLETED'
})
print('LearningEngine: execution recorded')

pd = PatternDetector()
patterns = pd.detect_all([
    {'task_id': f't{i}', 'department': 'eng', 'duration': 120+i*10, 'error': 'timeout', 'qa_passed': False}
    for i in range(5)
])
print(f'PatternDetector: {len(patterns)} patterns found')
for p in patterns:
    print(f'  - {p.pattern_type.value}: confidence={p.confidence:.2f}')

pw = ProposalWorkflow('props')
p = pw.create(
    title='Fix timeouts',
    proposal_type=ProposalType.PROCESS_CHANGE,
    description='Increase timeout threshold',
    rationale='Pattern shows 80% timeout rate',
    priority=ProposalPriority.HIGH
)
print(f'ProposalWorkflow: created {p.proposal_id}')

pw.submit_for_review(p.proposal_id)
pw.review(p.proposal_id, True, 'governor@vjsos-ai', 'Approved')
prop = pw.get_proposal(p.proposal_id)
print(f'Proposal status: {prop.status.value}')
"
""", "Learning: full component demo")

# ─── SEGMENT 8: FULL INTEGRATION TEST (HERO SHOT) ────────────────
def segment_integration_test():
    run("python tests/test_phase2_integration.py", "HERO SHOT: Full integration test suite", delay_after=3.0)

# ─── SEGMENT 9: POST-TEST STATE ──────────────────────────────────
def segment_post_test():
    run("python scripts/skills_cli.py list", "Post-test: skills list")
    run("python scripts/plugins_cli.py list", "Post-test: plugins list")
    run("""
python -c "
from analytics import DashboardGenerator
d = DashboardGenerator()
exec_summary = d.generate_executive_summary()
import json
print(json.dumps(exec_summary, indent=2))
"
""", "Post-test: executive dashboard")
    run("""
python -c "
from learning import ProposalWorkflow
pw = ProposalWorkflow('props')
for p in pw.list_all():
    print(f'{p.proposal_id}: {p.title} [{p.status.value}]')
"
""", "Post-test: learning proposals")

# ─── MAIN ────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="VJSOS-AI Video Recording Segments")
    parser.add_argument("segment", choices=[
        "cold_open", "architecture", "skills", "plugins",
        "message_bus", "analytics", "learning",
        "integration_test", "post_test", "ALL"
    ], help="Which segment to run")
    args = parser.parse_args()

    segments = {
        "cold_open": segment_cold_open,
        "architecture": segment_architecture,
        "skills": segment_skills,
        "plugins": segment_plugins,
        "message_bus": segment_message_bus,
        "analytics": segment_analytics,
        "learning": segment_learning,
        "integration_test": segment_integration_test,
        "post_test": segment_post_test,
    }

    if args.segment == "ALL":
        for name, fn in segments.items():
            if name != "message_bus":  # manual
                print(f"\n{'#'*60}\n### RUNNING: {name.upper()}\n{'#'*60}")
                fn()
    else:
        segments[args.segment]()

    print("\n✅ Segment complete. Check recording.")