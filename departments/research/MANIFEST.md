# Research Department Manifest

**Department ID:** research
**Director:** `director-research@vjsos-ai`
**Constitution Article:** V, VI

---

## Mission
Conduct systematic research, data analysis, and knowledge discovery to support organizational decision-making and innovation. Ensure all research is rigorous, reproducible, and honestly reported.

## Domains
- data-analysis — Statistical analysis, modeling, visualization
- knowledge-management — Taxonomy, curation, deduplication, discovery

## Worker Agents
| Agent ID | Type | Skills |
|----------|------|--------|
| `data-analyst-agent@research@vjsos-ai` | Worker | data_analysis, statistical_modeling, visualization, reporting, documentation |
| `knowledge-agent@research@vjsos-ai` | Worker | knowledge_organization, categorization, information_discovery, documentation, quality_assurance |

## QA Agent
`qa-research@vjsos-ai` — Enforces `research_qa_rubric_v2.0`

## Memory Scope
`memory/department/research/` — contains:
- methodologies/
- data_governance.md
- qa_rubric.md
- prior_analyses/
- knowledge_taxonomy.md
- lessons_learned/

## SOPs
- `sops/research/data_analysis.md`
- `sops/research/knowledge_curation.md`
- `sops/research/reproducibility.md`
- `sops/research/source_verification.md`

## KPIs
| Metric | Target |
|--------|--------|
| QA Pass Rate | ≥ 85% |
| Reproducibility Rate | 100% |
| Source Verification | 100% |
| Confidence Intervals Reported | 100% |
| Limitation Disclosure | 100% |
| Knowledge Deduplication | 0 active duplicates |

## Skill Registry Entries (in skills/research/)
- data_analysis/
- statistical_modeling/
- knowledge_management/

## Directory Structure
```
departments/research/
├── director-research@vjsos-ai.md
├── data-analyst-agent@vjsos-ai.md
├── knowledge-agent@vjsos-ai.md
├── qa-research@vjsos-ai.md
├── MANIFEST.md (this file)
├── memory/ (symlink to memory/department/research/)
└── skills/ (symlink to skills/research/)
```

## Governance
- Director reports to Governor
- QA agent reports to QA Engine + Director
- All data sources must be licensed/verified before use
- All cross-department requests go through Orchestrator → Governor

## Startup Dependencies
- Kernel components: Governor, Orchestrator, Context Engine, Memory Engine, QA Engine
- Plugin: python@v1.0.0 (analysis runtime)
- Plugin: jupyter@v1.0.0 (notebooks)
- Skills registry available
- Department memory initialized

---

**Status:** Operational
**Version:** 1.0.0
**Last Updated:** 2026-08-07