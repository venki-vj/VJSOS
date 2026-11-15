# Policy 0001: Agent Lifecycle Management

**Status:** DRAFT
**Effective:** 2026-08-07
**Governor Approval:** Required

## Purpose

This policy establishes the lifecycle phases for VJSOS-AI agents and the governance procedures for each phase transition.

## Agent Lifecycle Phases

| Phase | Requirements | Governor Action |
|-------|--------------|-----------------|
| **Proposital** | Agent draft written, domain assigned | No action required |
| **Registered** | Agent manifest registered via Governor | Must review within 48h |
| **Validated** | Unit tests pass, QA review complete | Must approve or reject |
| **Active** | Agent operational in department | Continuous monitoring |
| **Deprecated** | Superseded by newer agent | Must document deprecation |
| **Retired** | Removed from production | Final audit required |

## Phase Transitions

### Proposital → Registered

1. Agent prompt exists in `agents/{department}/`
2. Agent manifest created with:
   - `agent_id`: unique identifier
   - `type`: Director, QA, or Worker
   - `domain`: department affiliation
   - `memory_tier`: session, agent, department
3. Submit via `python -m governor.register_agent`

### Registered → Validated

1. All unit tests pass (pytest)
2. QA review completed by department QA agent
3. Governor approval documented in decision log

### Validated → Active

1. Governor final approval
2. Agent added to Orchestrator's agent registry
3. Department director notification

## Governance Rules

- **Rule 1:** No agent self-modification (Constitution Article VII)
- **Rule 2:** All decisions must be logged (Constitution Article III)
- **Rule 3:** Governor override required for cross-department agents
- **Rule 4:** Annual agent audit by QA Engine

## Exceptions

Any deviation from this policy requires a Governor decision with human approval (Constitution Article I).