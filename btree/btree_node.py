class BTreeNode:
    def __init__(self, keys, max_keys, children=None, is_leaf=True):
        self.keys = keys or []
        self.children = children  # BTreeNodeのリスト
        self.is_leaf = is_leaf
        self.max_keys = max_keys
