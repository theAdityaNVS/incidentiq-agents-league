# IncidentIQ — Demo Web App Plan

## What we're building

A FastAPI backend that exposes the IncidentIQ reasoning agent over HTTP, plus a
`frontend/` folder that will hold the static UI (HTML/CSS/JS). Both are served by
a single `uvicorn` process — no separate build step needed for the demo.

## Architecture

```
agents-league-microsoft/
  src/incidentiq/
    api.py          ← FastAPI app (this is what we added)
    agent.py        ← reasoning loop (run_local used; run_foundry untouched)
    postmortem.py   ← ReasoningTrace → Markdown
    tools.py        ← mock telemetry tools
    mock_data.py    ← demo incident + telemetry
  frontend/         ← static files served at /  (placeholder for now)
  requirements.txt  ← fastapi + uvicorn added
```

## Endpoints

| Method | Path              | Description                                                      |
|--------|-------------------|------------------------------------------------------------------|
| GET    | /api/incident     | Returns the demo incident (INC-4471) as JSON                     |
| POST   | /api/diagnose     | Runs `run_local()`, returns full `ReasoningTrace` as JSON        |
| GET    | /api/postmortem   | Runs `run_local()`, returns `{"markdown": "<post-mortem text>"}` |
| GET    | /*                | Static files from `frontend/` (future UI)                        |

### ReasoningTrace JSON shape (`POST /api/diagnose`)

```json
{
  "incident":    { "id": "...", "title": "...", ... },
  "tool_calls":  [{ "tool": "...", "args": {}, "result": "..." }],
  "hypotheses":  [{ "statement": "...", "verdict": "kept|eliminated|open",
                    "evidence": ["..."], "reasoning": "..." }],
  "root_cause":  "...",
  "mitigation":  "...",
  "durable_fix": "..."
}
```

## Reasoning mode

**Local only.** `run_local(verbose=False)` is used exclusively. `run_foundry` is
never called and its stub is untouched. No Azure credentials required.

## Running the server

```bash
# Install dependencies (once)
pip install -r requirements.txt

# From the project root
uvicorn incidentiq.api:app --reload --app-dir src

# Or from src/ directly
cd src
uvicorn incidentiq.api:app --reload
```

Open http://localhost:8000/docs for the interactive API explorer (Swagger UI).

## Next steps

- Build the frontend UI in `frontend/` (HTML + vanilla JS calling the 3 endpoints)
- Wire up `run_foundry` when Azure credentials are available
- Add a scenario selector to the API (different mock incidents)
