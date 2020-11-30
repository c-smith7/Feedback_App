import sys

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import *


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
        self.student = QLineEdit(self)
        self.yes_button = QRadioButton('&Yes')
        self.no_button = QRadioButton('&No')
        self.feedback_temp = QPlainTextEdit(self)
        self.feedback_output = QPlainTextEdit(self)
        self.generate_output = QPushButton('Generate Feedback')
        self.copy_output = QPushButton('Copy Output Feedback')
        # Add widgets to layout
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
        self.setLayout(layout)
        # Button configs
        self.no_button.setChecked(True)
        self.generate_output.setDefault(True)
        self.copy_output.setDefault(True)
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
        self.feedback_temp.setStyleSheet('background-color: rgb(200, 200, 200)')
        self.feedback_output.setStyleSheet('background-color: rgb(200, 200, 200)')
        self.student.setStyleSheet('background-color: rgb(200, 200, 200)')
        # Signals and slots
        self.feedback_script()
        copy_button()
        self.generate_output.clicked.connect(self.feedback_script)
        self.copy_output.clicked.connect(copy_button)

    def feedback_script(self):
        global new_student
        global output
        student_name = self.student.text()
        feedback_input = self.feedback_temp.toPlainText()
        feedback_output = feedback_input.replace('we', f'{student_name} and I', 1)
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


def copy_button():
    clipboard = QtGui.QGuiApplication.clipboard()
    clipboard.setText(output)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
