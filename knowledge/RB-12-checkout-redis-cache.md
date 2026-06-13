# RB-12 — checkout-api payment-token cache

**Service:** checkout-api
**Owner:** Payments Platform

## Token cache
- The payment-token cache can run in two modes: in-process LRU (default before v2.41) or Redis lookup (v2.41+).
- **The Redis connection pool default `max=10`.** This is sized for low-concurrency dev, not production token-lookup volume.
- Symptom of an undersized pool: `redis_pool_wait_ms` rises sharply and logs show `redis pool exhausted, waiting for connection`.

## Safe rollback
- Rolling back checkout-api to the previous minor (e.g. v2.40.x) reverts to the in-process LRU and restores latency immediately.
- Alternatively, feature-flag `token_cache=lru` to disable the Redis path without a deploy.

## Tuning the Redis path before re-enabling
- Raise `redis.pool.max` to at least 50 for production; add alerting on `redis_pool_wait_ms > 50`.
- Add a short in-process L1 cache in front of Redis (L2) to cut lookup volume.
