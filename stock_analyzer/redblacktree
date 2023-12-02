from redblacknode import RedBlackNode

# 0 is black, 1 is red
class RedBlackTree:
    """This class is a representation of a red black tree. Here we initialize the RB Tree, and create a special
     node where we assign it to null and 0 represents the color of the node. We also set root to be equal to the
     null node """
    def __init__(self):
        self.null = RedBlackNode(None, 0) # inserts black root
        self.root = self.null

    def findNode(self, node=None, key=None):
        if node is None:
            node = self.root

        if node == self.null or key == node.key:
            return node

        if key < node.key:
            return self.findNode(node.left, key)
        else:
            return self.findNode(node.right, key)

    def insertNode(self, key):
        newNode = RedBlackNode(key, 1)
        # 1 is red
        self.insertHelper(newNode)
        self.balanceColor(newNode)

    def insertHelper(self, newNode):
        parent = None
        current = self.root

        while current != self.null:
            parent = current
            if newNode < current.key:
                current = current.left
            else:
                current = current.right

        newNode.parent = parent
        if parent is None:
            self.root = newNode
        elif newNode.key < parent.key:
            parent.left = newNode
        else:
            parent.right = newNode

        newNode.left = self.null
        newNode.right = self.null

    def balanceColor(self, node):
        while node.parent.color == 1:
            if node.parent == node.parent.parent.left:
                nodeUncle = node.parent.parent.right

                if nodeUncle == 1:
                    node.parent.color = 0
                    nodeUncle.color = 0
                    node.parent.parent.color = 1
                    node = node.parent.parent

                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.rotateLeft(node)

                    node.parent.color = 0
                    node.parent.parent.color = 1
                    self.rotateRight(node.parent.parent)
            else:
                if nodeUncle == 1:
                    node.parent.color = 0
                    nodeUncle.color = 0
                    node.parent.parent.color = 1
                    node = node.parent.parent

                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.rotateLeft(node)

                    node.parent.color = 0
                    node.parent.parent.color = 1
                    self.rotateRight(node.parent.parent)

        self.root.color = 0 # reset root to black

    def rotateLeft(self, node):
        rightChild = node.right
        node.right = rightChild.left

        if rightChild.left:
            rightChild.left.parent = node

        rightChild.left = node
        rightChild.parent = node.parent
        node.parent = rightChild

        self.updateParentChildNodes(rightChild.parent, node, rightChild)
        return rightChild

    def rotateRight(self, node):
        leftChild = node.left
        node.left = leftChild.right

        if leftChild.right:
            leftChild.right.parent = node

        leftChild.right = node
        leftChild.parent = node.parent
        node.parent = leftChild

        self.updateParentChildNodes(leftChild.parent, node, leftChild)
        return leftChild

    def returnRoot(self):
        return self.root

