# GenAI system design case studies

Each one: **clarify → architecture → deep dives → evaluation → risks**. Rehearse out loud in 45 minutes.

---

## 1. Enterprise knowledge copilot (internal search + Q&A over Confluence/SharePoint/Drive)

**Clarify:** 50K employees, ~2M docs, strict permissions, answers must cite sources, < 2 s TTFT.

**Architecture:** connectors with change feeds and ACL capture → parse/chunk (structure-aware, contextual headers) →
embed → hybrid index with ACL fields. Query path: rewrite follow-ups → hybrid search **with the user's group filter** →
cross-encoder re-rank → prompt with citations → stream → groundedness check.

**Deep dives:** ACL sync lag (permission revoked but still indexed: short sync intervals plus a live
permission check on the top-k for sensitive sources); freshness; multilingual content; "who owns this?" questions
(people search as a tool).

**Eval:** golden set per department, retrieval recall@10, faithfulness, citation accuracy; online thumbs, reformulation rate, search-to-answer clicks.

**Risks:** data leakage (the top risk), stale content, over-reliance. Show a "sources" panel and confidence.

*Your story hook:* this is close to a RAG platform you've led for thousands of users. Use real numbers and the lessons you learned.

## 2. Customer support agent (answers + actions: refunds, order changes)

**Architecture:** triage router (intent + risk) → FAQ/RAG answers for informational intents; tool-using agent for
actions with **tools scoped to the authenticated customer**; policy engine checks (refund ≤ $X auto, above → human);
handoff to a human with a conversation summary.

**Deep dives:** tool design + idempotency (no double refunds), conversation state machine, escalation triggers
(sentiment, repeated failure, explicit request), multilingual, cost per resolved ticket.

**Eval:** resolution/deflection rate, CSAT, escalation precision, wrong-action rate (target ~0), policy violations.

## 3. Document intelligence pipeline (invoices, contracts, forms at 70K+ docs/month)

**Architecture:** ingest (email/upload/API) → queue → OCR/layout extraction → classifier (doc type, language) →
translation if needed → **specialized extraction agents** per doc type with schema-constrained output → validation
(business rules, cross-field checks, confidence) → auto-approve or **human review queue** → downstream systems.

**Deep dives:** confidence calibration and review routing, parallelism and retries per stage, cost per document
(small models for classification, large only for hard extractions), audit trail, re-processing when prompts change.

**Eval:** field-level precision/recall/exact match by doc type, straight-through-processing rate, reviewer correction rate, latency SLA.

*Your story hook:* the multi-agent pipeline you led. Have the architecture, the numbers, and one hard trade-off ready.

## 4. Coding assistant (IDE autocomplete + chat)

**Two products with different latency budgets:** inline completion (< ~300 ms, small fast model, fill-in-the-middle,
context from the open files plus nearby code retrieved from the repo) and chat/agent (larger model, repo-wide retrieval, tool use: run tests, search code).

**Deep dives:** context selection (repo graph, recently edited files), caching, telemetry for acceptance rate,
security (secrets in context, license filtering), enterprise isolation.

**Eval:** acceptance rate, retained-code rate after N minutes, pass@k on internal tasks, SWE-bench-style agent tasks.

## 5. LLM gateway / platform for a whole company

**Features:** single API for many models/providers; authN, per-team quotas and budgets (tokens/min, $/month);
routing (by task, cost, latency, region); fallbacks; prompt registry; caching (exact + semantic); PII redaction;
logging/tracing; eval hooks; usage chargeback.

**Deep dives:** token-bucket rate limiting per tenant and per upstream deployment, failover between regions,
streaming through the gateway, data retention policies, adding a new model safely (eval gate + shadow).

## 6. ChatGPT-scale consumer chat serving

**Focus:** GPU capacity planning by tokens/s, continuous batching, KV cache memory, prefix caching for system prompts,
model routing (small model for simple turns), conversation storage, abuse prevention, multi-region failover,
graceful degradation under load (queueing, shorter max output, smaller model).

## 7. Semantic search for e-commerce (text + image)

**Architecture:** product embeddings (text + image, CLIP-style), hybrid with BM25 for brands/SKUs, learning-to-rank
with behavioral features, query understanding with an LLM for attribute extraction ("red running shoes under $100" → filters).

**Eval:** NDCG on judged queries, zero-result rate, conversion, revenue per search.

## 8. Meeting summarizer / action-item extractor

**Architecture:** speech-to-text with diarization → chunked map-reduce or hierarchical summarization for long
transcripts → structured extraction (decisions, owners, due dates) → user review → push to task tracker (tool call with approval).

**Deep dives:** long-context vs map-reduce trade-offs, speaker attribution errors, privacy/consent, latency for live notes.

**Eval:** human rubric (coverage, accuracy, no hallucinated action items), action-item precision/recall.
