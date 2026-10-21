# Heaps, top-K, intervals, greedy

## Heaps

Python's `heapq` is a **min-heap**. For a max-heap, push negated values. Push tuples `(priority, tiebreak, item)`
so items never get compared directly.

**Top K largest:** keep a min-heap of size K. O(n log k). (Quickselect is O(n) average.)

```python
import heapq
def top_k_frequent(nums, k):
    from collections import Counter
    return [x for x, _ in heapq.nlargest(k, Counter(nums).items(), key=lambda p: p[1])]
    # O(n) alternative: bucket sort by frequency
```

**Running median:** two heaps. A max-heap holds the low half, a min-heap the high half; rebalance so sizes differ by ≤ 1.

```python
class MedianFinder:
    def __init__(self):
        self.low, self.high = [], []         # low is a max-heap (negated)
    def add(self, x):
        heapq.heappush(self.low, -x)
        heapq.heappush(self.high, -heapq.heappop(self.low))
        if len(self.high) > len(self.low):
            heapq.heappush(self.low, -heapq.heappop(self.high))
    def median(self):
        if len(self.low) > len(self.high): return -self.low[0]
        return (-self.low[0] + self.high[0]) / 2
```

**K-way merge:** push the head of each list; pop the smallest, push its successor. O(N log k).

## Intervals

Almost always: **sort by start**, then sweep.

```python
def merge(intervals):
    intervals.sort()
    out = [intervals[0]]
    for s, e in intervals[1:]:
        if s <= out[-1][1]: out[-1][1] = max(out[-1][1], e)
        else: out.append([s, e])
    return out

def min_meeting_rooms(intervals):
    starts = sorted(s for s, _ in intervals)
    ends = sorted(e for _, e in intervals)
    rooms = j = 0
    for s in starts:
        if s < ends[j]: rooms += 1
        else: j += 1
    return rooms
```

Non-overlapping Intervals (min removals): **sort by end**, greedily keep the interval that ends earliest.

## Greedy

Greedy works when a local choice can be shown never to hurt (an exchange argument). Say *why* out loud.

- **Jump Game:** track the farthest reachable index.
- **Gas Station:** if the total gas ≥ total cost, start right after the point where the running tank went negative.
- **Task Scheduler:** `max(len(tasks), (maxCount - 1) * (n + 1) + numberOfTasksWithMaxCount)`.
- **Partition Labels:** record the last index of each char; cut when `i == max last-index so far`.

## Practice

Kth Largest Element · Last Stone Weight · K Closest Points to Origin · Task Scheduler · Design Twitter ·
Find Median from Data Stream · Merge k Sorted Lists · Insert Interval · Merge Intervals ·
Non-overlapping Intervals · Meeting Rooms II · Jump Game I & II · Gas Station · Partition Labels
