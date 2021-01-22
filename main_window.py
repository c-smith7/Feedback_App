import os
import sys
import time

from PyQt5 import QtGui, QtCore, Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import *
from main_widget import Window, Splashscreen


# noinspection PyArgumentList
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.app_widget = Window()
        self.setCentralWidget(self.app_widget)
        self._createActions()
        self._createMenuBar()
        self._connectActions()
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
        edit_menu.addAction(self.edit_teachers)
        help_menu = menuBar.addMenu('&Help')

    def _createActions(self):
        self.sign_out = QAction('&Log Out', self)
        self.edit_signature = QAction('Edit Feedback Signature', self)
        self.edit_teachers = QAction('&Edit Liked Teachers', self)

    def _connectActions(self):
        self.sign_out.triggered.connect(self.logout)
        self.edit_teachers.triggered.connect(self.teacher_list_widget)

    def closeEvent(self, event):
        try:
            self.app_widget.browser.quit()
        except:
            pass

    def logout(self):
        """slot of logout option in menubar"""
        if os.path.exists('cookie'):
            os.remove('cookie')
            self.app_widget.login_button_counter = 0
            msgBox = QMessageBox(self)
            msgBox.setWindowModality(QtCore.Qt.WindowModal)
            msgBox.setWindowFlag(QtCore.Qt.ToolTip)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText('Successfully Logged Out!')
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.setDefaultButton(QMessageBox.Ok)
            msgBox.setStyleSheet(
                'QMessageBox {background-color: rgb(53, 53, 53); border-top: 25px solid rgb(115, 115, 115);'
                'border-left: 1px solid rgb(115, 115, 115); border-right: 1px solid rgb(115, 115, 115);'
                'border-bottom: 1px solid rgb(115, 115, 115)}'
                'QLabel {color: rgb(235, 235, 235); padding-top: 30px}'
                'QPushButton {background-color: rgb(115, 115, 115); color: rgb(235, 235, 235);'
                'border-radius: 11px; padding: 5px; min-width: 5em}'
                'QPushButton:pressed {background-color: rgb(53, 53, 53)}'
                'QPushButton:hover {border: 0.5px solid white}')
            msgBox.exec()
        else:
            msgBox = QMessageBox(self)
            msgBox.setWindowModality(QtCore.Qt.WindowModal)
            msgBox.setWindowFlag(QtCore.Qt.ToolTip)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText('Already Logged Out!')
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.setDefaultButton(QMessageBox.Ok)
            msgBox.setStyleSheet(
                'QMessageBox {background-color: rgb(53, 53, 53); border-top: 25px solid rgb(115, 115, 115);'
                'border-left: 1px solid rgb(115, 115, 115); border-right: 1px solid rgb(115, 115, 115);'
                'border-bottom: 1px solid rgb(115, 115, 115)}'
                'QLabel {color: rgb(235, 235, 235); padding-top: 30px}'
                'QPushButton {background-color: rgb(115, 115, 115); color: rgb(235, 235, 235);'
                'border-radius: 11px; padding: 5px; min-width: 5em}'
                'QPushButton:pressed {background-color: rgb(53, 53, 53)}'
                'QPushButton:hover {border: 0.5px solid white}')
            msgBox.exec()

    def teacher_list_widget(self):
        dialog = QDialog(self, QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        dialog.setWindowTitle('VIPKid Feedback App')
        dialog.setMinimumWidth(450)
        # widget layout
        layout = QVBoxLayout()
        # Instructions
        instructions = QLabel()
        instructions.setWordWrap(True)
        instructions.setText('<h3>Liked Teachers List</h3>'
                             '<ul style="margin-left: 10px; -qt-list-indent: 0;">'
                             '<li>Add teachers by using the <b>Add Teacher</b> button below.</li>'
                             '<li>Remove teachers by right clicking on a teacher name and selecting <b>Remove</b>.</li></ul>')
        layout.addWidget(instructions)
        layout.addSpacing(9)
        # List Widget
        list_widget = QListWidget(dialog)
        list_widget.addItems(self.app_widget.valid_teachers)
        layout.addWidget(list_widget)
        # Add button
        add_teacher_button = QPushButton('Add Teacher', dialog)
        add_teacher_button.setMaximumWidth(150)
        layout.addWidget(add_teacher_button)
        layout.addSpacing(7)
        # Reminder to user
        reminder = QLabel()
        reminder.setWordWrap(True)
        reminder.setStyleSheet('Font: 9px')
        reminder.setText('<i>Remember, it is best to add teachers who have '
                         'feedback templates that are compatible with VIPKid Feedback App. '
                         'Head to the <b>Help Menu</b> for more details on what templates are compatible.</i>')
        layout.addWidget(reminder)
        dialog.setLayout(layout)
        # slots
        list_widget.itemClicked.connect(self.TestClicked)
        # add_teacher_button.clicked.connect()
        dialog.exec()

    def TestClicked(self, item):
        print(item.text() + ' selected')

    # def add_teacher(self):


if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = Splashscreen()
    window = MainWindow()
    window.show()
    splash.stop(window)
    app.exec()