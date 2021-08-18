import time
from PyQt5 import Qt, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QSplashScreen, qApp


class Splashscreen:
    def __init__(self):
        start = time.time()
        splash_pix = QPixmap('../icons/pencil_432x432.png')
        self.splash = QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
        self.splash.show()
        while time.time() - start < 2:
            time.sleep(0.001)
            qApp.processEvents()

    def stop(self, widget):
        self.splash.finish(widget)
