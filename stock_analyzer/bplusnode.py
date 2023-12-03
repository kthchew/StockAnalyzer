import math


class Node:
    def __init__(self, items: list, children: list):
        self.items = items
        self.children = children
        self.nextLeaf = None

    def child_count(self):
        """Return the number of child nodes."""
        return len(self.children)

    def item_count(self):
        """Return the number of items in the node."""
        return len(self.items)

    def is_leaf(self):
        """Return whether this node is a leaf node."""
        return len(self.children) == 0

    def add_item(self, item):
        """Add the given item to this node in the proper order."""
        for i in range(self.item_count()):
            if item <= self.items[i]:
                self.items.insert(i, item)
                return
        self.items.append(item)

    def split_node(self):
        """Return a node containing the left half of this node's elements, the middle element of
        this node, and a node containing the right half. Neither node will contain the middle
        element."""
        left = []
        right = []
        left_children = []
        right_children = []

        if not self.is_leaf():
            middle_index = math.ceil(self.item_count()/2)-1
            for i in range(middle_index-1):
                left.append(self.items[i])
            middle = self.items[middle_index]
            for i in range(middle_index + 1, self.item_count()):
                right.append(self.items[i])

            for i in range(len(left) + 1):
                left_children.append(self.children[i])
            for i in range(len(left) + 1, self.child_count()):
                right_children.append(self.children[i])

        else:
            middle_index = math.ceil(self.item_count()/2)-1
            for i in range(middle_index + 1):
                left.append(self.items[i])
            for i in range(middle_index + 1, self.item_count()):
                right.append(self.items[i])
            middle = right[0]

        return Node(left, left_children), middle, Node(right, right_children)

    def split_child(self, index):
        """Split the indexth child (starting at 0) into two children, and moves the middle
        element in that child to the current node."""
        left, middle, right = self.children[index].split_node()
        right.nextLeaf = self.children[index].nextLeaf
        self.children[index].items = left.items
        self.children[index].children = left.children
        self.children[index].nextLeaf = right
        self.children.insert(index + 1, right)
        self.add_item(middle)
