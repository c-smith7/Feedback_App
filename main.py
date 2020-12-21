import sys
import re
import time
import pickle
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import *
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.chrome.options import Options


class Window(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Window config
        self.setWindowTitle('VIPKid Feedback App')
        self.resize(425, 500)
        app_icon = QtGui.QIcon()
        app_icon.addFile('pencil.png', QtCore.QSize(16, 16))
        self.setWindowIcon(app_icon)
        # Create layout instance
        layout = QVBoxLayout()
        # Widgets
        self.get_template = QPushButton('Get Feedback Template')
        self.student = QLineEdit(self)
        self.yes_button = QRadioButton('&Yes')
        self.no_button = QRadioButton('&No')
        self.feedback_temp = QPlainTextEdit(self)
        self.feedback_output = QPlainTextEdit(self)
        self.generate_output = QPushButton('Generate Feedback')
        self.copy_output = QPushButton('Copy Output Feedback')
        self.clear_form = QPushButton('Clear Form')
        # Add widgets to layout
        layout.addWidget(self.get_template)
        layout.addWidget(QLabel('Student Name:'))
        layout.addWidget(self.student)
        layout.addSpacing(4)
        layout.addWidget(QLabel('New Student?'))
        layout.addWidget(self.yes_button)
        layout.addWidget(self.no_button)
        layout.addSpacing(4)
        layout.addWidget(QLabel('Feedback Template:'))
        layout.addWidget(self.feedback_temp)
        layout.addSpacing(2)
        layout.addWidget(self.generate_output)
        layout.addSpacing(4)
        layout.addWidget(QLabel('Output Feedback:'))
        layout.addWidget(self.feedback_output)
        layout.addSpacing(2)
        layout.addWidget(self.copy_output)
        layout.addWidget(self.clear_form)
        self.setLayout(layout)
        # Button configs
        self.no_button.setChecked(True)
        self.generate_output.setDefault(True)
        self.copy_output.setDefault(True)
        self.clear_form.setDefault(True)
        self.feedback_temp.setTabChangesFocus(True)
        self.feedback_output.setTabChangesFocus(True)
        self.yes_button.setFocusPolicy(Qt.NoFocus)
        self.no_button.setFocusPolicy(Qt.NoFocus)
        self.feedback_output.setFocusPolicy(Qt.NoFocus)
        # Dark theme
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        self.setPalette(palette)
        self.generate_output.setStyleSheet('background-color: rgb(115, 115, 115); color: rgb(235, 235, 235);')
        self.copy_output.setStyleSheet('background-color: rgb(115, 115, 115); color: rgb(235, 235, 235);')
        self.clear_form.setStyleSheet('background-color: rgb(115, 115, 115); color: rgb(235, 235, 235);')
        self.get_template.setStyleSheet('background-color: rgb(115, 115, 115); color: rgb(235, 235, 235);')
        self.feedback_temp.setStyleSheet('background-color: rgb(200, 200, 200)')
        self.feedback_output.setStyleSheet('background-color: rgb(200, 200, 200)')
        self.student.setStyleSheet('background-color: rgb(200, 200, 200)')
        # Signals and slots
        # self.feedback_script()
        self.generate_output.clicked.connect(self.feedback_script)
        self.copy_output.clicked.connect(self.copy_button)
        self.clear_form.clicked.connect(self.clear_form_button)
        self.get_template.clicked.connect(self.feedback_automation_button)

    def feedback_script(self):
        global new_student
        global output
        student_name = self.student.text()
        feedback_input = self.feedback_temp.toPlainText()
        feedback_output = re.sub('we|We', f'{student_name} and I', feedback_input, 1)
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
        clipboard = QtGui.QGuiApplication.clipboard()
        clipboard.setText(output)

    def feedback_automation_button(self):
        options = Options()
        options.headless = True
        browser = webdriver.Chrome(options=options)
        browser.get('https://www.vipkid.com/login?prevUrl=https%3A%2F%2Fwww.vipkid.com%2Ftc%2Fmissing')
        # Clear any previous text from text boxes.
        self.student.clear()
        self.feedback_temp.clear()
        # Add cookies to login to teacher portal.
        try:
            with open('cookie', 'rb') as cookiesfile:
                cookies = pickle.load(cookiesfile)
                for cookie in cookies:
                    browser.add_cookie(cookie)
                browser.refresh()
                missing_cf_button = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'to-do-type')))
                missing_cf_button.click()
        except Exception:
            print("Login to save cookies.")
        # Save cookies file after login
        with open('cookie', 'wb') as file:
            pickle.dump(browser.get_cookies(), file)
        # Get student name
        try:
            student_name = str(WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div/div/div[2]/div/div[3]/div[3]/table/tbody/tr[1]/td[4]/div/div/div/span'))).get_attribute('innerHTML').splitlines()[0])
            student_name = student_name.title()
            self.student.setText(student_name)  # populate this name in 'student name' box in GUI.
        except TimeoutException:
            pop_up = QMessageBox()
            pop_up.setText('All student feedback completed!')
            pop_up.addButton(QPushButton('OK'), QMessageBox.Close)
            browser.quit()
        # Navigate to templates window
        materials_button = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div[1]/div/div[2]/div/div[3]/div[3]/table/tbody/tr[1]/td[7]/div/div/div[2]')))
        materials_button.click()
        browser.switch_to.window(browser.window_handles[-1])
        time.sleep(1)
        template_button = browser.find_element_by_xpath("//*[@id='tab-5']")
        browser.execute_script("arguments[0].click();", template_button)
        time.sleep(1)
        # Click show 'more' button until all templates are shown.
        show_more_button = browser.find_element_by_xpath("//*[@id='__layout']/div/div/div[3]/div/div[1]/div[1]/div[2]/section/div[2]/div[4]/div/button")
        try:
            while show_more_button.is_displayed():
                browser.execute_script("arguments[0].click()", show_more_button)
        except StaleElementReferenceException:
            time.sleep(1)
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
                self.feedback_temp.insertPlainText(template)
                break
            elif teacher_name not in valid_teachers:
                non_valid_teacher_count -= 1
                continue
        if non_valid_teacher_count == 0:
            pop_up = QMessageBox()
            pop_up.setText('No valid teacher templates :(')
            pop_up.addButton(QPushButton('OK'), QMessageBox.Close)
        browser.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
