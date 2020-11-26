import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import *


# https://realpython.com/python-menus-toolbars/


class Window(QMainWindow):
    """Main Window"""
    def __init__(self, parent=None):
        """Initializer"""
        super().__init__(parent)
        self.setWindowTitle('Sample GUI')
        self.setWindowIcon(QtGui.QIcon('vipkid.png'))
        self.resize(600, 900)
        self.centralWidget = QLabel('Hello, World')
        self.centralWidget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(self.centralWidget)
        self._createActions()
        self._createMenuBar()
        self._createContextMenu()
        self._connectActions()

    # def _window_widget(self):

    def _createMenuBar(self):
        menu_bar = self.menuBar()
        # File menu and actions
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)
        # Edit menu and actions
        edit_menu = menu_bar.addMenu('&Edit')
        edit_menu.addAction(self.copy_action)
        edit_menu.addAction(self.paste_action)
        edit_menu.addAction(self.cut_action)
        edit_menu.addAction(self.select_action)
        edit_menu.addSeparator()
        # add submenu in Edit menu
        find_menu = edit_menu.addMenu('Find and Replace')
        find_menu.addAction('Find...')
        find_menu.addAction('Replace...')
        # Help Menu and actions
        help_menu = menu_bar.addMenu('&Help')
        help_menu.addAction(self.help_content_action)
        help_menu.addAction(self.about_action)

    def _createContextMenu(self):
        self.centralWidget.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.centralWidget.addAction(self.copy_action)
        self.centralWidget.addAction(self.paste_action)
        self.centralWidget.addAction(self.cut_action)

    # def _createToolBars(self):
    #     file_toolbar = self.addToolBar('File')
    #     edit_toolbar = self.addToolBar('Edit')

    def _createActions(self):
        self.new_action = QAction('&New', self)
        self.open_action = QAction('&Open...', self)
        self.save_action = QAction("&Save", self)
        self.exit_action = QAction("&Exit", self)
        self.copy_action = QAction("&Copy", self)
        self.paste_action = QAction("&Paste", self)
        self.cut_action = QAction("&Cut", self)
        self.select_action = QAction("&Select All", self)
        self.copy_action.setShortcut(QKeySequence.Copy)
        self.paste_action.setShortcut(QKeySequence.Paste)
        self.cut_action.setShortcut(QKeySequence.Cut)
        self.help_content_action = QAction("&Help Content", self)
        self.about_action = QAction("&About", self)

    def copyContent(self):
        self.centralWidget.setText("<b>Edit > Copy</b> clicked")

    def pasteContent(self):
        self.centralWidget.setText("<b>Edit > Pate</b> clicked")

    def cutContent(self):
        self.centralWidget.setText("<b>Edit > Cut</b> clicked")

    def _connectActions(self):
        self.copy_action.triggered.connect(self.copyContent)
        self.paste_action.triggered.connect(self.pasteContent)
        self.cut_action.triggered.connect(self.cutContent)
        self.exit_action.triggered.connect(self.close)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
