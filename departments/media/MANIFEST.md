# Media Department Manifest

**Department ID:** media
**Director:** `director-media@vjsos-ai`
**Constitution Article:** V, VI

---

## Mission
Create, edit, and publish multimedia content following production standards and audience requirements. Story development and creative execution for VJSOS channels (Android tutorials, Kids Studio, etc.).

## Domains
- research — Fact-checking, source verification, topic research
- writing — Script creation, editing, formatting
- publishing — SEO, distribution, platform optimization

## Worker Agents
| Agent ID | Type | Skills |
|----------|------|--------|
| `research-agent@media@vjsos-ai` | Worker | research, fact_checking, source_verification, citation_management, documentation |
| `script-agent@media@vjsos-ai` | Worker | script_writing, editing, formatting, documentation, qa_review |
| `publishing-agent@media@vjsos-ai` | Worker | content_formatting, seo_optimization, distribution, documentation, quality_check |

## QA Agent
`qa-media@vjsos-ai` — Enforces `media_qa_rubric_v2.0` (includes Child Safety)

## Memory Scope
`memory/department/media/` — contains:
- style_guides/
  - android_tutorials.md
  - kids_studio.md
- content_calendars/
- character_sheets/
- qa_rubric.md
- child_safety_checklist.md
- lessons_learned/

## SOPs
- `sops/media/script_writing.md`
- `sops/media/research_verification.md`
- `sops/media/publishing_checklist.md`
- `sops/media/child_safety_review.md`
- `sops/media/22_agent_workflow.md`

## KPIs
| Metric | Target |
|--------|--------|
| QA Pass Rate | ≥ 85% |
| Publishing Timeline Adherence | ≥ 90% |
| Factual Accuracy (verified claims) | 100% |
| Child Safety Compliance | 100% (zero tolerance) |
| Brand Consistency Score | ≥ 95% |
| Audience Retention (per channel) | Baseline +5% YoY |

## Skill Registry Entries (in skills/media/)
- research_verification/
- script_writing/
- content_publishing/
- seo_optimization/
- child_safety_review/

## Directory Structure
```
departments/media/
├── director-media@vjsos-ai.md
├── research-agent@vjsos-ai.md
├── script-agent@vjsos-ai.md
├── publishing-agent@vjsos-ai.md
├── qa-media@vjsos-ai.md
├── MANIFEST.md (this file)
├── memory/ (symlink to memory/department/media/)
└── skills/ (symlink to skills/media/)
```

## Governance
- Director reports to Governor
- QA agent reports to QA Engine + Director
- Child Safety is non-negotiable — all Kids Studio content requires QA safety pass
- All cross-department requests go through Orchestrator → Governor

## Startup Dependencies
- Kernel components: Governor, Orchestrator, Context Engine, Memory Engine, QA Engine
- Plugin: youtube@v1.0.0 (publishing)
- Plugin: spotify@v1.0.0 (publishing)
- Plugin: instagram@v1.0.0 (social)
- Skills registry available
- Department memory initialized

---

**Status:** Operational
**Version:** 1.0.0
**Last Updated:** 2026-08-07