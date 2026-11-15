# Business Department Manifest

**Department ID:** business
**Director:** `director-business@vjsos-ai`
**Constitution Article:** V, VI

---

## Mission
Drive business strategy, revenue generation, and market expansion through data-driven insights and strategic planning. Ensure all business decisions are grounded, risk-assessed, and aligned to VJSOS vision.

## Domains
- strategy — Business strategy, market analysis, competitive intelligence
- revenue — Financial planning, pricing strategy, revenue optimization

## Worker Agents
| Agent ID | Type | Skills |
|----------|------|--------|
| `strategy-agent@business@vjsos-ai` | Worker | strategic_planning, market_analysis, financial_modeling, competitive_analysis, documentation |
| `revenue-agent@business@vjsos-ai` | Worker | revenue_strategy, financial_planning, pricing_models, market_analysis, documentation |

## QA Agent
`qa-business@vjsos-ai` — Enforces `business_qa_rubric_v2.0`

## Memory Scope
`memory/department/business/` — contains:
- business_model_canvas.md
- market_intelligence/
- financial_models/
- pricing_strategy.md
- qa_rubric.md
- kpi_dashboard.md
- lessons_learned/

## SOPs
- `sops/business/strategic_analysis.md`
- `sops/business/financial_modeling.md`
- `sops/business/pricing_approval.md`
- `sops/business/forecast_review.md`

## KPIs
| Metric | Target |
|--------|--------|
| QA Pass Rate | ≥ 85% |
| Forecast Accuracy | ≥ 85% (vs actual) |
| Validated Assumptions | 100% |
| ROI-Positive Recommendations | ≥ 80% |
| Risk Documentation | 100% |
| Decision-to-Action Time | < 1 week |

## Skill Registry Entries (in skills/business/)
- strategic_planning/
- financial_modeling/
- revenue_optimization/
- market_analysis/

## Directory Structure
```
departments/business/
├── director-business@vjsos-ai.md
├── strategy-agent@vjsos-ai.md
├── revenue-agent@vjsos-ai.md
├── qa-business@vjsos-ai.md
├── MANIFEST.md (this file)
├── memory/ (symlink to memory/department/business/)
└── skills/ (symlink to skills/business/)
```

## Governance
- Director reports to Governor
- QA agent reports to QA Engine + Director
- Financial commitments require Governor + Human approval
- All cross-department requests go through Orchestrator → Governor

## Startup Dependencies
- Kernel components: Governor, Orchestrator, Context Engine, Memory Engine, QA Engine
- Plugin: google-sheets@v1.0.0 (financial models)
- Plugin: stripe@v1.0.0 (revenue data)
- Skills registry available
- Department memory initialized

---

**Status:** Operational
**Version:** 1.0.0
**Last Updated:** 2026-08-07