#! python3
# HistoryWindow.py

from PySide6.QtWidgets import QWidget, QDialogButtonBox, QAbstractItemView
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt

import pyMagSafeGui
from UI_HistoryWindow import Ui_hist_window


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

        # retrieve the torrent history and build the model
        history = pyMagSafeGui.read_hist()
        model = self.create_hist_model()
        self.add_hist(model, history)

        # create treeview to hold the torrent history
        self.treeView.setModel(model)
        self.treeView.header().resizeSection(0, 180)
        self.treeView.header().resizeSection(1, 250)
        self.treeView.header().resizeSection(2, 500)
        self.treeView.setSortingEnabled(True)
        self.treeView.setSelectionMode(QAbstractItemView.MultiSelection)

        # close hist_window button
        self.buttonBox.button(QDialogButtonBox.Close).clicked.connect(self.close)

        # resend selection to main window button
        self.buttonBox.button(QDialogButtonBox.Retry).setText("Resend")

        # clear selection button
        self.buttonBox.button(QDialogButtonBox.Reset).clicked.connect(self.treeView.clearSelection)
        self.buttonBox.button(QDialogButtonBox.Reset).setText("Clear Selection")

        # refresh history button
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.refresh_hist)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).setText("Refresh")

    def create_hist_model(self):
        # initialize the model to store the torrent history
        model = QStandardItemModel(0, 3, self)
        model.setHeaderData(0, Qt.Horizontal, "Date")
        model.setHeaderData(1, Qt.Horizontal, "Torrent")
        model.setHeaderData(2, Qt.Horizontal, "Magnet")
        return model

    def add_hist(self, model, history):
        # add the history to the model
        hist_keys = history.keys()
        for item in hist_keys:
            torrents = history.get(item)
            for torrent, magnet in torrents:
                model.appendRow([StandardItem(item), StandardItem(torrent), StandardItem(magnet)])

    def refresh_hist(self):
        # while self.treeView.model().rowCount() > 0:
        #     self.treeView.model().removeRow(0)
        history = pyMagSafeGui.read_hist()
        model = self.create_hist_model()
        self.add_hist(model, history)
        self.treeView.setModel(model)
