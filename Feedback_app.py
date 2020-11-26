import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import *


class Window(QWidget):
    def __init__(self):
        super().__init__()
        # Window options
        self.setWindowIcon(QtGui.QIcon('vipkid.png'))
        self.setWindowTitle('VIPKid Feedback App')
        self.resize(425, 500)
        # Create layout instance
        layout = QVBoxLayout()
        # Add widgets to layout
        layout.addWidget(QLabel('Student Name:'))
        layout.addWidget(QLineEdit())
        layout.addSpacing(4)
        layout.addWidget(QLabel('New Student?'))
        layout.addWidget(QRadioButton('Yes'))
        layout.addWidget(QRadioButton('No'))
        layout.addSpacing(4)
        layout.addWidget(QLabel('Feedback Template:'))
        layout.addWidget(QTextEdit())
        layout.addSpacing(4)
        layout.addWidget(QLabel('Output Feedback:'))
        layout.addWidget(QTextEdit())
        layout.addSpacing(2)
        # Alt. method for addWidget
        student_name = QPushButton('Copy Output Feedback')
        layout.addWidget(student_name)
        self.setLayout(layout)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())