# Trees, BSTs, tries

## DFS recursion: think "what do I need from my children?"

Most tree problems are a post-order function that returns something to the parent and updates a global answer.

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def diameter(root):
    best = 0
    def height(node):
        nonlocal best
        if not node:
            return 0
        l, r = height(node.left), height(node.right)
        best = max(best, l + r)          # path through this node
        return 1 + max(l, r)             # what the parent needs
    height(root)
    return best

def max_path_sum(root):
    best = float("-inf")
    def gain(node):
        nonlocal best
        if not node:
            return 0
        l, r = max(gain(node.left), 0), max(gain(node.right), 0)   # drop negative branches
        best = max(best, node.val + l + r)
        return node.val + max(l, r)
    gain(root)
    return best
```

## BFS: level order

```python
from collections import deque
def level_order(root):
    if not root: return []
    res, q = [], deque([root])
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left: q.append(node.left)
            if node.right: q.append(node.right)
        res.append(level)
    return res
```

Right side view = last element of each level. Zigzag = reverse every other level.

## BST

- In-order traversal of a BST is **sorted**. Kth smallest = the kth element of the in-order traversal.
- Validate a BST by passing `(low, high)` bounds down. Don't compare only with the children.
- Lowest common ancestor in a BST: walk from the root; split point where p and q diverge.

```python
def is_valid_bst(node, low=float("-inf"), high=float("inf")):
    if not node: return True
    if not (low < node.val < high): return False
    return is_valid_bst(node.left, low, node.val) and is_valid_bst(node.right, node.val, high)
```

LCA in a general binary tree: return the node if it's p or q; if both sides return non-null, this node is the LCA.

## Serialize / deserialize

Pre-order with null markers ("#"), then rebuild with an iterator. O(n).

## Trie

**Recognize:** prefix search, autocomplete, word games on grids (Word Search II), longest common prefix.

```python
class Trie:
    def __init__(self):
        self.root = {}
    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node["$"] = True
    def _walk(self, s):
        node = self.root
        for ch in s:
            if ch not in node: return None
            node = node[ch]
        return node
    def search(self, word):
        node = self._walk(word); return bool(node and "$" in node)
    def starts_with(self, prefix):
        return self._walk(prefix) is not None
```

Word Search II: build a trie of words, DFS the grid once, prune trie nodes as words are found.

## Practice

Invert Binary Tree · Maximum Depth · Diameter of Binary Tree · Balanced Binary Tree · Same Tree · Subtree of Another Tree ·
LCA of a BST · Level Order Traversal · Right Side View · Count Good Nodes · Validate BST · Kth Smallest in a BST ·
Construct Tree from Preorder and Inorder · Binary Tree Maximum Path Sum · Serialize and Deserialize Binary Tree ·
Implement Trie · Design Add and Search Words · Word Search II
