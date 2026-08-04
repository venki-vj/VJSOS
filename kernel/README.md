# VJSOS Kernel — README

> The immutable core of VJSOS.

## What Is the Kernel?

The kernel is the **source of truth** for VJSOS — the one place that defines who we are and how we work. Everything else (governance, architecture, SOPs, business units) depends on and references the kernel.

Think of it like the Linux kernel: a small, stable core that everything else builds on.

## Contents

| File | Purpose |
|------|---------|
| [[kernel/Mission]] | One-sentence mission + North Star |
| [[kernel/Vision]] | Long-term picture |
| [[kernel/CorePrinciples]] | The 7 operating values (behavioral) |
| [[kernel/CoreWorkflow]] | The 5-step execution cycle |
| [[kernel/ExecutionCycle]] | Daily / weekly / monthly / quarterly rhythms |
| [[kernel/Interfaces]] | Contracts between layers |
| [[kernel/Standards]] | Pointer to governance standards |

## Rules of the Kernel

1. **Immutable:** Kernel files change only through a formal process (CEO + Architect approval).
2. **Single source of truth:** When conflict arises, kernel wins.
3. **Versioned:** Kernel changes are tagged (e.g., `kernel-v0.1`).
4. **Referenced, not duplicated:** Other docs link to kernel/ rather than copy it.
5. **Consistency check:** Every major decision must be consistent with the kernel.

## How to Change the Kernel

1. Propose a change (draft, ADR-style).
2. Get **CEO + Architect** approval.
3. Record rationale as an ADR (see [[decisions/README]]).
4. Bump kernel version.
5. Update reverse-dependencies.

## Relationship to Other Layers

```
KERNEL (immutable truth)
   │
   ├── governance/  → encodes the rules (how we work)
   ├── company/     → interprets the kernel (who we are)
   ├── docs/        → applies it (the system)
   ├── prompts/     → agents aligned to it
   └── knowledge/   → the graph that links it all
```

## Related

- [[company/Mission]], [[company/CoreValues]] — fuller, friendlier versions of kernel principles
- [[docs/ARCHITECTURE]] — the target operating model
- [[governance/Standards]] — the enforceable rules