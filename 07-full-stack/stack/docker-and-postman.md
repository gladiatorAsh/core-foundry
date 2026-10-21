# Docker and Postman

## Docker

**Concepts:** an **image** is a read-only stack of layers; a **container** is a running instance with a writable layer; a registry (ACR, ECR, Docker Hub) stores images.
Containers share the host kernel (namespaces + cgroups for isolation), so they're lighter than VMs but less isolated.

**Dockerfile best practices**

```dockerfile
# Multi-stage build for an ASP.NET Core API: the SDK is only in the build stage, so the final image is small
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY *.csproj ./
RUN dotnet restore                      # cached unless the project file changes
COPY . .
RUN dotnet publish -c Release -o /app --no-restore

FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=build /app .
USER app                                # don't run as root (the .NET 8+ images ship a non-root 'app' user)
EXPOSE 8080
ENTRYPOINT ["dotnet", "Api.dll"]
```

- Order instructions from least to most frequently changing so **layer caching** works (dependency manifests before source code).
- Use `.dockerignore` (exclude `.git`, `node_modules`, `bin/obj`, secrets). Pin base image versions (or digests). Prefer slim/distroless bases.
- One process per container; logs to stdout/stderr; configuration via environment variables; secrets from the orchestrator or a vault, **never baked into images**.
- `HEALTHCHECK` or orchestrator probes; handle SIGTERM for graceful shutdown (`exec`-form `ENTRYPOINT` so the app is PID 1 and receives signals).
- Scan images (Trivy, Defender, ECR scanning) and rebuild regularly for base-image patches.
- **docker compose** for local multi-service development (API + DB + Redis), with healthcheck-based `depends_on`.
- `ENTRYPOINT` (the executable) vs `CMD` (default args); `COPY` (preferred) vs `ADD` (also extracts archives / fetches URLs).

## Postman (API testing workflow)

- **Collections** organize requests; **environments** hold variables (`{{baseUrl}}`, `{{token}}`) per environment (dev/staging/prod); collection and global variables; secrets as secret-type variables (not committed).
- **Pre-request scripts** (generate auth tokens, timestamps, signatures) and **tests** in JavaScript:

```js
pm.test("returns 201 with an id", () => {
  pm.response.to.have.status(201);
  const body = pm.response.json();
  pm.expect(body.id).to.be.a("string");
  pm.collectionVariables.set("orderId", body.id);   // chain into the next request
});
```

- Run collections in CI with **Newman** (or the Postman CLI); data-driven runs with CSV/JSON files; mock servers for frontend work before the backend exists;
  monitors for scheduled checks; generate collections from OpenAPI specs; contract testing against the schema.
- Interview angle: explain how you test APIs at each level: unit tests (xUnit/pytest) → integration tests (WebApplicationFactory/TestClient + Testcontainers) →
  contract/API tests (Postman/Newman or schema-based) → E2E (Playwright) → load tests (k6, JMeter, Azure Load Testing).
