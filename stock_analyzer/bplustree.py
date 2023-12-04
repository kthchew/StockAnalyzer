from bplusnode import Node
import time


class BPlusTree:
    def __init__(self, n, L):
        self.n = n
        self.L = L
        self.root = Node([], [])

    def insert(self, item):
        """Insert the provided item in the tree. Nodes are automatically split if necessary."""
        path = []
        current: Node = self.root

        """Navigates to a leaf"""
        while not current.isLeaf():
            next_index = 0
            for i in range(current.itemCount()):
                if item > current.items[i]:
                    next_index += 1
                else:
                    break
            path.append((current, next_index))
            current = current.children[next_index]

        current.addItem(item)
        for node, child in reversed(path):
            child_node = node.children[child]

            if child_node.itemCount() > self.L or child_node.child_count() > self.n:
                node.splitChild(child)

        if self.root.itemCount() > self.L:
            left, mid, right = self.root.splitNode()
            left.nextLeaf = right
            mid = Node([mid], [left, right])
            self.root = mid

    def runDateFilter(self, start_date: time.struct_time, end_date: time.struct_time, function, *args):
        """Runs the provided function on all items between the start and end date.
        The function's first argument is the item in the tree to process. Other arguments provided to this method
        are passed into the provided function."""
        current = self.root
        while not current.isLeaf():
            for i in range(current.itemCount()):
                item = current.items[i]
                if start_date <= item.date:
                    current = current.children[i]
                    break
                if i == current.itemCount() - 1:
                    current = current.children[i + 1]

        i = 0
        for j in range(current.itemCount()):
            if current.items[j].date >= start_date:
                i = j
                break

        while current.items[i].date <= end_date:
            function(current.items[i], *args)
            i += 1
            if i == self.L:
                i = 0
                current = current.nextLeaf
