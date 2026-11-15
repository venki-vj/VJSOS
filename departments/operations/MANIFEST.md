# Operations Department Manifest

**Department ID:** operations
**Director:** `director-operations@vjsos-ai`
**Constitution Article:** V, VI

---

## Mission
Ensure smooth day-to-day operations through process optimization, automation, and reliability — turning manual work into governed, idempotent systems.

## Domains
- automation — Process automation, workflow optimization, idempotent scripts

## Worker Agents
| Agent ID | Type | Skills |
|----------|------|--------|
| `automation-agent@operations@vjsos-ai` | Worker | process_automation, workflow_optimization, monitoring, testing, documentation |

## QA Agent
`qa-operations@vjsos-ai` — Enforces `operations_qa_rubric_v2.0`

## Memory Scope
`memory/department/operations/` — contains:
- process_maps/
- automation_inventory.md
- idempotency_patterns.md
- safety_checklists.md
- qa_rubric.md
- runbooks/
- lessons_learned/

## SOPs
- `sops/operations/automation_development.md`
- `sops/operations/idempotency.md`
- `sops/operations/rollback_procedures.md`

## KPIs
| Metric | Target |
|--------|--------|
| QA Pass Rate | ≥ 90% |
| Automation Reliability | ≥ 99% |
| Idempotency Verified | 100% |
| Dry-Run Validated | 100% |
| Time Saved (monthly) | Tracked |
| Rollback Ready | 100% |

## Skill Registry Entries (in skills/operations/)
- process_automation/
- workflow_optimization/

## Directory Structure
```
departments/operations/
├── director-operations@vjsos-ai.md
├── automation-agent@vjsos-ai.md
├── qa-operations@vjsos-ai.md
├── MANIFEST.md (this file)
├── memory/ (symlink to memory/department/operations/)
└── skills/ (symlink to skills/operations/)
```

## Governance
- Director reports to Governor
- QA agent reports to QA Engine + Director
- Destructive automation requires Governor approval
- All cross-department requests go through Orchestrator → Governor

## Startup Dependencies
- Kernel components: Governor, Orchestrator, Context Engine, Memory Engine, QA Engine
- Plugin: github@v1.2.0 (automation CI)
- Skills registry available
- Department memory initialized

---

**Status:** Operational
**Version:** 1.0.0
**Last Updated:** 2026-08-07