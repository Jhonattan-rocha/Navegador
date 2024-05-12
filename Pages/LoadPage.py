from PySide6.QtCore import (QMetaObject, QSize, QUrl)
from PySide6.QtGui import (QIcon)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWidgets import (QVBoxLayout, QWidget, QSizePolicy)

from CustomElements.CustomProfile import CustomWebEngineProfile


class LoadPage(QWidget):

    def __init__(self, parent=None, main_page=None, title="SurfEase", html="", cache_path=""):
        super().__init__(parent)
        self.main_page = main_page
        self.title = title
        self.html = html
        self.cache_path = cache_path

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
        self.container = QVBoxLayout(Form)
        self.container.setObjectName(u"container")
        self.container.setContentsMargins(0, 0, 0, 0)
        self.container.setSizeConstraint(QVBoxLayout.SizeConstraint.SetDefaultConstraint)
        self.load_page = QWidget(Form)
        self.load_page.implementation = Form
        self.main_container = QVBoxLayout(self.load_page)
        self.main_container.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(sizePolicyExpanding)
        self.main_container.setObjectName(u"main_container")
        self.profile_load_page = CustomWebEngineProfile("profile_web", parent=self, cache_path=self.cache_path)
        self.page_web_for_load = QWebEnginePage(self.profile_load_page, self)
        self.page_web_for_load.setObjectName("page_web_for_load")
        self.webEngineView = QWebEngineView(self.page_web_for_load)
        self.webEngineView.setSizePolicy(sizePolicyExpanding)
        self.webEngineView.setContentsMargins(0, 0, 0, 0)
        self.webEngineView.setObjectName(u"webEngineView")
        self.webEngineView.load(QUrl(self.html))
        self.main_container.addWidget(self.webEngineView)
        self.container.addWidget(self.load_page)
        QMetaObject.connectSlotsByName(Form)
