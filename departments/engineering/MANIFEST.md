# Engineering Department Manifest

**Department ID:** engineering
**Director:** `director-engineering@vjsos-ai`
**Constitution Article:** V, VI

---

## Mission
Design, build, test, and maintain high-quality software systems following VJSOS architectural standards. Produce infrastructure automation and development tools that power VJSOS products and operations.

## Domains
- android — Android platform development (Kotlin, Compose, SDK)
- backend — Backend systems, APIs, databases, microservices
- infrastructure — CI/CD, IaC, deployment, observability, security
- architecture — System architecture, patterns, code review

## Worker Agents
| Agent ID | Type | Skills |
|----------|------|--------|
| `android-agent@engineering@vjsos-ai` | Worker | android_development, anr_analysis, performance_optimization, debugging, testing, architecture_design |
| `backend-agent@engineering@vjsos-ai` | Worker | api_design, database_architecture, microservices, testing, documentation, observability |
| `infrastructure-agent@engineering@vjsos-ai` | Worker | ci_cd_pipeline, automation, monitoring, security, testing, documentation |
| `code-review-agent@engineering@vjsos-ai` | Worker | code_review, architecture_validation, standards_enforcement, documentation, testing |

## QA Agent
`qa-engineering@vjsos-ai` — Enforces `engineering_qa_rubric_v2.0`

## Memory Scope
`memory/department/engineering/` — contains:
- architecture_patterns.md
- coding_standards.md
- testing_standards.md
- ci_cd_standards.md
- qa_rubric.md
- lessons_learned/

## SOPs
- `sops/engineering/code_review.md`
- `sops/engineering/testing.md`
- `sops/engineering/release_management.md`
- `sops/engineering/architecture_review.md`
- `sops/engineering/dependency_management.md`

## KPIs
| Metric | Target |
|--------|--------|
| QA Pass Rate | ≥ 90% |
| Defect Rate | < 5/MAD (Mean Agreed Deployments) |
| Test Coverage (new code) | 100% |
| Build Success Rate | ≥ 95% |
| Mean Time to Resolution | < 4h |
| Documentation Completeness | 100% for public APIs |

## Skill Registry Entries (in skills/engineering/)
- android_development/
- anr_analysis/
- performance_optimization/
- backend_api_design/
- database_architecture/
- ci_cd_pipeline/
- infrastructure_automation/
- code_review/

## Directory Structure
```
departments/engineering/
├── director-engineering@vjsos-ai.md
├── android-agent@vjsos-ai.md
├── backend-agent@vjsos-ai.md
├── infrastructure-agent@vjsos-ai.md
├── code-review-agent@vjsos-ai.md
├── qa-engineering@vjsos-ai.md
├── MANIFEST.md (this file)
├── memory/ (symlink to memory/department/engineering/)
└── skills/ (symlink to skills/engineering/)
```

## Governance
- Director reports to Governor
- QA agent reports to QA Engine + Director
- Worker agents report to Director via Orchestrator
- All cross-department requests go through Orchestrator → Governor

## Startup Dependencies
- Kernel components: Governor, Orchestrator, Context Engine, Memory Engine, QA Engine
- Plugin: github@v1.2.0 (for CI/CD, repos)
- Plugin: android-sdk@v1.0.0 (for Android builds)
- Skills registry available
- Department memory initialized

---

**Status:** Operational
**Version:** 1.0.0
**Last Updated:** 2026-08-07