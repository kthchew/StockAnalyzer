import csv
import time

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
        self.highlightedFeature.addItems(["Trading Volume", "Gains/Losses"])

        self.dateFilterStart = QtWidgets.QDateEdit(QtCore.QDate(2022, 1, 1))

        self.dateFilterLabel = QtWidgets.QLabel()
        self.dateFilterLabel.setText("to")
        shrink = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum)
        self.dateFilterLabel.setSizePolicy(shrink)

        self.dateFilterEnd = QtWidgets.QDateEdit(QtCore.QDate(2023, 1, 1))

        self.dataStructure = QtWidgets.QComboBox()
        self.dataStructure.addItems(["B Tree", "B+ Tree", "Red-Black Tree"])
        self.dataStructure.setPlaceholderText("Data Structure")

        self.makeTreeButton = QtWidgets.QPushButton("Build Tree")
        self.makeTreeButton.clicked.connect(self.timeCreateTree)

        self.makeMapButton = QtWidgets.QPushButton("Build Map")
        self.makeMapButton.clicked.connect(self.timeCreateMap)
        self.makeMapButton.setEnabled(False)

        self.webMapView = QtWebEngineWidgets.QWebEngineView()
        self.webMapView.load(QtCore.QUrl("https://example.com"))

        self.mapTimerLabel = QtWidgets.QLabel()
        self.mapTimerLabel.setText("Time to create map: ?")

        self.treeTimerLabel = QtWidgets.QLabel()
        self.treeTimerLabel.setText("Time to create tree: ?")

        comboBoxLayout = QtWidgets.QHBoxLayout()
        comboBoxLayout.addWidget(self.countryFilter)
        comboBoxLayout.addWidget(self.highlightedFeature)
        comboBoxLayout.addWidget(self.dateFilterStart)
        comboBoxLayout.addWidget(self.dateFilterLabel)
        comboBoxLayout.addWidget(self.dateFilterEnd)
        comboBoxLayout.addWidget(self.dataStructure)

        buttonLayout = QtWidgets.QHBoxLayout()
        buttonLayout.addWidget(self.makeTreeButton)
        buttonLayout.addWidget(self.makeMapButton)

        bottomLayout = QtWidgets.QHBoxLayout()
        spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        bottomLayout.addSpacerItem(spacer)
        bottomLayout.addWidget(self.mapTimerLabel)
        bottomLayout.addWidget(self.treeTimerLabel)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(comboBoxLayout)
        self.layout.addLayout(buttonLayout)
        self.layout.addWidget(self.webMapView)
        self.layout.addLayout(bottomLayout)

        self.container = QtWidgets.QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

    def loadMap(self, url):
        self.webMapView.load(url)

    def timeCreateTree(self):
        """Times the tree creation and adds the time in seconds to the UI."""
        start = time.time()
        self.createTree()
        end = time.time()
        self.treeTimerLabel.setText("Time to create tree: " + str(round(end - start, 2)) + " sec")

    def createTree(self):
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
                # skip header row
                if r[0] == "Date":
                    continue
                # column brand name is skipped
                dataPoint = MarketDay(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[9], r[10], r[11])
                self.tree.insert(dataPoint)

        self.makeMapButton.setEnabled(True)

    def timeCreateMap(self):
        start = time.time()
        url = self.createMap()
        self.loadMap(url)
        end = time.time()
        self.mapTimerLabel.setText("Time to create map: " + str(round(end - start, 2)) + " sec")

    def createMap(self):
        # TODO: actually create map here
        return "https://www.example.com"
