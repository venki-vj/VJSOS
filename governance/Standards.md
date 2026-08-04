# VJSOS Standards

## Coding Standards

### Python
- Ruff (line-length 100, target py311)
- Type hints for public APIs
- Docstrings for modules, classes, functions

### JavaScript / TypeScript
- ESLint + Prettier
- ES2022 modules
- Strict TypeScript config

### Bash
- `set -euo pipefail`
- Functions over inline scripts
- ShellCheck clean

## File Organization

```
VJSOS/
├── README.md
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── VERSION
├── .github/
│   ├── workflows/
│   ├── ISSUE_TEMPLATE/
│   └── dependabot.yml
├── company/
├── governance/
├── kernel/
├── knowledge/
├── metrics/
├── prompts/
├── projects/
├── engineering/
├── assets/
├── decisions/
├── docs/
└── obsidian-vault/
```

## Commit Message Format

```
type(scope): subject

[optional body]

[optional footer: issue refs]
```

| Type | Meaning |
|------|---------|
| feat | New feature |
| fix | Bug fix |
| docs | Documentation only |
| style | Formatting, no logic change |
| refactor | Code restructuring |
| test | Add or modify tests |
| chore | Maintenance, dependencies |
| build | Build system, CI |
| perf | Performance improvement |

**Scope**: `docs`, `engineering`, `projects/android`, `projects/kids-studio`, `governance`, `kernel`, etc.

**Examples**:
- `feat(android): add CapCut tutorial series`
- `fix(kids-studio): correct Episode 1 timing`
- `docs(governance): add NamingConvention`

## Branch Strategy

- `main` — protected, release-ready
- `feature/*` — new work (feature, fix, docs)
- `hotfix/*` — emergency fixes from `main`

**Rules**:
- Branch from `main`
- PR required for all merges
- At least 1 approval (code), 1 approval (docs)
- CI must pass
- Squash merge preferred

## Review Requirements

| Change Type | Approvers |
|-------------|-----------|
| Code (Python/JS) | 2 |
| Documentation | 1 |
| Config/CI | 1 |
| Assets | 1 |

## Documentation Standards

See [[governance/DocumentationRules]], [[governance/MarkdownStyleGuide]], [[governance/Versioning]], [[governance/ReleasePolicy]]