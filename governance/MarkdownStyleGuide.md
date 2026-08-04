# VJSOS Markdown Style Guide

> Consistency across all VJSOS documentation.

## Headings

| Level | Syntax | Usage |
|-------|--------|-------|
| H1 | `# Title` | Once per document (from `title` frontmatter) |
| H2 | `## Section` | Major sections |
| H3 | `### Subsection` | Subdivisions |
| H4 | `#### Detail` | Inline details, rare |

### Heading Style
- **Sentence case** for short docs
- **Capitalized** for formal documents (VISION, MISSION, etc.)
- **No trailing periods**

## Lists

### Unordered Lists

```markdown
- Item one
- Item two
  - Nested item (2-space indent)
  - Another nested
- Item three
```

### Ordered Lists

```markdown
1. First item
2. Second item
   1. Nested (3-space indent after number)
3. Third item
```

### Task Lists (for checklists)

```markdown
- [ ] Unfinished task
- [x] Done task
```

## Tables

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Cell 1,1 | Cell 1,2 | Cell 1,3 |
| Cell 2,1 | Cell 2,2 | Cell 2,3 |

**Rules:**
- Always include header separator (`---`)
- Pad columns with `-` characters
- Keep table width reasonable (< 100 chars)
- Use tables for structured data, not prose

## Code Blocks

### Inline Code
`inline code` for file names, snippets, variables.

### Fenced Blocks
\`\`\`language
// Specify language for syntax highlighting
\`\`\`

### Common Languages
- `markdown` for Markdown examples
- `yaml` for frontmatter
- `bash` for shell commands
- `python` for Python
- `javascript`, `typescript`
- `mermaid` for diagrams

## Frontmatter

Every document must start with:

```yaml
---
title: Title Here
date: YYYY-MM-DD
version: X.Y.Z
tags: [tag1, tag2]
---
```

## Links

### External Links
`[display text](https://example.com)`

### Internal Links (Wiki-Links)
`[[Page Name]]`

### Anchor Links
`[Section](#section-name)`

## Emphasis

- `**bold**` for strong emphasis
- `*italic*` for mild emphasis
- `**_bold and italic_**` combined (rare)

## Blockquotes
`> Quote text`
Prefer sparingly; use for key quotes or notes only.

## Horizontal Rules
Use `---` sparingly (between major sections only).

## Images

```markdown
![Alt text](path/to/image.png)
{: .center }  <!-- Center alignment if needed -->
```

**Alt text:** Required. Describe purpose, not just content.

## Callouts / Admonitions

Use blockquotes with emoji prefix:

```markdown
> 📌 Note: This is a note
> More details here.

> ⚠️ Warning: This is a warning
> Important information.

> ✅ Pro Tip: This is a tip
> Helpful technique.
```

## File Naming

- Lowercase
- Hyphens for spaces
- No special characters
- Descriptive names

## Content Structure

1. Frontmatter
2. H1 Title (from frontmatter `title`)
3. Brief intro (1-2 sentences)
4. H2 Sections for main content
5. H2 References / Links (optional)

## Version Notes

When documenting versions:
- Use `v0.1.0` format (no `v` in Version control tags in Git)
- Dates: `YYYY-MM-DD` format (ISO 8601)
- Times: `HH:MM AM/PM IST` (or specify timezone)