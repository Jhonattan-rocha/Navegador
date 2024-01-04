from PySide6.QtCore import (QMetaObject, QSize, QUrl)
from PySide6.QtGui import (QIcon)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QVBoxLayout, QWidget, QSizePolicy)


class LoadPage(QWidget):

    def __init__(self, parent=None, main_page=None, title="SurfEase", html=""):
        super().__init__(parent)
        self.main_page = main_page
        self.title = title
        self.html = html

        self.setupUi(self)

    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        icon = QIcon()
        icon.addFile(u"figs/icon.png", QSize(), QIcon.Normal, QIcon.Off)
        sizePolicyExpanding = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicyExpanding.setHorizontalStretch(0)
        sizePolicyExpanding.setVerticalStretch(0)
        Form.resize(798, 577)
        Form.setWindowTitle(self.title)
        Form.setWindowIcon(icon)
        self.load_page = QWidget(Form)
        self.load_page.implementation = Form
        self.main_container = QVBoxLayout(self.load_page)
        self.main_container.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(sizePolicyExpanding)
        self.main_container.setObjectName(u"main_container")
        self.webEnginePage = QWebEngineView(Form)
        self.webEnginePage.setSizePolicy(sizePolicyExpanding)
        self.webEnginePage.setContentsMargins(0, 0, 0, 0)
        self.webEnginePage.setObjectName(u"webEnginePage")
        # self.webEnginePage.setUrl(QUrl(u"about:blank"))
        self.webEnginePage.load(QUrl.fromLocalFile(self.html))
        self.main_container.addWidget(self.webEnginePage)
        QMetaObject.connectSlotsByName(Form)
