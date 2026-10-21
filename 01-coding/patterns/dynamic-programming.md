# Dynamic programming

**Recognize:** "number of ways", "min/max cost", "is it possible", and choices at each step whose
subproblems overlap. If brute force is recursion that recomputes the same arguments, it's DP.

## The 4-step recipe (say it out loud)

1. **State:** what does `dp[i]` (or `dp[i][j]`) mean, in words?
2. **Transition:** how does a state come from smaller states?
3. **Base cases.**
4. **Order + answer:** iteration order and which cell is the answer. Then optimize space.

Start top-down (`@cache`) if it's faster to get right, then convert to bottom-up if asked.

## 1-D

```python
from functools import cache
def climb_stairs(n):
    a, b = 1, 1
    for _ in range(n - 1): a, b = b, a + b
    return b

def rob(nums):                           # House Robber
    take, skip = 0, 0
    for x in nums: take, skip = skip + x, max(take, skip)
    return max(take, skip)

def coin_change(coins, amount):          # min coins (unbounded knapsack)
    INF = amount + 1
    dp = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a: dp[a] = min(dp[a], dp[a - c] + 1)
    return dp[amount] if dp[amount] != INF else -1

def word_break(s, words):
    words, n = set(words), len(s)
    dp = [True] + [False] * n            # dp[i]: s[:i] breakable
    for i in range(1, n + 1):
        dp[i] = any(dp[j] and s[j:i] in words for j in range(i))
    return dp[n]
```

**Longest Increasing Subsequence:** O(n log n) with patience sorting: keep `tails[k]` = the smallest tail of
an increasing subsequence of length k+1; `bisect_left` each element in.

## 2-D

```python
def lcs(a, b):                           # Longest Common Subsequence
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            dp[i][j] = dp[i-1][j-1] + 1 if a[i-1] == b[j-1] else max(dp[i-1][j], dp[i][j-1])
    return dp[-1][-1]

def edit_distance(a, b):
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1): dp[i][0] = i
    for j in range(n + 1): dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i-1] == b[j-1]: dp[i][j] = dp[i-1][j-1]
            else: dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])  # delete, insert, replace
    return dp[m][n]
```

## 0/1 knapsack (Partition Equal Subset Sum, Target Sum)

Iterate capacity **backwards** so each item is used at most once:

```python
def can_partition(nums):
    total = sum(nums)
    if total % 2: return False
    target = total // 2
    dp = [True] + [False] * target
    for x in nums:
        for s in range(target, x - 1, -1):
            dp[s] = dp[s] or dp[s - x]
    return dp[target]
```

Unbounded (coin change) iterates **forwards**.

## Other families

- **Intervals DP** (`dp[l][r]`): Burst Balloons, Longest Palindromic Subsequence. Iterate by length.
- **State machine:** stock problems with cooldown/fee have states held / sold / rest.
- **Bitmask DP:** traveling salesman for n ≤ 20: `dp[mask][last]`.
- **Palindromes:** expand around the center (2n−1 centers) is O(n²) with O(1) space.

## Practice

Climbing Stairs · Min Cost Climbing Stairs · House Robber I & II · Longest Palindromic Substring ·
Palindromic Substrings · Decode Ways · Coin Change · Maximum Product Subarray · Word Break ·
Longest Increasing Subsequence · Partition Equal Subset Sum · Unique Paths · Longest Common Subsequence ·
Best Time to Buy and Sell Stock with Cooldown · Coin Change II · Target Sum · Interleaving String ·
Edit Distance · Burst Balloons · Regular Expression Matching
