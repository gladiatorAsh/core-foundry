# Design-a-data-structure problems

These show up a lot in AI-assisted and "practical" rounds because they extend naturally (add TTL, add
concurrency, add persistence). Know these cold.

## LRU cache: O(1) get/put

`OrderedDict` is acceptable in most interviews. Be ready to build it with a hash map + doubly linked list.

```python
class Node:
    __slots__ = ("key", "val", "prev", "next")
    def __init__(self, key=0, val=0):
        self.key, self.val, self.prev, self.next = key, val, None, None

class LRUCache:
    def __init__(self, capacity):
        self.cap, self.map = capacity, {}
        self.head, self.tail = Node(), Node()          # sentinels
        self.head.next, self.tail.prev = self.tail, self.head
    def _remove(self, n):
        n.prev.next, n.next.prev = n.next, n.prev
    def _add_front(self, n):
        n.prev, n.next = self.head, self.head.next
        self.head.next.prev = n
        self.head.next = n
    def get(self, key):
        if key not in self.map: return -1
        n = self.map[key]; self._remove(n); self._add_front(n)
        return n.val
    def put(self, key, val):
        if key in self.map: self._remove(self.map[key])
        n = self.map[key] = Node(key, val); self._add_front(n)
        if len(self.map) > self.cap:
            lru = self.tail.prev; self._remove(lru); del self.map[lru.key]
```

**Follow-ups to expect:** thread safety (one lock; or striped locks by key hash), TTL (store an expiry and
check lazily on get, plus a periodic sweep or a min-heap of expiries), distributed LRU (consistent
hashing across nodes; each node runs its own LRU).

## LFU cache: O(1)

`key -> (val, freq)`, `freq -> OrderedDict of keys`, plus `min_freq`. On access, move the key to `freq+1`;
if the old bucket empties and it was `min_freq`, increment `min_freq`. On insert, `min_freq = 1`.

## Rate limiters

```python
import time
from collections import deque

class SlidingWindowLog:                  # exact, O(requests) memory
    def __init__(self, limit, window_s):
        self.limit, self.window, self.log = limit, window_s, deque()
    def allow(self, now=None):
        now = time.monotonic() if now is None else now
        while self.log and self.log[0] <= now - self.window:
            self.log.popleft()
        if len(self.log) < self.limit:
            self.log.append(now); return True
        return False

class TokenBucket:                       # allows bursts up to capacity, O(1) memory
    def __init__(self, rate_per_s, capacity):
        self.rate, self.cap = rate_per_s, capacity
        self.tokens, self.last = capacity, time.monotonic()
    def allow(self, cost=1):
        now = time.monotonic()
        self.tokens = min(self.cap, self.tokens + (now - self.last) * self.rate)
        self.last = now
        if self.tokens >= cost:
            self.tokens -= cost; return True
        return False
```

Distributed version: Redis with an atomic Lua script (or `INCR` + `EXPIRE` for a fixed window) keyed by user/API key.

## In-memory key-value store with TTL and transactions (classic progressive problem)

- v1: `set/get/delete` with a dict.
- v2: TTL. Store `(value, expires_at)`, check on read, and sweep with a heap.
- v3: `begin/commit/rollback`, nested. Keep a stack of change logs (old values, or a tombstone for
  "didn't exist"); rollback restores from the top log; commit merges the top log into the one below.
- v4: snapshots/persistence. Append-only log + periodic snapshot; replay the log on start.

## Others worth knowing

Min Stack (track the min with each push) · Time Based Key-Value Store (per-key list + binary search) ·
Design Hit Counter (circular buffer of 300 buckets) · Snapshot Array (per-index list of (snap_id, val)) ·
Design Twitter (merge k feeds with a heap) · Insert Delete GetRandom O(1) (array + index map; swap with last on delete).
