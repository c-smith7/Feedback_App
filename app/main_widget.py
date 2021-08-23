import json
import os
import pickle
import re
import time

import enchant
from PyQt5 import Qt, QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import QMovie
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtWidgets import QSplashScreen, qApp
from enchant import tokenize
from enchant.errors import TokenizerNotFoundError
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


# noinspection PyArgumentList,PyTypeChecker,PyBroadException,PyUnresolvedReferences
class Window(QWidget):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        # Widget config
        self.threadpool = QThreadPool()
        self.layout = QVBoxLayout()
        # Widgets
        self.feedback_temp = SpellTextEdit()
        self.feedback_label = QLabel('Feedback :')
        self.feedback_output = QPlainTextEdit(self)
        self.generate_output = QPushButton('Generate Feedback')
        # New student hbox
        self.new_student_hbox = QHBoxLayout()
        self.new_student = QLabel('New Student? :')
        self.yes_button = QRadioButton('&Yes')
        self.no_button = QRadioButton('&No')
        self.new_student_hbox.addWidget(self.new_student, 1)
        self.new_student_hbox.addSpacing(4)
        self.new_student_hbox.addWidget(self.yes_button, 5)
        self.new_student_hbox.addWidget(self.no_button, 45)
        # Student name hbox
        self.student_hbox = QHBoxLayout()
        self.student_label = QLabel('Student Name :')
        self.student = QLineEdit()
        self.student.setFixedHeight(24)
        self.student_hbox.addWidget(self.student_label)
        self.student_hbox.addWidget(self.student)
        # HBox button group 1
        self.hbox_buttons1 = QWidget()
        self.hbox_buttonsLayout1 = QHBoxLayout(self.hbox_buttons1)
        self.login_button = QPushButton('Login')
        self.get_template_button = QPushButton('Get Feedback Template')
        self.get_template_button.setEnabled(False)
        self.loading = QLabel()
        self.loading.setVisible(False)
        self.login_success = QLabel('Logged In!')
        self.login_success.setVisible(False)
        self.logged_in_already = QLabel('Already logged in!')
        self.logged_in_already.setVisible(False)
        self.get_template_tip = QLabel()
        self.pixmap = QPixmap(':/icons/tooltip')
        self.get_template_tip.setPixmap(self.pixmap)
        self.hbox_buttonsLayout1.addWidget(self.get_template_button, 3)
        self.hbox_buttonsLayout1.addWidget(self.get_template_tip)
        self.hbox_buttonsLayout1.addSpacing(15)
        self.hbox_buttonsLayout1.addWidget(self.login_button, 1)
        self.hbox_buttonsLayout1.addWidget(self.loading)
        self.hbox_buttonsLayout1.addWidget(self.login_success)
        self.hbox_buttonsLayout1.addWidget(self.logged_in_already)
        # HBox button group 2
        self.hbox_buttonsLayout2 = QHBoxLayout()
        self.copy_output_button = QPushButton('Copy Feedback')
        self.clear_form_button = QPushButton('Clear')
        self.copy_output_tip = QLabel()
        self.copy_output_tip.setPixmap(self.pixmap)
        self.hbox_buttonsLayout2.addWidget(self.copy_output_tip, 1)
        self.hbox_buttonsLayout2.addWidget(self.copy_output_button, 50)
        self.hbox_buttonsLayout2.addSpacing(5)
        self.hbox_buttonsLayout2.addWidget(self.clear_form_button, 48)
        # HBox group 3
        self.hbox_Layout3 = QHBoxLayout()
        self.template_label = QLabel('Feedback Template :')
        self.available_templates = QComboBox(self)
        self.available_templates.setVisible(False)
        # lists used to store teacher names and respective templates in combobox
        self.teacher_list = []
        self.template_list = []
        self.hbox_Layout3.addWidget(self.template_label, 2)
        self.hbox_Layout3.addWidget(self.available_templates, 1)
        # Add widgets to layout
        self.layout.addWidget(self.hbox_buttons1)
        self.layout.addWidget(QHline())
        self.layout.addSpacing(5)
        self.layout.addLayout(self.student_hbox)
        self.layout.addSpacing(7)
        self.layout.addLayout(self.new_student_hbox)
        self.layout.addSpacing(7)
        self.layout.addLayout(self.hbox_Layout3)
        self.layout.addSpacing(2)
        self.layout.addWidget(self.feedback_temp, 6)
        self.layout.addSpacing(5)
        self.layout.addWidget(self.generate_output)
        self.layout.addSpacing(5)
        self.layout.addWidget(QHline())
        self.layout.addSpacing(5)
        self.layout.addWidget(self.feedback_label)
        self.layout.addSpacing(2)
        self.layout.addWidget(self.feedback_output, 5)
        self.layout.addSpacing(2)
        self.layout.addLayout(self.hbox_buttonsLayout2)
        self.setLayout(self.layout)
        # Button configs
        self.no_button.setChecked(True)
        self.generate_output.setDefault(True)
        self.copy_output_button.setDefault(True)
        self.clear_form_button.setDefault(True)
        self.get_template_button.setDefault(True)
        self.feedback_temp.setTabChangesFocus(True)
        self.feedback_output.setTabChangesFocus(True)
        self.yes_button.setFocusPolicy(Qt.NoFocus)
        self.no_button.setFocusPolicy(Qt.NoFocus)
        self.feedback_output.setFocusPolicy(Qt.NoFocus)
        # Style sheets
        self.generate_output.setStyleSheet('QPushButton {background-color: rgb(115, 115, 115); color: rgb(235, 235, 235);'
                                           'border-radius: 14px; padding: 5px; font: bold 14px; font-family: "Segoe UI";}'
                                           'QPushButton:pressed {background-color: rgb(53, 53, 53)}'
                                           'QPushButton:hover {border: 0.5px solid white}')
        self.copy_output_button.setStyleSheet('QPushButton {background-color: rgb(115, 115, 115); color: rgb(235, 235, 235);'
                                              'border-radius: 14px; padding: 5px; font: bold 14px; font-family: "Segoe UI";}'
                                              'QPushButton:pressed {background-color: rgb(53, 53, 53)}'
                                              'QPushButton:hover {border: 0.5px solid white}')
        self.clear_form_button.setStyleSheet('QPushButton {background-color: rgb(115, 115, 115); color: rgb(235, 235, 235);'
                                             'border-radius: 14px; padding: 5px; font: bold 14px; font-family: "Segoe UI";}'
                                             'QPushButton:pressed {background-color: rgb(53, 53, 53)}'
                                             'QPushButton:hover {border: 0.5px solid white}')
        self.get_template_button.setStyleSheet('QPushButton {background-color: rgb(115, 115, 115); color: rgb(235, 235, 235);'
                                               'border-radius: 14px; padding: 5px; font: bold 14px; font-family: "Segoe UI";}'
                                               'QPushButton:pressed {background-color: rgb(53, 53, 53)}'
                                               'QPushButton:hover {border: 0.5px solid white}'
                                               'QPushButton:disabled {color: rgb(53, 53, 53)}')
        self.login_button.setStyleSheet('QPushButton {background-color: rgb(115, 115, 115); color: rgb(235, 235, 235);'
                                        'border-radius: 14px; padding: 5px; font: bold 14px; font-family: "Segoe UI";}'
                                        'QPushButton:pressed {background-color: rgb(53, 53, 53)}'
                                        'QPushButton:hover {border: 0.5px solid white}')
        self.available_templates.setStyleSheet('QComboBox {background-color: rgb(115, 115, 115); color: rgb(235, 235, 235);'
                                               'border-radius: 9px; padding-left: 10px; padding-top: 2px; padding-bottom: 2px;'
                                               'font-family: "Segoe UI"; font-size: 14px;}'
                                               'QComboBox::drop-down {background-color: rgb(115, 115, 115); border-radius: 8.3px;'
                                               'padding-right: 12px;}'
                                               'QComboBox::down-arrow {image: url(:/icons/down_arrow);}'
                                               'QComboBox QAbstractItemView {background-color: rgb(53, 53, 53);'
                                               'color: rgb(235, 235, 235); selection-background-color: rgb(115, 115, 115);'
                                               'border: 1px solid rgb(53, 53, 53); font-family: "Segoe UI"; font-size: 14px;}')
        self.feedback_temp.setStyleSheet('background-color: rgb(36, 36, 36); border-radius: 4px; font-size: 14px; font-family: "Segoe UI";'
                                         'color: rgb(235, 235, 235); border: 0.5px solid rgba(115, 115, 115, 0.5)')
        self.feedback_output.setStyleSheet('background-color: rgb(36, 36, 36); border-radius: 4px; font-size: 14px; font-family: "Segoe UI";'
                                           'color: rgb(235, 235, 235); border: 0.5px solid rgba(115, 115, 115, 0.5)')
        self.student.setStyleSheet('background-color: rgb(36, 36, 36); border-radius: 2px; font-size: 14px; font-family: "Segoe UI";'
                                   'color: rgb(235, 235, 235); border: 0.5px solid rgba(115, 115, 115, 0.5)')
        self.student_label.setStyleSheet('font-size: 14px; font-family: "Segoe UI"; color: rgb(235, 235, 235)')
        self.new_student.setStyleSheet('font-size: 14px; font-family: "Segoe UI"; color: rgb(235, 235, 235)')
        self.template_label.setStyleSheet('font-size: 14px; font-family: "Segoe UI"; color: rgb(235, 235, 235)')
        self.feedback_label.setStyleSheet('font-size: 14px; font-family: "Segoe UI"; color: rgb(235, 235, 235)')
        self.yes_button.setStyleSheet('font-size: 14px; font-family: "Segoe UI"; color: rgb(235, 235, 235)')
        self.no_button.setStyleSheet('font-size: 14px; font-family: "Segoe UI"; color: rgb(235, 235, 235)')
        self.login_success.setStyleSheet('font-size: 12px; font-family: "Segoe UI"; color: rgb(235, 235, 235)')
        self.logged_in_already.setStyleSheet('font-size: 12px; font-family: "Segoe UI"; color: rgb(235, 235, 235)')
        # Tool Tips
        self.get_template_tip.setToolTip('<ul style="margin-left: 10px; -qt-list-indent: 0;">'
                                         '<li>Automatically get lesson feedback template.</li>'
                                         '<li>Login is required to use this feature.</li>'
                                         '<li>Log in using the "Login" button.</li>'
                                         '</ul>')
        self.copy_output_tip.setToolTip('<ul style="margin-left: 10px; -qt-list-indent: 0;">'
                                        '<li>Copy feedback output to clipboard.</li>'
                                        '<li>Use windows key <img src=":/icons/windows_logo"> + V to access clipboard.</li>'
                                        '</ul>')
        self.generate_output.setToolTip('Generate feedback from template.')
        self.clear_form_button.setToolTip('Clear student name & template.')
        self.login_button.setToolTip('Login & Connect to VIPKid.')
        # self.student.setToolTip('Get template for specific student') //needed after search function implemented
        # Start global webdriver
        if os.path.exists('../cookie'):
            options = Options()
            options.headless = True
            self.browser = webdriver.Chrome(options=options)
            print('driver connected')
        # Signals and slots
        self.login_button_counter = 0
        if os.path.exists('../cookie'):
            self.login_button.clicked.connect(self.login_check_cookie)
        else:
            self.login_button.clicked.connect(self.login_nocookies)
        self.get_template_button.clicked.connect(self.feedback_automation)
        self.generate_output.clicked.connect(self.feedback_script)
        self.copy_output_button.clicked.connect(self.copy)
        self.clear_form_button.clicked.connect(self.clear_form)
        self.available_templates.activated[str].connect(self.available_templates_combobox)

    def load_feedback_signature(self):
        try:
            with open('signature.txt', 'r') as file:
                self.signature = file.read()
        except Exception as e:
            msgBox = QMessageBox(self)
            msgBox.setWindowModality(QtCore.Qt.WindowModal)
            msgBox.setWindowFlag(QtCore.Qt.ToolTip)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText('There was an error loading your feedback signature.')
            msgBox.setDetailedText(e)
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

    def feedback_script(self):
        student_name = self.student.text()
        # load currently saved signatures and replace student keywords with student_name.
        with open(r'C:\Users\mcmco\Desktop\Python_scripts\Feedback_GUI\app\backend_data\signature.json', 'r') as openfile:
            signatures = json.load(openfile)
            signature_default = signatures['default'].replace('(student)', student_name)
            signature_new = signatures['new_student'].replace('(student)', student_name)
        # get feedback template input
        feedback_input = self.feedback_temp.toPlainText()
        # produce feedback output
        feedback_output = re.sub(' we |We ', f' {student_name} and I ', feedback_input, 1)
        feedback_output = ' '.join(feedback_output.split())
        if self.no_button.isChecked():
            self.final_output = f'{feedback_output} {signature_default}'
            if feedback_input.split(' ', 1)[0] in ['We', 'we']:
                self.final_output = f'In this lesson, {self.final_output}'
        elif self.yes_button.isChecked():
            self.final_output = f'{feedback_output} {signature_new}'
            if feedback_input.split(' ', 1)[0] in ['We', 'we']:
                self.final_output = f'In this lesson, {self.final_output}'
        if student_name == '':
            self.feedback_output.clear()
        else:
            self.feedback_output.clear()
            self.feedback_output.insertPlainText(self.final_output)

    def clear_form(self):
        self.student.clear()
        self.feedback_temp.clear()
        self.feedback_output.clear()

    def copy(self):
        try:
            clipboard = QtGui.QGuiApplication.clipboard()
            clipboard.setText(self.final_output)
        except Exception:
            pass

    def login_check_cookie(self):
        if os.path.exists('../cookie'):
            self.login_slots()
        else:
            self.login_nocookies()

    def login(self):
        print('LoginHERE')
        if os.path.exists('../cookie'):
            self.login_button.setEnabled(False)
            self.browser.get('https://www.vipkid.com/login?prevUrl=https%3A%2F%2Fwww.vipkid.com%2Ftc%2Fmissing')
            with open('../cookie', 'rb') as cookiesfile:
                cookies = pickle.load(cookiesfile)
                for cookie in cookies:
                    self.browser.add_cookie(cookie)
                self.browser.refresh()
                missing_cf_button = WebDriverWait(self.browser, 3).until(EC.element_to_be_clickable((By.CLASS_NAME, 'to-do-type')))
                self.browser.execute_script("arguments[0].click();", missing_cf_button)
                self.login_button_counter = 1
                print('Logged In!')
                self.get_template_button.setEnabled(True)
                self.login_button.setEnabled(True)
            os.remove('../cookie')
            with open('../cookie', 'wb') as file:
                pickle.dump(self.browser.get_cookies(), file)
        else:
            print('Went to else statement.')
            self.login_nocookies()

    def login_error_msg(self):
        msgBox = QMessageBox(self)
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowModality(Qt.WindowModal)
        msgBox.setWindowFlag(Qt.ToolTip)
        msgBox.setText('There was a problem logging into VIPKid.\nPlease try again.')
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

    def login_nocookies(self):
        try:
            if self.login_button_counter == 0:
                msgBox = QMessageBox(self)
                msgBox.setWindowModality(Qt.WindowModal)
                msgBox.setWindowFlag(Qt.ToolTip)
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setText('Click the "Login" button below.\nLog in to VIPKid in the window that opens.')
                msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                ok_button = msgBox.button(QMessageBox.Ok)
                ok_button.setText('Login')
                msgBox.setDefaultButton(QMessageBox.Ok)
                msgBox.setStyleSheet('QMessageBox {background-color: rgb(53, 53, 53); border-top: 25px solid rgb(115, 115, 115);'
                                     'border-left: 1px solid rgb(115, 115, 115); border-right: 1px solid rgb(115, 115, 115);'
                                     'border-bottom: 1px solid rgb(115, 115, 115); font-family: "Segoe UI";}'
                                     'QLabel {color: rgb(235, 235, 235); padding-top: 30px; font-family: "Segoe UI";}'
                                     'QPushButton {background-color: rgb(115, 115, 115); color: rgb(235, 235, 235);'
                                     'border-radius: 11px; padding: 5px; min-width: 5em; font-family: "Segoe UI";}'
                                     'QPushButton:pressed {background-color: rgb(53, 53, 53)}'
                                     'QPushButton:hover {border: 0.5px solid white}')
                result = msgBox.exec()
                if result == QMessageBox.Ok:
                    self.login_nocookies_slots()
        except Exception:
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText('Error')
            msgBox.setDetailedText(e)
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

    def login_nocookies_prompt(self):
        self.login_button.setEnabled(False)
        self.browser = webdriver.Chrome()
        self.browser.get('https://www.vipkid.com/login?prevUrl=https%3A%2F%2Fwww.vipkid.com%2Ftc%2Fmissing')
        # Wait for user login.
        WebDriverWait(self.browser, 2147483647).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div/ul/li[2]/a')))
        time.sleep(1)
        # Save cookies file after login
        with open('../cookie', 'wb') as file:
            pickle.dump(self.browser.get_cookies(), file)
        time.sleep(1)
        self.browser.quit()
        options = Options()
        options.headless = True
        self.browser = webdriver.Chrome(options=options)
        self.browser.get('https://www.vipkid.com/login?prevUrl=https%3A%2F%2Fwww.vipkid.com%2Ftc%2Fmissing')
        try:
            with open('../cookie', 'rb') as cookiesfile:
                cookies = pickle.load(cookiesfile)
                for cookie in cookies:
                    self.browser.add_cookie(cookie)
                self.browser.refresh()
                missing_cf_button = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'to-do-type')))
                self.browser.execute_script("arguments[0].click();", missing_cf_button)
                self.login_button_counter = 1
                print('Logged In!')
                self.get_template_button.setEnabled(True)
                self.login_button.setEnabled(True)
        except Exception as e:
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText('Error')
            msgBox.setDetailedText(e)
            msgBox.setStyleSheet('QMessageBox {background-color: rgb(53, 53, 53); border-top: 25px solid rgb(115, 115, 115);'
                                 'border-left: 1px solid rgb(115, 115, 115); border-right: 1px solid rgb(115, 115, 115);'
                                 'border-bottom: 1px solid rgb(115, 115, 115); font-family: "Segoe UI";}'
                                 'QLabel {color: rgb(235, 235, 235); padding-top: 30px; font-family: "Segoe UI";}'
                                 'QPushButton {background-color: rgb(115, 115, 115); color: rgb(235, 235, 235);'
                                 'border-radius: 11px; padding: 5px; min-width: 5em; font-family: "Segoe UI";}'
                                 'QPushButton:pressed {background-color: rgb(53, 53, 53)}'
                                 'QPushButton:hover {border: 0.5px solid white}')
            msgBox.exec()

    def feedback_automation(self):
        """Automatically retrieves feedback templates for missing CFs."""
        # Reset radio button to default
        self.no_button.setChecked(True)
        # Clear any previous text from text boxes.
        self.student.clear()
        self.feedback_temp.clear()
        self.feedback_output.clear()
        # clear the lists used for combobox
        self.teacher_list.clear()
        self.template_list.clear()
        # clear combobox
        self.available_templates.clear()
        self.available_templates.setVisible(False)
        progress_bar = QProgressDialog('', '', 0, 100, self)
        progress_bar.setWindowModality(Qt.WindowModal)
        progress_bar.setWindowFlag(Qt.FramelessWindowHint)
        progress_bar.setAttribute(Qt.WA_TranslucentBackground)
        bar = QProgressBar()
        bar.setFixedHeight(15)
        bar.setTextVisible(False)
        progress_bar.setBar(bar)
        progress_bar.setWindowTitle('VIPKid Feedback App')
        label = QLabel('  Getting feedback template...')
        label.setStyleSheet('color: rgb(235, 235, 235); font: 14px; font-family: "Segoe UI";')
        progress_bar.setLabel(label)
        progress_bar.setStyleSheet('QProgressBar {border: 1px solid rgb(115, 115, 115); border-radius: 7px;'
                                   'background-color: rgb(36, 36, 36);}'
                                   'QProgressBar::chunk {background-color: rgb(115, 115, 115); border-radius: 6px;}')
        progress_bar.setCancelButton(None)
        progress_bar.forceShow()
        progress_bar.setValue(0)
        self.browser.refresh()
        time.sleep(1)
        progress_bar.setValue(10)
        try:
            try:
                WebDriverWait(self.browser, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div[1]/div/div[2]/div/div[3]/div[3]/div/span/div/div/div/p')))
                progress_bar.setValue(50)
                time.sleep(1)
                progress_bar.setValue(100)
                self.feedback_output.clear()
                msgBox = QMessageBox(self)
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setWindowFlag(Qt.ToolTip)
                msgBox.setText('All student feedback completed!')
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
            except TimeoutException:
                progress_bar.setValue(15)
                student_name = str(WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div/div/div[2]/div/div[3]/div[3]/table/tbody/tr[1]/td[4]/div/div/div/span'))).get_attribute('innerHTML').splitlines()[0])
                try:
                    nickname = str(self.browser.find_element_by_xpath('//*[@id="__layout"]/div/div[2]/div/div[1]/div/div[2]/div/div[3]/div[3]/table/tbody/tr[1]/td[4]/div/div/div/span/span').get_attribute('innerHTML').strip())
                    if nickname.startswith('(') and nickname.endswith(')'):
                        nickname = nickname[1:-1]
                    self.student.setText(nickname)
                except NoSuchElementException:
                    student_name = student_name.title()
                    if student_name.isupper():
                        student_name = ''.join(student_name.split()).title()
                    self.student.setText(student_name)
                progress_bar.setValue(25)
                materials_button = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='__layout']/div/div[2]/div/div[1]/div/div[2]/div/div[3]/div[3]/table/tbody/tr[1]/td[7]/div/div/div[2]")))
                self.browser.execute_script("arguments[0].click();", materials_button)
                progress_bar.setValue(35)
                print("Click materials button")
                self.browser.switch_to.window(self.browser.window_handles[1])
                progress_bar.setValue(50)
                print("Switch windows to materials browser tab")
                template_button = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.ID, 'tab-5')))
                self.browser.execute_script("arguments[0].click();", template_button)
                time.sleep(0.5)
                progress_bar.setValue(65)
                print("Click template tab on materials page")
                # Click show 'more' button until all templates are shown.
                try:
                    progress_bar.setValue(70)
                    show_more_button = WebDriverWait(self.browser, 3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__layout"]/div/div/div[3]/div/div[1]/div[1]/div[3]/section/div[2]/div[4]/div/button')))
                    progress_bar.setValue(75)
                    while show_more_button.is_displayed():
                        self.browser.execute_script("arguments[0].click()", show_more_button)
                    progress_bar.setValue(80)
                except (StaleElementReferenceException, TimeoutException):
                    pass
                time.sleep(1)
                progress_bar.setValue(90)
                # Iterate through every <li> tag, if there are any, until we find a teacher name in csv file.
                try:
                    ul_list = self.browser.find_element_by_class_name('shared-notes-list-container')
                    li_tags = ul_list.find_elements_by_tag_name('li')
                    progress_bar.setValue(95)
                    # load current liked teachers list
                    try:
                        if os.path.exists(r'C:\Users\mcmco\Desktop\Python_scripts\Feedback_GUI\app\backend_data\liked_teachers.json'):
                            with open(r'C:\Users\mcmco\Desktop\Python_scripts\Feedback_GUI\app\backend_data\liked_teachers.json', 'r') as file:
                                liked_teachers = json.load(file)
                    except Exception:
                        msgBox = QMessageBox(self)
                        msgBox.setIcon(QMessageBox.Information)
                        msgBox.setWindowFlag(Qt.ToolTip)
                        msgBox.setText('Could not find your Liked Teachers. Please try again.')
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
                    # iterate through each teacher name
                    invalid_teacher_count = int(len(li_tags))
                    for li_tag in li_tags:
                        teacher_name = li_tag.find_element_by_xpath(".//div[2]/div[1]").get_attribute('innerHTML').splitlines()[0]
                        if teacher_name in liked_teachers:
                            self.teacher_list.append(teacher_name)
                            template = str(li_tag.find_element_by_xpath(".//div[2]/div[2]").text)
                            self.template_list.append(template)
                        elif teacher_name not in liked_teachers:
                            invalid_teacher_count -= 1
                            continue
                    progress_bar.setValue(100)
                    if invalid_teacher_count != 0:
                        self.available_templates.addItems(self.teacher_list)
                        self.available_templates.setVisible(True)
                        self.feedback_temp.insertPlainText(self.template_list[0])
                    elif invalid_teacher_count == 0:
                        if len(li_tags) != 0:
                            progress_bar.close()
                            progress_bar.setAttribute(Qt.WA_DeleteOnClose, True)
                            msgBox = QMessageBox(self)
                            msgBox.setIcon(QMessageBox.Information)
                            msgBox.setWindowFlag(Qt.ToolTip)
                            msgBox.setText('No available templates from liked teachers :(\n'
                                           '\n'
                                           'Would you like to see the Top 5 templates?')
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
                                try:
                                    for li_tag in li_tags[:5]:
                                        teacher_name = li_tag.find_element_by_xpath(".//div[2]/div[1]").get_attribute('innerHTML').splitlines()[0]
                                        template = str(li_tag.find_element_by_xpath(".//div[2]/div[2]").text)
                                        self.teacher_list.append(teacher_name)
                                        self.template_list.append(template)
                                    self.available_templates.addItems(self.teacher_list)
                                    self.available_templates.setVisible(True)
                                    self.feedback_temp.insertPlainText(self.template_list[0])
                                except Exception:
                                    for li_tag in li_tags:
                                        teacher_name = li_tag.find_element_by_xpath(".//div[2]/div[1]").get_attribute('innerHTML').splitlines()[0]
                                        template = str(li_tag.find_element_by_xpath(".//div[2]/div[2]").text)
                                        self.teacher_list.append(teacher_name)
                                        self.template_list.append(template)
                                    self.available_templates.addItems(self.teacher_list)
                                    self.available_templates.setVisible(True)
                                    self.feedback_temp.insertPlainText(self.template_list[0])
                        elif len(li_tags) == 0:
                            progress_bar.close()
                            progress_bar.setAttribute(Qt.WA_DeleteOnClose, True)
                            msgBox = QMessageBox(self)
                            msgBox.setIcon(QMessageBox.Information)
                            msgBox.setWindowFlag(Qt.ToolTip)
                            msgBox.setText('No available templates from liked teachers :(')
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
                except NoSuchElementException:
                    progress_bar.close()
                    progress_bar.setAttribute(Qt.WA_DeleteOnClose, True)
                    msgBox = QMessageBox(self)
                    msgBox.setIcon(QMessageBox.Information)
                    msgBox.setWindowFlag(Qt.ToolTip)
                    msgBox.setText('No available templates from liked teachers :(')
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
                self.browser.close()
                self.browser.switch_to.window(self.browser.window_handles[0])
                if len(self.browser.window_handles) > 1:
                    self.browser.switch_to.window(self.browser.window_handles[-1])
                    self.browser.close()
                    self.browser.switch_to.window(self.browser.window_handles[0])
        except Exception as e:
            progress_bar.close()
            progress_bar.setAttribute(Qt.WA_DeleteOnClose, True)
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowFlag(Qt.ToolTip)
            msgBox.setText('There was a problem getting student feedback.')
            msgBox.setInformativeText('Please try again by clicking the "Retry" button below.')
            msgBox.setDetailedText(str(e))
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            retry_button = msgBox.button(QMessageBox.Ok)
            retry_button.setText('Retry')
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
            if msgBox.clickedButton() == retry_button:
                print('Running again..')
                self.browser.switch_to.window(self.browser.window_handles[0])
                self.browser.refresh()
                time.sleep(2)
                self.get_template_button.click()

    def available_templates_combobox(self):
        """ Each item in combobox will return its respective template"""
        index_activated = self.available_templates.currentIndex()
        self.feedback_temp.clear()
        self.feedback_temp.insertPlainText(self.template_list[index_activated])

    def login_started(self):
        gif = QMovie(':/icons/spinner')
        self.loading.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.loading.setAttribute(Qt.WA_TranslucentBackground)
        self.loading.setMovie(gif)
        gif.start()
        self.loading.show()

    def login_finished(self):
        self.loading.close()

    def login_msg(self):
        self.login_success.setVisible(True)

    def login_msg_close(self):
        self.login_success.setVisible(False)

    def login_already_msg(self):
        self.logged_in_already.setVisible(True)

    def login_already_msg_close(self):
        self.logged_in_already.setVisible(False)

    def login_button_status(self):
        self.login_button.setEnabled(True)

    def login_slots(self):
        if self.login_button_counter == 0:
            worker = WorkerThread(self.login)
            worker.signal.started.connect(self.login_started)
            worker.signal.finished.connect(self.login_finished)
            worker.signal.login_open.connect(self.login_msg)
            worker.signal.login_close.connect(self.login_msg_close)
            worker.signal.login_error.connect(self.login_error_msg)
            worker.signal.login_button.connect(self.login_button_status)
            self.threadpool.start(worker)

        else:
            worker = WorkerThreadAlreadyLogin()
            worker.signal.login_close.connect(self.login_msg_close)
            worker.signal.started.connect(self.login_already_msg)
            worker.signal.finished.connect(self.login_already_msg_close)
            self.threadpool.start(worker)

    def login_nocookies_slots(self):
        worker = WorkerThreadNoCookies(self.login_nocookies_prompt)
        worker.signal.started.connect(self.login_started)
        worker.signal.finished.connect(self.login_finished)
        worker.signal.login_open.connect(self.login_msg)
        worker.signal.login_close.connect(self.login_msg_close)
        worker.signal.login_button.connect(self.login_button_status)
        self.threadpool.start(worker)


class WorkerSignals(QObject):
    started = pyqtSignal()
    finished = pyqtSignal()
    login_open = pyqtSignal()
    login_close = pyqtSignal()
    nocookies_msg = pyqtSignal()
    login_prompt = pyqtSignal()
    login_error = pyqtSignal()
    login_button = pyqtSignal()


class WorkerThread(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(WorkerThread, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signal = WorkerSignals()

    @pyqtSlot()
    def run(self):
        self.signal.started.emit()
        try:
            self.fn(*self.args, **self.kwargs)
            self.signal.finished.emit()
            self.signal.login_open.emit()
            time.sleep(4)
            self.signal.login_close.emit()
        except Exception:
            self.signal.finished.emit()
            self.signal.login_error.emit()
            self.signal.login_button.emit()


class WorkerThreadNoCookies(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(WorkerThreadNoCookies, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signal = WorkerSignals()

    @pyqtSlot()
    def run(self):
        self.signal.started.emit()
        try:
            self.fn(*self.args, **self.kwargs)
            self.signal.finished.emit()
            self.signal.login_open.emit()
            time.sleep(5)
            self.signal.login_close.emit()
        except Exception:
            self.signal.finished.emit()
            self.signal.login_error.emit()
            self.signal.login_button.emit()


class WorkerThreadAlreadyLogin(QRunnable):
    def __init__(self, *args, **kwargs):
        super(WorkerThreadAlreadyLogin, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.signal = WorkerSignals()

    @pyqtSlot()
    def run(self):
        self.signal.login_close.emit()
        self.signal.started.emit()
        time.sleep(3)
        self.signal.finished.emit()


class SpellTextEdit(QPlainTextEdit):
    """QPlainTextEdit subclass which does spell-checking using PyEnchant"""
    def __init__(self, *args):
        QPlainTextEdit.__init__(self, *args)

        # Start with a default dictionary based on the current locale.
        self.highlighter = SpellChecker(self.document())
        self.highlighter.setDict(enchant.Dict())


class SpellChecker(QSyntaxHighlighter):
    """QSyntaxHighlighter subclass which consults a PyEnchant dictionary"""
    tokenizer = None
    token_filters = (tokenize.EmailFilter, tokenize.URLFilter)
    err_format = QTextCharFormat()
    err_format.setUnderlineColor(Qt.red)
    err_format.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)

    def __init__(self, *args):
        QSyntaxHighlighter.__init__(self, *args)

        # Initialize private members
        self._sp_dict = None
        self._chunkers = []

    def chunkers(self):
        """Gets the chunkers in use"""
        return self._chunkers

    def dict(self):
        """Gets the spelling dictionary in use"""
        return self._sp_dict

    def setChunkers(self, chunkers):
        """Sets the list of chunkers to be used"""
        self._chunkers = chunkers
        self.setDict(self.dict())

    def setDict(self, sp_dict):
        """Sets the spelling dictionary to be used"""
        try:
            self.tokenizer = tokenize.get_tokenizer(sp_dict.tag, chunkers=self._chunkers, filters=self.token_filters)
        except TokenizerNotFoundError:
            # Fall back to English tokenizer
            self.tokenizer = tokenize.get_tokenizer(chunkers=self._chunkers, filters=self.token_filters)
        self._sp_dict = sp_dict

        self.rehighlight()

    def highlightBlock(self, text):
        """Overridden QSyntaxHighlighter method to apply the highlight"""
        if not self._sp_dict:
            return

        # Build a list of all misspelled words and highlight them
        misspellings = []
        for (word, pos) in self.tokenizer(text):
            if not self._sp_dict.check(word):
                self.setFormat(pos, len(word), self.err_format)
                misspellings.append((pos, pos + len(word)))


# noinspection PyArgumentList
class QHline(QFrame):
    """creates a dark grey horizontal line break"""
    def __init__(self):
        super(QHline, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setStyleSheet('color: rgb(115, 115, 115)')


class Splashscreen:
    def __init__(self):
        start = time.time()
        splash_pix = QPixmap(':/icons/pencil_splash')
        self.splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
        self.splash.show()
        while time.time() - start < 2:
            time.sleep(0.001)
            qApp.processEvents()

    def stop(self, widget):
        self.splash.finish(widget)

