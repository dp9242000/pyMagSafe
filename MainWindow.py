#! python3
# MainWindow.py

from PySide6.QtWidgets import (QMainWindow, QWidget, QPushButton, QStatusBar, QAbstractItemView,
                               QVBoxLayout, QFileDialog, QTreeView, QDialogButtonBox, QToolBar)
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
        self.button = QPushButton("&Send to Deluge")
        self.button.clicked.connect(self.go_button_clicked)
        self.button.setStatusTip("Send all .magnets in list to Deluge")
        self.button.setStyleSheet("background-color: #013220")

        # file open dialog button
        self.dlgButton = QPushButton("Select &File(s)...")
        self.dlgButton.setStatusTip("Open dialog to select .magnet files")
        self.dlgButton.clicked.connect(self.dlg_button_clicked)

        # delete selection button
        self.delSelButton = QPushButton("&Delete Selection")
        self.delSelButton.setStatusTip("Delete selected torrents (saves to history first)")
        self.delSelButton.clicked.connect(self.del_sel_button_clicked)
        self.delSelButton.setStyleSheet("background-color: #8b0000")

        # Create model to be used in the QTreeView
        self.model = QStandardItemModel(0, 2, self)
        self.model.setHeaderData(0, Qt.Horizontal, "Torrent")
        self.model.setHeaderData(1, Qt.Horizontal, "Magnet")

        # Create QTreeView to hold the model
        self.fname = QTreeView()
        self.fname.setModel(self.model)
        self.fname.header().resizeSection(0, 250)
        self.fname.header().resizeSection(1, 250)
        self.fname.setSortingEnabled(True)
        self.fname.setSelectionMode(QAbstractItemView.MultiSelection)

        # create layout and add all widgets to it
        layout = QVBoxLayout()
        layout.addWidget(self.fname)
        layout.addWidget(self.dlgButton)
        layout.addWidget(self.delSelButton)
        layout.addWidget(self.button)

        window = QWidget()
        window.setLayout(layout)

        self.setCentralWidget(window)

        # initialize toolbar
        toolbar = QToolBar("Tools")
        toolbar.toggleViewAction().setEnabled(False)
        self.addToolBar(toolbar)

        # create history action to use in toolbar and/or menus
        hist_button_action = QAction("&History", self)
        hist_button_action.setStatusTip("View old magnets")
        hist_button_action.triggered.connect(self.hist_button_clicked)

        toolbar.addAction(hist_button_action)

        self.setStatusBar(QStatusBar(self))

        # self.menu = self.menuBar()
        # menu_menu = self.menu.addMenu("&Menu")
        # menu_menu.addAction(hist_button_action)

    def add_mag(self, magnets):
        # add magnets to the model
        for torrent, magnet in magnets:
            self.model.appendRow([StandardItem(torrent), StandardItem(magnet)])

    def go_button_clicked(self):
        # user clicked the Send to Deluge button
        self.fname.selectAll()
        magnets = []
        # iterate through the rows in the model
        while self.fname.model().rowCount() > 0:
            magnet = self.fname.model().index(0, 1)
            magnet = magnet.model().itemFromIndex(magnet).text()
            magnets.append(magnet)
            self.fname.model().removeRow(0)
        # send magnets to deluge
        pyMagSafeGui.send_to_deluge(magnets)
        self.fname.clearSelection()

    def dlg_button_clicked(self):
        # user clicked the Select Files button
        # initialize filter for the file select dialog
        filter = "magnet(*.magnet)"

        # retrieve the default path for the file select dialog
        config = pyMagSafeGui.read_config()
        path = config.get("Default Path", os.path.expanduser(""))
        path = os.path.abspath(path)

        # call the file select dialog
        dlg = QFileDialog(self)
        dlg.setDirectory(path)
        dlg.setFileMode(QFileDialog.FileMode.ExistingFile)
        file = dlg.getOpenFileNames(self, filter=filter, dir=path)

        # retrieve the magnets from the files
        magnets = pyMagSafeGui.read_magnets(file[0])

        # add the magnets to the model
        self.add_mag(magnets)

        # set the default path for future use based on the directory the user selected .magnet files from
        for item in (file[0]):
            path = os.path.abspath(os.path.dirname(item))
            if os.path.exists(path):
                pyMagSafeGui.save_config("Default Path", path)
                break

    def hist_button_clicked(self, checked):
        # user clicked the history window button
        # if the history window is not already open, open it
        if self.hist_window is None:
            self.hist_window = HistoryWindow()
            self.hist_window.show()
            self.hist_window.buttonBox.button(QDialogButtonBox.Retry).clicked.connect(self.hist_retry_button_clicked)
        # else close the history window
        else:
            self.hist_window.close()
            self.hist_window = None

    def hist_retry_button_clicked(self):
        # user clicked the resend button inside the history window
        magnets = []
        # retrieve the selection from the history window
        indexes = self.hist_window.treeView.selectedIndexes()
        # initialize a set to store the rows, use set to prevent duplicates
        index_rows = set()
        for index in indexes:
            index_rows.add(index.row())
        # iterate through the rows and retrieve the torrent name and magnet
        for index in index_rows:
            torrent = self.hist_window.treeView.model().index(index, 1)
            torrent = torrent.model().itemFromIndex(torrent).text()
            magnet = self.hist_window.treeView.model().index(index, 2)
            magnet = magnet.model().itemFromIndex(magnet).text()
            value = (torrent, magnet)
            magnets.append(value)
        # add the magnets to the QTreeView self.fname
        self.add_mag(magnets)
        # clear the selection in the history window
        self.hist_window.treeView.clearSelection()

    def closeEvent(self, event: QCloseEvent) -> None:
        # close button clicked in Main window, close hist_window too
        if self.hist_window:
            self.hist_window.close()
            self.hist_window = None

    def del_sel_button_clicked(self):
        # user clicked the Delete Selection button
        # retrieve selected rows from the list
        indexes = self.fname.selectedIndexes()
        # initialize set to store the row numbers, set is used to prevent duplicate rows
        index_rows = set()
        # grab the row numbers
        for index in indexes:
            index_rows.add(index.row())
        # convert set to list for sorting
        index_rows = list(index_rows)
        index_rows.sort(reverse=True)
        # iterate through the rows and remove them from the list
        for index in index_rows:
            self.fname.model().removeRow(index)
        # ensure the selection is cleared
        self.fname.clearSelection()
