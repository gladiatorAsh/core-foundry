# Stacks, monotonic stacks/queues, linked lists

## Stack

**Recognize:** matching pairs, "most recent", nested structure, undo, evaluating expressions.

```python
def is_valid(s):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
        else:
            stack.append(ch)
    return not stack
```

## Monotonic stack: "next greater/smaller element"

**Recognize:** "next warmer day", "largest rectangle", "stock span", for each element find the nearest
bigger/smaller one. O(n): each index is pushed and popped once.

```python
def daily_temperatures(t):
    res = [0] * len(t)
    stack = []                       # indices, temperatures decreasing
    for i, x in enumerate(t):
        while stack and t[stack[-1]] < x:
            j = stack.pop()
            res[j] = i - j
        stack.append(i)
    return res

def largest_rectangle(heights):
    heights = heights + [0]          # sentinel flushes the stack
    stack, best = [], 0              # indices with increasing heights
    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] >= h:
            height = heights[stack.pop()]
            left = stack[-1] + 1 if stack else 0
            best = max(best, height * (i - left))
        stack.append(i)
    return best
```

## Monotonic deque: sliding window maximum

```python
from collections import deque
def max_sliding_window(nums, k):
    dq, res = deque(), []            # indices, values decreasing
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            res.append(nums[dq[0]])
    return res
```

## Linked lists

**Techniques:** dummy head, fast/slow pointers, reverse in place, merge.

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val, self.next = val, next

def reverse(head):
    prev = None
    while head:
        head.next, prev, head = prev, head, head.next
    return prev

def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            return True
    return False

def merge_two(a, b):
    dummy = tail = ListNode()
    while a and b:
        if a.val <= b.val: tail.next, a = a, a.next
        else: tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b
    return dummy.next
```

- Middle of list: slow/fast; when fast ends, slow is at the middle.
- Cycle start (Floyd): after meeting, reset one pointer to head; advance both by 1; they meet at the start.
- Reorder list = find middle + reverse second half + merge alternately.

## Practice

Valid Parentheses · Min Stack · Evaluate Reverse Polish Notation · Daily Temperatures · Car Fleet ·
Largest Rectangle in Histogram · Sliding Window Maximum · Reverse Linked List · Merge Two Sorted Lists ·
Linked List Cycle · Reorder List · Remove Nth Node From End · Merge k Sorted Lists · Copy List with Random Pointer
