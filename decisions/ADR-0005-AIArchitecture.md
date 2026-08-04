# ADR-0005-AIArchitecture: AI Workforce as Specialized Agents

## Status
Accepted

## Date
2026-08-04

## Context
VJSOS requires AI assistance across many domains. Approaches considered:

1. **Single general-purpose agent** — one LLM context, handle everything
2. **External AI tools only** — Copilot, Notion AI, etc.
3. **AI employees** — 14 specialized agents, each with a versioned prompt, KPIs, escalation rules
4. **Human-only team** — no AI in core workflows

Requirements:
- Specialization per domain of expertise
- Traceable outputs
- Version-controlled prompts
- Escalation path to human
- Measurable performance

## Decision
Define VJSOS's AI agents as **14 specialized employees**, each with:
- A versioned system prompt (`prompts/{AGENT}/prompt.md`)
- Defined responsibilities, inputs, outputs
- KPIs (how we measure them)
- Escalation rules (when they defer to humans)

### Agent Roster
| Agent | Role | Domain |
|-------|------|--------|
| CEO | Strategy, resource allocation | Leadership |
| Architect | Technical design, pipelines | Engineering |
| Research | Market/audience validation | Content |
| Project Manager | Sprint execution, task tracking | Process |
| Writer | Scripts, dialogue, beats | Kids Studio |
| Animation Director | Visual style, 22-agent workflow | Kids Studio |
| Sound Director | Voice, music, foley, mixing | Kids Studio |
| Child Safety | Safety gatekeeper, review | Governance |
| Rights Clearance | IP verification, licensing | Legal |
| Publisher | Upload, metadata, scheduling | Distribution |
| SEO | Titles, thumbnails, tags | Growth |
| Analytics | Performance review, learnings | Metrics |
| QA | Final QC, technical + content | Quality |
| VFX | Effects, transitions, compositing | Production |

### Prompt versioning
- Each prompt stored as `prompts/{AGENT}/prompt.md`
- Version incremented on change (`0.1.0` → `0.2.0`)
- Change logged via ADR or version bump in CHANGELOG

## Consequences

### Positive
- Specialization: each agent tuned for its domain
- Traceability: versioned prompts mean we know what generated each output
- Escalation: clear paths when AI hits limits
- Scalability: can add new agents as needs grow
- Governance: agent roles aligned with company values/core principles

### Negative
- More prompts to maintain than a single agent
- Coordination overhead between agents
- Prompt drift possible if not versioned
- Need a manager agent (Project Manager) to orchestrate

## Alternatives Considered

| Alternative | Rejected Because |
|-------------|-----------------|
| Single general agent | Poor specialization, loses domain detail |
| External AI tools only | No customization, no traceability |
| No AI workforce | Misses the VJSOS competitive advantage |

## Related ADRs
- [[decisions/ADR-0001-Vision]] — part of Brain layer
- [[decisions/ADR-0002-Markdown]] — prompts stored as Markdown
- [[decisions/ADR-0008-Kernel]] — governance of AI workforce

## Future Work
- Implement agent orchestration layer
- Add automated prompt A/B testing
- Extend to agent-to-agent communication protocol