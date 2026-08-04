# ADR-0003-GitHub: Source of Truth

## Status
Accepted

## Date
2026-08-04

## Context
VJSOS needs a centralized, backed-up source of truth for all code, documentation, prompts, and assets. Options considered:
1. GitHub (public or private)
2. GitLab
3. Self-hosted Git server
4. Google Drive / Dropbox (not version-controlled)

Requirements:
- Remote backup
- Branch protection for governance files
- CI/CD integration
- Good developer experience (IDE, CLI, UI)
- Free or low cost for early stage
- Familiar to collaborators

## Decision
Use **GitHub** (github.com) as the primary remote repository.

### Implementation details
- Repository name: `vjsos` (to be renamed `vjsos/vjsos` after org creation)
- Branch protection: `main` requires PR + 1 approval + CI pass
- CI via GitHub Actions (`.github/workflows/`)
- Dependabot for dependency automation
- Issue templates for bug reports and feature requests
- Pull request template with phase classification

## Consequences

### Positive
- Industry-standard tooling and integrations
- Free for public repos (good for showcasing VJSOS methodology)
- Built-in CI/CD (GitHub Actions)
- Branch protection + required reviews for governance
- Familiar interface for collaborators
- Built-in release management
- Dependabot for dependency hygiene

### Negative
- Vendor lock-in (vendor-specific features)
- GitHub may change terms/pricing
- No offline fallback (local backup needed)

## Alternatives Considered

| Alternative | Rejected Because |
|-------------|-----------------|
| GitLab | GitHub ecosystem wider; fewer collaborators on GitLab |
| Self-hosted Git | Maintenance overhead; single point of failure |
| Google Drive/Dropbox | Not version-controlled; no CI/CD; merge conflicts |
| Not using a remote | Risk of data loss; can't collaborate |

## Related ADRs
- [[decisions/ADR-0002-Markdown]] — knowledge format
- [[decisions/ADR-0005-AIArchitecture]] — agent prompts stored in repo
- [[governance/RepositoryRules]] — repo management rules