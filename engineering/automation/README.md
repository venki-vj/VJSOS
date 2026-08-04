# Engineering — Automation Layer

> CI/CD, pipeline automation, and deployment scripts.

## Purpose

Automation removes human error and frees mental capacity for creative work.

## Current Automations

| Name | Trigger | Function |
|------|---------|----------|
| `docs-validate.yml` | On PR | Validate markdown frontmatter, check wiki-links |
| `ci.yml` | On push/PR | CI (lint, validate, test) |
| `release.yml` | On tag | Create GitHub release from CHANGELOG |
| `dependabot.yml` | Daily | Update GitHub Actions + npm deps |

## Pipeline Overview

```
┌──────────┐    ┌─────────┐    ┌──────────┐
│  Content  │───→│  Script  │───→│   Render  │
│  Created  │    │  Tool    │    │  Engine    │
└──────────┘    └─────────┘    └──────────┘
                        │
                        ▼
                    ┌──────────┐
                    │  Post to  │
                    │  YouTube  │
                    └──────────┘
```

## Future Automations (Roadmap)

| # | Idea | Phase |
|---|------|-------|
| 1 | Daily session log parser → Obsidian graph | Phase 2 |
| 2 | YouTube upload automation | Phase 2 |
| 3 | Render queue manager (multiple jobs) | Phase 2 |
| 4 | Asset naming + tagging bot | Phase 2 |

## Adding a New Automation

1. Create `engineering/scripts/new-automation.sh`
2. Document it in this README
3. Add a GitHub Action if it's a CI trigger
4. Assign a KPI (see [[metrics/KPIs]])

## Links

- [[engineering/]], [[decisions/ADR-0003-GitHub]]
- `.github/workflows/` directory
- [[metrics/OKRs]]