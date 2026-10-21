"""Executes the Python templates embedded in 01-coding/patterns/*.md and checks them on known answers.
Run: python -m unittest discover tests   (or: python -m pytest tests)"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NS: dict = {}
for md in sorted((ROOT / "01-coding" / "patterns").glob("*.md")):
    for block in re.findall(r"```python\n(.*?)```", md.read_text(encoding="utf-8"), flags=re.S):
        exec(compile(block, str(md), "exec"), NS)   # templates are self-contained by design
for md in [ROOT / "05-ml-fundamentals" / "transformers-and-llms.md"]:
    for block in re.findall(r"```python\n(.*?)```", md.read_text(encoding="utf-8"), flags=re.S):
        exec(compile(block, str(md), "exec"), NS)
F = type("F", (), NS)


def build_list(vals):
    head = None
    for v in reversed(vals):
        head = F.ListNode(v, head)
    return head


def to_list(node):
    out = []
    while node:
        out.append(node.val); node = node.next
    return out


class TestArrays(unittest.TestCase):
    def test_hashing_prefix_window(self):
        self.assertEqual(F.two_sum([2, 7, 11, 15], 9), [0, 1])
        self.assertEqual(sorted(map(sorted, F.group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))),
                         [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]])
        self.assertEqual(F.subarray_sum_equals_k([1, 1, 1], 2), 2)
        self.assertEqual(F.subarray_sum_equals_k([1, -1, 0], 0), 3)
        self.assertEqual(F.three_sum([-1, 0, 1, 2, -1, -4]), [[-1, -1, 2], [-1, 0, 1]])
        self.assertEqual(F.longest_substring_at_most_k_distinct("eceba", 2), 3)
        self.assertEqual(F.min_window("ADOBECODEBANC", "ABC"), "BANC")
        self.assertEqual(F.min_window("a", "aa"), "")


class TestBinarySearch(unittest.TestCase):
    def test_all(self):
        self.assertEqual(F.first_true(0, 4, lambda i: [1, 3, 5, 7, 9][i] >= 6), 3)
        self.assertEqual(F.min_eating_speed([3, 6, 7, 11], 8), 4)
        self.assertEqual(F.search_rotated([4, 5, 6, 7, 0, 1, 2], 0), 4)
        self.assertEqual(F.search_rotated([4, 5, 6, 7, 0, 1, 2], 3), -1)


class TestStacksLists(unittest.TestCase):
    def test_stacks(self):
        self.assertTrue(F.is_valid("([]{})")); self.assertFalse(F.is_valid("(]"))
        self.assertEqual(F.daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]), [1, 1, 4, 2, 1, 1, 0, 0])
        self.assertEqual(F.largest_rectangle([2, 1, 5, 6, 2, 3]), 10)
        self.assertEqual(F.max_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3), [3, 3, 5, 5, 6, 7])

    def test_lists(self):
        self.assertEqual(to_list(F.reverse(build_list([1, 2, 3]))), [3, 2, 1])
        self.assertEqual(to_list(F.merge_two(build_list([1, 3]), build_list([2, 4]))), [1, 2, 3, 4])
        head = build_list([1, 2, 3]); head.next.next.next = head.next
        self.assertTrue(F.has_cycle(head)); self.assertFalse(F.has_cycle(build_list([1, 2])))


class TestTrees(unittest.TestCase):
    def test_trees(self):
        T = F.TreeNode
        root = T(1, T(2, T(4), T(5)), T(3))
        self.assertEqual(F.diameter(root), 3)
        self.assertEqual(F.max_path_sum(T(-10, T(9), T(20, T(15), T(7)))), 42)
        self.assertEqual(F.level_order(root), [[1], [2, 3], [4, 5]])
        self.assertTrue(F.is_valid_bst(T(2, T(1), T(3))))
        self.assertFalse(F.is_valid_bst(T(5, T(1), T(4, T(3), T(6)))))
        t = F.Trie(); t.insert("apple")
        self.assertTrue(t.search("apple")); self.assertFalse(t.search("app")); self.assertTrue(t.starts_with("app"))


class TestGraphs(unittest.TestCase):
    def test_graphs(self):
        self.assertEqual(F.oranges_rotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]), 4)
        self.assertEqual(F.oranges_rotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]]), -1)
        self.assertEqual(F.num_islands([list("11000"), list("11000"), list("00100"), list("00011")]), 3)
        order = F.find_order(4, [[1, 0], [2, 0], [3, 1], [3, 2]])
        self.assertEqual(order[0], 0); self.assertEqual(order[-1], 3)
        self.assertEqual(F.find_order(2, [[0, 1], [1, 0]]), [])
        d = F.DSU(3); self.assertTrue(d.union(0, 1)); self.assertFalse(d.union(1, 0))
        self.assertEqual(F.network_delay([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2), 2)


class TestHeapsIntervals(unittest.TestCase):
    def test_all(self):
        self.assertEqual(sorted(F.top_k_frequent([1, 1, 1, 2, 2, 3], 2)), [1, 2])
        m = F.MedianFinder()
        for x in [5, 15, 1, 3]:
            m.add(x)
        self.assertEqual(m.median(), 4)
        self.assertEqual(F.merge([[1, 3], [2, 6], [8, 10], [15, 18]]), [[1, 6], [8, 10], [15, 18]])
        self.assertEqual(F.min_meeting_rooms([[0, 30], [5, 10], [15, 20]]), 2)


class TestBacktrackingDP(unittest.TestCase):
    def test_backtracking(self):
        self.assertEqual(len(F.subsets([1, 2, 3])), 8)
        self.assertEqual(sorted(F.combination_sum([2, 3, 6, 7], 7)), [[2, 2, 3], [7]])
        self.assertEqual(len(F.permutations([1, 2, 3])), 6)

    def test_dp(self):
        self.assertEqual(F.climb_stairs(5), 8)
        self.assertEqual(F.rob([2, 7, 9, 3, 1]), 12)
        self.assertEqual(F.coin_change([1, 2, 5], 11), 3)
        self.assertEqual(F.coin_change([2], 3), -1)
        self.assertTrue(F.word_break("leetcode", ["leet", "code"]))
        self.assertEqual(F.lcs("abcde", "ace"), 3)
        self.assertEqual(F.edit_distance("horse", "ros"), 3)
        self.assertTrue(F.can_partition([1, 5, 11, 5])); self.assertFalse(F.can_partition([1, 2, 3, 5]))


class TestDesign(unittest.TestCase):
    def test_lru(self):
        c = F.LRUCache(2); c.put(1, 1); c.put(2, 2)
        self.assertEqual(c.get(1), 1); c.put(3, 3)
        self.assertEqual(c.get(2), -1); c.put(4, 4)
        self.assertEqual(c.get(1), -1); self.assertEqual(c.get(3), 3); self.assertEqual(c.get(4), 4)

    def test_rate_limiters(self):
        w = F.SlidingWindowLog(2, 10)
        self.assertEqual([w.allow(0), w.allow(1), w.allow(2), w.allow(10.5)], [True, True, False, True])
        tb = F.TokenBucket(rate_per_s=0.0001, capacity=2)
        self.assertEqual([tb.allow(), tb.allow(), tb.allow()], [True, True, False])


class TestAttention(unittest.TestCase):
    def test_attention_shapes_and_mask(self):
        try:
            import numpy as np
        except ImportError:
            self.skipTest("numpy not installed")
        rng = np.random.default_rng(0)
        Q, K, V = (rng.normal(size=(4, 8)) for _ in range(3))
        out = F.attention(Q, K, V, causal=True)
        self.assertEqual(out.shape, (4, 8))
        np.testing.assert_allclose(out[0], V[0], rtol=1e-6)   # first token can only attend to itself


if __name__ == "__main__":
    unittest.main()
