# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_ops.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_dialog(object):
    def setupUi(self, dialog):
        if not dialog.objectName():
            dialog.setObjectName(u"dialog")
        dialog.resize(286, 238)
        self.verticalLayout_2 = QVBoxLayout(dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.add_page = QPushButton(dialog)
        self.add_page.setObjectName(u"add_page")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_page.sizePolicy().hasHeightForWidth())
        self.add_page.setSizePolicy(sizePolicy)
        self.add_page.setMaximumSize(QSize(16777215, 40))

        self.verticalLayout.addWidget(self.add_page)

        self.donwloads_page = QPushButton(dialog)
        self.donwloads_page.setObjectName(u"donwloads_page")
        sizePolicy.setHeightForWidth(self.donwloads_page.sizePolicy().hasHeightForWidth())
        self.donwloads_page.setSizePolicy(sizePolicy)
        self.donwloads_page.setMaximumSize(QSize(16777215, 40))

        self.verticalLayout.addWidget(self.donwloads_page)

        self.historic_page = QPushButton(dialog)
        self.historic_page.setObjectName(u"historic_page")
        sizePolicy.setHeightForWidth(self.historic_page.sizePolicy().hasHeightForWidth())
        self.historic_page.setSizePolicy(sizePolicy)
        self.historic_page.setMaximumSize(QSize(16777215, 40))

        self.verticalLayout.addWidget(self.historic_page)

        self.findpage = QPushButton(dialog)
        self.findpage.setObjectName(u"findpage")
        sizePolicy.setHeightForWidth(self.findpage.sizePolicy().hasHeightForWidth())
        self.findpage.setSizePolicy(sizePolicy)
        self.findpage.setMaximumSize(QSize(16777215, 40))

        self.verticalLayout.addWidget(self.findpage)

        self.configs = QPushButton(dialog)
        self.configs.setObjectName(u"configs")
        sizePolicy.setHeightForWidth(self.configs.sizePolicy().hasHeightForWidth())
        self.configs.setSizePolicy(sizePolicy)
        self.configs.setMaximumSize(QSize(16777215, 40))

        self.verticalLayout.addWidget(self.configs)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(dialog)

        QMetaObject.connectSlotsByName(dialog)
    # setupUi

    def retranslateUi(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog", u"Op\u00e7\u00f5es", None))
        self.add_page.setText(QCoreApplication.translate("dialog", u"Add New Page", None))
        self.donwloads_page.setText(QCoreApplication.translate("dialog", u"Donwloads", None))
        self.historic_page.setText(QCoreApplication.translate("dialog", u"historic", None))
        self.findpage.setText(QCoreApplication.translate("dialog", u"Buscar na p\u00e1gina", None))
        self.configs.setText(QCoreApplication.translate("dialog", u"Configura\u00e7\u00f5es", None))
    # retranslateUi

