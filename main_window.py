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
        signature_menu = edit_menu.addMenu('Edit Feedback Signatures')
        signature_menu.addAction(self.default_signature)
        signature_menu.addAction(self.new_student_signature)
        edit_menu.addAction(self.edit_teachers)
        help_menu = menuBar.addMenu('&Help')
        help_menu.addAction(self.help)
        help_menu.addAction(self.support)
        help_menu.addAction(self.submit_feedback)
        help_menu.addAction(self.suggest_feature)

    def _createActions(self):
        self.sign_out = QAction('&Log Out', self)
        self.default_signature = QAction('Default Signature', self)
        self.new_student_signature = QAction('New Student Signature', self)
        self.edit_teachers = QAction('&Edit Liked Teachers', self)
        self.help = QAction('&Help', self)
        self.support = QAction('Contact &Support...', self)
        self.submit_feedback = QAction('Submit Feedback...', self)
        self.suggest_feature = QAction('Suggest a Feature...', self)

    def _connectActions(self):
        self.sign_out.triggered.connect(self.logout)
        self.edit_teachers.triggered.connect(self.teacher_list_widget)
        self.default_signature.triggered.connect(self.feedback_signature_default)
        self.new_student_signature.triggered.connect(self.feedback_signature_new)
        self.help.triggered.connect(self.help_widget)
        self.support.triggered.connect(self.contact_support_widget)
        self.submit_feedback.triggered.connect(self.feedback_url)
        self.suggest_feature.triggered.connect(self.feature_url)

    def closeEvent(self, event):
        try:
            self.app_widget.browser.quit()
        except:
            pass

# LOGOUT menubar function
    def logout(self):
        """slot for logout option in menubar"""
        msgBox = QMessageBox(self)
        msgBox.setWindowModality(QtCore.Qt.WindowModal)
        msgBox.setWindowFlag(QtCore.Qt.ToolTip)
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText('<p><b>Are you sure you would like to logout?</b></p>'
                       'If you logout, you will need to re-login<br>'
                       'with your VIPKid login info the next time <br>'
                       'you use the Feedback App.')
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msgBox.setDefaultButton(QMessageBox.Cancel)
        msgBox.setStyleSheet(
            'QMessageBox {background-color: rgb(53, 53, 53); border-top: 25px solid rgb(115, 115, 115);'
            'border-left: 1px solid rgb(115, 115, 115); border-right: 1px solid rgb(115, 115, 115);'
            'border-bottom: 1px solid rgb(115, 115, 115); font-family: "Segoe UI";}'
            'QLabel {color: rgb(235, 235, 235); padding-top: 30px; font-family: "Segoe UI";}'
            'QPushButton {background-color: rgb(115, 115, 115); color: rgb(235, 235, 235);'
            'border-radius: 11px; padding: 5px; min-width: 5em; font-family: "Segoe UI";}'
            'QPushButton:pressed {background-color: rgb(53, 53, 53)}'
            'QPushButton:hover {border: 0.5px solid white}')
        result = msgBox.exec()
        if result == QMessageBox.Yes:
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
        title = QLabel('<h2>Liked Teachers List</h2>')
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
        self.new_teacher_name.setFixedHeight(24)
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
                                       'font-family: "Segoe UI"; font-size: 14px;}'
                                       'QListView::item:hover {background-color: rgb(115, 115, 115)}'
                                       'QListView::item:selected:active {background-color: rgb(115, 115, 115)}')
        self.new_teacher_name.setStyleSheet('background-color: rgb(36, 36, 36); border-radius: 2px; font-size: 14px;'
                                            'color: rgb(235, 235, 235); border: 0.5px solid rgba(115, 115, 115, 0.5);'
                                            'font-family: "Segoe UI";')
        self.add_teacher_button.setStyleSheet('QPushButton {background-color: rgb(115, 115, 115); color: rgb(235, 235, 235);'
                                              'border-radius: 14px; padding: 5px; font: bold 14px; font-family: "Segoe UI";}'
                                              'QPushButton:pressed {background-color: rgb(53, 53, 53)}'
                                              'QPushButton:hover {border: 0.5px solid white}')
        self.remove_teacher_button.setStyleSheet('QPushButton {background-color: rgb(115, 115, 115); color: rgb(235, 235, 235);'
                                                 'border-radius: 14px; padding: 5px; font: bold 14px; font-family: "Segoe UI";}'
                                                 'QPushButton:pressed {background-color: rgb(53, 53, 53)}'
                                                 'QPushButton:hover {border: 0.5px solid white}'
                                                 'QPushButton:disabled {color: rgb(53, 53, 53)}')
        title.setStyleSheet('font-family: "Segoe UI";color: rgb(235, 235, 235)')
        reminder.setStyleSheet('font-size: 10px; font-family: "Segoe UI"; color: rgb(235, 235, 235)')
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

    # Edit default feedback signature dialog.
    def feedback_signature_default(self):
        dialog = QDialog(self, QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        dialog.setWindowTitle('VIPKid Feedback App')
        dialog.setMinimumWidth(450)
        # widget layout
        layout = QVBoxLayout()
        title = QLabel('<h2>Edit Default Signature</h2>')
        layout.addWidget(title)
        self.signature_textbox_default = QPlainTextEdit(dialog)
        # load current default feedback signature
        self.load_signature('default')
        layout.addWidget(self.signature_textbox_default)
        # save_button hbox
        save_hbox_layout = QHBoxLayout()
        save_default_signature_btn = QPushButton('Save', dialog)
        save_default_signature_btn.setMinimumWidth(150)
        self.save_confirmed = QLabel('Saved Successfully!')
        self.save_confirmed.setVisible(False)
        save_hbox_layout.addWidget(save_default_signature_btn, 1, alignment=QtCore.Qt.AlignLeft)
        save_hbox_layout.addWidget(self.save_confirmed, 5)
        layout.addLayout(save_hbox_layout)
        dialog.setLayout(layout)
        # style
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, QColor(235, 235, 235))
        dialog.setPalette(palette)
        self.signature_textbox_default.setStyleSheet('background-color: rgb(36, 36, 36); border-radius: 4px; font-size: 14px;'
                                                     'color: rgb(235, 235, 235); border: 0.5px solid rgba(115, 115, 115, 0.5)')
        save_default_signature_btn.setStyleSheet('QPushButton {background-color: rgb(115, 115, 115); color: rgb(235, 235, 235);'
                                                 'border-radius: 14px; padding: 5px; font: bold 14px; font-family: "Segoe UI";}'
                                                 'QPushButton:pressed {background-color: rgb(53, 53, 53)}'
                                                 'QPushButton:hover {border: 0.5px solid white}')
        title.setStyleSheet('font-family: "Segoe UI"; color: rgb(235, 235, 235)')
        self.save_confirmed.setStyleSheet('font-family: "Segoe UI"; font-size: 14px; color: rgb(235, 235, 235)')
        # slots
        save_default_signature_btn.clicked.connect(self.save_signature_slots_default)
        dialog.exec()

    # Edit new student feedback signature dialog.
    def feedback_signature_new(self):
        dialog = QDialog(self, QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        dialog.setWindowTitle('VIPKid Feedback App')
        dialog.setMinimumWidth(450)
        # widget layout
        layout = QVBoxLayout()
        title = QLabel('<h2>Edit New Student Signature</h2>')
        layout.addWidget(title)
        self.signature_textbox_new = QPlainTextEdit(dialog)
        # load current feedback signature
        self.load_signature('new')
        layout.addWidget(self.signature_textbox_new)
        # save_button hbox
        save_hbox_layout = QHBoxLayout()
        save_new_signature_btn = QPushButton('Save', dialog)
        save_new_signature_btn.setMinimumWidth(150)
        self.save_confirmed = QLabel('Saved Successfully!')
        self.save_confirmed.setVisible(False)
        save_hbox_layout.addWidget(save_new_signature_btn, 1, alignment=QtCore.Qt.AlignLeft)
        save_hbox_layout.addWidget(self.save_confirmed, 5)
        layout.addLayout(save_hbox_layout)
        dialog.setLayout(layout)
        # style
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, QColor(235, 235, 235))
        dialog.setPalette(palette)
        self.signature_textbox_new.setStyleSheet('background-color: rgb(36, 36, 36); border-radius: 4px; font-size: 14px;'
                                                 'color: rgb(235, 235, 235); border: 0.5px solid rgba(115, 115, 115, 0.5)')
        save_new_signature_btn.setStyleSheet('QPushButton {background-color: rgb(115, 115, 115); color: rgb(235, 235, 235);'
                                             'border-radius: 14px; padding: 5px; font: bold 14px; font-family: "Segoe UI";}'
                                             'QPushButton:pressed {background-color: rgb(53, 53, 53)}'
                                             'QPushButton:hover {border: 0.5px solid white}')
        title.setStyleSheet('font-family: "Segoe UI"; color: rgb(235, 235, 235)')
        self.save_confirmed.setStyleSheet('font-family: "Segoe UI"; font-size: 14px; color: rgb(235, 235, 235)')
        # slots
        save_new_signature_btn.clicked.connect(self.save_signature_slots_new)
        dialog.exec()

    def load_signature(self, sig_type: str):
        try:
            with open('signature.json', 'r') as openfile:
                self.signature = json.load(openfile)
                if sig_type == 'default':
                    self.signature_textbox_default.setPlainText(self.signature['default'])
                elif sig_type == 'new':
                    self.signature_textbox_new.setPlainText(self.signature['new_student'])
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

    def save_signature_default(self):
        # update dictionary data.
        edited_signature = self.signature_textbox_default.toPlainText()
        self.signature['default'] = edited_signature
        # write updated data to json.
        with open('signature.json', 'w') as outfile:
            json.dump(self.signature, outfile)

    def save_signature_new(self):
        edited_signature = self.signature_textbox_new.toPlainText()
        self.signature['new_student'] = edited_signature
        with open('signature.json', 'w') as outfile:
            json.dump(self.signature, outfile)

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

    def save_signature_slots_default(self):
        worker = SaveSignatureWorkerThreadDefault(self.save_signature_default)
        worker.signal.saved_msg_signal.connect(self.saved_msg)
        worker.signal.saved_msg_close_signal.connect(self.saved_msg_close)
        worker.signal.saved_error.connect(self.saved_error_msg)
        self.main_window_threadpool.start(worker)

    def save_signature_slots_new(self):
        worker = SaveSignatureWorkerThreadNew(self.save_signature_new)
        worker.signal.saved_msg_signal.connect(self.saved_msg)
        worker.signal.saved_msg_close_signal.connect(self.saved_msg_close)
        worker.signal.saved_error.connect(self.saved_error_msg)
        self.main_window_threadpool.start(worker)

    def help_widget(self):
        dialog = QDialog(self, QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        dialog.setWindowTitle('VIPKid Feedback App')
        help_widget = QTextBrowser(dialog)
        help_widget.setMinimumSize(475, 425)
        help_widget.setHtml('<h2 style="margin-bottom: 2px";>Help Menu</h2>'
                            'Last updated: 2 February 2021'
                            '<hr>'
                            '<h3>Video Tutorials</h3>'
                            '<ul>'
                            '<li><a href="https://www.youtube.com/watch?v=qo_2mlkbs9g" style="color: #4d94ff; text-decoration: none;"> Full-length Tutorial (19:54)</a></li>'
                            '<li><a href="https://youtu.be/nsJ5m8Drx-g" style="color: #4d94ff; text-decoration: none;"> Day-to-Day Use Tutorial (4:09)</a></li></li>'
                            '</ul>'
                            '<h3>How to use the app:</h3>'                          
                            '<ol>'
                            '<li>Click the <b>Login</b> button, and wait for the "Logged In!" message to appear.</li>'
                            '<ul>'
                            '<li>When using the app for the first time, a window will open for you to login into the '
                            'VIPKid website.</li>'
                            '<li>After logging into VIPKid, the window will close automatically and you will be returned to '
                            'the feedback app.</li>'
                            '<li>After logging in for the first time, the app will remember your login info. So that '
                            'the next time you use the app, you will be logged in automatically after clicking the '
                            '<b>Login</b> button.</li>'
                            '</ul>'
                            '<li>Click <b>Get Feedback Template</b> button.</li>'
                            '<ul>'
                            '<li>Clicking this button will automatically get the student name and feedback template for each '
                            'of your current missing class feedback submissions, in chronological order.</li>'
                            '<li>The feedback templates that the app gets are based on the teachers in the '
                            '<b>Liked Teachers List</b> in the Edit Menu.</li>'
                            '<li>If any of the teachers in your <b>Liked Teachers List</b>, also have templates in the '
                            'materials section of the lesson you are giving feedback for, their names will be shown in a '
                            'drop down menu for you to choose from.</li>'
                            "<li>Selecting a teacher's name will automatically put their respective feedback template "
                            "in the <i>Feedback Template</i> text box.</li>"
                            '</ul>'
                            "<li>Next, you'll want to go ahead and make any revisions to the template, if needed.</li>"
                            '<li>Select whether or not your current feedback is for a new student.</li>'
                            '<li>Click <b>Generate Feedback</b> button.</li>'
                            '<ul>'
                            "<li>This will customize your feedback by using your student's name and adding your personal "
                            "<b>Feedback Signature</b>, which you can find in the Edit Menu.</li>"
                            '<li>It will also take into account if you have selected whether the current feedback is a '
                            'new student or not. Based on your selection, either the <i>Default Signature</i> or the '
                            '<i>New Student Signature</i> will be used.</li>'
                            '</ul>'
                            '<li>Once you are happy with the customized feedback, copy it by clicking the <b>Copy Feedback</b> button.</li>'
                            "<li>Lastly, you can now use your custom feedback when submitting your student's class feedback.</li>"
                            '</ol>')
        help_widget.setOpenExternalLinks(True)
        help_widget.setStyleSheet('background-color: rgb(53, 53, 53); font-size: 14px; color: rgb(235, 235, 235);'
                                  'border: transparent; font-family: "Segoe UI";')
        dialog.setStyleSheet('background-color: rgb(53, 53, 53);')
        dialog.setFixedSize(475, 425)
        dialog.exec()

    def feedback_url(self):
        url = QtCore.QUrl('https://carlossmith.typeform.com/to/BwQMNq0g')
        if not QtGui.QDesktopServices.openUrl(url):
            QMessageBox.warning(self, 'Submit Feedback...', 'Unable to submit feedback at this time, please try again.')

    def feature_url(self):
        url = QtCore.QUrl('https://carlossmith.typeform.com/to/mbrd6nKD')
        if not QtGui.QDesktopServices.openUrl(url):
            QMessageBox.warning(self, 'Suggest Feature...', 'Unable to suggest feature at this time, please try again.')

    def contact_support_widget(self):
        dialog = QDialog(self, QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        dialog.setWindowTitle('VIPKid Feedback App')
        help_widget = QTextBrowser(dialog)
        help_widget.setMinimumSize(375, 215)
        help_widget.setHtml('<h3>Contact Support</h3>'
                            'Shoot us an email at: <a href="mailto: feedbackapp.contact@gmail.com" style="color: #4d94ff; text-decoration: none;">feedbackapp.contact@gmail.com</a><br>'
                            'In your email, please include:'
                            '<ul>'
                            '<li>A detailed explanation of the issue you are facing.</li>'
                            '<li>Any screenshots or videos of your issue.</li>'
                            '</ul>'
                            '<p>-Or-</p>'
                            'Tweet us <a href="https://twitter.com/The_FeedbackApp" style="color: #4d94ff; text-decoration: none;">@The_FeedbackApp</a>')
        help_widget.setOpenExternalLinks(True)
        help_widget.setStyleSheet('background-color: rgb(53, 53, 53); font-size: 14px; color: rgb(235, 235, 235);'
                                  'border: transparent; font-family: "Segoe UI";')
        dialog.setStyleSheet('background-color: rgb(53, 53, 53);')
        dialog.setFixedSize(375, 215)
        dialog.exec()


class WorkerSignals(QObject):
    saved_msg_signal = pyqtSignal()
    saved_msg_close_signal = pyqtSignal()
    saved_error = pyqtSignal()


class SaveSignatureWorkerThreadDefault(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(SaveSignatureWorkerThreadDefault, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signal = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            self.signal.saved_msg_close_signal.emit()
            time.sleep(0.5)
            self.fn(*self.args, **self.kwargs)
            self.signal.saved_msg_signal.emit()
        except Exception:
            self.signal.saved_error.emit()


class SaveSignatureWorkerThreadNew(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(SaveSignatureWorkerThreadNew, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signal = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            self.signal.saved_msg_close_signal.emit()
            time.sleep(0.5)
            self.fn(*self.args, **self.kwargs)
            self.signal.saved_msg_signal.emit()
        except Exception:
            self.signal.saved_error.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = Splashscreen()
    window = MainWindow()
    window.show()
    splash.stop(window)
    app.exec()
