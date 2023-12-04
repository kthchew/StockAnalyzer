import csv
import time

from PySide6.QtCore import QRunnable, Slot, QObject, Signal

from stock_analyzer.bplustree import BPlusTree
from stock_analyzer.btree import BTree
from stock_analyzer.marketday import MarketDay
from stock_analyzer.redblacktree import RedBlackTree


class Signals(QObject):
    treeCreated = Signal(float, float)


class TreeWorker(QRunnable):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.signals = Signals()

    @Slot()
    def run(self):
        """
        Runs and times a creation of a tree with the 'data.csv' file. Emits a signal with the start and end times once
        complete.
        """
        start = time.time()
        match self.window.dataStructure.currentIndex():
            case 0:
                self.window.tree = BTree(self.window.nVal.value(), self.window.lVal.value())
            case 1:
                self.window.tree = BPlusTree(self.window.nVal.value(), self.window.lVal.value())
            case 2:
                self.window.tree = RedBlackTree()
            case _:
                return

        with open("data.csv") as file:
            reader = csv.reader(file)
            for r in reader:
                # skip header row
                if r[0] == "Date":
                    continue
                # column brand name is skipped
                dataPoint = MarketDay(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[9], r[10], r[11])
                self.window.tree.insert(dataPoint)

        end = time.time()
        self.signals.treeCreated.emit(start, end)


