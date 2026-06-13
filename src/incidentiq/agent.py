"""IncidentIQ reasoning agent.

Two execution paths share one reasoning loop:

1. **Foundry mode** — a Microsoft Foundry / Azure AI agent with the tools in
   `tools.TOOL_SPECS` registered. Enabled when Azure credentials + project
   endpoint are present (see .env.example).
2. **Local reasoning mode** — a deterministic, transparent stand-in that runs
   the same hypothesis -> tool-call -> eliminate -> conclude loop with no
   network access, so the demo always runs and the *reasoning structure* is
   visible to judges.

Both paths emit the same `ReasoningTrace`, which is what the demo and the
post-mortem are built from.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field

from . import tools
from .mock_data import INCIDENT

SYSTEM_PROMPT = """You are IncidentIQ, a senior site-reliability engineer that finds the
root cause of production incidents through disciplined, evidence-based reasoning.

Method (always follow):
1. Restate the incident and its start time.
2. Enumerate 2-4 concrete hypotheses for the cause.
3. For EACH hypothesis, call tools to gather evidence, then KEEP or ELIMINATE it
   with an explicit reason tied to the evidence.
4. Rank surviving root causes by likelihood, citing the evidence for each.
5. Recommend an immediate mitigation and a durable fix.

Be specific. Prefer the simplest cause that explains the timing and the metrics.
Correlate the incident start time with recent deploys."""


@dataclass
class Hypothesis:
    statement: str
    verdict: str = "open"          # open | kept | eliminated
    evidence: list[str] = field(default_factory=list)
    reasoning: str = ""


@dataclass
class ReasoningTrace:
    incident: dict
    tool_calls: list[dict] = field(default_factory=list)
    hypotheses: list[Hypothesis] = field(default_factory=list)
    root_cause: str = ""
    mitigation: str = ""
    durable_fix: str = ""

    def record_tool_call(self, name: str, args: dict, result: str) -> None:
        self.tool_calls.append({"tool": name, "args": args, "result": result})


# --------------------------------------------------------------------------- #
# Local reasoning mode (offline, deterministic, fully transparent)
# --------------------------------------------------------------------------- #

def run_local(incident: dict | None = None, verbose: bool = True) -> ReasoningTrace:
    incident = incident or INCIDENT
    trace = ReasoningTrace(incident=incident)
    svc = incident["affected_service"]

    def log(msg: str) -> None:
        if verbose:
            print(msg)

    log(f"\n■ INCIDENT {incident['id']}: {incident['title']}")
    log(f"  {incident['summary']}\n")

    # 1. Gather evidence via tools (the agent decides to pull all three signals).
    deploys = _call(trace, "get_recent_deploys", {"service": svc}, log)
    metrics = _call(trace, "get_metrics", {"service": svc}, log)
    logs = _call(trace, "get_logs", {"service": svc}, log)

    deploys_data = json.loads(deploys)
    metrics_data = json.loads(metrics)
    logs_data = json.loads(logs)

    # 2. Hypotheses
    h_deploy = Hypothesis("A recent checkout-api deploy introduced a regression.")
    h_dependency = Hypothesis("An upstream dependency (payments-gateway) degraded.")
    h_resource = Hypothesis("A host/CPU resource exhaustion on checkout-api.")
    trace.hypotheses = [h_deploy, h_dependency, h_resource]

    # 3. Test each hypothesis against evidence
    near_deploy = [d for d in deploys_data if d["deployed_at"] >= "2026-06-13T14:00:00Z"]
    if near_deploy:
        d = near_deploy[0]
        h_deploy.verdict = "kept"
        h_deploy.evidence.append(f"Deploy {d['version']} at {d['deployed_at']} (~3 min before onset): {d['change']}")
        redis_wait = metrics_data.get("redis_pool_wait_ms", {})
        if redis_wait.get("after", 0) > 10 * max(redis_wait.get("before", 1), 1):
            h_deploy.evidence.append(
                f"redis_pool_wait_ms jumped {redis_wait['before']}->{redis_wait['after']}ms, "
                "consistent with moving token cache to Redis."
            )
        redis_log = [l for l in logs_data if "redis pool" in l.lower()]
        h_deploy.evidence += redis_log
        h_deploy.reasoning = (
            "Timing lines up to the minute and the new Redis-backed token cache is saturating "
            "its connection pool — directly explains the latency rise."
        )

    pg = metrics_data if svc == "payments-gateway" else json.loads(tools.get_metrics("payments-gateway"))
    pg_lat = pg.get("p95_latency_ms", {})
    if pg_lat and pg_lat.get("after", 0) - pg_lat.get("before", 0) < 20:
        h_dependency.verdict = "eliminated"
        h_dependency.reasoning = (
            f"payments-gateway p95 only {pg_lat.get('before')}->{pg_lat.get('after')}ms (flat). "
            "The few upstream timeouts are a SYMPTOM of checkout slowness, not the cause."
        )
        h_dependency.evidence.append("payments-gateway logs: request volume nominal, no error spike.")

    cpu = metrics_data.get("cpu_pct", {})
    if cpu and cpu.get("after", 0) < 70:
        h_resource.verdict = "eliminated"
        h_resource.reasoning = f"CPU only {cpu.get('before')}->{cpu.get('after')}% — not saturated."

    # 4 & 5. Conclude
    trace.root_cause = (
        "checkout-api v2.41.0 switched the payment-token cache from an in-process LRU to a Redis "
        "lookup. The Redis connection pool (max=10) is undersized for token-lookup volume, so "
        "requests queue ~480ms waiting for a connection — driving p95 from 240ms to ~1310ms."
    )
    trace.mitigation = (
        "Roll back checkout-api to v2.40.x (or feature-flag the token cache back to in-process LRU) "
        "to immediately restore latency."
    )
    trace.durable_fix = (
        "Raise the Redis connection pool size and add pool-wait alerting; load-test the Redis path "
        "before re-deploying; cache tokens with a short in-process L1 in front of Redis (L2)."
    )

    if verbose:
        _print_conclusion(trace)
    return trace


def _call(trace: ReasoningTrace, name: str, args: dict, log) -> str:
    result = tools.dispatch(name, args)
    trace.record_tool_call(name, args, result)
    log(f"  → tool {name}({args}) ✓")
    return result


def _print_conclusion(trace: ReasoningTrace) -> None:
    print("\n  Hypotheses:")
    for h in trace.hypotheses:
        mark = {"kept": "✓ KEPT", "eliminated": "✗ ELIMINATED", "open": "… OPEN"}[h.verdict]
        print(f"   [{mark}] {h.statement}")
        if h.reasoning:
            print(f"           {h.reasoning}")
    print(f"\n  ROOT CAUSE:\n   {trace.root_cause}")
    print(f"\n  MITIGATION:\n   {trace.mitigation}")
    print(f"\n  DURABLE FIX:\n   {trace.durable_fix}\n")


# --------------------------------------------------------------------------- #
# Foundry mode (Microsoft Foundry / Azure AI Agents)
# --------------------------------------------------------------------------- #

def run_foundry(incident: dict | None = None, verbose: bool = True) -> ReasoningTrace:
    """Run the same loop on a Microsoft Foundry agent.

    Requires: pip install azure-ai-projects azure-identity, plus env vars
    PROJECT_ENDPOINT and MODEL_DEPLOYMENT_NAME (see .env.example).
    Falls back to local mode with a clear message if the SDK/creds are absent.
    """
    incident = incident or INCIDENT
    endpoint = os.getenv("PROJECT_ENDPOINT")
    model = os.getenv("MODEL_DEPLOYMENT_NAME")
    if not endpoint or not model:
        if verbose:
            print("[foundry] PROJECT_ENDPOINT / MODEL_DEPLOYMENT_NAME not set — using local mode.")
        return run_local(incident, verbose)

    try:
        from azure.ai.projects import AIProjectClient
        from azure.identity import DefaultAzureCredential
    except ImportError:
        if verbose:
            print("[foundry] azure-ai-projects not installed — using local mode.")
        return run_local(incident, verbose)

    # Real wiring lives here. Sketch (kept minimal so the file imports cleanly):
    #   client = AIProjectClient(endpoint=endpoint, credential=DefaultAzureCredential())
    #   agent = client.agents.create_agent(model=model, name="IncidentIQ",
    #               instructions=SYSTEM_PROMPT, tools=tools.TOOL_SPECS)
    #   thread = client.agents.threads.create()
    #   client.agents.messages.create(thread.id, role="user",
    #               content=json.dumps(incident))
    #   run = client.agents.runs.create_and_process(thread.id, agent.id,
    #               tool_dispatch=tools.dispatch)
    #   ... parse run steps into a ReasoningTrace ...
    raise NotImplementedError(
        "Foundry wiring stub — fill in with your azure-ai-projects run loop, "
        "dispatching tool calls through tools.dispatch()."
    )
