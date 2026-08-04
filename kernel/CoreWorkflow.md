# VJSOS Kernel — CoreWorkflow

> The immutable 5-step execution cycle.

## The Cycle

```
1. PLAN   → Set goals for the cycle (sprint, day)
2. EXECUTE → Do the work, phase-aware (1→2→3)
3. REVIEW  → Measure against goals; what landed?
4. RETRO   → What worked / blocked / should change?
5. IMPROVE → Update SOPs, ADRs, processes; loop
```

## Day Mapping (default rhythm)

| Day | Loop step | Reference |
|-----|-----------|-----------|
| Mon | PLAN | [[docs/sop/WEEKLY]] |
| Tue–Thu | EXECUTE | [[docs/sop/DAILY]] |
| Fri | REVIEW + RETRO | [[docs/sop/WEEKLY]] |
| Sat | IMPROVE (process updates) | [[docs/sop/WEEKLY]] |
| Sun | Rest / learning | [[company/Culture]] |

## Guardrails

- Always complete PLAN before EXECUTE.
- Always REVIEW before starting the next EXECUTE phase.
- IMPROVE writes changes back to versioned docs (no drift).
- Phase-4 work is never queued ahead of Phase 1–2.

## Related
- [[kernel/ExecutionCycle]]
- [[kernel/README]]