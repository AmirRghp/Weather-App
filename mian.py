from PyQt5.QtWidgets import QApplication
import sys
from images import images_rc
from ui.Weather import Weather

if __name__ == '__main__':
    app = QApplication(sys.argv)
    UIWindow = Weather()
    UIWindow.show()
    app.exec_()