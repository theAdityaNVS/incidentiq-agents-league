"""IncidentIQ FastAPI backend.

Three endpoints expose the local reasoning loop over HTTP:

  GET  /api/incident    — demo incident metadata
  POST /api/diagnose    — run the reasoning loop, return full ReasoningTrace as JSON
  GET  /api/postmortem  — run the reasoning loop, return post-mortem Markdown

Static files from the top-level frontend/ folder are served at /.

Reasoning mode: LOCAL only.  run_foundry is never called here.
"""

from __future__ import annotations

import dataclasses
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from . import mock_data, postmortem
from .agent import run_local

app = FastAPI(title="IncidentIQ", version="0.1.0")


@app.get("/api/incident")
def get_incident() -> dict:
    """Return the demo incident record."""
    return mock_data.INCIDENT


@app.post("/api/diagnose")
def diagnose() -> dict:
    """Run the local reasoning loop and return the full ReasoningTrace as JSON.

    Response shape:
      incident       — the incident dict
      tool_calls     — list of {tool, args, result}
      hypotheses     — list of {statement, verdict, evidence, reasoning}
      root_cause     — string
      mitigation     — string
      durable_fix    — string
    """
    trace = run_local(verbose=False)
    return dataclasses.asdict(trace)


@app.get("/api/postmortem")
def get_postmortem() -> dict:
    """Run the local reasoning loop and return the post-mortem as Markdown."""
    trace = run_local(verbose=False)
    return {"markdown": postmortem.to_markdown(trace)}


# Mount static files last so /api/* routes are matched first.
_frontend = Path(__file__).resolve().parent.parent.parent / "frontend"
_frontend.mkdir(exist_ok=True)
app.mount("/", StaticFiles(directory=str(_frontend), html=True), name="static")
