import csv
import unittest
import sys
print(sys.path)

from redblacktree import RedBlackTree
from marketday import MarketDay

class RBTreeTests(unittest.TestCase):
    def testBasicInsertions(self):
        # example from slide deck 4
        tree = RedBlackTree()
        tree.insert(5)
        tree.insert(7)
        tree.insert(3)
        # tree.insert(11)
        # tree.insert(6)
        # tree.insert(4)
        # tree.insert(17)

        self.assertEqual(tree.root.key, 5)
        self.assertEqual(tree.root.color, 0)
        self.assertEqual(tree.root.left.color, 1)
        self.assertEqual(tree.root.right.color, 1)

    def testFind(self):
        tree = RedBlackTree()
        with open("test.csv") as file:
            reader = csv.reader(file)
            for r in reader:
                # skip header row
                if r[0] == "Date":
                    continue
                # column brand name is skipped
                dataPoint = MarketDay(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[9], r[10], r[11])
                tree.insert(dataPoint)

        dataPoint = MarketDay("2023-09-20 00:00:00-04:00", "564.3499755859375",
                               "569.219970703125", "562.6599731445312", "563.8300170898438",
                               "1311500.0", "0.0", "0.0", "COST", "retail",
                               "usa")

        data_point2 = MarketDay("2023-06-23 00:00:00-04:00", "21.71629018950936",
                                "26.01165263931803", "25.302781633056032", "25.529226303100582",
                                "3230400.0", "0.0", "0.0", "FL", "footwear", "usa")

        self.assertTrue(tree.find(dataPoint))
        self.assertFalse(tree.find(data_point2))


if __name__ == '__main__':
    unittest.main()