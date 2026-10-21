// Tests every ```js block in 07-full-stack/practical-coding.md. Run: node --test tests/js/practical.test.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync, writeFileSync, mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..", "..");
const md = readFileSync(join(root, "07-full-stack", "practical-coding.md"), "utf8");
const code = [...md.matchAll(/```js\n([\s\S]*?)```/g)].map(m => m[1]).join("\n");
const file = join(mkdtempSync(join(tmpdir(), "practical-")), "practical.mjs");
writeFileSync(file, code);
const m = await import(pathToFileURL(file));
const sleep = ms => new Promise(r => setTimeout(r, ms));

test("debounce fires once with the latest args", async () => {
  const calls = []; const d = m.debounce(x => calls.push(x), 20);
  d(1); d(2); d(3); await sleep(40);
  assert.deepEqual(calls, [3]);
  d(4); d.cancel(); await sleep(40);
  assert.deepEqual(calls, [3]);
});

test("throttle runs immediately and once trailing", async () => {
  const calls = []; const t = m.throttle(x => calls.push(x), 30);
  t(1); t(2); t(3);
  assert.deepEqual(calls, [1]);
  await sleep(50);
  assert.deepEqual(calls, [1, 3]);
});

test("promiseAll keeps order, accepts values, rejects fast", async () => {
  assert.deepEqual(await m.promiseAll([sleep(20).then(() => "a"), "b", Promise.resolve("c")]), ["a", "b", "c"]);
  assert.deepEqual(await m.promiseAll([]), []);
  await assert.rejects(m.promiseAll([sleep(50), Promise.reject(new Error("x"))]), /x/);
  const settled = await m.promiseAllSettled([1, Promise.reject("no")]);
  assert.deepEqual(settled, [{ status: "fulfilled", value: 1 }, { status: "rejected", reason: "no" }]);
});

test("retry succeeds after failures and gives up after retries", async () => {
  let n = 0;
  const v = await m.retry(async () => { if (n++ < 2) throw new Error("fail"); return "ok"; }, { sleep: async () => {} });
  assert.equal(v, "ok"); assert.equal(n, 3);
  await assert.rejects(m.retry(async () => { throw new Error("always"); }, { retries: 2, sleep: async () => {} }), /always/);
});

test("mapWithConcurrency respects the limit and order", async () => {
  let active = 0, peak = 0;
  const out = await m.mapWithConcurrency([30, 10, 20, 5, 15], 2, async (ms, i) => {
    active++; peak = Math.max(peak, active); await sleep(ms); active--; return i;
  });
  assert.deepEqual(out, [0, 1, 2, 3, 4]); assert.equal(peak, 2);
});

test("EventEmitter on/once/off", () => {
  const e = new m.EventEmitter(); const got = [];
  const off = e.on("x", v => got.push(["on", v]));
  e.once("x", v => got.push(["once", v]));
  e.emit("x", 1); e.emit("x", 2); off(); assert.equal(e.emit("x", 3), false);
  assert.deepEqual(got, [["on", 1], ["once", 1], ["on", 2]]);
});

test("deepClone handles nesting, cycles, Date, Map, Set", () => {
  const src = { a: [1, { b: 2 }], d: new Date(0), m: new Map([["k", { v: 1 }]]), s: new Set([1]) };
  src.self = src;
  const c = m.deepClone(src);
  assert.notEqual(c, src); assert.equal(c.self, c);
  assert.deepEqual(c.a, src.a); assert.notEqual(c.a[1], src.a[1]);
  assert.equal(c.d.getTime(), 0); assert.notEqual(c.m.get("k"), src.m.get("k")); assert.ok(c.s.has(1));
});

test("memoize and curry", () => {
  let calls = 0; const sq = m.memoize(x => { calls++; return x * x; });
  sq(3); sq(3); assert.equal(calls, 1);
  const add3 = m.curry((a, b, c) => a + b + c);
  assert.equal(add3(1)(2)(3), 6); assert.equal(add3(1, 2)(3), 6); assert.equal(add3(1, 2, 3), 6);
});

test("LRUCache evicts least recently used", () => {
  const c = new m.LRUCache(2); c.put(1, 1); c.put(2, 2); c.get(1); c.put(3, 3);
  assert.equal(c.get(2), -1); assert.equal(c.get(1), 1); assert.equal(c.get(3), 3);
});

test("flatten and get", () => {
  assert.deepEqual(m.flatten([1, [2, [3, [4]]]]), [1, 2, 3, 4]);
  assert.deepEqual(m.flatten([1, [2, [3]]], 1), [1, 2, [3]]);
  const o = { a: { b: [{ c: 5 }] } };
  assert.equal(m.get(o, "a.b[0].c"), 5); assert.equal(m.get(o, "a.x.y", "def"), "def");
});
