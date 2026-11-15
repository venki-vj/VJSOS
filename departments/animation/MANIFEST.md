# Animation Department Manifest

**Department ID:** animation
**Director:** `director-animation@vjsos-ai`
**Constitution Article:** V, VI

---

## Mission
Create animated content, visual effects, and motion graphics following production pipelines and quality standards. Build character rigs, models, and assets for VJSOS media (primarily Kids Studio).

## Domains
- rigging — Character armatures, controls, skinning
- modeling — 3D assets, texturing, PBR materials

## Worker Agents
| Agent ID | Type | Skills |
|----------|------|--------|
| `rigging-agent@animation@vjsos-ai` | Worker | character_rigging, animation_controls, skinning, testing, documentation |
| `modeling-agent@animation@vjsos-ai` | Worker | 3d_modeling, texturing, asset_creation, quality_check, documentation |

## QA Agent
`qa-animation@vjsos-ai` — Enforces `animation_qa_rubric_v2.0` (includes Animator Checklist)

## Memory Scope
`memory/department/animation/` — contains:
- asset_pipeline.md
- rigging_standards.md
- modeling_standards.md
- animator_checklist.md (25 poses)
- child_safety_animation.md
- qa_rubric.md
- asset_library/
- lessons_learned/

## SOPs
- `sops/animation/rigging_pipeline.md`
- `sops/animation/modeling_pipeline.md`
- `sops/animation/asset_validation.md`
- `sops/animation/child_safety_animation.md`

## KPIs
| Metric | Target |
|--------|--------|
| QA Pass Rate | ≥ 85% |
| Animator Checklist | 100% (25/25 poses) |
| Topology Standard | 0 n-gons, clean edge flow |
| Asset Pipeline Compliance | 100% |
| Child Safety (Kids Studio) | 100% |
| On-Time Delivery | ≥ 90% |

## Skill Registry Entries (in skills/animation/)
- character_rigging/
- 3d_modeling/
- texturing/

## Directory Structure
```
departments/animation/
├── director-animation@vjsos-ai.md
├── rigging-agent@vjsos-ai.md
├── modeling-agent@vjsos-ai.md
├── qa-animation@vjsos-ai.md
├── MANIFEST.md (this file)
├── memory/ (symlink to memory/department/animation/)
└── skills/ (symlink to skills/animation/)
```

## Governance
- Director reports to Governor
- QA agent reports to QA Engine + Director
- All Kids Studio content requires Child Safety review via QA
- All cross-department requests go through Orchestrator → Governor

## Startup Dependencies
- Kernel components: Governor, Orchestrator, Context Engine, Memory Engine, QA Engine
- Plugin: blender@v1.0.0 (rendering, rigging)
- Skills registry available
- Department memory initialized

---

**Status:** Operational
**Version:** 1.0.0
**Last Updated:** 2026-08-07