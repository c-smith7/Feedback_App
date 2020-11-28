import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import QKeySequence
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
        layout.addSpacing(4)
        layout.addWidget(QLabel('Output Feedback:'))
        layout.addWidget(self.feedback_output)
        layout.addSpacing(2)
        layout.addWidget(self.copy_output)
        self.setLayout(layout)
        self.no_button.setChecked(True)
        self.copy_output.setDefault(True)
        self.feedback_temp.setTabChangesFocus(True)
        self.feedback_output.setTabChangesFocus(True)
        self.yes_button.setFocusPolicy(Qt.NoFocus)
        self.no_button.setFocusPolicy(Qt.NoFocus)
        self.feedback_script()
        self.copy_output.clicked.connect(self.feedback_script)

    def feedback_script(self):
        global new_student
        new_student = ''
        student_name = self.student.text()
        feedback = self.feedback_temp.toPlainText()
        if self.yes_button.isChecked():
            new_student = self.yes_button.text()
        self.feedback_output.insertPlainText(new_student)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())