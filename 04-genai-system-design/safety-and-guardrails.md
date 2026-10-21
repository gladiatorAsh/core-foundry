# Safety, security, and guardrails

## Threats (know the OWASP Top 10 for LLM Applications)

| Threat | Example | Mitigations |
|---|---|---|
| **Direct prompt injection / jailbreak** | "Ignore previous instructions and…" | Input classifiers (e.g. Prompt Shields, Llama Guard), robust system prompts, output checks, least privilege |
| **Indirect prompt injection** | A retrieved web page or email contains hidden instructions | Treat retrieved/tool content as data, delimit it clearly, **never grant it authority**, restrict tools, confirm actions with the user |
| Sensitive data disclosure | Model reveals another user's data or secrets | ACL-filtered retrieval, no secrets in prompts, PII redaction, per-tenant isolation, output DLP scanning |
| Excessive agency | Agent deletes data or emails customers on bad reasoning | Least-privilege tools, approvals for high-impact actions, rate limits, dry-run modes |
| Improper output handling | LLM output rendered as HTML/SQL/shell | Escape/validate outputs; never execute generated code outside a sandbox |
| Data/model poisoning | Malicious docs inserted into the index or training data | Source allow-lists, ingestion review, provenance tracking |
| Unbounded consumption | Prompt floods drive cost/DoS | Token-based rate limits, max context/output, per-tenant budgets |
| System prompt leakage | Users extract hidden instructions | Assume prompts are public; keep secrets out |
| Misinformation / hallucination | Confident wrong answers | Grounding, citations, abstention, human review for high-risk domains |

## Guardrail architecture

```
input  → [authN/authZ] → [rate/budget check] → [PII detection/redaction] → [injection & policy classifier]
       → orchestrator (tools run with the USER's permissions)
output → [schema validation] → [groundedness check] → [content safety classifier] → [PII/DLP scan] → user
```

Guardrails add latency, so run classifiers in parallel with retrieval, use small fast models, and apply the
expensive checks only on risky routes.

## Governance (enterprise and FAANG both care)

- Audit logs of prompts, retrieved sources, tool calls, and outputs (with retention and access controls).
- Data handling: no training on customer data without consent; regional processing; deletion workflows.
- Red-teaming before launch and periodically; abuse monitoring dashboards.
- Model cards / system cards documenting intended use and limitations.
- Responsible AI reviews for sensitive uses (hiring, lending, health).
- Regulation awareness: EU AI Act risk tiers, sector rules (HIPAA, financial). Don't over-claim legal expertise in interviews.
