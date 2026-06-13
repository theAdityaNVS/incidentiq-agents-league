"""Mock telemetry for IncidentIQ demo scenarios.

This stands in for real Azure Monitor / Log Analytics / GitHub Deployments data so
the agent can run end-to-end without live infrastructure. In production these
functions would be backed by Azure MCP tools.
"""

from __future__ import annotations

# --- Scenario: checkout latency spiked 5x at 14:05 UTC -----------------------

DEPLOYS = [
    {
        "service": "checkout-api",
        "version": "v2.41.0",
        "deployed_at": "2026-06-13T14:02:00Z",
        "change": "Switch payment-token cache from in-process LRU to Redis lookup",
        "author": "rsharma",
    },
    {
        "service": "catalog-api",
        "version": "v1.88.2",
        "deployed_at": "2026-06-13T09:10:00Z",
        "change": "Add product badge field to response",
        "author": "lwu",
    },
    {
        "service": "payments-gateway",
        "version": "v3.12.0",
        "deployed_at": "2026-06-12T18:30:00Z",
        "change": "Upgrade TLS library",
        "author": "akhan",
    },
]

METRICS = {
    "checkout-api": {
        "p95_latency_ms": {"before": 240, "after": 1310},
        "error_rate_pct": {"before": 0.2, "after": 0.4},
        "redis_pool_wait_ms": {"before": 1, "after": 480},
        "redis_connection_errors": {"before": 0, "after": 0},
        "cpu_pct": {"before": 38, "after": 41},
    },
    "payments-gateway": {
        "p95_latency_ms": {"before": 90, "after": 95},
        "error_rate_pct": {"before": 0.1, "after": 0.1},
    },
    "catalog-api": {
        "p95_latency_ms": {"before": 60, "after": 62},
        "error_rate_pct": {"before": 0.0, "after": 0.0},
    },
}

LOGS = {
    "checkout-api": [
        "2026-06-13T14:05:11Z WARN  redis pool exhausted, waiting for connection (waiters=37)",
        "2026-06-13T14:05:12Z WARN  payment-token lookup took 612ms (threshold 50ms)",
        "2026-06-13T14:05:14Z INFO  redis GET token:* avg 480ms over last 1m",
        "2026-06-13T14:05:20Z WARN  redis pool size=10, in_use=10, max=10",
        "2026-06-13T14:05:31Z ERROR upstream timeout to payments-gateway after 1000ms (1.3% of reqs)",
    ],
    "payments-gateway": [
        "2026-06-13T14:05:31Z INFO  request volume nominal; no error spike observed",
    ],
    "catalog-api": [
        "2026-06-13T14:05:00Z INFO  steady state, p95 62ms",
    ],
}

INCIDENT = {
    "id": "INC-4471",
    "title": "Checkout latency spiked ~5x",
    "summary": "checkout-api p95 latency rose from ~240ms to ~1300ms starting ~14:05 UTC. "
    "Customers report slow 'Place order' button. No full outage.",
    "started_at": "2026-06-13T14:05:00Z",
    "affected_service": "checkout-api",
}
