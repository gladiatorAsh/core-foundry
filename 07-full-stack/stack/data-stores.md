# Data stores from your resume: SQL Server, Cosmos DB, MongoDB, Redis

General SQL, indexing, and isolation are in [../databases-and-sql.md](../databases-and-sql.md). Cosmos DB is covered in [azure.md](azure.md#cosmos-db).

## SQL Server specifics

- **Clustered index:** defines the physical order of the table (one per table; usually the primary key). **Nonclustered indexes** point to clustered-key values;
  `INCLUDE` columns make them covering. Choose narrow, ever-increasing clustered keys (identity/sequential GUID) to avoid page splits.
- Execution plans: look for scans vs seeks, key lookups (fix with `INCLUDE`), implicit conversions (type mismatches kill index use), bad cardinality estimates (stale statistics).
- **Parameter sniffing:** a plan compiled for one parameter value performs badly for others. Mitigations: `OPTION (RECOMPILE)`, `OPTIMIZE FOR`, Query Store plan forcing.
- **Query Store** tracks plan history and regressions. **RCSI** (Read Committed Snapshot Isolation) makes readers use row versions instead of shared locks (fewer blocking issues; uses tempdb).
- Temporal tables (built-in history), columnstore indexes (analytics), table partitioning, Always On availability groups (HA/DR). Azure SQL adds serverless and Hyperscale tiers.

## MongoDB

- Document model (BSON), flexible schema, max document size **16 MB**.
- **Embed vs reference:** embed data read together and bounded in size (an order with its line items); reference when it's unbounded, shared, or updated independently (a user's millions of events).
- Indexes: single, compound (follow the **ESR rule**: Equality fields, then Sort, then Range), multikey (arrays), text, TTL (auto-expire), partial, wildcard. Check with `explain()`.
- **Aggregation pipeline:** `$match` (early, to use indexes) → `$group` → `$sort` → `$project` → `$lookup` (join) → `$unwind`.
- Replica sets (primary + secondaries, automatic election; read preference and write concern `w: "majority"` for durability). Sharding by **shard key** (hashed for even writes, ranged for range queries); a bad shard key is very hard to change.
- Multi-document ACID transactions exist (since 4.0) but cost more; design so most writes touch one document.

## Redis

- In-memory data structure server. Command execution is single-threaded (I/O can be multi-threaded since Redis 6), so it's very fast, and slow commands (`KEYS *`, big `SMEMBERS`) block everyone. Use `SCAN`.
- **Data structures → use cases:** strings (cache values, counters with `INCR`), hashes (objects), lists (queues), sets (unique membership), **sorted sets** (leaderboards, rate-limit windows, priority queues),
  streams (event log with consumer groups), bitmaps/HyperLogLog (analytics), geo indexes, plus JSON and vector search in Redis Stack/Redis 8.
- **Expiry and eviction:** TTL per key; when memory is full, the `maxmemory-policy` decides: `noeviction`, `allkeys-lru`, `volatile-lru`, `allkeys-lfu`, `volatile-ttl`, … (cache workloads usually use `allkeys-lru`/`lfu`).
- **Persistence:** RDB snapshots (compact, may lose recent writes) vs AOF (append-only log, more durable, `everysec` fsync typical) or both. As a pure cache you can disable persistence.
- **Scaling and HA:** replication + Sentinel (failover), or **Redis Cluster** (16,384 hash slots across shards; multi-key operations require the same slot, so use hash tags `{user:42}`).
- **Patterns:** cache-aside with TTL + jitter; distributed rate limiter (Lua script or `INCR` + `EXPIRE`); session store; distributed lock with `SET key value NX PX ttl`
  (single-instance locks are fine for efficiency; for correctness-critical locking add fencing tokens; Redlock's guarantees are debated); pub/sub (fire-and-forget) vs streams (durable, replayable).
- Pitfalls: big keys and hot keys, missing TTLs causing memory growth, cache stampedes, treating the cache as the source of truth.

## Choosing between them (a quick answer you can give)

| Need | Pick |
|---|---|
| Relational data, transactions, reporting | SQL Server / Postgres |
| Global distribution, massive scale, predictable key-based access, multi-model on Azure | Cosmos DB |
| Flexible documents, rapid iteration, rich queries on JSON | MongoDB (or Cosmos DB for MongoDB) |
| Sub-millisecond reads, counters, queues, leaderboards, rate limits | Redis (in front of a durable store) |
