# VJSOS-AI Operating System Specification

**Version:** 1.0.0
**Status:** Draft
**Constitution Article:** IV, V, VII, VIII

---

## 1. Overview

The VJSOS-AI Operating System is a framework for building AI-native organizations. It provides the infrastructure for governed, scalable, high-quality AI work across departments, disciplines, and domains.

### System Architecture

```
                    VJSOS-AI OPERATING SYSTEM

                             USER
                               │
                  message_bus.request
                               │
                               ▼
                    ┌─────────────────────┐
                    │  SYSTEM GOVERNOR    │
                    │  (constitution)     │
                    └─────────────────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    ▼                     ▼
         ┌──────────────────┐  ┌──────────────────┐
         │  ORCHESTRATOR    │  │  CONTEXT ENGINE  │
         │  (task routing)  │  │  (min. context)  │
         └──────────────────┘  └──────────────────┘
                    │                     │
                    │              context_package
                    │                     │
                    ▼                     ▼
         ┌──────────────────────────────────────────┐
         │         DEPARTMENT ROUTERS               │
         │                                          │
         │  Engineering  Media  Business  Research   │
         │  Animation     Operations  Infra  Know.  │
         └──────────────────────────────────────────┘
                    │                     │
                    ▼                     ▼
         ┌──────────────────┐  ┌──────────────────┐
         │  WORKER AGENTS   │  │  QA AGENTS       │
         │  (specialists)   │  │  (verifiers)     │
         └──────────────────┘  └──────────────────┘
                    │                     │
                    │       feedback      │
                    └─────────┬───────────┘
                              ▼
                   ┌──────────────────┐
                   │  MEMORY ENGINE    │
                   │  (4-tier)         │
                   └──────────────────┘
                              │
                              ▼
                   ┌──────────────────┐
                   │  LEARNING ENGINE │
                   │  (post-mortems)   │
                   └──────────────────┘
                              │
                              ▼
                   ┌──────────────────┐
                   │  ANALYTICS       │
                   │  (metrics, ops)   │
                   └──────────────────┘
```

---

## 2. Core Components

### 2.1 System Governor

**Responsibilities:**
- Constitutional compliance enforcement
- Architectural integrity monitoring
- Conflict resolution
- Agent lifecycle approval
- Skill and memory governance
- Refactoring authorization
- Human override coordination

**Singleton.** All agents inherit its authority structure.

**See:** `docs/specs/KERNEL_SPEC.md#1-system-governor`

---

### 2.2 Orchestrator

**Responsibilities:**
- Intent analysis
- Task decomposition
- Department/agent selection
- Context package assembly
- QA gate enforcement
- Output aggregation
- Execution tracing

**Workflow:**
1. Receive request from user via message bus
2. Analyze intent → capability map
3. Select departments → agents
4. Request context package
5. Dispatch tasks with correlation_id
6. Collect → QA → (pass) aggregate | (fail) feedback loop
7. Return to user via message bus

**See:** `docs/specs/KERNEL_SPEC.md#2-orchestrator`

---

### 2.3 Context Engine

**Responsibilities:**
- Intent-to-knowledge mapping
- Relevance scoring
- Token-budget-aware context packaging
- Dependency resolution
- Context bloat prevention

**Key Principle:** Every agent receives only what it needs, when it needs it.

**See:** `docs/specs/KERNEL_SPEC.md#3-context-engine`

---

### 2.4 Memory Engine

**Four-tier Model:**

| Tier | Scope | Owner | TTL |
|------|-------|-------|-----|
| Session | Current conversation | Agent | 24h |
| Agent | Domain knowledge | Agent | 180d |
| Department | Domain patterns, SOPs | Department | ∞ |
| Global | Company vision, Constitution | Governor | ∞ |

**Features:**
- Deduplication (content + semantic)
- Embedding-based search
- Lifecycle enforcement
- Cross-linking and traceability

**See:** `docs/specs/KERNEL_SPEC.md#4-memory-engine`

---

### 2.5 QA Engine

**Responsibilities:**
- Quality verification (accuracy, completeness, documentation, tests, constitution compliance)
- Regression detection
- Feedback generation
- Verdict issuance

**Architecture:**
- Central QA Engine coordinates department-specific QA agents
- Each department QA enforces domain-specific rubrics
- All verifications logged and auditable
- Appeal path to Governor, not bypass

**See:** `docs/specs/KERNEL_SPEC.md#5-qa-engine`

---

### 2.6 Learning Engine

**Responsibilities:**
- Post-mortem analysis
- Pattern detection
- Skill improvement proposals
- Memory consolidation recommendations
- Process optimization suggestions

**Workflow:**
```
Task Completion
    ↓
QA Pass/Fail Record
    ↓
Learning Engine Analysis
    ↓
Pattern Detected? → Yes → Draft Improvement Proposal
    ↓                     (skill update, memory add, SOP change, new test)
    No
    ↓
Log to Insights
```

**Improvement Proposal Lifecycle:**
```
Draft → QA Review → Governor Approval → Scheduled → Deployed
```

**See:** `docs/specs/LEARNING_ENGINE_SPEC.md`

---

### 2.7 Analytics Engine

**Responsibilities:**
- KPI tracking per agent/department/system
- Performance metrics
- Quality metrics
- Cost metrics
- Error tracking

**Dashboard:** `analytics/` contains metric definitions; dashboards rendered in UI.

**See:** `docs/specs/ANALYTICS_ENGINE_SPEC.md`

---

## 3. Department Framework

### 3.1 Department Lifecycle

```
Proposal (RFC)
    ↓
Governor Approval
    ↓
Department Director Creation
    ↓
Agent Registration
    ↓
Skill Assignment
    ↓
Memory Initialization
    ↓
QA Setup
    ↓
Operational
```

### 3.2 Department Manifest (`departments/{name}/MANIFEST.md`)

```yaml
department_id: "engineering"
director: "director-engineering@vjsos-ai"
mission: "Produce reliable, tested, documented software artifacts and infrastructure automation"
domains:
  - android
  - backend
  - architecture
  - automation
  - ci-cd
workers:
  - android-agent@vjsos-ai
  - backend-agent@vjsos-ai
  - architecture-agent@vjsos-ai
qa_agent: "qa-engineering@vjsos-ai"
skills:
  - android_development
  - backend_development
  - system_architecture
  - ci-cd_pipeline
memory_scope: "department"
sops: ["code_review", "testing_standard", "release_management"]
kpis:
  - tasks_completed_per_week
  - qa_pass_rate
  - defect_rate
  - mean_time_to_resolution
metrics_dashboard: "/dashboards/engineering"
```

---

## 4. Agent Framework

### 4.1 Agent Identity

Every agent has a canonical identity:
```
agent_id: {name}@{department}@{namespace}
type: worker | director | qa | singleton
tier: global | department | project | session
status: operational | deprecated | onboarding | suspended
```

Example: `android-agent@engineering@vjsos-ai`

### 4.2 Agent Lifecycle

```
Manifest Creation (Governor Approved)
    ↓
Onboarding
    ↓
QA Verification (rubric test)
    ↓
Operational
    ↓
Performance Monitoring
    ↓
(Deprecated | Suspended | Evolved)
```

### 4.3 Agent Manifest (`agents/{name}/{name}.md`)

```yaml
agent_id: "android-agent@engineering@vjsos-ai"
type: "worker"
department: "engineering"
director: "director-engineering@vjsos-ai"
mission: "Build, test, and maintain Android applications following VJSOS quality standards"
domains: ["android", "kotlin", "compose"]
skills:
  - android_development
  - debugging
  - anr_analysis
  - performance_optimization
  - testing
memory_scope: "agent"
inputs:
  - orchestrator dispatches
  - department announcements
  - qa feedback
outputs:
  - task_results
  - documentation
  - test artifacts
  - skill improvement_proposals
sla:
  response_time: "30s"
  task_completion: "4h"  # per typical task
  documentation: "100%"
qa_rubric: "engineering_qa_rubric_v2.0"
status: "operational"
version: "2.3.1"
dependencies: ["android-sdk@vjsos-ai", "ci-cd_pipeline@vjsos-ai"]
```

### 4.4 Agent Communication Rules (Article VII)

- **All messages** flow through the Orchestrator
- **No direct agent-to-agent calls** (except QA → worker for feedback)
- **Department directors** coordinate within their department through the Orchestrator
- **Escalations** go to Governor
- **System events** broadcast on message bus

---

## 5. Skill Framework

### 5.1 Skill as Package

Each skill is a self-contained capability package:

```
skills/
├── android/
│   ├── binder/
│   │   ├── skill.md       # manifest
│   │   ├── prompt.md      # implementation prompt
│   │   ├── tests/         # automated tests
│   │   ├── examples/      # reference examples
│   │   └── metadata.json  # version, owner, dependencies
│   ├── anr_analysis/
│   └── performance/
```

### 5.2 Skill Manifest (`skill.md`)

```yaml
skill_id: "anr_analysis"
version: "2.1.0"
owner: "android-agent@engineering@vjsos-ai"
domain: "android"
description: "Detects and analyzes Android Application Not Responding (ANR) conditions"
type: "analysis"
inputs:
  - stack_traces (required)
  - thread_dumps (required)
  - device_info (optional)
  - memory_snapshot (optional)
outputs:
  - anr_report (json)
    - root_cause (categorical)
    - deadlock_probability (0-1)
    - affected_threads (list)
    - fix_recommendation (structured)
examples:
  - example_001: "Stack trace indicating main thread blocked on disk I/O"
  - example_002: "Deadlocked threads in lock contention"
dependencies:
  - android_sdk:v21+
  - kotlin_coroutines:1.7+
tests:
  - test_positive_detection.yaml
  - test_false_positive_rate.yaml
  - test_output_format.yaml
qa_status: "verified"
last_reviewed: "2026-08-05"
changelog: |
  - v2.1.0: Added deadlock probability scoring
  - v2.0.0: Rewrote for Kotlin coroutines scope analysis
  - v1.0.0: Initial release
```

### 5.3 Skill Types

| Type | Description |
|------|-------------|
| `analysis` | Reads inputs, produces insight |
| `generation` | Produces new content (code, script, design) |
| `verification` | Tests or validates artifacts |
| `automation` | Executes repeatable procedures |
| `orchestration` | Coordinates multi-step workflows |
| `monitoring` | Continuously observes system state |

### 5.4 Skill Test Format

Every skill must have tests. Test format:

```
tests/test_{test_name}.yaml
```

```yaml
name: "ANR Detection — Main Thread Blocked on I/O"
skill: "anr_analysis"
version: "2.1.0"
input:
  stack_traces:
    - thread: "main"
      stack: "at java.io.FileInputStream.readBytes(Native Method), at java.io.FileInputStream.read(FileInputStream.java:...)"
  expected_root_cause: "disk_io_main_thread"
assertions:
  - assertion: "anr_report.root_cause == 'disk_io_main_thread'"
  - assertion: "anr_report.deadlock_probability < 0.1"
  - assertion: "anr_report.affected_threads contains 'main'"
expected_output_contains:
  - "Do not perform disk I/O on the main thread"
  - "Use Dispatchers.IO or Worker threads"
```

---

## 6. Plugin System

### 6.1 Plugin Interface

External tools (GitHub, Jira, Obsidian, YouTube API, Android Studio, etc.) connect via a standard plugin interface:

```yaml
# plugins/{tool}/manifest.json
{
  "plugin_id": "github@v1.2.0",
  "type": "api_integration",
  "auth_method": "oauth | api_key | ssh",
  "interface_version": "vjsos-ai-plugin-v1",
  "capabilities": [
    "read_repositories",
    "create_issues",
    "manage_pull_requests",
    "trigger_workflows",
    "read_analytics"
  ],
  "rate_limits": {
    "calls_per_minute": 5000,
    "per_ip": true
  },
  "required_permissions": [
    "admin:repo_hook"
  ],
  "governor_approval": true,
  "last_audited": "2026-08-05"
}
```

### 6.2 Plugin SDK

Plugins implement handlers for:
- `on_event(event_type, payload)` — react to system events
- `on_schedule(cron)` — recurring tasks
- `on_request(endpoint, params)` — expose internal APIs
- `on_stream(source)` — consume external data streams

### 6.3 Plugin Lifecycle

```
Installed → Governor Reviews → QA Verifies → Approved → Active
    ↑                                    ↓
    ←────── Superseded/New Version ──────
```

---

## 7. Bootstrap & Initialization

### 7.1 Bootstrap Sequence (Phase 0)

1. **Constitution Load** — Governor validates and signs the Constitution
2. **Kernel Initialize** — All kernel components start, health-check pass
3. **Department Creation** — Core departments created from manifests
4. **Agent Registration** — Workers register with Governor
5. **Skill Registration** — All skills load into registry
6. **Memory Initialize** — Tier 4 loads first, then Tier 3
7. **Plugin Load** — External integrations authorized
8. **Operational** — System accepts user requests

### 7.2 Phase 1-4 Implementation

**Phase 1 — Kernel:** Governor, Orchestrator, Context Engine, Memory Engine, QA Engine

**Phase 2 — Infrastructure:** Skill Registry, Plugin Manager, Event Bus, Analytics, Learning Engine

**Phase 3 — Departments:** Engineering, Media, Research, Business (one director + agents each)

**Phase 4 — Expansion:** Animation, Operations, Infrastructure, Knowledge, Automation

---

## 8. Versioning & Compatibility

### 8.1 Semantic Versioning
- `MAJOR` — breaking changes (Constitution amendments, protocol changes)
- `MINOR` — backward-compatible feature additions
- `PATCH` — bug fixes, non-breaking updates

### 8.2 Protocol Versions
Message types and plugin interfaces are versioned independently:

```
protocol_version: "vjsos-ai-mbus-v1.3.0"
plugin_interface: "vjsos-ai-plugin-v1.2.0"
skill_format: "vjsos-ai-skill-v1.0.0"
```

### 8.3 Migration Policy
- Breaking protocol changes require 6-month deprecation window
- Old format support maintained during migration period
- Governor manages migration schedules

---

## 9. Observability & Monitoring

### 9.1 Logging
Every agent emits structured logs to:
- `logs/audit.log` — every user-facing action (Constitution Rule 6: observability)
- `logs/events.log` — system events (state transitions, errors, escalations)
- `logs/debug.log` — developer-level diagnostics

### 9.2 Metrics
- **Kernel:** uptime, message latency, queue depth, error rate
- **Orchestrator:** plan success rate, dispatch latency, QA cycle count
- **Agents:** task completion rate, QA pass rate, context tokens used
- **Departments:** throughput, quality score, regression count
- **Learning:** improvement adoption rate, pattern detection accuracy

### 9.3 Alerting
Critical alerts route to Governor → Human:
- System downtime > 5m
- Constitutional violation detected
- QA failure rate > 5% over 1h
- Memory growth exceeds threshold

---

## 10. Security Model

### 10.1 Trust Boundaries
```
┌──────────────────────────────────────┐
│               USER                   │
└────────────────┬─────────────────────┘
                 │ request
                 ▼
┌──────────────────────────────────────┐
│         GOVERNOR (root)              │
│   - Constitution enforcement         │
│   - Human-in-the-loop for overrides  │
└──────────────────────────────────────┘
                 │
         ┌───────┴───────┐
         ▼               ▼
┌──────────────────┐  ┌──────────────────┐
│  ORCHESTRATOR    │  │  CONTEXT ENGINE  │
└──────────────────┘  └──────────────────┘
         │               │
         ▼               ▼
┌──────────────────────────────────────┐
│       DEPARTMENTS (sandboxed)        │
│  Each has its own agent + QA bubble  │
└──────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│         SHARED SERVICES              │
│   Memory • Learning • Analytics      │
└──────────────────────────────────────┘
```

### 10.2 Credential Management
- No credentials stored in prompts or agent memory
- Plugin-managed auth (OAuth, API keys, SSH) through secure vault
- Governor approves all plugin auth methods

### 10.3 Isolation
- Agents operate in isolated sandboxes
- Memory accesses audited
- Cross-department data sharing through Orchestrator only

---

**End of VJSOS-AI Operating System Specification**

### Next Documents
- `docs/specs/DEPLOYMENT_SPEC.md` — How to run VJSOS-AI locally
- `docs/specs/LEARNING_ENGINE_SPEC.md` — Continuous improvement workflows
- `docs/specs/ANALYTICS_ENGINE_SPEC.md` — Metrics and dashboards
- `docs/DEPARTMENTS.md` — All department manifests
- `docs/AGENTS.md` — All agent manifests
- `docs/SKILLS.md` — All skill manifests

### Quick Start
See `docs/QUICKSTART.md` for local setup and bootstrap instructions.