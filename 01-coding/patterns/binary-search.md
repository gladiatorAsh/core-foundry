# Binary search

**Recognize:** sorted input, "minimum/maximum value such that ...", rotated arrays, very large search
spaces (10^9), O(log n) required.

## One template to rule them all: find the first index where `ok(i)` is true

```python
def first_true(lo, hi, ok):
    """Smallest x in [lo, hi] with ok(x) True; returns hi + 1 if none. ok must be monotonic F..F T..T."""
    while lo <= hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid - 1
        else:
            lo = mid + 1
    return lo
```

- Lower bound (first `>= target`): `first_true(0, n-1, lambda i: a[i] >= target)`
- Upper bound (first `> target`): `first_true(0, n-1, lambda i: a[i] > target)`
- Python has these built in: `bisect_left`, `bisect_right`.

## Binary search on the answer

When the answer is a number and "can we do it with X?" is monotonic.

```python
import math
def min_eating_speed(piles, h):            # Koko Eating Bananas
    def ok(speed):
        return sum(math.ceil(p / speed) for p in piles) <= h
    return first_true(1, max(piles), ok)
```

Same shape: Capacity To Ship Packages, Split Array Largest Sum, Minimize Max Distance, Magnetic Force.

## Rotated sorted array

At each step one half is sorted; check whether the target lies in the sorted half.

```python
def search_rotated(a, target):
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == target:
            return mid
        if a[lo] <= a[mid]:                 # left half sorted
            if a[lo] <= target < a[mid]: hi = mid - 1
            else: lo = mid + 1
        else:                               # right half sorted
            if a[mid] < target <= a[hi]: lo = mid + 1
            else: hi = mid - 1
    return -1
```

## Pitfalls

- Infinite loops from `lo = mid` with `while lo < hi`. Stick to one template.
- A predicate that isn't actually monotonic.
- Median of Two Sorted Arrays: binary search on the **partition** of the shorter array, O(log min(m, n)).

## Practice

Binary Search · Search a 2D Matrix · Koko Eating Bananas · Find Minimum in Rotated Sorted Array ·
Search in Rotated Sorted Array · Time Based Key-Value Store · Median of Two Sorted Arrays · Split Array Largest Sum
