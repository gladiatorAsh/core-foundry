# LLM system design framework

Example prompts: *"Design a customer support assistant over our help center."* *"Design an internal enterprise
search/copilot."* *"Design an agent that books travel."* *"Design ChatGPT-like serving for 10M users."*

## 1. Clarify (5–8 min)

- **Users and job to be done.** Who asks what? What does success look like (deflection rate, time saved, task completion)?
- **Knowledge sources:** what data, how much, how fresh, what formats, and **who is allowed to see what** (ACLs).
- **Actions:** read-only answers, or does it *do* things (refunds, tickets, emails)? Actions change the risk profile.
- **Quality bar and risk:** cost of a wrong answer (legal/medical/financial = high), need for citations, human handoff.
- **Scale and latency:** QPS, concurrent sessions, acceptable time-to-first-token (e.g. < 1 s) and total latency.
- **Constraints:** budget per request, data residency, model choices (hosted API vs self-hosted open weights), languages.

## 2. Decide whether you need an LLM, and how much

- Could search + templates do it? Could a classifier route 60% of traffic to canned flows?
- Start with **prompting + retrieval**; fine-tune only with evidence (see [fine-tuning-and-alignment.md](fine-tuning-and-alignment.md)).
- **Workflow before agent:** fixed steps you can test beat open-ended autonomy unless the task truly needs it.

## 3. High-level architecture (draw this)

```
Client ──► API gateway (auth, rate limit, tenant) ──► Orchestrator
                                                     │  ├─ input guardrails (PII, injection, policy)
                                                     │  ├─ query understanding / routing (intent, model tier)
                                                     │  ├─ retrieval (hybrid search + ACL filter + re-rank)
                                                     │  ├─ prompt assembly (versioned templates, token budget)
                                                     │  ├─ LLM call(s) via model gateway (fallbacks, caching)
                                                     │  ├─ tool calls (if agentic) with permission checks
                                                     │  └─ output guardrails (grounding check, safety, format)
                                                     ▼
                                   Streaming response (SSE) + citations
Offline: ingestion pipeline → chunk → embed → index        Observability: traces, evals, feedback, cost
```

## 4. Deep dives (pick 2–3, depending on the interviewer's interest)

1. **Retrieval quality:** chunking, hybrid search, re-ranking, query rewriting, permission trimming ([rag.md](rag.md)).
2. **Evaluation:** golden sets, LLM-as-judge with calibration, online signals, release gates ([evaluation.md](evaluation.md)).
3. **Latency and cost:** streaming, caching (exact, semantic, prompt/prefix), model routing, token budgets ([llm-serving.md](llm-serving.md)).
4. **Safety:** prompt injection from documents, data exfiltration, tool permissioning ([safety-and-guardrails.md](safety-and-guardrails.md)).
5. **Agents:** planning, tool schemas, loops, idempotency, human-in-the-loop ([agents.md](agents.md)).
6. **Freshness and updates:** incremental indexing, deletes (right to be forgotten), re-embedding on model change.

## 5. Rollout and operations

Offline eval gate → internal dogfood → shadow mode → small % A/B with guardrail metrics → ramp.
Version **prompts, models, retrieval config, and indexes** together; be able to roll back each independently.
Monitor: answer rate, citation rate, thumbs-down rate, escalations, latency (TTFT, p95 total), cost/request, safety flags.

## Staff-level talking points

- "Quality is a retrieval problem before it's a generation problem. I'd measure recall@k first."
- "Every model upgrade is a regression risk, so prompts and models ship behind the same eval gate as code."
- "Permissions are enforced at retrieval time with security filters, never by asking the model to hide things."
- "Cost scales with tokens, not requests. The biggest levers are context size, model routing, and caching."
- "For actions, the model proposes and deterministic code with the user's own permissions executes."
