# AWS services (from your resume)

## IAM (always comes up)

- **Principals:** users (avoid long-lived keys), groups, **roles** (assumed temporarily via STS; for services, cross-account access, and workloads).
- **Policies:** identity-based (attached to principals), **resource-based** (S3 bucket policy, SQS policy), permission boundaries, SCPs (organization-wide guardrails), session policies.
- **Evaluation logic:** an **explicit deny always wins**; otherwise access needs an explicit allow; the default is implicit deny. Cross-account access needs both sides to allow.
- A role has a **trust policy** (who can assume it) and permission policies (what it can do).
- Least privilege, no root usage, MFA, IAM Access Analyzer, short-lived credentials (roles for EC2/ECS/Lambda; OIDC federation for CI instead of access keys).

## ECS (Elastic Container Service)

- **Task definition** (container images, CPU/memory, env vars, secrets, ports, logging) → **task** (running instance) → **service** (keeps N tasks running, integrates with load balancers, rolling or blue/green deploys via CodeDeploy).
- Launch types: **Fargate** (serverless; no instances to manage) vs EC2 (you manage the cluster capacity; cheaper at steady scale, GPU and custom AMIs).
- **Task execution role** (ECS agent pulls images and secrets, writes logs) vs **task role** (what your app code can access).
- Behind an ALB with target groups and health checks; service auto scaling on CPU/memory/request count; service discovery via Cloud Map / Service Connect.
- ECS vs EKS: ECS is simpler and AWS-native; EKS gives Kubernetes portability and ecosystem.

## Lambda

- Event-driven functions (API Gateway, S3, SQS, EventBridge, DynamoDB Streams). Max **15-minute** execution; memory 128 MB–10 GB (CPU scales with memory).
- **Cold starts:** new execution environments initialize runtime + code. Mitigate with smaller packages, init outside the handler, **provisioned concurrency**, or SnapStart (Java, and since 2024 Python/.NET).
- **Concurrency:** an account-level regional limit (default 1,000, raisable); reserved concurrency caps/guarantees per function; throttling returns 429 for synchronous invokes.
- SQS → Lambda: batch size, partial batch failure reporting, visibility timeout ≥ 6× function timeout, DLQ. Idempotent handlers (at-least-once delivery).
- Connecting to RDS from Lambda: use **RDS Proxy** to pool connections.

## API Gateway

- **REST APIs** (feature-rich: usage plans/API keys, request validation, caching, WAF) vs **HTTP APIs** (cheaper, faster, JWT authorizers, fewer features) vs **WebSocket APIs**.
- Throttling (token bucket: rate + burst) at account, stage, and method levels; usage plans per API key.
- Authorizers: IAM, Cognito, JWT, Lambda authorizers. Integration timeout is about 29 s by default, so long work goes async (return 202, process via SQS/Step Functions).

## RDS (and Aurora)

- Managed relational databases (Postgres, MySQL, SQL Server, Oracle, MariaDB): automated backups, point-in-time restore, patching.
- **Multi-AZ:** a synchronous standby in another AZ for **high availability** (automatic failover, typically 1–2 min); not for read scaling.
- **Read replicas:** asynchronous copies for **read scaling** (replication lag); can be cross-region and promoted.
- Aurora: shared distributed storage (6 copies across 3 AZs), fast failover, up to 15 low-lag replicas, Aurora Serverless v2 for variable load.
- Parameter groups, Performance Insights, encryption at rest (KMS), IAM database authentication, Secrets Manager rotation.

## S3

- Object storage with **11 nines of durability**. Strong read-after-write consistency for all operations (since Dec 2020).
- Storage classes: Standard, Intelligent-Tiering, Standard-IA, One Zone-IA, Glacier Instant/Flexible Retrieval, Glacier Deep Archive; lifecycle rules move/expire objects.
- **Presigned URLs** for time-limited direct client uploads/downloads (keeps large files off your servers). Multipart upload for large objects.
- Block Public Access on by default; bucket policies, encryption (SSE-S3/SSE-KMS), versioning + Object Lock, event notifications (to Lambda/SQS/EventBridge), CloudFront in front for delivery.

## CloudWatch

Metrics (namespaces, dimensions, custom metrics, embedded metric format), Logs (log groups, Logs Insights queries, metric filters, retention settings),
Alarms (on metrics or composite; actions to SNS/auto scaling), dashboards, X-Ray / Application Signals for tracing, Synthetics canaries.

## Your multi-region order-processing experience (story hook)

You've used ECS, RDS, IAM, and load balancing in a multi-region order-processing app. Be ready to explain: the region strategy (active-active vs active-passive),
how data was replicated, how failover worked, and what you'd change today. Pair it with [../../02-system-design/case-studies.md](../../02-system-design/case-studies.md).

## Azure ↔ AWS quick map

App Service ↔ Elastic Beanstalk / App Runner · Functions ↔ Lambda · Service Bus ↔ SQS/SNS · Event Grid ↔ EventBridge · Event Hubs ↔ Kinesis ·
Cosmos DB ↔ DynamoDB · Azure SQL ↔ RDS · Blob ↔ S3 · Key Vault ↔ Secrets Manager/KMS · Entra ID ↔ IAM Identity Center/Cognito · App Insights ↔ CloudWatch/X-Ray · Logic Apps ↔ Step Functions.
