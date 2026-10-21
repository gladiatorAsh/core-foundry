# Node.js

## Runtime model

- **V8** runs JavaScript; **libuv** provides the event loop and a **thread pool** (default 4 threads, set by `UV_THREADPOOL_SIZE`) used for
  file system operations, `dns.lookup`, some `crypto` (pbkdf2, scrypt), and `zlib`. Network I/O uses the OS's non-blocking APIs (epoll/kqueue/IOCP), not the pool.
- One main thread runs your JavaScript, so **CPU-heavy code blocks every request**. Offload it to `worker_threads`, a job queue, or another service.

## Event loop phases

`timers` (setTimeout/setInterval) → `pending callbacks` → `poll` (I/O; waits here when idle) → `check` (`setImmediate`) → `close callbacks`.
Between every callback: **`process.nextTick` queue**, then the **promise microtask queue**.

```js
setTimeout(() => console.log("timeout"), 0);
setImmediate(() => console.log("immediate"));
Promise.resolve().then(() => console.log("promise"));
process.nextTick(() => console.log("nextTick"));
// nextTick, promise, then timeout/immediate (order of those two is not guaranteed from the main module;
// inside an I/O callback, setImmediate always runs first)
```

Recursive `process.nextTick` can starve I/O, so prefer `setImmediate` to yield.

## Scaling across cores

- **cluster** module / PM2: multiple processes sharing a port (one event loop each). In containers, prefer one process per container and scale replicas.
- **worker_threads**: threads with their own V8 isolate for CPU work; share memory via `SharedArrayBuffer`; communicate with `postMessage`.

## Streams and backpressure

Readable, Writable, Duplex, Transform. Process large data without loading it all into memory. **Backpressure:** when `write()` returns `false`, stop until `'drain'`.
Use `stream.pipeline()` (or `await pipeline(...)` from `node:stream/promises`), which handles errors and cleanup; `.pipe()` doesn't propagate errors.

```js
import { pipeline } from "node:stream/promises";
import { createReadStream, createWriteStream } from "node:fs";
import { createGzip } from "node:zlib";
await pipeline(createReadStream("big.log"), createGzip(), createWriteStream("big.log.gz"));
```

## Frameworks

- **Express:** minimal; middleware chain `(req, res, next)`; error middleware has **4 arguments** `(err, req, res, next)` and is registered last.
  Express 5 forwards rejected promises from async handlers to error middleware.
- **Fastify:** faster, schema-based validation/serialization, plugin encapsulation.
- **NestJS:** opinionated, Angular-like (modules, DI, decorators), good for large teams.

## Error handling and reliability

- Operational errors (bad input, timeouts) → handle and respond. Programmer errors (bugs) → log and restart the process (let the orchestrator replace it).
- `process.on('unhandledRejection')` / `uncaughtException`: log and exit; don't keep running in an unknown state.
- **Graceful shutdown:** on SIGTERM stop accepting connections, finish in-flight requests, close DB pools, then exit (with a timeout).
- Timeouts on every outbound call (`AbortSignal.timeout(ms)` with `fetch`, which is built in since Node 18).

## Performance and debugging

`--inspect` + Chrome DevTools, `clinic.js` / flame graphs, `--cpu-prof`, heap snapshots for leaks (look for growing arrays/maps, listeners, closures).
Avoid synchronous APIs (`fs.readFileSync`) on request paths; avoid big `JSON.parse` on the main thread; cache; use connection pooling (`undici` agent, DB pools).

## Security

`helmet` for headers, input validation (zod / ajv), rate limiting, parameterized queries, `npm audit` / Dependabot, lockfiles committed,
avoid `eval`/`child_process` with user input, watch for prototype pollution (`__proto__` keys in merged JSON).

## Modules and packaging

ESM (`"type": "module"`, `import`) vs CommonJS (`require`). `package-lock.json` pins the full tree; `npm ci` in CI. Semver: `^1.2.3` allows minor/patch updates.
Node LTS releases are even-numbered; use an active LTS in production.

## Node vs .NET vs Python (be ready for "which would you pick?")

| | Node.js | ASP.NET Core | Python (FastAPI) |
|---|---|---|---|
| Strength | I/O-heavy APIs, real-time (WebSockets), shared language with the frontend | High throughput, strong typing, mature enterprise tooling, multithreaded | ML/AI ecosystem, fast iteration, data work |
| Concurrency | Single-threaded event loop + workers | Thread pool + async/await, true parallelism | asyncio event loop; GIL limits CPU threads |
| Watch out | CPU-bound work blocks everything | Heavier ceremony for tiny services | CPU-bound work needs processes; typing is optional |
