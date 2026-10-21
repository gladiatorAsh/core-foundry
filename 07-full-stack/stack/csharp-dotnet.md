# C# and .NET (incl. ASP.NET Core, ASP.NET MVC, EF Core)

## Language fundamentals interviewers probe

- **Value vs reference types:** `struct`s are copied by value (stack or inline); `class`es are references to heap objects. **Boxing** wraps a value type in an object (allocation; avoid in hot paths).
- `record` / `record struct`: value-based equality, `with` expressions, good for DTOs and immutable data.
- **Nullable reference types** (`string?`): compile-time null-safety warnings. Enable them in every project.
- **Generics** with constraints (`where T : class, new()`); covariance (`IEnumerable<out T>`) and contravariance (`Action<in T>`).
- Delegates, `Func`/`Action`, lambdas, events (multicast delegates; unsubscribe to avoid leaks).
- Pattern matching (`switch` expressions, property and list patterns), `init`-only setters, primary constructors, `required` members.
- `Span<T>` / `Memory<T>`: slice arrays/strings without allocating (high-performance parsing).

## Memory and GC

- Generational GC: **gen 0** (new, collected often) → **gen 1** → **gen 2** (long-lived). The **Large Object Heap** holds objects ≥ 85,000 bytes (collected with gen 2; can fragment, so pool big buffers with `ArrayPool<T>`).
- Server GC (throughput, per-core heaps) vs workstation GC. `IDisposable` + `using` release **unmanaged** resources deterministically (connections, file handles); the GC handles memory.
- Common leaks: static collections, event handlers never unsubscribed, captured closures, timers.

## async/await

- The compiler turns an `async` method into a **state machine**; `await` returns the thread to the pool while I/O is pending. It's for scalability, not raw speed.
- **Never block on async code** (`.Result`, `.Wait()`): deadlock risk in contexts with a synchronization context, and thread-pool starvation in ASP.NET Core.
- Avoid `async void` except for event handlers (exceptions can't be caught). `ValueTask` for hot paths that often complete synchronously.
- `Task.WhenAll` for parallel I/O; `SemaphoreSlim` / `Parallel.ForEachAsync(…, new ParallelOptions { MaxDegreeOfParallelism = n })` to bound concurrency;
  `Channel<T>` for producer–consumer pipelines; pass `CancellationToken` through every layer.
- `ConfigureAwait(false)` in library code (not needed in ASP.NET Core app code, which has no synchronization context).

## LINQ

- **Deferred execution:** queries run when enumerated (`foreach`, `ToList()`). Enumerating twice runs twice. Materialize when needed.
- `IEnumerable<T>` (in-memory, LINQ to Objects, delegates) vs `IQueryable<T>` (expression trees translated by a provider such as EF Core to SQL).
  Calling `AsEnumerable()`/`ToList()` too early pulls the whole table into memory.

## ASP.NET Core

- **Middleware pipeline:** order matters (exception handling → HTTPS redirection → static files → routing → CORS → authentication → authorization → endpoints).
- **Dependency injection lifetimes:** singleton (one per app), **scoped** (one per request; e.g. `DbContext`), transient (new each time).
  **Captive dependency bug:** injecting a scoped service into a singleton keeps it alive forever (and shares it across requests).
- Minimal APIs vs controllers; model binding + validation (data annotations / FluentValidation); filters; `ProblemDetails` for errors.
- `IHttpClientFactory` (avoids socket exhaustion and stale DNS from `new HttpClient()` per call), Polly / `Microsoft.Extensions.Http.Resilience` for retries/circuit breakers.
- Configuration (`appsettings` + environment variables + Key Vault), `IOptions<T>`, logging with `ILogger`, health checks, OpenTelemetry.
- Background work: `IHostedService` / `BackgroundService`; use a queue for anything that must survive restarts.

## ASP.NET MVC (classic and Core)

- **Model** (data + business logic), **View** (Razor templates), **Controller** (handles the request, picks the view). Routing maps URLs to controller actions.
- Model binding, validation attributes, anti-forgery tokens (`[ValidateAntiForgeryToken]`) for CSRF, filters (authorization, action, exception), partial views and view components.
- Classic ASP.NET MVC (System.Web, .NET Framework, IIS) vs ASP.NET Core MVC (cross-platform, unified MVC + Web API, built-in DI). Migration story: strangler pattern, route by route.

## Entity Framework Core

- `DbContext` is a unit of work + identity map; **scoped per request**; not thread-safe.
- Change tracking vs `AsNoTracking()` for read-only queries (faster, less memory).
- **N+1:** lazy loading in loops. Use `Include`/`ThenInclude`, projection with `Select` to DTOs, or `AsSplitQuery()` to avoid cartesian explosion with multiple collections.
- Migrations (`dotnet ef migrations add`), applied in CI/CD or at startup with care; zero-downtime = expand/contract.
- Optimistic concurrency with a concurrency token (`rowversion` in SQL Server) → `DbUpdateConcurrencyException`.
- Raw SQL with `FromSql` (parameterized by interpolation). Compiled queries for hot paths. Log generated SQL in development.

## Testing

xUnit/NUnit, Moq/NSubstitute, `WebApplicationFactory` for integration tests of APIs, Testcontainers for real databases, FluentAssertions.

## Questions to rehearse

1. `IEnumerable` vs `IQueryable`? 2. What happens if you call `.Result` on a Task in ASP.NET? 3. DI lifetimes and the captive dependency problem.
4. `struct` vs `class` vs `record`. 5. How does the GC decide what to collect, and what is the LOH? 6. How would you find and fix an N+1 problem in EF Core?
7. Middleware order for auth. 8. `Task` vs `ValueTask`. 9. How do you make an API idempotent in ASP.NET Core? 10. `IHttpClientFactory`: why?
