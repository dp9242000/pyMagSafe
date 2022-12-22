#! python3
# MainWindow.py

from PySide6.QtWidgets import (QMainWindow, QStatusBar, QAbstractItemView, QFileDialog, QDialogButtonBox, QToolBar)
from PySide6.QtGui import QAction, QStandardItemModel, QCloseEvent, QStandardItem
from PySide6.QtCore import Qt
from PySide6 import QtCore
from PySide6.QtSql import QSqlTableModel

import os

import pyMagSafeGui
from UI_MainWindow import Ui_main_window


def set_title(window, title, count=0):
    if count > 0:
        window.setWindowTitle(f"{title} ({count})")
    else:
        window.setWindowTitle(f"{title}")


class StandardItem(QStandardItem):
    def __init__(self, txt=""):
        super().__init__()
        txt = str(txt)
        self.setText(txt)
        self.setEditable(False)


class MainWindow(QMainWindow, Ui_main_window):
    def __init__(self):
        # MAIN WINDOW

        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("pyMagSafe")
        self.setObjectName("pyMagSafe")
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dockWidget_Main)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dockWidget_Hist)

        # self.widget_Main.resize(2000, 1000)
        self.resize(1500, 500)

        # initialize toolbar
        toolbar = QToolBar("Tools")
        toolbar.toggleViewAction().setEnabled(False)
        self.addToolBar(toolbar)

        # create history action to use in toolbar and/or menus
        hist_button_action = QAction("&History", self)
        hist_button_action.setStatusTip("View old magnets window")
        hist_button_action.triggered.connect(self.hist_button_clicked)

        # create history action to use in toolbar and/or menus
        std_window_button_action = QAction("StD", self)
        std_window_button_action.setStatusTip("Send to Deluge window")
        std_window_button_action.triggered.connect(self.std_button_clicked)

        toolbar.addAction(std_window_button_action)
        toolbar.addAction(hist_button_action)

        self.setStatusBar(QStatusBar(self))

        # END MAIN WINDOW

        # SEND TO DELUGE WIDGET

        # Send to Deluge window title
        self.std_window_title = "Send to Deluge"

        # Create model to be used in the QTreeView
        self.main_model = QStandardItemModel(0, 2, self)
        self.main_model.setHeaderData(0, Qt.Horizontal, "Torrent")
        self.main_model.setHeaderData(1, Qt.Horizontal, "Magnet")

        # Create QTreeView to hold the model
        self.treeView_Main.setModel(self.main_model)
        self.treeView_Main.header().resizeSection(0, 250)
        self.treeView_Main.header().resizeSection(1, 250)
        self.treeView_Main.setSortingEnabled(True)
        self.treeView_Main.setSelectionMode(QAbstractItemView.MultiSelection)

        # file open dialog button
        self.buttonBox_Main.button(QDialogButtonBox.Open).clicked.connect(self.dlg_button_clicked)
        self.buttonBox_Main.button(QDialogButtonBox.Open).setText("Select &File(s)...")
        self.buttonBox_Main.button(QDialogButtonBox.Open).setStatusTip("Open dialog to select .magnet files")

        # delete selection button
        self.buttonBox_Main.button(QDialogButtonBox.Reset).clicked.connect(self.del_sel_button_clicked)
        self.buttonBox_Main.button(QDialogButtonBox.Reset).setText("&Delete")
        self.buttonBox_Main.button(QDialogButtonBox.Reset).setStatusTip("Delete selected torrents (saves to history first)")

        # Send to Deluge button
        self.buttonBox_Main.button(QDialogButtonBox.Save).clicked.connect(self.go_button_clicked)
        self.buttonBox_Main.button(QDialogButtonBox.Save).setText("&Send to Deluge")
        self.buttonBox_Main.button(QDialogButtonBox.Save).setStatusTip("Send all magnets in list to Deluge")

        # END SEND TO DELUGE WIDGET

        # HISTORY WIDGET

        # create the history model
        hist_model = self.create_hist_model()

        # create treeview to hold the torrent history
        self.treeView_Hist.setModel(hist_model)
        self.treeView_Hist.setSortingEnabled(True)
        self.treeView_Hist.setSelectionMode(QAbstractItemView.MultiSelection)
        # self.treeView_Hist.selectionModel.selectionChanged.connect(self.hist_window_title_change)
        self.connect(self.treeView_Hist.selectionModel(),
                     QtCore.SIGNAL("selectionChanged(QItemSelection, QItemSelection)"),
                     self.hist_window_title_change)
        self.treeView_Hist.resizeColumnToContents(0)
        self.treeView_Hist.header().resizeSection(2, 500)
        self.treeView_Hist.resizeColumnToContents(1)
        self.treeView_Hist.resizeColumnToContents(3)
        self.treeView_Hist.resizeColumnToContents(4)

        # close hist_window button
        self.buttonBox_Hist.button(QDialogButtonBox.Close).clicked.connect(self.dockWidget_Hist.hide)
        self.buttonBox_Hist.button(QDialogButtonBox.Close).setStatusTip("Close the History window")

        # resend selection to main window button
        self.buttonBox_Hist.button(QDialogButtonBox.Retry).clicked.connect(self.hist_retry_button_clicked)
        self.buttonBox_Hist.button(QDialogButtonBox.Retry).setText("Re&send")
        self.buttonBox_Hist.button(QDialogButtonBox.Retry).setStatusTip("Requeue the selection for resend")

        # clear selection button
        self.buttonBox_Hist.button(QDialogButtonBox.Reset).clicked.connect(self.treeView_Hist.clearSelection)
        self.buttonBox_Hist.button(QDialogButtonBox.Reset).setText("C&lear")
        self.buttonBox_Hist.button(QDialogButtonBox.Reset).setStatusTip("Clear selection")

        # refresh button
        self.buttonBox_Hist.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.refresh_hist)
        self.buttonBox_Hist.button(QDialogButtonBox.RestoreDefaults).setText("&Refresh")
        self.buttonBox_Hist.button(QDialogButtonBox.RestoreDefaults).setStatusTip("Refresh the items in the history")

        # END HISTORY WIDGET

    def add_mag(self, magnets):
        # add magnets to the model
        for magnet in magnets:
            self.main_model.appendRow([StandardItem(magnet.text), StandardItem(magnet.link)])
        set_title(self.dockWidget_Main, self.std_window_title, self.main_model.rowCount())

    def go_button_clicked(self):
        # user clicked the Send to Deluge button
        self.treeView_Main.selectAll()
        magnets = []
        # iterate through the rows in the model
        while self.treeView_Main.model().rowCount() > 0:
            magnet = self.treeView_Main.model().index(0, 1)
            magnet = magnet.model().itemFromIndex(magnet).text()
            magnets.append(magnet)
            self.treeView_Main.model().removeRow(0)
        # send magnets to deluge
        pyMagSafeGui.send_to_deluge(magnets)
        self.treeView_Main.clearSelection()
        set_title(self.dockWidget_Main, self.std_window_title, self.main_model.rowCount())

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
        set_title(self.dockWidget_Main, self.std_window_title, self.main_model.rowCount())

        # set the default path for future use based on the directory the user selected .magnet files from
        for item in (file[0]):
            path = os.path.abspath(os.path.dirname(item))
            if os.path.exists(path):
                pyMagSafeGui.save_config("Default Path", path)
                break

    def hist_button_clicked(self, checked):
        # user clicked the history window button
        # if the history window is not already open, open it
        if self.dockWidget_Hist.isHidden():
            self.dockWidget_Hist.show()
        # else close the history window
        else:
            self.dockWidget_Hist.hide()

    def std_button_clicked(self, checked):
        # user clicked the history window button
        # if the history window is not already open, open it
        if self.dockWidget_Main.isHidden():
            self.dockWidget_Main.show()
        # else close the history window
        else:
            self.dockWidget_Main.hide()

    def hist_retry_button_clicked(self):
        # user clicked the resend button inside the history window
        magnets = []
        # retrieve the selection from the history window
        indexes = self.treeView_Hist.selectedIndexes()
        # initialize a set to store the rows, use set to prevent duplicates
        index_rows = set()
        for index in indexes:
            index_rows.add(index.row())
        # iterate through the rows and retrieve the torrent name and magnet
        for index in index_rows:
            torrent = self.treeView_Hist.model().index(index, 1)
            torrent = torrent.data()
            magnet = self.treeView_Hist.model().index(index, 2)
            magnet = magnet.data()
            dt = self.treeView_Hist.model().index(index, 3)
            dt = dt.data()
            value = pyMagSafeGui.Magnet(torrent, magnet, dt)
            magnets.append(value)
        # add the magnets to the QTreeView self.fname
        self.add_mag(magnets)
        # clear the selection in the history window
        self.treeView_Hist.clearSelection()

    def closeEvent(self, event: QCloseEvent) -> None:
        # close button clicked in Main window, close hist_window too
        if self.dockWidget_Hist:
            self.dockWidget_Hist.close()
            self.dockWidget_Hist = None
        if self.dockWidget_Main:
            self.dockWidget_Main.close()
            self.dockWidget_Main = None

    def del_sel_button_clicked(self):
        # user clicked the Delete Selection button
        # retrieve selected rows from the list
        indexes = self.treeView_Main.selectedIndexes()
        # initialize set to store the row numbers, set is used to prevent duplicate values
        index_rows = set()
        # grab the row numbers
        for index in indexes:
            index_rows.add(index.row())
        # convert set to list for sorting
        index_rows = list(index_rows)
        index_rows.sort(reverse=True)
        # iterate through the rows and remove them from the list
        for index in index_rows:
            self.treeView_Main.model().removeRow(index)
        # ensure the selection is cleared
        self.treeView_Main.clearSelection()
        set_title(self.dockWidget_Main, self.std_window_title, self.main_model.rowCount())

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
        self.treeView_Hist.setModel(model)

    def hist_window_title_change(self):
        indexes = self.treeView_Hist.selectedIndexes()
        # initialize set to store the row numbers, set is used to prevent duplicate values
        index_rows = set()
        # grab the row numbers
        for index in indexes:
            index_rows.add(index.row())
        set_title(self.dockWidget_Hist, "History", len(index_rows))
