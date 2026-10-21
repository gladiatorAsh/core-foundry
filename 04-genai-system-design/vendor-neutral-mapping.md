# Translating your Azure stack for FAANG interviews

FAANG interviewers want **concepts and trade-offs**, not product names, and they may not know Azure services.
Name the generic component first, then optionally "for example, Azure AI Search". At Google, expect GCP
equivalents; at Amazon, AWS. Never let a product name stand in for an explanation.

| Generic capability | Azure (your experience) | GCP | AWS | Open source / self-hosted |
|---|---|---|---|---|
| LLM API | Azure OpenAI / Azure AI Foundry models | Vertex AI (Gemini) | Bedrock | vLLM / TGI serving Llama, Mistral, Qwen |
| Agent orchestration / platform | Azure AI Foundry Agent Service, Semantic Kernel | Vertex AI Agent Builder, ADK | Bedrock Agents / AgentCore | LangGraph, CrewAI, AutoGen |
| Search + vector retrieval | Azure AI Search (hybrid, semantic ranker) | Vertex AI Search, Vector Search | OpenSearch, Kendra, Bedrock Knowledge Bases | Elasticsearch/OpenSearch, pgvector, FAISS, Milvus |
| Document OCR/layout | Azure AI Document Intelligence | Document AI | Textract | Tesseract, docTR, Unstructured |
| Content safety / injection detection | Azure AI Content Safety, Prompt Shields | Model Armor, safety filters | Bedrock Guardrails | Llama Guard, NeMo Guardrails |
| Evaluation & tracing | Azure AI Foundry evaluations, App Insights | Vertex AI evaluation | Bedrock evaluations, CloudWatch | Ragas, DeepEval, Langfuse, Phoenix |
| Serverless compute | Azure Functions | Cloud Run / Functions | Lambda | Knative |
| Containers | AKS, Container Apps | GKE, Cloud Run | EKS, ECS | Kubernetes |
| Messaging / streaming | Service Bus / Event Hubs | Pub/Sub | SQS / Kinesis, MSK | Kafka, RabbitMQ |
| Object storage | Blob Storage | Cloud Storage | S3 | MinIO |
| NoSQL | Cosmos DB | Firestore / Bigtable / Spanner | DynamoDB | Cassandra, MongoDB |
| Cache | Azure Cache for Redis | Memorystore | ElastiCache | Redis / Valkey |
| Secrets & identity | Key Vault, Entra ID, managed identities | Secret Manager, IAM, Workload Identity | Secrets Manager, IAM roles | Vault, OIDC |
| Workflow orchestration | Logic Apps, Durable Functions | Workflows, Composer | Step Functions | Temporal, Airflow |

## How to phrase it

- "We used a hybrid keyword + vector index with a semantic re-ranker (Azure AI Search in our case)."
- "Agents ran as stateless workers pulling from a durable queue, so retries and scaling were independent per stage."
- "Each tool call used the end user's delegated identity, so authorization was enforced by the downstream system."

## Google-specific note

You've talked to recruiters about Google roles on the **ADK (Agent Development Kit)** stack. Before a Google loop, skim the
ADK docs and Vertex AI Agent Engine. Be ready to compare ADK concepts (agents, tools, sessions/state, multi-agent
hierarchies, evaluation) with Semantic Kernel / Foundry agents you've used.
