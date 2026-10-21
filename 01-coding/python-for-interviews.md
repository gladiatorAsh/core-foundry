# Python for interviews

## Standard library you should reach for without thinking

```python
from collections import Counter, defaultdict, deque, OrderedDict
from heapq import heappush, heappop, heapify, nlargest, nsmallest
from bisect import bisect_left, bisect_right, insort
from functools import cache, lru_cache, reduce
from itertools import accumulate, combinations, permutations, product, pairwise, groupby
import math   # math.inf, math.gcd, math.comb, math.isqrt
```

## Idioms

```python
counts = Counter(s); counts.most_common(k)
graph = defaultdict(list)
grid = [[0] * cols for _ in range(rows)]          # NOT [[0]*cols]*rows (aliased rows)
for i, (a, b) in enumerate(zip(xs, ys)): ...
sorted(items, key=lambda x: (-x.score, x.name))    # multi-key sort
prefix = [0, *accumulate(nums)]
heappush(h, (priority, counter, item))             # counter breaks ties; items never compared
divmod(17, 5)                                      # (3, 2)
-7 // 2 == -4                                      # floor division rounds DOWN (use int(-7/2) for truncation)
float("inf"), math.inf
s[::-1]                                            # reverse
"".join(chars)                                     # strings are immutable; build with a list
```

## Gotchas interviewers notice

- Mutable default arguments: `def f(x, acc=[])` reuses one list across calls.
- `list.pop(0)` and `x in list` are O(n).
- String concatenation in a loop is O(n²) worst case; use a list + `join`.
- Recursion limit is ~1000 by default; deep DFS needs `sys.setrecursionlimit` or an iterative version.
- `@cache` on a method caches `self` too (memory leak); prefer an inner function.
- `copy` vs `deepcopy` for nested lists; `path[:]` when appending a backtracking path.

## Type hints and dataclasses (looks senior, costs nothing)

```python
from dataclasses import dataclass, field

@dataclass(order=True)
class Job:
    priority: int
    name: str = field(compare=False)

def schedule(jobs: list[Job]) -> list[str]: ...
```
