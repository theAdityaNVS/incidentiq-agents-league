"""Tools the IncidentIQ agent can call during its reasoning loop.

Each function is a thin, well-documented capability the model invokes via tool /
function calling. In production these are backed by Azure MCP servers (Azure
Monitor, Log Analytics, GitHub). Here they read from mock_data so the demo runs
offline. The JSON schemas in TOOL_SPECS are what we register with the
Microsoft Foundry agent.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

from . import mock_data

# Knowledge base of runbooks / past post-mortems. In production this is indexed by a
# Foundry IQ knowledge base (agentic retrieval); locally we read these files directly so
# the cited-grounding behaviour is demonstrable offline.
_KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent.parent / "knowledge"


def get_recent_deploys(service: str | None = None, hours: int = 12) -> str:
    """Return recent deployments, optionally filtered to a service."""
    deploys = mock_data.DEPLOYS
    if service:
        deploys = [d for d in deploys if d["service"] == service]
    return json.dumps(deploys, indent=2)


def get_metrics(service: str) -> str:
    """Return before/after metric values for a service around the incident window."""
    return json.dumps(mock_data.METRICS.get(service, {}), indent=2)


def get_logs(service: str, limit: int = 20) -> str:
    """Return recent log lines for a service."""
    lines = mock_data.LOGS.get(service, [])[:limit]
    return json.dumps(lines, indent=2)


def _search_azure(query: str, top: int) -> list[dict[str, Any]] | None:
    """Foundry IQ retrieval via Azure AI Search. Returns hits, or None to fall back to local.

    Activates only when AZURE_SEARCH_ENDPOINT + AZURE_SEARCH_INDEX are set (see .env.example
    and FOUNDRY_PLAN.md). Auth: AZURE_SEARCH_KEY if present, else DefaultAzureCredential.
    """
    endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
    index = os.getenv("AZURE_SEARCH_INDEX")
    if not endpoint or not index:
        return None
    try:
        from azure.search.documents import SearchClient

        key = os.getenv("AZURE_SEARCH_KEY")
        if key:
            from azure.core.credentials import AzureKeyCredential

            cred = AzureKeyCredential(key)
        else:
            from azure.identity import DefaultAzureCredential

            cred = DefaultAzureCredential()
        client = SearchClient(endpoint=endpoint, index_name=index, credential=cred)
        results = client.search(search_text=query, top=top)
        hits: list[dict[str, Any]] = []
        for r in results:
            source = r.get("source") or r.get("title") or r.get("id") or "doc"
            hits.append(
                {
                    "source": source,
                    "citation": r.get("citation") or str(source).split(".")[0],
                    "snippet": " ".join((r.get("content") or "").split())[:280],
                }
            )
        return hits or None
    except Exception:
        # Any SDK/auth/network issue → fall back to the offline scan so the demo never breaks.
        return None


def search_runbooks(query: str, top: int = 3) -> str:
    """Search the runbook / post-mortem knowledge base and return cited snippets.

    Returns a JSON list of {source, citation, snippet}. `citation` is the source doc id
    (e.g. "RB-12") so the agent can ground and cite each finding. When Azure AI Search creds
    are configured this is real **Foundry IQ agentic retrieval**; otherwise it falls back to
    a keyword scan over the knowledge/ markdown files so the demo works offline.
    """
    azure_hits = _search_azure(query, top)
    if azure_hits is not None:
        return json.dumps(azure_hits, indent=2)

    terms = [t for t in re.split(r"\W+", query.lower()) if len(t) > 2]
    hits: list[dict[str, Any]] = []
    if not _KNOWLEDGE_DIR.exists():
        return json.dumps(hits)
    for path in sorted(_KNOWLEDGE_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        low = text.lower()
        score = sum(low.count(t) for t in terms)
        if score == 0:
            continue
        # pick the most relevant paragraph as the snippet
        paras = [p.strip() for p in text.split("\n\n") if p.strip()]
        best = max(paras, key=lambda p: sum(p.lower().count(t) for t in terms))
        hits.append(
            {
                "source": path.name,
                "citation": path.stem.split("-")[0] + "-" + path.stem.split("-")[1]
                if "-" in path.stem
                else path.stem,
                "snippet": " ".join(best.split())[:280],
                "_score": score,
            }
        )
    hits.sort(key=lambda h: h["_score"], reverse=True)
    for h in hits:
        h.pop("_score", None)
    return json.dumps(hits[:top], indent=2)


# --- Tool registry -----------------------------------------------------------

TOOL_FUNCTIONS = {
    "get_recent_deploys": get_recent_deploys,
    "get_metrics": get_metrics,
    "get_logs": get_logs,
    "search_runbooks": search_runbooks,
}

# OpenAI/Foundry-style function schemas, registered with the agent.
TOOL_SPECS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "get_recent_deploys",
            "description": "List recent deployments (service, version, time, change summary, author). "
            "Use this to correlate the incident start time with code/config changes.",
            "parameters": {
                "type": "object",
                "properties": {
                    "service": {"type": "string", "description": "Filter to one service. Omit for all."},
                    "hours": {"type": "integer", "description": "Look-back window in hours."},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_metrics",
            "description": "Get before/after metric values (latency, error rate, resource saturation) "
            "for a service around the incident window.",
            "parameters": {
                "type": "object",
                "properties": {"service": {"type": "string"}},
                "required": ["service"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_logs",
            "description": "Fetch recent log lines for a service to find error signatures and saturation signals.",
            "parameters": {
                "type": "object",
                "properties": {
                    "service": {"type": "string"},
                    "limit": {"type": "integer"},
                },
                "required": ["service"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_runbooks",
            "description": "Search the runbook and past post-mortem knowledge base (Foundry IQ) for "
            "grounding. Returns cited snippets so each finding can reference an authoritative source "
            "and avoid hallucination. Call this to confirm hypotheses against known patterns.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "What to look up, e.g. 'redis connection pool default size checkout'"},
                    "top": {"type": "integer", "description": "Max results to return."},
                },
                "required": ["query"],
            },
        },
    },
]


def dispatch(name: str, arguments: dict[str, Any]) -> str:
    """Execute a tool call by name with the given arguments and return its string result.

    Tolerant of unexpected/extra kwargs from the model: never raises, always returns a
    string so the tool-calling loop stays consistent.
    """
    fn = TOOL_FUNCTIONS.get(name)
    if fn is None:
        return json.dumps({"error": f"unknown tool '{name}'"})
    try:
        return fn(**arguments)
    except TypeError:
        # Model passed unexpected kwargs — keep only the ones the function accepts.
        import inspect

        allowed = set(inspect.signature(fn).parameters)
        safe = {k: v for k, v in arguments.items() if k in allowed}
        try:
            return fn(**safe)
        except Exception as exc:  # last-resort guard
            return json.dumps({"error": f"{type(exc).__name__}: {exc}"})
    except Exception as exc:
        return json.dumps({"error": f"{type(exc).__name__}: {exc}"})
