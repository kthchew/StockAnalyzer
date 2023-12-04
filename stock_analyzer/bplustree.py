from stock_analyzer.bplusnode import Node


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

    def printTree(self):
        current = self.root
        while not current.is_leaf():
            current = current.children[0]

        for i in range(current.item_count()):
            print(current.items[i])

        while current.nextLeaf is not None:
            current = current.nextLeaf
            for i in range(current.item_count()):
                print(current.items[i])
                
        def runDateFilter(self, start_date: time.struct_time, end_date: time.struct_time, function, *args):
        """Runs the provided function on all items between the start and end date.
        The function's first argument is the item in the tree to process. Other arguments provided to this method
        are passed into the provided function."""
        current = self.root
        while not current.is_leaf():
            for i in range(current.item_count()):
                item = current.items[i]
                if start_date <= item.date:
                    current = current.children[i]
                    break
                if i == current.item_count()-1:
                    current = current.children[i+1]
                    
        i = 0
        for j in range (current.items):
            if current.items[j].date >= start_date:
                i = j
                break
                
        while current.items[i].date <= end_date:
            function(current.items[i], *args)
            i += 1
            if i == self.L:
                i = 0
                current = current.nextLeaf
