# Global Memory Tier

**TTL:** infinite
**Scope:** governor
**Created:** 2026-11-15T11:42:44.660763Z

## Purpose
This tier stores memory entries that persist for the specified TTL and scope.

## Structure
- Keys are UUID-based identifiers
- Each entry is a JSON file with metadata and content
- Deduplication uses semantic similarity threshold (0.95)

## Access
- **Session** tier: Agent-scoped, auto-purged after 24h
- **Agent** tier: Agent-scoped, purged after 180 days of inactivity
- **Department** tier: Department-scoped, requires director approval
- **Global** tier: Governor-scoped, requires Governor approval for modifications
