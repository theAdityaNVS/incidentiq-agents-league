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
- **Foundry IQ integration is LIVE.** Azure AI Search `incidentiq-srch` (resource group `incidentiq-rg`, East US, free tier). Index `incidentiq-kb` with fields `content`/`source`/`citation`. Env vars in `.env` (gitignored) and Vercel production env. `_search_azure` in `tools.py` activates automatically when `AZURE_SEARCH_ENDPOINT` is set.
- **No secrets in git.** `.env` is gitignored; admin key only in `.env` + Vercel env vars. Git history clean (verified `git log -S`).
- **Safety:** no destructive actions are auto-executed (rollback / PR are suggestions, human-in-the-loop).

## Current status (2026-06-15)
- ✅ Profile activated, registered, project created on Innovation Studio
- ✅ Reasoning agent + FastAPI backend + dashboard built and tested end-to-end
- ✅ Public GitHub repo pushed (no secrets in history)
- ✅ **Foundry IQ integration LIVE** — Azure AI Search `incidentiq-srch` (East US, free tier), index `incidentiq-kb`, 3 runbooks indexed. `search_runbooks` routes to `_search_azure` when `AZURE_SEARCH_ENDPOINT` + `AZURE_SEARCH_INDEX` + `AZURE_SEARCH_KEY` are set. Confirmed 3 citations returned from live Vercel deployment.
- ✅ Vercel env vars set + redeployed — `agents-league-microsoft.vercel.app` live with Azure citations
- ✅ All P1 bugs fixed (regex, dispatch, verdict, citations panel, glow CSS)
- ✅ Architecture diagram (`docs/architecture.svg`)
- ⬜ 2-min demo video (script ready in `VIDEO_SCRIPT.md`) — record + upload + add link to Innovation Studio
- ⬜ Read Disclaimer + CoC → Submit on Innovation Studio
- ⬜ Discord post for community vote
