from PySide6.QtWidgets import QApplication
from ui_mainwindow import MainWindow
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
