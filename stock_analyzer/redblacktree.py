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
            print(f"Node: {node}, Item: {item}")
            return node
        if item < node.item and node.left:
            return self.findHelper(node.left, item)
        elif item > node.item and node.right:
            return self.findHelper(node.right, item)
        else:
            return None

    """the insert helper function carries all the functionality of inserting a new node into
    the RB Tree"""
    def insert(self, key):
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

        if node.parent == None:
            node.color = 0
            return
        if node.parent.parent == None:
            return

        self.balanceTree(node)

    def balanceTree(self, node):
        self.root.color = 0
        while node.parent and node.parent.color == 1:
            if node.parent == node.parent.parent.left:
                nodeUncle = node.parent.parent.left
                if nodeUncle and nodeUncle.color == 1:
                    node.parent.color = 0
                    nodeUncle.color = 0
                    node.parent.parent.color = 1
                    node = node.parent.parent

                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.rotateRight(node)

                    node.parent.color = 0
                    node.parent.parent.color = 1
                    self.rotateLeft(node.parent.parent)
            else:
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
            if node == self.root:
                break

        self.root.color = 0                                   # reset root to black

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
            node.praent.right = leftChild
        else:
            node.parent.left = leftChild
        leftChild.right = node
        node.parent = leftChild

    # def rotateLeftRight(self, node):
    #     node.left = self.rotateLeft(node.left)
    #     rotatedNode = self.rotateRight(node)
    #     return rotatedNode
    #
    # def rotateRightLeft(self, node):
    #     node.right = self.rotateRight(node.right)
    #     rotatedNode = self.rotateLeft(node)
    #     return rotatedNode

    def returnRoot(self):
        return self.root

    # def calculateTradingVolume(self, dateStart, dateEnd):


