# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_downloads.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QLayout, QScrollArea,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_download_list(object):
    def setupUi(self, download_list):
        if not download_list.objectName():
            download_list.setObjectName(u"download_list")
        download_list.resize(400, 200)
        download_list.setMinimumSize(QSize(400, 200))
        self.verticalLayout = QVBoxLayout(download_list)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = QScrollArea(download_list)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaDownloadListContents = QWidget()
        self.scrollAreaDownloadListContents.setObjectName(u"scrollAreaDownloadListContents")
        self.scrollAreaDownloadListContents.setGeometry(QRect(0, 0, 380, 180))
        self.container_download_notifications = QVBoxLayout(self.scrollAreaDownloadListContents)
        self.container_download_notifications.setObjectName(u"container_download_notifications")
        self.container_download_notifications.setSizeConstraint(QLayout.SetMinAndMaxSize)
        self.scrollArea.setWidget(self.scrollAreaDownloadListContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.retranslateUi(download_list)

        QMetaObject.connectSlotsByName(download_list)
    # setupUi

    def retranslateUi(self, download_list):
        download_list.setWindowTitle(QCoreApplication.translate("download_list", u"Dialog", None))
    # retranslateUi

