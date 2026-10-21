# Interview loops by company (Staff / Senior Applied AI & ML roles)

> **Read this first:** loops change often and differ by org and team. Everything below was checked in
> October 2026 against the sources at the bottom of this page, and some of those sources are
> third-party reports rather than official statements. **Ask your recruiter for the exact loop,
> whether rounds are virtual or in person, and whether AI tools are allowed in any round.** Recruiters
> will tell you, and it's the single highest-value question you can ask.

## Level map (rough equivalents)

| Company | Senior | Staff | Senior Staff / Principal |
|---|---|---|---|
| Google | L5 | **L6** | L7 |
| Meta | E5 | **E6** | E7 |
| Amazon | SDE III / L6 | **Principal L7** (big jump) | L8 |
| Apple | ICT4 | **ICT5** | ICT6 |
| Microsoft | 63–64 (Senior) | **65–67 (Principal)** | 68+ |
| Netflix | Senior (L5) | **L6** | L7 |
| NVIDIA | Senior | **Principal / Staff** | Distinguished |

The level you're *interviewed* at and the level you're *offered* can differ. At Staff, the
design and behavioral rounds decide the level more than coding does.

## What's new in 2025–2026 (affects how you practice)

- **AI-assisted coding at Meta.** From late 2025, Meta added an AI-assisted coding round: CoderPad with
  an AI chat panel, typically 60 min, closer to pair programming on a realistic, multi-part problem.
  You're scored on problem solving, code quality, *how you steer and verify the AI*, and communication.
  Reports say E6 has one standard + one AI-assisted round, and at E7+ the AI-assisted round replaces both
  coding rounds. See [ai-assisted-coding.md](ai-assisted-coding.md).
- **Google went back to some in-person rounds** to counter AI cheating in remote interviews (Sundar Pichai,
  2025). Many loops are still virtual; ask. Google's standard coding environment is plain text with
  **no execution and no autocomplete**, so practice writing correct code without running it.
- **Amazon bans GenAI tools during interviews** unless explicitly permitted (internal guidance reported
  March 2025); using them can disqualify you.
- **ML system design shifted to LLM systems.** The most common ML design prompt is now "design an
  LLM-powered X" (support assistant over a knowledge base, enterprise search, agent). Classic
  recommender and ranking questions still appear, especially at Meta, Netflix, Google Ads and YouTube.

---

## Google (L6 Staff SWE / ML)

| Stage | Format |
|---|---|
| Google Hiring Assessment | Online work-style questionnaire (multiple choice/Likert). Low scores can end the process. |
| Recruiter screen | ~30 min: background, scope, motivation. |
| Technical screen | 1–2 × 45 min coding on a plain doc (no run, no autocomplete). |
| Onsite (4–6) | **2 coding** (45 min, harder), **2 system design** (60 min; ML-flavored for ML roles), **1 Role-Related Knowledge** (deep dive on your past technical decisions / ML depth), **1 Googleyness & Leadership** |
| After | Hiring committee → team matching → offer. Team match can take weeks. |

**What decides L6 vs L5:** system design depth at global scale (multi-region, consistency, failure modes,
cost), and leadership stories about influence across teams without authority.
**Googleyness:** collaboration, comfort with ambiguity, bias to learning from failure, no "lone hero" stories.

## Meta (E6 / E7, ML or Product/Infra)

| Stage | Format |
|---|---|
| Screen | Coding (45 min, 2 problems) — E6 may get a combined leadership + coding assessment instead |
| Onsite | Coding (standard: 45 min, 2 problems, **code execution off**), **AI-assisted coding** (60 min), **System design** (Product Architecture or Infra/Distributed, or **ML System Design** for MLE), **Behavioral** ("Jedi": conflict, ambiguity, growth, impact) |
| After | Hiring committee → team match ("bootcamp" style for some orgs) |

**Notes:** Meta coding = speed. Two mediums in ~40 min with clean code and no hints. Behavioral alone can
down-level you, so bring Staff-scope stories (multi-quarter, multi-team, ambiguous). ML design for Meta
usually means ranking/recommendation (feed, ads, notifications, Reels), plus LLM integration questions.

## Amazon (SDE III / Principal, Applied Scientist, ML Engineer)

| Stage | Format |
|---|---|
| Online assessment | Sometimes skipped for senior candidates |
| Phone screen | Coding + 1–2 Leadership Principle (LP) questions |
| Loop (4–5) | Each round = **LP questions (~half the time)** + technical (coding, system design, or ML depth). One interviewer is the **Bar Raiser** (an independent interviewer from another team who can veto). |

**Notes:** Every interviewer is assigned 2–3 LPs. Prepare **2 stories per LP**, with metrics. For L7 and up,
expect "Think Big", "Have Backbone", "Are Right, A Lot", and "Dive Deep" at org-wide scope. No GenAI tools.
See [../06-behavioral/amazon-leadership-principles.md](../06-behavioral/amazon-leadership-principles.md).

## Apple (ICT5)

Team-driven; there's no single loop. Typically a hiring-manager screen, then 5–8 interviews in a day, mostly
with the team: coding (often practical), domain depth (ML/LLM for AI/ML orgs), design, and lots of
"walk me through a project you shipped". Expect privacy/on-device questions for ML (on-device inference,
quantization, federated or private learning). Strong emphasis on craft and ownership of details.

## Microsoft (Senior / Principal)

Recruiter screen → 4–5 interviews (coding, design, behavioral/culture), with a final **"As Appropriate" (AA)**
interview with a senior leader who decides. Culture questions map to growth mindset, customer focus, and
"One Microsoft" collaboration. Your Azure AI Foundry / Azure OpenAI depth is directly relevant to many AI orgs.

## Netflix (L5/L6, ML / Personalization)

Very team-specific. Expect a deep **culture** round (read the Netflix culture memo: freedom & responsibility,
candor, "keeper test"), ML design for personalization/search/experimentation, and **experimentation and
causal inference** depth (A/B tests, interleaving, metrics). Senior-only hiring, high bar for judgment.

## NVIDIA (Senior / Principal AI engineer)

Team-specific. Commonly: coding, deep domain rounds (LLM inference/training, GPU performance, CUDA basics,
TensorRT-LLM / Triton for serving roles), system design, and hiring-manager behavioral. For applied AI roles,
expect RAG/agent architecture (NeMo, NIM) and latency/throughput reasoning.

---

## Sources

- [Inside the Meta 2026 loop — Cracking the Tech Interview (Apr 2026)](https://dglearning.substack.com/p/inside-the-meta-2026-loop-rounds)
- [AI-enabled coding interview overview — AlgoMonster](https://algo.monster/ai-enabled-coding-interview)
- [Google L6 interview guide — Hello Interview](https://www.hellointerview.com/guides/google/l6)
- [Google to reintroduce in-person interviews — Storyboard18](https://www.storyboard18.com/brand-makers/google-to-reintroduce-in-person-interviews-amid-rising-ai-cheating-concerns-79624.htm)
- [Amazon bans AI tools during job interviews — ITPro (Mar 2025)](https://itpro.com/business/careers-and-training/amazon-bans-ai-tools-during-job-interviews)
- [Amazon Leadership Principles (official)](https://www.aboutamazon.com/working-at-amazon/our-leadership-principles)
- [ML engineer interview in the post-LLM era — techinterview.org](https://www.techinterview.org/post/3233474925/ml-engineer-interview-post-llm-era/)
- [Netflix culture memo](https://jobs.netflix.com/culture)
