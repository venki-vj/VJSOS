# VJSOS Naming Convention

## Files

| Type | Pattern | Example |
|------|---------|---------|
| Markdown docs | `lowercase-hyphens.md` | `content-calendar.md` |
| Scripts (Python) | `lowercase_hyphens.py` | `render_pipeline.py` |
| Scripts (Bash) | `lowercase-hyphens.sh` | `deploy-to-github.sh` |
| Scripts (JS) | `lowercaseHyphens.js` | `validateLinks.js` |
| Assets | `YYYY-MM-DD_descriptor_version.ext` | `2026-08-04_wind-chime_bell_v1.blend` |
| Prompts | `AGENT_ROLE.md` | `CEO_AGENT.md` |
| ADRs | `ADR-XXXX-ShortName.md` | `ADR-0001-Vision.md` |
| Session logs | `YYYY-MM-DD-DayN.md` | `2026-08-04-Day1.md` |

## Folders

| Type | Pattern | Example |
|------|---------|---------|
| General | `lowercase-hyphens/` | `content-calendar/` |
| Business units | `PascalCase/` | `Android/`, `KidsStudio/` |
| Projects | `lowercase-hyphens/` | `asset-organizer/` |

## Wiki-Links (Obsidian)

- Internal: `[[Page Name]]` or `[[Page Name|display]]`
- Anchor: `[[Page Name#Section]]`
- Avoid: spaces in filenames that break links

## Frontmatter (Required)

```yaml
title: Descriptive Title
date: 2026-08-04
version: 0.1.1
tags: [tag1, tag2]
```

## Exceptions

- `README.md`, `LICENSE`, `CHANGELOG.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `VERSION` — keep standard names
- Root config files (`.gitignore`, `.github/`, etc.) — platform conventions