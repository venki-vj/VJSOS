# ADR-0001-Vision: Three-Layer Architecture

## Status
Accepted

## Date
2026-08-04

## Context
VJSOS operates on current consumer hardware (Acer Aspire E5, integrated graphics). Production-quality animation, rendering, and local AI models are slow or impossible. We need an architecture that:
1. Allows productive work immediately
2. Scales gracefully as we add hardware
3. Keeps decision-making simple under resource constraints
4. Prevents bottlenecks in the wrong places

## Decision
Adopt the **three-layer architecture**:

| Layer | Name | Function | Current Hardware |
|-------|------|----------|----------------|
| 1 | **Brain** | Documentation, planning, knowledge, research, prompt engineering | ✅ 100% possible |
| 2 | **Factory** | Rendering, animation, local AI, video production | ⚠️ Slow |
| 3 | **Data Center** | Dedicated render machine, AI workstation, NAS, backup server | ❌ Not yet |

### Implementation
- Brain-layer work (docs, Obsidian, Git, research) happens on current laptop
- Factory-layer work (Blender, Remotion) is possible but slow — batch and schedule
- Data Center is deferred until Phase 3 work blocks revenue (see [[governance/Standards]])

### Phase-Aware Rule
Phase 1 work must always precede Phase 2 work in scheduling.
Phase 2 work must always precede Phase 3 work.
Phase 3-4 work is intentionally deferred unless it generates revenue.

## Consequences

### Positive
- Clear scope of what works on current hardware (100% Phase 1–2)
- No premature hardware spend (₹5L saved initially)
- Structured upgrade path (see [[docs/infrastructure]])
- Work classification prevents wasted effort on impossible tasks

### Negative
- Phase 3 work (animation, rendering) is slow — affects production velocity
- No redundancy or backup (single machine)
- Limited collaboration (one laptop)

## Alternatives Considered

| Alternative | Rejected Because |
|-------------|-----------------|
| Single-layer (treat as content studio) | Doesn't capture the AI infrastructure angle; future expansion unclear |
| Cloud-first (all production in cloud) | Expensive ongoing, no ownership of infrastructure |
| Buy high-end workstation now | Capital-intensive, no proof of concept yet, violates "capability before capacity" |
| Agency/hired model | Doesn't fit the independent creator/scalable vision |

## Related ADRs
- [[decisions/ADR-0007-Infrastructure]] — the supporting capability model
- [[decisions/ADR-0008-Kernel]] — this is part of the immutable kernel