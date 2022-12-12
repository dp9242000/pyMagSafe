#! python3
# history_window.py

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt

import pyMagSafeGui
from HistoryWindow import Ui_hist_window


class StandardItem(QStandardItem):
    def __init__(self, txt=""):
        super().__init__()
        self.setText(txt)
        self.setEditable(False)

class HistoryWindow(QWidget, Ui_hist_window):
    def __init__(self):
        super().__init__()
        self.setObjectName("History")
        self.setupUi(self)

        history = pyMagSafeGui.read_hist()
        model = self.create_hist_model(self)
        self.add_hist(model, history)

        self.treeView.setModel(model)
        self.treeView.header().resizeSection(0, 180)
        self.treeView.header().resizeSection(1, 250)
        self.treeView.header().resizeSection(2, 500)
        self.treeView.setSortingEnabled(True)

    def create_hist_model(self, parent):
        model = QStandardItemModel(0, 3, self)
        model.setHeaderData(0, Qt.Horizontal, "Date")
        model.setHeaderData(1, Qt.Horizontal, "Torrent")
        model.setHeaderData(2, Qt.Horizontal, "Magnet")
        return model

    def add_hist(self, model, history):
        hist_keys = history.keys()
        for item in hist_keys:
            torrents = history.get(item)
            for torrent, magnet in torrents:
                model.appendRow([StandardItem(item), StandardItem(torrent), StandardItem(magnet)])
