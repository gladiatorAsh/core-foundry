# What "Staff" means in an interview

Interviewers aren't checking whether you can do the work. They're checking **the scope at which you operate**.
Senior-level answers in a Staff loop get down-leveled even when they're correct.

| Dimension | Senior (L5/E5) | Staff (L6/E6) |
|---|---|---|
| Scope | A project / a team | Multiple teams, a whole system, a multi-quarter roadmap |
| Ambiguity | Takes a defined problem and executes | Defines the problem: what to build, what *not* to build, and why |
| Design | A working design | A design with explicit trade-offs, failure modes, migration path, cost, and an evolution plan |
| Influence | Leads their team | Aligns teams and leaders without authority; resolves cross-org conflict |
| Technical judgment | Picks good tools | Knows when *not* to use ML/LLMs; sets technical direction and standards |
| People | Mentors juniors | Grows senior engineers; raises the bar for the org (reviews, design docs, hiring) |
| Impact | Shipped features | Moved business metrics; changed how other teams build |

## In each round

**Coding:** Staff candidates are expected to be clean and fast, but coding rarely earns the level.
Don't lose it here. Narrate trade-offs, test without being asked, and finish with time to spare.

**System design:** drive the conversation. Spend the first 5–8 min on requirements and **what success
means** (SLOs, metrics, cost envelope). Name 2–3 alternatives for each big decision and pick one with a
reason. Proactively cover: failure modes, data consistency, observability, security/privacy, rollout and
migration, cost. Close with "what I'd do in v2" and "what I'd measure".

**ML / GenAI design:** start from the business objective, then the ML objective. Say why ML/LLM at all, and
what the non-ML baseline is. Evaluation design (offline + online) is where Staff candidates separate themselves.

**Behavioral:** stories must show **cross-team scope**, **a decision you owned under ambiguity**, **a conflict
you resolved with data**, **someone you grew**, and **a failure with a real lesson**. Use numbers.

## Phrases that signal Staff thinking

- "Before we design, what does success look like in six months, and what will we *not* support?"
- "There are two viable approaches. Here's the trade-off, and here's what would make me switch."
- "The riskiest part is X, so I'd de-risk it first with a spike or a shadow deployment."
- "This needs agreement from teams A and B; here's how I'd get it."
- "I'd measure this with ..., and I'd roll back if ..."

## Your angle (Applied AI, enterprise)

Your strongest Staff signals: you've **owned production RAG and multi-agent systems end to end** (a platform
serving thousands of users, a document pipeline processing ~70K documents/month) and **led teams of 8–20**.
Make sure every design answer includes the parts most candidates skip: evaluation harnesses, permission-aware
retrieval, cost per request, rollout and guardrails. That's where you're ahead.
