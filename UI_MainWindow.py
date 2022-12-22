# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, Qt)
from PySide6.QtWidgets import (QDialogButtonBox, QDockWidget, QHBoxLayout, QTreeView, QVBoxLayout, QWidget)

class Ui_main_window(object):
    def setupUi(self, main_window):
        if not main_window.objectName():
            main_window.setObjectName(u"main_window")
        main_window.resize(998, 525)
        self.horizontalLayout = QHBoxLayout(main_window)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.dockWidget_Main = QDockWidget(main_window)
        self.dockWidget_Main.setObjectName(u"dockWidget_Main")
        self.dockWidget_Main.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.dockWidgetContents_Main = QWidget()
        self.dockWidgetContents_Main.setObjectName(u"dockWidgetContents_Main")
        self.verticalLayout_4 = QVBoxLayout(self.dockWidgetContents_Main)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.treeView_Main = QTreeView(self.dockWidgetContents_Main)
        self.treeView_Main.setObjectName(u"treeView_Main")

        self.verticalLayout_4.addWidget(self.treeView_Main)

        self.buttonBox_Main = QDialogButtonBox(self.dockWidgetContents_Main)
        self.buttonBox_Main.setObjectName(u"buttonBox_Main")
        self.buttonBox_Main.setStandardButtons(QDialogButtonBox.Open|QDialogButtonBox.Reset|QDialogButtonBox.Save)

        self.verticalLayout_4.addWidget(self.buttonBox_Main)

        self.dockWidget_Main.setWidget(self.dockWidgetContents_Main)

        self.horizontalLayout.addWidget(self.dockWidget_Main)

        self.dockWidget_Hist = QDockWidget(main_window)
        self.dockWidget_Hist.setObjectName(u"dockWidget_Hist")
        self.dockWidget_Hist.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.dockWidgetContents_Hist = QWidget()
        self.dockWidgetContents_Hist.setObjectName(u"dockWidgetContents_Hist")
        self.verticalLayout_3 = QVBoxLayout(self.dockWidgetContents_Hist)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.treeView_Hist = QTreeView(self.dockWidgetContents_Hist)
        self.treeView_Hist.setObjectName(u"treeView_Hist")

        self.verticalLayout_3.addWidget(self.treeView_Hist)

        self.buttonBox_Hist = QDialogButtonBox(self.dockWidgetContents_Hist)
        self.buttonBox_Hist.setObjectName(u"buttonBox_Hist")
        self.buttonBox_Hist.setStandardButtons(QDialogButtonBox.Close|QDialogButtonBox.Reset|QDialogButtonBox.RestoreDefaults|QDialogButtonBox.Retry)

        self.verticalLayout_3.addWidget(self.buttonBox_Hist)

        self.dockWidget_Hist.setWidget(self.dockWidgetContents_Hist)

        self.horizontalLayout.addWidget(self.dockWidget_Hist)


        self.retranslateUi(main_window)

        QMetaObject.connectSlotsByName(main_window)
    # setupUi

    def retranslateUi(self, main_window):
        main_window.setWindowTitle(QCoreApplication.translate("main_window", u"pyMagSafe", None))
        self.dockWidget_Main.setWindowTitle(QCoreApplication.translate("main_window", u"Send to Deluge", None))
        self.dockWidget_Hist.setWindowTitle(QCoreApplication.translate("main_window", u"History", None))
    # retranslateUi
