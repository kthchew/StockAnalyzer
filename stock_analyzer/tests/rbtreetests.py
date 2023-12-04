import csv
import time
import unittest

from stock_analyzer.redblacktree import RedBlackTree
from stock_analyzer.marketday import MarketDay


class RBTreeTests(unittest.TestCase):
    def makeTree(self):
        tree = RedBlackTree()
        with open("test.csv") as file:
            reader = csv.reader(file)
            for r in reader:
                # skip header row
                if r[0] == "Date":
                    continue
                # column brand name is skipped
                data_point = MarketDay(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[9], r[10], r[11])
                tree.insert(data_point)
        return tree

    def testBasicInsertions(self):
        # example from slide deck 4
        tree = RedBlackTree()
        tree.insert(5)
        tree.insert(7)
        tree.insert(3)

        self.assertEqual(tree.root.item, 5)
        self.assertEqual(tree.root.color, 0)
        self.assertEqual(tree.root.left.color, 1)
        self.assertEqual(tree.root.right.color, 1)

    def testRunDateFilter(self):
        tree = self.makeTree()
        start = time.strptime("2023-09-19 00:00:00-04:00", "%Y-%m-%d %H:%M:%S%z")
        end = time.strptime("2023-09-21 00:00:00-04:00", "%Y-%m-%d %H:%M:%S%z")
        a = []

        def increment(item, arr):
            arr.append(item.country)

        tree.runDateFilter(start, end, increment, a)
        self.assertEqual(["usa", "usa", "usa"], a)


if __name__ == '__main__':
    unittest.main()
