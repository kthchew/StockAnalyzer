class RedBlackNode:
    def __init__(self, item, color=1, parent=None, left=None, right=None):
        self.item = item
        self.color = color
        self.parent = parent
        self.left = left
        self.right = right

    def __lt__(self, other):
        if other is None or not isinstance(other, RedBlackNode):
            return NotImplemented
        return self.item < other.item
