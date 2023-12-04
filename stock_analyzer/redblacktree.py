import time
from queue import Queue

from stock_analyzer.redblacknode import RedBlackNode
from stock_analyzer.marketday import MarketDay


# 0 is black, 1 is red
class RedBlackTree:
    """This class is a representation of a red black tree. Here we initialize the RB Tree, and create a special
     node where we assign it to null and 0 represents the color of the node. We also set root to be equal to the
     null node."""

    def __init__(self):
        self.null = RedBlackNode(None, 0)  # inserts black root (0)
        self.root = self.null

    def runDateFilter(self, startDate: time.struct_time, endDate: time.struct_time, function, *args):
        queue = Queue()
        queue.put(self.root)
        while not queue.empty():
            current: RedBlackNode = queue.get()
            item: MarketDay = current.item
            if startDate <= item.date <= endDate:
                function(item, *args)

            if item.date >= startDate and current.left is not None and current.left != self.null:
                queue.put(current.left)
            if item.date <= endDate and current.right is not None and current.left != self.null:
                queue.put(current.right)

    def insert(self, key):
        """the insert helper function carries all the functionality of inserting a new node into
    the RB Tree"""
        node = RedBlackNode(key)
        node.parent = None
        node.item = key
        node.left = self.null
        node.right = self.null
        node.color = 1

        parent = None
        current = self.root

        while current != self.null:
            parent = current
            if node.item < current.item:
                current = current.left
            else:
                current = current.right

        node.parent = parent
        if parent is None:
            self.root = node
        elif parent and node.item < parent.item:
            parent.left = node
        else:
            parent.right = node

        if node.parent is None:
            node.color = 0
            return
        if node.parent.parent is None:
            return

        self.balanceTree(node)

    def balanceTree(self, node):
        self.root.color = 0

        while node.parent and node.parent.color == 1:
            if node.parent == node.parent.parent.right:
                nodeUncle = node.parent.parent.left
                if nodeUncle.color == 1:
                    nodeUncle.color = 0
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    node = node.parent.parent
                    # self.rotateLeft(node)

                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.rotateRight(node)

                    node.parent.color = 0
                    node.parent.parent.color = 1
                    self.rotateLeft(node.parent.parent)
            else:
                nodeUncle = node.parent.parent.right
                if nodeUncle.color == 1:
                    nodeUncle.color = 0
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    node = node.parent.parent
                    # self.rotateLeft(node)
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.rotateLeft(node)

                    node.parent.color = 0
                    node.parent.parent.color = 1
                    self.rotateRight(node.parent.parent)

        self.root.color = 0

    def rotateLeft(self, node):
        rightChild = node.right
        node.right = rightChild.left
        if rightChild.left != self.null:
            rightChild.left.parent = node

        rightChild.parent = node.parent
        if node.parent is None:
            self.root = rightChild
        elif node == node.parent.left:
            node.parent.left = rightChild
        else:
            node.parent.right = rightChild
        rightChild.left = node
        node.parent = rightChild

    def rotateRight(self, node):
        leftChild = node.left
        node.left = leftChild.right
        if leftChild.right != self.null:
            leftChild.right.parent = node

        leftChild.parent = node.parent
        if node.parent is None:
            self.root = leftChild
        elif node == node.parent.right:
            node.parent.right = leftChild
        else:
            node.parent.left = leftChild
        leftChild.right = node
        node.parent = leftChild

    def returnRoot(self):
        return self.root
