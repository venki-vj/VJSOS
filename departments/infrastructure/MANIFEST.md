# Infrastructure Department Manifest

**Department ID:** infrastructure
**Director:** `director-infrastructure@vjsos-ai`
**Constitution Article:** V, VI

---

## Mission
Provide and maintain the technical infrastructure, tools, and platforms required for organizational operations with reliability, security, and cost-efficiency.

## Domains
- infrastructure — IaC, CI/CD, deployment, monitoring, security

## Worker Agents
| Agent ID | Type | Skills |
|----------|------|--------|
| `devops-agent@infrastructure@vjsos-ai` | Worker | infrastructure_management, ci_cd_pipeline, deployment, monitoring, security |

## QA Agent
`qa-infrastructure@vjsos-ai` — Enforces `infrastructure_qa_rubric_v2.0`

## Memory Scope
`memory/department/infrastructure/` — contains:
- architecture_standards.md
- security_policies.md
- cost_governance.md
- qa_rubric.md
- runbooks/
- disaster_recovery.md
- lessons_learned/

## SOPs
- `sops/infrastructure/iac_development.md`
- `sops/infrastructure/security_review.md`
- `sops/infrastructure/disaster_recovery.md`
- `sops/infrastructure/change_management.md`

## KPIs
| Metric | Target |
|--------|--------|
| QA Pass Rate | ≥ 90% |
| Uptime | ≥ 99.9% |
| Security Critical Findings | 0 |
| Rollback Time | < 5min |
| Error Budget Burn/deploy | < 2% |
| Cost Awareness | Budget alerts at 80% |

## Skill Registry Entries (in skills/infrastructure/)
- infrastructure_management/
- ci_cd_pipeline/
- observability/

## Directory Structure
```
departments/infrastructure/
├── director-infrastructure@vjsos-ai.md
├── devops-agent@vjsos-ai.md
├── qa-infrastructure@vjsos-ai.md
├── MANIFEST.md (this file)
├── memory/ (symlink to memory/department/infrastructure/)
└── skills/ (symlink to skills/infrastructure/)
```

## Governance
- Director reports to Governor
- QA agent reports to QA Engine + Director
- Production infra changes require Director + rollback plan
- Security incidents escalate to Governor immediately
- All cross-department requests go through Orchestrator → Governor

## Startup Dependencies
- Kernel components: Governor, Orchestrator, Context Engine, Memory Engine, QA Engine
- Plugin: terraform@v1.0.0, kubernetes@v1.0.0, github@v1.2.0
- Skills registry available
- Department memory initialized

---

**Status:** Operational
**Version:** 1.0.0
**Last Updated:** 2026-08-07