# PM-INC-3990 — Prior incident: Redis pool exhaustion on cart-api

**Date:** 2026-02-18 · **Service:** cart-api · **Duration:** 41 min

## Summary
A deploy moved session lookups to Redis. The connection pool (`max=10`) saturated under
production volume; p95 rose 4x. Resolved by rolling back, then re-shipping with `pool.max=64`
plus an in-process L1 cache.

## Lesson learned
Any change that moves a hot per-request lookup to a networked store (Redis/DB) must ship with
a production-sized connection pool and pool-wait alerting. This pattern has now recurred on
checkout-api — see RB-12.
