# Engineering — Scripts

> Utility scripts for daily operations.

## Purpose
One-off and reusable scripts that automate routine tasks.

## Catalog

| Script | Language | Purpose |
|--------|----------|---------|
| `parse-session-log.py` | Python | Parse daily session logs into structured JSON |
| `validate-frontmatter.py` | Python | Check all markdown files have required frontmatter |
| `check-wiki-links.py` | Python | Validate internal wiki-links resolve |
| `gen-changelog.py` | Python | Auto-generate CHANGELOG from commit messages |
| `backup-obsidian.sh` | Bash | Sync obsidian-vault to backup drive |
| `render-queue.py` | Python | Manage Blender render jobs with priorities |
| `upload-youtube.py` | Python | YouTube upload with metadata from JSON |

## Adding a Script

1. Create in `engineering/scripts/`
2. Add shebang, docstring, CLI interface
3. Update this README
4. Consider if it belongs in `engineering/automation/` (CI-triggered) instead

## Execution

```bash
# From repo root
python engineering/scripts/parse-session-log.py --date 2026-08-05
```

## Links
- [[engineering/automation/README]]
- [[governance/Standards]]