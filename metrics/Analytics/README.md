# VJSOS Metrics — Analytics

> Analytics pipeline, dashboards, and tracking setup.

## Data Sources

| Source | Type | Access |
|--------|------|--------|
| YouTube Analytics | Video performance, audience | YouTube Studio API |
| GitHub | Commits, PRs, CI, issues | GitHub REST/GraphQL API |
| Local | Session logs, time tracking | Obsidian vault files |
| Custom | Render pipeline, asset tracking | Local scripts (engineering/scripts/) |

## Collection

### Daily (automated where possible)
- Git commits + stats (GitHub API)
- YouTube video metrics (last 48h)
- Session log created ([[sessions/YYYY-MM-DD-DayN.md]])

### Weekly (manual review)
- Channel performance summary
- Sprint metrics (velocity, blockers)
- AI agent utilization

### Monthly (automated + review)
- Full metrics snapshot → [[metrics/MonthlyReports]]
- OKR progress scoring
- Revenue estimate update

## Dashboards

### 1. Channel Dashboard (weekly)
- Views, watch time, retention, CTR
- Subscriber growth
- Revenue estimate
- Top/bottom videos

### 2. Production Dashboard (during production)
- Episode status (script → storyboard → animatic → render → QC)
- Asset readiness
- Blocker list

### 3. Engineering Dashboard (continuous)
- CI status (pass/fail)
- PR queue
- Deploy frequency
- Test coverage

## Tooling

| Tool | Purpose |
|------|---------|
| YouTube Studio | Primary video analytics |
| GitHub Insights | Engineering metrics |
| Obsidian (Dataview) | Session log queries |
| Custom scripts | Cross-platform aggregation |

## Automation Roadmap

1. **Phase 1 (Now):** Manual collection + session logs
2. **Phase 2 (v0.5):** GitHub Actions → daily JSON dump to `metrics/Analytics/`
3. **Phase 3 (v1.0):** Central dashboard (Grafana / custom)
4. **Phase 4 (v2.0):** Automated alerts + anomaly detection

## Links
- [[metrics/OKRs]], [[metrics/KPIs]], [[metrics/MonthlyReports]]
- [[engineering/scripts/README.md]]