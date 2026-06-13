# IncidentIQ — Root-Cause Reasoning Agent for Production Incidents

**Agents League Hackathon (Microsoft Innovation Studio) · Track: Reasoning Agents · Foundry IQ**

When a production system breaks — say checkout latency spikes 5x — on-call
engineers burn hours under pressure manually correlating logs, metrics, and
recent deploys. IncidentIQ is an autonomous reasoning agent that does that
correlation in seconds: given an incident alert it pulls the telemetry, forms
hypotheses, **tests and eliminates each one through multi-step reasoning**, ranks
the surviving root causes with evidence, and drafts a post-mortem plus a
suggested fix.

The point of the project is the *visible reasoning*: hypothesis → tool call →
eliminate → conclude.

## Quick start

```bash
# Local reasoning mode — runs fully offline, no Azure needed
python -m incidentiq.main

# Also write the post-mortem
python -m incidentiq.main --postmortem out.md

# Microsoft Foundry mode (needs Azure creds; see .env.example)
python -m incidentiq.main --foundry
```

Run from the `src/` directory, or `pip install -e .` first.

## Run the web app

```bash
# Install web dependencies (once)
pip install -r requirements.txt

# From the project root
uvicorn incidentiq.api:app --reload --app-dir src
```

Open **http://localhost:8000/docs** for the interactive API explorer.

| Endpoint | What it does |
|----------|-------------|
| `GET /api/incident` | Returns the demo incident (INC-4471) |
| `POST /api/diagnose` | Runs the reasoning loop, returns full `ReasoningTrace` as JSON |
| `GET /api/postmortem` | Runs the reasoning loop, returns post-mortem Markdown |

The frontend UI lives in `frontend/` and is served at `/`.
Local reasoning mode only — no Azure credentials required.

## What a run looks like

```
■ INCIDENT INC-4471: Checkout latency spiked ~5x
  → tool get_recent_deploys(...) ✓
  → tool get_metrics(...) ✓
  → tool get_logs(...) ✓

  Hypotheses:
   [✓ KEPT]        A recent checkout-api deploy introduced a regression.
   [✗ ELIMINATED]  An upstream dependency (payments-gateway) degraded.
   [✗ ELIMINATED]  Host/CPU resource exhaustion on checkout-api.

  ROOT CAUSE: checkout-api v2.41.0 moved the payment-token cache to Redis;
  the pool (max=10) is undersized, so requests queue ~480ms ...
```

## How it works

Two execution paths share one reasoning loop and produce the same
`ReasoningTrace`:

1. **Foundry mode** (`agent.run_foundry`) — a Microsoft Foundry / Azure AI agent
   with the tools in `tools.TOOL_SPECS` registered, orchestrated via the Agent
   Framework. This is the required Microsoft IQ layer (Foundry IQ).
2. **Local reasoning mode** (`agent.run_local`) — a deterministic, transparent
   stand-in that runs the identical hypothesis → tool-call → eliminate → conclude
   loop offline, so the demo always works and the reasoning is inspectable.

Tools (`get_recent_deploys`, `get_metrics`, `get_logs`) are backed by mock
telemetry here and by **Azure MCP** servers (GitHub Deployments, Azure Monitor,
Log Analytics) in production.

See [`docs/architecture.md`](docs/architecture.md) for the diagram.

## Layout

```
src/incidentiq/
  agent.py       reasoning loop (Foundry + local modes), ReasoningTrace
  tools.py       agent tools + JSON schemas registered with Foundry
  mock_data.py   demo telemetry (stands in for Azure MCP)
  postmortem.py  ReasoningTrace -> Markdown post-mortem
  main.py        CLI entry point
scenarios/        incident scenarios
docs/             architecture
```

## Submission checklist (see IDEA.md)

- [x] Innovation Studio profile activated + registered
- [x] Project created on Innovation Studio (Reasoning Agents track)
- [x] Working project — runnable reasoning loop with tools
- [ ] Foundry wiring filled in (`agent.run_foundry` stub) + tested with creds
- [ ] Demo video ≤2 min (problem → live run → architecture → impact)
- [ ] Public GitHub repo linked in the project's Code Repository field
- [ ] Architecture diagram attached

## Tech

Microsoft Foundry (Foundry IQ) · Azure MCP · Agent Framework · GitHub Copilot · Python
