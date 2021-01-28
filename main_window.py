import json
import os
import sys
import time

from PyQt5 import QtGui, QtCore, Qt
from PyQt5.QtCore import QObject, pyqtSignal, QRunnable, pyqtSlot, QThreadPool
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import *
from main_widget import Window, Splashscreen


class TeachersModel(QtCore.QAbstractListModel):
    def __init__(self, *args, teachers=None, **kwargs):
        super(TeachersModel, self).__init__(*args, **kwargs)
        self.teachers_list = teachers or []

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            text = self.teachers_list[index.row()]
            return text

    def rowCount(self, index):
        return len(self.teachers_list)


# noinspection PyArgumentList
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.app_widget = Window()
        self.setCentralWidget(self.app_widget)
        self._createActions()
        self._createMenuBar()
        self._connectActions()
        # Liked Teachers list
        self.model = TeachersModel()
        self.load_liked_teachers()
        # window config
        self.setWindowTitle('VIPKid Feedback App')
        self.resize(525, 725)
        self.app_icon = QtGui.QIcon()
        self.app_icon.addFile('pencil.png', QtCore.QSize(16, 16))
        self.setWindowIcon(self.app_icon)
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, QColor(235, 235, 235))
        self.setPalette(palette)
        # main window threadpool
        self.main_window_threadpool = QThreadPool()

    def _createMenuBar(self):
        menuBar = self.menuBar()
        menuBar.setStyleSheet('QMenuBar {background: rgb(53, 53, 53); border-bottom: 1px solid rgba(36, 36, 36, .5);}'
                              'QMenuBar::item {color: rgb(235, 235, 235); font-size: 11px; font-family: "Segoe UI";}'
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
        self.edit_signature.triggered.connect(self.teacher_signature_widget)

    def closeEvent(self, event):
        try:
            self.app_widget.browser.quit()
        except:
            pass

# LOGOUT menubar function
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
            msgBox.setStyleSheet('QMessageBox {background-color: rgb(53, 53, 53); border-top: 25px solid rgb(115, 115, 115);'
                                 'border-left: 1px solid rgb(115, 115, 115); border-right: 1px solid rgb(115, 115, 115);'
                                 'border-bottom: 1px solid rgb(115, 115, 115); font-family: "Segoe UI";}'
                                 'QLabel {color: rgb(235, 235, 235); padding-top: 30px; font-family: "Segoe UI";}'
                                 'QPushButton {background-color: rgb(115, 115, 115); color: rgb(235, 235, 235);'
                                 'border-radius: 11px; padding: 5px; min-width: 5em; font-family: "Segoe UI";}'
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
                'border-bottom: 1px solid rgb(115, 115, 115); font-family: "Segoe UI";}'
                'QLabel {color: rgb(235, 235, 235); padding-top: 30px; font-family: "Segoe UI";}'
                'QPushButton {background-color: rgb(115, 115, 115); color: rgb(235, 235, 235);'
                'border-radius: 11px; padding: 5px; min-width: 5em; font-family: "Segoe UI";}'
                'QPushButton:pressed {background-color: rgb(53, 53, 53)}'
                'QPushButton:hover {border: 0.5px solid white}')
            msgBox.exec()

# Liked Teachers menubar function
    def teacher_list_widget(self):
        dialog = QDialog(self, QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        dialog.setWindowTitle('VIPKid Feedback App')
        dialog.setMinimumWidth(450)
        # widget layout
        layout = QVBoxLayout()
        # Instructions Tool Tip
        hbox_tooltip = QHBoxLayout()
        title = QLabel('<h3>Liked Teachers List</h3>')
        title_tip = QLabel()
        title_tip.setPixmap(self.app_widget.pixmap)
        title_tip.setToolTip('<ul style="margin-left: 10px; -qt-list-indent: 0;">'
                             '<li><b>Add</b> a teacher by typing their name and pressing '
                             'the <br>"Add Teacher" button.</li>'
                             '<li><b>Remove</b> a teacher by selecting their name and '
                             'pressing the "Remove Teacher" button.</li>'
                             '</ul>')
        hbox_tooltip.addWidget(title, 1)
        hbox_tooltip.addWidget(title_tip, 5)
        layout.addLayout(hbox_tooltip)
        layout.addSpacing(9)
        # Add teacher button and textedit
        hbox_buttons_layout = QHBoxLayout()
        self.new_teacher_name = QLineEdit()
        self.new_teacher_name.setFixedHeight(21)
        self.add_teacher_button = QPushButton('Add Teacher', dialog)
        hbox_buttons_layout.addWidget(self.new_teacher_name)
        hbox_buttons_layout.addSpacing(3)
        hbox_buttons_layout.addWidget(self.add_teacher_button)
        self.add_teacher_button.setMinimumWidth(150)
        layout.addLayout(hbox_buttons_layout)
        layout.addSpacing(3)
        # List Widget
        self.list_widget = QListView(dialog)
        self.list_widget.setModel(self.model)
        layout.addWidget(self.list_widget)
        layout.addSpacing(3)
        # Remove teacher button
        self.remove_teacher_button = QPushButton('Remove Teacher', dialog)
        self.remove_teacher_button.setMaximumWidth(150)
        layout.addWidget(self.remove_teacher_button)
        layout.addSpacing(7)
        # Reminder to user
        reminder = QLabel()
        reminder.setWordWrap(True)
        reminder.setText('<i>Remember, it is best to add teachers who have '
                         'feedback templates that are compatible with VIPKid Feedback App. '
                         'Head to the <b>Help Menu</b> for more details on what templates are compatible.</i>')
        layout.addWidget(reminder)
        dialog.setLayout(layout)
        # style
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, QColor(235, 235, 235))
        dialog.setPalette(palette)
        self.list_widget.setStyleSheet('QListView {background-color: rgb(36, 36, 36); border-radius: 4px;'
                                       'color: rgb(235, 235, 235); border: 0.5px solid rgba(115, 115, 115, 0.5);'
                                       'font-family: "Segoe UI"; font-size: 12px;}'
                                       'QListView::item:hover {background-color: rgb(115, 115, 115)}'
                                       'QListView::item:selected:active {background-color: rgb(115, 115, 115)}')
        self.new_teacher_name.setStyleSheet('background-color: rgb(36, 36, 36); border-radius: 2px; font-size: 12px;'
                                            'color: rgb(235, 235, 235); border: 0.5px solid rgba(115, 115, 115, 0.5);'
                                            'font-family: "Segoe UI";')
        self.add_teacher_button.setStyleSheet('QPushButton {background-color: rgb(115, 115, 115); color: rgb(235, 235, 235);'
                                              'border-radius: 12px; padding: 5px; font: bold 12px; font-family: "Segoe UI";}'
                                              'QPushButton:pressed {background-color: rgb(53, 53, 53)}'
                                              'QPushButton:hover {border: 0.5px solid white}')
        self.remove_teacher_button.setStyleSheet('QPushButton {background-color: rgb(115, 115, 115); color: rgb(235, 235, 235);'
                                                 'border-radius: 12px; padding: 5px; font: bold 12px; font-family: "Segoe UI";}'
                                                 'QPushButton:pressed {background-color: rgb(53, 53, 53)}'
                                                 'QPushButton:hover {border: 0.5px solid white}'
                                                 'QPushButton:disabled {color: rgb(53, 53, 53)}')
        title.setStyleSheet('font-family: "Segoe UI";color: rgb(235, 235, 235)')
        reminder.setStyleSheet('font-size: 9px; font-family: "Segoe UI"; color: rgb(235, 235, 235)')
        # slots
        self.add_teacher_button.clicked.connect(self.add_teacher)
        self.remove_teacher_button.clicked.connect(self.remove_teacher)
        dialog.exec()

    def add_teacher(self):
        added_teacher = self.new_teacher_name.text()
        if added_teacher:
            self.model.teachers_list.append(added_teacher)
            self.model.layoutChanged.emit()
            self.new_teacher_name.clear()
            self.save_liked_teachers()

    def remove_teacher(self):
        # Delete? MsgBox
        indexes = self.list_widget.selectedIndexes()
        index_text = self.model.teachers_list[indexes[0].row()]
        msgBox = QMessageBox(self)
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowFlag(QtCore.Qt.ToolTip)
        msgBox.setTextFormat(QtCore.Qt.RichText)
        msgBox.setText(f'Are you sure you want to remove:<br>'
                       f'<b>{index_text}</b>?')
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgBox.setDefaultButton(QMessageBox.Yes)
        msgBox.setStyleSheet('QMessageBox {background-color: rgb(53, 53, 53); border-top: 25px solid rgb(115, 115, 115);'
                             'border-left: 1px solid rgb(115, 115, 115); border-right: 1px solid rgb(115, 115, 115);'
                             'border-bottom: 1px solid rgb(115, 115, 115); font-family: "Segoe UI";}'
                             'QLabel {color: rgb(235, 235, 235); padding-top: 30px; font-family: "Segoe UI";}'
                             'QPushButton {background-color: rgb(115, 115, 115); color: rgb(235, 235, 235);'
                             'border-radius: 11px; padding: 5px; min-width: 5em; font-family: "Segoe UI";}'
                             'QPushButton:pressed {background-color: rgb(53, 53, 53)}'
                             'QPushButton:hover {border: 0.5px solid white}')
        result = msgBox.exec()
        if result == QMessageBox.Yes:
            if indexes:
                index = indexes[0]
                del self.model.teachers_list[index.row()]
                self.model.layoutChanged.emit()
                self.list_widget.clearSelection()
                self.save_liked_teachers()

    def load_liked_teachers(self):
        try:
            with open('liked_teachers.json', 'r') as file:
                self.model.teachers_list = json.load(file)
        except Exception:
            pass

    def save_liked_teachers(self):
        with open('liked_teachers.json', 'w') as file:
            json.dump(self.model.teachers_list, file)

    # Signature menubar function
    def teacher_signature_widget(self):
        dialog = QDialog(self, QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        dialog.setWindowTitle('VIPKid Feedback App')
        dialog.setMinimumWidth(450)
        # widget layout
        layout = QVBoxLayout()
        title = QLabel('<h3>Edit Feedback Signature</h3>')
        layout.addWidget(title)
        self.signature_textbox = QPlainTextEdit(dialog)
        # load current feedback signature
        self.load_signature()
        layout.addWidget(self.signature_textbox)
        # save_button hbox
        save_hbox_layout = QHBoxLayout()
        self.save_signature_button = QPushButton('Save', dialog)
        self.save_signature_button.setMinimumWidth(150)
        self.save_confirmed = QLabel('Saved Successfully!')
        self.save_confirmed.setVisible(False)
        save_hbox_layout.addWidget(self.save_signature_button, 1, alignment=QtCore.Qt.AlignLeft)
        save_hbox_layout.addWidget(self.save_confirmed, 5)
        layout.addLayout(save_hbox_layout)
        dialog.setLayout(layout)
        # style
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, QColor(235, 235, 235))
        dialog.setPalette(palette)
        self.signature_textbox.setStyleSheet('background-color: rgb(36, 36, 36); border-radius: 4px; font-size: 12px;'
                                             'color: rgb(235, 235, 235); border: 0.5px solid rgba(115, 115, 115, 0.5)')
        self.save_signature_button.setStyleSheet('QPushButton {background-color: rgb(115, 115, 115); color: rgb(235, 235, 235);'
                                                 'border-radius: 12px; padding: 5px; font: bold 12px; font-family: "Segoe UI";}'
                                                 'QPushButton:pressed {background-color: rgb(53, 53, 53)}'
                                                 'QPushButton:hover {border: 0.5px solid white}')
        title.setStyleSheet('font-family: "Segoe UI"; color: rgb(235, 235, 235)')
        self.save_confirmed.setStyleSheet('font-family: "Segoe UI"; font-size: 12px; color: rgb(235, 235, 235)')
        # slots
        self.save_signature_button.clicked.connect(self.save_signature_slots)
        dialog.exec()

    def load_signature(self):
        try:
            with open('signature.txt', 'r') as file:
                signature = file.read()
                self.signature_textbox.setPlainText(signature)
        except Exception:
            msgBox = QMessageBox(self)
            msgBox.setWindowModality(QtCore.Qt.WindowModal)
            msgBox.setWindowFlag(QtCore.Qt.ToolTip)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText('There was an error loading your feedback signature.')
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.setDefaultButton(QMessageBox.Ok)
            msgBox.setStyleSheet(
                'QMessageBox {background-color: rgb(53, 53, 53); border-top: 25px solid rgb(115, 115, 115);'
                'border-left: 1px solid rgb(115, 115, 115); border-right: 1px solid rgb(115, 115, 115);'
                'border-bottom: 1px solid rgb(115, 115, 115); font-family: "Segoe UI";}'
                'QLabel {color: rgb(235, 235, 235); padding-top: 30px; font-family: "Segoe UI";}'
                'QPushButton {background-color: rgb(115, 115, 115); color: rgb(235, 235, 235);'
                'border-radius: 11px; padding: 5px; min-width: 5em; font-family: "Segoe UI";}'
                'QPushButton:pressed {background-color: rgb(53, 53, 53)}'
                'QPushButton:hover {border: 0.5px solid white}')
            msgBox.exec()

    def save_signature(self):
        with open('signature.txt', 'w') as file:
            new_signature = self.signature_textbox.toPlainText()
            file.write(new_signature)

    def saved_error_msg(self):
        msgBox = QMessageBox(self)
        msgBox.setWindowModality(QtCore.Qt.WindowModal)
        msgBox.setWindowFlag(QtCore.Qt.ToolTip)
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText('There was an error saving your feedback signature.\n'
                       'Please try saving again.')
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.setDefaultButton(QMessageBox.Ok)
        msgBox.setStyleSheet(
            'QMessageBox {background-color: rgb(53, 53, 53); border-top: 25px solid rgb(115, 115, 115);'
            'border-left: 1px solid rgb(115, 115, 115); border-right: 1px solid rgb(115, 115, 115);'
            'border-bottom: 1px solid rgb(115, 115, 115); font-family: "Segoe UI";}'
            'QLabel {color: rgb(235, 235, 235); padding-top: 30px; font-family: "Segoe UI";}'
            'QPushButton {background-color: rgb(115, 115, 115); color: rgb(235, 235, 235);'
            'border-radius: 11px; padding: 5px; min-width: 5em; font-family: "Segoe UI";}'
            'QPushButton:pressed {background-color: rgb(53, 53, 53)}'
            'QPushButton:hover {border: 0.5px solid white}')
        msgBox.exec()

    def saved_msg(self):
        self.save_confirmed.setVisible(True)

    def saved_msg_close(self):
        self.save_confirmed.setVisible(False)

    def save_signature_slots(self):
        worker = SaveSignatureWorkerThread(self.save_signature)
        worker.signal.saved_msg_signal.connect(self.saved_msg)
        worker.signal.saved_msg_close_signal.connect(self.saved_msg_close)
        worker.signal.saved_error.connect(self.saved_error_msg)
        self.main_window_threadpool.start(worker)


class WorkerSignals(QObject):
    saved_msg_signal = pyqtSignal()
    saved_msg_close_signal = pyqtSignal()
    saved_error = pyqtSignal()


class SaveSignatureWorkerThread(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(SaveSignatureWorkerThread, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signal = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            self.fn(*self.args, **self.kwargs)
            time.sleep(0.25)
            self.signal.saved_msg_signal.emit()
            time.sleep(3)
            self.signal.saved_msg_close_signal.emit()
        except Exception:
            self.signal.saved_error.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = Splashscreen()
    window = MainWindow()
    window.show()
    splash.stop(window)
    app.exec()
