import sys

from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Window(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Window options
        self.setWindowIcon(QtGui.QIcon('vipkid.png'))
        self.setWindowTitle('VIPKid Feedback App')
        self.resize(425, 500)
        # Create layout instance
        layout = QVBoxLayout()
        # Widgets
        self.student = QLineEdit(self)
        self.yes_button = QRadioButton('&Yes')
        self.no_button = QRadioButton('&No')
        self.feedback_temp = QTextEdit(self)
        self.feedback_output = QTextEdit(self)
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
        self.no_button.setChecked(True)
        self.generate_output.setDefault(True)
        self.copy_output.setDefault(True)
        self.feedback_temp.setTabChangesFocus(True)
        self.feedback_output.setTabChangesFocus(True)
        self.yes_button.setFocusPolicy(Qt.NoFocus)
        self.no_button.setFocusPolicy(Qt.NoFocus)
        self.feedback_output.setFocusPolicy(Qt.NoFocus)
        self.feedback_script()
        copy_button()
        self.generate_output.clicked.connect(self.feedback_script)
        self.copy_output.clicked.connect(copy_button)

    def feedback_script(self):
        global new_student
        global output
        new_student = ''
        student_name = self.student.text()
        feedback_input = self.feedback_temp.toPlainText()
        feedback_output = feedback_input.replace('we', f'{student_name} and I', 1)
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
            self.feedback_output.insertPlainText(output)


def copy_button():
    clipboard = QtGui.QGuiApplication.clipboard()
    clipboard.setText(output)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())