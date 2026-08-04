---
title: VJSOS — Master Context for Local LLM
date: 2026-08-04
version: 0.1.0
project: VJSOS
tags: [vjsos, architecture, youtube, android, ai, startup, master-context]
---

# VJSOS — Master Context for Local LLM

**Load this file first** when initializing any local LLM session for VJSOS work. It provides the high-level framing, key decisions, and pointers to all other documentation.

---

## What is VJSOS?

VJSOS (VJ Studios / VJ Systems of Software) is a **multi-business-unit content + software studio** founded 2026-08-04 by Venkatesh. It operates as a three-layer system:

| Layer | Name | Function | Hardware Need |
|-------|------|----------|---------------|
| 1 | **Brain** | Documentation, planning, knowledge, research, prompt engineering, Git, Obsidian | Current laptop ✅ |
| 2 | **Factory** | Rendering, animation, local AI, video production | Bottleneck on current laptop ⚠️ |
| 3 | **Data Center** | Dedicated render machine, AI workstation, NAS, backup server, GPU server | Future investment 🔮 |

**Core Principle:** *Build capability before buying capacity.* Hardware accelerates a working system; it doesn't replace one.

---

## Business Units

1. **Android Channel** — YouTube channel: tutorials, how-to, AI tools for Android devs, Windows/Office/CapCut/Notion/GitHub/Android Studio tutorials, device fixes, skill tutorials. Primary language: English + Hindi/Telugu for India reach + global export.
2. **Kids Studio** — "Mystery Makers Club" animated series (3–5 min episodes, ages 6–12). Characters: Mira, Bo, Nila, Pip, Professor Pebble. Setting: Brightbucket Bay. Production pipeline: 22-agent workflow → Blender rigged 2D animation → professional quality.
3. **Software Products** — Tools, agents, utilities built internally and potentially commercialized.

---

## Key Documentation (All in `docs/`)

| File | Purpose |
|------|---------|
| `VISION.md` | Company vision, mission, long-term direction |
| `PRINCIPLES.md` | Operating principles, decision-making rules |
| `ROADMAP.md` | Phased roadmap with milestones |
| `ARCHITECTURE.md` | Technical architecture, stack choices |
| `DECISIONS.md` | Decision log (ADRs) |
| `BUSINESS_UNITS.md` | Details per business unit |
| `DAILY_EXECUTION.md` | Daily workflow, habits, rituals |
| `WEEKLY_SPRINTS.md` | Sprint structure, planning, review |
| `INFRASTRUCTURE.md` | Hardware phases, server topology, upgrade triggers |
| `AI_WORKFORCE.md` | Agent roles, prompts, orchestration |
| `KNOWLEDGE_GRAPH.md` | How knowledge is organized, linked, retrieved |
| `ANDROID_CHANNEL.md` | Channel strategy, content pillars, series |
| `KIDS_STUDIO.md` | Series bible, production pipeline, episode tracker |
| `SOFTWARE_PRODUCTS.md` | Product ideas, specs, status |
| `CHANGELOG.md` | Version history of VJSOS itself |

---

## Prompts & SOPs

- `prompts/` — Agent system prompts (CEO, Architect, Research, PM, etc.)
- `sop/` — Standard Operating Procedures (Daily, Weekly, Monthly)
- `sessions/` — Session logs by date (e.g., `2026-08-04_DAY1.md`)

---

## Hardware Reality (Current: Acer Aspire E5-573, ~2015-16, Intel iGPU, Win 11)

| Phase | Capability | Status |
|-------|------------|--------|
| 1 | Planning, docs, Git, Obsidian, VS Code, research, architecture | ✅ 100% |
| 2 | Python, FastAPI, SQLite, React, Electron, Android dev, basic agents | ✅ 90% |
| 3 | Remotion, FFmpeg, light Blender, image gen, local 7B LLM, video render | ⚠️ Slow |
| 4 | 30B–70B models, high-quality Blender, 4K, training, Unreal, render farms | ❌ No |

**Upgrade triggers:** When Phase 3 work genuinely blocks revenue/capability, not before.

---

## YouTube 2026 Strategy (Condensed)

- **Niche:** One niche + three pillars + one promise/video + one repeatable format + one audience.
- **Top niches for India:** How-to/tutorial, Education/career, Product reviews, Gaming/fandom, Behind-the-scenes/podcasts, Shorts.
- **Packaging:** Title promises ONE thing. Thumbnail shows outcome/problem. First 5–10s matches title. No clickbait.
- **Analytics:** CTR first 24h (Home/Suggested + Subs). Watch time: absolute for long, relative for short.
- **Timing test:** Weekdays 6:30–9:30 PM IST, Weekends 10 AM–1 PM, Shorts 12–2 PM & 7–10 PM. After 10–15 uploads, use own data.
- **India advantage:** 100M+ channels, 15K+ at 1M subs, 45B hours India-content watched globally. Local language + global topic + clean packaging = highest upside.

---

## How to Use This Context

1. Load `MASTER_CONTEXT.md` first
2. Load relevant domain file (e.g., `KIDS_STUDIO.md` for animation work)
3. Load relevant prompt from `prompts/` for agent role
4. Load relevant SOP from `sop/` for process
5. Append session notes to `sessions/YYYY-MM-DD_DAYN.md`
6. Update `CHANGELOG.md` when decisions change

---

## Current Sprint: VJSOS v0.1 — Foundation

**Goal:** Complete repository structure, initial docs, architecture decisions, templates, prompt library, SOPs, daily/weekly execution system, git-ready Markdown, Obsidian-ready [[wiki]] links, local-LLM-ready context files.

**Status:** Day 1 — creating documentation pack and git repo.

---

## Links

- Source guide: [[vjsos-guide-context]]
- Company vision: [[vjsos-company-vision]]
- Infrastructure facts: [[vjsos-infrastructure-facts]]
- Project root: `C:\Users\venki\Claude\Projects\VJSOS\`
- Obsidian vault: `C:\Users\venki\Claude\Projects\VJSOS\obsidian-vault\`