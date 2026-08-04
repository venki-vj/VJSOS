# VJSOS Knowledge Graph — README

> The central nervous system: how knowledge is organized, linked, and queried.

## Philosophy

The knowledge graph is not a folder — it's a **queryable network** of VJSOS truth. Every artifact is a node; every wiki-link is an edge. We treat knowledge as compound interest (see [[company/CoreValues]]).

## Node Types

| Type | Prefix | Examples |
|------|--------|----------|
| **Concept** | (none) | `Phase-aware development`, `Child safety gate` |
| **Artifact** | `assets/`, `projects/`, `prompts/` | `assets/characters/2026-08-04_mira_v1.blend` |
| **Person/Role** | `prompts/` | `prompts/CEO`, `prompts/AnimationDirector` |
| **Decision** | `decisions/` | `decisions/ADR-0001-Vision` |
| **Process** | `docs/sop/`, `engineering/` | `docs/sop/DAILY`, `engineering/automation/README` |
| **Product** | `projects/` | `projects/Android`, `projects/KidsStudio` |

## Edge Types

| Type | Meaning | Example |
|------|---------|---------|
| `depends-on` | B cannot start before A | `Episode 1` depends-on `Character rigs` |
| `part-of` | B is a component of A | `Character rigs` part-of `Kids Studio` |
| `produced-by` | A was created by B | `Script v1` produced-by `prompts/Writer` |
| `references` | A cites B for authority | `ADR-0001` references `kernel/CorePrinciples` |
| `relates-to` | Semantic similarity | `Android tutorials` relates-to `Kids Studio assets` |
| `governs` | A enforces rules on B | `governance/Standards` governs `engineering/` |

## Query Patterns

### 1. "What do I need before starting X?"
```text
X (e.g., "Episode 1 script")
  → edges: depends-on
  → prerequisites
```

### 2. "Where is asset Y?"
```text
Y (e.g., "Mira character rig")
  → edges: part-of
  → location: projects/KidsStudio/characters/
```

### 3. "Who owns process Z?"
```text
Z (e.g., "Render pipeline")
  → edges: produced-by, governs
  → owners: Animation Director, engineering/automation
```

### 4. "What decisions affect topic W?"
```text
W (e.g., "Infrastructure upgrade")
  → edges: references
  → ADRs: ADR-0001, ADR-0007, ADR-0008
```

## Implementation

- **Primary navigation:** Obsidian graph view + wiki-links (`[[...]]`)
- **Index:** [[knowledge/index]] (cross-linked domain map)
- **Schema:** [[knowledge/graph-schema]] (formal entity/relationship definitions)

## Maintenance Rules

- Every new artifact gets an ID and at least 1 incoming wiki-link.
- Broken links flagged in CI (see `.github/workflows/ci.yml`).
- Quarterly graph audit (see [[metrics/QuarterlyReports]]).

## Related

- [[kernel/Interfaces]] (Brain→Factory contract)
- [[knowledge/index]], [[knowledge/graph-schema]]
- [[governance/DocumentationRules]]