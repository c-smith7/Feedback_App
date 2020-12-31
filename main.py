import os
import pickle
import re
import sys
import time
import enchant
from enchant import tokenize
from enchant.errors import TokenizerNotFoundError
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import QPalette, QColor, QSyntaxHighlighter, QTextCharFormat
from PyQt5.QtWidgets import *
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# class ProgressBar(QProgressDialog):
#     def __init__(self):
#         super(ProgressBar, self).__init__()
#         self.setStyleSheet('QProgressBar {border: 1px solid grey; border-radius: 5px; background-color: rgb(53, 53, 53);}'
#                            'QProgressBar::chunk {background-color: rgb(200, 200, 200); border-radius: 4px;}')
#         self.setMinimum(0)
#         self.setWindowFlags(Qt.FramelessWindowHint)
#         self.setWindowModality(Qt.WindowModal)
#         self.setCancelButton(None)
#         self.setFixedHeight(10)
#         self.setTextVisible(False)
#         progress_bar.setVisible(False)


# noinspection PyArgumentList,PyTypeChecker
class Window(QWidget):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        # Window config
        self.setWindowTitle('VIPKid Feedback App')
        self.resize(500, 675)
        self.app_icon = QtGui.QIcon()
        self.app_icon.addFile('pencil.png', QtCore.QSize(16, 16))
        self.setWindowIcon(self.app_icon)
        # Create layout instance
        layout = QVBoxLayout()
        # Widgets
        self.get_template = QPushButton('Get Feedback Template')
        self.student = QLineEdit(self)
        self.yes_button = QRadioButton('&Yes')
        self.no_button = QRadioButton('&No')
        self.feedback_temp = SpellTextEdit()
        self.feedback_output = QPlainTextEdit(self)
        self.generate_output = QPushButton('Generate Feedback')
        # self.progress_bar = ProgressBar()
        # self.progress_bar = QProgressBar(self)
        # self.progress_bar.setVisible(False)
        # HBox button group
        self.hbox_buttons = QWidget()
        self.hbox_buttonsLayout = QHBoxLayout(self.hbox_buttons)
        self.copy_output = QPushButton('Copy Feedback')
        self.clear_form = QPushButton('Clear')
        self.hbox_buttonsLayout.addWidget(self.copy_output)
        self.hbox_buttonsLayout.addWidget(self.clear_form)
        # Add widgets to layout
        layout.addSpacing(7)
        layout.addWidget(self.get_template)
        layout.addSpacing(7)
        # layout.addWidget(self.progress_bar)
        # self.progress_bar.hide_bar()
        # layout.addSpacing(2)
        # layout.addWidget(self.progress_bar)
        layout.addWidget(QHline())
        layout.addSpacing(5)
        layout.addWidget(QLabel('Student Name:'))
        layout.addSpacing(2)
        layout.addWidget(self.student)
        layout.addSpacing(7)
        layout.addWidget(QLabel('New Student?'))
        layout.addWidget(self.yes_button)
        layout.addWidget(self.no_button)
        layout.addSpacing(7)
        layout.addWidget(QLabel('Feedback Template:'))
        layout.addSpacing(2)
        layout.addWidget(self.feedback_temp)
        layout.addSpacing(5)
        layout.addWidget(self.generate_output)
        layout.addSpacing(5)
        layout.addWidget(QHline())
        layout.addSpacing(5)
        layout.addWidget(QLabel('Feedback:'))
        layout.addSpacing(2)
        layout.addWidget(self.feedback_output)
        layout.addSpacing(2)
        layout.addWidget(self.hbox_buttons)
        self.setLayout(layout)
        # Button configs
        self.no_button.setChecked(True)
        self.generate_output.setDefault(True)
        self.copy_output.setDefault(True)
        self.clear_form.setDefault(True)
        self.get_template.setDefault(True)
        self.feedback_temp.setTabChangesFocus(True)
        self.feedback_output.setTabChangesFocus(True)
        self.yes_button.setFocusPolicy(Qt.NoFocus)
        self.no_button.setFocusPolicy(Qt.NoFocus)
        self.feedback_output.setFocusPolicy(Qt.NoFocus)
        # Dark mode
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        self.setPalette(palette)
        self.generate_output.setStyleSheet('QPushButton {background-color: rgb(115, 115, 115); color: rgb(235, 235, 235);'
                                           'border-radius: 12px; padding: 5px; font: bold 12px;}'
                                           'QPushButton:pressed {background-color: rgb(53, 53, 53)}'
                                           'QPushButton:hover {border: 0.5px solid white}')
        self.copy_output.setStyleSheet('QPushButton {background-color: rgb(115, 115, 115); color: rgb(235, 235, 235);'
                                       'border-radius: 12px; padding: 5px; font: bold 12px;}'
                                       'QPushButton:pressed {background-color: rgb(53, 53, 53)}'
                                       'QPushButton:hover {border: 0.5px solid white}')
        self.clear_form.setStyleSheet('QPushButton {background-color: rgb(115, 115, 115); color: rgb(235, 235, 235);'
                                      'border-radius: 12px; padding: 5px; font: bold 12px;}'
                                      'QPushButton:pressed {background-color: rgb(53, 53, 53)}'
                                      'QPushButton:hover {border: 0.5px solid white}')
        self.get_template.setStyleSheet('QPushButton {background-color: rgb(115, 115, 115); color: rgb(235, 235, 235);'
                                        'border-radius: 12px; padding: 5px; font: bold 12px;}'
                                        'QPushButton:pressed {background-color: rgb(53, 53, 53)}'
                                        'QPushButton:hover {border: 0.5px solid white}')
        self.feedback_temp.setStyleSheet('background-color: rgb(200, 200, 200); border-radius: 4px')
        self.feedback_output.setStyleSheet('background-color: rgb(200, 200, 200); border-radius: 4px')
        self.student.setStyleSheet('background-color: rgb(200, 200, 200); border-radius: 2px')
        # Tool Tips
        self.get_template.setToolTip('Automatically get feedback template')
        self.copy_output.setToolTip('Copies output to clipboard')
        self.generate_output.setToolTip('Generate feedback from template')
        self.clear_form.setToolTip('Clear student name & template')
        # self.student.setToolTip('Get template for specific student') //needed after search function implemented
        # Spell checker for PLainTextEdit boxes.
        # self.spell_check = SpellChecker(self.feedback_temp)
        # self.spell_check.setDict(enchant.Dict())
        # Signals and slots
        self.generate_output.clicked.connect(self.feedback_script)
        self.copy_output.clicked.connect(self.copy_button)
        self.clear_form.clicked.connect(self.clear_form_button)
        self.get_template.clicked.connect(self.feedback_automation_button)

    def feedback_script(self):
        global new_student
        global output
        student_name = self.student.text()
        feedback_input = self.feedback_temp.toPlainText()
        feedback_output = re.sub(' we |We', f' {student_name} and I ', feedback_input, 1)
        feedback_output = ' '.join(feedback_output.split())
        if self.yes_button.isChecked():
            new_student = 'yes'
        elif self.no_button.isChecked():
            new_student = 'no'
        if new_student == 'no':
            output = f'{feedback_output} Fantastic job today {student_name}! ' \
                     f'Keep practicing your English and working hard, you are ' \
                     f'improving every class! See you next time {student_name}. ' \
                     f'亲爱的父母，如果您喜欢今天的课程，请考虑给我一个5分的苹果评估。 这项评估对我的工作非常重要。 非常感谢! ' \
                     f'From, Teacher Carlos ZDG.'
        elif new_student == 'yes':
            output = f'{feedback_output} Fantastic job today {student_name}! ' \
                     f'It was great meeting you. Keep up the great work, and I hope ' \
                     f'to see you in my class again soon. ' \
                     f'亲爱的父母，如果您喜欢今天的课程，请考虑给我一个5分的苹果评估。 这项评估对我的工作非常重要。 非常感谢! ' \
                     f'From, Teacher Carlos ZDG.'
        if student_name == '':
            self.feedback_output.clear()
        else:
            self.feedback_output.clear()
            self.feedback_output.insertPlainText(output)

    def clear_form_button(self):
        self.student.clear()
        self.feedback_temp.clear()

    def copy_button(self):
        try:
            clipboard = QtGui.QGuiApplication.clipboard()
            clipboard.setText(output)
        except Exception:
            pass

    def feedback_automation_button(self):
        # Clear any previous text from text boxes.
        global browser
        self.student.clear()
        self.feedback_temp.clear()
        if os.path.exists('cookie'):
            progress_bar = QProgressDialog('', '', 0, 100, self)
            progress_bar.setWindowModality(Qt.WindowModal)
            progress_bar.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
            progress_bar.setFixedWidth(375)
            progress_bar.setFixedHeight(80)
            bar = QProgressBar()
            bar.setFixedHeight(15)
            bar.setTextVisible(False)
            progress_bar.setBar(bar)
            progress_bar.setWindowTitle('VIPKid Feedback App')
            label = QLabel('Getting feedback template...')
            label.setStyleSheet('color: rgb(200, 200, 200); font: 12px')
            progress_bar.setLabel(label)
            progress_bar.setStyleSheet('QProgressDialog {background-color: rgb(53, 53, 53);}'
                                       'QProgressBar {border: 1px solid grey; border-radius: 7px;'
                                       'background-color: rgb(53, 53, 53);}'
                                       'QProgressBar::chunk {background-color: rgb(200, 200, 200); border-radius: 6px;}')
            progress_bar.setCancelButton(None)
            progress_bar.forceShow()
            progress_bar.setValue(0)
            try:
                options = Options()
                options.headless = True
                browser = webdriver.Chrome(options=options)
                progress_bar.setValue(5)
                browser.get('https://www.vipkid.com/login?prevUrl=https%3A%2F%2Fwww.vipkid.com%2Ftc%2Fmissing')
                print('Headless browser started!')
                progress_bar.setValue(10)
                with open('cookie', 'rb') as cookiesfile:
                    cookies = pickle.load(cookiesfile)
                    for cookie in cookies:
                        browser.add_cookie(cookie)
                    browser.refresh()
                    progress_bar.setValue(20)
                    missing_cf_button = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'to-do-type')))
                    browser.execute_script("arguments[0].click();", missing_cf_button)
                    print('Logged In!')
                    progress_bar.setValue(35)
                    time.sleep(1)
                # Get student name, if there is one.
                try:
                    browser.find_element_by_xpath('//*[@id="__layout"]/div/div[2]/div/div[1]/div/div[2]/div/div[3]/div[3]/div/span/div/div/div/p')
                    progress_bar.close()
                    progress_bar.setAttribute(Qt.WA_DeleteOnClose, True)
                    msgBox = QMessageBox(self)
                    msgBox.setIcon(QMessageBox.Information)
                    msgBox.setText('All student feedback completed!')
                    msgBox.setWindowTitle('VIPKid Feedback App')
                    msgBox_icon = QtGui.QIcon()
                    msgBox_icon.addFile('pencil.png', QtCore.QSize(16, 16))
                    msgBox.setWindowIcon(msgBox_icon)
                    msgBox.setStandardButtons(QMessageBox.Ok)
                    msgBox.setDefaultButton(QMessageBox.Ok)
                    msgBox.setStyleSheet('background-color: rgb(53, 53, 53); color: rgb(235, 235, 235);')
                    msgBox.exec()
                    browser.quit()
                except NoSuchElementException:
                    print("There are feedbacks due.")
                    progress_bar.setValue(40)
                    student_name = str(WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div/div/div[2]/div/div[3]/div[3]/table/tbody/tr[1]/td[4]/div/div/div/span'))).get_attribute('innerHTML').splitlines()[0])
                    student_name = student_name.title()
                    if student_name.isupper():
                        student_name = ''.join(student_name.split()).title()
                    # print(student_name)
                    self.student.setText(student_name)
                    progress_bar.setValue(55)
                # Navigate to templates window
                    materials_button = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='__layout']/div/div[2]/div/div[1]/div/div[2]/div/div[3]/div[3]/table/tbody/tr[1]/td[7]/div/div/div[2]")))
                    browser.execute_script("arguments[0].click();", materials_button)
                    progress_bar.setValue(65)
                    # print('materials button clicked.')
                    browser.switch_to.window(browser.window_handles[-1])
                    template_button = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='tab-5']")))
                    browser.execute_script("arguments[0].click();", template_button)
                    progress_bar.setValue(70)
                    # print('template button clicked.')
                    time.sleep(1)
                    # Click show 'more' button until all templates are shown.
                    show_more_button = browser.find_element_by_xpath("//*[@id='__layout']/div/div/div[3]/div/div[1]/div[1]/div[2]/section/div[2]/div[4]/div/button")
                    try:
                        while show_more_button.is_displayed():
                            browser.execute_script("arguments[0].click()", show_more_button)
                    except StaleElementReferenceException:
                        time.sleep(1)
                    progress_bar.setValue(85)
                    # print('all templates showing.')
                    # Iterate through every <li> tag until we find a teacher name in csv file.
                    ul_list = browser.find_element_by_class_name('shared-notes-list-container')
                    li_tags = ul_list.find_elements_by_tag_name('li')
                    valid_teachers = ['Katie EAV', 'Tammy PHT', 'Amber MZC', 'Andrew BAR', 'Kimberly BDP', 'Miranda CR',
                                      'Richard ZZ', 'Tomas B', 'Stefanie BD', 'Kristina EB', 'Jessica XH', 'Thomas CH']
                    invalid_teacher_count = int(len(li_tags))
                    progress_bar.setValue(90)
                    for li_tag in li_tags:
                        teacher_name = li_tag.find_element_by_xpath(".//div[2]/div[1]").get_attribute('innerHTML').splitlines()[0]
                        if teacher_name in valid_teachers:
                            template = str(li_tag.find_element_by_xpath(".//div[2]/div[2]").text)
                            # print(template)
                            self.feedback_temp.insertPlainText(template)
                            progress_bar.setValue(100)
                            break
                        elif teacher_name not in valid_teachers:
                            invalid_teacher_count -= 1
                            continue
                    if invalid_teacher_count == 0:
                        progress_bar.close()
                        progress_bar.setAttribute(Qt.WA_DeleteOnClose, True)
                        msgBox = QMessageBox(self)
                        msgBox.setIcon(QMessageBox.Information)
                        msgBox.setText('No valid teacher templates :(')
                        msgBox.setWindowTitle('VIPKid Feedback App')
                        msgBox_icon = QtGui.QIcon()
                        msgBox_icon.addFile('pencil.png', QtCore.QSize(16, 16))
                        msgBox.setWindowIcon(msgBox_icon)
                        msgBox.setStandardButtons(QMessageBox.Ok)
                        msgBox.setDefaultButton(QMessageBox.Ok)
                        msgBox.setStyleSheet('background-color: rgb(53, 53, 53); color: rgb(235, 235, 235);')
                        msgBox.exec()
                    browser.quit()
            except Exception as e:
                progress_bar.close()
                progress_bar.setAttribute(Qt.WA_DeleteOnClose, True)
                msgBox = QMessageBox(self)
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setText('There was a problem getting student feedback.')
                msgBox.setInformativeText('Please try again by clicking the "Retry" button below.\n'
                                          '\n'
                                          'If issue persists after trying several times, please email *****')
                msgBox.setDetailedText(f'{e}')
                msgBox.setWindowTitle('VIPKid Feedback App')
                msgBox_icon = QtGui.QIcon()
                msgBox_icon.addFile('pencil.png', QtCore.QSize(16, 16))
                msgBox.setWindowIcon(msgBox_icon)
                msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                retry_button = msgBox.button(QMessageBox.Ok)
                retry_button.setText('Retry')
                msgBox.setDefaultButton(QMessageBox.Ok)
                msgBox.setStyleSheet('background-color: rgb(53, 53, 53); color: rgb(235, 235, 235);')
                msgBox.exec()
                if msgBox.clickedButton() == retry_button:
                    browser.quit()
                    print('Running again..')
                    self.get_template.click()
                else:
                    browser.quit()
        else:
            try:
                msgBox = QMessageBox(self)
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setText('Please login to VIPKid Website.')
                msgBox.setInformativeText('Click "Login" button below, and a separate window will open to login.\n'
                                          '\n'
                                          'You will only need to log into VIPKid once.\n'
                                          'From now on, you will NOT need to login when you use this app.')
                msgBox.setWindowTitle('VIPKid Feedback App')
                msgBox_icon = QtGui.QIcon()
                msgBox_icon.addFile('pencil.png', QtCore.QSize(16, 16))
                msgBox.setWindowIcon(msgBox_icon)
                msgBox.setStandardButtons(QMessageBox.Ok)
                ok_button = msgBox.button(QMessageBox.Ok)
                ok_button.setText('Login')
                msgBox.setDefaultButton(QMessageBox.Ok)
                msgBox.setStyleSheet('background-color: rgb(53, 53, 53); color: rgb(235, 235, 235);')
                msgBox.exec()
                browser = webdriver.Chrome()
                browser.get('https://www.vipkid.com/login?prevUrl=https%3A%2F%2Fwww.vipkid.com%2Ftc%2Fmissing')
                # Wait for user login.
                WebDriverWait(browser, 300).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div/ul/li[2]/a')))
                time.sleep(1)
                # Save cookies file after login
                with open('cookie', 'wb') as file:
                    pickle.dump(browser.get_cookies(), file)
                # Get student name if there is one.
                try:
                    browser.find_element_by_xpath('//*[@id="__layout"]/div/div[2]/div/div[1]/div/div[2]/div/div[3]/div[3]/div/span/div/div/div/p')
                    msgBox = QMessageBox(self)
                    msgBox.setIcon(QMessageBox.Information)
                    msgBox.setText('All student feedback completed!')
                    msgBox.setWindowTitle('VIPKid Feedback App')
                    msgBox_icon = QtGui.QIcon()
                    msgBox_icon.addFile('pencil.png', QtCore.QSize(16, 16))
                    msgBox.setWindowIcon(msgBox_icon)
                    msgBox.setStandardButtons(QMessageBox.Ok)
                    msgBox.setDefaultButton(QMessageBox.Ok)
                    msgBox.setStyleSheet('background-color: rgb(53, 53, 53); color: rgb(235, 235, 235);')
                    msgBox.exec()
                    browser.quit()
                except NoSuchElementException:
                    # print("There are feedbacks due.")
                    student_name = str(WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div/div/div[2]/div/div[3]/div[3]/table/tbody/tr[1]/td[4]/div/div/div/span'))).get_attribute('innerHTML').splitlines()[0])
                    student_name = student_name.title()
                    # print(student_name)
                    self.student.setText(student_name)
                    # Navigate to templates window
                    materials_button = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div[1]/div/div[2]/div/div[3]/div[3]/table/tbody/tr[1]/td[7]/div/div/div[2]')))
                    browser.execute_script("arguments[0].click();", materials_button)
                    # print('materials button clicked.')
                    browser.switch_to.window(browser.window_handles[-1])
                    browser.minimize_window()
                    time.sleep(1)
                    template_button = browser.find_element_by_xpath("//*[@id='tabb-5']")
                    browser.execute_script("arguments[0].click();", template_button)
                    # print('template button clicked.')
                    time.sleep(1)
                    # Click show 'more' button until all templates are shown.
                    show_more_button = browser.find_element_by_xpath("//*[@id='__layout']/div/div/div[3]/div/div[1]/div[1]/div[2]/section/div[2]/div[4]/div/button")
                    try:
                        while show_more_button.is_displayed():
                            browser.execute_script("arguments[0].click()", show_more_button)
                    except StaleElementReferenceException:
                        time.sleep(1)
                    # print('all templates showing.')
                    # Iterate through every <li> tag until we find a teacher name in csv file.
                    ul_list = browser.find_element_by_class_name('shared-notes-list-container')
                    li_tags = ul_list.find_elements_by_tag_name('li')
                    valid_teachers = ['Katie EAV', 'Tammy PHT', 'Amber MZC', 'Andrew BAR', 'Kimberly BDP', 'Miranda CR',
                                      'Richard ZZ', 'Tomas B', 'Stefanie BD', 'Kristina EB', 'Jessica XH', 'Thomas CH']
                    non_valid_teacher_count = int(len(li_tags))
                    for li_tag in li_tags:
                        teacher_name = li_tag.find_element_by_xpath(".//div[2]/div[1]").get_attribute('innerHTML').splitlines()[0]
                        if teacher_name in valid_teachers:
                            template = str(li_tag.find_element_by_xpath(".//div[2]/div[2]").text)
                            # print(template)
                            self.feedback_temp.insertPlainText(template)
                            break
                        elif teacher_name not in valid_teachers:
                            non_valid_teacher_count -= 1
                            continue
                    if non_valid_teacher_count == 0:
                        msgBox = QMessageBox(self)
                        msgBox.setIcon(QMessageBox.Information)
                        msgBox.setText('No valid teacher templates :(')
                        msgBox.setWindowTitle('VIPKid Feedback App')
                        msgBox_icon = QtGui.QIcon()
                        msgBox_icon.addFile('pencil.png', QtCore.QSize(16, 16))
                        msgBox.setWindowIcon(msgBox_icon)
                        msgBox.setStandardButtons(QMessageBox.Ok)
                        msgBox.setDefaultButton(QMessageBox.Ok)
                        msgBox.setStyleSheet('background-color: rgb(53, 53, 53); color: rgb(235, 235, 235);')
                        msgBox.exec()
                    browser.quit()
            except Exception as e:
                msgBox = QMessageBox(self)
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setText('There was a problem getting student feedback..')
                msgBox.setInformativeText('Please try again by clicking the "Retry" button below.')
                msgBox.setDetailedText(f'{e}\n'
                                       'If the issue persists after trying several times to get student feedback,\n'
                                       'please email *****')
                msgBox.setWindowTitle('VIPKid Feedback App')
                msgBox_icon = QtGui.QIcon()
                msgBox_icon.addFile('pencil.png', QtCore.QSize(16, 16))
                msgBox.setWindowIcon(msgBox_icon)
                msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                retry_button = msgBox.button(QMessageBox.Ok)
                retry_button.setText('Retry')
                msgBox.setDefaultButton(QMessageBox.Ok)
                msgBox.setStyleSheet('background-color: rgb(53, 53, 53); color: rgb(235, 235, 235);')
                msgBox.exec()
                if msgBox.clickedButton() == retry_button:
                    browser.quit()
                    print('Running again..')
                    self.get_template.click()
                else:
                    browser.quit()


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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
