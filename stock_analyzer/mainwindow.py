import csv

from PySide6 import QtCore, QtWidgets, QtWebEngineWidgets

from stock_analyzer.btree import BTree
from stock_analyzer.marketday import MarketDay


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.tree = None
        self.setWindowTitle("Stock Analyzer")

        self.countryFilter = QtWidgets.QComboBox()
        self.countryFilter.setPlaceholderText("Country Filter")

        self.highlightedFeature = QtWidgets.QComboBox()
        self.highlightedFeature.setPlaceholderText("Highlighted Feature")

        self.dateFilterStart = QtWidgets.QDateEdit(QtCore.QDate(2022, 1, 1))

        self.dateFilterLabel = QtWidgets.QLabel()
        self.dateFilterLabel.setText("to")
        shrink = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum)
        self.dateFilterLabel.setSizePolicy(shrink)


        self.dateFilterEnd = QtWidgets.QDateEdit(QtCore.QDate(2023, 1, 1))

        self.dataStructure = QtWidgets.QComboBox()
        self.dataStructure.addItems(["B Tree", "B+ Tree", "Red-Black Tree"])

        self.webMapView = QtWebEngineWidgets.QWebEngineView()
        self.webMapView.load(QtCore.QUrl("https://example.com"))

        self.timerLabel = QtWidgets.QLabel()
        self.timerLabel.setText("Time to create map: ?")

        comboBoxLayout = QtWidgets.QHBoxLayout()
        comboBoxLayout.addWidget(self.countryFilter)
        comboBoxLayout.addWidget(self.highlightedFeature)
        comboBoxLayout.addWidget(self.dateFilterStart)
        comboBoxLayout.addWidget(self.dateFilterLabel)
        comboBoxLayout.addWidget(self.dateFilterEnd)
        comboBoxLayout.addWidget(self.dataStructure)

        bottomLayout = QtWidgets.QHBoxLayout()
        spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        bottomLayout.addSpacerItem(spacer)
        bottomLayout.addWidget(self.timerLabel)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(comboBoxLayout)
        self.layout.addWidget(self.webMapView)
        self.layout.addLayout(bottomLayout)

        self.container = QtWidgets.QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

    def loadMap(self, url):
        self.webMapView.load(url)

    def createMap(self):
        match self.dataStructure.currentIndex():
            case 0:
                self.tree = BTree(5, 4)
            # case 1:
            #     self.tree = BPlusTree(5, 4)
            # case 2:
            #     self.tree = RBTree()
            case _:
                return

        with open("data.csv") as file:
            reader = csv.reader(file)
            for r in reader:
                # some columns (stock splits, brand name) are skipped
                dataPoint = MarketDay(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[9], r[10], r[11])
                self.tree.insert(dataPoint)
