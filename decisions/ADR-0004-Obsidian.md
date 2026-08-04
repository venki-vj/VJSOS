# ADR-0004-Obsidian: Knowledge Vault

## Status
Accepted

## Date
2026-08-04

## Context
VJSOS produces hundreds of Markdown files (docs, prompts, SOPs, session logs). We need a way to view, navigate, and query these as a connected knowledge base (not a flat file structure).

Requirements:
- Graph view of wiki-links
- Full-text search
- Daily notes (session logging)
- Local-first (works offline)
- Free or low-cost
- Works with Markdown + wiki-links

## Decision
Adopt **Obsidian** as the primary knowledge management interface, using its vault feature to point at the VJSOS `obsidian-vault/` directory (which contains symlinks/copies of docs).

### Implementation
- Vault location: `/c/Users/venki/Claude/Projects/VJSOS/obsidian-vault/`
- Daily notes: `sessions/YYYY-MM-DD-DayN.md` (manages daily session logs)
- Templates: Welcome.md, Dashboard.md, session log template
- Core plugins enabled: file explorer, graph, backlinks, daily notes, templates
- Appearance: dark theme, teal accent color

## Consequences

### Positive
- Powerful graph view for finding connections
- Full-text search across all docs
- Daily notes feature maps perfectly to session logging
- Local-first: no internet required
- Free for personal use (sufficient for early stage)
- Template system for consistent docs

### Negative
- Desktop app only (not web-based)
- No real-time collaboration (single-user locally)
- Vault sync via Git (manual or third-party)
- Some features require paid Sync plan (not needed yet)

## Alternatives Considered

| Alternative | Rejected Because |
|-------------|-----------------|
| Notion | Not local-first, vendor lock-in |
| Roam Research | Expensive, web-only |
| VS Code + extensions | Good but less focused on graph view |
| Plain Git web UI | Poor search and no graph view |

## Related ADRs
- [[decisions/ADR-0002-Markdown]] — knowledge format
- [[decisions/ADR-0001-Vision]] — part of Brain layer
- [[knowledge/README]] — knowledge graph schema