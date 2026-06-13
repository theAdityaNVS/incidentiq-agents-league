# IncidentIQ — Architecture

```
                 ┌─────────────────────────┐
   Incident      │   Incident alert (JSON)  │
   alert  ─────▶ │  id, summary, service    │
                 └───────────┬─────────────┘
                             │
                             ▼
            ┌────────────────────────────────────┐
            │     Microsoft Foundry Agent          │
            │     (Foundry IQ reasoning loop)      │
            │                                      │
            │  SYSTEM PROMPT: SRE root-cause method│
            │  1 restate → 2 hypotheses →          │
            │  3 test via tools → 4 rank →         │
            │  5 mitigation + fix                  │
            └───────┬───────────────┬─────────────┘
                    │ tool calls    │  (Agent Framework orchestration)
                    ▼               ▼
        ┌───────────────────────────────────────┐
        │            Azure MCP tools             │
        │  get_recent_deploys  (GitHub Deploys)  │
        │  get_metrics         (Azure Monitor)   │
        │  get_logs            (Log Analytics)   │
        └───────────────────────────────────────┘
                    │
                    ▼
        ┌───────────────────────────────────────┐
        │   ReasoningTrace  →  Post-mortem .md    │
        │   (ranked root cause + evidence trail   │
        │    + suggested fix / PR)                │
        └───────────────────────────────────────┘

Build assist: GitHub Copilot.    Demo runs offline via the local reasoning
mode; the same trace structure is produced in Foundry mode.
```

## Components

- **Microsoft Foundry agent (Foundry IQ)** — hosts the reasoning loop and tool
  calling; the required Microsoft IQ intelligence layer for this submission.
- **Azure MCP tools** — `get_recent_deploys`, `get_metrics`, `get_logs` expose
  deploy history, Azure Monitor metrics, and Log Analytics logs as agent tools.
- **Agent Framework** — orchestrates the hypothesis → tool-call → eliminate →
  conclude steps and parses run steps into a `ReasoningTrace`.
- **GitHub Copilot** — used during build (noted in the submission).
- **Output** — a Markdown post-mortem with the ranked root cause, the evidence
  trail, and a suggested fix.
