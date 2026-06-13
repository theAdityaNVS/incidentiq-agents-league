# IncidentIQ — Project Memory

Persistent context so any session (or teammate) can resume instantly. Update when state changes.

## What this is
**IncidentIQ** — a root-cause reasoning agent for production incidents. Given an incident
alert, it pulls logs/metrics/deploy history, forms hypotheses, tests and eliminates each
through multi-step reasoning, ranks the root cause with evidence, and drafts a post-mortem
plus a suggested fix.

- **Hackathon:** Agents League @ AISF 2026 (Microsoft Innovation Studio)
- **Track:** 🧠 Reasoning Agents (tool: Microsoft Foundry)
- **Required IQ layer:** Foundry IQ (agentic retrieval / grounded cited answers) — see FOUNDRY_PLAN.md
- **Deadline:** submissions close **June 14, 2026**; winners June 30
- **Owner:** Aditya Nadamuni (theadityanvs)

## Key links
- Innovation Studio project: https://innovationstudio.microsoft.com/hackathons/Agents-League-Hackathon/project/124636 (project ID **124636**, Owner: Aditya Nadamuni, track: Reasoning Agents)
- Public GitHub repo: https://github.com/theAdityaNVS/incidentiq-agents-league
- Hackathon About page: https://innovationstudio.microsoft.com/hackathons/Agents-League-Hackathon

## Architecture (current)
```
Incident alert → Reasoning loop (hypothesis → tool call → eliminate → conclude)
                 ├─ tools: get_recent_deploys / get_metrics / get_logs (mock_data today; Azure MCP later)
                 └─ output: ReasoningTrace → post-mortem markdown
Two run modes share one loop & one ReasoningTrace:
  • run_local   — offline, deterministic, no Azure. Used by the web app + demo today.
  • run_foundry — STUB. To be filled with Azure AI Foundry agent + Foundry IQ retrieval.
Web app: FastAPI (src/incidentiq/api.py) serves /api/incident, /api/diagnose, /api/postmortem
         and the static dashboard (frontend/index.html + logo.png) at /.
```

## File map
- `src/incidentiq/agent.py` — reasoning loop, `ReasoningTrace`, `run_local`, `run_foundry` (stub)
- `src/incidentiq/tools.py` — agent tools + JSON schemas (registered with Foundry)
- `src/incidentiq/mock_data.py` — demo telemetry (stands in for Azure MCP)
- `src/incidentiq/postmortem.py` — trace → markdown
- `src/incidentiq/api.py` — FastAPI backend
- `src/incidentiq/main.py` — CLI (`python -m incidentiq.main [--foundry] [--postmortem out.md]`)
- `frontend/index.html` — SRE dashboard (single file); `frontend/logo.png`
- `docs/architecture.md` — diagram (ASCII; needs an image version showing Foundry IQ)
- `PLAN.md` — web-app build plan · `TRACKER.md` — submission checklist · `FOUNDRY_PLAN.md` — IQ integration + cost

## How to run
```bash
pip install -r requirements.txt
uvicorn incidentiq.api:app --reload --app-dir src   # → http://localhost:8000
python -m incidentiq.main                            # CLI, local reasoning mode
```

## Decisions & constraints
- **Local reasoning mode is the safe demo path** — always runs offline, no creds, no cost.
- **Foundry IQ integration is MANDATORY to qualify** (hackathon rule). Currently NOT done — this is the #1 open item. See FOUNDRY_PLAN.md for the free/low-cost path (~$0 within Azure free tier + $200 credit).
- **No secrets in git.** `.env` and `.venv` are git-ignored; only `.env.example` is committed.
- **Safety:** no destructive actions are auto-executed (rollback / PR are suggestions, human-in-the-loop).

## Current status (2026-06-13)
- ✅ Profile activated, registered, project created on Innovation Studio
- ✅ Reasoning agent + FastAPI backend + dashboard built and tested end-to-end (local mode)
- ✅ Public GitHub repo pushed (no secrets)
- ⬜ Foundry IQ integration (mandatory) — planned, not built
- ⬜ Architecture diagram image · ⬜ 2-min demo video · ⬜ Final submit on Innovation Studio
