# Dividido de Pages/Implementation.py (ver a façade em Pages/Implementation.py).

import datetime
import os.path
import re
import threading
import uuid

from PySide6.QtCore import (QFile, QStringListModel, Slot, QSize, QUrl, Qt, QPoint, QCoreApplication)
from PySide6.QtGui import (QCursor, QDesktopServices, QPainter, QRegion, QPageSize, QPageRanges, 
                           QFont, QIcon, QPixmap, QTextCursor, QAction, QPageLayout)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWebEngineCore import QWebEngineDownloadRequest, QWebEnginePage, QWebEngineNewWindowRequest
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QDialog, QCompleter, QMenu, QFileDialog, QGroupBox, QHBoxLayout, QCommandLinkButton,
                               QSizePolicy, QLayout, QProgressBar, QLabel, QWidget, QPushButton, QVBoxLayout, QMessageBox)
from PySide6.QtWebEngineCore import QWebEngineCertificateError
from PySide6.QtPrintSupport import QPrinter, QPrintPreviewDialog

from bs4 import BeautifulSoup
from colorama import init
from uuid import uuid4
from DataOperations.register_recover import recover_download_historic, recover_historic, \
    remove_download_historic_item, register_console_historic, update_historic, update_download_status
from DataOperations.register_recover import register_download_historic, register_historic, remove_historic_item
from Pages.Dialogs.ConsolePage import ConsolePage
from Pages.DefaultSearchPage import DefaultSearchPage
from Pages.Download import DownloadsPage
from Pages.Dialogs.FindInPage import FindInPage
from Pages.Historico import HistoricoPage
from Pages.ShortCuts import ShortcutManager
from configs.Config import settings_app
from Pages.Dialogs.NewWindowDialog import NewWindowDialog

init(autoreset=True)

class HistoricoImplementation(QWidget):

    def __init__(self, parent=None, main_page=None):
        super().__init__(parent)
        self.identification = str(uuid.uuid4())
        self.ui = HistoricoPage()
        self.ui.setup_ui(self)
        self.ui.arrow_left_back_historic.hide()
        self.main_page = main_page
        self.loaded_items = 0
        self.items_per_load = 10  # Número de itens carregados a cada scroll
        self.load_historic(10)
        self.connect_signals()

    def connect_signals(self):
        self.ui.scrollAreaHistoric.verticalScrollBar().valueChanged.connect(self.scroll_event)
        self.ui.search_input.textChanged.connect(lambda txt: self.load_historic(10, txt))

    def disconnect_signals(self):
        self.ui.scrollAreaHistoric.verticalScrollBar().valueChanged.disconnect()
        self.ui.search_input.textChanged.disconnect()
    
    def load_more_items(self, f: str = ""):
        # Paginação por OFFSET no banco (antes buscava tudo e fatiava, e o
        # load_historic reiniciava loaded_items=0, recarregando os 10 primeiros).
        history = recover_historic(f=f, order_desc=True,
                                   offset=self.loaded_items, limit=self.items_per_load)
        for his in history:
            self.add_historic_item(historic_data=his)
        self.loaded_items += len(history)

    def scroll_event(self):
        scrollbar = self.ui.scrollAreaHistoric.verticalScrollBar()
        if scrollbar.value() >= scrollbar.maximum() - 100:  # Verifica se o usuário está próximo do final
            self.load_more_items(f=self.ui.search_input.text())

    def load_historic(self, limit: int, f: str = ''):
        layout = self.ui.container_historic_page.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        QCoreApplication.processEvents()
        self.items_per_load = max(limit, 1)
        history = recover_historic(f=f, order_desc=True, limit=limit)
        self.loaded_items = len(history)
        for his in history:
            self.add_historic_item(historic_data=his)


    def open_historic_site(self, site):
        from Pages.impl.search_page import DefaultSearchPageImplementation
        default_page = DefaultSearchPageImplementation(self.main_page.ui.tabs, main_page=self.main_page).ui.page
        self.main_page.ui.tabs.addTab(default_page, "Nova pagina")
        last_page = self.main_page.ui.tabs.count() - 1
        layout = self.main_page.ui.tabs.widget(last_page)
        webview = layout.findChildren(QWebEngineView)
        if webview:
            webview[0].load(site)

    def add_historic_item(self, historic_data):
        if self.main_page:
            historic_item = QGroupBox()
            historic_item.setObjectName(u"historic_item")
            sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(historic_item.sizePolicy().hasHeightForWidth())
            font = QFont()
            font.setFamilies([u"Segoe UI"])
            font.setBold(True)
            font.setUnderline(True)
            icon5 = QIcon()
            icon5.addFile(u"figs/site.png", QSize(), QIcon.Normal, QIcon.Off)
            icon6 = QIcon()
            icon6.addFile(u"figs/x.png", QSize(), QIcon.Normal, QIcon.Off)
            historic_item.setSizePolicy(sizePolicy)
            historic_item.setMinimumSize(QSize(400, 50))
            historic_item.setMaximumSize(QSize(16777215, 60))
            historic_item.setStyleSheet(u"QGroupBox {\n"
                                        "	border: 1px solid lightgray;\n"
                                        "	border-radius: 20px;\n"
                                        "	width: 100%;\n"
                                        "}")
            historic_item.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
            horizontalLayout_7 = QHBoxLayout(historic_item)
            horizontalLayout_7.setSpacing(0)
            horizontalLayout_7.setObjectName(u"horizontalLayout_7")
            horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
            group_dados_historic_site = QGroupBox(historic_item)
            group_dados_historic_site.setObjectName(u"group_dados_historic_site")
            group_dados_historic_site.setStyleSheet(u"QGroupBox {\n"
                                                    "	border: none;\n"
                                                    "	margin: 0;\n"
                                                    "	padding: 0;\n"
                                                    "}")
            verticalLayout_12 = QVBoxLayout(group_dados_historic_site)
            verticalLayout_12.setObjectName(u"verticalLayout_12")
            verticalLayout_12.setContentsMargins(0, 0, 0, 0)
            groupBox_2 = QGroupBox(group_dados_historic_site)
            groupBox_2.setObjectName(u"groupBox_2")
            sizePolicy.setHeightForWidth(groupBox_2.sizePolicy().hasHeightForWidth())
            groupBox_2.setSizePolicy(sizePolicy)
            groupBox_2.setStyleSheet(u"")
            verticalLayout_13 = QVBoxLayout(groupBox_2)
            verticalLayout_13.setObjectName(u"verticalLayout_13")
            verticalLayout_13.setContentsMargins(10, 0, 0, 0)
            open_site = QCommandLinkButton(groupBox_2)
            open_site.setText(f"Site: {historic_data.site}\nData: {datetime.datetime.strptime(str(historic_data.download_time), '%Y-%m-%d %H:%M:%S.%f')}")
            open_site.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            open_site.setObjectName(u"open_site")
            sizePolicy.setHeightForWidth(open_site.sizePolicy().hasHeightForWidth())
            open_site.setSizePolicy(sizePolicy)
            open_site.clicked.connect(lambda: self.open_historic_site(historic_data.site))
            open_site.setMaximumSize(QSize(16777215, 16777215))
            open_site.setFont(font)
            open_site.setIcon(icon5)

            verticalLayout_13.addWidget(open_site)

            verticalLayout_12.addWidget(groupBox_2)

            horizontalLayout_7.addWidget(group_dados_historic_site)

            del_item_historic = QPushButton(historic_item)
            del_item_historic.setObjectName(u"del_item_historic")
            sizePolicy.setHeightForWidth(del_item_historic.sizePolicy().hasHeightForWidth())
            del_item_historic.setSizePolicy(sizePolicy)
            del_item_historic.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            del_item_historic.clicked.connect(
                lambda: remove_historic_item(id=historic_data.id,
                                             remove_view=True, widget=historic_item,
                                             layout=self.ui.container_historic_page))
            del_item_historic.setMaximumSize(QSize(40, 40))
            del_item_historic.setMinimumSize(QSize(40, 40))
            del_item_historic.setStyleSheet(u"QPushButton {\n"
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
            del_item_historic.setIcon(icon6)

            horizontalLayout_7.addWidget(del_item_historic)

            self.ui.container_historic_page.addWidget(historic_item)
