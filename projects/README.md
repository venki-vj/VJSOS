# VJSOS Projects

> Business unit project directories.

Each business unit and product has its own structured project folder. These may be independent Git repositories in the future, but are tracked by the VJSOS umbrella repo for consistency.

## Project Index

| Project | Business Unit | Status | Repo |
|---------|---------------|--------|------|
| [[projects/Android]] | Creator Education | Active | vjsos-android |
| [[projects/KidsStudio]] | Kids Entertainment | Pre-production | vjsos-kids-studio |
| [[projects/InternalTools]] | Internal Software | Active | vjsos-tools |
| [[projects/PlayStore]] | App Publishing | Planning | vjsos-playstore |
| [[projects/OpenSource]] | Community | Planning | vjsos-open-source |

## Structure Convention

Each project folder follows:

```
{project}/
├── README.md
├── VERSION
├── docs/
├── src/
├── tests/
└── assets/
```

## Git Strategy

| Project | Strategy |
|---------|----------|
| Android | Subtree in monorepo or separate repo |
| KidsStudio | Separate repo when animation begins |
| InternalTools | Separate repo (product-ready) |
| Others | Monorepo for now |

## Links

- [[docs/ARCHITECTURE]]
- [[company/Organization]]
- [[prompts/PROJECT_MANAGER]]