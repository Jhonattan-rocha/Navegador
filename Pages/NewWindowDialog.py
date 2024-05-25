import sys
from PySide6.QtCore import QUrl, QSize
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QSizePolicy, QPushButton


class NewWindowDialog(QDialog):
    def __init__(self, url, parent=None):
        super().__init__(parent)

        sizePolicyExpanding = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicyExpanding.setHorizontalStretch(0)
        sizePolicyExpanding.setVerticalStretch(0)
        self.resize(600, 400)

        layout = QVBoxLayout()

        self.url_edit = QLabel(url)
        self.url_edit.setSizePolicy(sizePolicyExpanding)
        self.url_edit.setMaximumSize(QSize(h=40, w=sys.maxsize))
        layout.addWidget(self.url_edit)

        self.content_view = QWebEngineView()
        self.content_view.load(QUrl(url))
        self.setWindowTitle(self.content_view.title())

        layout.addWidget(self.content_view)

        self.setLayout(layout)
