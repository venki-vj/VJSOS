---
title: VJSOS Infrastructure & Hardware Phases
date: 2026-08-04
version: 0.1.0
---

# VJSOS Infrastructure & Hardware Phases

## Current Setup (Day 1)

| Component | Model |
|-----------|-------|
| Laptop | Acer Aspire E5-573 (~2015-16) |
| CPU | Intel Core i5 (5th gen) |
| GPU | Intel integrated graphics |
| RAM | 8GB (assumed baseline) |
| Storage | Original HDD + possibly small SSD |
| OS | Windows 11 |

## Phase-Wise Capability Matrix

| Phase | Capability | Current Laptop | When to Upgrade |
|-------|------------|----------------|-----------------|
| **Phase 1** — Brain | Planning, Docs, Git, Obsidian, VS Code, Research, Prompt Engineering, Android scripts, Architecture | ✅ 100% | Never needed |
| **Phase 2** — Software | Python, FastAPI, SQLite, React, Electron, GitHub, Android App Dev, Basic AI Agents | ✅ 90% | Phase 3 bottleneck |
| **Phase 3** — Factory | Remotion, FFmpeg, Light Blender, Image Generation, Local 7B LLMs, Video Rendering | ⚠️ Slow | When render blocks revenue |
| **Phase 4** — Data Center | 30B-70B models, High-quality Blender/Cycles, 4K animation, Model training, Heavy Unreal, Render farms | ❌ No | Dedicated workstation required |

## Infrastructure Evolution Roadmap

### Version 0.1 (Current)
- Existing Acer laptop
- Git + Obsidian + VS Code for docs and code
- GitHub for remote backup
- External drive for backup

### Version 0.5
- **RAM upgrade** (16GB if motherboard supports it)
- **SSD upgrade** (larger NVMe if slot available)
- **Better external backup** (reliable drive for 3-2-1 rule)

### Version 1.0
- **Dedicated workstation:**
  - CPU: AMD Ryzen 9 (12+ cores)
  - RAM: 64GB DDR5
  - GPU: RTX 5070 / 5080 class (or current equivalent)
  - SSD: 2–4TB NVMe
  - NAS for backup + team access

### Version 2.0
- **Local AI server:**
  - RTX 5090-class GPU
  - 128GB RAM
  - For 13B-30B local models serving

### Version 3.0
- **Render node:**
  - Dedicated machine for Blender/Cycles rendering
  - Possibly dual-GPU or Threadripper-class

### Version 4.0
- **Studio network:**
  - Development Machine (coding, docs, Brain-layer work)
  - Rendering Machine (Factory-layer)
  - AI Server (LLM inference, generation)
  - NAS + Backup Server
  - Laptop becomes thin client

## Spending Priority (If given budget)

### Stage 1: Foundation (₹50,000–100,000)
1. Larger NVMe SSD (if upgradeable)
2. Reliable external backup drive
3. More RAM (if upgradeable)
4. UPS for stability

### Stage 2: Workstation (₹2–3 lakh)
Only when VJSOS starts generating revenue:
- Dedicated production workstation (see v1.0 specs above)
- NOT a gaming PC — a production machine optimized for Blender + AI

## Upgrade Triggers (Decision Rules)

| Trigger | Action |
|---------|--------|
| Phase 3 work blocks revenue | Order v1.0 workstation |
| Revenue > ₹500K/month | Plan v2.0 (AI server) |
| 3+ concurrent projects | v3.0 render node |
| Team of 3+ | v4.0 studio network |

## Current Constraints

- No GPU acceleration in Blender
- 7B models only run slowly locally
- No 4K rendering capability
- Node.js crashes on some operations
- npm install issues reported
- Remotion rendering is slow

These are acceptable for now — we work within Phase 1-2 scope and use AI tools/cloud for Phase 3-4 tasks.

---

Links: [[PRINCIPLES]], [[RODO]], [[SOFTWARE_PRODUCTS]]