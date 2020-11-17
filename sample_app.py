import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


# https://realpython.com/python-menus-toolbars/


class Window(QMainWindow):
    """Main Window"""
    def __init__(self, parent=None):
        """Initializer"""
        super().__init__(parent)
        self.setWindowTitle('Sample GUI')
        self.setWindowIcon(QtGui.QIcon('vipkid.png'))
        self.resize(400, 200)
        self.centralWidget = QLabel('Hello, World')
        self.centralWidget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(self.centralWidget)
        self._createMenuBar()
        self._createToolBars()

    def _createMenuBar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        edit_menu = menu_bar.addMenu('&Edit')
        help_menu = menu_bar.addMenu('&Help')

    def _createToolBars(self):
        file_toolbar = self.addToolBar('File')
        edit_toolbar = self.addToolBar('Edit')
        help_toolbar = self.addToolBar('Help')

    def _createActions(self):
        self.new_action = QAction('&New', self)
        self.open_action = QAction ('&Open...', self)
        self.saveAction = QAction("&Save", self)
        self.exitAction = QAction("&Exit", self)
        self.copyAction = QAction("&Copy", self)
        self.pasteAction = QAction("&Paste", self)
        self.cutAction = QAction("&Cut", self)
        self.helpContentAction = QAction("&Help Content", self)
        self.aboutAction = QAction("&About", self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
