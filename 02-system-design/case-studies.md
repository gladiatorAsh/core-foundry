# Classic system design case studies (compact outlines)

Rehearse each one out loud in 35 minutes. Each outline lists: **core idea**, the **hard parts** interviewers
probe, and **Staff-level extras**.

---

## 1. URL shortener
- **Core:** write: generate key (base62 of a counter from a ticket server or range-allocated ID blocks, or a hash
  with collision check) → KV store `key → long_url`. Read: cache → KV → 301/302 redirect.
- **Hard parts:** key generation without coordination (pre-allocated ID ranges per server); 301 (cacheable, loses
  analytics) vs 302; custom aliases; expiry.
- **Extras:** click analytics through an async log (Kafka → stream aggregation → OLAP); abuse/malware URL scanning.

## 2. Rate limiter (distributed)
- **Core:** token bucket per (user, API) in Redis with an atomic Lua script; enforced at the API gateway.
- **Hard parts:** race conditions (atomic ops), multi-region (local limits + async sync, accept slight overage),
  failing open vs closed when Redis is down.
- **Extras:** tiered limits, `429` + `Retry-After` headers, shadow mode before enforcing.

## 3. News feed (Twitter/Facebook home timeline)
- **Core:** fan-out on **write** (push post IDs into followers' feed caches) for normal users; fan-out on **read**
  (pull at request time) for celebrities. Hybrid merge at read.
- **Hard parts:** celebrity fan-out, feed ranking, pagination with a cursor, deletes/edits propagating.
- **Extras:** ranking service (candidate generation → ranker), cold start, cost of the fan-out storage.

## 4. Chat / messaging (WhatsApp, Slack)
- **Core:** persistent WebSocket connections via gateway servers; a connection registry (user → gateway);
  messages written to a store partitioned by conversation ID with per-conversation sequence numbers; offline
  delivery via push notifications plus sync-on-reconnect from the last seen sequence.
- **Hard parts:** ordering (per-conversation sequence), delivery/read receipts, group fan-out, presence at scale
  (heartbeats, lazy presence), end-to-end encryption implications.
- **Extras:** multi-device sync, message search (separate index), retention policies.

## 5. Notification system
- **Core:** API → validation/preferences → priority queues per channel (push/SMS/email) → workers → providers
  (APNs/FCM/Twilio/SES), with retries and a DLQ.
- **Hard parts:** dedupe (idempotency keys), user preferences/quiet hours, rate limiting per user, templating, provider failover.
- **Extras:** delivery tracking and analytics, digesting low-priority notifications.

## 6. Typeahead / search autocomplete
- **Core:** offline job builds prefix → top-K suggestions from query logs; served from an in-memory trie or a KV of
  prefixes (sharded by prefix), with CDN/browser caching of short prefixes.
- **Hard parts:** freshness (trending terms via a streaming top-K), personalization, filtering offensive terms, latency < 100 ms.
- **Extras:** debounce on the client; multi-language; ranking signals.

## 7. Web crawler
- **Core:** URL frontier (priority + per-host politeness queues) → fetchers → parse → dedupe (URL seen set via Bloom
  filter; content fingerprint via SimHash) → store → extract links back to the frontier.
- **Hard parts:** politeness/robots.txt, traps (infinite calendars), recrawl scheduling by change rate, distribution by host hash.

## 8. Distributed key-value store / cache
- **Core:** consistent hashing with virtual nodes; replication factor N; quorum reads/writes; gossip membership; LSM storage.
- **Hard parts:** tunable consistency (W + R > N), conflict resolution (vector clocks vs LWW), hinted handoff, anti-entropy with Merkle trees.

## 9. Video streaming (YouTube/Netflix)
- **Core:** upload → object storage → transcoding DAG (multiple resolutions/codecs, segmenting for HLS/DASH) → CDN.
  Playback with **adaptive bitrate**. Metadata in a DB; views counted asynchronously.
- **Hard parts:** transcoding cost/parallelism, CDN strategy (pre-position popular content), resumable uploads.

## 10. Ride sharing / proximity (Uber, Yelp)
- **Core:** drivers send location every few seconds → in-memory geo index (geohash/S2/H3 cells or a quadtree) → match
  riders to nearby available drivers; trip state machine in a durable store.
- **Hard parts:** high write rate of location updates (keep in memory, don't write each one to a DB), hot cells
  (downtown), matching fairness, surge pricing as a separate stream computation.

## 11. Payment system / wallet
- **Core:** idempotency keys on every API; double-entry ledger (append-only); state machine per payment; PSP
  integration with async webhooks; daily reconciliation.
- **Hard parts:** exactly-once *effect* (idempotency + dedupe), distributed transactions (saga + outbox), audit, PCI scope.

## 12. Metrics / logging platform (Datadog-like)
- **Core:** agents → ingestion gateway → Kafka → stream processors (rollups) → time-series DB (hot) + object storage (cold);
  query service with downsampling.
- **Hard parts:** high-cardinality tags, late data, retention tiers, alert evaluation at scale.

---

## How to practice

Pick one, set a 35-minute timer, talk out loud (record it), and draw in Excalidraw. Afterwards, compare against
[system-design-primer](https://github.com/donnemartin/system-design-primer) or Hello Interview's write-up of the same problem.
