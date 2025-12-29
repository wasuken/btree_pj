from .btree_node import BTreeNode


class BTree:
    def __init__(self, max_keys: int, initial_data: list[int] = None):
        self.max_keys = max_keys
        self.min_keys = max_keys // 2
        self.root = None
        if initial_data:
            self.root = self._build_from_array(initial_data)

    def _build_from_array(self, data: list[int]) -> BTreeNode:
        sorted_data = sorted(data)  # ソート
        return self._split_recursively(sorted_data)

    def _split_recursively(self, arr: list[int]) -> BTreeNode:
        if len(arr) <= self.max_keys:
            # 分割不要：単一ノード作成
            node = BTreeNode(max_keys=self.max_keys, keys=arr, is_leaf=True)
            # print(f"Leaf created: {node.keys}")
            return node

        else:
            # 分割必要：中間値で分割して子ノードを作る
            mid_index = len(arr) // 2
            mid_value = arr[mid_index]
            left_arr = arr[:mid_index]
            right_arr = arr[mid_index + 1 :]

            # 再帰的に子ノードを作成
            left_child = self._split_recursively(left_arr)
            right_child = self._split_recursively(right_arr)

            # 中間値をキーとする親ノードを作成
            result = BTreeNode(
                max_keys=self.max_keys,
                keys=[mid_value],
                is_leaf=False,
                children=[left_child, right_child],
            )
            # print(f"Internal node created: keys={result.keys}, children_count={len(result.children)}")
            return result

    def search(self, value: int) -> int | None:
        node = self.root
        while node:
            n = len(node.keys)
            for i in range(n):
                key = node.keys[i]
                if key == value:
                    return key
                elif key > value:
                    # left,rightしかないが、将来的に>3になったときにも対応可能
                    if node.is_leaf:
                        return None
                    else:
                        node = node.children[i]
                        break
                elif i == n - 1:
                    # 一番大きい範囲
                    if node.is_leaf:
                        return None
                    else:
                        node = node.children[n]
                        break
        return None

    def append_node_key(self, node, key):
        node.keys.append(key)
        node.keys.sort()
        if len(node.keys) > self.max_keys:
            nnode = self._split_recursively(node.keys)
            node.only_data_copy(nnode)

    def insert(self, value: int) -> None:
        if self.root is None:
            # 空ツリーの場合、新しいルートを作る
            self.root = BTreeNode(keys=[value], max_keys=self.max_keys, is_leaf=True)
            return
        # 挿入処理
        node = self.root
        while node:
            n = len(node.keys)
            for i in range(n):
                key = node.keys[i]
                if key == value:
                    return
                elif key > value:
                    # left,rightしかないが、将来的に>3になったときにも対応可能
                    if node.is_leaf:
                        self.append_node_key(node, value)
                        return
                    else:
                        node = node.children[i]
                        break
                elif i == n - 1:
                    # 一番大きい範囲
                    if node.is_leaf:
                        self.append_node_key(node, value)
                        return
                    else:
                        node = node.children[n]
                        break
        return None

    # def delete(self, value) -> int|None:
    #     if self.root is None:
    #         # 空ツリーの場合、無視
    #         return None
    #     # 削除処理
    #     node = self.root
    #     while node:
    #         n = len(node.keys)
    #         for i in range(n):
    #             key = node.keys[i]
    #             if key == value:
    #                 node.keys.remove(value)
    #                 # 見つかった。
    #                 return value
    #             elif key > value:
    #                 # left,rightしかないが、将来的に>3になったときにも対応可能
    #                 if node.is_leaf:
    #                     return None
    #                 else:
    #                     node = node.children[i]
    #                     break
    #             elif i == n - 1:
    #                 # 一番大きい範囲
    #                 if node.is_leaf:
    #                     return None
    #                 else:
    #                     node = node.children[n]
    #                     break
    #     return None
    def _collect_all_keys(self, node):
        keys = node.keys
        if not node.is_leaf:
            for child in node.children:
                keys += self._collect_all_keys(child)
        return keys

    def delete(self, value):
        if self.search(value):
            all_keys = self._collect_all_keys(self.root)  # 全キーを収集
            all_keys.sort()
            all_keys.remove(value)
            self.root = self._split_recursively(all_keys)  # 再構築
            return value
        return None

    def dprint(self):
        self.root.dprint()
