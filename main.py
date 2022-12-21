from PySide6.QtWidgets import QApplication

import pyMagSafeSQLI
from MainWindow import MainWindow
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # initialize database
    pyMagSafeSQLI.create_table(pyMagSafeSQLI.sql_create_config_table)
    pyMagSafeSQLI.create_table(pyMagSafeSQLI.sql_create_torrent_magnet_table)

    window = MainWindow()
    window.show()

    # start the event loop
    app.exec()
