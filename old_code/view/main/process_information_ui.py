# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'process_information.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QFrame, QGroupBox,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_ProcessInformation(object):
    def setupUi(self, ProcessInformation):
        if not ProcessInformation.objectName():
            ProcessInformation.setObjectName(u"ProcessInformation")
        ProcessInformation.resize(311, 599)
        self.verticalLayout_2 = QVBoxLayout(ProcessInformation)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.title = QLabel(ProcessInformation)
        self.title.setObjectName(u"title")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.title.setFont(font)

        self.verticalLayout_2.addWidget(self.title)

        self.line = QFrame(ProcessInformation)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        self.groupBox_2 = QGroupBox(ProcessInformation)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(-1, 0, -1, -1)
        self.transientConditions = QWidget(self.groupBox_2)
        self.transientConditions.setObjectName(u"transientConditions")
        self.timeConditionLayout = QFormLayout(self.transientConditions)
        self.timeConditionLayout.setObjectName(u"timeConditionLayout")
        self.timeConditionLayout.setContentsMargins(0, -1, 0, -1)
        self.label_2 = QLabel(self.transientConditions)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setScaledContents(False)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.timeConditionLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.id = QLabel(self.transientConditions)
        self.id.setObjectName(u"id")
        self.id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.timeConditionLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.id)

        self.label_3 = QLabel(self.transientConditions)
        self.label_3.setObjectName(u"label_3")

        self.timeConditionLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_3)

        self.createTime = QLabel(self.transientConditions)
        self.createTime.setObjectName(u"createTime")
        self.createTime.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.timeConditionLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.createTime)

        self.label_4 = QLabel(self.transientConditions)
        self.label_4.setObjectName(u"label_4")

        self.timeConditionLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_4)

        self.status = QLabel(self.transientConditions)
        self.status.setObjectName(u"status")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.timeConditionLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.status)


        self.verticalLayout_5.addWidget(self.transientConditions)


        self.verticalLayout_2.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(ProcessInformation)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout = QVBoxLayout(self.groupBox_3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.startCalculation = QPushButton(self.groupBox_3)
        self.startCalculation.setObjectName(u"startCalculation")
        self.startCalculation.setMinimumSize(QSize(0, 60))

        self.verticalLayout.addWidget(self.startCalculation)

        self.editCalculationSchedule = QPushButton(self.groupBox_3)
        self.editCalculationSchedule.setObjectName(u"editCalculationSchedule")
        self.editCalculationSchedule.setMinimumSize(QSize(0, 60))

        self.verticalLayout.addWidget(self.editCalculationSchedule)

        self.editResultFileFormat = QPushButton(self.groupBox_3)
        self.editResultFileFormat.setObjectName(u"editResultFileFormat")
        self.editResultFileFormat.setEnabled(True)
        self.editResultFileFormat.setMinimumSize(QSize(0, 60))

        self.verticalLayout.addWidget(self.editResultFileFormat)


        self.verticalLayout_2.addWidget(self.groupBox_3)

        self.verticalSpacer = QSpacerItem(20, 229, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.retranslateUi(ProcessInformation)

        QMetaObject.connectSlotsByName(ProcessInformation)
    # setupUi

    def retranslateUi(self, ProcessInformation):
        ProcessInformation.setWindowTitle(QCoreApplication.translate("ProcessInformation", u"Progress Information", None))
        self.title.setText(QCoreApplication.translate("ProcessInformation", u"Process Information", None))
        self.groupBox_2.setTitle("")
        self.label_2.setText(QCoreApplication.translate("ProcessInformation", u"ID :", None))
        self.id.setText(QCoreApplication.translate("ProcessInformation", u"-", None))
        self.label_3.setText(QCoreApplication.translate("ProcessInformation", u"Started : ", None))
        self.createTime.setText(QCoreApplication.translate("ProcessInformation", u"-", None))
        self.label_4.setText(QCoreApplication.translate("ProcessInformation", u"Status :", None))
        self.status.setText(QCoreApplication.translate("ProcessInformation", u"Not Running", None))
        self.groupBox_3.setTitle("")
        self.startCalculation.setText(QCoreApplication.translate("ProcessInformation", u"Start Calculation", None))
        self.editCalculationSchedule.setText(QCoreApplication.translate("ProcessInformation", u"Edit Calculation Schedule", None))
#if QT_CONFIG(tooltip)
        self.editResultFileFormat.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.editResultFileFormat.setText(QCoreApplication.translate("ProcessInformation", u"Edit Result Data File Format", None))
    # retranslateUi

