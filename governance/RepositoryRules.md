# VJSOS Repository Rules

## Creation Rules

| Rule | Requirement |
|------|-------------|
| Naming | `vjsos-{unit}` or `vjsos-{product}` (e.g., `vjsos-android`, `vjsos-asset-organizer`) |
| Visibility | Private by default; public with CEO approval |
| Description | One-sentence purpose in repo settings |

## Required Files (Every Repo)

| File | Purpose |
|------|---------|
| `README.md` | Project overview, quick start, links |
| `LICENSE` | MIT (or as specified) |
| `CHANGELOG.md` | Keep a Changelog format |
| `CONTRIBUTING.md` | Contribution guidelines |
| `.gitignore` | Appropriate for stack |
| `docs/` | Frontmatter-enabled documentation |

## Branch Protection (GitHub Settings)

| Setting | Value |
|---------|-------|
| Protect `main` | ✅ Required |
| Require PR | ✅ Required |
| Require approvals | 1 (code), 1 (docs) |
| Dismiss stale approvals | ✅ |
| Require status checks | ✅ CI must pass |
| Require up-to-date branches | ✅ |
| Include admins | ✅ |

## Pull Request Process

1. Create branch from `main` (`feature/`, `bugfix/`, `docs/`)
2. Make changes with conventional commits
3. Open PR with filled template
4. CI must pass (lint, tests, docs)
5. Get required approvals
6. Squash merge to `main`
7. Delete branch

## Merge Strategy

| Type | Strategy |
|------|----------|
| Feature / Bugfix | Squash merge |
| Docs | Squash merge |
| Hotfix | Merge commit (preserve history) |

## Release Process

1. Version bump in `VERSION` file
2. Update `CHANGELOG.md`
3. Tag release: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
4. Push tag: `git push origin vX.Y.Z`
5. GitHub Actions `release.yml` creates release automatically

## Archival / Deletion

- Archive after 12 months of inactivity (GitHub settings)
- Delete only with CEO approval and data backup