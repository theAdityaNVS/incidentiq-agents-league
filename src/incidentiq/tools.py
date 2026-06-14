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
def _resolve_knowledge_dir() -> Path | None:
    """Locate the knowledge/ dir across local + serverless (Vercel) layouts."""
    here = Path(__file__).resolve()
    candidates = [
        here.parent.parent.parent / "knowledge",  # repo root from src/incidentiq/
        Path.cwd() / "knowledge",
        Path("/var/task/knowledge"),
    ]
    candidates += [p / "knowledge" for p in list(here.parents)[:6]]
    for c in candidates:
        if c.exists():
            return c
    return None


# In-code copy of the knowledge base so cited grounding works even where the knowledge/
# files aren't on disk (e.g. Vercel serverless, which doesn't bundle non-imported data dirs).
# Mirrors the knowledge/*.md files; the on-disk files are preferred when present.
_EMBEDDED_KB: dict[str, str] = {
    "RB-12-checkout-redis-cache.md": (
        "RB-12 checkout-api payment-token cache. The Redis connection pool default max=10, "
        "sized for low-concurrency dev, not production token-lookup volume. Symptom of an "
        "undersized pool: redis_pool_wait_ms rises sharply and logs show 'redis pool exhausted, "
        "waiting for connection'. Safe rollback: roll back checkout-api to the previous minor "
        "(v2.40.x) to revert to the in-process LRU and restore latency, or feature-flag "
        "token_cache=lru. Durable fix: raise redis.pool.max to at least 50 and add alerting on "
        "redis_pool_wait_ms; add a short in-process L1 cache in front of Redis."
    ),
    "RB-07-latency-triage.md": (
        "RB-07 latency spike triage. A regression that begins within ~5 minutes of a deploy is a "
        "deploy regression until proven otherwise; pull recent deploys first. An upstream "
        "dependency is only the cause if its own latency/error rate rose materially; a flat "
        "upstream with a few timeouts is a symptom of the caller being slow, not the cause. CPU "
        "under ~70% rules out CPU exhaustion. Connection-pool wait times in the hundreds of ms "
        "indicate a saturated pool. Prefer the fastest safe mitigation (rollback / feature flag) first."
    ),
    "PM-INC-3990-redis-pool.md": (
        "PM-INC-3990 prior incident on cart-api. A deploy moved session lookups to Redis; the "
        "connection pool (max=10) saturated under production volume and p95 rose 4x. Resolved by "
        "rolling back, then re-shipping with pool.max=64 plus an in-process L1 cache. Lesson: any "
        "change moving a hot per-request lookup to a networked store must ship with a "
        "production-sized connection pool and pool-wait alerting. This pattern has recurred on "
        "checkout-api (see RB-12)."
    ),
}


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

    # Prefer on-disk knowledge files; fall back to the embedded copy when the dir isn't
    # present (e.g. serverless). Either way produces (filename, text) pairs to score.
    kdir = _resolve_knowledge_dir()
    if kdir is not None:
        docs = [(p.name, p.read_text(encoding="utf-8")) for p in sorted(kdir.glob("*.md"))]
    else:
        docs = sorted(_EMBEDDED_KB.items())

    for name, text in docs:
        low = text.lower()
        score = sum(low.count(t) for t in terms)
        if score == 0:
            continue
        # pick the most relevant paragraph as the snippet
        paras = [p.strip() for p in text.split("\n\n") if p.strip()] or [text]
        best = max(paras, key=lambda p: sum(p.lower().count(t) for t in terms))
        stem = name.rsplit(".", 1)[0]
        parts = stem.split("-")
        citation = f"{parts[0]}-{parts[1]}" if len(parts) > 1 else stem
        hits.append(
            {
                "source": name,
                "citation": citation,
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
