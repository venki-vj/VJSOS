# VJSOS Decisions — ADR Index

> Architecture Decision Records (ADRs) — the permanent, traceable record of key decisions.

## Process

1. A decision needs an ADR when it:
   - Affects multiple business units
   - Is difficult/expensive to reverse
   - Establishes a standard or policy
   - Changes the architecture

2. Template:
   ```markdown
   # ADR-XXXX-Name

   ## Status
   Proposed | Accepted | Superseded by ADR-XXXX | Deprecated

   ## Context
   What is the issue we're addressing?

   ## Decision
   What did we decide?

   ## Consequences
   Positive and negative impacts.

   ## Alternatives Considered
   What else did we consider?

   ## Related ADRs
   [[ADR-0001-...]]
   ```

3. Save to `decisions/ADR-XXXX-Name.md`
4. Reference in [[governance/Standards]] and relevant docs
5. Review quarterly in [[metrics/QuarterlyReports]]

## ADR Index

| Number | Title | Status | Date | Affects |
|--------|-------|--------|------|---------|
| [[decisions/ADR-0001-Vision]] | Three-Layer Architecture | Accepted | 2026-08-04 | Entire organization |
| [[decisions/ADR-0002-Markdown]] | Markdown as Knowledge Format | Accepted | 2026-08-04 | Documentation, knowledge |
| [[decisions/ADR-0003-GitHub]] | GitHub as Source of Truth | Accepted | 2026-08-04 | All repos, CI/CD |
| [[decisions/ADR-0004-Obsidian]] | Obsidian as Knowledge Vault | Accepted | 2026-08-04 | Knowledge management |
| [[decisions/ADR-0005-AIArchitecture]] | 14 Specialized AI Agents | Accepted | 2026-08-04 | AI workforce |
| [[decisions/ADR-0006-Governance]] | Internal Governance | Accepted | 2026-08-04 | All processes |
| [[decisions/ADR-0007-Infrastructure]] | Phase-Wise Capability | Accepted | 2026-08-04 | Infrastructure |
| [[decisions/ADR-0008-Kernel]] | Immutable Kernel Core | Accepted | 2026-08-04 | All decisions |

## Templates

- `ADR-TEMPLATE.md` — use for new ADRs

## Related
- [[kernel/Interfaces]] (ADR references)
- [[governance/Standards]]
- [[governance/ReleasePolicy]] (ADR review cadence)