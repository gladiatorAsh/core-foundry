"""Curated coding problem list. Run `python tools/problems.py` to regenerate 01-coding/problem-list.md."""
from pathlib import Path

# (title, leetcode slug, difficulty, priority) — priority: 1 = must do, 2 = strongly recommended, 3 = stretch
PROBLEMS = {
    "Arrays & hashing": [
        ("Two Sum", "two-sum", "E", 1), ("Contains Duplicate", "contains-duplicate", "E", 2),
        ("Valid Anagram", "valid-anagram", "E", 2), ("Group Anagrams", "group-anagrams", "M", 1),
        ("Top K Frequent Elements", "top-k-frequent-elements", "M", 1),
        ("Product of Array Except Self", "product-of-array-except-self", "M", 1),
        ("Longest Consecutive Sequence", "longest-consecutive-sequence", "M", 1),
        ("Subarray Sum Equals K", "subarray-sum-equals-k", "M", 1),
        ("Encode and Decode Strings", "encode-and-decode-strings", "M", 2),
        ("Valid Sudoku", "valid-sudoku", "M", 3),
    ],
    "Two pointers & sliding window": [
        ("Valid Palindrome", "valid-palindrome", "E", 2), ("3Sum", "3sum", "M", 1),
        ("Container With Most Water", "container-with-most-water", "M", 1),
        ("Trapping Rain Water", "trapping-rain-water", "H", 1),
        ("Best Time to Buy and Sell Stock", "best-time-to-buy-and-sell-stock", "E", 2),
        ("Longest Substring Without Repeating Characters", "longest-substring-without-repeating-characters", "M", 1),
        ("Longest Repeating Character Replacement", "longest-repeating-character-replacement", "M", 2),
        ("Permutation in String", "permutation-in-string", "M", 2),
        ("Minimum Window Substring", "minimum-window-substring", "H", 1),
        ("Sliding Window Maximum", "sliding-window-maximum", "H", 2),
    ],
    "Stacks": [
        ("Valid Parentheses", "valid-parentheses", "E", 1), ("Min Stack", "min-stack", "M", 2),
        ("Evaluate Reverse Polish Notation", "evaluate-reverse-polish-notation", "M", 2),
        ("Daily Temperatures", "daily-temperatures", "M", 1), ("Car Fleet", "car-fleet", "M", 3),
        ("Largest Rectangle in Histogram", "largest-rectangle-in-histogram", "H", 1),
        ("Basic Calculator II", "basic-calculator-ii", "M", 2),
    ],
    "Binary search": [
        ("Binary Search", "binary-search", "E", 2), ("Search a 2D Matrix", "search-a-2d-matrix", "M", 2),
        ("Koko Eating Bananas", "koko-eating-bananas", "M", 1),
        ("Find Minimum in Rotated Sorted Array", "find-minimum-in-rotated-sorted-array", "M", 1),
        ("Search in Rotated Sorted Array", "search-in-rotated-sorted-array", "M", 1),
        ("Time Based Key-Value Store", "time-based-key-value-store", "M", 1),
        ("Median of Two Sorted Arrays", "median-of-two-sorted-arrays", "H", 2),
        ("Split Array Largest Sum", "split-array-largest-sum", "H", 3),
    ],
    "Linked lists": [
        ("Reverse Linked List", "reverse-linked-list", "E", 1), ("Merge Two Sorted Lists", "merge-two-sorted-lists", "E", 1),
        ("Linked List Cycle", "linked-list-cycle", "E", 2), ("Reorder List", "reorder-list", "M", 2),
        ("Remove Nth Node From End of List", "remove-nth-node-from-end-of-list", "M", 2),
        ("Copy List with Random Pointer", "copy-list-with-random-pointer", "M", 2),
        ("Add Two Numbers", "add-two-numbers", "M", 3), ("LRU Cache", "lru-cache", "M", 1),
        ("Merge k Sorted Lists", "merge-k-sorted-lists", "H", 1),
        ("Reverse Nodes in k-Group", "reverse-nodes-in-k-group", "H", 3),
    ],
    "Trees": [
        ("Invert Binary Tree", "invert-binary-tree", "E", 2), ("Maximum Depth of Binary Tree", "maximum-depth-of-binary-tree", "E", 2),
        ("Diameter of Binary Tree", "diameter-of-binary-tree", "E", 1), ("Balanced Binary Tree", "balanced-binary-tree", "E", 2),
        ("Subtree of Another Tree", "subtree-of-another-tree", "E", 3),
        ("Lowest Common Ancestor of a BST", "lowest-common-ancestor-of-a-binary-search-tree", "M", 2),
        ("Lowest Common Ancestor of a Binary Tree", "lowest-common-ancestor-of-a-binary-tree", "M", 1),
        ("Binary Tree Level Order Traversal", "binary-tree-level-order-traversal", "M", 1),
        ("Binary Tree Right Side View", "binary-tree-right-side-view", "M", 1),
        ("Validate Binary Search Tree", "validate-binary-search-tree", "M", 1),
        ("Kth Smallest Element in a BST", "kth-smallest-element-in-a-bst", "M", 2),
        ("Construct Binary Tree from Preorder and Inorder", "construct-binary-tree-from-preorder-and-inorder-traversal", "M", 2),
        ("Binary Tree Maximum Path Sum", "binary-tree-maximum-path-sum", "H", 1),
        ("Serialize and Deserialize Binary Tree", "serialize-and-deserialize-binary-tree", "H", 1),
    ],
    "Tries": [
        ("Implement Trie", "implement-trie-prefix-tree", "M", 1),
        ("Design Add and Search Words", "design-add-and-search-words-data-structure", "M", 2),
        ("Word Search II", "word-search-ii", "H", 2),
    ],
    "Heaps & intervals": [
        ("Kth Largest Element in an Array", "kth-largest-element-in-an-array", "M", 1),
        ("K Closest Points to Origin", "k-closest-points-to-origin", "M", 1), ("Task Scheduler", "task-scheduler", "M", 2),
        ("Design Twitter", "design-twitter", "M", 3), ("Find Median from Data Stream", "find-median-from-data-stream", "H", 1),
        ("Merge Intervals", "merge-intervals", "M", 1), ("Insert Interval", "insert-interval", "M", 2),
        ("Non-overlapping Intervals", "non-overlapping-intervals", "M", 2), ("Meeting Rooms II", "meeting-rooms-ii", "M", 1),
    ],
    "Backtracking": [
        ("Subsets", "subsets", "M", 1), ("Combination Sum", "combination-sum", "M", 1), ("Permutations", "permutations", "M", 1),
        ("Subsets II", "subsets-ii", "M", 3), ("Word Search", "word-search", "M", 1),
        ("Palindrome Partitioning", "palindrome-partitioning", "M", 3),
        ("Letter Combinations of a Phone Number", "letter-combinations-of-a-phone-number", "M", 2),
        ("Generate Parentheses", "generate-parentheses", "M", 2), ("N-Queens", "n-queens", "H", 3),
    ],
    "Graphs": [
        ("Number of Islands", "number-of-islands", "M", 1), ("Clone Graph", "clone-graph", "M", 1),
        ("Max Area of Island", "max-area-of-island", "M", 3), ("Rotting Oranges", "rotting-oranges", "M", 1),
        ("Pacific Atlantic Water Flow", "pacific-atlantic-water-flow", "M", 2), ("Course Schedule", "course-schedule", "M", 1),
        ("Course Schedule II", "course-schedule-ii", "M", 1), ("Graph Valid Tree", "graph-valid-tree", "M", 2),
        ("Number of Connected Components", "number-of-connected-components-in-an-undirected-graph", "M", 2),
        ("Redundant Connection", "redundant-connection", "M", 2), ("Accounts Merge", "accounts-merge", "M", 2),
        ("Word Ladder", "word-ladder", "H", 1), ("Network Delay Time", "network-delay-time", "M", 1),
        ("Cheapest Flights Within K Stops", "cheapest-flights-within-k-stops", "M", 2),
        ("Min Cost to Connect All Points", "min-cost-to-connect-all-points", "M", 3),
        ("Alien Dictionary", "alien-dictionary", "H", 1), ("Swim in Rising Water", "swim-in-rising-water", "H", 3),
    ],
    "Dynamic programming": [
        ("Climbing Stairs", "climbing-stairs", "E", 2), ("House Robber", "house-robber", "M", 1),
        ("House Robber II", "house-robber-ii", "M", 2), ("Longest Palindromic Substring", "longest-palindromic-substring", "M", 1),
        ("Decode Ways", "decode-ways", "M", 1), ("Coin Change", "coin-change", "M", 1),
        ("Maximum Product Subarray", "maximum-product-subarray", "M", 2), ("Word Break", "word-break", "M", 1),
        ("Longest Increasing Subsequence", "longest-increasing-subsequence", "M", 1),
        ("Partition Equal Subset Sum", "partition-equal-subset-sum", "M", 2), ("Unique Paths", "unique-paths", "M", 2),
        ("Longest Common Subsequence", "longest-common-subsequence", "M", 1),
        ("Best Time to Buy and Sell Stock with Cooldown", "best-time-to-buy-and-sell-stock-with-cooldown", "M", 3),
        ("Coin Change II", "coin-change-ii", "M", 2), ("Target Sum", "target-sum", "M", 2),
        ("Edit Distance", "edit-distance", "M", 1), ("Burst Balloons", "burst-balloons", "H", 3),
        ("Regular Expression Matching", "regular-expression-matching", "H", 3),
    ],
    "Design-a-data-structure": [
        ("LFU Cache", "lfu-cache", "H", 2), ("Insert Delete GetRandom O(1)", "insert-delete-getrandom-o1", "M", 1),
        ("Design Hit Counter", "design-hit-counter", "M", 2), ("Snapshot Array", "snapshot-array", "M", 2),
        ("Design In-Memory File System", "design-in-memory-file-system", "H", 3),
        ("Logger Rate Limiter", "logger-rate-limiter", "E", 2),
    ],
}

LABEL = {"E": "Easy", "M": "Medium", "H": "Hard"}
PRIO = {1: "★★★ must", 2: "★★ should", 3: "★ stretch"}

def render() -> str:
    total = sum(len(v) for v in PROBLEMS.values())
    must = sum(1 for v in PROBLEMS.values() for p in v if p[3] == 1)
    lines = [
        "# Curated problem list",
        "",
        f"{total} problems ({must} marked *must*). Do all *must* problems first (≈ 4 weeks at 3/day), then *should*.",
        "Tick the box in your fork as you go, and log misses for spaced re-solves (day 3, 7, 21).",
        "",
        "_Generated by `python tools/problems.py`; edit the list there._",
        "",
    ]
    for section, items in PROBLEMS.items():
        lines += [f"## {section}", "", "| Done | Problem | Difficulty | Priority |", "|---|---|---|---|"]
        for title, slug, diff, prio in sorted(items, key=lambda p: (p[3], "EMH".index(p[2]))):
            lines.append(f"| [ ] | [{title}](https://leetcode.com/problems/{slug}/) | {LABEL[diff]} | {PRIO[prio]} |")
        lines.append("")
    return "\n".join(lines)

if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "01-coding" / "problem-list.md"
    out.write_text(render())
    print(f"wrote {out}")
