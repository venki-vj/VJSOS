# VJSOS Versioning Policy

> Based on [Semantic Versioning 2.0.0](https://semver.org/).

## Format

```
MAJOR.MINOR.PATCH
```

### MAJOR
Incompatible changes to API, architecture, or breaking decisions.

### MINOR
New functionality, features, non-breaking additions.

### PATCH
Bug fixes, documentation updates, small tweaks.

## What Gets Versioned

| Artifact | Versioning |
|----------|------------|
| Docs / SOPs | Version in frontmatter |
| Prompts | Version in frontmatter |
| ADRs | Version in frontmatter |
| Assets | Version suffix: `_vN` |
| Products | SemVer on release |
| Infrastructure | ADR-style versioning |

## Version Tags (Git)

```
v0.1.0    → Major release
v0.1.1    → Patch release
v0.2.0    → Minor feature release
v1.0.0    → First production release
```

### Tagging
```bash
git tag -a v0.1.1 -m "Release v0.1.1"
git push origin v0.1.1
```

## Dependencies

All dependencies must be version-pinned:
- `requirements.txt`: `package==1.2.3`
- `package.json`: `"package": "1.2.3"`
- `Dockerfile`: `FROM image:tag`

## Release Branches

| Branch | Purpose |
|--------|---------|
| `main` | Release-ready, always versioned |
| `develop` | Integration branch (future) |
| `v0.1.0` | Release branch for v0.1.0 |
| `hotfix/v0.1.1` | Hotfix branch |

## Automation

GitHub Actions `release.yml` automates:
- Version tag triggers release
- CHANGELOG.md → release notes
- GitHub Release creation

## Changelog Format

See [[CHANGELOG]] for template. Keep a Changelog standard:
- `[v0.2.0] - YYYY-MM-DD` headers
- `### Added`, `### Changed`, `### Removed`
- Bullet points, concise

## Deprecation

Before removing:
1. Mark deprecated in current version
2. Wait 1 minor release cycle
3. Remove in next MAJOR release

## Links

- [[governance/Standards]]
- [[governance/ReleasePolicy]]
- [[CHANGELOG]]