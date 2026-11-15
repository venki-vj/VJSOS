# VJSOS-AI Memory Architecture

**4-Tier Memory Model**
**Version:** 1.0.0
**Last Updated:** 2026-08-07

---

## Overview

VJSOS-AI uses a 4-tier memory architecture inspired by human cognitive systems — from immediate recall (Session) to institutional wisdom (Global).

```
┌─────────────────────────────────────────────────┐
│ TIER 4: GLOBAL  (∞ TTL, Governor-owned)         │
│ Constitution, Company Vision, Core Principles   │
├─────────────────────────────────────────────────┤
│ TIER 3: DEPARTMENT (∞ TTL, Director-owned)      │
│ Department SOPs, Knowledge, Patterns            │
├─────────────────────────────────────────────────┤
│ TIER 2: AGENT (180d TTL, Agent-owned)           │
│ Domain knowledge, skill expertise, lessons      │
├─────────────────────────────────────────────────┤
│ TIER 1: SESSION (24h TTL, Current conversation) │
│ Task context, immediate working memory          │
└─────────────────────────────────────────────────┘
```

---

## Tier Details

| Tier | Name | Scope | Owner | TTL | Dedup Threshold |
|------|------|-------|-------|-----|-----------------|
| 1 | Session | Current conversation | Agent | 24h | 0.95 |
| 2 | Agent | Domain expertise | Agent | 180d | 0.95 |
| 3 | Department | Department knowledge | Director | ∞ | 0.95 |
| 4 | Global | Organizational knowledge | Governor | ∞ | 0.95 |

---

## Read/Write Rules

| Operation | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|-----------|--------|--------|--------|--------|
| Agent read | ✅ | ✅ | ✅* | ✅* |
| Agent write | ✅ | ✅ | ❌ | ❌ |
| Director read | ✅ | ✅ | ✅ | ✅ |
| Director write | ❌ | ❌ | ✅ | ❌ |
| Governor read | ✅ | ✅ | ✅ | ✅ |
| Governor write | ❌ | ❌ | ✅ | ✅ |
| *Context Engine can pull from tiers 3 & 4 | | | | |

---

## Directory Structure

```
memory/
├── README.md              ← This file
├── session/               ← Tier 1: Session memory (24h TTL)
│   ├── README.md
│   └── {correlation_id}/
│       ├── context.json
│       ├── conversation.md
│       └── working_notes.md
├── agent/                 ← Tier 2: Agent memory (180d TTL)
│   ├── README.md
│   └── {agent_id}/
│       ├── expertise.md
│       ├── skill_history.md
│       ├── lessons_learned.md
│       └── feedback_log.md
├── department/            ← Tier 3: Department memory (∞ TTL)
│   ├── README.md
│   └── {department}/
│       ├── MANIFEST.md
│       ├── sops/
│       ├── knowledge_base.md
│       ├── patterns.md
│       └── runbooks/
├── global/                ← Tier 4: Global memory (∞ TTL)
│   ├── README.md
│   ├── constitution.md    ← Copy of AI_CONSTITUTION.md
│   ├── decisions.md        ← Governor decision log
│   └── vision.md           ← Company vision and values
└── engine.md              ← Memory Engine prompt (from kernel)
```

---

## Deduplication

Memory Engine enforces deduplication at 0.95 semantic similarity threshold:

- **Content dedup:** Exact or near-duplicate text
- **Semantic dedup:** Embedding-based semantic similarity

When a memory is marked for storage, the engine:
1. Generates embedding of content
2. Searches for similar existing memories (same tier)
3. If `similarity > 0.95`: reference existing, don't store duplicate
4. If `similarity ≤ 0.95`: store new memory with link to related memories

---

## Memory Object Schema

```json
{
  "memory_id": "mem_20260807_123456_abc123",
  "tier": 1,
  "owner": "android-agent@engineering@vjsos-ai",
  "type": "context | expertise | decision | pattern | lesson | SOP",
  "correlation_id": "corr_789xyz",
  "created_at": "2026-08-07T12:34:56Z",
  "expires_at": "2026-08-08T12:34:56Z",  // null for ∞ TTL
  "content": {
    "summary": "Brief summary of memory content",
    "body": "Full memory content",
    "embedding": [0.1, 0.2, ...]  // 768-dim vector
  },
  "context": {
    "related_memories": ["mem_...", "mem_..."],
    "parent_memory": null,
    "source": "agent_output | human_input | qa_feedback"
  },
  "governance": {
    "access_level": "read | read_write | restricted",
    "audit_trail": ["mem_..."],
    "tags": ["android", "kotlin", "performance"]
  },
  "lifecycle": {
    "version": "1.0.0",
    "status": "active | deprecated | archived",
    "last_reviewed": "2026-08-07T12:34:56Z",
    "review_interval_days": 180
  }
}
```

---

## Initialization

On system bootstrap (Phase 0, Step 6 of Bootstrap Sequence):

1. **Tier 4 (Global)** loads first:
   - Constitution
   - Company Vision
   - Governor decision log

2. **Tier 3 (Department)** loads next:
   - Department MANIFEST.md → memory/department/
   - SOPs
   - Knowledge base

3. **Tier 2 (Agent)** loads on-demand:
   - Agent manifests
   - Expertise documents
   - Skill history

4. **Tier 1 (Session)** is ephemeral:
   - Created per task
   - Destroyed after 24h

---

## See Also

- `docs/specs/KERNEL_SPEC.md#4-memory-engine` — Technical specification
- `docs/specs/AI_OPERATING_SYSTEM_SPEC.md#3-context-engine` — Context integration
- `docs/AI_CONSTITUTION.md` — Article IV (Rule 4: No Knowledge Duplication)