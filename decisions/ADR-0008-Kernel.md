# ADR-0008-Kernel: Immutable Core

## Status
Accepted

## Date
2026-08-05

## Context
VJSOS has many moving parts (agents, docs, business units, tools). We need a single, stable reference point that:
1. Never changes without deliberate process
2. Resolves conflicts between layers
3. Defines "who we are" at the deepest level
4. Can be pointed to by everything else

Without this, decisions drift, values erode, and scaling creates chaos.

## Decision
Create an **immutable kernel** at `kernel/` containing:

| File | Purpose |
|------|---------|
| `Mission.md` | One-sentence mission + North Star |
| `Vision.md` | Long-term aspirational picture |
| `CorePrinciples.md` | The 7 operating values (behavioral) |
| `CoreWorkflow.md` | 5-step execution cycle (Plan → Execute → Review → Retro → Improve) |
| `ExecutionCycle.md` | Daily/weekly/monthly/quarterly rhythms with triggers |
| `Interfaces.md` | Contracts between Brain/Factory/Data Center layers |
| `Standards.md` | Immutable pointer to `governance/Standards.md` |

### Kernel Rules

1. **Immutability:** Kernel files cannot be edited directly. Changes require:
   - Formal proposal (ADR-style)
   - **CEO + Architect** approval (both must agree)
   - Rationale recorded as ADR
   - Kernel version bump (semantic: `kernel-v0.1.0`)
   - Reverse-dependency update

2. **Single Source of Truth:** When governance, architecture, or process documents conflict, the kernel wins.

3. **Referential Integrity:** All layers reference kernel via wiki-links (`[[kernel/CorePrinciples]]`). No duplication.

4. **Audit Trail:** Every kernel change is an ADR. Quarterly kernel review in [[metrics/QuarterlyReports]].

### What the Kernel Is NOT
- Not a place for detailed procedures (those are in `governance/`, `docs/sop/`)
- Not a place for business unit specifics (those are in `projects/`, `company/`)
- Not a place for tool configurations (those are in `engineering/`)

### Kernel Versioning
| Version | Trigger |
|---------|---------|
| `kernel-v0.1.0` | Initial creation (Day 1) |
| `kernel-v0.2.0` | New core principle added |
| `kernel-v1.0.0` | Major structural change (new layer, removed layer) |

## Consequences

### Positive
- Absolute clarity on "what VJSOS is"
- Conflict resolution mechanism
- Onboarding anchor (new agents/humans read kernel first)
- Prevents value drift at scale

### Negative
- Change process is intentionally slow
- Requires discipline to reference, not duplicate
- Two-person approval can be a bottleneck

## Alternatives Considered

| Alternative | Rejected Because |
|-------------|-----------------|
| No kernel (agile-only) | Values drift; no anchor at scale |
| Flexible principles | "Everything is negotiable" → nothing matters |
| Living document (editable by all) | No stability; chaos under growth |

## Related ADRs
- [[decisions/ADR-0001-Vision]] — kernel includes the three-layer vision
- [[decisions/ADR-0005-AIArchitecture]] — agents aligned to kernel
- [[decisions/ADR-0006-Governance]] — governance enforces kernel
- [[decisions/ADR-0007-Infrastructure]] — phase-aware is a kernel principle