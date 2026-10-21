# core-foundry

Interview prep for two tracks at FAANG and similar companies (Google, Meta, Amazon, Apple, Microsoft, Netflix, NVIDIA):

- **Staff / Senior Applied AI and ML Engineer**
- **Senior / Staff Full-Stack Engineer** (React/Angular, Node.js, C#/.NET, Python, Azure/AWS)

Notes to read, and **340+ questions to quiz yourself** with spaced repetition.

Everything here is written for this repo in plain language, with links to the best public sources
(GitHub repos, books, engineering blogs, official pages) for going deeper.

## Start here

1. Read [00-strategy/loops-by-company.md](00-strategy/loops-by-company.md) (what each loop looks like in 2026) and
   [00-strategy/staff-level-signals.md](00-strategy/staff-level-signals.md) (what earns the Staff level).
2. Follow the [STUDY_PLAN.md](STUDY_PLAN.md) (10 weeks, ~1.5–2 h/day; compressible to 4 weeks). It has an AI/ML track and a full-stack track.
3. Quiz yourself daily, using either:
   - **Terminal:** `python tools/quiz.py` (no install; Python 3.9+)
   - **Browser / phone:** open [`quiz.html`](quiz.html). It's a single file that works offline.

## Contents

| Section | What's inside |
|---|---|
| [00-strategy](00-strategy/) | Loops by company, Staff-level signals, the new AI-assisted coding round |
| [01-coding](01-coding/README.md) | 9 pattern guides with tested Python templates, a 121-problem curated list, complexity and Python cheat sheets |
| [02-system-design](02-system-design/README.md) | Framework, building blocks and trade-offs, estimation, 12 classic case studies |
| [03-ml-system-design](03-ml-system-design/README.md) | Framework, metrics and A/B testing, 8 case studies (recs, search, ads, fraud, integrity, ETA…) |
| [04-genai-system-design](04-genai-system-design/README.md) | **The round most likely to decide an Applied AI loop:** RAG, LLM serving, agents, evaluation, fine-tuning, safety, 8 case studies, Azure → generic/GCP/AWS mapping |
| [05-ml-fundamentals](05-ml-fundamentals/README.md) | Classical ML, deep learning, transformers and LLMs, probability and statistics |
| [07-full-stack](07-full-stack/README.md) | **Full-stack track:** JS/TS, React, browser performance and accessibility, frontend system design, APIs and auth, SQL, web security (OWASP 2025), DevOps, tested JS utilities, plus a deep dive on every technology on your resume (Node.js, .NET/EF Core/MVC, Python, Angular, Redux, D3, HTML/CSS, Azure, AWS, SQL Server, Cosmos DB, MongoDB, Redis, Docker, Postman) |
| [06-behavioral](06-behavioral/README.md) | STAR-L, a story bank built around your projects (fill in), a question bank, all 16 Amazon LPs |
| [quizzes](quizzes/README.md) | The question bank (JSON) and how to add your own questions |
| [RESOURCES.md](RESOURCES.md) | Curated external resources: GitHub repos, books, courses, blogs |

## Quiz tool

```bash
python tools/quiz.py                        # 15 questions, due-for-review first, then new
python tools/quiz.py --topic genai -n 20    # one topic (prefix match: --topic gen)
python tools/quiz.py --topic full-stack --tag dotnet   # full-stack track, one technology
python tools/quiz.py --topic coding --topic system-design
python tools/quiz.py --mode cards           # flashcards: answer out loud, then self-grade
python tools/quiz.py --tag rag --tag agents # by tag
python tools/quiz.py --due                  # only what's due today (daily review)
python tools/quiz.py --stats                # mastery per topic + weakest tags
python tools/quiz.py --list                 # topics and counts
```

**How spaced repetition works here:** each question sits in a box (0–5). Correct (or "good") moves it up a box;
wrong ("again") sends it back to 0; "hard" keeps it in place. A question is due again after 0, 1, 3, 7, 16, or 35 days
depending on its box. "Mastered" means it reached box 3. CLI progress is saved to `.progress.json` (git-ignored; commit it
if you want it on other machines). Browser progress is saved in that browser.

After adding or editing questions, run `python tools/validate.py` and `python tools/build_web_quiz.py` to refresh `quiz.html`.

## Repo maintenance

```bash
python -m unittest discover tests     # tests every Python template + the quiz logic + the question bank
node --test tests/js/practical.test.mjs   # tests every JavaScript utility in 07-full-stack/practical-coding.md
python tools/problems.py              # regenerate 01-coding/problem-list.md
python tools/build_web_quiz.py        # regenerate quiz.html
```

CI ([.github/workflows/ci.yml](.github/workflows/ci.yml)) runs the tests and checks that `quiz.html` is up to date.

## A note on accuracy

Interview formats change fast. The company loop notes were checked in October 2026 and cite their sources. Some sources
are third-party reports, so confirm details (AI tool policy, in-person vs virtual, number of rounds) with your recruiter.
