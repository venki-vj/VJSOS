# ADR-0007-Infrastructure: Phase-Wise Capability Model

## Status
Accepted

## Date
2026-08-05

## Context
VJSOS runs on consumer hardware (Acer Aspire E5, integrated graphics, 8GB RAM, Windows 11). We cannot:
- Run 30B+ parameter models locally
- Render 4K animation in reasonable time
- Train custom models
- Run heavy Unreal Engine workloads

We need a framework that:
1. Acknowledges current limitations honestly
2. Defines what *is* possible now
3. Creates clear upgrade triggers (not wishful thinking)
4. Prevents premature capital expenditure

## Decision
Adopt a **four-phase capability model** with explicit hardware requirements and upgrade triggers.

### Phase 1 — Brain (100% on current hardware)
| Capability | Status |
|------------|--------|
| Documentation, planning, research | ✅ |
| Git, Obsidian, VS Code | ✅ |
| Prompt engineering, AI agents | ✅ |
| Architecture, roadmaps | ✅ |

### Phase 2 — Software Factory (90% on current hardware)
| Capability | Status |
|------------|--------|
| Python, FastAPI, SQLite | ✅ |
| React, Electron, GitHub | ✅ |
| Android app development | ✅ |
| Basic AI agents (local 7B) | ✅ |

### Phase 3 — Creative Factory (Slow on current hardware)
| Capability | Status |
|------------|--------|
| Light Blender (EEVEE, simple scenes) | ⚠️ Slow |
| Remotion (short renders) | ⚠️ Slow |
| Image generation (SD, local) | ⚠️ Slow |
| Local 7B LLM inference | ⚠️ Slow |
| Video rendering (FFmpeg) | ⚠️ Slow |

### Phase 4 — Data Center (Not practical on current hardware)
| Capability | Status |
|------------|--------|
| 30B–70B local models | ❌ |
| High-quality Blender (Cycles, 4K) | ❌ |
| Model training | ❌ |
| Heavy Unreal Engine | ❌ |
| Large render farms | ❌ |

## Upgrade Triggers (Objective, Not Aspirational)

| Trigger | Action |
|---------|--------|
| Phase 3 work genuinely blocks revenue | Order v1.0 workstation (Ryzen 9, 64GB, RTX 5080-class, 4TB NVMe) |
| Revenue > ₹500K/month sustained | Plan v2.0 (local AI server) |
| 3+ concurrent production projects | Plan v3.0 (render node) |
| Team of 3+ full-time | Plan v4.0 (studio network: Dev → Render → AI → NAS) |

## Infrastructure Evolution Roadmap

| Version | Hardware | Capability |
|---------|----------|------------|
| 0.1 | Existing Acer laptop | Phase 1–2 full |
| 0.5 | RAM upgrade + SSD + backup drive | Faster Phase 2–3 |
| 1.0 | Dedicated workstation (see above) | Phase 3 comfortable |
| 2.0 | Local AI server (RTX 5090, 128GB) | 13B–30B models |
| 3.0 | Render node (dual GPU/Threadripper) | Parallel rendering |
| 4.0 | Studio network (4 machines) | Full pipeline |

## Consequences

### Positive
- Honest assessment prevents frustration
- Capital efficiency (no premature spend)
- Clear ROI criteria for upgrades
- Work can progress on Phase 1–2 while learning Phase 3

### Negative
- Phase 3 is slow (animation renders take hours)
- Some features deferred (no local 70B model)
- Single point of failure (one laptop)

## Alternatives Considered

| Alternative | Rejected Because |
|-------------|-----------------|
| Buy workstation now (₹3-5L) | No validated revenue; violates "capability before capacity" |
| Cloud-only rendering | Ongoing cost; latency; no asset ownership |
| Hybrid (local + cloud) | Complexity; cost uncertainty |

## Related ADRs
- [[decisions/ADR-0001-Vision]] — three-layer architecture
- [[decisions/ADR-0008-Kernel]] — phase-aware is a core principle