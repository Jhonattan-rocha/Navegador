# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'console.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QLineEdit, QPlainTextEdit,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Console(object):
    def setupUi(self, Console):
        if not Console.objectName():
            Console.setObjectName(u"Console")
        Console.resize(899, 670)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Console.sizePolicy().hasHeightForWidth())
        Console.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(Console)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(Console)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.container_script = QGroupBox(self.groupBox)
        self.container_script.setObjectName(u"container_script")
        sizePolicy.setHeightForWidth(self.container_script.sizePolicy().hasHeightForWidth())
        self.container_script.setSizePolicy(sizePolicy)
        self.container_script.setMinimumSize(QSize(0, 400))
        self.container_script.setStyleSheet(u"QGroupBox {\n"
"	border: 1px solid gray;\n"
"	background-color: white;\n"
"	border-radius: 20px;\n"
"    padding: 10px;\n"
"}")
        self.verticalLayout_4 = QVBoxLayout(self.container_script)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.script = QPlainTextEdit(self.container_script)
        self.script.setObjectName(u"script")
        self.script.setStyleSheet(u"QPlainTextEdit {\n"
"	border: none;\n"
"}")

        self.verticalLayout_4.addWidget(self.script)


        self.verticalLayout_2.addWidget(self.container_script)

        self.container_console = QGroupBox(self.groupBox)
        self.container_console.setObjectName(u"container_console")
        sizePolicy.setHeightForWidth(self.container_console.sizePolicy().hasHeightForWidth())
        self.container_console.setSizePolicy(sizePolicy)
        self.container_console.setMinimumSize(QSize(0, 0))
        self.container_console.setMaximumSize(QSize(16777215, 16777215))
        self.container_console.setStyleSheet(u"QGroupBox {\n"
"	border: 1px solid gray;\n"
"	background-color: white;\n"
"	border-radius: 10px;\n"
"	padding: 20px;\n"
"}")
        self.verticalLayout_3 = QVBoxLayout(self.container_console)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.console_output = QPlainTextEdit(self.container_console)
        self.console_output.setObjectName(u"console_output")
        self.console_output.setStyleSheet(u"QPlainTextEdit {\n"
"	border: none;\n"
"	border-bottom: 1px solid black;\n"
"	border-bottom-right-radius: 10px;\n"
"    border-bottom-left-radius: 10px;\n"
"	padding: 10px;\n"
"}")

        self.verticalLayout_3.addWidget(self.console_output)

        self.console_input = QLineEdit(self.container_console)
        self.console_input.setObjectName(u"console_input")
        sizePolicy.setHeightForWidth(self.console_input.sizePolicy().hasHeightForWidth())
        self.console_input.setSizePolicy(sizePolicy)
        self.console_input.setMinimumSize(QSize(0, 35))
        self.console_input.setMaximumSize(QSize(16777215, 50))
        self.console_input.setStyleSheet(u"QLineEdit {\n"
"	border: 1px solid black;\n"
"	border-radius: 10px;\n"
"	padding-left: 5px;\n"
"    padding-right: 5px;\n"
"}")

        self.verticalLayout_3.addWidget(self.console_input)


        self.verticalLayout_2.addWidget(self.container_console)


        self.verticalLayout.addWidget(self.groupBox)


        self.retranslateUi(Console)

        QMetaObject.connectSlotsByName(Console)
    # setupUi

    def retranslateUi(self, Console):
        Console.setWindowTitle(QCoreApplication.translate("Console", u"Form", None))
        self.groupBox.setTitle("")
        self.container_script.setTitle("")
        self.container_console.setTitle("")
    # retranslateUi

