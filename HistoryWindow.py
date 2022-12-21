#! python3
# HistoryWindow.py

from PySide6.QtWidgets import QWidget, QDialogButtonBox, QAbstractItemView
from PySide6.QtGui import QStandardItem
from PySide6.QtCore import Qt
from PySide6.QtSql import QSqlDatabase, QSqlTableModel

import pyMagSafeSQLI
from UI_HistoryWindow import Ui_hist_window

conn = pyMagSafeSQLI.conn


class StandardItem(QStandardItem):
    def __init__(self, txt=""):
        super().__init__()
        txt = str(txt)
        self.setText(txt)
        self.setEditable(False)


class HistoryWindow(QWidget, Ui_hist_window):
    def __init__(self):
        super().__init__()
        self.setObjectName("History")
        self.setupUi(self)

        self.main_win = self.parent()

        # create the history model
        model = self.create_hist_model()

        # create treeview to hold the torrent history
        self.treeView.setModel(model)
        self.treeView.setSortingEnabled(True)
        self.treeView.setSelectionMode(QAbstractItemView.MultiSelection)
        self.treeView.resizeColumnToContents(0)
        self.treeView.header().resizeSection(2, 500)
        self.treeView.resizeColumnToContents(1)
        self.treeView.resizeColumnToContents(3)
        self.treeView.resizeColumnToContents(4)

        # close hist_window button
        self.buttonBox.button(QDialogButtonBox.Close).clicked.connect(self.close)

        # resend selection to main window button
        self.buttonBox.button(QDialogButtonBox.Retry).setText("Resend")

        # clear selection button
        self.buttonBox.button(QDialogButtonBox.Reset).clicked.connect(self.treeView.clearSelection)
        self.buttonBox.button(QDialogButtonBox.Reset).setText("Clear Selection")

        # refresh button
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.refresh_hist)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).setText("Refresh")

    def create_hist_model(self):
        # initialize the model to store the torrent history
        model = QSqlTableModel(self)
        model.setTable("torrent_magnet")
        model.setHeaderData(0, Qt.Horizontal, "ID")
        model.setHeaderData(1, Qt.Horizontal, "Torrent")
        model.setHeaderData(2, Qt.Horizontal, "Magnet")
        model.setHeaderData(3, Qt.Horizontal, "Create_DT")
        model.setHeaderData(4, Qt.Horizontal, "Update_DT")
        return model

    def refresh_hist(self):
        model = self.create_hist_model()
        self.treeView.setModel(model)
