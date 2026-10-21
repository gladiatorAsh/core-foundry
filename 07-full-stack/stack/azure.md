# Azure services (from your resume)

Interviewers at Microsoft and Azure-heavy companies go deep here; elsewhere, use these as examples of the generic concepts
(see [../../04-genai-system-design/vendor-neutral-mapping.md](../../04-genai-system-design/vendor-neutral-mapping.md)).

## App Service

PaaS hosting for web apps/APIs (Windows or Linux, code or containers). App Service **plans** define compute (scale up = bigger SKU; scale out = more instances, autoscale rules).
**Deployment slots** (staging → swap with warm-up for zero-downtime deploys and instant rollback). Built-in auth (Easy Auth), VNet integration, private endpoints, managed identity.
Settings → environment variables; reference Key Vault secrets from app settings.

## Azure Functions

- Event-driven serverless: **triggers** (HTTP, Timer, Queue/Service Bus, Event Grid, Event Hubs, Blob, Cosmos DB change feed) and **bindings** (declarative inputs/outputs).
- Hosting plans: **Consumption** (scale to zero, pay per execution, cold starts, short default timeout), **Flex Consumption** (newer: faster scale, VNet, always-ready instances),
  **Premium** (pre-warmed instances, no cold start, VNet, longer runs), **Dedicated** (App Service plan).
- **Durable Functions:** stateful orchestrations in code, with patterns for function chaining, **fan-out/fan-in**, async HTTP APIs (202 + status endpoint), monitors, **human interaction** (wait for an external event with a timeout), and entities.
  Orchestrator code must be **deterministic** (no `DateTime.Now`, random, or direct I/O; use the context APIs) because it is replayed.
- Good for: event processing, glue code, scheduled jobs, document pipelines (your OCR → classify → extract flow maps naturally to Durable Functions fan-out).

## Logic Apps

Low-code workflows with 1,000+ connectors (Office 365, SharePoint, ServiceNow, Salesforce, SAP). **Consumption** (multi-tenant, pay per action) vs **Standard** (single-tenant, runs on the Functions runtime, VNet, stateful/stateless workflows).
Use for integration-heavy workflows owned by mixed teams; use Functions/code when logic is complex or needs unit tests.

## Messaging: pick the right one

| Service | Model | Use for |
|---|---|---|
| **Service Bus** | Enterprise message broker: queues + topics/subscriptions, sessions (FIFO per key), dead-lettering, duplicate detection, transactions | Commands and business workflows that must not be lost |
| **Event Grid** | Push-based event routing (pub/sub) with filtering | Reacting to state changes ("blob created", "resource updated") |
| **Event Hubs** | High-throughput event streaming with partitions and retention (Kafka-compatible endpoint) | Telemetry, logs, clickstreams, analytics pipelines |
| Storage Queues | Simple, cheap queues | Basic background work at large scale |

## Cosmos DB

- Globally distributed multi-model database (NoSQL API most common; also MongoDB, Cassandra, Gremlin, Table, and PostgreSQL options).
- **Partition key** is the most important design decision: high cardinality, even distribution, and matching your most common query filter. A logical partition is limited to 20 GB.
  Cross-partition queries cost more. Hierarchical partition keys help with tenant-skew in multi-tenant apps.
- **Request Units (RU/s):** a normalized cost per operation (a 1 KB point read ≈ 1 RU). Provisioned (manual or autoscale) vs serverless. 429s mean you exceeded RU/s, so retry with backoff and fix the hot partition.
- **Five consistency levels:** Strong → Bounded staleness → **Session** (default; read-your-own-writes per session) → Consistent prefix → Eventual. Stronger = higher latency/RU cost and lower availability across regions.
- Point reads (`id` + partition key) are the cheapest operation. Indexing policy: everything is indexed by default; exclude unused paths to save RUs on writes.
- **Change feed** for event-driven processing (materialized views, sync to search indexes). Vector search is supported (useful for RAG alongside operational data).

## Azure Cache for Redis

Managed Redis for caching, sessions, rate limiting, distributed locks, and pub/sub. Tiers differ in clustering, persistence, geo-replication, and VNet support.
Patterns you used: cache-aside in front of SQL/Cosmos for low-latency APIs. See [data-stores.md](data-stores.md#redis) for Redis internals.

## Key Vault and managed identity

Store secrets, keys, and certificates; access with **managed identity** (no credentials in code or config). Use RBAC on the vault, soft delete + purge protection, and key rotation.
Apps reference secrets via Key Vault references or the SDK with `DefaultAzureCredential`.

## Blob Storage

Object storage with **hot / cool / cold / archive** tiers and lifecycle management rules. SAS tokens (prefer user-delegation SAS) for time-limited direct client upload/download.
Immutable storage for compliance; event triggers via Event Grid. ADLS Gen2 adds hierarchical namespaces for analytics.

## Observability and security

**Application Insights** / Azure Monitor (requests, dependencies, traces, live metrics, KQL queries), **Entra ID** (app registrations, OAuth flows, on-behalf-of),
private endpoints + VNets, Defender for Cloud, Azure Policy, RBAC at management group / subscription / resource-group scopes.

## Teams and integrations

Copilots in Microsoft Teams are built with Bot Framework / Teams AI library or Copilot Studio; Microsoft Graph for M365 data (with delegated permissions); adaptive cards for rich UI.
Your Icertis work (chatbots over email/Teams/SMS; Workday and ServiceNow integrations) is a good integration story.
