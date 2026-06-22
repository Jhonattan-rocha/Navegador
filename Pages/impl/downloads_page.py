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

class DownloadImplementation(QWidget):

    def __init__(self, parent=None, main_page=None):
        super().__init__(parent)
        self.identification = str(uuid.uuid4())
        self.ui = DownloadsPage()
        self.ui.setup_ui(self)
        self.ui.arrow_left_back.hide()
        self.main_page = main_page
        self.loaded_items = 0
        self.items_per_load = 10  # Número de itens carregados a cada scroll
        self.load_download_historic(limit=10)
        self.connect_signals()
        
    def connect_signals(self):
        self.ui.scrollAreaDownloads.verticalScrollBar().valueChanged.connect(self.scroll_event)
        self.ui.search_input.textChanged.connect(lambda txt: self.load_download_historic(10, txt))

    def disconnect_signals(self):
        self.ui.scrollAreaDownloads.verticalScrollBar().valueChanged.disconnect()
        self.ui.search_input.textChanged.disconnect()
    
    def load_more_items(self, f: str = ""):
        downloads = recover_download_historic(f=f, order_desc=True,
                                              offset=self.loaded_items, limit=self.items_per_load)
        for download_data in downloads:
            DownloadImplementation.add_download_history(main_page=self, download_data=download_data)
        self.loaded_items += len(downloads)

    def scroll_event(self):
        scrollbar = self.ui.scrollAreaDownloads.verticalScrollBar()
        if scrollbar.value() >= scrollbar.maximum() - 100:  # Verifica se o usuário está próximo do final
            self.load_more_items(f=self.ui.search_input.text())

    def load_download_historic(self, limit: int, f: str = ""):
        layout = self.ui.container_downloads_itens_page.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        QCoreApplication.processEvents()
        self.items_per_load = max(limit, 1)
        history = recover_download_historic(f=f, limit=limit, order_desc=True)
        self.loaded_items = len(history)
        for download in history:
            DownloadImplementation.add_download_history(main_page=self, download_data=download)

    @staticmethod
    def add_download_history(main_page, download_data):
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        download_item = QGroupBox()
        download_item.setObjectName(u"download_item")
        sizePolicy.setHeightForWidth(download_item.sizePolicy().hasHeightForWidth())
        download_item.setSizePolicy(sizePolicy)
        download_item.setMinimumSize(QSize(400, 100))
        download_item.setMaximumSize(QSize(16777215, 100))
        download_item.setStyleSheet(u"QGroupBox {\n"
                                    "	border: 1px solid lightgray;\n"
                                    "	border-radius: 20px;\n"
                                    "	width: 100%;\n"
                                    "}")
        download_item.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        horizontalLayout_4 = QHBoxLayout(download_item)
        horizontalLayout_4.setSpacing(0)
        horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        group_icon = QGroupBox(download_item)
        group_icon.setObjectName(u"group_icon")
        sizePolicy.setHeightForWidth(group_icon.sizePolicy().hasHeightForWidth())
        group_icon.setSizePolicy(sizePolicy)
        group_icon.setMinimumSize(QSize(60, 0))
        group_icon.setMaximumSize(QSize(60, 16777215))
        verticalLayout_5 = QVBoxLayout(group_icon)
        verticalLayout_5.setObjectName(u"verticalLayout_5")
        icon_item = QLabel(group_icon)
        pixmap = QPixmap(u"figs/file.ico")

        # Redimensionar o ícone para um tamanho específico (por exemplo, 64x64 pixels)
        tamanho_desejado = QSize(32, 32)
        pixmap_redimensionado = pixmap.scaled(tamanho_desejado, aspectMode=Qt.KeepAspectRatio)

        icon_item.setPixmap(pixmap_redimensionado)

        icon_item.setObjectName(u"icon_item")
        sizePolicy.setHeightForWidth(icon_item.sizePolicy().hasHeightForWidth())
        icon_item.setSizePolicy(sizePolicy)

        verticalLayout_5.addWidget(icon_item)

        horizontalLayout_4.addWidget(group_icon)

        group_dados = QGroupBox(download_item)
        group_dados.setObjectName(u"group_dados")
        group_dados.setStyleSheet(u"QGroupBox {\n"
                                  "	border: none;\n"
                                  "	margin: 0;\n"
                                  "	padding: 0;\n"
                                  "}")
        verticalLayout_10 = QVBoxLayout(group_dados)
        verticalLayout_10.setObjectName(u"verticalLayout_10")
        verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        groupBox = QGroupBox(group_dados)
        groupBox.setObjectName(u"groupBox")
        sizePolicy.setHeightForWidth(groupBox.sizePolicy().hasHeightForWidth())
        groupBox.setSizePolicy(sizePolicy)
        groupBox.setStyleSheet(u"")
        verticalLayout_11 = QVBoxLayout(groupBox)
        verticalLayout_11.setObjectName(u"verticalLayout_11")
        verticalLayout_11.setContentsMargins(10, 0, 0, 0)
        name_arquivo = QLabel(groupBox)
        data_objeto = datetime.datetime.strptime(str(download_data.download_time), '%Y-%m-%d %H:%M:%S.%f')
        data_formatada = data_objeto.strftime('%d/%m/%Y %H:%M')

        name_arquivo.setText(f"Nome: {download_data.suggested_file_name} Data: f{data_formatada}")
        name_arquivo.setObjectName(u"name_arquivo")
        sizePolicy.setHeightForWidth(name_arquivo.sizePolicy().hasHeightForWidth())
        name_arquivo.setSizePolicy(sizePolicy)

        verticalLayout_11.addWidget(name_arquivo)

        path_arquivo = QLabel(groupBox)
        path_arquivo.setText(f'Path: {download_data.folder_path}')
        path_arquivo.setObjectName(u"path_arquivo")
        sizePolicy.setHeightForWidth(path_arquivo.sizePolicy().hasHeightForWidth())
        path_arquivo.setSizePolicy(sizePolicy)
        path_arquivo.setStyleSheet(u"QLabel {\n"
                                   "	width: '100%';\n"
                                   "}")

        verticalLayout_11.addWidget(path_arquivo)

        status = QLabel(groupBox)
        status.setText(f"Status: {download_data.status}")
        status.setObjectName(u"status")
        sizePolicy.setHeightForWidth(status.sizePolicy().hasHeightForWidth())
        status.setSizePolicy(sizePolicy)

        verticalLayout_11.addWidget(status)

        open_file_path = QCommandLinkButton(groupBox)
        open_file_path.setObjectName(u"open_file_path")
        open_file_path.setText("Abrir no local do arquivo")
        open_file_path.setCursor(QCursor(Qt.PointingHandCursor))
        open_file_path.clicked.connect(lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(download_data.folder_path)))
        sizePolicy.setHeightForWidth(open_file_path.sizePolicy().hasHeightForWidth())
        open_file_path.setSizePolicy(sizePolicy)
        open_file_path.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setBold(True)
        font.setUnderline(True)
        open_file_path.setFont(font)
        icon5 = QIcon()
        icon5.addFile(u"figs/file.ico", QSize(), QIcon.Normal, QIcon.Off)
        open_file_path.setIcon(icon5)

        verticalLayout_11.addWidget(open_file_path)

        verticalLayout_10.addWidget(groupBox)

        horizontalLayout_4.addWidget(group_dados)

        del_item = QPushButton(download_item)
        del_item.setObjectName(u"del_item")
        sizePolicy.setHeightForWidth(del_item.sizePolicy().hasHeightForWidth())
        del_item.setSizePolicy(sizePolicy)
        del_item.setCursor(QCursor(Qt.PointingHandCursor))
        del_item.clicked.connect(lambda: remove_download_historic_item(download_data, True, download_item,
                                                                       main_page.ui.container_downloads_itens_page))
        del_item.setMaximumSize(QSize(40, 40))
        del_item.setStyleSheet(u"QPushButton {\n"
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
        icon5 = QIcon()
        icon5.addFile(u"figs/x.png", QSize(), QIcon.Normal, QIcon.Off)
        del_item.setIcon(icon5)

        horizontalLayout_4.addWidget(del_item)

        main_page.ui.container_downloads_itens_page.addWidget(download_item)

    @staticmethod
    def add_download_notification(main_pages, download_data, show_progress=True) -> QProgressBar:
        if main_pages:
            download_item_list = QGroupBox()
            download_item_list.setObjectName(u"download_item_list")
            sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(download_item_list.sizePolicy().hasHeightForWidth())
            download_item_list.setSizePolicy(sizePolicy)
            download_item_list.setMaximumSize(QSize(16777215, 100))
            verticalLayout_3 = QVBoxLayout(download_item_list)
            verticalLayout_3.setObjectName(u"verticalLayout_3")
            download_name_list = QLabel(download_item_list)
            data_objeto = datetime.datetime.strptime(f'{download_data.download_time}', '%Y-%m-%d %H:%M:%S.%f')
            data_formatada = data_objeto.strftime('%d/%m/%Y %H:%M')
            download_name_list.setText(f"Nome: {download_data.suggested_file_name}\nData: {data_formatada}")
            download_name_list.setObjectName(u"download_name_list")

            verticalLayout_3.addWidget(download_name_list)

            download_path_list = QLabel(download_item_list)
            download_path_list.setText(f"Path: {download_data.folder_path}")
            download_path_list.setObjectName(u"download_path_list")

            verticalLayout_3.addWidget(download_path_list)

            progressBar = QProgressBar(download_item_list)
            progressBar.setObjectName(u"progressBar")
            progressBar.setMaximum(100)
            progressBar.setValue(0)

            if not show_progress:
                progressBar.hide()

            verticalLayout_3.addWidget(progressBar)

            (main_pages.findChild(QLayout, 'container_download_notifications')
             .addWidget(download_item_list))

            return progressBar
