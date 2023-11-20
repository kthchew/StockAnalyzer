from PySide6 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Stock Analyzer")

        self.countryFilter = QtWidgets.QComboBox()
        self.countryFilter.setPlaceholderText("Country Filter")

        self.highlightedFeature = QtWidgets.QComboBox()
        self.highlightedFeature.setPlaceholderText("Highlighted Feature")

        self.dateFilter = QtWidgets.QComboBox()
        self.dateFilter.setPlaceholderText("Date Filter")

        self.dataStructure = QtWidgets.QComboBox()
        self.dataStructure.addItems(["B Tree", "B+ Tree", "Red-Black Tree"])

        self.webMapView = QtWebEngineWidgets.QWebEngineView()
        self.webMapView.load(QtCore.QUrl("https://example.com"))

        self.timerLabel = QtWidgets.QLabel()
        self.timerLabel.setText("Time to create map: ?")

        comboBoxLayout = QtWidgets.QHBoxLayout()
        comboBoxLayout.addWidget(self.countryFilter)
        comboBoxLayout.addWidget(self.highlightedFeature)
        comboBoxLayout.addWidget(self.dateFilter)
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
