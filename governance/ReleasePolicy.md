# VJSOS Release Policy

## Cadence

| Release Type | Frequency | Cadence |
|-------------|-----------|---------|
| Patch | Bug fixes | As needed |
| Minor | Features, non-breaking changes | First Monday of month |
| Major | Breaking changes, new features | Planned quarterly |

## Process

### Preparation (1 week before)
- Review `CHANGELOG.md` for completeness
- Finalize version in `VERSION` file
- Get final approvals (CEO + Architect)
- Run full CI pipeline

### Cut (Release Monday)
1. **Tag release**: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
2. **Push**: `git push origin vX.Y.Z`
3. **GitHub Actions** triggered: `release.yml` automatically

### Communication (Same day)
- GitHub Release created automatically with changelog
- Internal notification (team chat, email)
- Documentation update: post-release notes in `CHANGELOG.md`

## Branch Management

### Release Branches
- `main` always points to latest release
- `vX.Y.Z` release branch (may be deleted post-merge)
- Hotfix branches created from `main`

### Hotfixes (Critical bugs)
- Created from `main`
- Merge as soon as tested (post-merge)
- No impact on `CHANGELOG.md` (use emergency channel)

## Quality Gates

| Gate | Requirement |
|------|-------------|
| Code Review | 1 approval (architect) |
| CI Status | All checks green |
| Tests | All existing tests pass |
| Documentation | Docs updated, linted |
| Branch Protection | GitHub settings enforced |

## Backout

If post-release issues found:
1. Create hotfix branch from `main`
2. Bug fix, test, push tag
3. GitHub Actions trigger release (patch)

## Version Bumping Rules

| Scenario | Version Bump |
|----------|--------------|
| New features | MINOR |
| Bug fixes | PATCH |
| Breaking changes | MAJOR |
| Internal tooling | PATCH |
| Documentation only | PATCH |

## What Gets Released

1. `README.md`
2. `LICENSE`
3. `CHANGELOG.md`
4. Source code (Git repository)
5. Website assets (if any)
6. Documentation (if versioned)

## Links

- [[governance/Standards]]
- [[CHANGELOG]]
- [[governance/Versioning]]