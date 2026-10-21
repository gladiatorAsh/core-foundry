# DevOps and cloud fundamentals

## CI/CD

- **CI:** every push runs lint → type-check → unit tests → build → integration tests → security scans (dependencies, secrets, SAST). Fast feedback (< 10 min).
- **CD:** build once, promote the same artifact through environments; infrastructure as code (Terraform, Bicep, Pulumi); automated rollback on health-check failure.
- Trunk-based development + feature flags beats long-lived branches for fast-moving teams.
- Test pyramid: many unit tests, fewer integration tests, few E2E tests. Contract tests between services.

## Deployment strategies

| Strategy | How | Trade-off |
|---|---|---|
| Rolling | Replace instances gradually | Simple; old and new versions run together (must be compatible) |
| **Blue/green** | Two full environments; switch traffic | Instant rollback; double capacity during the switch |
| **Canary** | Small % of traffic to the new version, watch metrics, ramp up | Catches problems early; needs good metrics and automation |
| Feature flags | Deploy dark, release by flag | Decouples deploy from release; flag debt must be cleaned up |
| Shadow | Mirror traffic to the new version, discard responses | Safe for testing load/behavior (also used for new ML models) |

Database changes must be backward compatible across a deploy (expand → migrate → contract).

## Containers and Kubernetes (enough for interviews)

- Containers: image layers, small base images (distroless/alpine), multi-stage builds, run as non-root, one process per container, config via environment variables.
- Kubernetes objects: **Pod** (one or more containers), **Deployment** (replicas + rolling updates), **Service** (stable virtual IP/DNS for pods),
  **Ingress / Gateway** (HTTP routing), **ConfigMap/Secret**, **HPA** (autoscale on CPU/memory/custom metrics), **liveness vs readiness probes**
  (restart a stuck container vs remove it from load balancing), resource requests/limits, namespaces.
- When not to use Kubernetes: small teams and simple services are often better served by PaaS (App Service, Container Apps, Cloud Run).

## Observability

- **Logs** (structured JSON, correlation IDs), **metrics** (RED for services: rate, errors, duration; USE for resources: utilization, saturation, errors),
  **traces** (OpenTelemetry spans across services).
- **SLIs/SLOs/error budgets:** e.g. SLI = % of requests < 300 ms; SLO = 99.9% over 30 days; spending the error budget slows feature releases.
- Alert on user-facing symptoms (SLO burn rate), not every CPU spike. Every alert needs a runbook.

## The Twelve-Factor App (the ones interviewers ask about)

Config in the environment · stateless processes (state in backing services) · dev/prod parity · logs as event streams ·
disposability (fast start, graceful shutdown) · backing services as attached resources · one codebase, many deploys.

## Cloud cost basics

Right-size instances, autoscale, use reserved/committed capacity for steady load and spot/preemptible for batch, put CDN in front of static content,
move cold data to cheaper storage tiers, set budgets and alerts, tag resources by team. For AI features: token budgets, caching, model routing.
