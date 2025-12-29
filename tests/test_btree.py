import unittest
from btree import BTree


class TestBTree(unittest.TestCase):
    def setUp(self):
        self.max_keys = 2

    def test_search_empty_tree(self):
        btree = BTree(self.max_keys)
        self.assertIsNone(btree.search(5))

    def test_search_single_node(self):
        btree = BTree(self.max_keys, [5])
        self.assertEqual(btree.search(5), 5)
        self.assertIsNone(btree.search(3))

    def test_search_multiple_values(self):
        btree = BTree(self.max_keys, [1, 3, 5, 7, 9])
        print(btree.root.keys, btree.root.children)
        self.assertEqual(btree.search(1), 1)
        self.assertEqual(btree.search(5), 5)
        self.assertEqual(btree.search(9), 9)
        self.assertIsNone(btree.search(2))
        self.assertIsNone(btree.search(10))


if __name__ == "__main__":
    # 簡単な動作テスト
    btree = BTree(2, [1, 2, 3, 4, 5])
    print(f"Search 3: {btree.search(3)}")
    print(f"Search 6: {btree.search(6)}")
    unittest.main()
