import csv
import time

from PySide6 import QtCore, QtWidgets, QtWebEngineWidgets

from stock_analyzer.map import testMap
from stock_analyzer.bplustree import BPlusTree
from stock_analyzer.btree import BTree
from stock_analyzer.marketday import MarketDay
from stock_analyzer.redblacktree import RedBlackTree


class CountryAction(QtWidgets.QWidgetAction):
    def toggleCountry(self, checked):
        if self.text() == "Select All":
            if checked:
                self.parent().selectedCountries = set([x.lower() for x in self.parent().allCountries])
                for item in self.parent().children():
                    item.setChecked(True)
            else:
                self.parent().selectedCountries.clear()
                for item in self.parent().children():
                    item.setChecked(False)
            print(self.parent().selectedCountries)
            return

        if self.text().lower() in self.parent().selectedCountries:
            self.parent().selectedCountries.remove(self.text().lower())
        else:
            self.parent().selectedCountries.add(self.text().lower())
        print(self.parent().selectedCountries)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.tree = None
        self.setWindowTitle("Stock Analyzer")

        self.countryFilter = QtWidgets.QMenu()
        self.countryFilter.setTitle("Country Filter")
        self.countryFilter.selectedCountries = set()
        self.countryFilter.allCountries = {"USA", "Japan", "Germany", "Switzerland", "Canada", "Netherlands", "France"}
        filterItem = CountryAction(self.countryFilter)
        filterItem.setText("Select All")
        filterItem.setCheckable(True)
        filterItem.setChecked(False)
        filterItem.triggered.connect(filterItem.toggleCountry)
        self.countryFilter.addAction(filterItem)
        for country in self.countryFilter.allCountries:
            filterItem = CountryAction(self.countryFilter)
            filterItem.setText(country)
            filterItem.setCheckable(True)
            filterItem.setChecked(False)
            filterItem.triggered.connect(filterItem.toggleCountry)
            self.countryFilter.addAction(filterItem)
        self.countryFilterButton = QtWidgets.QPushButton()
        self.countryFilterButton.setText("Country Filter")
        self.countryFilterButton.setMenu(self.countryFilter)

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

        self.bSettingsLabel = QtWidgets.QLabel()
        self.bSettingsLabel.setText("B/B+ Tree Settings (no effect on R/B tree)")
        self.bSettingsLabel.setSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum)
        self.nVal = QtWidgets.QSpinBox()
        self.nVal.setMinimum(1)
        self.nVal.setMaximum(100)
        self.nVal.setValue(5)
        self.nVal.setPrefix("Max Children: ")
        self.lVal = QtWidgets.QSpinBox()
        self.lVal.setMinimum(1)
        self.lVal.setMaximum(100)
        self.lVal.setValue(4)
        self.lVal.setPrefix("Max Items Per Node: ")

        self.makeTreeButton = QtWidgets.QPushButton("Build Tree")
        self.makeTreeButton.clicked.connect(self.timeCreateTree)

        self.makeMapButton = QtWidgets.QPushButton("Build Map")
        self.makeMapButton.clicked.connect(self.timeCreateMap)
        self.makeMapButton.setEnabled(False)

        self.webMapView = QtWebEngineWidgets.QWebEngineView()
        self.loadMap("intro.html")
        self.webMapView.setSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)

        self.mapTimerLabel = QtWidgets.QLabel()
        self.mapTimerLabel.setText("Time to create map: ?")

        self.treeTimerLabel = QtWidgets.QLabel()
        self.treeTimerLabel.setText("Time to create tree: ?")

        comboBoxLayout = QtWidgets.QHBoxLayout()
        comboBoxLayout.addWidget(self.countryFilterButton)
        comboBoxLayout.addWidget(self.highlightedFeature)
        comboBoxLayout.addWidget(self.dateFilterStart)
        comboBoxLayout.addWidget(self.dateFilterLabel)
        comboBoxLayout.addWidget(self.dateFilterEnd)
        comboBoxLayout.addWidget(self.dataStructure)

        bSettingsLayout = QtWidgets.QHBoxLayout()
        bSettingsLayout.addWidget(self.bSettingsLabel)
        bSettingsLayout.addWidget(self.nVal)
        bSettingsLayout.addWidget(self.lVal)

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
        self.layout.addLayout(bSettingsLayout)
        self.layout.addLayout(buttonLayout)
        self.layout.addWidget(self.webMapView)
        self.layout.addLayout(bottomLayout)

        self.container = QtWidgets.QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

    def loadMap(self, fileName):
        with open(fileName, 'r') as file:
            data = file.read()
        self.webMapView.setHtml(data)

    def timeCreateTree(self):
        """Times the tree creation and adds the time in seconds to the UI."""
        start = time.time()
        self.createTree()
        end = time.time()
        self.treeTimerLabel.setText("Time to create tree: " + str(round(end - start, 2)) + " sec")

    def createTree(self):
        match self.dataStructure.currentIndex():
            case 0:
                self.tree = BTree(self.nVal.value(), self.lVal.value())
            case 1:
                self.tree = BPlusTree(self.nVal.value(), self.lVal.value())
            case 2:
                self.tree = RedBlackTree()
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
        testMap()
        return "output_map.html"
