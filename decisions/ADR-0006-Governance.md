# ADR-0006-Governance: Internal Standards System

## Status
Accepted

## Date
2026-08-05

## Context
VJSOS needs a standards system to:
1. Define the rules of operation
2. Create fairness and clarity for contributors
3. Scale without chaos
4. Make onboarding easier
5. Ensure consistency across teams

Options considered:
- No formal standards (organic growth)
- A single governance document (GDPR-like)
- Decentralized standards per team
- Multi-level governance (global, team, personal)

## Decision
Implement a **multi-tiered governance** with three levels:

### Level 1: Global Standards (`governance/`)
- `Standards.md` — core coding, file organization, review rules
- `NamingConvention.md` — naming patterns, wiki-links, IDs
- `RepositoryRules.md` — repo creation, branch protection, process
- `DocumentationRules.md` — frontmatter, wiki-links, update cadence
- `MarkdownStyleGuide.md` — headings, lists, tables, code, frontmatter
- `Versioning.md` — Semantic Versioning rules, tagging
- `ReleasePolicy.md` — release cadence, hotfixes

### Level 2: Team Standards (per business unit)
- Config per project: `.github/workflows/`, `.github/ISSUE_TEMPLATE/`
- Project-specific CONTRIBUTING.md
- Local documentation rules

### Level 3: Personal Preferences
- Git user config
- Obsidian settings
- IDE configurations

### Governance Mechanisms
- **ADRs:** Architecture Decision Records (for major decisions)
- **SOPs:** Standard Operating Procedures (for daily operations)
- **Checklists:** Workflow steps
- **Templates:** GitHub, documentation
- **Metrics:** KPIs, OKRs, dashboards

## Consequences

### Positive
- Clear, documented rules for all operations
- Easy onboarding (contributors find standards quickly)
- Scalability (teams can have their own level 2 rules)
- Traceable decision-making via ADRs
- Consistency across all artifacts (docs, code, prompts)
- Reduced friction

### Negative
- Some overhead to maintain multiple documents
- May feel bureaucratic initially
- Requires discipline to keep updated

## Alternatives Considered

| Alternative | Rejected Because |
|-------------|-----------------|
| No formal standards | Chaos at scale; unclear expectations |
| Single mega-document | Too rigid; hard to maintain |
| Fully decentralized | Inconsistency; duplicate effort |

## Related ADRs
- [[decisions/ADR-0002-Markdown]] — knowledge format
- [[decisions/ADR-0008-Kernel]] — immutable core references governance