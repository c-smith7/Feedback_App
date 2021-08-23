import sys
from PyQt5 import QtCore, Qt
from PyQt5.QtWidgets import QMessageBox, QApplication
from selenium.common.exceptions import SessionNotCreatedException

from app.main_widget import Splashscreen
from app.main_window import MainWindow

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        splash = Splashscreen()
        window = MainWindow()
        window.show()
        splash.stop(window)
        app.exec()
    except SessionNotCreatedException as e:
        msgBox = QMessageBox()
        msgBox.setWindowModality(QtCore.Qt.WindowModal)
        msgBox.setWindowFlags(QtCore.Qt.ToolTip | QtCore.Qt.WindowStaysOnTopHint)
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setTextFormat(QtCore.Qt.RichText)
        msgBox.setText("You need to update Chromedriver!<br><a href='https://chromedriver.chromium.org/downloads'>UPDATE HERE</a>")
        msgBox.setDetailedText(str(e))
        msgBox.setStandardButtons(QMessageBox.Cancel)
        msgBox.setStyleSheet(
            'QMessageBox {background-color: rgb(53, 53, 53); border-top: 1px solid rgb(115, 115, 115);'
            'border-left: 1px solid rgb(115, 115, 115); border-right: 1px solid rgb(115, 115, 115);'
            'border-bottom: 1px solid rgb(115, 115, 115); font-family: "Segoe UI";}'
            'QLabel {color: rgb(235, 235, 235); padding-top: 10px; font-family: "Segoe UI";}'
            'QPushButton {background-color: rgb(115, 115, 115); color: rgb(235, 235, 235);'
            'border-radius: 11px; padding: 5px; min-width: 5em; font-family: "Segoe UI"; font-size: 12px;}'
            'QPushButton:pressed {background-color: rgb(53, 53, 53)}'
            'QPushButton:hover {border: 0.5px solid white}')
        msgBox.exec()
    except Exception as e:
        msgBox = QMessageBox()
        msgBox.setWindowModality(QtCore.Qt.WindowModal)
        msgBox.setWindowFlags(QtCore.Qt.ToolTip | QtCore.Qt.WindowStaysOnTopHint)
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText('Unknown error..')
        msgBox.setDetailedText(str(e))
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.setDefaultButton(QMessageBox.Ok)
        msgBox.setStyleSheet(
            'QMessageBox {background-color: rgb(53, 53, 53); border-top: 1px solid rgb(115, 115, 115);'
            'border-left: 1px solid rgb(115, 115, 115); border-right: 1px solid rgb(115, 115, 115);'
            'border-bottom: 1px solid rgb(115, 115, 115); font-family: "Segoe UI";}'
            'QLabel {color: rgb(235, 235, 235); padding-top: 10px; font-family: "Segoe UI";}'
            'QPushButton {background-color: rgb(115, 115, 115); color: rgb(235, 235, 235);'
            'border-radius: 11px; padding: 5px; min-width: 5em; font-family: "Segoe UI"; font-size: 12px;}'
            'QPushButton:pressed {background-c'
            'color: rgb(53, 53, 53)}'
            'QPushButton:hover {border: 0.5px solid white}')
        msgBox.exec()

