---
title: VJSOS Architecture
date: 2026-08-05
version: 0.1.2
tags: [architecture, kernel, multi-agent, orchestration]
---

# VJSOS Architecture

> The operating system for independent media studios.

## System Overview

```
VJSOS Kernel
           │
    ┌──────┼──────┐
    │      │      │
Memory Engine  Task Planner  Knowledge Base
    │      │      │
    └──────┼──────┘
           │
   Multi-Agent Orchestrator
           │
┌──────┬──────┬──────┬──────┐
│      │      │      │
Claude  ChatGPT  Gemini  Local LLMs
│      │      │      │
└──────┴──────┴──────┘
           │
   Git • Bash • Docker • Blender • AOSP
```

---

## Layer Definitions

### 1. VJSOS Kernel (Immutable Core)

The kernel is the source of truth — never changes without formal process.

| Component | File | Purpose |
|-----------|------|---------|
| Mission | `kernel/Mission.md` | One-line mission + North Star |
| Vision | `kernel/Vision.md` | Long-term picture |
| CorePrinciples | `kernel/CorePrinciples.md` | 7 operating values |
| CoreWorkflow | `kernel/CoreWorkflow.md` | 5-step execution cycle |
| ExecutionCycle | `kernel/ExecutionCycle.md` | Daily/weekly/monthly/quarterly rhythms |
| Interfaces | `kernel/Interfaces.md` | Contracts between layers |
| Standards | `kernel/Standards.md` | Pointer to governance/Standards.md |

**Authority:** CEO + Architect approval required for changes.

---

### 2. Memory Engine

Persistent, queryable memory across sessions and agents.

| Subsystem | Technology | Location |
|-----------|------------|----------|
| Working Memory | Local agent context | In-session |
| Episodic Memory | Session logs | `obsidian-vault/sessions/` |
| Semantic Memory | Knowledge graph | `knowledge/` + wiki-links |
| Procedural Memory | SOPs, prompts | `docs/sop/`, `prompts/` |
| Vector Memory | Embeddings for search | Future: local embedding index |

**Key principle:** Everything written is retrievable. No knowledge loss.

---

### 3. Task Planner

Decomposes goals into executable tasks with phase awareness.

| Capability | Implementation |
|------------|----------------|
| Goal decomposition | Project Manager agent |
| Phase classification | [[governance/Standards]] Phase 1-4 |
| Dependency resolution | DAG from task graph |
| Scheduling | Sprint + daily blocks |
| Blocking detection | Project Manager escalation |

---

### 4. Knowledge Base

Structured, linkable knowledge graph.

| Layer | Implementation |
|-------|----------------|
| Entities | Markdown files with frontmatter IDs |
| Relationships | Wiki-links `[[Page]]` |
| Schema | `knowledge/graph-schema.md` |
| Index | `knowledge/index.md` |
| Query | Obsidian graph view + search |
| Validation | CI link checking |

---

### 5. Multi-Agent Orchestrator

Coordinates 14 specialized AI agents.

| Agent | Role | Prompt | KPIs |
|-------|------|--------|------|
| CEO | Strategy, allocation | `prompts/CEO_AGENT.md` | OKR completion |
| Architect | Tech design, pipelines | `prompts/ARCHITECT_AGENT.md` | ADR quality |
| Research | Market validation | `prompts/RESEARCH_AGENT.md` | Insight accuracy |
| Project Manager | Sprint execution | `prompts/PROJECT_MANAGER.md` | Velocity, blockers |
| Writer | Scripts, dialogue | `prompts/WRITER_AGENT.md` | Script quality |
| Animation Director | Visual style, 22-step | `prompts/ANIMATION_DIRECTOR.md` | Episode quality |
| Sound Director | Audio, mixing | `prompts/SOUND_DIRECTOR.md` | Mix quality |
| Child Safety | Safety gatekeeper | `prompts/CHILD_SAFETY.md` | 100% pass |
| Rights Clearance | IP verification | `prompts/RIGHTS_CLEARANCE.md` | Zero violations |
| Publisher | Upload, metadata | `prompts/PUBLISHER_AGENT.md` | On-time publish |
| SEO | Packaging, discovery | `prompts/SEO_AGENT.md` | CTR, retention |
| Analytics | Performance review | `prompts/ANALYTICS_AGENT.md` | Insight depth |
| QA | Final QC | `prompts/QA_AGENT.md` | Defect rate |
| VFX | Effects, compositing | `prompts/VFX_AGENT.md` | Visual quality |

**Orchestration patterns:**
- Sequential (pipeline): Writer → Animation → Sound → QA
- Parallel (fan-out): Research + SEO + Analytics simultaneously
- Human-in-loop: Child Safety, Rights Clearance, QA are mandatory gates

---

### 6. Model Layer (LLM Providers)

| Provider | Use Case | Access |
|----------|----------|--------|
| **Claude (Sonnet/Opus)** | Primary reasoning, code, analysis | API + CLI |
| **ChatGPT (GPT-4o)** | Creative writing, dialogue | API |
| **Gemini (Pro/Flash)** | Long-context research, multimodal | API |
| **Local LLMs (Ollama/LM Studio)** | Offline, private, cost-controlled | Local GPU |

**Routing strategy:**
- Creative/strategic → Claude
- High-volume generation → Local LLMs
- Research with citations → ChatGPT + Gemini
- Code review → Claude

---

### 7. Tool Layer (Execution Surface)

| Tool | Purpose | Integration |
|------|---------|-------------|
| **Git** | Version control, history, collaboration | `git`, GitHub Actions |
| **Bash** | Scripting, automation, one-offs | `engineering/scripts/` |
| **Docker** | Reproducible environments, CI | `.github/workflows/` |
| **Blender** | 3D animation, rendering, rigging | `projects/KidsStudio/` |
| **AOSP** | Android platform development | `projects/Android/` |

**Tool philosophy:** Every tool is scriptable, versioned, and has a documented SOP.

---

## Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        HUMAN INTENT                             │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PROJECT MANAGER AGENT                        │
│              (Decomposes → Phase-classifies → Schedules)        │
└──────────────────────────┬──────────────────────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
   │   BRAIN     │  │  FACTORY    │  │ DATA CENTER │
   │  (Phase 1-2)│  │  (Phase 3)  │  │  (Phase 4)  │
   └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
          │                │                │
   ┌──────┴──────┐  ┌──────┴──────┐  ┌──────┴──────┐
   │ Multi-Agent │  │   Blender   │  │  Render Farm│
   │ Orchestrator│  │  + Docker   │  │  + AI Server│
   └─────────────┘  └─────────────┘  └─────────────┘
```

---

## Phase-Aware Execution Model

| Phase | Layer | Capability | Current Hardware |
|-------|-------|------------|------------------|
| **Phase 1** | Brain | Docs, planning, research, Git, Obsidian, prompt engineering | ✅ 100% |
| **Phase 2** | Factory (light) | Python, FastAPI, React, Android dev, basic agents | ✅ 90% |
| **Phase 3** | Factory (heavy) | Blender, Remotion, image gen, 7B LLM, video render | ⚠️ Slow |
| **Phase 4** | Data Center | 30B+ models, 4K render, training, Unreal, render farms | ❌ Deferred |

**Rule:** Never schedule Phase N+1 before Phase N work is complete for that cycle.

---

## Governance Integration

| Layer | Governance Artifact |
|-------|---------------------|
| Kernel | `kernel/` (immutable) |
| Standards | `governance/Standards.md` |
| Naming | `governance/NamingConvention.md` |
| Repos | `governance/RepositoryRules.md` |
| Docs | `governance/DocumentationRules.md` |
| Style | `governance/MarkdownStyleGuide.md` |
| Versioning | `governance/Versioning.md` |
| Releases | `governance/ReleasePolicy.md` |
| Decisions | `decisions/ADR-XXXX-*.md` |

---

## Metrics & Observability

| Dimension | Tooling | Cadence |
|-----------|---------|---------|
| Content velocity | GitHub + YouTube Analytics | Daily |
| Pipeline health | Custom scripts | Per episode |
| Agent performance | Session logs | Weekly |
| System health | CI pass rate, disk, CPU | Continuous |
| Business KPIs | `metrics/KPIs/` | Monthly |

---

## Deployment Topology (Target v1.0)

```
┌──────────────────────────────────────────────────────────┐
│                    VJSOS Studio Network                  │
├──────────────┬──────────────┬──────────────┬─────────────┤
│   DEV MACHINE │  RENDER NODE  │   AI SERVER   │  NAS/BACKUP │
│  (Laptop+)   │  (Threadripper) │  (RTX 5090+)  │  (10TB RAID)│
│  Brain+Light │  Factory Heavy  │  LLMs/Render  │  Cold Store │
└──────────────┴──────────────┴──────────────┴─────────────┘
```

---

## Related

- [[docs/MASTER_CONTEXT]] — high-level context for local LLMs
- [[docs/ROADMAP]] — phased evolution v0.1→v4.0
- [[docs/infrastructure]] — hardware phases and upgrade triggers
- [[kernel/README]] — kernel concept and authority
- [[governance/Standards]] — enforceable rules
- [[knowledge/graph-schema.md]] — formal knowledge graph schema