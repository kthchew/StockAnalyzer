from bplusnode import Node


class BPlusTree:
    def __init__(self, n, L):
        self.n = n
        self.L = L
        self.root = Node([], [])

    def insert(self, item):
        """Insert the provided item in the tree. Nodes are automatically split if necessary."""
        path = []
        current: Node = self.root

        """navigates to a leaf"""
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

            if child_node.item_count() > self.L or child_node.child_count() > self.n:
                node.split_child(child)

        if self.root.item_count() > self.L:
            left, mid, right = self.root.split_node()
            left.nextLeaf = right
            right.nextLeaf = self.root.nextLeaf
            mid = Node([mid], [left, right])
            self.root = mid

    def find(self, item):
        """Return True if the item is found in the tree, False otherwise."""
        current = self.root
        while not current.is_leaf():
            next_index = 0
            for i in range(current.item_count()):
                if item == current.items[i]:
                    return True

                if item > current.items[i]:
                    next_index += 1
                else:
                    break
            current = current.children[next_index]
        return False