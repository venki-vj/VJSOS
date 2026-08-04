# Changelog

All notable changes to VJSOS are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- GitHub branch protection configuration
- First Android tutorial script (Video #13)
- Kids Studio Episode 1 script draft

## [v0.1.1] - 2026-08-05

### Added
- Company folder (`company/`) with Mission, Vision, CoreValues, Culture, Organization, BusinessModel
- Governance layer (`governance/`) with Standards, NamingConvention, RepositoryRules, DocumentationRules, MarkdownStyleGuide, Versioning, ReleasePolicy
- Immutable Kernel (`kernel/`) with Mission, Vision, CorePrinciples, CoreWorkflow, ExecutionCycle, Interfaces, Standards
- Knowledge graph (`knowledge/`) with README, index, graph-schema
- Metrics layer (`metrics/`) with OKRs, KPIs, Analytics, QuarterlyReports, MonthlyReports
- Engineering tools (`engineering/`) with automation, scripts, builders, ENGINES
- All 8 Architecture Decision Records (`decisions/ADR-0001` through `ADR-0008`)
- Full architecture specification (`docs/ARCHITECTURE_SPEC.md`)

### Changed
- Restructured the repo to an Operating System-style architecture
- `tools/` relocated into `engineering/`
- README updated with new structure
- MASTER_CONTEXT updated to v0.1.1

## [v0.1.0] - 2026-08-04

### Added
- Initial repository structure
- Core documentation suite (`docs/`)
  - MASTER_CONTEXT, VISION, PRINCIPLES, ROADMAP, INFRASTRUCTURE
- Agent prompt library (`docs/prompts/`) — 8 agents
- Standard Operating Procedures (`docs/sop/`) — DAILY, WEEKLY, MONTHLY
- Obsidian vault (`obsidian-vault/`) with Welcome, Dashboard, config
- Day 1 session log (`obsidian-vault/sessions/2026-08-04_day1.md`)
- GitHub infrastructure (`.github/`) — CI, releases, dependabot, templates
- CI workflow for lint, docs validation, JSON config checks

### Changed
- Established VJSOS as a multi-business-unit content + software studio

### Fixed
- CI workflow: removed Node.js build-test job (documentation-only repo had no package.json)