# System design framework (60 minutes)

| Time | Step | Output on the whiteboard |
|---|---|---|
| 0–8 | **Requirements** | Functional (3–5 bullets, prioritized), non-functional (scale, latency, availability, consistency, durability), explicit *out of scope* |
| 8–13 | **Estimates** | DAU, QPS (avg/peak), storage/yr, bandwidth. Only what changes a decision. |
| 13–18 | **API + data model** | Endpoints/RPCs with key params; core entities and access patterns |
| 18–30 | **High-level design** | Boxes and arrows for the main read and write paths. Walk one request end to end. |
| 30–50 | **Deep dives** (2–3) | The hardest parts: hot keys, fan-out, consistency, ordering, failure handling |
| 50–60 | **Wrap-up** | Bottlenecks, failure modes, monitoring/SLOs, cost, what v2 looks like |

At Staff level, **you drive**. Don't wait to be asked about failures or trade-offs.

## Requirements questions to ask every time

- Who are the users and what are the top 2–3 use cases? What's explicitly out of scope?
- Scale: DAU/MAU, requests per user per day, read:write ratio, data size per item, growth rate.
- Latency targets (p50/p99) for the main paths? Real-time or eventual?
- Consistency: is stale data OK? For how long? Any operation that must never be lost or doubled (payments)?
- Availability target (99.9% ≈ 8.8 h/yr down; 99.99% ≈ 53 min/yr)?
- Geography: single region or global? Data residency?
- Security/privacy: auth model, PII, multi-tenancy, audit.

## The deep-dive checklist (pick what's relevant)

- **Data:** SQL vs NoSQL and why; partition key; hot partitions; secondary indexes; schema evolution.
- **Scale reads:** cache (where, what, TTL, invalidation, stampede protection), read replicas, CDN.
- **Scale writes:** sharding, write-behind queues, batching, idempotency keys.
- **Async:** queue vs log (Kafka), at-least-once + idempotent consumers, retries with backoff, dead-letter queue.
- **Consistency:** strong vs eventual, read-your-writes, conflict resolution, distributed transactions (saga/outbox).
- **Availability:** replication, failover, multi-AZ/region, graceful degradation, load shedding, circuit breakers.
- **Observability:** SLIs/SLOs, metrics, tracing, alerting on symptoms, not causes.
- **Security:** authN/authZ, encryption in transit/at rest, rate limiting, abuse prevention.
- **Cost:** biggest cost driver and one way to cut it.
- **Evolution:** migration plan, backfills, feature flags, schema changes without downtime.

## Trade-off language

"We could do A (pros/cons) or B (pros/cons). Given requirement X, I'd pick A. If X changes to Y, I'd switch to B."

## Common mistakes

- Jumping to boxes before requirements; designing for 1B users when the prompt implies 10K.
- Naming technologies without justifying them ("use Kafka" without saying why a log is needed).
- One giant deep dive that runs out of time; never discussing failures.
- Ignoring the interviewer's hints. They're steering you toward what they want to evaluate.
