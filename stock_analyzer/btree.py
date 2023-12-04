import time

from stock_analyzer.bnode import Node
from queue import Queue


class BTree:
    """A class representing a B tree. n is the maximum number of children a node can have,
    l is the maximum number of items a node can have."""

    def __init__(self, n, l):
        self.n = n
        self.l = l
        self.root = Node([], [])

    def insert(self, item):
        """Insert the provided item in the tree. Nodes are automatically split if necessary."""
        path = []
        current: Node = self.root
        while not current.is_leaf():
            next_index = 0
            for i in range(current.item_count()):
                if item > current.items[i]:
                    next_index += 1
                else:
                    break
            path.append((current, next_index))
            current = current.children[next_index]

        current.add_item(item)
        for node, child in reversed(path):
            child_node = node.children[child]
            if child_node.item_count() > self.l or child_node.child_count() > self.n:
                node.split_child(child)
        if self.root.item_count() > self.l:
            left, mid, right = self.root.split_node()
            mid = Node([mid], [left, right])
            self.root = mid

    def find(self, item):
        """Return True if the item is found in the tree, False otherwise."""
        queue = Queue()
        queue.put(self.root)
        while not queue.empty():
            current = queue.get()
            for i in range(current.item_count()):
                if item == current.items[i]:
                    return True

                if i == 0 and item <= current.items[i] and not current.is_leaf():
                    queue.put(current.children[i])
                if item >= current.items[i] and not current.is_leaf():
                    queue.put(current.children[i + 1])
                else:
                    break
        return False

    def runDateFilter(self, start_date: time.struct_time, end_date: time.struct_time, function, *args):
        """Runs the provided function on all items between the start and end date.
        The function's first argument is the item in the tree to process. Other arguments provided to this method
        are passed into the provided function."""
        queue = Queue()
        queue.put(self.root)
        while not queue.empty():
            current: Node = queue.get()
            for i in range(current.item_count()):
                item = current.items[i]

                if start_date <= item.date <= end_date:
                    function(item, *args)

                # things to the left have an older date, so check this is at least the start date (if not, then useful
                # items can't possibly be to the left)
                # similar logic with searching to the right
                if i == 0 and item.date >= start_date and not current.is_leaf():
                    queue.put(current.children[i])
                if item.date <= end_date and not current.is_leaf():
                    queue.put(current.children[i + 1])
