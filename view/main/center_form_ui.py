# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'center_form.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QComboBox, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QLayout, QLineEdit, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QSplitter,
    QStackedWidget, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)

class Ui_Center(object):
    def setupUi(self, Center):
        if not Center.objectName():
            Center.setObjectName(u"Center")
        Center.resize(627, 855)
        self.verticalLayout_14 = QVBoxLayout(Center)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.splitter_2 = QSplitter(Center)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Orientation.Horizontal)
        self.layoutWidget = QWidget(self.splitter_2)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.treeWidget = QTreeWidget(self.layoutWidget)
        font = QFont()
        font.setBold(True)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setFont(0, font);
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        font1 = QFont()
        font1.setFamilies([u"\ub9d1\uc740 \uace0\ub515"])
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setKerning(True)
        font2 = QFont()
        font2.setFamilies([u"\ub9d1\uc740 \uace0\ub515"])
        font2.setPointSize(10)
        font2.setBold(False)
        QTreeWidgetItem(self.treeWidget)
        __qtreewidgetitem1 = QTreeWidgetItem(self.treeWidget)
        __qtreewidgetitem1.setFont(0, font1);
        __qtreewidgetitem2 = QTreeWidgetItem(self.treeWidget)
        __qtreewidgetitem2.setFont(0, font2);
        QTreeWidgetItem(__qtreewidgetitem2)
        QTreeWidgetItem(__qtreewidgetitem2)
        QTreeWidgetItem(__qtreewidgetitem2)
        QTreeWidgetItem(__qtreewidgetitem2)
        __qtreewidgetitem3 = QTreeWidgetItem(self.treeWidget)
        __qtreewidgetitem3.setFont(0, font2);
        QTreeWidgetItem(__qtreewidgetitem3)
        QTreeWidgetItem(__qtreewidgetitem3)
        __qtreewidgetitem4 = QTreeWidgetItem(self.treeWidget)
        __qtreewidgetitem4.setFont(0, font2);
        __qtreewidgetitem5 = QTreeWidgetItem(self.treeWidget)
        __qtreewidgetitem5.setFont(0, font2);
        QTreeWidgetItem(__qtreewidgetitem5)
        QTreeWidgetItem(__qtreewidgetitem5)
        self.treeWidget.setObjectName(u"treeWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy)
        self.treeWidget.setMaximumSize(QSize(180, 16777215))
        font3 = QFont()
        font3.setPointSize(10)
        font3.setBold(False)
        self.treeWidget.setFont(font3)
        self.treeWidget.setStyleSheet(u"# Custom Style (Blue)\n"
"QTreeWidget{\n"
"    show-decoration-selected: 1;\n"
"}\n"
"QTreeWidget::item{\n"
"    height: 24px;\n"
"    border-right: 1px dotted grey;\n"
"}\n"
"QTreeWidget::item:hover {\n"
"    border: 1px solid #567dbc;\n"
"    /* border-left-color: transparent; */\n"
"    border-radius: 6px;\n"
"    /* background-color: lightblue; */\n"
"    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #e7effd, stop:1 #cbdaf1);\n"
"    selection-color : black;\n"
"    /* padding-left: 1px; \uae30\ubcf8\uc73c\ub85c 1px\uc774 \uc801\uc6a9\ub418\uc5b4 \uc788\uc73c\ubbc0\ub85c \ub530\ub85c \ucd94\uac00\ud560 \ud544\uc694\ub294 \uc5c6\uc74c */\n"
"}\n"
"QTreeWidget::item:selected:active{\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6ea1f1, stop:1 #3d87bf);\n"
"    border-radius: 6px;\n"
"}\n"
"QTreeWidget::item:selected:!active {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6b9be8, stop:1 #577fbf);\n"
"    border-radius: 6px;\n"
"}\n"
"")
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.setIndentation(10)
        self.treeWidget.setUniformRowHeights(True)
        self.treeWidget.setAnimated(True)
        self.treeWidget.header().setVisible(True)
        self.treeWidget.header().setCascadingSectionResizes(False)
        self.treeWidget.header().setMinimumSectionSize(60)
        self.treeWidget.header().setDefaultSectionSize(140)
        self.treeWidget.header().setHighlightSections(False)
        self.treeWidget.header().setProperty(u"showSortIndicator", False)

        self.horizontalLayout.addWidget(self.treeWidget)

        self.stackedWidget = QStackedWidget(self.layoutWidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setMaximumSize(QSize(16777215, 16777215))
        self.page_geometry = QWidget()
        self.page_geometry.setObjectName(u"page_geometry")
        self.verticalLayout_6 = QVBoxLayout(self.page_geometry)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.title_2 = QLabel(self.page_geometry)
        self.title_2.setObjectName(u"title_2")
        font4 = QFont()
        font4.setPointSize(12)
        font4.setBold(True)
        self.title_2.setFont(font4)

        self.verticalLayout_6.addWidget(self.title_2)

        self.line_5 = QFrame(self.page_geometry)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.Shape.HLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_6.addWidget(self.line_5)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalSpacer_33 = QSpacerItem(386, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_33)

        self.button_geometry_add = QPushButton(self.page_geometry)
        self.button_geometry_add.setObjectName(u"button_geometry_add")
        self.button_geometry_add.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_13.addWidget(self.button_geometry_add)

        self.button_geometry_remove = QPushButton(self.page_geometry)
        self.button_geometry_remove.setObjectName(u"button_geometry_remove")
        self.button_geometry_remove.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_13.addWidget(self.button_geometry_remove)


        self.verticalLayout_6.addLayout(self.horizontalLayout_13)

        self.tree_geometry = QTreeWidget(self.page_geometry)
        QTreeWidgetItem(self.tree_geometry)
        self.tree_geometry.setObjectName(u"tree_geometry")
        self.tree_geometry.setFont(font3)
        self.tree_geometry.setStyleSheet(u"# Custom Style (Blue)\n"
"QTreeWidget{\n"
"    show-decoration-selected: 1;\n"
"}\n"
"QTreeWidget::item{\n"
"    height: 24px;\n"
"    border-right: 1px dotted grey;\n"
"}\n"
"QTreeWidget::item:hover {\n"
"    border: 1px solid #567dbc;\n"
"    /* border-left-color: transparent; */\n"
"    border-radius: 6px;\n"
"    /* background-color: lightblue; */\n"
"    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #e7effd, stop:1 #cbdaf1);\n"
"    selection-color : black;\n"
"    /* padding-left: 1px; \uae30\ubcf8\uc73c\ub85c 1px\uc774 \uc801\uc6a9\ub418\uc5b4 \uc788\uc73c\ubbc0\ub85c \ub530\ub85c \ucd94\uac00\ud560 \ud544\uc694\ub294 \uc5c6\uc74c */\n"
"}\n"
"QTreeWidget::item:selected:active{\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6ea1f1, stop:1 #3d87bf);\n"
"    border-radius: 6px;\n"
"}\n"
"QTreeWidget::item:selected:!active {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6b9be8, stop:1 #577fbf);\n"
"    border-radius: 6px;\n"
"}\n"
"")
        self.tree_geometry.setAlternatingRowColors(True)
        self.tree_geometry.header().setVisible(False)

        self.verticalLayout_6.addWidget(self.tree_geometry)

        self.AdvancedGroupBox_2 = QGroupBox(self.page_geometry)
        self.AdvancedGroupBox_2.setObjectName(u"AdvancedGroupBox_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.AdvancedGroupBox_2.sizePolicy().hasHeightForWidth())
        self.AdvancedGroupBox_2.setSizePolicy(sizePolicy1)
        self.AdvancedGroupBox_2.setMaximumSize(QSize(16777215, 150))
        font5 = QFont()
        font5.setPointSize(9)
        font5.setBold(True)
        self.AdvancedGroupBox_2.setFont(font5)
        self.AdvancedGroupBox_2.setStyleSheet(u"QGroupBox {\n"
"    border: 1px solid;\n"
"    border-radius: 6;\n"
"    margin-top: 9;\n"
"    border-color : #c8c8c8;\n"
"	padding: 3;   \n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    left: 10;\n"
"    padding: 2 3;\n"
"}")
        self.AdvancedGroupBox_2.setCheckable(False)
        self.AdvancedGroupBox_2.setChecked(False)
        self.gridLayout_14 = QGridLayout(self.AdvancedGroupBox_2)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.label_83 = QLabel(self.AdvancedGroupBox_2)
        self.label_83.setObjectName(u"label_83")
        font6 = QFont()
        font6.setPointSize(9)
        font6.setBold(False)
        self.label_83.setFont(font6)

        self.gridLayout_14.addWidget(self.label_83, 0, 0, 1, 1)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(-1, 0, -1, -1)
        self.button_geometry_reset = QPushButton(self.AdvancedGroupBox_2)
        self.button_geometry_reset.setObjectName(u"button_geometry_reset")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.button_geometry_reset.sizePolicy().hasHeightForWidth())
        self.button_geometry_reset.setSizePolicy(sizePolicy2)
        self.button_geometry_reset.setMinimumSize(QSize(0, 30))
        self.button_geometry_reset.setFont(font6)

        self.horizontalLayout_14.addWidget(self.button_geometry_reset)

        self.horizontalSpacer_72 = QSpacerItem(17, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_72)

        self.button_geometry_apply = QPushButton(self.AdvancedGroupBox_2)
        self.button_geometry_apply.setObjectName(u"button_geometry_apply")
        sizePolicy2.setHeightForWidth(self.button_geometry_apply.sizePolicy().hasHeightForWidth())
        self.button_geometry_apply.setSizePolicy(sizePolicy2)
        self.button_geometry_apply.setMinimumSize(QSize(0, 30))
        self.button_geometry_apply.setFont(font6)

        self.horizontalLayout_14.addWidget(self.button_geometry_apply)

        self.button_geometry_cancel = QPushButton(self.AdvancedGroupBox_2)
        self.button_geometry_cancel.setObjectName(u"button_geometry_cancel")
        sizePolicy2.setHeightForWidth(self.button_geometry_cancel.sizePolicy().hasHeightForWidth())
        self.button_geometry_cancel.setSizePolicy(sizePolicy2)
        self.button_geometry_cancel.setMinimumSize(QSize(0, 30))
        self.button_geometry_cancel.setFont(font6)

        self.horizontalLayout_14.addWidget(self.button_geometry_cancel)


        self.gridLayout_14.addLayout(self.horizontalLayout_14, 2, 1, 1, 1)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(-1, -1, 0, -1)
        self.edit_input_position_x = QLineEdit(self.AdvancedGroupBox_2)
        self.edit_input_position_x.setObjectName(u"edit_input_position_x")
        sizePolicy2.setHeightForWidth(self.edit_input_position_x.sizePolicy().hasHeightForWidth())
        self.edit_input_position_x.setSizePolicy(sizePolicy2)
        self.edit_input_position_x.setFont(font6)
        self.edit_input_position_x.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_10.addWidget(self.edit_input_position_x)

        self.edit_input_position_y = QLineEdit(self.AdvancedGroupBox_2)
        self.edit_input_position_y.setObjectName(u"edit_input_position_y")
        sizePolicy2.setHeightForWidth(self.edit_input_position_y.sizePolicy().hasHeightForWidth())
        self.edit_input_position_y.setSizePolicy(sizePolicy2)
        self.edit_input_position_y.setFont(font6)
        self.edit_input_position_y.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_10.addWidget(self.edit_input_position_y)

        self.edit_input_position_z = QLineEdit(self.AdvancedGroupBox_2)
        self.edit_input_position_z.setObjectName(u"edit_input_position_z")
        sizePolicy2.setHeightForWidth(self.edit_input_position_z.sizePolicy().hasHeightForWidth())
        self.edit_input_position_z.setSizePolicy(sizePolicy2)
        self.edit_input_position_z.setFont(font6)
        self.edit_input_position_z.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_10.addWidget(self.edit_input_position_z)


        self.gridLayout_14.addLayout(self.horizontalLayout_10, 0, 1, 1, 1)

        self.line_12 = QFrame(self.AdvancedGroupBox_2)
        self.line_12.setObjectName(u"line_12")
        self.line_12.setFrameShape(QFrame.Shape.HLine)
        self.line_12.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_14.addWidget(self.line_12, 1, 1, 1, 1)


        self.verticalLayout_6.addWidget(self.AdvancedGroupBox_2)

        self.verticalSpacer_5 = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_5)

        self.stackedWidget.addWidget(self.page_geometry)
        self.page_mesh_generation = QWidget()
        self.page_mesh_generation.setObjectName(u"page_mesh_generation")
        self.verticalLayout_12 = QVBoxLayout(self.page_mesh_generation)
        self.verticalLayout_12.setSpacing(6)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.title_5 = QLabel(self.page_mesh_generation)
        self.title_5.setObjectName(u"title_5")
        self.title_5.setFont(font4)

        self.verticalLayout_12.addWidget(self.title_5)

        self.line_8 = QFrame(self.page_mesh_generation)
        self.line_8.setObjectName(u"line_8")
        self.line_8.setFrameShape(QFrame.Shape.HLine)
        self.line_8.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_12.addWidget(self.line_8)

        self.scrollArea = QScrollArea(self.page_mesh_generation)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContentsOnFirstShow)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 403, 728))
        self.verticalLayout_5 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.AdvancedGroupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.AdvancedGroupBox.setObjectName(u"AdvancedGroupBox")
        sizePolicy1.setHeightForWidth(self.AdvancedGroupBox.sizePolicy().hasHeightForWidth())
        self.AdvancedGroupBox.setSizePolicy(sizePolicy1)
        self.AdvancedGroupBox.setMaximumSize(QSize(16777215, 150))
        self.AdvancedGroupBox.setFont(font5)
        self.AdvancedGroupBox.setStyleSheet(u"QGroupBox {\n"
"    border: 1px solid;\n"
"    border-radius: 6;\n"
"    margin-top: 9;\n"
"    border-color : #c8c8c8;\n"
"	padding: 3;   \n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    left: 10;\n"
"    padding: 2 3;\n"
"}")
        self.AdvancedGroupBox.setCheckable(False)
        self.AdvancedGroupBox.setChecked(False)
        self.verticalLayout_11 = QVBoxLayout(self.AdvancedGroupBox)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(9, -1, -1, -1)
        self.basegridBox = QGroupBox(self.AdvancedGroupBox)
        self.basegridBox.setObjectName(u"basegridBox")
        font7 = QFont()
        font7.setPointSize(8)
        font7.setBold(False)
        self.basegridBox.setFont(font7)
        self.basegridBox.setStyleSheet(u"QGroupBox {\n"
"    border: 1px solid;\n"
"    border-radius: 6;\n"
"    margin-top: 9;\n"
"    border-color : #c8c8c8;\n"
"	padding: 3;   \n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    left: 10;\n"
"    padding: 2 3;\n"
"}")
        self.gridLayout_10 = QGridLayout(self.basegridBox)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.label_48 = QLabel(self.basegridBox)
        self.label_48.setObjectName(u"label_48")
        self.label_48.setFont(font6)

        self.gridLayout_10.addWidget(self.label_48, 1, 0, 1, 1)

        self.label_50 = QLabel(self.basegridBox)
        self.label_50.setObjectName(u"label_50")
        self.label_50.setFont(font6)

        self.gridLayout_10.addWidget(self.label_50, 0, 0, 1, 1)

        self.label_49 = QLabel(self.basegridBox)
        self.label_49.setObjectName(u"label_49")
        self.label_49.setFont(font6)

        self.gridLayout_10.addWidget(self.label_49, 2, 0, 1, 1)

        self.lineEdit_basegrid_x = QLineEdit(self.basegridBox)
        self.lineEdit_basegrid_x.setObjectName(u"lineEdit_basegrid_x")
        sizePolicy2.setHeightForWidth(self.lineEdit_basegrid_x.sizePolicy().hasHeightForWidth())
        self.lineEdit_basegrid_x.setSizePolicy(sizePolicy2)
        self.lineEdit_basegrid_x.setFont(font6)
        self.lineEdit_basegrid_x.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.lineEdit_basegrid_x, 0, 1, 1, 1)

        self.lineEdit_basegrid_y = QLineEdit(self.basegridBox)
        self.lineEdit_basegrid_y.setObjectName(u"lineEdit_basegrid_y")
        sizePolicy2.setHeightForWidth(self.lineEdit_basegrid_y.sizePolicy().hasHeightForWidth())
        self.lineEdit_basegrid_y.setSizePolicy(sizePolicy2)
        self.lineEdit_basegrid_y.setFont(font6)
        self.lineEdit_basegrid_y.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.lineEdit_basegrid_y, 1, 1, 1, 1)

        self.lineEdit_basegrid_z = QLineEdit(self.basegridBox)
        self.lineEdit_basegrid_z.setObjectName(u"lineEdit_basegrid_z")
        sizePolicy2.setHeightForWidth(self.lineEdit_basegrid_z.sizePolicy().hasHeightForWidth())
        self.lineEdit_basegrid_z.setSizePolicy(sizePolicy2)
        self.lineEdit_basegrid_z.setFont(font6)
        self.lineEdit_basegrid_z.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.lineEdit_basegrid_z, 2, 1, 1, 1)

        self.gridLayout_10.setColumnStretch(0, 1)
        self.gridLayout_10.setColumnStretch(1, 1)

        self.verticalLayout_11.addWidget(self.basegridBox)


        self.verticalLayout_5.addWidget(self.AdvancedGroupBox)

        self.boundaryGroupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.boundaryGroupBox.setObjectName(u"boundaryGroupBox")
        self.boundaryGroupBox.setFont(font5)
        self.boundaryGroupBox.setStyleSheet(u"QGroupBox {\n"
"    border: 1px solid;\n"
"    border-radius: 6;\n"
"    margin-top: 9;\n"
"    border-color : #c8c8c8;\n"
"	padding: 3;   \n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    left: 10;\n"
"    padding: 2 3;\n"
"}")
        self.gridLayout_11 = QGridLayout(self.boundaryGroupBox)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.edit_castellation_3 = QLineEdit(self.boundaryGroupBox)
        self.edit_castellation_3.setObjectName(u"edit_castellation_3")
        sizePolicy2.setHeightForWidth(self.edit_castellation_3.sizePolicy().hasHeightForWidth())
        self.edit_castellation_3.setSizePolicy(sizePolicy2)
        self.edit_castellation_3.setFont(font6)
        self.edit_castellation_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.edit_castellation_3, 3, 1, 1, 1)

        self.edit_castellation_4 = QLineEdit(self.boundaryGroupBox)
        self.edit_castellation_4.setObjectName(u"edit_castellation_4")
        sizePolicy2.setHeightForWidth(self.edit_castellation_4.sizePolicy().hasHeightForWidth())
        self.edit_castellation_4.setSizePolicy(sizePolicy2)
        self.edit_castellation_4.setFont(font6)
        self.edit_castellation_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.edit_castellation_4, 5, 1, 1, 1)

        self.label_52 = QLabel(self.boundaryGroupBox)
        self.label_52.setObjectName(u"label_52")
        self.label_52.setFont(font6)

        self.gridLayout_11.addWidget(self.label_52, 0, 0, 1, 1)

        self.edit_castellation_1 = QLineEdit(self.boundaryGroupBox)
        self.edit_castellation_1.setObjectName(u"edit_castellation_1")
        sizePolicy2.setHeightForWidth(self.edit_castellation_1.sizePolicy().hasHeightForWidth())
        self.edit_castellation_1.setSizePolicy(sizePolicy2)
        self.edit_castellation_1.setFont(font6)
        self.edit_castellation_1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.edit_castellation_1, 0, 1, 1, 1)

        self.label_54 = QLabel(self.boundaryGroupBox)
        self.label_54.setObjectName(u"label_54")
        self.label_54.setFont(font6)

        self.gridLayout_11.addWidget(self.label_54, 3, 0, 1, 1)

        self.label_53 = QLabel(self.boundaryGroupBox)
        self.label_53.setObjectName(u"label_53")
        self.label_53.setFont(font6)

        self.gridLayout_11.addWidget(self.label_53, 5, 0, 1, 1)

        self.edit_castellation_5 = QLineEdit(self.boundaryGroupBox)
        self.edit_castellation_5.setObjectName(u"edit_castellation_5")
        self.edit_castellation_5.setEnabled(False)
        sizePolicy2.setHeightForWidth(self.edit_castellation_5.sizePolicy().hasHeightForWidth())
        self.edit_castellation_5.setSizePolicy(sizePolicy2)
        self.edit_castellation_5.setFont(font6)
        self.edit_castellation_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.edit_castellation_5, 7, 1, 1, 1)

        self.edit_castellation_2 = QLineEdit(self.boundaryGroupBox)
        self.edit_castellation_2.setObjectName(u"edit_castellation_2")
        sizePolicy2.setHeightForWidth(self.edit_castellation_2.sizePolicy().hasHeightForWidth())
        self.edit_castellation_2.setSizePolicy(sizePolicy2)
        self.edit_castellation_2.setFont(font6)
        self.edit_castellation_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.edit_castellation_2, 1, 1, 1, 1)

        self.label_51 = QLabel(self.boundaryGroupBox)
        self.label_51.setObjectName(u"label_51")
        self.label_51.setEnabled(False)
        self.label_51.setFont(font6)

        self.gridLayout_11.addWidget(self.label_51, 7, 0, 1, 1)

        self.label_55 = QLabel(self.boundaryGroupBox)
        self.label_55.setObjectName(u"label_55")
        self.label_55.setFont(font6)

        self.gridLayout_11.addWidget(self.label_55, 1, 0, 1, 1)

        self.gridLayout_11.setColumnStretch(0, 1)
        self.gridLayout_11.setColumnStretch(1, 1)

        self.verticalLayout_5.addWidget(self.boundaryGroupBox)

        self.bufferLayerBox = QGroupBox(self.scrollAreaWidgetContents)
        self.bufferLayerBox.setObjectName(u"bufferLayerBox")
        self.bufferLayerBox.setEnabled(True)
        self.bufferLayerBox.setFont(font5)
        self.bufferLayerBox.setStyleSheet(u"QGroupBox {\n"
"    border: 1px solid;\n"
"    border-radius: 6;\n"
"    margin-top: 9;\n"
"    border-color : #c8c8c8;\n"
"	padding: 3;   \n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    left: 10;\n"
"    padding: 2 3;\n"
"}")
        self.bufferLayerBox.setCheckable(False)
        self.bufferLayerBox.setChecked(False)
        self.gridLayout_12 = QGridLayout(self.bufferLayerBox)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(-1, 9, -1, 9)
        self.edit_snap_3 = QLineEdit(self.bufferLayerBox)
        self.edit_snap_3.setObjectName(u"edit_snap_3")
        sizePolicy2.setHeightForWidth(self.edit_snap_3.sizePolicy().hasHeightForWidth())
        self.edit_snap_3.setSizePolicy(sizePolicy2)
        self.edit_snap_3.setFont(font6)
        self.edit_snap_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_12.addWidget(self.edit_snap_3, 2, 1, 1, 1)

        self.label_58 = QLabel(self.bufferLayerBox)
        self.label_58.setObjectName(u"label_58")
        self.label_58.setFont(font6)

        self.gridLayout_12.addWidget(self.label_58, 0, 0, 1, 1)

        self.edit_snap_4 = QLineEdit(self.bufferLayerBox)
        self.edit_snap_4.setObjectName(u"edit_snap_4")
        sizePolicy2.setHeightForWidth(self.edit_snap_4.sizePolicy().hasHeightForWidth())
        self.edit_snap_4.setSizePolicy(sizePolicy2)
        self.edit_snap_4.setFont(font6)
        self.edit_snap_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_12.addWidget(self.edit_snap_4, 3, 1, 1, 1)

        self.edit_snap_2 = QLineEdit(self.bufferLayerBox)
        self.edit_snap_2.setObjectName(u"edit_snap_2")
        sizePolicy2.setHeightForWidth(self.edit_snap_2.sizePolicy().hasHeightForWidth())
        self.edit_snap_2.setSizePolicy(sizePolicy2)
        self.edit_snap_2.setFont(font6)
        self.edit_snap_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_12.addWidget(self.edit_snap_2, 1, 1, 1, 1)

        self.edit_snap_1 = QLineEdit(self.bufferLayerBox)
        self.edit_snap_1.setObjectName(u"edit_snap_1")
        sizePolicy2.setHeightForWidth(self.edit_snap_1.sizePolicy().hasHeightForWidth())
        self.edit_snap_1.setSizePolicy(sizePolicy2)
        self.edit_snap_1.setFont(font6)
        self.edit_snap_1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_12.addWidget(self.edit_snap_1, 0, 1, 1, 1)

        self.label_56 = QLabel(self.bufferLayerBox)
        self.label_56.setObjectName(u"label_56")
        self.label_56.setFont(font6)

        self.gridLayout_12.addWidget(self.label_56, 2, 0, 1, 1)

        self.label_57 = QLabel(self.bufferLayerBox)
        self.label_57.setObjectName(u"label_57")
        self.label_57.setFont(font6)

        self.gridLayout_12.addWidget(self.label_57, 1, 0, 1, 1)

        self.label_59 = QLabel(self.bufferLayerBox)
        self.label_59.setObjectName(u"label_59")
        self.label_59.setFont(font6)

        self.gridLayout_12.addWidget(self.label_59, 3, 0, 1, 1)

        self.gridLayout_12.setColumnStretch(0, 1)
        self.gridLayout_12.setColumnStretch(1, 1)

        self.verticalLayout_5.addWidget(self.bufferLayerBox)

        self.bufferLayerBox_2 = QGroupBox(self.scrollAreaWidgetContents)
        self.bufferLayerBox_2.setObjectName(u"bufferLayerBox_2")
        self.bufferLayerBox_2.setEnabled(True)
        self.bufferLayerBox_2.setFont(font5)
        self.bufferLayerBox_2.setStyleSheet(u"QGroupBox {\n"
"    border: 1px solid;\n"
"    border-radius: 6;\n"
"    margin-top: 9;\n"
"    border-color : #c8c8c8;\n"
"	padding: 3;   \n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    left: 10;\n"
"    padding: 2 3;\n"
"}")
        self.bufferLayerBox_2.setCheckable(False)
        self.bufferLayerBox_2.setChecked(False)
        self.gridLayout_13 = QGridLayout(self.bufferLayerBox_2)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(-1, 9, -1, 9)
        self.label_63 = QLabel(self.bufferLayerBox_2)
        self.label_63.setObjectName(u"label_63")
        self.label_63.setFont(font6)

        self.gridLayout_13.addWidget(self.label_63, 2, 0, 1, 1)

        self.edit_boundary_layer_4 = QLineEdit(self.bufferLayerBox_2)
        self.edit_boundary_layer_4.setObjectName(u"edit_boundary_layer_4")
        sizePolicy2.setHeightForWidth(self.edit_boundary_layer_4.sizePolicy().hasHeightForWidth())
        self.edit_boundary_layer_4.setSizePolicy(sizePolicy2)
        self.edit_boundary_layer_4.setFont(font6)
        self.edit_boundary_layer_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_13.addWidget(self.edit_boundary_layer_4, 4, 1, 1, 1)

        self.label_62 = QLabel(self.bufferLayerBox_2)
        self.label_62.setObjectName(u"label_62")
        self.label_62.setFont(font6)

        self.gridLayout_13.addWidget(self.label_62, 6, 0, 1, 1)

        self.label_60 = QLabel(self.bufferLayerBox_2)
        self.label_60.setObjectName(u"label_60")
        self.label_60.setFont(font6)

        self.gridLayout_13.addWidget(self.label_60, 4, 0, 1, 1)

        self.label_61 = QLabel(self.bufferLayerBox_2)
        self.label_61.setObjectName(u"label_61")
        self.label_61.setFont(font6)

        self.gridLayout_13.addWidget(self.label_61, 5, 0, 1, 1)

        self.edit_boundary_layer_2 = QLineEdit(self.bufferLayerBox_2)
        self.edit_boundary_layer_2.setObjectName(u"edit_boundary_layer_2")
        sizePolicy2.setHeightForWidth(self.edit_boundary_layer_2.sizePolicy().hasHeightForWidth())
        self.edit_boundary_layer_2.setSizePolicy(sizePolicy2)
        self.edit_boundary_layer_2.setFont(font6)
        self.edit_boundary_layer_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_13.addWidget(self.edit_boundary_layer_2, 2, 1, 1, 1)

        self.edit_boundary_layer_5 = QLineEdit(self.bufferLayerBox_2)
        self.edit_boundary_layer_5.setObjectName(u"edit_boundary_layer_5")
        sizePolicy2.setHeightForWidth(self.edit_boundary_layer_5.sizePolicy().hasHeightForWidth())
        self.edit_boundary_layer_5.setSizePolicy(sizePolicy2)
        self.edit_boundary_layer_5.setFont(font6)
        self.edit_boundary_layer_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_13.addWidget(self.edit_boundary_layer_5, 5, 1, 1, 1)

        self.edit_boundary_layer_1 = QLineEdit(self.bufferLayerBox_2)
        self.edit_boundary_layer_1.setObjectName(u"edit_boundary_layer_1")
        sizePolicy2.setHeightForWidth(self.edit_boundary_layer_1.sizePolicy().hasHeightForWidth())
        self.edit_boundary_layer_1.setSizePolicy(sizePolicy2)
        self.edit_boundary_layer_1.setFont(font6)
        self.edit_boundary_layer_1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_13.addWidget(self.edit_boundary_layer_1, 1, 1, 1, 1)

        self.label_65 = QLabel(self.bufferLayerBox_2)
        self.label_65.setObjectName(u"label_65")
        self.label_65.setFont(font6)

        self.gridLayout_13.addWidget(self.label_65, 3, 0, 1, 1)

        self.edit_boundary_layer_3 = QLineEdit(self.bufferLayerBox_2)
        self.edit_boundary_layer_3.setObjectName(u"edit_boundary_layer_3")
        sizePolicy2.setHeightForWidth(self.edit_boundary_layer_3.sizePolicy().hasHeightForWidth())
        self.edit_boundary_layer_3.setSizePolicy(sizePolicy2)
        self.edit_boundary_layer_3.setFont(font6)
        self.edit_boundary_layer_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_13.addWidget(self.edit_boundary_layer_3, 3, 1, 1, 1)

        self.edit_boundary_layer_6 = QLineEdit(self.bufferLayerBox_2)
        self.edit_boundary_layer_6.setObjectName(u"edit_boundary_layer_6")
        sizePolicy2.setHeightForWidth(self.edit_boundary_layer_6.sizePolicy().hasHeightForWidth())
        self.edit_boundary_layer_6.setSizePolicy(sizePolicy2)
        self.edit_boundary_layer_6.setFont(font6)
        self.edit_boundary_layer_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_13.addWidget(self.edit_boundary_layer_6, 6, 1, 1, 1)

        self.label_64 = QLabel(self.bufferLayerBox_2)
        self.label_64.setObjectName(u"label_64")
        self.label_64.setFont(font6)

        self.gridLayout_13.addWidget(self.label_64, 1, 0, 1, 1)

        self.gridLayout_13.setColumnStretch(0, 1)
        self.gridLayout_13.setColumnStretch(1, 1)

        self.verticalLayout_5.addWidget(self.bufferLayerBox_2)

        self.verticalSpacer_9 = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_9)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_12.addWidget(self.scrollArea)

        self.line_13 = QFrame(self.page_mesh_generation)
        self.line_13.setObjectName(u"line_13")
        self.line_13.setFrameShape(QFrame.Shape.HLine)
        self.line_13.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_12.addWidget(self.line_13)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(-1, 0, -1, -1)
        self.button_edit_hostfile_mesh = QPushButton(self.page_mesh_generation)
        self.button_edit_hostfile_mesh.setObjectName(u"button_edit_hostfile_mesh")
        sizePolicy2.setHeightForWidth(self.button_edit_hostfile_mesh.sizePolicy().hasHeightForWidth())
        self.button_edit_hostfile_mesh.setSizePolicy(sizePolicy2)
        self.button_edit_hostfile_mesh.setMinimumSize(QSize(0, 35))
        self.button_edit_hostfile_mesh.setFont(font6)

        self.horizontalLayout_11.addWidget(self.button_edit_hostfile_mesh)

        self.horizontalSpacer_71 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_71)

        self.button_mesh_generate = QPushButton(self.page_mesh_generation)
        self.button_mesh_generate.setObjectName(u"button_mesh_generate")
        sizePolicy2.setHeightForWidth(self.button_mesh_generate.sizePolicy().hasHeightForWidth())
        self.button_mesh_generate.setSizePolicy(sizePolicy2)
        self.button_mesh_generate.setMinimumSize(QSize(0, 35))
        self.button_mesh_generate.setFont(font5)

        self.horizontalLayout_11.addWidget(self.button_mesh_generate)


        self.verticalLayout_12.addLayout(self.horizontalLayout_11)

        self.stackedWidget.addWidget(self.page_mesh_generation)
        self.page_models = QWidget()
        self.page_models.setObjectName(u"page_models")
        self.verticalLayout_8 = QVBoxLayout(self.page_models)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.title_3 = QLabel(self.page_models)
        self.title_3.setObjectName(u"title_3")
        self.title_3.setFont(font4)

        self.verticalLayout_8.addWidget(self.title_3)

        self.line_6 = QFrame(self.page_models)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.Shape.HLine)
        self.line_6.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_8.addWidget(self.line_6)

        self.groupBox_10 = QGroupBox(self.page_models)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.groupBox_10.setFont(font5)
        self.groupBox_10.setStyleSheet(u"QGroupBox {\n"
"    border: 1px solid;\n"
"    border-radius: 6;\n"
"    margin-top: 9;\n"
"    border-color : #c8c8c8;\n"
"	padding: 3;   \n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    left: 10;\n"
"    padding: 2 3;\n"
"}")
        self.gridLayout_16 = QGridLayout(self.groupBox_10)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.label_69 = QLabel(self.groupBox_10)
        self.label_69.setObjectName(u"label_69")
        self.label_69.setFont(font6)

        self.gridLayout_16.addWidget(self.label_69, 2, 0, 1, 1)

        self.comboBox_7 = QComboBox(self.groupBox_10)
        self.comboBox_7.addItem("")
        self.comboBox_7.addItem("")
        self.comboBox_7.setObjectName(u"comboBox_7")
        self.comboBox_7.setFont(font6)

        self.gridLayout_16.addWidget(self.comboBox_7, 4, 2, 1, 1)

        self.label_81 = QLabel(self.groupBox_10)
        self.label_81.setObjectName(u"label_81")
        self.label_81.setEnabled(True)
        self.label_81.setFont(font6)
        self.label_81.setIndent(5)

        self.gridLayout_16.addWidget(self.label_81, 6, 0, 1, 1)

        self.comboBox_2 = QComboBox(self.groupBox_10)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")
        self.comboBox_2.setFont(font6)

        self.gridLayout_16.addWidget(self.comboBox_2, 0, 2, 1, 1)

        self.label_76 = QLabel(self.groupBox_10)
        self.label_76.setObjectName(u"label_76")
        self.label_76.setFont(font6)

        self.gridLayout_16.addWidget(self.label_76, 7, 0, 1, 1)

        self.label_75 = QLabel(self.groupBox_10)
        self.label_75.setObjectName(u"label_75")
        self.label_75.setFont(font6)

        self.gridLayout_16.addWidget(self.label_75, 4, 0, 1, 1)

        self.comboBox_8 = QComboBox(self.groupBox_10)
        self.comboBox_8.addItem("")
        self.comboBox_8.setObjectName(u"comboBox_8")
        self.comboBox_8.setFont(font6)

        self.gridLayout_16.addWidget(self.comboBox_8, 7, 2, 1, 1)

        self.label_74 = QLabel(self.groupBox_10)
        self.label_74.setObjectName(u"label_74")
        self.label_74.setFont(font6)

        self.gridLayout_16.addWidget(self.label_74, 3, 0, 1, 1)

        self.comboBox_6 = QComboBox(self.groupBox_10)
        self.comboBox_6.addItem("")
        self.comboBox_6.setObjectName(u"comboBox_6")
        self.comboBox_6.setFont(font6)

        self.gridLayout_16.addWidget(self.comboBox_6, 3, 2, 1, 1)

        self.comboBox_4 = QComboBox(self.groupBox_10)
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.setObjectName(u"comboBox_4")
        self.comboBox_4.setFont(font6)

        self.gridLayout_16.addWidget(self.comboBox_4, 2, 2, 1, 1)

        self.comboBox_3 = QComboBox(self.groupBox_10)
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.setObjectName(u"comboBox_3")
        self.comboBox_3.setFont(font6)

        self.gridLayout_16.addWidget(self.comboBox_3, 1, 2, 1, 1)

        self.label = QLabel(self.groupBox_10)
        self.label.setObjectName(u"label")
        self.label.setFont(font6)

        self.gridLayout_16.addWidget(self.label, 0, 0, 1, 1)

        self.label_5 = QLabel(self.groupBox_10)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font6)

        self.gridLayout_16.addWidget(self.label_5, 1, 0, 1, 1)

        self.comboBox_10 = QComboBox(self.groupBox_10)
        self.comboBox_10.addItem("")
        self.comboBox_10.addItem("")
        self.comboBox_10.addItem("")
        self.comboBox_10.setObjectName(u"comboBox_10")
        self.comboBox_10.setEnabled(True)
        self.comboBox_10.setFont(font6)

        self.gridLayout_16.addWidget(self.comboBox_10, 6, 2, 1, 1)

        self.gridLayout_16.setColumnStretch(0, 1)
        self.gridLayout_16.setColumnStretch(1, 1)

        self.verticalLayout_8.addWidget(self.groupBox_10)

        self.verticalSpacer_6 = QSpacerItem(20, 877, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_6)

        self.stackedWidget.addWidget(self.page_models)
        self.page_initial_conditions = QWidget()
        self.page_initial_conditions.setObjectName(u"page_initial_conditions")
        self.verticalLayout_9 = QVBoxLayout(self.page_initial_conditions)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.title_4 = QLabel(self.page_initial_conditions)
        self.title_4.setObjectName(u"title_4")
        self.title_4.setFont(font4)

        self.verticalLayout_9.addWidget(self.title_4)

        self.line_7 = QFrame(self.page_initial_conditions)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setFrameShape(QFrame.Shape.HLine)
        self.line_7.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_9.addWidget(self.line_7)

        self.groupBox_12 = QGroupBox(self.page_initial_conditions)
        self.groupBox_12.setObjectName(u"groupBox_12")
        self.groupBox_12.setFont(font5)
        self.groupBox_12.setStyleSheet(u"QGroupBox {\n"
"    border: 1px solid;\n"
"    border-radius: 6;\n"
"    margin-top: 9;\n"
"    border-color : #c8c8c8;\n"
"	padding: 3;   \n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    left: 10;\n"
"    padding: 2 3;\n"
"}")
        self.gridLayout_9 = QGridLayout(self.groupBox_12)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.edit_fluid_v_x = QLineEdit(self.groupBox_12)
        self.edit_fluid_v_x.setObjectName(u"edit_fluid_v_x")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.edit_fluid_v_x.sizePolicy().hasHeightForWidth())
        self.edit_fluid_v_x.setSizePolicy(sizePolicy3)
        self.edit_fluid_v_x.setMaximumSize(QSize(16777215, 16777215))
        self.edit_fluid_v_x.setFont(font6)
        self.edit_fluid_v_x.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.edit_fluid_v_x)

        self.edit_fluid_v_y = QLineEdit(self.groupBox_12)
        self.edit_fluid_v_y.setObjectName(u"edit_fluid_v_y")
        sizePolicy3.setHeightForWidth(self.edit_fluid_v_y.sizePolicy().hasHeightForWidth())
        self.edit_fluid_v_y.setSizePolicy(sizePolicy3)
        self.edit_fluid_v_y.setMaximumSize(QSize(16777215, 16777215))
        self.edit_fluid_v_y.setFont(font6)
        self.edit_fluid_v_y.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.edit_fluid_v_y)

        self.edit_fluid_v_z = QLineEdit(self.groupBox_12)
        self.edit_fluid_v_z.setObjectName(u"edit_fluid_v_z")
        sizePolicy3.setHeightForWidth(self.edit_fluid_v_z.sizePolicy().hasHeightForWidth())
        self.edit_fluid_v_z.setSizePolicy(sizePolicy3)
        self.edit_fluid_v_z.setMaximumSize(QSize(16777215, 16777215))
        self.edit_fluid_v_z.setFont(font6)
        self.edit_fluid_v_z.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.edit_fluid_v_z)


        self.gridLayout_9.addLayout(self.horizontalLayout_3, 3, 1, 1, 1)

        self.label_44 = QLabel(self.groupBox_12)
        self.label_44.setObjectName(u"label_44")
        self.label_44.setFont(font6)

        self.gridLayout_9.addWidget(self.label_44, 2, 0, 1, 1)

        self.label_45 = QLabel(self.groupBox_12)
        self.label_45.setObjectName(u"label_45")
        self.label_45.setFont(font6)

        self.gridLayout_9.addWidget(self.label_45, 0, 0, 1, 1)

        self.edit_fluid_2 = QLineEdit(self.groupBox_12)
        self.edit_fluid_2.setObjectName(u"edit_fluid_2")
        self.edit_fluid_2.setFont(font6)
        self.edit_fluid_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_9.addWidget(self.edit_fluid_2, 1, 1, 2, 1)

        self.edit_fluid_1 = QLineEdit(self.groupBox_12)
        self.edit_fluid_1.setObjectName(u"edit_fluid_1")
        self.edit_fluid_1.setFont(font6)
        self.edit_fluid_1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_9.addWidget(self.edit_fluid_1, 0, 1, 1, 1)

        self.label_43 = QLabel(self.groupBox_12)
        self.label_43.setObjectName(u"label_43")
        self.label_43.setFont(font6)

        self.gridLayout_9.addWidget(self.label_43, 3, 0, 1, 1)

        self.gridLayout_9.setColumnStretch(0, 1)
        self.gridLayout_9.setColumnStretch(1, 1)

        self.verticalLayout_9.addWidget(self.groupBox_12)

        self.groupBox_11 = QGroupBox(self.page_initial_conditions)
        self.groupBox_11.setObjectName(u"groupBox_11")
        self.groupBox_11.setFont(font5)
        self.groupBox_11.setStyleSheet(u"QGroupBox {\n"
"    border: 1px solid;\n"
"    border-radius: 6;\n"
"    margin-top: 9;\n"
"    border-color : #c8c8c8;\n"
"	padding: 3;   \n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    left: 10;\n"
"    padding: 2 3;\n"
"}")
        self.gridLayout_8 = QGridLayout(self.groupBox_11)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.comboBox_9 = QComboBox(self.groupBox_11)
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.setObjectName(u"comboBox_9")

        self.gridLayout_8.addWidget(self.comboBox_9, 3, 1, 1, 1)

        self.edit_solid_2 = QLineEdit(self.groupBox_11)
        self.edit_solid_2.setObjectName(u"edit_solid_2")
        self.edit_solid_2.setFont(font6)
        self.edit_solid_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.edit_solid_2, 2, 1, 1, 1)

        self.label_9 = QLabel(self.groupBox_11)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font6)

        self.gridLayout_8.addWidget(self.label_9, 2, 0, 1, 1)

        self.edit_solid_1 = QLineEdit(self.groupBox_11)
        self.edit_solid_1.setObjectName(u"edit_solid_1")
        self.edit_solid_1.setFont(font6)
        self.edit_solid_1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.edit_solid_1, 0, 1, 2, 1)

        self.label_42 = QLabel(self.groupBox_11)
        self.label_42.setObjectName(u"label_42")
        self.label_42.setFont(font6)

        self.gridLayout_8.addWidget(self.label_42, 3, 0, 1, 1)

        self.label_41 = QLabel(self.groupBox_11)
        self.label_41.setObjectName(u"label_41")
        self.label_41.setFont(font6)

        self.gridLayout_8.addWidget(self.label_41, 1, 0, 1, 1)

        self.gridLayout_8.setColumnStretch(0, 1)
        self.gridLayout_8.setColumnStretch(1, 1)

        self.verticalLayout_9.addWidget(self.groupBox_11)

        self.verticalSpacer_7 = QSpacerItem(20, 634, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_9.addItem(self.verticalSpacer_7)

        self.stackedWidget.addWidget(self.page_initial_conditions)
        self.page_mmh = QWidget()
        self.page_mmh.setObjectName(u"page_mmh")
        self.verticalLayout_3 = QVBoxLayout(self.page_mmh)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.sprayMMH = QLabel(self.page_mmh)
        self.sprayMMH.setObjectName(u"sprayMMH")
        self.sprayMMH.setFont(font4)

        self.verticalLayout_3.addWidget(self.sprayMMH)

        self.line_2 = QFrame(self.page_mmh)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_3.addWidget(self.line_2)

        self.groupBox_5 = QGroupBox(self.page_mmh)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setFont(font5)
        self.groupBox_5.setStyleSheet(u"QGroupBox {\n"
"    border: 1px solid;\n"
"    border-radius: 6;\n"
"    margin-top: 9;\n"
"    border-color : #c8c8c8;\n"
"	padding: 3;   \n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    left: 10;\n"
"    padding: 2 3;\n"
"}")
        self.gridLayout = QGridLayout(self.groupBox_5)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_18 = QLabel(self.groupBox_5)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setFont(font6)

        self.gridLayout.addWidget(self.label_18, 6, 0, 1, 1)

        self.label_11 = QLabel(self.groupBox_5)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font6)

        self.gridLayout.addWidget(self.label_11, 2, 0, 1, 1)

        self.edit_spray_mmh_3 = QLineEdit(self.groupBox_5)
        self.edit_spray_mmh_3.setObjectName(u"edit_spray_mmh_3")
        self.edit_spray_mmh_3.setFont(font6)
        self.edit_spray_mmh_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.edit_spray_mmh_3, 3, 1, 1, 1)

        self.label_12 = QLabel(self.groupBox_5)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font6)

        self.gridLayout.addWidget(self.label_12, 3, 0, 1, 1)

        self.edit_spray_mmh_4 = QLineEdit(self.groupBox_5)
        self.edit_spray_mmh_4.setObjectName(u"edit_spray_mmh_4")
        self.edit_spray_mmh_4.setFont(font6)
        self.edit_spray_mmh_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.edit_spray_mmh_4, 4, 1, 1, 1)

        self.edit_spray_mmh_5 = QLineEdit(self.groupBox_5)
        self.edit_spray_mmh_5.setObjectName(u"edit_spray_mmh_5")
        self.edit_spray_mmh_5.setFont(font6)
        self.edit_spray_mmh_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.edit_spray_mmh_5, 6, 1, 1, 1)

        self.label_6 = QLabel(self.groupBox_5)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font6)

        self.gridLayout.addWidget(self.label_6, 0, 0, 1, 1)

        self.edit_spray_mmh_2 = QLineEdit(self.groupBox_5)
        self.edit_spray_mmh_2.setObjectName(u"edit_spray_mmh_2")
        self.edit_spray_mmh_2.setFont(font6)
        self.edit_spray_mmh_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.edit_spray_mmh_2, 2, 1, 1, 1)

        self.edit_spray_mmh_1 = QLineEdit(self.groupBox_5)
        self.edit_spray_mmh_1.setObjectName(u"edit_spray_mmh_1")
        self.edit_spray_mmh_1.setFont(font6)
        self.edit_spray_mmh_1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.edit_spray_mmh_1, 0, 1, 1, 1)

        self.label_13 = QLabel(self.groupBox_5)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFont(font6)

        self.gridLayout.addWidget(self.label_13, 4, 0, 1, 1)

        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)

        self.verticalLayout_3.addWidget(self.groupBox_5)

        self.groupBox_4 = QGroupBox(self.page_mmh)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setFont(font5)
        self.groupBox_4.setStyleSheet(u"QGroupBox {\n"
"    border: 1px solid;\n"
"    border-radius: 6;\n"
"    margin-top: 9;\n"
"    border-color : #c8c8c8;\n"
"	padding: 3;   \n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    left: 10;\n"
"    padding: 2 3;\n"
"}")
        self.gridLayout_6 = QGridLayout(self.groupBox_4)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.edit_spray_mmh_13 = QLineEdit(self.groupBox_4)
        self.edit_spray_mmh_13.setObjectName(u"edit_spray_mmh_13")
        self.edit_spray_mmh_13.setFont(font6)
        self.edit_spray_mmh_13.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.edit_spray_mmh_13, 4, 1, 1, 1)

        self.label_24 = QLabel(self.groupBox_4)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setFont(font6)

        self.gridLayout_6.addWidget(self.label_24, 2, 0, 1, 1)

        self.label_21 = QLabel(self.groupBox_4)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setFont(font6)

        self.gridLayout_6.addWidget(self.label_21, 0, 0, 1, 1)

        self.label_23 = QLabel(self.groupBox_4)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setFont(font6)

        self.gridLayout_6.addWidget(self.label_23, 3, 0, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.edit_spray_mmh_9 = QLineEdit(self.groupBox_4)
        self.edit_spray_mmh_9.setObjectName(u"edit_spray_mmh_9")
        self.edit_spray_mmh_9.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_5.addWidget(self.edit_spray_mmh_9)

        self.edit_spray_mmh_10 = QLineEdit(self.groupBox_4)
        self.edit_spray_mmh_10.setObjectName(u"edit_spray_mmh_10")
        self.edit_spray_mmh_10.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_5.addWidget(self.edit_spray_mmh_10)

        self.edit_spray_mmh_11 = QLineEdit(self.groupBox_4)
        self.edit_spray_mmh_11.setObjectName(u"edit_spray_mmh_11")
        self.edit_spray_mmh_11.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_5.addWidget(self.edit_spray_mmh_11)


        self.gridLayout_6.addLayout(self.horizontalLayout_5, 2, 1, 1, 1)

        self.label_22 = QLabel(self.groupBox_4)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setFont(font6)

        self.gridLayout_6.addWidget(self.label_22, 4, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.edit_spray_mmh_6 = QLineEdit(self.groupBox_4)
        self.edit_spray_mmh_6.setObjectName(u"edit_spray_mmh_6")
        self.edit_spray_mmh_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_4.addWidget(self.edit_spray_mmh_6)

        self.edit_spray_mmh_7 = QLineEdit(self.groupBox_4)
        self.edit_spray_mmh_7.setObjectName(u"edit_spray_mmh_7")
        self.edit_spray_mmh_7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_4.addWidget(self.edit_spray_mmh_7)

        self.edit_spray_mmh_8 = QLineEdit(self.groupBox_4)
        self.edit_spray_mmh_8.setObjectName(u"edit_spray_mmh_8")
        self.edit_spray_mmh_8.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_4.addWidget(self.edit_spray_mmh_8)


        self.gridLayout_6.addLayout(self.horizontalLayout_4, 0, 1, 1, 1)

        self.edit_spray_mmh_12 = QLineEdit(self.groupBox_4)
        self.edit_spray_mmh_12.setObjectName(u"edit_spray_mmh_12")
        self.edit_spray_mmh_12.setFont(font6)
        self.edit_spray_mmh_12.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.edit_spray_mmh_12, 3, 1, 1, 1)

        self.gridLayout_6.setColumnStretch(0, 1)
        self.gridLayout_6.setColumnStretch(1, 1)

        self.verticalLayout_3.addWidget(self.groupBox_4)

        self.verticalSpacer_2 = QSpacerItem(20, 536, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)

        self.stackedWidget.addWidget(self.page_mmh)
        self.page_nto = QWidget()
        self.page_nto.setObjectName(u"page_nto")
        self.verticalLayout_4 = QVBoxLayout(self.page_nto)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.sprayMMH_2 = QLabel(self.page_nto)
        self.sprayMMH_2.setObjectName(u"sprayMMH_2")
        self.sprayMMH_2.setFont(font4)

        self.verticalLayout_4.addWidget(self.sprayMMH_2)

        self.line_3 = QFrame(self.page_nto)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_4.addWidget(self.line_3)

        self.groupBox_7 = QGroupBox(self.page_nto)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.groupBox_7.setFont(font5)
        self.groupBox_7.setStyleSheet(u"QGroupBox {\n"
"    border: 1px solid;\n"
"    border-radius: 6;\n"
"    margin-top: 9;\n"
"    border-color : #c8c8c8;\n"
"	padding: 3;   \n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    left: 10;\n"
"    padding: 2 3;\n"
"}")
        self.gridLayout_4 = QGridLayout(self.groupBox_7)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_14 = QLabel(self.groupBox_7)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setFont(font6)

        self.gridLayout_4.addWidget(self.label_14, 4, 0, 1, 1)

        self.label_7 = QLabel(self.groupBox_7)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font6)

        self.gridLayout_4.addWidget(self.label_7, 0, 0, 1, 1)

        self.label_20 = QLabel(self.groupBox_7)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setFont(font6)

        self.gridLayout_4.addWidget(self.label_20, 6, 0, 1, 1)

        self.edit_spray_nto_4 = QLineEdit(self.groupBox_7)
        self.edit_spray_nto_4.setObjectName(u"edit_spray_nto_4")
        self.edit_spray_nto_4.setFont(font6)
        self.edit_spray_nto_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.edit_spray_nto_4, 4, 1, 1, 1)

        self.edit_spray_nto_5 = QLineEdit(self.groupBox_7)
        self.edit_spray_nto_5.setObjectName(u"edit_spray_nto_5")
        self.edit_spray_nto_5.setFont(font6)
        self.edit_spray_nto_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.edit_spray_nto_5, 6, 1, 1, 1)

        self.label_16 = QLabel(self.groupBox_7)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setFont(font6)

        self.gridLayout_4.addWidget(self.label_16, 2, 0, 1, 1)

        self.edit_spray_nto_3 = QLineEdit(self.groupBox_7)
        self.edit_spray_nto_3.setObjectName(u"edit_spray_nto_3")
        self.edit_spray_nto_3.setFont(font6)
        self.edit_spray_nto_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.edit_spray_nto_3, 3, 1, 1, 1)

        self.edit_spray_nto_2 = QLineEdit(self.groupBox_7)
        self.edit_spray_nto_2.setObjectName(u"edit_spray_nto_2")
        self.edit_spray_nto_2.setFont(font6)
        self.edit_spray_nto_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.edit_spray_nto_2, 2, 1, 1, 1)

        self.edit_spray_nto_1 = QLineEdit(self.groupBox_7)
        self.edit_spray_nto_1.setObjectName(u"edit_spray_nto_1")
        self.edit_spray_nto_1.setFont(font6)
        self.edit_spray_nto_1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.edit_spray_nto_1, 0, 1, 1, 1)

        self.label_15 = QLabel(self.groupBox_7)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setFont(font6)

        self.gridLayout_4.addWidget(self.label_15, 3, 0, 1, 1)

        self.gridLayout_4.setColumnStretch(0, 1)
        self.gridLayout_4.setColumnStretch(1, 1)

        self.verticalLayout_4.addWidget(self.groupBox_7)

        self.groupBox_6 = QGroupBox(self.page_nto)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setFont(font5)
        self.groupBox_6.setStyleSheet(u"QGroupBox {\n"
"    border: 1px solid;\n"
"    border-radius: 6;\n"
"    margin-top: 9;\n"
"    border-color : #c8c8c8;\n"
"	padding: 3;   \n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    left: 10;\n"
"    padding: 2 3;\n"
"}")
        self.gridLayout_7 = QGridLayout(self.groupBox_6)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.edit_spray_nto_6 = QLineEdit(self.groupBox_6)
        self.edit_spray_nto_6.setObjectName(u"edit_spray_nto_6")
        self.edit_spray_nto_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_6.addWidget(self.edit_spray_nto_6)

        self.edit_spray_nto_7 = QLineEdit(self.groupBox_6)
        self.edit_spray_nto_7.setObjectName(u"edit_spray_nto_7")
        self.edit_spray_nto_7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_6.addWidget(self.edit_spray_nto_7)

        self.edit_spray_nto_8 = QLineEdit(self.groupBox_6)
        self.edit_spray_nto_8.setObjectName(u"edit_spray_nto_8")
        self.edit_spray_nto_8.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_6.addWidget(self.edit_spray_nto_8)


        self.gridLayout_7.addLayout(self.horizontalLayout_6, 0, 1, 1, 1)

        self.label_26 = QLabel(self.groupBox_6)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setFont(font6)

        self.gridLayout_7.addWidget(self.label_26, 0, 0, 1, 1)

        self.label_28 = QLabel(self.groupBox_6)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setFont(font6)

        self.gridLayout_7.addWidget(self.label_28, 4, 0, 1, 1)

        self.label_25 = QLabel(self.groupBox_6)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setFont(font6)

        self.gridLayout_7.addWidget(self.label_25, 2, 0, 1, 1)

        self.edit_spray_nto_13 = QLineEdit(self.groupBox_6)
        self.edit_spray_nto_13.setObjectName(u"edit_spray_nto_13")
        self.edit_spray_nto_13.setFont(font6)
        self.edit_spray_nto_13.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.edit_spray_nto_13, 4, 1, 1, 1)

        self.label_27 = QLabel(self.groupBox_6)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setFont(font6)

        self.gridLayout_7.addWidget(self.label_27, 3, 0, 1, 1)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.edit_spray_nto_9 = QLineEdit(self.groupBox_6)
        self.edit_spray_nto_9.setObjectName(u"edit_spray_nto_9")
        self.edit_spray_nto_9.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_7.addWidget(self.edit_spray_nto_9)

        self.edit_spray_nto_10 = QLineEdit(self.groupBox_6)
        self.edit_spray_nto_10.setObjectName(u"edit_spray_nto_10")
        self.edit_spray_nto_10.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_7.addWidget(self.edit_spray_nto_10)

        self.edit_spray_nto_11 = QLineEdit(self.groupBox_6)
        self.edit_spray_nto_11.setObjectName(u"edit_spray_nto_11")
        self.edit_spray_nto_11.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_7.addWidget(self.edit_spray_nto_11)


        self.gridLayout_7.addLayout(self.horizontalLayout_7, 2, 1, 1, 1)

        self.edit_spray_nto_12 = QLineEdit(self.groupBox_6)
        self.edit_spray_nto_12.setObjectName(u"edit_spray_nto_12")
        self.edit_spray_nto_12.setFont(font6)
        self.edit_spray_nto_12.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.edit_spray_nto_12, 3, 1, 1, 1)

        self.gridLayout_7.setColumnStretch(0, 1)
        self.gridLayout_7.setColumnStretch(1, 1)

        self.verticalLayout_4.addWidget(self.groupBox_6)

        self.verticalSpacer_3 = QSpacerItem(20, 588, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_3)

        self.stackedWidget.addWidget(self.page_nto)
        self.page_numerical_conditions = QWidget()
        self.page_numerical_conditions.setObjectName(u"page_numerical_conditions")
        self.verticalLayout_7 = QVBoxLayout(self.page_numerical_conditions)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_8 = QLabel(self.page_numerical_conditions)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font4)

        self.verticalLayout_7.addWidget(self.label_8)

        self.line_4 = QFrame(self.page_numerical_conditions)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_7.addWidget(self.line_4)

        self.groupBox_8 = QGroupBox(self.page_numerical_conditions)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.groupBox_8.setFont(font)
        self.groupBox_8.setStyleSheet(u"QGroupBox {\n"
"    border: 1px solid;\n"
"    border-radius: 6;\n"
"    margin-top: 9;\n"
"    border-color : #c8c8c8;\n"
"	padding: 3;   \n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    left: 10;\n"
"    padding: 2 3;\n"
"}")
        self.gridLayout_15 = QGridLayout(self.groupBox_8)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.combo_numerical_3 = QComboBox(self.groupBox_8)
        self.combo_numerical_3.addItem("")
        self.combo_numerical_3.addItem("")
        self.combo_numerical_3.addItem("")
        self.combo_numerical_3.setObjectName(u"combo_numerical_3")

        self.gridLayout_15.addWidget(self.combo_numerical_3, 2, 1, 1, 1)

        self.label_29 = QLabel(self.groupBox_8)
        self.label_29.setObjectName(u"label_29")

        self.gridLayout_15.addWidget(self.label_29, 0, 0, 1, 1)

        self.combo_numerical_2 = QComboBox(self.groupBox_8)
        self.combo_numerical_2.addItem("")
        self.combo_numerical_2.addItem("")
        self.combo_numerical_2.addItem("")
        self.combo_numerical_2.setObjectName(u"combo_numerical_2")
        self.combo_numerical_2.setAcceptDrops(False)

        self.gridLayout_15.addWidget(self.combo_numerical_2, 1, 1, 1, 1)

        self.label_10 = QLabel(self.groupBox_8)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_15.addWidget(self.label_10, 4, 0, 1, 1)

        self.label_30 = QLabel(self.groupBox_8)
        self.label_30.setObjectName(u"label_30")

        self.gridLayout_15.addWidget(self.label_30, 1, 0, 1, 1)

        self.combo_numerical_5 = QComboBox(self.groupBox_8)
        self.combo_numerical_5.addItem("")
        self.combo_numerical_5.addItem("")
        self.combo_numerical_5.addItem("")
        self.combo_numerical_5.setObjectName(u"combo_numerical_5")

        self.gridLayout_15.addWidget(self.combo_numerical_5, 4, 1, 1, 1)

        self.combo_numerical_4 = QComboBox(self.groupBox_8)
        self.combo_numerical_4.addItem("")
        self.combo_numerical_4.addItem("")
        self.combo_numerical_4.setObjectName(u"combo_numerical_4")

        self.gridLayout_15.addWidget(self.combo_numerical_4, 3, 1, 1, 1)

        self.combo_numerical_1 = QComboBox(self.groupBox_8)
        self.combo_numerical_1.addItem("")
        self.combo_numerical_1.addItem("")
        self.combo_numerical_1.setObjectName(u"combo_numerical_1")

        self.gridLayout_15.addWidget(self.combo_numerical_1, 0, 1, 1, 1)

        self.label_32 = QLabel(self.groupBox_8)
        self.label_32.setObjectName(u"label_32")

        self.gridLayout_15.addWidget(self.label_32, 3, 0, 1, 1)

        self.label_31 = QLabel(self.groupBox_8)
        self.label_31.setObjectName(u"label_31")

        self.gridLayout_15.addWidget(self.label_31, 2, 0, 1, 1)

        self.gridLayout_15.setColumnStretch(0, 1)
        self.gridLayout_15.setColumnStretch(1, 1)

        self.verticalLayout_7.addWidget(self.groupBox_8)

        self.groupBox_9 = QGroupBox(self.page_numerical_conditions)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.groupBox_9.setFont(font)
        self.groupBox_9.setStyleSheet(u"QGroupBox {\n"
"    border: 1px solid;\n"
"    border-radius: 6;\n"
"    margin-top: 9;\n"
"    border-color : #c8c8c8;\n"
"	padding: 3;   \n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    left: 10;\n"
"    padding: 2 3;\n"
"}")
        self.gridLayout_5 = QGridLayout(self.groupBox_9)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.edit_numerical_1 = QLineEdit(self.groupBox_9)
        self.edit_numerical_1.setObjectName(u"edit_numerical_1")
        font8 = QFont()
        font8.setBold(False)
        self.edit_numerical_1.setFont(font8)
        self.edit_numerical_1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.edit_numerical_1, 0, 1, 1, 1)

        self.label_34 = QLabel(self.groupBox_9)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setFont(font8)

        self.gridLayout_5.addWidget(self.label_34, 0, 0, 1, 1)

        self.edit_numerical_2 = QLineEdit(self.groupBox_9)
        self.edit_numerical_2.setObjectName(u"edit_numerical_2")
        self.edit_numerical_2.setFont(font8)
        self.edit_numerical_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.edit_numerical_2, 1, 1, 1, 1)

        self.combo_numerical_6 = QComboBox(self.groupBox_9)
        self.combo_numerical_6.addItem("")
        self.combo_numerical_6.addItem("")
        self.combo_numerical_6.setObjectName(u"combo_numerical_6")

        self.gridLayout_5.addWidget(self.combo_numerical_6, 3, 1, 1, 1)

        self.label_37 = QLabel(self.groupBox_9)
        self.label_37.setObjectName(u"label_37")
        self.label_37.setFont(font8)

        self.gridLayout_5.addWidget(self.label_37, 3, 0, 1, 1)

        self.label_36 = QLabel(self.groupBox_9)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setFont(font8)

        self.gridLayout_5.addWidget(self.label_36, 2, 0, 1, 1)

        self.label_35 = QLabel(self.groupBox_9)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setFont(font8)

        self.gridLayout_5.addWidget(self.label_35, 1, 0, 1, 1)

        self.edit_numerical_3 = QLineEdit(self.groupBox_9)
        self.edit_numerical_3.setObjectName(u"edit_numerical_3")
        self.edit_numerical_3.setFont(font8)
        self.edit_numerical_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.edit_numerical_3, 2, 1, 1, 1)

        self.gridLayout_5.setColumnStretch(0, 1)
        self.gridLayout_5.setColumnStretch(1, 1)

        self.verticalLayout_7.addWidget(self.groupBox_9)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_4)

        self.stackedWidget.addWidget(self.page_numerical_conditions)
        self.page_run_conditions = QWidget()
        self.page_run_conditions.setObjectName(u"page_run_conditions")
        self.verticalLayout = QVBoxLayout(self.page_run_conditions)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.title = QLabel(self.page_run_conditions)
        self.title.setObjectName(u"title")
        sizePolicy2.setHeightForWidth(self.title.sizePolicy().hasHeightForWidth())
        self.title.setSizePolicy(sizePolicy2)
        self.title.setFont(font4)

        self.verticalLayout.addWidget(self.title)

        self.line = QFrame(self.page_run_conditions)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.groupBox_2 = QGroupBox(self.page_run_conditions)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setFont(font)
        self.groupBox_2.setStyleSheet(u"QGroupBox {\n"
"    border: 1px solid;\n"
"    border-radius: 6;\n"
"    margin-top: 9;\n"
"    border-color : #c8c8c8;\n"
"	padding: 3;   \n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    left: 10;\n"
"    padding: 2 3;\n"
"}")
        self.gridLayout_2 = QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.combo_run_1 = QComboBox(self.groupBox_2)
        self.combo_run_1.addItem("")
        self.combo_run_1.addItem("")
        self.combo_run_1.setObjectName(u"combo_run_1")

        self.gridLayout_2.addWidget(self.combo_run_1, 6, 1, 1, 1)

        self.edit_run_3 = QLineEdit(self.groupBox_2)
        self.edit_run_3.setObjectName(u"edit_run_3")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.edit_run_3.sizePolicy().hasHeightForWidth())
        self.edit_run_3.setSizePolicy(sizePolicy4)
        self.edit_run_3.setMinimumSize(QSize(135, 0))
        font9 = QFont()
        font9.setFamilies([u"\ub9d1\uc740 \uace0\ub515"])
        font9.setPointSize(9)
        font9.setBold(False)
        self.edit_run_3.setFont(font9)
        self.edit_run_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.edit_run_3, 2, 1, 1, 1)

        self.edit_run_5 = QLineEdit(self.groupBox_2)
        self.edit_run_5.setObjectName(u"edit_run_5")
        sizePolicy4.setHeightForWidth(self.edit_run_5.sizePolicy().hasHeightForWidth())
        self.edit_run_5.setSizePolicy(sizePolicy4)
        self.edit_run_5.setMinimumSize(QSize(135, 0))
        self.edit_run_5.setFont(font9)
        self.edit_run_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.edit_run_5, 4, 1, 1, 1)

        self.label_71 = QLabel(self.groupBox_2)
        self.label_71.setObjectName(u"label_71")
        self.label_71.setFont(font9)

        self.gridLayout_2.addWidget(self.label_71, 8, 0, 1, 1)

        self.edit_run_8 = QLineEdit(self.groupBox_2)
        self.edit_run_8.setObjectName(u"edit_run_8")
        sizePolicy4.setHeightForWidth(self.edit_run_8.sizePolicy().hasHeightForWidth())
        self.edit_run_8.setSizePolicy(sizePolicy4)
        self.edit_run_8.setMinimumSize(QSize(135, 0))
        self.edit_run_8.setFont(font9)
        self.edit_run_8.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.edit_run_8, 8, 1, 1, 1)

        self.label_77 = QLabel(self.groupBox_2)
        self.label_77.setObjectName(u"label_77")
        self.label_77.setFont(font9)

        self.gridLayout_2.addWidget(self.label_77, 0, 0, 1, 1)

        self.label_67 = QLabel(self.groupBox_2)
        self.label_67.setObjectName(u"label_67")
        self.label_67.setFont(font9)

        self.gridLayout_2.addWidget(self.label_67, 4, 0, 1, 1)

        self.edit_run_7 = QLineEdit(self.groupBox_2)
        self.edit_run_7.setObjectName(u"edit_run_7")
        sizePolicy4.setHeightForWidth(self.edit_run_7.sizePolicy().hasHeightForWidth())
        self.edit_run_7.setSizePolicy(sizePolicy4)
        self.edit_run_7.setMinimumSize(QSize(135, 0))
        self.edit_run_7.setFont(font9)
        self.edit_run_7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.edit_run_7, 7, 1, 1, 1)

        self.label_78 = QLabel(self.groupBox_2)
        self.label_78.setObjectName(u"label_78")
        self.label_78.setFont(font9)

        self.gridLayout_2.addWidget(self.label_78, 1, 0, 1, 1)

        self.edit_run_2 = QLineEdit(self.groupBox_2)
        self.edit_run_2.setObjectName(u"edit_run_2")
        sizePolicy4.setHeightForWidth(self.edit_run_2.sizePolicy().hasHeightForWidth())
        self.edit_run_2.setSizePolicy(sizePolicy4)
        self.edit_run_2.setMinimumSize(QSize(135, 0))
        self.edit_run_2.setFont(font9)
        self.edit_run_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.edit_run_2, 1, 1, 1, 1)

        self.label_72 = QLabel(self.groupBox_2)
        self.label_72.setObjectName(u"label_72")
        self.label_72.setFont(font9)

        self.gridLayout_2.addWidget(self.label_72, 6, 0, 1, 1)

        self.label_79 = QLabel(self.groupBox_2)
        self.label_79.setObjectName(u"label_79")
        self.label_79.setFont(font9)

        self.gridLayout_2.addWidget(self.label_79, 2, 0, 1, 1)

        self.edit_run_4 = QLineEdit(self.groupBox_2)
        self.edit_run_4.setObjectName(u"edit_run_4")
        sizePolicy4.setHeightForWidth(self.edit_run_4.sizePolicy().hasHeightForWidth())
        self.edit_run_4.setSizePolicy(sizePolicy4)
        self.edit_run_4.setMinimumSize(QSize(135, 0))
        self.edit_run_4.setFont(font9)
        self.edit_run_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.edit_run_4, 3, 1, 1, 1)

        self.label_70 = QLabel(self.groupBox_2)
        self.label_70.setObjectName(u"label_70")
        self.label_70.setFont(font9)

        self.gridLayout_2.addWidget(self.label_70, 7, 0, 1, 1)

        self.label_80 = QLabel(self.groupBox_2)
        self.label_80.setObjectName(u"label_80")
        self.label_80.setFont(font9)

        self.gridLayout_2.addWidget(self.label_80, 3, 0, 1, 1)

        self.edit_run_1 = QLineEdit(self.groupBox_2)
        self.edit_run_1.setObjectName(u"edit_run_1")
        sizePolicy4.setHeightForWidth(self.edit_run_1.sizePolicy().hasHeightForWidth())
        self.edit_run_1.setSizePolicy(sizePolicy4)
        self.edit_run_1.setMinimumSize(QSize(135, 0))
        self.edit_run_1.setFont(font9)
        self.edit_run_1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.edit_run_1, 0, 1, 1, 1)

        self.groupBox_13 = QGroupBox(self.groupBox_2)
        self.groupBox_13.setObjectName(u"groupBox_13")
        sizePolicy2.setHeightForWidth(self.groupBox_13.sizePolicy().hasHeightForWidth())
        self.groupBox_13.setSizePolicy(sizePolicy2)
        font10 = QFont()
        font10.setFamilies([u"\ub9d1\uc740 \uace0\ub515"])
        font10.setPointSize(10)
        font10.setBold(True)
        self.groupBox_13.setFont(font10)
        self.groupBox_13.setCheckable(True)
        self.groupBox_13.setChecked(False)
        self.verticalLayout_13 = QVBoxLayout(self.groupBox_13)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.frame = QFrame(self.groupBox_13)
        self.frame.setObjectName(u"frame")
        self.horizontalLayout_16 = QHBoxLayout(self.frame)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(-1, 0, -1, 0)
        self.label_68 = QLabel(self.frame)
        self.label_68.setObjectName(u"label_68")
        self.label_68.setFont(font9)

        self.horizontalLayout_16.addWidget(self.label_68)

        self.edit_run_6 = QLineEdit(self.frame)
        self.edit_run_6.setObjectName(u"edit_run_6")
        sizePolicy4.setHeightForWidth(self.edit_run_6.sizePolicy().hasHeightForWidth())
        self.edit_run_6.setSizePolicy(sizePolicy4)
        self.edit_run_6.setMinimumSize(QSize(135, 0))
        self.edit_run_6.setFont(font9)
        self.edit_run_6.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_16.addWidget(self.edit_run_6)


        self.verticalLayout_13.addWidget(self.frame)


        self.gridLayout_2.addWidget(self.groupBox_13, 5, 0, 1, 2)

        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout_2.setColumnStretch(1, 1)

        self.verticalLayout.addWidget(self.groupBox_2)

        self.verticalSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.stackedWidget.addWidget(self.page_run_conditions)
        self.page_run = QWidget()
        self.page_run.setObjectName(u"page_run")
        self.verticalLayout_2 = QVBoxLayout(self.page_run)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.title_6 = QLabel(self.page_run)
        self.title_6.setObjectName(u"title_6")
        sizePolicy2.setHeightForWidth(self.title_6.sizePolicy().hasHeightForWidth())
        self.title_6.setSizePolicy(sizePolicy2)
        self.title_6.setFont(font4)

        self.verticalLayout_2.addWidget(self.title_6)

        self.line_9 = QFrame(self.page_run)
        self.line_9.setObjectName(u"line_9")
        self.line_9.setFrameShape(QFrame.Shape.HLine)
        self.line_9.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line_9)

        self.groupBox = QGroupBox(self.page_run)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setFont(font)
        self.groupBox.setStyleSheet(u"QGroupBox {\n"
"    border: 1px solid;\n"
"    border-radius: 6;\n"
"    margin-top: 9;\n"
"    border-color : #c8c8c8;\n"
"	padding: 3;   \n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    left: 10;\n"
"    padding: 2 3;\n"
"}")
        self.gridLayout_3 = QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.edit_run_9 = QLabel(self.groupBox)
        self.edit_run_9.setObjectName(u"edit_run_9")
        self.edit_run_9.setFont(font8)
        self.edit_run_9.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.edit_run_9, 1, 1, 1, 1)

        self.edit_run_id = QLabel(self.groupBox)
        self.edit_run_id.setObjectName(u"edit_run_id")
        self.edit_run_id.setFont(font8)
        self.edit_run_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.edit_run_id, 0, 1, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font8)
        self.label_2.setScaledContents(False)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font8)

        self.gridLayout_3.addWidget(self.label_4, 2, 0, 1, 1)

        self.edit_run_10 = QLabel(self.groupBox)
        self.edit_run_10.setObjectName(u"edit_run_10")
        self.edit_run_10.setFont(font8)
        self.edit_run_10.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.edit_run_10, 2, 1, 1, 1)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font8)

        self.gridLayout_3.addWidget(self.label_3, 1, 0, 1, 1)

        self.gridLayout_3.setColumnStretch(1, 1)

        self.verticalLayout_2.addWidget(self.groupBox)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(-1, 0, -1, -1)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer)

        self.button_edit_hostfile_run = QPushButton(self.page_run)
        self.button_edit_hostfile_run.setObjectName(u"button_edit_hostfile_run")
        sizePolicy2.setHeightForWidth(self.button_edit_hostfile_run.sizePolicy().hasHeightForWidth())
        self.button_edit_hostfile_run.setSizePolicy(sizePolicy2)
        self.button_edit_hostfile_run.setMinimumSize(QSize(0, 30))
        self.button_edit_hostfile_run.setFont(font6)

        self.horizontalLayout_8.addWidget(self.button_edit_hostfile_run)


        self.verticalLayout_2.addLayout(self.horizontalLayout_8)

        self.line_10 = QFrame(self.page_run)
        self.line_10.setObjectName(u"line_10")
        self.line_10.setFrameShape(QFrame.Shape.HLine)
        self.line_10.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line_10)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, -1, -1)
        self.button_run = QPushButton(self.page_run)
        self.button_run.setObjectName(u"button_run")
        self.button_run.setMinimumSize(QSize(0, 35))
        self.button_run.setFont(font5)
        self.button_run.setCheckable(False)

        self.horizontalLayout_2.addWidget(self.button_run)

        self.button_pause = QPushButton(self.page_run)
        self.button_pause.setObjectName(u"button_pause")
        self.button_pause.setMinimumSize(QSize(0, 35))
        self.button_pause.setFont(font8)

        self.horizontalLayout_2.addWidget(self.button_pause)

        self.button_stop = QPushButton(self.page_run)
        self.button_stop.setObjectName(u"button_stop")
        self.button_stop.setMinimumSize(QSize(0, 35))
        self.button_stop.setFont(font8)

        self.horizontalLayout_2.addWidget(self.button_stop)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.verticalSpacer_8 = QSpacerItem(20, 601, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_8)

        self.stackedWidget.addWidget(self.page_run)

        self.horizontalLayout.addWidget(self.stackedWidget)

        self.horizontalLayout.setStretch(1, 1)
        self.splitter_2.addWidget(self.layoutWidget)

        self.verticalLayout_14.addWidget(self.splitter_2)


        self.retranslateUi(Center)

        self.stackedWidget.setCurrentIndex(0)
        self.comboBox_2.setCurrentIndex(2)
        self.combo_numerical_2.setCurrentIndex(1)
        self.button_run.setDefault(False)


        QMetaObject.connectSlotsByName(Center)
    # setupUi

    def retranslateUi(self, Center):
        Center.setWindowTitle(QCoreApplication.translate("Center", u"Form", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Center", u"Control Menu", None));

        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.treeWidget.topLevelItem(0)
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("Center", u"Geometry", None));
        ___qtreewidgetitem2 = self.treeWidget.topLevelItem(1)
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("Center", u"Mesh Generation", None));
        ___qtreewidgetitem3 = self.treeWidget.topLevelItem(2)
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("Center", u"Setup", None));
        ___qtreewidgetitem4 = ___qtreewidgetitem3.child(0)
        ___qtreewidgetitem4.setText(0, QCoreApplication.translate("Center", u"Models", None));
        ___qtreewidgetitem5 = ___qtreewidgetitem3.child(1)
        ___qtreewidgetitem5.setText(0, QCoreApplication.translate("Center", u"Initial Conditions", None));
        ___qtreewidgetitem6 = ___qtreewidgetitem3.child(2)
        ___qtreewidgetitem6.setText(0, QCoreApplication.translate("Center", u"Spray - NMH", None));
        ___qtreewidgetitem7 = ___qtreewidgetitem3.child(3)
        ___qtreewidgetitem7.setText(0, QCoreApplication.translate("Center", u"Spray - NTO", None));
        ___qtreewidgetitem8 = self.treeWidget.topLevelItem(3)
        ___qtreewidgetitem8.setText(0, QCoreApplication.translate("Center", u"Solution", None));
        ___qtreewidgetitem9 = ___qtreewidgetitem8.child(0)
        ___qtreewidgetitem9.setText(0, QCoreApplication.translate("Center", u"Numerical Conditions", None));
        ___qtreewidgetitem10 = ___qtreewidgetitem8.child(1)
        ___qtreewidgetitem10.setText(0, QCoreApplication.translate("Center", u"Run Conditions", None));
        ___qtreewidgetitem11 = self.treeWidget.topLevelItem(4)
        ___qtreewidgetitem11.setText(0, QCoreApplication.translate("Center", u"Run", None));
        ___qtreewidgetitem12 = self.treeWidget.topLevelItem(5)
        ___qtreewidgetitem12.setText(0, QCoreApplication.translate("Center", u"Results", None));
        ___qtreewidgetitem13 = ___qtreewidgetitem12.child(0)
        ___qtreewidgetitem13.setText(0, QCoreApplication.translate("Center", u"Residual", None));
        ___qtreewidgetitem14 = ___qtreewidgetitem12.child(1)
        ___qtreewidgetitem14.setText(0, QCoreApplication.translate("Center", u"Post", None));
        self.treeWidget.setSortingEnabled(__sortingEnabled)

        self.title_2.setText(QCoreApplication.translate("Center", u"Geometry", None))
        self.button_geometry_add.setText(QCoreApplication.translate("Center", u"Add", None))
        self.button_geometry_remove.setText(QCoreApplication.translate("Center", u"Remove", None))
        ___qtreewidgetitem15 = self.tree_geometry.headerItem()
        ___qtreewidgetitem15.setText(0, QCoreApplication.translate("Center", u"Name", None));

        __sortingEnabled1 = self.tree_geometry.isSortingEnabled()
        self.tree_geometry.setSortingEnabled(False)
        ___qtreewidgetitem16 = self.tree_geometry.topLevelItem(0)
        ___qtreewidgetitem16.setText(0, QCoreApplication.translate("Center", u"fluid", None));
        self.tree_geometry.setSortingEnabled(__sortingEnabled1)

        self.AdvancedGroupBox_2.setTitle(QCoreApplication.translate("Center", u"< Input Position >", None))
        self.label_83.setText(QCoreApplication.translate("Center", u"X/ Y/ Z", None))
        self.button_geometry_reset.setText(QCoreApplication.translate("Center", u"Reset", None))
        self.button_geometry_apply.setText(QCoreApplication.translate("Center", u"Position Picking Mode", None))
        self.button_geometry_cancel.setText(QCoreApplication.translate("Center", u"Cancel", None))
        self.edit_input_position_x.setText(QCoreApplication.translate("Center", u"0", None))
        self.edit_input_position_y.setText(QCoreApplication.translate("Center", u"0", None))
        self.edit_input_position_z.setText(QCoreApplication.translate("Center", u"0", None))
        self.title_5.setText(QCoreApplication.translate("Center", u"Mesh generation", None))
        self.AdvancedGroupBox.setTitle(QCoreApplication.translate("Center", u"< Base Grid >", None))
        self.basegridBox.setTitle(QCoreApplication.translate("Center", u"< Number of Cells per Direction >", None))
        self.label_48.setText(QCoreApplication.translate("Center", u"Y", None))
        self.label_50.setText(QCoreApplication.translate("Center", u"X", None))
        self.label_49.setText(QCoreApplication.translate("Center", u"Z", None))
        self.lineEdit_basegrid_x.setText(QCoreApplication.translate("Center", u"161", None))
        self.lineEdit_basegrid_y.setText(QCoreApplication.translate("Center", u"81", None))
        self.lineEdit_basegrid_z.setText(QCoreApplication.translate("Center", u"81", None))
        self.boundaryGroupBox.setTitle(QCoreApplication.translate("Center", u"< Castellation >", None))
        self.edit_castellation_3.setText(QCoreApplication.translate("Center", u"0", None))
        self.edit_castellation_4.setText(QCoreApplication.translate("Center", u"0", None))
        self.label_52.setText(QCoreApplication.translate("Center", u"Cell between levels", None))
        self.edit_castellation_1.setText(QCoreApplication.translate("Center", u"2", None))
        self.label_54.setText(QCoreApplication.translate("Center", u"Surface Minimum Level", None))
        self.label_53.setText(QCoreApplication.translate("Center", u"Surface Maximum Level", None))
        self.edit_castellation_5.setText(QCoreApplication.translate("Center", u"0", None))
        self.edit_castellation_2.setText(QCoreApplication.translate("Center", u"60", None))
        self.label_51.setText(QCoreApplication.translate("Center", u"Volume Refinement level", None))
        self.label_55.setText(QCoreApplication.translate("Center", u"Feature Angle Threshold", None))
        self.bufferLayerBox.setTitle(QCoreApplication.translate("Center", u"< Snap >", None))
        self.edit_snap_3.setText(QCoreApplication.translate("Center", u"30", None))
        self.label_58.setText(QCoreApplication.translate("Center", u"Smoothing for Surface", None))
        self.edit_snap_4.setText(QCoreApplication.translate("Center", u"5", None))
        self.edit_snap_2.setText(QCoreApplication.translate("Center", u"2.0", None))
        self.edit_snap_1.setText(QCoreApplication.translate("Center", u"3", None))
        self.label_56.setText(QCoreApplication.translate("Center", u"Solve Iteration", None))
        self.label_57.setText(QCoreApplication.translate("Center", u"Tolerance", None))
        self.label_59.setText(QCoreApplication.translate("Center", u"Feature snap Iteration", None))
        self.bufferLayerBox_2.setTitle(QCoreApplication.translate("Center", u"< Boundary Layer >", None))
        self.label_63.setText(QCoreApplication.translate("Center", u"First Layer Thickness", None))
        self.edit_boundary_layer_4.setText(QCoreApplication.translate("Center", u"0.1", None))
        self.label_62.setText(QCoreApplication.translate("Center", u"Max. Thickness Ratio", None))
        self.label_60.setText(QCoreApplication.translate("Center", u"Min. Total Thickness", None))
        self.label_61.setText(QCoreApplication.translate("Center", u"Feature Angle Threshold", None))
        self.edit_boundary_layer_2.setText(QCoreApplication.translate("Center", u"0.3", None))
        self.edit_boundary_layer_5.setText(QCoreApplication.translate("Center", u"360", None))
        self.edit_boundary_layer_1.setText(QCoreApplication.translate("Center", u"3", None))
        self.label_65.setText(QCoreApplication.translate("Center", u"Expansion Ratio", None))
        self.edit_boundary_layer_3.setText(QCoreApplication.translate("Center", u"1.3", None))
        self.edit_boundary_layer_6.setText(QCoreApplication.translate("Center", u"0.5", None))
        self.label_64.setText(QCoreApplication.translate("Center", u"Number of Layers", None))
        self.button_edit_hostfile_mesh.setText(QCoreApplication.translate("Center", u"Edit host file", None))
        self.button_mesh_generate.setText(QCoreApplication.translate("Center", u"Mesh generate", None))
        self.title_3.setText(QCoreApplication.translate("Center", u"Models", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("Center", u"< Properties >", None))
        self.label_69.setText(QCoreApplication.translate("Center", u"Phase Change Model", None))
        self.comboBox_7.setItemText(0, QCoreApplication.translate("Center", u"On", None))
        self.comboBox_7.setItemText(1, QCoreApplication.translate("Center", u"Off", None))

        self.label_81.setText(QCoreApplication.translate("Center", u"\u2514 Reaction Model", None))
        self.comboBox_2.setItemText(0, QCoreApplication.translate("Center", u"kEpsilon", None))
        self.comboBox_2.setItemText(1, QCoreApplication.translate("Center", u"kOmega", None))
        self.comboBox_2.setItemText(2, QCoreApplication.translate("Center", u"kOmegaSST ", None))

        self.label_76.setText(QCoreApplication.translate("Center", u"Species", None))
        self.label_75.setText(QCoreApplication.translate("Center", u"Chemical Reaction", None))
        self.comboBox_8.setItemText(0, QCoreApplication.translate("Center", u"MMH+NTO", None))

        self.label_74.setText(QCoreApplication.translate("Center", u"Thermophysical Property", None))
        self.comboBox_6.setItemText(0, QCoreApplication.translate("Center", u"NASA polynomial", None))

        self.comboBox_4.setItemText(0, QCoreApplication.translate("Center", u"On", None))
        self.comboBox_4.setItemText(1, QCoreApplication.translate("Center", u"Off", None))

        self.comboBox_3.setItemText(0, QCoreApplication.translate("Center", u"On", None))
        self.comboBox_3.setItemText(1, QCoreApplication.translate("Center", u"Off", None))

        self.label.setText(QCoreApplication.translate("Center", u"RANS", None))
        self.label_5.setText(QCoreApplication.translate("Center", u"Film", None))
        self.comboBox_10.setItemText(0, QCoreApplication.translate("Center", u"31Reaction", None))
        self.comboBox_10.setItemText(1, QCoreApplication.translate("Center", u"31Reaction+global", None))
        self.comboBox_10.setItemText(2, QCoreApplication.translate("Center", u"51Reaction", None))

        self.title_4.setText(QCoreApplication.translate("Center", u"Initial Conditions", None))
        self.groupBox_12.setTitle(QCoreApplication.translate("Center", u"< Fluid >", None))
        self.edit_fluid_v_x.setText(QCoreApplication.translate("Center", u"0", None))
        self.edit_fluid_v_y.setText(QCoreApplication.translate("Center", u"0", None))
        self.edit_fluid_v_z.setText(QCoreApplication.translate("Center", u"0", None))
        self.label_44.setText(QCoreApplication.translate("Center", u"Temperature [K]", None))
        self.label_45.setText(QCoreApplication.translate("Center", u"Pressure [atm]", None))
        self.edit_fluid_2.setText(QCoreApplication.translate("Center", u"310", None))
        self.edit_fluid_1.setText(QCoreApplication.translate("Center", u"1", None))
        self.label_43.setText(QCoreApplication.translate("Center", u"Velocity [m/s]", None))
        self.groupBox_11.setTitle(QCoreApplication.translate("Center", u"< Solid >", None))
        self.comboBox_9.setItemText(0, QCoreApplication.translate("Center", u"externalWallHeatFluxTemperature", None))
        self.comboBox_9.setItemText(1, QCoreApplication.translate("Center", u"Convective Heat Transfer", None))
        self.comboBox_9.setItemText(2, QCoreApplication.translate("Center", u"wallHeatTransfer", None))

        self.edit_solid_2.setText(QCoreApplication.translate("Center", u"1000", None))
        self.label_9.setText(QCoreApplication.translate("Center", u"Heat coefficient [W/(m^2K)]", None))
        self.edit_solid_1.setText(QCoreApplication.translate("Center", u"300", None))
        self.label_42.setText(QCoreApplication.translate("Center", u"External Type", None))
        self.label_41.setText(QCoreApplication.translate("Center", u"Temperature [K]", None))
        self.sprayMMH.setText(QCoreApplication.translate("Center", u"Spray Property - MMH", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("Center", u"< Operating Condition >", None))
        self.label_18.setText(QCoreApplication.translate("Center", u"SMD [um]", None))
        self.label_11.setText(QCoreApplication.translate("Center", u"Duration [sec]", None))
        self.edit_spray_mmh_3.setText(QCoreApplication.translate("Center", u"26", None))
        self.label_12.setText(QCoreApplication.translate("Center", u"Velocity [m/s]", None))
        self.edit_spray_mmh_4.setText(QCoreApplication.translate("Center", u"5000000", None))
        self.edit_spray_mmh_5.setText(QCoreApplication.translate("Center", u"31", None))
        self.label_6.setText(QCoreApplication.translate("Center", u"Total Mass [kg]", None))
        self.edit_spray_mmh_2.setText(QCoreApplication.translate("Center", u"0.1", None))
        self.edit_spray_mmh_1.setText(QCoreApplication.translate("Center", u"1.32e-4", None))
        self.label_13.setText(QCoreApplication.translate("Center", u"Parcels Per Second", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Center", u"< Geometric Condition >", None))
        self.edit_spray_mmh_13.setText(QCoreApplication.translate("Center", u"0", None))
        self.label_24.setText(QCoreApplication.translate("Center", u"Direction (x,y,z)", None))
        self.label_21.setText(QCoreApplication.translate("Center", u"Position (x,y,z) [m]", None))
        self.label_23.setText(QCoreApplication.translate("Center", u"Outer Diameter [m]", None))
        self.edit_spray_mmh_9.setText(QCoreApplication.translate("Center", u"1", None))
        self.edit_spray_mmh_10.setText(QCoreApplication.translate("Center", u"0", None))
        self.edit_spray_mmh_11.setText(QCoreApplication.translate("Center", u"0", None))
        self.label_22.setText(QCoreApplication.translate("Center", u"Inner Diameter [m]", None))
        self.edit_spray_mmh_6.setText(QCoreApplication.translate("Center", u"0.0001", None))
        self.edit_spray_mmh_7.setText(QCoreApplication.translate("Center", u"0.0", None))
        self.edit_spray_mmh_8.setText(QCoreApplication.translate("Center", u"0.0", None))
        self.edit_spray_mmh_12.setText(QCoreApplication.translate("Center", u"5.8e-4", None))
        self.sprayMMH_2.setText(QCoreApplication.translate("Center", u"Spray Property - NTO", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("Center", u"< Operating Condition >", None))
        self.label_14.setText(QCoreApplication.translate("Center", u"Parcels Per Second", None))
        self.label_7.setText(QCoreApplication.translate("Center", u"Total Mass [kg]", None))
        self.label_20.setText(QCoreApplication.translate("Center", u"SMD [um]", None))
        self.edit_spray_nto_4.setText(QCoreApplication.translate("Center", u"5000000", None))
        self.edit_spray_nto_5.setText(QCoreApplication.translate("Center", u"26", None))
        self.label_16.setText(QCoreApplication.translate("Center", u"Duration [sec]", None))
        self.edit_spray_nto_3.setText(QCoreApplication.translate("Center", u"18", None))
        self.edit_spray_nto_2.setText(QCoreApplication.translate("Center", u"0.1", None))
        self.edit_spray_nto_1.setText(QCoreApplication.translate("Center", u"2.18e-4", None))
        self.label_15.setText(QCoreApplication.translate("Center", u"Velocity [m/s]", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("Center", u"< Geometric Condition >", None))
        self.edit_spray_nto_6.setText(QCoreApplication.translate("Center", u"0.0001", None))
        self.edit_spray_nto_7.setText(QCoreApplication.translate("Center", u"0.0", None))
        self.edit_spray_nto_8.setText(QCoreApplication.translate("Center", u"0.0", None))
        self.label_26.setText(QCoreApplication.translate("Center", u"Position [m]", None))
        self.label_28.setText(QCoreApplication.translate("Center", u"Inner Diameter [m]", None))
        self.label_25.setText(QCoreApplication.translate("Center", u"Direction", None))
        self.edit_spray_nto_13.setText(QCoreApplication.translate("Center", u"9.8e-4", None))
        self.label_27.setText(QCoreApplication.translate("Center", u"Outer Diameter [m]", None))
        self.edit_spray_nto_9.setText(QCoreApplication.translate("Center", u"1", None))
        self.edit_spray_nto_10.setText(QCoreApplication.translate("Center", u"0", None))
        self.edit_spray_nto_11.setText(QCoreApplication.translate("Center", u"0", None))
        self.edit_spray_nto_12.setText(QCoreApplication.translate("Center", u"1.5e-3", None))
        self.label_8.setText(QCoreApplication.translate("Center", u"Numerical Conditions", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("Center", u"< Discretization Schemes >", None))
        self.combo_numerical_3.setItemText(0, QCoreApplication.translate("Center", u"Minmod", None))
        self.combo_numerical_3.setItemText(1, QCoreApplication.translate("Center", u"MinmodV", None))
        self.combo_numerical_3.setItemText(2, QCoreApplication.translate("Center", u"vanLeer", None))

        self.label_29.setText(QCoreApplication.translate("Center", u"Time", None))
        self.combo_numerical_2.setItemText(0, QCoreApplication.translate("Center", u"Minmod", None))
        self.combo_numerical_2.setItemText(1, QCoreApplication.translate("Center", u"MinmodV", None))
        self.combo_numerical_2.setItemText(2, QCoreApplication.translate("Center", u"vanLeer", None))

        self.label_10.setText(QCoreApplication.translate("Center", u"Mass Fraction", None))
        self.label_30.setText(QCoreApplication.translate("Center", u"Momentum", None))
        self.combo_numerical_5.setItemText(0, QCoreApplication.translate("Center", u"Minmod", None))
        self.combo_numerical_5.setItemText(1, QCoreApplication.translate("Center", u"MinmodV", None))
        self.combo_numerical_5.setItemText(2, QCoreApplication.translate("Center", u"vanLeer", None))

        self.combo_numerical_4.setItemText(0, QCoreApplication.translate("Center", u"upwind", None))
        self.combo_numerical_4.setItemText(1, QCoreApplication.translate("Center", u"Minmod", None))

        self.combo_numerical_1.setItemText(0, QCoreApplication.translate("Center", u"Euler", None))
        self.combo_numerical_1.setItemText(1, QCoreApplication.translate("Center", u"Steady", None))

        self.label_32.setText(QCoreApplication.translate("Center", u"Turbulence", None))
        self.label_31.setText(QCoreApplication.translate("Center", u"Energy", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("Center", u"< PIMPLE >", None))
        self.edit_numerical_1.setText(QCoreApplication.translate("Center", u"2", None))
        self.label_34.setText(QCoreApplication.translate("Center", u"nCorrectors", None))
        self.edit_numerical_2.setText(QCoreApplication.translate("Center", u"1", None))
        self.combo_numerical_6.setItemText(0, QCoreApplication.translate("Center", u"Kurganov", None))
        self.combo_numerical_6.setItemText(1, QCoreApplication.translate("Center", u"Tamdor", None))

        self.label_37.setText(QCoreApplication.translate("Center", u"fluxScheme", None))
        self.label_36.setText(QCoreApplication.translate("Center", u"nonOthogonality", None))
        self.label_35.setText(QCoreApplication.translate("Center", u"nOuterCorrectors", None))
        self.edit_numerical_3.setText(QCoreApplication.translate("Center", u"60", None))
        self.title.setText(QCoreApplication.translate("Center", u"Run Conditions", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Center", u"< Properties >", None))
        self.combo_run_1.setItemText(0, QCoreApplication.translate("Center", u"Binary", None))
        self.combo_run_1.setItemText(1, QCoreApplication.translate("Center", u"Ascii", None))

        self.edit_run_3.setText(QCoreApplication.translate("Center", u"1.e-6", None))
        self.edit_run_5.setText(QCoreApplication.translate("Center", u"1000", None))
        self.label_71.setText(QCoreApplication.translate("Center", u"Time Precision\n"
"(Number of Significnat Figures)", None))
        self.edit_run_8.setText(QCoreApplication.translate("Center", u"6", None))
        self.label_77.setText(QCoreApplication.translate("Center", u"Start Time", None))
        self.label_67.setText(QCoreApplication.translate("Center", u"Number of Iterations", None))
        self.edit_run_7.setText(QCoreApplication.translate("Center", u"6", None))
        self.label_78.setText(QCoreApplication.translate("Center", u"End Time", None))
        self.edit_run_2.setText(QCoreApplication.translate("Center", u"0.02", None))
        self.label_72.setText(QCoreApplication.translate("Center", u"Data Write Format", None))
        self.label_79.setText(QCoreApplication.translate("Center", u"Time interval", None))
        self.edit_run_4.setText(QCoreApplication.translate("Center", u"0.4", None))
        self.label_70.setText(QCoreApplication.translate("Center", u"Data Write Precision\n"
"(Number of Significnat Figures)", None))
        self.label_80.setText(QCoreApplication.translate("Center", u"Save interval", None))
        self.edit_run_1.setText(QCoreApplication.translate("Center", u"0", None))
        self.groupBox_13.setTitle(QCoreApplication.translate("Center", u"Retain Only the Most Recent Files", None))
        self.label_68.setText(QCoreApplication.translate("Center", u"Maximum Number of Data Files", None))
        self.title_6.setText(QCoreApplication.translate("Center", u"Run", None))
        self.groupBox.setTitle(QCoreApplication.translate("Center", u"< Process Information >", None))
        self.edit_run_9.setText(QCoreApplication.translate("Center", u"-", None))
        self.edit_run_id.setText(QCoreApplication.translate("Center", u"-", None))
        self.label_2.setText(QCoreApplication.translate("Center", u"ID :", None))
        self.label_4.setText(QCoreApplication.translate("Center", u"Status :", None))
        self.edit_run_10.setText(QCoreApplication.translate("Center", u"Not Running", None))
        self.label_3.setText(QCoreApplication.translate("Center", u"Started : ", None))
        self.button_edit_hostfile_run.setText(QCoreApplication.translate("Center", u"Edit host file", None))
        self.button_run.setText(QCoreApplication.translate("Center", u"Run", None))
        self.button_pause.setText(QCoreApplication.translate("Center", u"Pause", None))
        self.button_stop.setText(QCoreApplication.translate("Center", u"Stop", None))
    # retranslateUi

