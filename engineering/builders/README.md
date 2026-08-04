# Engineering — Builders

> Scaffolding tools, project generators, and boilerplate creators.

## Purpose
Generate consistent project structures with one command.

## Catalog

| Builder | Generates | Command |
|---------|-----------|---------|
| `init-android-project.py` | Android tutorial project structure | `python engineering/builders/init-android-project.py <name>` |
| `init-kids-episode.py` | Episode folder with 22-step template | `python engineering/builders/init-kids-episode.py EP-XXX` |
| `init-internal-tool.py` | Python/React boilerplate | `python engineering/builders/init-internal-tool.py <name>` |
| `init-github-repo.py` | Repo with CI, templates, protection | `python engineering/builders/init-github-repo.py <name>` |

## Template Structure

Templates live in `engineering/builders/templates/`:

```
templates/
├── android-project/
│   ├── README.md
│   ├── scripts/
│   ├── recordings/
│   └── thumbnails/
├── kids-episode/
│   ├── README.md
│   ├── 22-step-checklist.md
│   ├── scripts/
│   ├── storyboard/
│   └── render-output/
└── internal-tool/
    ├── README.md
    ├── src/
    ├── tests/
    └── .github/
```

## Creating a New Builder

1. Add template folder under `templates/`
2. Create builder script that copies + templatizes (Jinja2 or f-strings)
3. Document in this README

## Links
- [[engineering/automation/README]]
- [[governance/RepositoryRules]]