#! python3
# main.py

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton,
                               QVBoxLayout, QFileDialog, QListWidget)
import os
import shelve
import sys
from datetime import datetime
import subprocess


# Getting the current date and time
dt = datetime.now()

# getting the timestamp
ts = datetime.timestamp(dt)

folderName = os.path.join('.','outFiles')
os.makedirs(folderName, exist_ok = True)
magnets = []
# giving file extension
ext = '.magnet'

# open shelf file to save and read magnets
shelfFilePath = os.path.join(folderName, 'pyMagSafe')
shelfFile = shelve.open(shelfFilePath)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("pyMagSafe")

        self.button = QPushButton("Send to Deluge")
        self.button.clicked.connect(self.go_button_clicked)
        self.fname = QListWidget()
        self.dlgButton = QPushButton("Select File(s)...")
        self.dlgButton.clicked.connect(self.dlg_button_clicked)

        layout = QVBoxLayout()
        layout.addWidget(self.fname)
        layout.addWidget(self.dlgButton)
        layout.addWidget(self.button)

        window = QWidget()
        window.setLayout(layout)

        # add button as widget
        self.setCentralWidget(window)

    def go_button_clicked(self):
        self.fname.clear()

    def dlg_button_clicked(self):
        filter = "magnet(*.magnet)"
        file = QFileDialog.getOpenFileNames(self, filter=filter)
        self.fname.addItems(file[0])
        # self.dlg.setFilter(".magnet files (*.magnet)")


# open all .magnet files in deluge
def sendToDeluge(file_list):
    # iterating over all files
    for file in file_list:
        if file.endswith(ext) and os.path.exists(file):
            print(file)  # printing file name of desired extension
            with open(file) as f:
                line = f.read()
                magnets.append((file, line))
                os.remove(file)

    # save magnets with timestamp as key
    shelfFile[str(ts)] = magnets


    # open magnet links in deluge
    for magnet in magnets:
        subprocess.run(["deluge", magnet[1]])

app = QApplication(sys.argv)

window = MainWindow()
window.show()

# start the event loop
app.exec()

shelfFile.close()

