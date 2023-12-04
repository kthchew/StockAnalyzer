import time

from PySide6 import QtCore, QtWidgets, QtWebEngineWidgets

from stock_analyzer.map import Map
from stock_analyzer.treeworker import TreeWorker


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
            return

        if self.text().lower() in self.parent().selectedCountries:
            self.parent().selectedCountries.remove(self.text().lower())
        else:
            self.parent().selectedCountries.add(self.text().lower())


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.tree = None
        self.setWindowTitle("Stock Analyzer")

        self.countryFilter = QtWidgets.QMenu()
        self.countryFilter.setTitle("Country Filter")
        self.countryFilter.allCountries = {"USA", "Japan", "Germany", "Switzerland", "Canada", "Netherlands", "France"}
        self.countryFilter.selectedCountries = set([x.lower() for x in self.countryFilter.allCountries])
        filterItem = CountryAction(self.countryFilter)
        filterItem.setText("Select All")
        filterItem.setCheckable(True)
        filterItem.setChecked(True)
        filterItem.triggered.connect(filterItem.toggleCountry)
        self.countryFilter.addAction(filterItem)
        for country in self.countryFilter.allCountries:
            filterItem = CountryAction(self.countryFilter)
            filterItem.setText(country)
            filterItem.setCheckable(True)
            filterItem.setChecked(True)
            filterItem.triggered.connect(filterItem.toggleCountry)
            self.countryFilter.addAction(filterItem)
        self.countryFilterButton = QtWidgets.QPushButton()
        self.countryFilterButton.setText("Country Filter")
        self.countryFilterButton.setMenu(self.countryFilter)

        self.highlightedFeature = QtWidgets.QComboBox()
        self.highlightedFeature.setPlaceholderText("Highlighted Feature")
        self.highlightedFeature.addItems(["Highs (Average)", "Lows (Average)", "Trading Volume (Total)"])
        self.featureError = QtWidgets.QErrorMessage()
        self.featureError.setWindowTitle("No Feature Selected")

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
        self.makeTreeButton.clicked.connect(self.startCreateTree)

        self.makeMapButton = QtWidgets.QPushButton("Build Map")
        self.makeMapButton.clicked.connect(self.timeCreateMap)
        self.makeMapButton.setEnabled(False)

        self.webMapView = QtWebEngineWidgets.QWebEngineView()
        self.loadMap("intro.html")
        self.webMapView.setSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding,
                                      QtWidgets.QSizePolicy.Policy.MinimumExpanding)

        self.loadingLabel = QtWidgets.QLabel()
        self.loadingLabel.setText("Please wait, making tree...")
        self.loadingLabel.setVisible(False)

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
        bottomLayout.addWidget(self.loadingLabel)
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

        self.threadpool = QtCore.QThreadPool()

    def loadMap(self, fileName):
        with open(fileName, 'r') as file:
            data = file.read()
        self.webMapView.setHtml(data)

    def endCreateTree(self, start: float, end: float):
        """
        Responds when the background thread finishes creating the tree. Updates the UI to show the time it took.
        :param start: The start time
        :param end: The end time
        :return: None
        """
        self.treeTimerLabel.setText("Time to create tree: " + str(round(end - start, 2)) + " sec")
        self.makeMapButton.setEnabled(True)
        self.makeTreeButton.setEnabled(True)
        self.loadingLabel.setVisible(False)

    def startCreateTree(self):
        """
        Begins a new thread to create the tree.
        :return: None
        """
        self.makeMapButton.setDisabled(True)
        self.makeTreeButton.setDisabled(True)
        self.loadingLabel.setVisible(True)
        treeWorker = TreeWorker(self)
        treeWorker.signals.treeCreated.connect(self.endCreateTree)
        self.threadpool.start(treeWorker)

    def timeCreateMap(self):
        if self.highlightedFeature.currentIndex() == -1:
            self.featureError.showMessage("Please select a feature before building the map.")
            return

        start = time.time()
        url = self.createMap()
        self.loadMap(url)
        end = time.time()
        self.mapTimerLabel.setText("Time to create map: " + str(round(end - start, 2)) + " sec")

    def createMap(self):
        startDate = self.dateFilterStart.date().toPython().timetuple()
        endDate = self.dateFilterEnd.date().toPython().timetuple()
        vols, highs, lows = self.calculateStats(startDate, endDate)
        Map(highs, lows, vols, self.highlightedFeature.currentIndex())
        return "index.html"

    def calculateStats(self, dateStart, dateEnd):
        """Returns total volumes, average high, average low for each country in a dictionary."""
        volumes = dict()
        highs = dict()
        lows = dict()
        count = [0]

        def updateVolume(item, vols: dict, his: dict, los: dict, count: list, countries: set):
            if item.country not in countries:
                return
            count[0] += 1
            if item.country in vols.keys():
                vols[item.country] += item.vol
                his[item.country] += item.high
                los[item.country] += item.low
            else:
                vols[item.country] = item.vol
                his[item.country] = item.high
                los[item.country] = item.low

        self.tree.runDateFilter(dateStart, dateEnd, updateVolume, volumes, highs, lows, count, self.countryFilter.selectedCountries)
        for key in highs:
            highs[key] /= count[0]
        for key in lows:
            lows[key] /= count[0]
        return volumes, highs, lows
