# Building blocks and their trade-offs

## Storage

| Option | Use when | Watch out for |
|---|---|---|
| Relational (Postgres, MySQL, Azure SQL, Spanner) | Relations, transactions, ad-hoc queries, strong consistency | Write scaling needs sharding (Vitess, Citus) or Spanner-style systems |
| Key-value / wide-column (DynamoDB, Cassandra, Bigtable, Cosmos DB) | Huge scale, known access patterns, high write throughput | Design tables around queries; no joins; hot partitions |
| Document (MongoDB, Cosmos DB) | Flexible schema, nested objects read together | Cross-document transactions are limited/expensive |
| Object storage (S3, GCS, Azure Blob) | Blobs, media, data lake, backups | Not for low-latency small reads; eventual listing in some systems |
| Search (Elasticsearch/OpenSearch, Azure AI Search) | Full-text, faceting, relevance, hybrid vector | Secondary store; indexing lag; keep the source of truth elsewhere |
| Time-series (Prometheus, InfluxDB, Druid) | Metrics, events by time | Cardinality explosions |
| Graph (Neo4j, TAO-style) | Many-hop relationship queries | Often a KV store with adjacency lists is enough |
| Vector (pgvector, Azure AI Search, FAISS, Pinecone, Milvus) | Embedding similarity search | ANN recall vs latency; filtering + ANN; re-indexing on model change |

## Indexes

B-tree: range queries, read-optimized. LSM tree: write-optimized (memtable → SSTables + compaction), used by
Cassandra/RocksDB/Bigtable; reads may check multiple SSTables (bloom filters help). Composite index order
matters (leftmost prefix rule).

## Replication

- **Leader–follower:** simple; async replicas give read scaling but **replication lag** (stale reads). Fix
  read-your-writes by reading from the leader for a short window after a write, or by session tokens.
- **Multi-leader:** multi-region writes; needs conflict resolution (LWW, CRDTs, app-level merge).
- **Leaderless (Dynamo-style):** quorum `W + R > N` for overlapping reads/writes; hinted handoff, read repair, anti-entropy (Merkle trees).

## Partitioning (sharding)

- **Hash** on key: even spread, but range scans are hard. **Consistent hashing** with virtual nodes minimizes
  data movement when nodes join/leave.
- **Range:** efficient scans; risk of hot ranges (e.g. time-ordered keys).
- **Hot keys:** add a random suffix ("salting") and aggregate on read; cache in front; split the celebrity.
- Cross-shard queries need scatter-gather; cross-shard transactions need 2PC or sagas.

## Consistency and consensus

- **CAP:** during a network partition, choose consistency or availability. **PACELC:** else (no partition), choose latency or consistency.
- **Linearizable** (single up-to-date copy) > **sequential** > **causal** > **eventual**.
- Consensus (Raft/Paxos; etcd, ZooKeeper) for leader election, config, locks, and metadata, not the data path.
- **Distributed transactions:** 2PC (blocking, coordinator SPOF) vs **saga** (local transactions + compensations).
  **Transactional outbox:** write the event to an outbox table in the same DB transaction; a relay publishes it, so you never get "DB updated but event lost".

## Caching

- Patterns: **cache-aside** (app reads cache, falls back to DB, populates), write-through, write-back (risk of loss), refresh-ahead.
- Invalidation: TTL + explicit delete on write (delete, don't update, to avoid races).
- **Stampede/thundering herd:** request coalescing (single flight), jittered TTLs, stale-while-revalidate.
- Eviction: LRU, LFU, TTL. Hot keys: local in-process cache + distributed cache.
- CDN for static and cacheable dynamic content; edge invalidation is slow, so version your URLs.

## Messaging

| | Queue (SQS, RabbitMQ, Service Bus) | Log (Kafka, Kinesis, Event Hubs, Pub/Sub) |
|---|---|---|
| Model | Message consumed and deleted | Append-only, consumers track offsets, replayable |
| Ordering | Usually none (FIFO variants exist) | Per partition |
| Fan-out | One consumer per message | Many consumer groups read independently |
| Use | Task distribution, background jobs | Event streams, CDC, analytics, rebuilding state |

Delivery semantics: at-most-once, **at-least-once (default) + idempotent consumers**, exactly-once (only within
a system like Kafka transactions; end to end, it's at-least-once + dedupe).

## Reliability patterns

Timeouts everywhere · retries with **exponential backoff + jitter** · idempotency keys · circuit breakers ·
bulkheads · load shedding/backpressure · graceful degradation (serve stale or partial) · health checks + autoscaling ·
blue/green and canary deploys · rate limiting (token bucket at the gateway).

## Networking and APIs

- REST for public CRUD; **gRPC** for internal low-latency typed RPC; GraphQL when clients need flexible aggregation.
- Real-time: long polling < SSE (server → client stream; good for LLM token streaming) < WebSockets (bi-directional).
- L4 vs L7 load balancing; sticky sessions only when necessary; API gateway for auth, rate limits, routing.
- Pagination: cursor-based (stable under inserts) over offset.

## IDs

UUIDv4 (random, no coordination, bad index locality) · UUIDv7 / ULID (time-ordered) · Snowflake (time + machine + sequence, 64-bit, sortable) · DB sequences (simple, central).

## Probabilistic data structures

Bloom filter (membership, false positives only) · Count-Min Sketch (frequency, overestimates) ·
HyperLogLog (cardinality, ~1–2% error in KBs) · Reservoir sampling (uniform sample from a stream).
