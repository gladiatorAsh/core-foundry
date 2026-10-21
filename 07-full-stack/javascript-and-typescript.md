# JavaScript and TypeScript

## The event loop (explain it with this example)

```js
console.log("1");
setTimeout(() => console.log("2"), 0);
Promise.resolve().then(() => console.log("3"));
queueMicrotask(() => console.log("4"));
console.log("5");
// Output: 1 5 3 4 2
```

- JavaScript runs one **call stack** per thread. Synchronous code runs to completion first.
- **Microtasks** (promise callbacks, `queueMicrotask`, `MutationObserver`) run right after the current task, **all of them**, before the next task.
- **Macrotasks** (timers, I/O, UI events, `MessageChannel`) run one per loop turn.
- The browser may **render between tasks** (after microtasks drain), so a long synchronous task or an endless microtask chain blocks rendering and input (hurting INP).
- `await x` = "pause here; resume in a microtask when x settles".
- Node.js adds phases (timers → pending callbacks → poll (I/O) → check (`setImmediate`) → close) plus `process.nextTick`, which runs before promise microtasks.

## Scope, closures, hoisting

- `var` is function-scoped and hoisted (initialized as `undefined`); `let`/`const` are block-scoped and in the **temporal dead zone** until declared.
- A **closure** is a function plus the variables it captured from its enclosing scope. It powers data privacy, factories, memoization, and debounce.
- The classic bug: `for (var i = 0; i < 3; i++) setTimeout(() => console.log(i))` prints `3 3 3`; with `let` it prints `0 1 2` (a new binding per iteration).

## `this`

Determined by **how a function is called**: a method call `obj.f()` → `obj`; a plain call `f()` → `undefined` in strict mode
(the global object in sloppy mode); `new F()` → the new object; `f.call/apply/bind(x)` → `x`. **Arrow functions don't have their own `this`**;
they capture it lexically (which is why they're used for callbacks inside classes).

## Prototypes and classes

Objects delegate property lookups along the **prototype chain**. `class` is syntax over prototypes. `Object.create(proto)`
makes an object with a given prototype. `instanceof` walks the chain.

## Equality and types

`===` (no coercion; always use it) vs `==` (coerces: `0 == ""` is true). `NaN !== NaN` (use `Number.isNaN`). `typeof null === "object"`
(historic bug). Objects compare by reference. `Object.is(-0, 0)` is false.

## Promises and async

- `Promise.all` (fail fast, all must resolve) · `Promise.allSettled` (wait for all, never rejects) · `Promise.race` (first to settle) ·
  `Promise.any` (first to **fulfill**; rejects with `AggregateError` only if all reject).
- Run independent awaits in parallel: `const [a, b] = await Promise.all([fa(), fb()])` instead of awaiting sequentially.
- Unhandled rejections crash Node processes by default. Always `catch`.
- Cancellation: `AbortController` + `signal` for `fetch` and your own async functions.
- Implementations of these are in [practical-coding.md](practical-coding.md).

## Modules

ES modules (`import`/`export`, static, tree-shakeable, async loading) vs CommonJS (`require`, dynamic, synchronous; legacy Node).
Dynamic `import()` enables code splitting.

## Memory leaks to name

Forgotten timers/intervals, event listeners not removed, closures holding large objects, detached DOM nodes still referenced,
unbounded caches (use `WeakMap`/`WeakRef` where appropriate).

## TypeScript essentials

```ts
type Result<T, E = Error> = { ok: true; value: T } | { ok: false; error: E };   // discriminated union

function handle(r: Result<number>) {
  if (r.ok) return r.value * 2;         // narrowed to { ok: true; value: number }
  throw r.error;
}

type Partialize<T> = { [K in keyof T]?: T[K] };                         // mapped type (built in as Partial<T>)
type ElementOf<T> = T extends readonly (infer U)[] ? U : never;         // conditional type + infer
type Handler = Parameters<typeof handle>[0];                            // utility types
const config = { retries: 3, mode: "fast" } as const satisfies Record<string, unknown>;
```

- Structural typing: compatibility by shape, not by name.
- `unknown` (must narrow before use) vs `any` (opts out of checking). Prefer `unknown` at boundaries.
- `interface` (extendable, declaration merging) vs `type` (unions, mapped/conditional types). Both are fine for object shapes.
- Generics with constraints: `function pluck<T, K extends keyof T>(obj: T, key: K): T[K]`.
- Types are erased at runtime, so validate external data (e.g. with zod) at the boundary.
- `strict: true` always; `noUncheckedIndexedAccess` catches undefined array/map access.
