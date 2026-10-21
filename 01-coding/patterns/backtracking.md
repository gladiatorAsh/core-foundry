# Backtracking

**Recognize:** "all combinations / permutations / subsets", "place N queens", word search, constraint
satisfaction. Output is exponential, so say so up front ("there are 2^n subsets, so this is inherently exponential").

## The template

```python
def backtrack(path, choices):
    if is_solution(path):
        result.append(path[:])       # copy!
        return
    for choice in choices:
        if not valid(choice): continue
        path.append(choice)          # choose
        backtrack(path, next_choices)
        path.pop()                   # un-choose
```

## The three classics

```python
def subsets(nums):
    res = []
    def go(i, path):
        res.append(path[:])
        for j in range(i, len(nums)):
            path.append(nums[j]); go(j + 1, path); path.pop()
    go(0, []); return res

def combination_sum(candidates, target):     # reuse allowed
    res = []
    def go(i, path, remaining):
        if remaining == 0: res.append(path[:]); return
        for j in range(i, len(candidates)):
            if candidates[j] > remaining: continue
            path.append(candidates[j]); go(j, path, remaining - candidates[j]); path.pop()
    go(0, [], target); return res

def permutations(nums):
    res, used = [], [False] * len(nums)
    def go(path):
        if len(path) == len(nums): res.append(path[:]); return
        for i, x in enumerate(nums):
            if used[i]: continue
            used[i] = True; path.append(x); go(path); path.pop(); used[i] = False
    go([]); return res
```

**Duplicates in the input** (Subsets II, Combination Sum II): sort first, then `if j > i and nums[j] == nums[j-1]: continue`.

## Complexity cheat sheet

| Problem | Time |
|---|---|
| Subsets | O(n · 2^n) |
| Permutations | O(n · n!) |
| Combinations C(n, k) | O(k · C(n, k)) |
| N-Queens | O(n!) with pruning |
| Word Search | O(rows · cols · 3^L) |

## Practice

Subsets I & II · Combination Sum I & II · Permutations · Word Search · Palindrome Partitioning ·
Letter Combinations of a Phone Number · N-Queens · Generate Parentheses
