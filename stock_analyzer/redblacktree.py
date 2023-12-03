from redblacknode import RedBlackNode
from marketday import MarketDay

# 0 is black, 1 is red
class RedBlackTree:
    """This class is a representation of a red black tree. Here we initialize the RB Tree, and create a special
     node where we assign it to null and 0 represents the color of the node. We also set root to be equal to the
     null node """
    def __init__(self):
        self.null = RedBlackNode(None, 0) # inserts black root (0)
        self.root = self.null

    def calculateTradingVolumes(self, dateStart, dateEnd):
        result = {}
        self.calculateTradingVolumesHelper(self.root, dateStart, dateEnd, result)
        return result

    def calculateTradingVolumesHelper(self, node, dateStart, dateEnd, result):
        if node == self.null:
            return

        """checking to see here if the date is within the range add it"""
        if dateStart <= node.item.date <= dateEnd:
            country = node.item.country
            result[country] = result.get(country, 0.0) + node.item.vol

        self.calculateTradingVolumesHelper(node.left, dateStart, dateEnd, result)
        self.calculateTradingVolumesHelper(node.right, dateStart, dateEnd, result)
        #  calculates the left and right subtrees
    """executes the find function that locates the date within the RB tree"""
    def find(self, item):
        return self.findHelper(self.root, item)

    """serves as the helper function that helps locate a given date in the RB Tree"""
    def findHelper(self, node, item):
        if node is None or item == node.item:
            return node
        if item < node.item and node.left:
            return self.findHelper(node.left, item)
        elif item > node.item and node.right:
            return self.findHelper(node.right, item)
        else:
            return None

    """main function that executes helper functions and inserts a node into the tree, from here we also 
    balance the tree color if it's unbalanced (change red to black, etc, and guarantee that the root is black)"""
    def insert(self, item):
        newNode = RedBlackNode(item, 1)  # 1 is red
        self.insertHelper(newNode)
        self.balanceColor(newNode)

    """the insert helper function carries all the functionality of inserting a new node into
    the RB Tree"""

    def insertHelper(self, newNode):
        parent = None
        current = self.root

        while current and current != self.null:
            parent = current
            if newNode.item < current.item:
                current = current.left
            else:
                current = current.right

        newNode.parent = parent
        if parent is None:
            self.root = newNode
        elif parent and newNode.item < parent.item:
            parent.left = newNode
        elif parent:
            parent.right = newNode

        newNode.left = self.null
        newNode.right = self.null

    def balanceColor(self, node):
        while node.parent and node.parent.color == 1:
            if node.parent == node.parent.parent.left:

                nodeUncle = node.parent.parent.right
                if nodeUncle and nodeUncle.color == 1:
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
                nodeUncle = node.parent.parent.left
                if nodeUncle and nodeUncle.color == 1:
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

    def updateParentChildNodes(self, parent, node, child):
        if parent:
            if parent.left == node:
                parent.left = child
            else:
                parent.right = child

        if child:
            child.parent = parent

    def rotateLeft(self, node):
        rightChild = node.right

        if rightChild:
            node.right = rightChild.left

            if rightChild.left:
                rightChild.left.parent = node

            rightChild.left = node
            rightChild.parent = node.parent
            node.parent = rightChild

            self.updateParentChildNodes(rightChild.parent, node, rightChild)
            return rightChild

        return node

    def rotateRight(self, node):
        leftChild = node.left

        if leftChild:
            node.left = leftChild.right

            if leftChild.right:
                leftChild.right.parent = node

            leftChild.right = node
            leftChild.parent = node.parent
            node.parent = leftChild

            self.updateParentChildNodes(leftChild.parent, node, leftChild)
            return leftChild

        return node

    def returnRoot(self):
        return self.root

    # def calculateTradingVolume(self, dateStart, dateEnd):


