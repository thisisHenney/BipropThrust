# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(439, 309)
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionShow = QAction(MainWindow)
        self.actionShow.setObjectName(u"actionShow")
        self.actionHide = QAction(MainWindow)
        self.actionHide.setObjectName(u"actionHide")
        self.actionNew = QAction(MainWindow)
        self.actionNew.setObjectName(u"actionNew")
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionRun = QAction(MainWindow)
        self.actionRun.setObjectName(u"actionRun")
        self.actionMesh = QAction(MainWindow)
        self.actionMesh.setObjectName(u"actionMesh")
        self.actionMesh.setCheckable(True)
        self.actionResidual = QAction(MainWindow)
        self.actionResidual.setObjectName(u"actionResidual")
        self.actionResidual.setCheckable(True)
        self.actionForces = QAction(MainWindow)
        self.actionForces.setObjectName(u"actionForces")
        self.actionTerminal = QAction(MainWindow)
        self.actionTerminal.setObjectName(u"actionTerminal")
        self.actionTextEditor = QAction(MainWindow)
        self.actionTextEditor.setObjectName(u"actionTextEditor")
        self.actionFileExplorer = QAction(MainWindow)
        self.actionFileExplorer.setObjectName(u"actionFileExplorer")
        self.actionLog = QAction(MainWindow)
        self.actionLog.setObjectName(u"actionLog")
        self.actionFoam_to_Tecplot = QAction(MainWindow)
        self.actionFoam_to_Tecplot.setObjectName(u"actionFoam_to_Tecplot")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 439, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuRun = QMenu(self.menubar)
        self.menuRun.setObjectName(u"menuRun")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        self.menuPost = QMenu(self.menubar)
        self.menuPost.setObjectName(u"menuPost")
        self.menuTools = QMenu(self.menubar)
        self.menuTools.setObjectName(u"menuTools")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuRun.menuAction())
        self.menubar.addAction(self.menuPost.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)
        self.menuRun.addAction(self.actionRun)
        self.menuView.addAction(self.actionMesh)
        self.menuView.addAction(self.actionResidual)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionLog)
        self.menuPost.addAction(self.actionFoam_to_Tecplot)
        self.menuTools.addAction(self.actionTerminal)
        self.menuTools.addAction(self.actionTextEditor)
        self.menuTools.addAction(self.actionFileExplorer)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About...", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionShow.setText(QCoreApplication.translate("MainWindow", u"Show", None))
        self.actionHide.setText(QCoreApplication.translate("MainWindow", u"Hide", None))
        self.actionNew.setText(QCoreApplication.translate("MainWindow", u"New...", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open...", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.actionRun.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.actionMesh.setText(QCoreApplication.translate("MainWindow", u"Mesh", None))
        self.actionResidual.setText(QCoreApplication.translate("MainWindow", u"Residual", None))
        self.actionForces.setText(QCoreApplication.translate("MainWindow", u"Forces", None))
        self.actionTerminal.setText(QCoreApplication.translate("MainWindow", u"Terminal", None))
        self.actionTextEditor.setText(QCoreApplication.translate("MainWindow", u"Text Editor", None))
        self.actionFileExplorer.setText(QCoreApplication.translate("MainWindow", u"File Explorer", None))
        self.actionLog.setText(QCoreApplication.translate("MainWindow", u"Log", None))
        self.actionFoam_to_Tecplot.setText(QCoreApplication.translate("MainWindow", u"Foam to Tecplot", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuRun.setTitle(QCoreApplication.translate("MainWindow", u"Run", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menuPost.setTitle(QCoreApplication.translate("MainWindow", u"Post", None))
        self.menuTools.setTitle(QCoreApplication.translate("MainWindow", u"Tools", None))
    # retranslateUi

