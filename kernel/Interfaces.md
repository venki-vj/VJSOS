# VJSOS Kernel — Interfaces

> Contracts between the three layers.

## Layer Definitions

| Layer | Dir | Produces | Consumes |
|-------|-----|----------|----------|
| Brain | `docs/`, `knowledge/`, `prompts/` | Requirements, content plans, decisions | Data from Factory, feedback from Data Center |
| Factory | `engineering/`, `projects/`, `assets/` | Code, automation, rendered assets, built tools | Specs from Brain, prompts from AI Workforce |
| Data Center | (future) `render/`, `ai-server/`, `nas/` | Rendering, inference, storage | Jobs from Factory, serves Brain |

## Contracts

### Brain → Factory
- **Spec format:** Markdown with frontmatter (title, version, tags)
- **Handoff:** PR in Git with assigned reviewer
- **Acceptance:** CI passes, 1 approval, docs updated

### Factory → Data Center
- **Job format:** YAML/JSON payload (render spec, model name, assets)
- **Queue:** GitHub Actions or future dedicated queue
- **Result:** Artifacts (video, model weights, logs) stored with metadata

### Human → AI
- **Interface:** Prompts in `prompts/{AGENT}/prompt.md` (versioned)
- **Invocation:** Context + task → Agent → Structured output
- **Review:** Human + Child Safety / Rights Clearance agents

### AI → Human
- **Output:** Markdown, JSON, or asset paths
- **Escalation:** Blockers → Project Manager → CEO
- **Traceability:** Every agent output logged to session file

## Non-Functional Requirements

| Contract | SLA |
|----------|-----|
| Brain→Factory spec clarity | ≥90% first-pass acceptance |
| Factory→Data Center job latency | <2 min queue (local), <10 min (cloud) |
| AI agent turnaround | <30s for Phase 1–2; Phase 3 async |
| Human review loop | <24h for Phase 1–2 tasks |

## Related
- [[docs/ARCHITECTURE]], [[kernel/README]]