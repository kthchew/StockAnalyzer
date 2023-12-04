import math


class Node:
    def __init__(self, items: list, children: list):
        self.items = items
        self.children = children
        self.nextLeaf = None

    def childCount(self):
        """Return the number of child nodes."""
        return len(self.children)

    def itemCount(self):
        """Return the number of items in the node."""
        return len(self.items)

    def isLeaf(self):
        """Return whether this node is a leaf node."""
        return len(self.children) == 0

    def addItem(self, item):
        """Add the given item to this node in the proper order."""
        for i in range(self.itemCount()):
            if item <= self.items[i]:
                self.items.insert(i, item)
                return
        self.items.append(item)

    def splitNode(self):
        """Return a node containing the left half of this node's elements, the first element of
        the right node, and a node containing the right half."""
        left = []
        right = []
        left_children = []
        right_children = []

        if not self.isLeaf():
            middle_index = math.ceil(self.itemCount() / 2) - 1
            for i in range(middle_index - 1):
                left.append(self.items[i])
            middle = self.items[middle_index]
            for i in range(middle_index + 1, self.itemCount()):
                right.append(self.items[i])

            for i in range(len(left) + 1):
                left_children.append(self.children[i])
            for i in range(len(left) + 1, self.childCount()):
                right_children.append(self.children[i])

        else:
            middle_index = math.ceil(self.itemCount() / 2) - 1
            for i in range(middle_index + 1):
                left.append(self.items[i])
            for i in range(middle_index + 1, self.itemCount()):
                right.append(self.items[i])
            middle = right[0]

        return Node(left, left_children), middle, Node(right, right_children)

    def splitChild(self, index):
        """Split the indexth child (starting at 0) into two children, and makes a copy of the middle
        element in that child in the current node."""
        left, middle, right = self.children[index].splitNode()
        right.nextLeaf = self.children[index].nextLeaf
        self.children[index].items = left.items
        self.children[index].children = left.children
        self.children[index].nextLeaf = right
        self.children.insert(index + 1, right)
        self.addItem(middle)
