from PySide6.QtCore import (QMetaObject, QSize)
from PySide6.QtGui import QIcon
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QGroupBox, QHBoxLayout,
                               QLineEdit, QPushButton, QSizePolicy, QVBoxLayout, QWidget)

from Pages.ShortCuts import ShortcutManager


class FindInPage(QWidget):

    def __init__(self, parent=None, webView: QWebEngineView = None):
        super().__init__(parent)
        self.setupUi(self)
        self.web = webView
        self.short_cuts = ShortcutManager()

        self.short_cuts.register_shortcut(self, "Esc", lambda: self.close())

    def on_change_text(self, text: str, forward):
        if not forward:
            self.web.page().findText(text, QWebEnginePage.FindFlag.FindBackward)
        else:
            self.web.page().findText(text)

    def closeEvent(self, event):
        self.find_in_page.setText("")
        self.web.clearFocus()
        super().closeEvent(event)

    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(365, 89)
        Dialog.setMaximumSize(QSize(16777215, 16777215))
        Dialog.setWindowTitle("Find")
        iconLupa = QIcon()
        iconLupa.addFile(u"figs/lupa.png", QSize(30, 30), QIcon.Normal, QIcon.Off)
        Dialog.setWindowIcon(iconLupa)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.find_in_page = QLineEdit(self.groupBox)
        self.find_in_page.setObjectName(u"find_in_page")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.find_in_page.sizePolicy().hasHeightForWidth())
        self.find_in_page.setSizePolicy(sizePolicy)
        self.find_in_page.setMinimumSize(QSize(0, 35))
        self.find_in_page.textChanged.connect(lambda txt: self.on_change_text(txt, True))
        self.find_in_page.setMaximumSize(QSize(16777215, 35))
        self.find_in_page.setStyleSheet(u"QLineEdit {\n"
                                        "	border: none;\n"
                                        "	border-radius: 15px;\n"
                                        "	padding-left: 5px;\n"
                                        "	padding-right: 5px;\n"
                                        "}")

        self.horizontalLayout.addWidget(self.find_in_page)
        iconNext = QIcon()
        iconNext.addFile(u"figs/b-arrow.png", QSize(30, 30), QIcon.Normal, QIcon.Off)

        self.next = QPushButton(self.groupBox)
        self.next.setObjectName(u"next")
        self.next.setIcon(iconNext)
        self.next.clicked.connect(lambda: self.on_change_text(self.find_in_page.text(), True))
        self.next.setMaximumSize(QSize(35, 35))
        self.next.setSizePolicy(sizePolicy)
        self.next.setStyleSheet(u"QPushButton {\n"
                                "    border: none;\n"
                                "	border-radius: 15px;\n"
                                "	background-color: none;\n"
                                "	text-align: center;\n"
                                "	color: white;\n"
                                "}\n"
                                "\n"
                                "QPushButton:hover {\n"
                                "	background-color: lightgray;\n"
                                "}")

        self.horizontalLayout.addWidget(self.next)

        iconPrev = QIcon()
        iconPrev.addFile(u"figs/t-arrow.png", QSize(30, 30), QIcon.Normal, QIcon.Off)

        self.previous = QPushButton(self.groupBox)
        self.previous.setObjectName(u"previous")
        self.previous.setSizePolicy(sizePolicy)
        self.previous.setIcon(iconPrev)
        self.previous.clicked.connect(lambda: self.on_change_text(self.find_in_page.text(), False))
        self.previous.setMaximumSize(QSize(35, 35))
        self.previous.setStyleSheet(u"QPushButton {\n"
                                    "    border: none;\n"
                                    "	border-radius: 15px;\n"
                                    "	background-color: none;\n"
                                    "	text-align: center;\n"
                                    "	color: white;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:hover {\n"
                                    "	background-color: lightgray;\n"
                                    "}")

        self.horizontalLayout.addWidget(self.previous)

        iconX = QIcon()
        iconX.addFile(u"figs/x.png", QSize(30, 30), QIcon.Normal, QIcon.Off)

        self.clear_search = QPushButton(self.groupBox)
        self.clear_search.setObjectName(u"clear_search")
        self.clear_search.setIcon(iconX)
        sizePolicy.setHeightForWidth(self.clear_search.sizePolicy().hasHeightForWidth())
        self.clear_search.setSizePolicy(sizePolicy)
        self.clear_search.clicked.connect(lambda: self.find_in_page.setText(""))
        self.clear_search.setMaximumSize(QSize(40, 40))
        self.clear_search.setStyleSheet(u"QPushButton {\n"
                                        "    border: none;\n"
                                        "	border-radius: 15px;\n"
                                        "	background-color: none;\n"
                                        "	text-align: center;\n"
                                        "	color: white;\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton:hover {\n"
                                        "	background-color: lightgray;\n"
                                        "}")

        self.horizontalLayout.addWidget(self.clear_search)

        self.verticalLayout.addWidget(self.groupBox)

        self.verticalLayout_2.addLayout(self.verticalLayout)

        QMetaObject.connectSlotsByName(Dialog)
