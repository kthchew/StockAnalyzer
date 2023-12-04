from stock_analyzer.bplusnode import Node
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

            if childNode.itemCount() > self.L or childNode.childCount() > self.n:
                node.splitChild(child)

        if self.root.itemCount() > self.L:
            left, mid, right = self.root.splitNode()
            left.nextLeaf = right
            mid = Node([mid], [left, right])
            self.root = mid

    def runDateFilter(self, startDate: time.struct_time, endDate: time.struct_time, function, *args):
        """Runs the provided function on all items between the start and end date.
        The function's first argument is the item in the tree to process. Other arguments provided to this method
        are passed into the provided function."""
        current = self.root
        while not current.isLeaf():
            for i in range(current.itemCount()):
                item = current.items[i]
                if startDate <= item.date:
                    current = current.children[i]
                    break
                if i == current.itemCount() - 1:
                    current = current.children[i + 1]
            else:
                if current.itemCount() == 0:
                    current = current.children[0]

        i = 0
        for j in range(current.itemCount()):
            if current.items[j].date >= startDate:
                i = j
                break

        while current.items[i].date <= endDate:
            function(current.items[i], *args)
            i += 1
            if i >= current.itemCount():
                i = 0
                current = current.nextLeaf
