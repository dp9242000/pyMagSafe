# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'HistoryWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QMetaObject, Qt)
from PySide6.QtWidgets import (QDialogButtonBox, QTreeView, QVBoxLayout)

class Ui_hist_window(object):
    def setupUi(self, hist_window):
        if not hist_window.objectName():
            hist_window.setObjectName(u"hist_window")
        hist_window.setEnabled(True)
        hist_window.resize(1000, 500)
        hist_window.setWindowTitle(u"History")
        self.verticalLayout_3 = QVBoxLayout(hist_window)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.treeView = QTreeView(hist_window)
        self.treeView.setObjectName(u"treeView")

        self.verticalLayout.addWidget(self.treeView)

        self.buttonBox = QDialogButtonBox(hist_window)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Close | QDialogButtonBox.Retry | QDialogButtonBox.Reset |
                                          QDialogButtonBox.RestoreDefaults)

        self.verticalLayout.addWidget(self.buttonBox)

        self.verticalLayout_3.addLayout(self.verticalLayout)

        # self.buttonBox.accepted.connect(hist_window.accept)
        # self.buttonBox.rejected.connect(hist_window.reject)
        # self.buttonBox.clicked.connect(hist_window.close)

        QMetaObject.connectSlotsByName(hist_window)
    # setupUi

