#! python3
# MainWindow.py

from PySide6.QtWidgets import (QMainWindow, QWidget, QPushButton, QStatusBar, QAbstractItemView,
                               QVBoxLayout, QFileDialog, QTreeView, QDialogButtonBox)
from PySide6.QtGui import QAction, QStandardItemModel, QCloseEvent
from PySide6.QtCore import Qt
import os

import pyMagSafeGui
from HistoryWindow import HistoryWindow, StandardItem


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("pyMagSafe")
        self.resize(600, 500)

        # initialize holder for history window
        self.hist_window = None

        # Send to Deluge button
        self.button = QPushButton("Send to Deluge")
        self.button.clicked.connect(self.go_button_clicked)
        self.button.setStatusTip("Send all .magnets in list to Deluge")

        # File list widget
        self.fname = QTreeView()
        # history = pyMagSafeGui.read_hist()
        self.model = QStandardItemModel(0, 2, self)
        self.model.setHeaderData(0, Qt.Horizontal, "Torrent")
        self.model.setHeaderData(1, Qt.Horizontal, "Magnet")
        # self.add_hist(model, history)

        self.fname.setModel(self.model)
        self.fname.header().resizeSection(0, 250)
        self.fname.header().resizeSection(1, 250)
        self.fname.setSortingEnabled(True)
        self.fname.setSelectionMode(QAbstractItemView.MultiSelection)

        # file open dialog button
        self.dlgButton = QPushButton("Select File(s)...")
        self.dlgButton.setStatusTip("Open dialog to select .magnet files")
        self.dlgButton.clicked.connect(self.dlg_button_clicked)

        # layout
        layout = QVBoxLayout()
        layout.addWidget(self.fname)
        layout.addWidget(self.dlgButton)
        layout.addWidget(self.button)

        window = QWidget()
        window.setLayout(layout)

        self.setCentralWidget(window)

        # # initialize toolbar
        # toolbar = QToolBar("Tools")
        # # toolbar.toggleViewAction().setEnabled(False)
        # self.addToolBar(toolbar)

        # create history action to use in toolbar and/or menus
        hist_button_action = QAction("&History", self)
        hist_button_action.setStatusTip("View old magnets")
        hist_button_action.triggered.connect(self.hist_button_clicked)

        self.setStatusBar(QStatusBar(self))

        self.menu = self.menuBar()

        menu_menu = self.menu.addMenu("&Menu")
        menu_menu.addAction(hist_button_action)

    def add_mag(self, magnets):
        for torrent, magnet in magnets:
            self.model.appendRow([StandardItem(torrent), StandardItem(magnet)])

    def go_button_clicked(self):
        self.fname.selectAll()
        magnets = []
        while self.fname.model().rowCount() > 0:
            magnet = self.fname.model().index(0, 1)
            magnet = magnet.model().itemFromIndex(magnet).text()
            magnets.append(magnet)
            self.fname.model().removeRow(0)
        pyMagSafeGui.send_to_deluge(magnets)
        self.fname.clearSelection()

    def dlg_button_clicked(self):
        filter = "magnet(*.magnet)"
        config = pyMagSafeGui.read_config()
        path = config.get("Default Path", os.path.expanduser(""))
        path = os.path.abspath(path)
        dlg = QFileDialog(self)
        dlg.setDirectory(path)
        dlg.setFileMode(QFileDialog.FileMode.ExistingFile)
        file = dlg.getOpenFileNames(self, filter=filter, dir=path)
        magnets = pyMagSafeGui.read_magnets(file[0])
        self.add_mag(magnets)
        for item in (file[0]):
            path = os.path.abspath(os.path.dirname(item))
            if os.path.exists(path):
                pyMagSafeGui.save_config("Default Path", path)
                break

    def hist_button_clicked(self, checked):
        if self.hist_window is None:
            self.hist_window = HistoryWindow()
            self.hist_window.show()
            self.hist_window.buttonBox.button(QDialogButtonBox.Retry).clicked.connect(self.hist_retry_button_clicked)
        else:
            self.hist_window.close()
            self.hist_window = None

    def hist_retry_button_clicked(self):
        magnets = []
        indexes = self.hist_window.treeView.selectedIndexes()
        index_rows = set()
        for index in indexes:
            index_rows.add(index.row())
        for index in index_rows:
            torrent = self.hist_window.treeView.model().index(index, 1)
            torrent = torrent.model().itemFromIndex(torrent).text()
            magnet = self.hist_window.treeView.model().index(index, 2)
            magnet = magnet.model().itemFromIndex(magnet).text()
            value = (torrent, magnet)
            magnets.append(value)
        self.add_mag(magnets)
        self.hist_window.treeView.clearSelection()

    def closeEvent(self, event: QCloseEvent) -> None:
        # close button clicked in Main window, close his_window too
        self.hist_window.close()
        self.hist_window = None
