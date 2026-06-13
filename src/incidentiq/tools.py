"""Tools the IncidentIQ agent can call during its reasoning loop.

Each function is a thin, well-documented capability the model invokes via tool /
function calling. In production these are backed by Azure MCP servers (Azure
Monitor, Log Analytics, GitHub). Here they read from mock_data so the demo runs
offline. The JSON schemas in TOOL_SPECS are what we register with the
Microsoft Foundry agent.
"""

from __future__ import annotations

import json
from typing import Any

from . import mock_data


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


# --- Tool registry -----------------------------------------------------------

TOOL_FUNCTIONS = {
    "get_recent_deploys": get_recent_deploys,
    "get_metrics": get_metrics,
    "get_logs": get_logs,
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
]


def dispatch(name: str, arguments: dict[str, Any]) -> str:
    """Execute a tool call by name with the given arguments and return its string result."""
    fn = TOOL_FUNCTIONS.get(name)
    if fn is None:
        return json.dumps({"error": f"unknown tool '{name}'"})
    return fn(**arguments)
