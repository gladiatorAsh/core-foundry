# Practical coding (JavaScript)

Front-end and full-stack loops often ask you to implement utilities from scratch. Every block below is tested in CI
(`node --test tests/js/practical.test.mjs`). Practice writing each one from memory in under 10 minutes, then talk through edge cases.

## debounce and throttle

```js
export function debounce(fn, wait) {
  let timer;
  function debounced(...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), wait);   // keep `this` and the latest args
  }
  debounced.cancel = () => clearTimeout(timer);
  return debounced;
}

export function throttle(fn, wait) {
  let last = 0, timer = null, pendingArgs = null;
  return function throttled(...args) {
    const now = Date.now();
    const remaining = wait - (now - last);
    if (remaining <= 0) {
      last = now;
      fn.apply(this, args);
    } else {
      pendingArgs = args;                                    // trailing call with the latest args
      if (!timer) {
        timer = setTimeout(() => {
          last = Date.now(); timer = null;
          fn.apply(this, pendingArgs);
        }, remaining);
      }
    }
  };
}
```

Debounce = run once activity stops (search input). Throttle = run at most once per interval (scroll, resize).

## Promise.all and Promise.allSettled

```js
export function promiseAll(items) {
  return new Promise((resolve, reject) => {
    const results = new Array(items.length);
    let remaining = items.length;
    if (remaining === 0) return resolve(results);
    items.forEach((item, i) => {
      Promise.resolve(item).then(value => {               // accept non-promise values too
        results[i] = value;                                // keep input order, not completion order
        if (--remaining === 0) resolve(results);
      }, reject);                                          // first rejection wins
    });
  });
}

export function promiseAllSettled(items) {
  return promiseAll(items.map(item =>
    Promise.resolve(item).then(
      value => ({ status: "fulfilled", value }),
      reason => ({ status: "rejected", reason }))));
}
```

## Retry with exponential backoff and jitter

```js
export async function retry(fn, { retries = 3, baseMs = 100, maxMs = 2000, sleep = ms => new Promise(r => setTimeout(r, ms)) } = {}) {
  for (let attempt = 0; ; attempt++) {
    try {
      return await fn(attempt);
    } catch (err) {
      if (attempt >= retries) throw err;
      const backoff = Math.min(maxMs, baseMs * 2 ** attempt);
      await sleep(Math.random() * backoff);               // "full jitter" avoids synchronized retries
    }
  }
}
```

## Concurrency limiter (run at most N async tasks at once)

```js
export async function mapWithConcurrency(items, limit, worker) {
  const results = new Array(items.length);
  let next = 0;
  async function lane() {
    while (next < items.length) {
      const i = next++;                                    // safe: JS is single-threaded between awaits
      results[i] = await worker(items[i], i);
    }
  }
  await Promise.all(Array.from({ length: Math.min(limit, items.length) }, lane));
  return results;
}
```

Use it for calling a rate-limited API (or an LLM endpoint) over many inputs.

## Event emitter

```js
export class EventEmitter {
  #listeners = new Map();
  on(event, fn) {
    if (!this.#listeners.has(event)) this.#listeners.set(event, new Set());
    this.#listeners.get(event).add(fn);
    return () => this.off(event, fn);                      // return an unsubscribe function
  }
  once(event, fn) {
    const off = this.on(event, (...args) => { off(); fn(...args); });
    return off;
  }
  off(event, fn) { this.#listeners.get(event)?.delete(fn); }
  emit(event, ...args) {
    for (const fn of [...(this.#listeners.get(event) ?? [])]) fn(...args);   // copy: listeners may unsubscribe
    return this.#listeners.get(event)?.size > 0;
  }
}
```

## Deep clone (handles cycles, Dates, Maps, Sets)

```js
export function deepClone(value, seen = new WeakMap()) {
  if (value === null || typeof value !== "object") return value;
  if (seen.has(value)) return seen.get(value);
  if (value instanceof Date) return new Date(value);
  if (value instanceof RegExp) return new RegExp(value.source, value.flags);
  if (value instanceof Map) {
    const out = new Map(); seen.set(value, out);
    value.forEach((v, k) => out.set(deepClone(k, seen), deepClone(v, seen)));
    return out;
  }
  if (value instanceof Set) {
    const out = new Set(); seen.set(value, out);
    value.forEach(v => out.add(deepClone(v, seen)));
    return out;
  }
  const out = Array.isArray(value) ? [] : Object.create(Object.getPrototypeOf(value));
  seen.set(value, out);
  for (const key of Reflect.ownKeys(value)) out[key] = deepClone(value[key], seen);
  return out;
}
```

Mention `structuredClone()` (built in since 2022) as what you'd use in production.

## Memoize and curry

```js
export function memoize(fn, keyFn = (...args) => JSON.stringify(args)) {
  const cache = new Map();
  return function (...args) {
    const key = keyFn(...args);
    if (!cache.has(key)) cache.set(key, fn.apply(this, args));
    return cache.get(key);
  };
}

export function curry(fn) {
  return function curried(...args) {
    return args.length >= fn.length ? fn.apply(this, args) : (...more) => curried.apply(this, [...args, ...more]);
  };
}
```

## LRU cache in JavaScript (Map keeps insertion order)

```js
export class LRUCache {
  constructor(capacity) { this.capacity = capacity; this.map = new Map(); }
  get(key) {
    if (!this.map.has(key)) return -1;
    const value = this.map.get(key);
    this.map.delete(key); this.map.set(key, value);          // move to most-recent
    return value;
  }
  put(key, value) {
    this.map.delete(key);
    this.map.set(key, value);
    if (this.map.size > this.capacity) this.map.delete(this.map.keys().next().value);   // evict oldest
  }
}
```

## Flatten and get-by-path

```js
export function flatten(arr, depth = Infinity) {
  return depth > 0
    ? arr.reduce((acc, x) => acc.concat(Array.isArray(x) ? flatten(x, depth - 1) : [x]), [])
    : arr.slice();
}

export function get(obj, path, fallback) {
  const keys = Array.isArray(path) ? path : path.replace(/\[(\w+)\]/g, ".$1").split(".").filter(Boolean);
  let cur = obj;
  for (const k of keys) {
    if (cur == null) return fallback;
    cur = cur[k];
  }
  return cur === undefined ? fallback : cur;
}
```

## UI tasks to practice (no code here; build them in a sandbox)

Autocomplete with debounce + keyboard navigation + ARIA · infinite scroll with `IntersectionObserver` · modal with focus trap ·
tabs/accordion with full keyboard support · star rating · drag-and-drop list · data table with sort/filter/pagination ·
a progress bar driven by a queue of tasks · a todo app with optimistic updates and undo · a streaming chat UI over SSE.
