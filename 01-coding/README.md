# Coding

## How to practice (for Staff loops)

1. **Learn the patterns, not the problems.** About 15 patterns cover nearly every interview question. Each
   pattern file has: how to recognize it, a Python template, pitfalls, and practice problems.
2. **Timebox:** 25 min per medium, 40 per hard. If stuck at 15 min, read the approach (not the code), then
   implement it from memory the next day.
3. **Practice the Google format:** at least once a week, solve in a plain text editor with **no running
   and no autocomplete**, then dry-run by hand with a small example.
4. **Practice the Meta format:** two mediums in 40 minutes, clean code, no hints.
5. **Practice the AI-assisted format** too: see [../00-strategy/ai-assisted-coding.md](../00-strategy/ai-assisted-coding.md).
6. **Spaced repetition:** re-solve each problem you missed after 3 days, 7 days, and 21 days. The quiz
   tool covers pattern recognition: `python tools/quiz.py --topic coding`.

## The interview script (say these out loud)

1. Restate the problem; ask about input size, value ranges, duplicates, empty input, and sortedness.
2. Give a brute-force approach and its complexity in one sentence.
3. Name the pattern and the better complexity. Get a nod before coding.
4. Write clean code: helper functions, clear names, no clever one-liners.
5. Dry-run with a small example **by hand**, then edge cases (empty, one element, all duplicates, negatives).
6. State final time and space complexity. Mention a follow-up (streaming input, distributed, very large data).

## Pattern index

| # | Pattern | File |
|---|---|---|
| 1 | Hashing, prefix sums, two pointers, sliding window | [patterns/arrays-and-strings.md](patterns/arrays-and-strings.md) |
| 2 | Binary search (incl. on the answer) | [patterns/binary-search.md](patterns/binary-search.md) |
| 3 | Stacks, monotonic stack/queue, linked lists | [patterns/stacks-queues-linked-lists.md](patterns/stacks-queues-linked-lists.md) |
| 4 | Trees, BST, tries | [patterns/trees-and-tries.md](patterns/trees-and-tries.md) |
| 5 | Graphs: BFS, DFS, topological sort, union-find, Dijkstra | [patterns/graphs.md](patterns/graphs.md) |
| 6 | Heaps, top-K, intervals, greedy | [patterns/heaps-intervals-greedy.md](patterns/heaps-intervals-greedy.md) |
| 7 | Backtracking | [patterns/backtracking.md](patterns/backtracking.md) |
| 8 | Dynamic programming | [patterns/dynamic-programming.md](patterns/dynamic-programming.md) |
| 9 | Design-a-data-structure (LRU, LFU, rate limiter, KV store) | [patterns/design-data-structures.md](patterns/design-data-structures.md) |

Also: [complexity-cheatsheet.md](complexity-cheatsheet.md) · [python-for-interviews.md](python-for-interviews.md) · [problem-list.md](problem-list.md)

## Best external lists

- [NeetCode 150](https://neetcode.io/practice) (with video explanations), the default list
- [Grind 75](https://www.techinterviewhandbook.org/grind75) (adjustable weekly plan)
- [Tech Interview Handbook: algorithms](https://www.techinterviewhandbook.org/algorithms/study-cheatsheet/)
- [LeetCode company tags](https://leetcode.com/problemset/) (Premium) for the last ~6 months at your target company
