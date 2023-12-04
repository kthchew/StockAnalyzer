import sys
from PySide6 import QtWidgets

from stock_analyzer.mainwindow import MainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
