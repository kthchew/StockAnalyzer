class Node:
    def __init__(self, items: list, children: list):
        self.items = items
        self.children = children

    def child_count(self):
        """Return the number of child nodes."""
        return len(self.children)

    def item_count(self):
        """Return the number of items in the node."""
        return len(self.items)

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
        middle_index = self.item_count() // 2
        middle = self.items[middle_index]
        left = []
        right = []
        for i in range(middle_index):
            left.append(self.children[i])
        for i in range(middle_index + 1, self.item_count()):
            right.append(self.children[i])
        return left, middle, right

    def split_child(self, index):
        """Split the indexth child (starting at 0) into two children, and moves the middle
        element in that child to the current node."""
        left, middle, right = self.children[index].split_node()
        self.children[index] = left
        self.children.insert(index + 1, right)
        self.add_item(middle)
