# Backend and API design

## REST API design checklist

- **Resources as nouns**, HTTP methods as verbs: `GET /orders/{id}`, `POST /orders`, `PATCH /orders/{id}`, `DELETE /orders/{id}`.
  Sub-resources for ownership: `GET /customers/{id}/orders`. Actions that aren't CRUD: `POST /orders/{id}:cancel` or `POST /orders/{id}/cancellation`.
- **Idempotency:** GET, PUT, DELETE are idempotent; POST isn't. Accept an `Idempotency-Key` header on POSTs that create
  side effects (payments, orders); store key → response for a TTL and replay it.
- **Status codes:** 200 OK, 201 Created (+ `Location`), 202 Accepted (async job), 204 No Content, 400 validation error,
  401 unauthenticated, 403 unauthorized, 404, 409 conflict (e.g. version mismatch), 412 precondition failed (ETag), 422 semantic validation,
  429 rate limited (+ `Retry-After`), 500, 502/503/504 upstream/unavailable/timeout.
- **Pagination:** cursor-based (`?cursor=…&limit=50`, return `next_cursor`) for large or changing data; offset only for small static sets.
- **Filtering/sorting:** `?status=open&sort=-created_at`. **Sparse fields:** `?fields=id,name`.
- **Versioning:** URL (`/v2/`) or header; additive changes don't need a new version; deprecate with notice.
- **Errors:** a consistent body, e.g. RFC 9457 Problem Details (`type`, `title`, `status`, `detail`, `instance`) + field errors.
- **Concurrency:** ETags + `If-Match` for optimistic locking (412 on mismatch).
- **Long operations:** 202 + job resource (`GET /jobs/{id}`) or webhooks; stream progress via SSE.
- Document with **OpenAPI**; generate clients; contract tests.

## REST vs gRPC vs GraphQL

| | REST | gRPC | GraphQL |
|---|---|---|---|
| Best for | Public APIs, CRUD, cacheability | Internal service-to-service, low latency, streaming | Many clients needing different shapes of data; aggregating backends |
| Format | JSON over HTTP | Protobuf over HTTP/2 | JSON; single endpoint |
| Strengths | Simple, HTTP caching, tooling | Typed contracts, fast, bidirectional streaming | No over/under-fetching, typed schema |
| Watch out | Over/under-fetching, chatty clients | Browser support needs a proxy (gRPC-Web) | N+1 resolvers (use DataLoader), caching and rate limiting are harder, query cost limits |

## Authentication and authorization

- **Sessions:** server-side session store + `HttpOnly; Secure; SameSite` cookie. Easy revocation. Needs CSRF protection for cookie auth.
- **JWT access tokens:** stateless, signed (RS256/ES256 for cross-service verification); short-lived (5–15 min) + refresh tokens (rotated);
  hard to revoke early, so keep them short. Validate `iss`, `aud`, `exp`, and signature. Don't store sensitive data in them (they're only base64-encoded).
- **OAuth 2.0** = delegated authorization. Use **Authorization Code + PKCE** for web/mobile/SPA. Client Credentials for service-to-service.
  The Implicit flow is deprecated. **OpenID Connect** adds authentication (an ID token with user identity) on top of OAuth 2.0.
- **SPA token storage:** prefer a backend-for-frontend (BFF) pattern holding tokens server-side with an HttpOnly session cookie; avoid tokens in localStorage.
- **Authorization models:** RBAC (roles), ABAC (attributes/policies), ReBAC (relationships, Zanzibar-style; e.g. OpenFGA). Enforce on the server for every request (object-level checks prevent IDOR).
- Your enterprise angle: Entra ID (Azure AD), managed identities, on-behalf-of flow for calling downstream APIs as the user.

## Background work

Queues (Service Bus, SQS, RabbitMQ) + workers for slow or retryable work; the outbox pattern for reliable events; scheduled jobs (cron, Hangfire, Celery beat);
retries with exponential backoff + jitter and a dead-letter queue; idempotent handlers.

## Concurrency in your languages

**C# / .NET**
- `async/await` frees threads during I/O (scalability, not speed). Don't block on async (`.Result`/`.Wait()`), which risks deadlocks and thread-pool starvation. Use `ConfigureAwait(false)` in libraries.
- `Task.WhenAll` for parallel I/O; `Parallel.ForEachAsync` / `Channel<T>` for bounded concurrency; `SemaphoreSlim` to limit concurrency; `CancellationToken` everywhere.
- ASP.NET Core: middleware pipeline, dependency injection lifetimes (**singleton / scoped / transient**; never inject scoped services into singletons),
  minimal APIs vs controllers, `IHttpClientFactory` (avoids socket exhaustion), Polly for resilience, EF Core (tracking vs `AsNoTracking`, migrations, N+1 via `Include`).

**Python**
- The **GIL** lets only one thread execute Python bytecode at a time (free-threaded builds are experimental since 3.13), so threads help I/O-bound work, not CPU-bound work.
  Use `multiprocessing`/process pools (or native extensions) for CPU-bound work.
- `asyncio`: a single-threaded event loop; never call blocking I/O inside `async def` (use async clients or `run_in_executor`/`asyncio.to_thread`).
- **FastAPI:** `async def` endpoints run on the event loop; plain `def` endpoints run in a threadpool. Pydantic models validate requests and responses; dependency injection with `Depends`;
  run with Uvicorn workers (or Gunicorn + Uvicorn workers) for multiple processes.

## Production readiness checklist

Health/readiness endpoints · structured logging with correlation IDs · metrics (RED: rate, errors, duration) · distributed tracing (OpenTelemetry) ·
timeouts on every outbound call · rate limiting · input validation · secrets in a vault · graceful shutdown · feature flags · runbooks.
