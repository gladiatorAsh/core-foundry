# Graphs

**First, identify the graph:** grid cells, word ladders (words are nodes), dependencies (courses), states
(lock combinations). Then pick the algorithm:

| Need | Algorithm | Complexity |
|---|---|---|
| Connected components, flood fill | DFS/BFS or union-find | O(V + E) |
| Shortest path, unweighted | **BFS** | O(V + E) |
| Shortest path, non-negative weights | **Dijkstra** (heap) | O(E log V) |
| Negative weights / at most K edges | Bellman-Ford (K rounds) | O(K·E) |
| Ordering with dependencies, cycle detection in a DAG | **Topological sort** (Kahn) | O(V + E) |
| Dynamic connectivity, redundant edge, MST | **Union-find** (+ Kruskal) | ~O(α(n)) per op |
| All-pairs (small V) | Floyd–Warshall | O(V³) |

## BFS on a grid (multi-source)

```python
from collections import deque
def oranges_rotting(grid):
    rows, cols = len(grid), len(grid[0])
    q, fresh = deque(), 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2: q.append((r, c))
            elif grid[r][c] == 1: fresh += 1
    minutes = 0
    while q and fresh:
        for _ in range(len(q)):
            r, c = q.popleft()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2; fresh -= 1; q.append((nr, nc))
        minutes += 1
    return minutes if fresh == 0 else -1
```

Mark visited **when you enqueue**, not when you dequeue, or nodes get enqueued many times.

## DFS: components / islands

```python
def num_islands(grid):
    rows, cols = len(grid), len(grid[0])
    def sink(r, c):
        if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] != "1":
            return
        grid[r][c] = "0"
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            sink(r + dr, c + dc)
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1; sink(r, c)
    return count
```

Deep recursion on a 10^6-cell grid can overflow Python's stack; mention an iterative stack as the fix.

## Topological sort (Kahn's algorithm)

```python
from collections import deque, defaultdict
def find_order(n, prerequisites):
    graph, indeg = defaultdict(list), [0] * n
    for course, pre in prerequisites:
        graph[pre].append(course); indeg[course] += 1
    q = deque(i for i in range(n) if indeg[i] == 0)
    order = []
    while q:
        node = q.popleft(); order.append(node)
        for nxt in graph[node]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0: q.append(nxt)
    return order if len(order) == n else []    # shorter => cycle
```

Alien Dictionary = build edges from the first differing character of adjacent words, then topo sort.
Edge case: a word followed by its own prefix ("abc" before "ab") is invalid.

## Union-find

```python
class DSU:
    def __init__(self, n):
        self.parent, self.rank = list(range(n)), [0] * n
    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]   # path halving
            x = self.parent[x]
        return x
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb: return False
        if self.rank[ra] < self.rank[rb]: ra, rb = rb, ra
        self.parent[rb] = ra
        self.rank[ra] += self.rank[ra] == self.rank[rb]
        return True
```

## Dijkstra

```python
import heapq
def network_delay(times, n, k):
    graph = defaultdict(list)
    for u, v, w in times: graph[u].append((v, w))
    dist = {}
    heap = [(0, k)]
    while heap:
        d, u = heapq.heappop(heap)
        if u in dist: continue               # stale entry
        dist[u] = d
        for v, w in graph[u]:
            if v not in dist: heapq.heappush(heap, (d + w, v))
    return max(dist.values()) if len(dist) == n else -1
```

## Practice

Number of Islands · Max Area of Island · Clone Graph · Rotting Oranges · Pacific Atlantic Water Flow ·
Surrounded Regions · Course Schedule I & II · Graph Valid Tree · Number of Connected Components ·
Redundant Connection · Word Ladder · Network Delay Time · Cheapest Flights Within K Stops ·
Min Cost to Connect All Points · Alien Dictionary · Swim in Rising Water
