#! python3
# main_window.py

from PySide6.QtWidgets import (QMainWindow, QWidget, QPushButton, QStatusBar,
                               QVBoxLayout, QFileDialog, QListWidget, QToolBar)
from PySide6.QtGui import QAction
import os

import pyMagSafeGui
from history_window import HistoryWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("pyMagSafe")

        # initialize holder for history window
        self.hist_window = None

        # Send to Deluge button
        self.button = QPushButton("Send to Deluge")
        self.button.clicked.connect(self.go_button_clicked)
        self.button.setStatusTip("Send all .magnets in list to Deluge")
        # File list widget
        self.fname = QListWidget()
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

    def go_button_clicked(self):
        items = []
        for i in range(self.fname.count()):
            items.append(str(self.fname.item(i).text()))
        pyMagSafeGui.send_to_deluge(pyMagSafeGui.read_magnets(items))
        self.fname.clear()

    def dlg_button_clicked(self):
        filter = "magnet(*.magnet)"
        path = pyMagSafeGui.read_config()
        path = os.path.abspath(path["Default Path"])
        print(path)
        dlg = QFileDialog(self)
        dlg.setDirectory(path)
        dlg.setFileMode(QFileDialog.FileMode.ExistingFile)
        file = dlg.getOpenFileNames(self, filter=filter, dir=path)
        self.fname.addItems(file[0])
        for item in (file[0]):
            path = os.path.abspath(os.path.dirname(item))
            if os.path.exists(path):
                pyMagSafeGui.save_config("Default Path", path)
                break

    def hist_button_clicked(self, checked):
        if self.hist_window is None:
            self.hist_window = HistoryWindow()
            self.hist_window.show()
        else:
            self.hist_window.close()
            self.hist_window = None
