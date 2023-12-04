import csv
import time
import unittest

from stock_analyzer.btree import BTree
from stock_analyzer.marketday import MarketDay


class BTreeTests(unittest.TestCase):
    def makeTree(self):
        tree = BTree(3, 2)
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
        self.assertEqual(tree.root.childCount(), 3)
        self.assertEqual(tree.root.children[0].items, [3, 4])
        self.assertEqual(tree.root.children[1].items, [6])
        self.assertEqual(tree.root.children[2].items, [11, 17])

        tree.insert(1)
        self.assertEqual(tree.root.items, [5])
        self.assertEqual(tree.root.childCount(), 2)
        self.assertEqual(tree.root.children[0].items, [3])
        self.assertEqual(tree.root.children[1].items, [7])
        self.assertEqual(tree.root.children[0].children[0].items, [1])
        self.assertEqual(tree.root.children[0].children[1].items, [4])
        self.assertEqual(tree.root.children[1].children[0].items, [6])
        self.assertEqual(tree.root.children[1].children[1].items, [11, 17])

    def test_find(self):
        tree = self.makeTree()

        data_point = MarketDay("2023-09-20 00:00:00-04:00", "564.3499755859375",
                              "569.219970703125", "562.6599731445312", "563.8300170898438",
                              "1311500.0", "0.0", "0.0", "COST", "retail",
                              "usa")
        data_point2 = MarketDay("2023-06-23 00:00:00-04:00", "21.71629018950936",
                               "26.01165263931803","25.302781633056032", "25.529226303100582",
                               "3230400.0", "0.0", "0.0", "FL", "footwear", "usa")

        self.assertTrue(tree.find(data_point))
        self.assertFalse(tree.find(data_point2))

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
