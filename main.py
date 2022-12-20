from PySide6.QtWidgets import QApplication

import pyMagSafeSQLI
from MainWindow import MainWindow
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # initialize database
    conn = pyMagSafeSQLI.create_connection()
    pyMagSafeSQLI.create_table(conn, pyMagSafeSQLI.sql_create_config_table)
    pyMagSafeSQLI.create_table(conn, pyMagSafeSQLI.sql_create_magnet_table)
    pyMagSafeSQLI.create_table(conn, pyMagSafeSQLI.sql_create_torrent_table)
    pyMagSafeSQLI.close_db(conn)

    window = MainWindow()
    window.show()

    # start the event loop
    app.exec()
