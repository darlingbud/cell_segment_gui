import os
import sys
import webbrowser
from PyQt5.QtCore import QSize, Qt, QUrl, QTimer, pyqtSignal,QCoreApplication

from windows import *

if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    mw = Mainwin()
    mw.show()
    sys.exit(app.exec_())
