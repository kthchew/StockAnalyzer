import csv
import unittest

from stock_analyzer.redblacktree import RedBlackTree
from stock_analyzer.marketday import MarketDay

class RBTreeTests(unittest.TestCase):
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

        result = tree.find(dataPoint)
        self.assertIsNotNone(result, f"expected {dataPoint} to be in the tree")

        result = tree.find(data_point2)
        self.assertIsNone(result, f"expected {data_point2} to not be in the tree")

        print("finished with tests")


if __name__ == '__main__':
    unittest.main()