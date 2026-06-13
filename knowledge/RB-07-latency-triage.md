# RB-07 — Latency spike triage

**Applies to:** any service with a p95 latency regression.

## First correlate timing with deploys
- A latency regression that begins within ~5 minutes of a deploy is a deploy regression until proven otherwise. Always pull `get_recent_deploys` first.

## Rule out vs. confirm
- **Upstream dependency**: only the cause if the dependency's own latency/error rate rose materially. A flat upstream with a few timeouts is a *symptom* of the caller being slow, not the cause.
- **Resource exhaustion**: confirm with CPU/memory/connection-pool saturation. CPU under ~70% effectively rules out CPU exhaustion.
- **Connection-pool saturation**: `*_pool_wait_ms` rising into the hundreds of ms indicates a saturated pool (DB, Redis, HTTP).

## Mean-time-to-resolution
- Prefer the fastest safe mitigation (rollback / feature flag) first, then schedule the durable fix.
