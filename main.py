import random
import time
from btree import BTree


# 比較用クラス
class SimpleList:
    def __init__(self, data=None):
        self.data = sorted(data or [])

    def insert(self, value):
        if value not in self.data:
            self.data.append(value)
            self.data.sort()

    def search(self, value):
        return value if value in self.data else None

    def delete(self, value):
        if value in self.data:
            self.data.remove(value)
            return value
        return None

    def range_search(self, min_val, max_val):
        return [x for x in self.data if min_val <= x <= max_val]


class SetWrapper:
    def __init__(self, data=None):
        self.data = set(data or [])

    def insert(self, value):
        self.data.add(value)

    def search(self, value):
        return value if value in self.data else None

    def delete(self, value):
        if value in self.data:
            self.data.remove(value)
            return value
        return None

    def range_search(self, min_val, max_val):
        return sorted([x for x in self.data if min_val <= x <= max_val])


def benchmark_search_heavy(name, data_structure, test_data, search_count=10000):
    print(f"\n=== {name} (Search Heavy) ===")

    # 少数のInsert test
    start = time.time()
    for value in test_data[-100:][:50]:
        data_structure.insert(value + 1000000)
    insert_time = time.time() - start
    print(f"Insert 50 values: {insert_time:.3f} seconds")

    # 大量Search test
    start = time.time()
    for _ in range(search_count):
        data_structure.search(random.choice(test_data))
    search_time = time.time() - start
    print(f"{search_count} searches: {search_time:.3f} seconds")

    # Range search test
    start = time.time()
    for _ in range(100):
        min_val = random.randint(1, 500000)
        max_val = min_val + random.randint(1000, 5000)
        result = data_structure.range_search(min_val, max_val)
    range_time = time.time() - start
    print(f"100 range searches: {range_time:.3f} seconds")

    # 少数のDelete test
    start = time.time()
    for value in test_data[-50:][:25]:
        data_structure.delete(value)
    delete_time = time.time() - start
    print(f"Delete 25 values: {delete_time:.3f} seconds")


if __name__ == "__main__":
    test_data = random.sample(range(1, 1000001), 100000)

    print("Building data structures...")
    btree = BTree(max_keys=10, initial_data=test_data)
    simple_list = SimpleList(test_data)
    set_wrapper = SetWrapper(test_data)

    benchmark_search_heavy("BTree", btree, test_data, 10000)
    benchmark_search_heavy("SimpleList", simple_list, test_data, 10000)
    benchmark_search_heavy("SetWrapper", set_wrapper, test_data, 10000)

    print("\n=== Range Search Demo ===")
    result = btree.range_search(50000, 50010)
    print(f"BTree range search (50000-50010): {len(result)} results")
    print(f"Sample results: {result[:5] if result else 'None'}")
