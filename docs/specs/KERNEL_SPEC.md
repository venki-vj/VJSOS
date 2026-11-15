# VJSOS-AI Kernel Architecture Specification

**Version:** 1.0.0
**Status:** Draft
**Constitution Article:** IV, VI
**Depends On:** AI_CONSTITUTION.md

---

## 1. System Governor (`governor`)

### Mission
Enforce constitutional compliance, maintain architectural integrity, resolve cross-department conflicts, approve agent/skill lifecycle events, control memory growth, trigger refactoring.

### Authority (Constitution Article VI)
- Final on all architectural and policy decisions
- Approve/reject new agents, skills, memory schemas
- Resolve inter-department disputes
- Mandate refactoring when complexity thresholds exceeded
- Archive orphaned memory
- Audit all agent actions

### Interface
```yaml
agent_id: governor@vjsos-ai
type: singleton
memory_tier: global
skills:
  - constitutional_analysis
  - architecture_review
  - conflict_resolution
  - memory_governance
  - agent_lifecycle_management
  - skill_registry_governance
  - refactoring_authorization
inputs:
  - escalation_requests
  - agent_registration_requests
  - skill_registration_requests
  - memory_growth_reports
  - architecture_change_proposals
  - qa_appeals
  - constitutional_amendment_rfcs
outputs:
  - governance_decisions
  - approval_denials
  - refactoring_mandates
  - memory_archive_orders
  - agent_skill_lifecycle_events
  - audit_findings
sla:
  escalation_response: "5m"
  registration_review: "1h"
  audit_completion: "24h"
```

### Decision Log
Every decision recorded in `memory/global/governor/decisions/` with:
- `decision_id`, `timestamp`, `type`, `requestor`, `rationale`, `constitution_articles`, `outcome`, `appeal_deadline`

### Human Override
Constitutional amendments (Articles II, III, IV) require human sign-off. Governor logs override request and waits.

---

## 2. Orchestrator (`orchestrator`)

### Mission
Coordinate all task execution. Decompose user requests, select departments and agents, build context packages, manage QA gates, assemble final output.

### Authority
- Task decomposition and routing
- Department/agent selection
- Context package assembly
- QA gate enforcement
- Output aggregation
- Correlation ID management

### Interface
```yaml
agent_id: orchestrator@vjsos-ai
type: singleton
memory_tier: global
skills:
  - intent_analysis
  - task_decomposition
  - department_selection
  - agent_selection
  - context_package_builder
  - qa_gate_manager
  - output_aggregator
  - correlation_tracking
  - priority_management
inputs:
  - user_requests (via message bus)
  - department_capabilities_registry
  - agent_registry
  - skill_registry
  - context_engine
  - qa_engine
outputs:
  - task_plans
  - context_packages
  - agent_dispatches
  - qa_submissions
  - final_outputs
  - execution_logs
sla:
  plan_generation: "30s"
  context_assembly: "10s"
  dispatch_latency: "5s"
```

### Orchestration Loop
```
1. Receive user request (message)
2. Analyze intent → required capabilities
3. Select department(s) → select agent(s) per capability
4. Request context package from Context Engine
5. Dispatch to agent(s) with context + correlation_id
6. Collect outputs → submit to QA Engine
7. On QA pass → aggregate → return to user
8. On QA fail → route feedback to agent → repeat (max 3 cycles)
9. Log complete execution trace
```

### Task Plan Schema
```json
{
  "plan_id": "uuid",
  "correlation_id": "uuid",
  "user_request": "string",
  "intent": {"primary": "string", "secondary": ["string"]},
  "departments": ["engineering", "media"],
  "steps": [
    {
      "step_id": "uuid",
      "agent": "agent_id",
      "skill": "skill_name",
      "input_ref": "memory_address",
      "output_ref": "memory_address",
      "depends_on": ["step_id"],
      "qa_required": true,
      "priority": "normal",
      "timeout": "duration"
    }
  ],
  "created_at": "ISO8601",
  "status": "planned | executing | qa | complete | failed"
}
```

---

## 3. Context Engine (`context-engine`)

### Mission
Build minimal, relevant context packages for agents. Eliminate context bloat. Maximize signal-to-noise.

### Authority
- Intent-to-knowledge mapping
- Relevance scoring
- Context package construction
- Token budget enforcement

### Interface
```yaml
agent_id: context-engine@vjsos-ai
type: singleton
memory_tier: global
skills:
  - intent_classification
  - knowledge_retrieval
  - relevance_scoring
  - token_budgeting
  - context_packaging
  - dependency_resolution
inputs:
  - orchestrator_requests (intent + agent + task)
  - knowledge_graph
  - memory_index
  - skill_registry
  - sop_index
  - adr_index
  - project_index
outputs:
  - context_packages
  - retrieval_metadata (what was included/excluded and why)
sla:
  package_build: "5s"
  max_tokens: "8000"  # configurable per agent tier
```

### Context Package Structure
```json
{
  "package_id": "uuid",
  "target_agent": "agent_id",
  "correlation_id": "uuid",
  "token_count": 4231,
  "sections": {
    "constitution": {"included": true, "articles": ["II", "III", "IV"], "tokens": 1200},
    "agent_prompt": {"included": true, "version": "1.2.0", "tokens": 800},
    "skills": [
      {"skill_id": "android.architecture", "version": "2.1.0", "tokens": 600}
    ],
    "memory": {
      "global": ["vision", "roadmap"],
      "department": ["architecture_patterns"],
      "agent": ["recent_anr_cases"],
      "project": ["current_sprint"]
    },
    "knowledge": [
      {"doc_id": "android_binder_architecture", "relevance": 0.94, "tokens": 1200}
    ],
    "sops": ["code_review", "testing_standard"],
    "adrs": ["ADR-004-binder-ipc"],
    "projects": ["vjsos-android"]
  },
  "excluded": [
    {"doc_id": "ios_swift_ui", "reason": "irrelevant_domain"}
  ],
  "built_at": "ISO8601"
}
```

### Relevance Algorithm
1. **Domain match** (0.4 weight) — agent's declared domains vs. content tags
2. **Recency** (0.2 weight) — exponential decay, half-life 30 days
3. **Frequency of use** (0.2 weight) — how often this knowledge helped similar tasks
4. **Explicit reference** (0.2 weight) — user or orchestrator explicitly requested

---

## 4. Memory Engine (`memory-engine`)

### Mission
Manage four-tier memory with lifecycle, indexing, and retrieval. Prevent bloat. Ensure consistency.

### Architecture
```
memory/
├── global/          # Tier 4: Company vision, roadmaps, principles, ADRs, constitution
├── department/      # Tier 3: Department standards, patterns, lessons, SOPs
├── agent/           # Tier 2: Agent-specific domain knowledge, case histories
├── project/         # Tier 2: Project context, sprint state, decisions
├── session/         # Tier 1: Current conversation, ephemeral state
├── lessons/         # Cross-cutting: Lessons learned, postmortems, improvements
├── adr/             # Architecture Decision Records (immutable once ratified)
└── index/           # Search index, embeddings, metadata
```

### Memory Object Schema
```json
{
  "memory_id": "uuid",
  "tier": "global | department | agent | project | session | lessons | adr",
  "owner": "agent_id | department_id | project_id | governor",
  "scope": ["domain_tags"],
  "content": {},
  "metadata": {
    "created_at": "ISO8601",
    "updated_at": "ISO8601",
    "ttl": "duration | null",
    "review_date": "ISO8601 | null",
    "version": "semver",
    "tags": ["string"],
    "source": "agent_output | human_input | learning_engine | migration",
    "verification_status": "unverified | verified | deprecated"
  },
  "links": ["memory_id"],  # related memories
  "embedding": "vector | null"
}
```

### Lifecycle Rules
| Tier | Default TTL | Review Cycle | Archive Trigger |
|------|-------------|--------------|-----------------|
| global | ∞ | 90 days | Never (constitution-protected) |
| department | ∞ | 60 days | Department dissolved |
| agent | 180 days | 30 days | Agent deprecated |
| project | 90 days post-completion | 14 days | Project archived |
| session | 24 hours | N/A | Session ends |
| lessons | ∞ | 90 days | Superseded by new lesson |
| adr | ∞ | Never | Superseded by new ADR |

### Interface
```yaml
agent_id: memory-engine@vjsos-ai
type: singleton
memory_tier: global
skills:
  - memory_crud
  - tier_management
  - lifecycle_enforcement
  - indexing_search
  - embedding_generation
  - deduplication
  - archival
inputs:
  - write_requests (from agents, learning engine, governor)
  - read_requests (from context engine, agents)
  - lifecycle_timers
  - governor_archive_orders
outputs:
  - memory_objects
  - search_results
  - lifecycle_events (created, updated, archived, expired)
  - index_updates
sla:
  write: "50ms"
  read: "100ms"
  search: "200ms"
  archive: "async"
```

### Deduplication
Before write, check:
1. Exact content match → return existing memory_id
2. Semantic similarity > 0.95 (embedding) → propose merge to Governor
3. Same owner + same scope + overlapping tags → propose consolidation

---

## 5. QA Engine (`qa-engine`)

### Mission
Independent quality verification for every agent output. Enforce standards. Prevent regressions. Block substandard work.

### Authority
- **Veto power:** No output passes without QA approval
- **Standard definition:** Each department QA defines its quality rubric
- **Regression detection:** Compare outputs against baselines
- **Escalation:** Appeal to Governor only

### Interface
```yaml
agent_id: qa-engine@vjsos-ai
type: singleton (coordinates department QA agents)
memory_tier: global
skills:
  - quality_rubric_evaluation
  - regression_testing
  - standard_enforcement
  - feedback_generation
  - verdict_issuance
  - appeal_management
inputs:
  - orchestrator_qa_submissions
  - department_qa_agents (worker outputs)
  - quality_rubrics (from department directors)
  - test_suites (from skills)
  - baselines (from analytics)
outputs:
  - qa_verdicts (pass | fail | conditional_pass)
  - detailed_feedback
  - regression_reports
  - improvement_suggestions
  - metrics_updates
sla:
  review_time: "2m" per output
  max_cycles: 3
```

### QA Verdict Schema
```json
{
  "verdict_id": "uuid",
  "submission_id": "uuid",
  "agent": "agent_id",
  "department": "department_id",
  "verdict": "pass | fail | conditional_pass",
  "score": 0.94,
  "rubric": "department_qa_rubric_v2.1",
  "checks": [
    {"check": "accuracy", "weight": 0.3, "score": 0.95, "pass": true},
    {"check": "completeness", "weight": 0.2, "score": 0.90, "pass": true},
    {"check": "documentation", "weight": 0.15, "score": 1.0, "pass": true},
    {"check": "tests_pass", "weight": 0.2, "score": 1.0, "pass": true},
    {"check": "constitution_compliance", "weight": 0.15, "score": 0.88, "pass": false, "notes": "Missing ADR reference"}
  ],
  "feedback": "Add ADR-004 reference to binder IPC section",
  "regression_check": {"baseline_score": 0.92, "delta": +0.02, "status": "improved"},
  "reviewed_at": "ISO8601",
  "reviewer": "qa-android@vjsos-ai"
}
```

### Department QA Agents
Each department has a dedicated QA agent:
- `qa-engineering@vjsos-ai`
- `qa-media@vjsos-ai`
- `qa-business@vjsos-ai`
- `qa-animation@vjsos-ai`
- `qa-operations@vjsos-ai`
- `qa-research@vjsos-ai`
- `qa-infrastructure@vjsos-ai`
- `qa-knowledge@vjsos-ai`
- `qa-automation@vjsos-ai`

They implement department-specific rubrics but share the QA Engine infrastructure.

### Appeal Process
```
Fail verdict → Agent may appeal once → Governor reviews → Final decision (binding)
```

---

## 6. Kernel Message Bus

All kernel components communicate via structured messages on the internal bus.

### Topics
- `kernel.governor.commands`
- `kernel.governor.events`
- `kernel.orchestrator.plans`
- `kernel.orchestrator.dispatches`
- `kernel.context.requests`
- `kernel.context.packages`
- `kernel.memory.operations`
- `kernel.qa.submissions`
- `kernel.qa.verdicts`
- `kernel.analytics.metrics`
- `kernel.audit.log`

### Delivery Guarantees
- At-least-once delivery
- Ordered per correlation_id
- Persistent until acknowledged
- Dead-letter queue for failed deliveries > 3 retries

---

## 7. Kernel Bootstrap Sequence

```
1. Governor loads Constitution → validates integrity → broadcasts "constitution_ready"
2. Memory Engine initializes tiers → loads index → broadcasts "memory_ready"
3. Context Engine connects to Memory + Knowledge → broadcasts "context_ready"
4. QA Engine loads rubrics → connects to department QA agents → broadcasts "qa_ready"
5. Orchestrator registers with all → loads agent/skill registries → broadcasts "orchestrator_ready"
6. Department Directors register agents → broadcast "department_ready"
7. System enters "operational" state
```

### Health Checks
Each kernel component exposes `/health`:
```json
{
  "component": "orchestrator",
  "status": "healthy | degraded | down",
  "uptime": "duration",
  "last_operation": "ISO8601",
  "queue_depth": 12,
  "error_rate": 0.001,
  "dependencies": {"context_engine": "healthy", "memory_engine": "healthy", "qa_engine": "healthy"}
}
```

---

## 8. Configuration

`config/kernel.yaml`:
```yaml
governor:
  escalation_timeout: "5m"
  registration_sla: "1h"
  audit_interval: "24h"

orchestrator:
  max_concurrent_plans: 50
  default_timeout: "10m"
  max_qa_cycles: 3

context_engine:
  default_token_budget: 8000
  max_token_budget: 32000
  relevance_weights:
    domain_match: 0.4
    recency: 0.2
    frequency: 0.2
    explicit_reference: 0.2

memory_engine:
  global_ttl: null
  department_ttl: null
  agent_ttl: "180d"
  project_ttl: "90d"
  session_ttl: "24h"
  deduplication_threshold: 0.95

qa_engine:
  default_review_timeout: "2m"
  max_qa_cycles: 3
  regression_baseline_window: "30d"
```

---

**End of Kernel Specification**