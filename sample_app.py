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
        self._createActions()
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
        self.save_action = QAction("&Save", self)
        self.exit_action = QAction("&Exit", self)
        self.copy_action = QAction("&Copy", self)
        self.paste_action = QAction("&Paste", self)
        self.cut_action = QAction("&Cut", self)
        self.help_content_action = QAction("&Help Content", self)
        self.about_action = QAction("&About", self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
