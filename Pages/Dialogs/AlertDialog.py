from typing import Callable

from PySide6.QtCore import (QMetaObject, QSize)
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QGroupBox, QHBoxLayout,
                               QLabel, QPushButton, QSizePolicy, QVBoxLayout, QWidget)


class Alert(QWidget):

    def __init__(self, parent=None, confirm=False, message: str = '', ok_button: Callable = None,
                 cancel_button: Callable = None):
        super().__init__(parent)
        self.confirm = confirm
        self.ok = ok_button
        self.mes = message
        self.cancel = cancel_button
        self.setupUi(self)

    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(421, 231)
        Dialog.setWindowTitle("Alert")
        iconAlert = QIcon()
        iconAlert.addFile(u"figs/alert.png", QSize(30, 30), QIcon.Normal, QIcon.Off)
        Dialog.setWindowIcon(iconAlert)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.message = QLabel(self.groupBox)
        self.message.setText(self.mes)
        self.message.setObjectName(u"message")
        sizePolicy.setHeightForWidth(self.message.sizePolicy().hasHeightForWidth())
        self.message.setSizePolicy(sizePolicy)

        self.verticalLayout_3.addWidget(self.message)

        self.verticalLayout.addWidget(self.groupBox)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.ok_button = QPushButton(Dialog)
        self.ok_button.setText("OK")
        self.ok_button.setObjectName(u"ok_button")
        self.ok_button.clicked.connect(self.ok)
        self.ok_button.setHidden(self.confirm)

        self.horizontalLayout.addWidget(self.ok_button)

        self.cancel_button = QPushButton(Dialog)
        self.cancel_button.setObjectName(u"cancel_button")
        self.cancel_button.setHidden(self.confirm)
        self.cancel_button.clicked.connect(self.cancel)
        self.cancel_button.setText("Cancelar")
        self.horizontalLayout.addWidget(self.cancel_button)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalLayout_2.addLayout(self.verticalLayout)

        QMetaObject.connectSlotsByName(Dialog)
