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
        while not current.isLeaf():
            nextIndex = 0
            for i in range(current.itemCount()):
                if item > current.items[i]:
                    nextIndex += 1
                else:
                    break
            path.append((current, nextIndex))
            current = current.children[nextIndex]

        current.addItem(item)
        for node, child in reversed(path):
            childNode = node.children[child]
            if childNode.itemCount() > self.l or childNode.childCount() > self.n:
                node.splitChild(child)
        if self.root.itemCount() > self.l:
            left, mid, right = self.root.splitNode()
            mid = Node([mid], [left, right])
            self.root = mid

    def find(self, item):
        """Return True if the item is found in the tree, False otherwise."""
        queue = Queue()
        queue.put(self.root)
        while not queue.empty():
            current = queue.get()
            for i in range(current.itemCount()):
                if item == current.items[i]:
                    return True

                if i == 0 and item <= current.items[i] and not current.isLeaf():
                    queue.put(current.children[i])
                if item >= current.items[i] and not current.isLeaf():
                    queue.put(current.children[i + 1])
                else:
                    break
        return False

    def printTree(self):
        """Return True if the item is found in the tree, False otherwise."""
        queue = Queue()
        queue.put(self.root)
        total = 0
        while not queue.empty():
            current = queue.get()
            total += current.itemCount()
            for child in current.children:
                queue.put(child)
        print(total)

    def runDateFilter(self, startDate: time.struct_time, endDate: time.struct_time, function, *args):
        """Runs the provided function on all items between the start and end date.
        The function's first argument is the item in the tree to process. Other arguments provided to this method
        are passed into the provided function."""
        queue = Queue()
        queue.put(self.root)
        while not queue.empty():
            current: Node = queue.get()
            for i in range(current.itemCount()):
                item = current.items[i]

                if startDate <= item.date <= endDate:
                    function(item, *args)

                # things to the left have an older date, so check this is at least the start date (if not, then useful
                # items can't possibly be to the left)
                # similar logic with searching to the right
                if i == 0 and item.date >= startDate and not current.isLeaf():
                    queue.put(current.children[i])
                if item.date <= endDate and not current.isLeaf():
                    queue.put(current.children[i + 1])
