# Story bank

These are **skeletons** built from your known work. They're deliberately incomplete: fill in the real details,
numbers, names (anonymized), and dates yourself. **Don't present anything you can't defend under three levels of
follow-up.** Keep each story to ~2.5 minutes spoken.

Fill in every `[ ]`. Then map each story to the questions in [question-bank.md](question-bank.md).

---

## Story 1: Building and scaling the RAG platform ("Crystal")

- **Situation:** Enterprise RAG platform at Cisco serving thousands of users. [ ] What problem did it replace? Who were the users? What was the baseline?
- **Task:** [ ] What did you own: architecture, team, roadmap? What made it hard (permissions, data quality, latency, scale, stakeholders)?
- **Actions (pick 3):** [ ] Key architecture decisions (hybrid retrieval? re-ranking? chunking strategy?) and the alternatives you rejected.
  [ ] How you set up evaluation. [ ] How you handled access control. [ ] How you got teams to adopt it.
- **Result:** [ ] Users, queries/day, quality metric change, latency, cost, teams onboarded.
- **Learning:** [ ] What would you design differently today?
- **Works for:** biggest technical achievement · technical decision under ambiguity · influence without authority · Dive Deep · Think Big.

## Story 2: Multi-agent document processing pipeline

- **Situation:** A multi-agent document pipeline processing ~70K documents/month on Azure. [ ] Which documents, which downstream business process, what was manual before?
- **Task:** [ ] Your role: architect/lead? Deadline? Accuracy requirement?
- **Actions:** [ ] Why multiple specialized agents vs one prompt. [ ] How you handled low-confidence results (human review?).
  [ ] Infrastructure choices (queues, Functions, scaling, retries). [ ] One production incident and how you handled it.
- **Result:** [ ] Throughput, straight-through-processing rate, hours saved, error rate, cost per document.
- **Learning:** [ ]
- **Works for:** delivering under pressure · Insist on the Highest Standards · Invent and Simplify · a production failure.

## Story 3: Leading a large team (8–20 engineers)

- **Situation:** [ ] Which program/team, how many people, what mix (onshore/offshore, contractors, seniority)?
- **Task:** [ ] The leadership challenge: missed deadlines, low morale, unclear priorities, scaling the team?
- **Actions:** [ ] Process or structure you changed. [ ] How you delegated technical ownership. [ ] A hard conversation you had.
- **Result:** [ ] Delivery metrics, retention, promotions of people you mentored.
- **Works for:** Hire and Develop the Best · mentoring · managing underperformance · Ownership.

## Story 4: Growing an engineer (mentorship)

- [ ] One specific person: where they started, what you did (stretch assignments, design reviews, feedback), where they are now.
- **Works for:** developing others · Staff "multiplier" signal · Google Leadership.

## Story 5: Disagreement with a leader or peer (and you were right, or wrong)

- [ ] A real technical or product disagreement (e.g. build vs buy, fine-tune vs RAG, a deadline vs quality trade-off).
- [ ] How you made your case (data, prototype, written doc) → outcome → how you committed if overruled.
- **Works for:** Have Backbone; Disagree and Commit · conflict · Earn Trust.

## Story 6: A failure or mistake you owned

- [ ] A launch that went wrong, a design that didn't scale, an estimate you missed.
- [ ] Your part in it, the fix, the systemic prevention, and what you changed about how you work.
- **Works for:** failure · Ownership · Learn and Be Curious · Earn Trust.

## Story 7: Simplifying something complex / saving cost

- [ ] E.g. a cost reduction in LLM spend (routing, caching, smaller models) or removing a component.
- **Works for:** Frugality · Invent and Simplify · technical judgment.

## Story 8: Working through ambiguity / defining direction

- [ ] A time there was no clear spec ("make our support smarter with AI"), and you defined the problem, the success metrics, and the roadmap.
- **Works for:** ambiguity · Think Big · Staff scope · Google "comfort with ambiguity".

## Story 9: Customer obsession

- [ ] A time you changed a technical plan because of user feedback or data (e.g. evaluation showed users wanted citations; you reprioritized).
- **Works for:** Customer Obsession · product sense.

## Story 10: Learning something new fast

- [ ] E.g. moving from .NET/full-stack into GenAI/agents; a certification (GH-300) or a new stack under deadline.
- **Works for:** Learn and Be Curious · growth mindset (Microsoft) · adaptability.

## Story 11 (full-stack): Unified Action Tracker

- **Situation:** A greenfield multi-tenant React/.NET platform replacing Azure DevOps workflows with a central action-management system. [ ] Why replace ADO? Who were the users?
- **Actions:** [ ] API and data-model design; Redis-backed low-latency architecture; analytics dashboards; migration tooling.
- **Result:** Migrated 10K+ records with zero data loss for global users. [ ] Latency, adoption, availability numbers.
- **Works for:** full-stack ownership · zero-downtime migration · Insist on the Highest Standards · Deliver Results.

## Story 12 (full-stack): Scaling an app from 30 to 5,000+ users

- **Situation:** React + .NET applications and copilots whose adoption grew from about 30 to 5,000+ users. [ ] What drove the growth?
- **Actions:** [ ] What broke as usage grew (performance, caching, data model, support load) and what you changed. Redis caching and optimized data models for low-latency APIs.
- **Result:** [ ] Latency/availability before vs after; team practices you introduced.
- **Works for:** Customer Obsession · scaling · technical judgment · product sense. Also pairs with the Microsoft 365 Admin Center feedback platform (React, .NET, SQL Server, Azure) as a second example.

---

## Practice log

| Date | Story | Question asked | Time | What to tighten |
|---|---|---|---|---|
| | | | | |
