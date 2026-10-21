# Complexity cheat sheet

## Input size → what's feasible (≈10^8 simple ops/sec in C++; Python is ~10–50× slower)

| n | Acceptable complexity | Typical approach |
|---|---|---|
| ≤ 12 | O(n!) | permutations, brute force |
| ≤ 20–25 | O(2^n), O(n·2^n) | subsets, bitmask DP |
| ≤ 500 | O(n³) | 3 nested loops, Floyd–Warshall, interval DP |
| ≤ 5,000 | O(n²) | 2-D DP, all pairs |
| ≤ 10^6 | O(n log n) | sorting, heap, binary search |
| ≤ 10^8 | O(n) | single pass, hashing, two pointers |
| > 10^9 | O(log n) or O(1) | binary search on the answer, math |

## Data structure operations

| Structure | Access | Search | Insert | Delete | Notes |
|---|---|---|---|---|---|
| Python list | O(1) | O(n) | O(1) amortized append; O(n) middle | O(n) (O(1) pop at end) | `pop(0)` is O(n): use `deque` |
| dict / set | – | O(1) avg | O(1) avg | O(1) avg | worst case O(n) |
| deque | O(1) ends | O(n) | O(1) ends | O(1) ends | index into middle is O(n) |
| heapq | O(1) min | O(n) | O(log n) | O(log n) pop | `heapify` is O(n) |
| Balanced BST (`sortedcontainers.SortedList`) | O(log n) | O(log n) | O(log n) | O(log n) | not in stdlib; ask before using |
| Trie | – | O(L) | O(L) | O(L) | L = word length |
| Union-find | – | ~O(α(n)) | – | – | path compression + union by rank |

## Sorting

| Algorithm | Best | Average | Worst | Space | Stable |
|---|---|---|---|---|---|
| Timsort (Python `sorted`) | O(n) | O(n log n) | O(n log n) | O(n) | yes |
| Quicksort | O(n log n) | O(n log n) | O(n²) | O(log n) | no |
| Mergesort | O(n log n) | O(n log n) | O(n log n) | O(n) | yes |
| Heapsort | O(n log n) | O(n log n) | O(n log n) | O(1) | no |
| Counting/radix | O(n + k) | O(n + k) | O(n + k) | O(n + k) | yes |
| Quickselect (k-th) | O(n) | O(n) | O(n²) | O(1) | – |

## Graph algorithms

BFS/DFS O(V+E) · Dijkstra (binary heap) O((V+E) log V) · Bellman-Ford O(V·E) · Floyd–Warshall O(V³) ·
Topological sort O(V+E) · Kruskal O(E log E) · Prim (heap) O(E log V)

## Recursion

Master theorem shortcuts: T(n)=2T(n/2)+O(n) → O(n log n) (merge sort) · T(n)=T(n/2)+O(1) → O(log n) ·
T(n)=2T(n/2)+O(1) → O(n) (tree traversal). Recursion space = max depth (O(h) for trees; O(n) if skewed).
