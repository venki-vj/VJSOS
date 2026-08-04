# VJSOS Documentation Rules

## Frontmatter (Required on ALL markdown docs)

```yaml
---
title: Descriptive Title
date: 2026-08-04
version: 0.1.1
tags: [tag1, tag2, tag3]
---
```

### Required Fields
| Field | Description | Example |
|-------|-------------|---------|
| title | Page H1 heading | `VJSOS Standards` |
| date | Last updated date | `2026-08-04` |
| version | Current version | `0.1.1` |
| tags | Array of relevant tags | `[governance, standards]` |

### Optional Fields
| Field | Description |
|-------|-------------|
| aliases | Array of alternate names |
| draft | Boolean: true = hidden from production |
| author | Page owner |
| status | `draft`, `review`, `published`, `archived` |

## Wiki-Links

### Internal Links
- **Format:** `[[Page Name]]`
- **With alias:** `[[Page Name|display text]]`
- **To section:** `[[Page Name#Section Name]]`
- **Relative:** `[[docs/ARCHITECTURE]]` (from vault root)

### Link Best Practices
- Prefer wiki-links over `[[]]` when linking to known pages
- Use descriptive aliases when the page title is a concept
- Link to the canonical page, not the alias

## Content Identifiers (IDs)

### For all major artifacts:
- ADRs: `ADR-XXXX-Name`
- Assets: `assets/type/YYYY-MM-DD_name_vN`
- Episodes: `EP-XXX-title`
- Videos: `VID-XXXX-title`
- Prompts: `AGENT_ROLE.md`
- Sessions: `YYYY-MM-DD-DayN.md`

## Update Policy

### When to update docs:
- Code/config changes
- Process changes
- Decision changes (via ADR)
- New tool introduction
- Policy changes

### Update triggers:
- **Daily:** Session logs
- **On change:** Code, architecture, decisions
- **Monthly:** Metrics report
- **Quarterly:** Full review

## Version Control

- All docs stored in Git
- Changes require PR + 1 approval (docs changes only)
- Version tags on major doc updates
- Changelog tracks major doc sections

## Automation Standards

- Markdown linting: `markdownlint-cli`
- Spell checking: `.cspell.json`
- Link checking: `markdown-link-check`
- Frontmatter validation: custom script

See [[governance/Standards]] for technical details.