from common.item import Item
from typing import List, Optional, Tuple


class Inventory:
    def __init__(self):
        self.storage: List[Optional[Tuple[Item, int]]] = [None for _ in range(16)]
        self.first_free_index = 0

    def add_item(self, item: Item):
        for i, elem in enumerate(self.storage):
            if elem is None:
                break
            storage_item, count = elem
            if storage_item.name == item.name:
                self.storage[i] = (storage_item, count + 1)
                return

        self.storage[self.first_free_index] = (item, 1)
        self.first_free_index += 1

    def remove_item(self, item: Item):
        for i, elem in enumerate(self.storage):
            if elem is None:
                break
            storage_item, count = elem
            if storage_item.name == item.name:
                self.storage[i] = (storage_item, count - 1)
                return

    def get_count(self, item: Item):
        for i, elem in enumerate(self.storage):
            if elem is None:
                break
            storage_item, count = elem
            if storage_item.name == item.name:
                return count
        return None

    def __getitem__(self, i):
        if self.storage[i] is None:
            return None
        return self.storage[i][0]
