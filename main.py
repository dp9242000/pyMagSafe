#! python3
# main.py

from PySide6.QtWidgets import QApplication

from MainWindow import MainWindow
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    # start the event loop
    app.exec()
