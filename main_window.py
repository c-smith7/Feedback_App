import sys

from PyQt5 import QtGui, QtCore, Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import *
from main_widget import Window, Splashscreen


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.app_widget = Window()
        self.setCentralWidget(self.app_widget)
        self._createActions()
        self._createMenuBar()
        # config
        self.setWindowTitle('VIPKid Feedback App')
        self.resize(525, 725)
        self.app_icon = QtGui.QIcon()
        self.app_icon.addFile('pencil.png', QtCore.QSize(16, 16))
        self.setWindowIcon(self.app_icon)
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, QColor(235, 235, 235))
        self.setPalette(palette)

    def _createMenuBar(self):
        menuBar = self.menuBar()
        menuBar.setStyleSheet('QMenuBar {background: rgb(53, 53, 53); color: rgb(235, 235, 235);'
                              'border-bottom: 1px solid rgba(36, 36, 36, .5)}'
                              'QMenuBar::item:selected {background: rgb(115, 115, 115);}')
        file_menu = menuBar.addMenu('&File')
        file_menu.addAction(self.sign_out)
        edit_menu = menuBar.addMenu('&Edit')
        edit_menu.addAction(self.edit_signature)
        # submenu
        teacher_menu = edit_menu.addMenu('Teacher Templates')
        teacher_menu.addAction('Add Teachers...')
        teacher_menu.addAction('Remove Teachers...')
        help_menu = menuBar.addMenu('&Help')

    def _createActions(self):
        self.sign_out = QAction('&Log Out', self)
        self.edit_signature = QAction('Edit Feedback Signature', self)

    def closeEvent(self, event):
        try:
            self.app_widget.browser.quit()
        except:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = Splashscreen()
    window = MainWindow()
    window.show()
    splash.stop(window)
    app.exec()
