# Arrays and strings: hashing, prefix sums, two pointers, sliding window

## Hashing

**Recognize:** "find a pair/complement", "count occurrences", "seen before?", "group by key".
O(n) time, O(n) space; trades memory for a pass.

```python
def two_sum(nums, target):
    seen = {}                      # value -> index
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i
    return []

from collections import defaultdict
def group_anagrams(words):
    groups = defaultdict(list)
    for w in words:
        groups[tuple(sorted(w))].append(w)   # or a 26-count tuple for O(k) keys
    return list(groups.values())
```

## Prefix sums

**Recognize:** "sum of subarray", "number of subarrays with sum K", range queries on a static array.
Key identity: `sum(i..j) = prefix[j+1] - prefix[i]`.

```python
def subarray_sum_equals_k(nums, k):
    count, running = 0, 0
    freq = {0: 1}                  # prefix sum 0 seen once (empty prefix)
    for x in nums:
        running += x
        count += freq.get(running - k, 0)
        freq[running] = freq.get(running, 0) + 1
    return count
```

Works with negatives, unlike a sliding window. Variants: running count of +1/−1 (balanced 0/1 subarrays),
prefix sums mod k (subarray divisible by k), 2-D prefix sums for matrix region sums.

## Two pointers

**Recognize:** sorted array, pairs/triplets, "in place", palindromes, merging.

```python
def three_sum(nums):
    nums.sort()
    res = []
    for i in range(len(nums) - 2):
        if i and nums[i] == nums[i - 1]:
            continue                       # skip duplicate anchors
        lo, hi = i + 1, len(nums) - 1
        while lo < hi:
            s = nums[i] + nums[lo] + nums[hi]
            if s < 0: lo += 1
            elif s > 0: hi -= 1
            else:
                res.append([nums[i], nums[lo], nums[hi]])
                lo += 1
                while lo < hi and nums[lo] == nums[lo - 1]:
                    lo += 1
    return res
```

Container With Most Water: move the pointer at the **shorter** wall, since the taller one can't improve the area.

## Sliding window

**Recognize:** contiguous subarray/substring + "longest/shortest/at most K/contains all".
Only valid when the window condition is **monotonic** (growing the window can only make it "more invalid").
That fails with negative numbers in sum problems; use prefix sums there instead.

```python
def longest_substring_at_most_k_distinct(s, k):
    count, left, best = {}, 0, 0
    for right, ch in enumerate(s):
        count[ch] = count.get(ch, 0) + 1
        while len(count) > k:              # shrink until valid
            count[s[left]] -= 1
            if count[s[left]] == 0:
                del count[s[left]]
            left += 1
        best = max(best, right - left + 1)
    return best

def min_window(s, t):                      # smallest window containing all of t
    from collections import Counter
    need, missing = Counter(t), len(t)
    left = start = 0; end = float("inf")
    for right, ch in enumerate(s):
        if need[ch] > 0: missing -= 1
        need[ch] -= 1
        while missing == 0:                # valid: try to shrink
            if right - left < end - start:
                start, end = left, right
            need[s[left]] += 1
            if need[s[left]] > 0: missing += 1
            left += 1
    return "" if end == float("inf") else s[start:end + 1]
```

**"Exactly K" trick:** `exactly(K) = atMost(K) - atMost(K-1)`.

## Pitfalls

- Sliding window with negative numbers: use prefix sums plus a hash map instead.
- Forgetting the `{0: 1}` seed in prefix-sum counting.
- Mutating a list while iterating; off-by-one in window length (`right - left + 1`).

## Practice

Two Sum · Group Anagrams · Top K Frequent Elements · Product of Array Except Self · Longest Consecutive Sequence ·
Subarray Sum Equals K · 3Sum · Container With Most Water · Trapping Rain Water · Longest Substring Without
Repeating Characters · Longest Repeating Character Replacement · Minimum Window Substring · Permutation in String
