# Full-stack engineering track

For **Senior / Staff Full-Stack, Product, Frontend-leaning, or Backend-leaning SWE** loops. The other folders still apply
(coding patterns, system design, behavioral). This folder adds what those loops test that AI/ML loops don't.

## How full-stack loops differ

| Round | AI/ML track | Full-stack track |
|---|---|---|
| Coding | Algorithms (LeetCode-style) | Algorithms **plus** a practical round: build a UI component, implement `debounce` / `Promise.all`, or build a small API |
| Design | ML / GenAI system design | Distributed system design **and/or frontend system design** (component architecture, state, data fetching, performance) |
| Domain depth | ML/LLM fundamentals | JavaScript/TypeScript, React, browser internals, HTTP, databases, security, plus your backend language (C#/.NET or Python) |
| Behavioral | Same | Same, with more product-sense questions ("how did you decide what to build?") |

Examples: Meta's **Front End Engineer** loop includes JavaScript-focused coding and a front-end system design round. Google
hires generalist SWEs and team-matches later, so the loop is mostly standard coding + system design. Product companies (Stripe, Airbnb,
Shopify) commonly use practical "build it" rounds. Confirm with your recruiter.

## Files

| File | Topics |
|---|---|
| [javascript-and-typescript.md](javascript-and-typescript.md) | Event loop, closures, `this`, promises/async, prototypes, modules, TypeScript type system |
| [react-and-frameworks.md](react-and-frameworks.md) | Rendering model, hooks rules, reconciliation and keys, memoization, state management, data fetching, Server Components/Next.js, Angular differences |
| [browser-performance-accessibility.md](browser-performance-accessibility.md) | Critical rendering path, Core Web Vitals (LCP, INP, CLS), loading strategies, caching, accessibility (WCAG, ARIA) |
| [frontend-system-design.md](frontend-system-design.md) | RADIO framework + 7 case studies (autocomplete, news feed, chat, data grid, collaborative editor, image gallery, e-commerce checkout) |
| [backend-and-apis.md](backend-and-apis.md) | REST design, status codes, idempotency, pagination, gRPC/GraphQL, auth (OAuth 2.0/OIDC, JWT, sessions), background jobs, concurrency in .NET and Python |
| [databases-and-sql.md](databases-and-sql.md) | SQL you must write fluently, indexes and query plans, isolation levels, N+1, migrations, SQL vs NoSQL |
| [web-security.md](web-security.md) | OWASP Top 10:2025, XSS, CSRF, injection, SSRF, CORS, CSP, cookies, secrets |
| [devops-and-cloud.md](devops-and-cloud.md) | CI/CD, containers, Kubernetes basics, deployment strategies, observability, 12-factor apps |
| [practical-coding.md](practical-coding.md) | **Tested** JavaScript implementations: debounce, throttle, `Promise.all`, retry with backoff, event emitter, deep clone, memoize, LRU, concurrency limiter, curry |

### Your stack, technology by technology (`stack/`)

Every technology on your resume, plus Node.js:

| File | Covers |
|---|---|
| [stack/nodejs.md](stack/nodejs.md) | Event loop phases, libuv thread pool, streams and backpressure, worker_threads vs cluster, Express/Fastify/NestJS, graceful shutdown, security |
| [stack/csharp-dotnet.md](stack/csharp-dotnet.md) | C# language, GC, async/await, LINQ, ASP.NET Core (middleware, DI lifetimes), **ASP.NET MVC**, **Entity Framework Core** |
| [stack/python.md](stack/python.md) | Language internals, GIL and asyncio, FastAPI + Pydantic, packaging, performance |
| [stack/html-css.md](stack/html-css.md) | Semantic HTML5, cascade and specificity, box model, Flexbox vs Grid, stacking contexts, responsive design, modern CSS |
| [stack/angular-redux-d3.md](stack/angular-redux-d3.md) | **Angular** (signals, OnPush, RxJS operators, forms), **Redux / Redux Toolkit**, **D3.js** (data joins, scales, D3 + React, SVG vs Canvas) |
| [stack/azure.md](stack/azure.md) | App Service, Functions + Durable Functions, Logic Apps, Service Bus vs Event Grid vs Event Hubs, **Cosmos DB**, Redis Cache, Key Vault, Blob, App Insights, Teams integrations |
| [stack/aws.md](stack/aws.md) | IAM, ECS (Fargate vs EC2), Lambda, API Gateway, RDS/Aurora, S3, CloudWatch, Azure ↔ AWS map |
| [stack/data-stores.md](stack/data-stores.md) | **SQL Server** specifics, **MongoDB**, **Redis** internals and patterns, choosing between them |
| [stack/docker-and-postman.md](stack/docker-and-postman.md) | Dockerfile best practices (multi-stage .NET example), compose, **Postman** collections/tests/Newman, API testing strategy |

Quiz yourself: `python tools/quiz.py --topic full-stack` (94 questions across all of the above; filter with `--tag nodejs`, `--tag dotnet`, `--tag azure`, `--tag aws`, `--tag redis`, …)

## Your angle

You've shipped full-stack enterprise apps (React/Angular + C#/.NET + Python/FastAPI on Azure) **and** production AI systems.
Position yourself as a **full-stack engineer who ships AI features end to end**: UI streaming, API design, data, evals, cost.
That combination is rarer than either half alone. Keep one or two stories ready where you owned the whole stack.

## Best external resources

- ★ [front-end-interview-handbook (GitHub, yangshun)](https://github.com/yangshun/front-end-interview-handbook) and [GreatFrontEnd](https://www.greatfrontend.com/): front-end questions and system design
- [top-javascript-interview-questions (GitHub)](https://github.com/greatfrontend/top-javascript-interview-questions) · [top-reactjs-interview-questions (GitHub)](https://github.com/greatfrontend/top-reactjs-interview-questions)
- [javascript-interview-questions (GitHub, sudheerj)](https://github.com/sudheerj/javascript-interview-questions) · [reactjs-interview-questions (GitHub, sudheerj)](https://github.com/sudheerj/reactjs-interview-questions)
- [You Don't Know JS (GitHub, getify)](https://github.com/getify/You-Dont-Know-JS): JavaScript deep dive
- [react.dev](https://react.dev/learn) (official docs) · [MDN Web Docs](https://developer.mozilla.org/) · [web.dev](https://web.dev/) (performance and Core Web Vitals)
- [developer-roadmap (GitHub)](https://github.com/kamranahmedse/developer-roadmap): frontend/backend/full-stack roadmaps
- [nodebestpractices (GitHub)](https://github.com/goldbergyoni/nodebestpractices)
- [OWASP Top 10](https://owasp.org/Top10/) · [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [Use The Index, Luke](https://use-the-index-luke.com/): SQL indexing, free
- [ASP.NET Core docs](https://learn.microsoft.com/aspnet/core/) · [FastAPI docs](https://fastapi.tiangolo.com/)
