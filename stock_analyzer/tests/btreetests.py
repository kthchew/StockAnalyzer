import unittest

from stock_analyzer.btree import BTree


class BTreeTests(unittest.TestCase):
    def test_basic_insertions(self):
        # example from slide deck 4
        tree = BTree(3, 2)
        tree.insert(5)
        tree.insert(7)
        tree.insert(3)
        tree.insert(11)
        tree.insert(6)
        tree.insert(4)
        tree.insert(17)

        self.assertEqual(tree.root.items, [5, 7])
        self.assertEqual(tree.root.child_count(), 3)
        self.assertEqual(tree.root.children[0].items, [3, 4])
        self.assertEqual(tree.root.children[1].items, [6])
        self.assertEqual(tree.root.children[2].items, [11, 17])

        tree.insert(1)
        self.assertEqual(tree.root.items, [5])
        self.assertEqual(tree.root.child_count(), 2)
        self.assertEqual(tree.root.children[0].items, [3])
        self.assertEqual(tree.root.children[1].items, [7])
        self.assertEqual(tree.root.children[0].children[0].items, [1])
        self.assertEqual(tree.root.children[0].children[1].items, [4])
        self.assertEqual(tree.root.children[1].children[0].items, [6])
        self.assertEqual(tree.root.children[1].children[1].items, [11, 17])


if __name__ == '__main__':
    unittest.main()
