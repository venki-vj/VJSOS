# Knowledge Department Manifest

**Department ID:** knowledge
**Director:** `director-knowledge@vjsos-ai`
**Constitution Article:** V, VI, IV Rule 4

---

## Mission
Maintain, organize, and distribute organizational knowledge ensuring accessibility and consistency across the enterprise. Enforce single-source-of-truth and zero duplication.

## Domains
- documentation — Technical documentation creation, maintenance, standards

## Worker Agents
| Agent ID | Type | Skills |
|----------|------|--------|
| `documentation-agent@knowledge@vjsos-ai` | Worker | documentation_creation, organization, knowledge_dist, quality_check, versioning |

## QA Agent
`qa-knowledge@vjsos-ai` — Enforces `knowledge_qa_rubric_v2.0`

## Memory Scope
`memory/department/knowledge/` — contains:
- documentation_standards.md
- taxonomy.md
- doc_health_dashboard.md
- qa_rubric.md
- style_guide.md
- lessons_learned/

## SOPs
- `sops/knowledge/documentation_creation.md`
- `sops/knowledge/knowledge_curation.md`
- `sops/knowledge/deduplication.md`

## KPIs
| Metric | Target |
|--------|--------|
| QA Pass Rate | ≥ 90% |
| Documentation Health Score | ≥ 85% |
| Active Duplicates | 0 |
| Coverage | ≥ 95% |
| Freshness (review-by met) | ≥ 90% |
| Search Success Rate | ≥ 95% |

## Skill Registry Entries (in skills/knowledge/)
- documentation_management/
- taxonomy_organization/

## Directory Structure
```
departments/knowledge/
├── director-knowledge@vjsos-ai.md
├── documentation-agent@vjsos-ai.md
├── qa-knowledge@vjsos-ai.md
├── MANIFEST.md (this file)
├── memory/ (symlink to memory/department/knowledge/)
└── skills/ (symlink to skills/knowledge/)
```

## Governance
- Director reports to Governor
- QA agent reports to QA Engine + Director
- Constitution content is immutable (Governor only for amendments)
- All cross-department requests go through Orchestrator → Governor

## Startup Dependencies
- Kernel components: Governor, Orchestrator, Context Engine, Memory Engine, QA Engine
- Skills registry available
- Department memory initialized
- Knowledge Agent (research dept) coordination for deduplication

---

**Status:** Operational
**Version:** 1.0.0
**Last Updated:** 2026-08-07