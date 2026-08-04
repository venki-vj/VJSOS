# ADR-0002-Markdown: Knowledge Format Standard

## Status
Accepted

## Date
2026-08-04

## Context
VJSOS needs a knowledge format that is:
1. Version-controlled with Git
2. Linkable (cross-references between documents)
3. Local-first (no vendor lock-in)
4. Portable to local LLMs
5. Human-readable in plain text
6. Structured enough for programmatic queries

Available options included Notion, Confluence, Obsidian (Markdown), custom CMS, and plain text.

## Decision
Adopt **Markdown with YAML frontmatter** as the single knowledge format, stored in a Git monorepo, viewed/navigated with **Obsidian** (for the graph view and wiki-link support).

### Key rules
- Every Markdown file has frontmatter (`title`, `date`, `version`, `tags`)
- Internal links use wiki-link notation: `[[Page Name]]`
- All docs are stored flat in directory structure under `docs/`, `prompts/`, `knowledge/`, etc.
- Obsidian vault is the `obsidian-vault/` directory (symlinks to docs for unified graph)

## Consequences

### Positive
- Git history for every decision, doc, and prompt
- Wiki-links create a natural knowledge graph
- Works offline, no vendor lock-in
- Importable into local LLMs (LLaMA Index, etc.)
- Obsidian graph view + search is powerful for discovery
- Plain text = survives tool changes

### Negative
- No database-style query language by default
- Merge conflicts in Markdown can need manual resolution
- Image embedding is file-path based (more on file system)
- Some formatting flexibility is lost (no rich text)

## Alternatives Considered

| Alternative | Rejected Because |
|-------------|-----------------|
| Notion | No local control, vendor lock-in, no Git |
| Confluence | Expensive, enterprise-focused, no local-first |
| Custom CMS | Overkill for a studio of 1; requires hosting/maintenance |
| Plain text only | No structure, hard to query programmatically |
| JSON/YAML only | Human-unfriendly, loses readability |

## Related ADRs
- [[decisions/ADR-0003-GitHub]] — Git hosting
- [[decisions/ADR-0004-Obsidian]] — Obsidian as viewer
- [[governance/MarkdownStyleGuide]] — style conventions