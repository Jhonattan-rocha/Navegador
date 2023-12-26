import datetime
import os.path
import re
import threading

from PySide6.QtCore import (QFile)
from PySide6.QtCore import (QSize, QUrl, Qt)
from PySide6.QtGui import (QCursor, QDesktopServices,
                           QFont, QIcon, QPixmap)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QDialog)
from PySide6.QtWidgets import (QFileDialog)
from PySide6.QtWidgets import (QGroupBox, QHBoxLayout, QCommandLinkButton,
                               QSizePolicy, QLayout, QProgressBar)
from PySide6.QtWidgets import (QLabel)
from PySide6.QtWidgets import (QPushButton,
                               QVBoxLayout)
from PySide6.QtWidgets import (QTabWidget, QLineEdit, QWidget)

from DataOperations.register_recover import recover_download_historic, recover_historic, \
    recover_adjacent_historic, remove_download_historic_item
from DataOperations.register_recover import register_download_historic, register_historic, remove_historic_item
from DownloaderManager import Downloader
from Pages.DefaultSearchPage import DefaultSearchPage
from Pages.Download import DownloadsPage
from Pages.Historic import HistoricPage


class Default(QWidget):

    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.ui = DefaultSearchPage()
        self.ui.setup_ui(self)
        self.main_window = main_window
        self.site_atual: dict = {}
        self.ui.arrow_left_historic.clicked.connect(
            lambda: Historic.load_direction_specific_historic(self, self.site_atual['name'],
                                                              self.site_atual['date_time'],
                                                              'ant'))
        self.ui.arrow_right_historic.clicked.connect(
            lambda: Historic.load_direction_specific_historic(self, self.site_atual['name'],
                                                              self.site_atual['date_time'],
                                                              'prox'))
        self.ui.url.returnPressed.connect(
            lambda web=self.ui.webEngineView, search=self.ui.url: self.search(web_loader=web,
                                                                              search_text=search.text()))
        self.ui.webEngineView.page().profile().downloadRequested.connect(self.download_file)

        self.ui.webEngineView.urlChanged.connect(
            lambda site, url_input=self.ui.url: self.update_url(url_input, site))
        self.ui.webEngineView.titleChanged.connect(
            lambda title, index=self.main_window.ui.tabs.indexOf(self.ui.page),
                   tabs=self.main_window.ui.tabs: self.update_title(title, index, tabs))
        self.ui.options.clicked.connect(lambda: self.open_dialog_ops(main_window=main_window))
        self.ui.download_buttton.clicked.connect(
            lambda: Download.open_dialog_download(main_window=main_window))

    @staticmethod
    def open_dialog_ops(main_window, view=True):
        if not main_window.dialog_ops:
            main_window.ui.tabs.setTabsClosable(True)
            loader = QUiLoader()
            ui_file = QFile(os.path.abspath(os.path.join("Pages", "dialog_ops.ui")))
            ui_file.open(QFile.ReadOnly)
            dialog_widget = loader.load(ui_file)
            ui_file.close()

            add_page = dialog_widget.findChild(QPushButton, 'add_page')
            add_page.clicked.connect(
                lambda: main_window.ui.tabs.addTab(Default(main_window, main_window).ui.page, "Nova Página"))

            download_page = dialog_widget.findChild(QPushButton, 'donwloads_page')
            download_page.clicked.connect(
                lambda: main_window.ui.tabs.addTab(Download(main_window).ui.downloads, "Downloads"))

            historic_page = dialog_widget.findChild(QPushButton, 'historic_page')
            historic_page.clicked.connect(
                lambda: main_window.ui.tabs.addTab(Historic(main_window, main_window).ui.historic, "Histórico"))

            # Criar o diálogo
            dialog = QDialog(main_window)
            dialog.setWindowTitle("Opções")
            dialog.setModal(True)  # Permitir interação com a janela principal
            layout = QVBoxLayout(dialog)
            layout.addWidget(dialog_widget)

            # Exibir o diálogo modalmente
            main_window.dialog_ops = {"fields": dialog_widget, "view": dialog}
            if view:
                dialog.exec()
        else:
            main_window.ui.tabs.setTabsClosable(True)
            main_window.dialog_ops['view'].exec()

    def update_url(self, url_input: QLineEdit, url: QUrl) -> None:
        data = datetime.datetime.now()
        self.site_atual = {"name": url.toString(), "cookies": [], "date_time": f"{data}"}
        register_historic(url.toString(), [], data)
        url_input.setText(url.toString())
        url_input.setCursorPosition(0)

    def limit_string(self, text: str, limit: int) -> str:
        if len(text) > limit:
            return text[:limit - 3] + "..."  # Corta o texto e adiciona "..." no final
        return text

    def update_title(self, text: str, index: int, tabs: QTabWidget) -> None:
        tabs.setTabText(index, self.limit_string(text, 30))

    @staticmethod
    def is_valid_url(url_string: str) -> bool:
        url_pattern = re.compile(
            r'^(https?://)?' +  # validar protocolo
            r'((([a-z\d]([a-z\d-]*[a-z\d])*)\.)+[a-z]{2,}|' +  # validar nome de domínio
            r'((\d{1,3}\.){3}\d{1,3}))' +  # validar OU endereço IP (v4)
            r'(:\d+)?(/[-a-z\d%_.~+]*)*' +  # validar porta e caminho
            r'(\?[;&a-z\d%_.~+=-]*)?' +  # validar string de consulta
            r'(#[-a-z\d_]*)?$',  # validar fragmento
            re.IGNORECASE  # ignora case sensitivity
        )
        return bool(re.match(url_pattern, url_string))

    def search(self, web_loader: QWebEngineView, search_text: str) -> None:
        if self.is_valid_url(search_text):
            url = f"{search_text}"

            if 'https://' not in search_text:
                url = f"https://{search_text}"

            web_loader.load(QUrl(url))
            return
        search_url = "https://www.google.com/search?q=" + search_text.replace(" ", "+")

        web_loader.load(QUrl(search_url))

    def download_file(self, download_item) -> None:
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        folder_path = QFileDialog.getExistingDirectory(self, "Selecionar pasta de destino", options=options)
        suggested_file_name = download_item.suggestedFileName()

        downloader = Downloader.Downloader(self)
        downloader.download_finished.connect(self.handle_download_finished,
                                             Qt.ConnectionType.QueuedConnection)
        downloader.download_failed.connect(self.handle_download_failed,
                                           Qt.ConnectionType.QueuedConnection)
        progress_bar = Download.add_download_notification(main_windows=self.main_window.dialog_download,
                                                          download_data={'download_time': datetime.datetime.now(),
                                                                         'name': suggested_file_name,
                                                                         'path': os.path.join(folder_path,
                                                                                              suggested_file_name)})
        downloader.progress_update.connect(lambda percent: self.handle_progress(percent, progress_bar),
                                           Qt.ConnectionType.QueuedConnection)

        threading.Thread(target=register_download_historic,
                         args=(suggested_file_name, folder_path, 'Baixando',
                               f'{datetime.datetime.now()}', 'download_notifications.json')).start()
        downloader.download_file(download_item.url().toString(), folder_path, suggested_file_name, progress_bar)

    def handle_progress(self, percent: float, progress_bar):
        progress_bar.setValue(percent)

    def handle_download_finished(self, suggested_file_name, folder_path):
        threading.Thread(target=register_download_historic,
                         args=(suggested_file_name, folder_path, 'Concluido',
                               f'{datetime.datetime.now()}')).start()

    def handle_download_failed(self, suggested_file_name, folder_path):
        threading.Thread(target=register_download_historic,
                         args=(suggested_file_name, folder_path, 'Erro', f'{datetime.datetime.now()}')).start()


class Download(QWidget):

    def __init__(self, parent=None, main_page=None):
        super().__init__(parent)
        self.ui = DownloadsPage()
        self.ui.setup_ui(self)
        self.ui.arrow_left_back.hide()
        self.main_page = main_page
        self.load_download_historic(self)

    @staticmethod
    def open_dialog_download(main_window, view=True):
        if not main_window.dialog_download:
            loader = QUiLoader()
            ui_file = QFile(os.path.abspath(os.path.join("Pages", "dialog_downloads.ui")))
            ui_file.open(QFile.ReadOnly)
            dialog_widget = loader.load(ui_file)
            ui_file.close()

            # Criar o diálogo
            dialog = QDialog(main_window)
            dialog.setWindowTitle("Downloads")
            dialog.setModal(True)  # Permitir interação com a janela principal
            layout = QVBoxLayout(dialog)
            layout.addWidget(dialog_widget)

            # Exibir o diálogo modalmente
            main_window.dialog_download = {"fields": dialog_widget, "view": dialog}
            Download.load_download_notificatios(main_window.dialog_download)

            if view:
                dialog.exec()
        else:
            main_window.dialog_download['view'].exec()

    @staticmethod
    def load_download_historic(main_window):
        layout = main_window.ui.container_downloads_itens_page.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        history = recover_download_historic()

        if bool(history):
            for download in history['Files']:
                Download.add_download_history(main_window=main_window, download_data=download)

    @staticmethod
    def load_download_notificatios(main_window):
        layout = main_window['fields'].findChild(QLayout, 'container_download_notifications')
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                layout.removeWidget(child.widget())
                child.widget().deleteLater()
                layout.update()

        history = recover_download_historic(file_saved='download_notifications.json')
        if bool(history):
            for download in history['Files']:
                Download.add_download_notification(main_windows=main_window, download_data=download,
                                                   show_progress=False)

    @staticmethod
    def add_download_history(main_window, download_data):
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
        data_objeto = datetime.datetime.strptime(download_data['download_time'], '%Y-%m-%d %H:%M:%S.%f')
        data_formatada = data_objeto.strftime('%d/%m/%Y %H:%M')

        name_arquivo.setText(f"Nome: {download_data['name']} Data: f{data_formatada}")
        name_arquivo.setObjectName(u"name_arquivo")
        sizePolicy.setHeightForWidth(name_arquivo.sizePolicy().hasHeightForWidth())
        name_arquivo.setSizePolicy(sizePolicy)

        verticalLayout_11.addWidget(name_arquivo)

        path_arquivo = QLabel(groupBox)
        path_arquivo.setText(f'Path: {download_data["path"]}')
        path_arquivo.setObjectName(u"path_arquivo")
        sizePolicy.setHeightForWidth(path_arquivo.sizePolicy().hasHeightForWidth())
        path_arquivo.setSizePolicy(sizePolicy)
        path_arquivo.setStyleSheet(u"QLabel {\n"
                                   "	width: '100%';\n"
                                   "}")

        verticalLayout_11.addWidget(path_arquivo)

        status = QLabel(groupBox)
        status.setText(f"Status: {download_data['status']}")
        status.setObjectName(u"status")
        sizePolicy.setHeightForWidth(status.sizePolicy().hasHeightForWidth())
        status.setSizePolicy(sizePolicy)

        verticalLayout_11.addWidget(status)

        open_file_path = QCommandLinkButton(groupBox)
        open_file_path.setObjectName(u"open_file_path")
        open_file_path.setText("Abrir no local do arquivo")
        open_file_path.setCursor(QCursor(Qt.PointingHandCursor))
        open_file_path.clicked.connect(lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(download_data['path'])))
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
                                                                       main_window.ui.container_downloads_itens_page))
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
                               "	transition: 1s;\n"
                               "	transition-delay: 1s;\n"
                               "	background-color: lightgray;\n"
                               "}")
        icon5 = QIcon()
        icon5.addFile(u"figs/x.png", QSize(), QIcon.Normal, QIcon.Off)
        del_item.setIcon(icon5)

        horizontalLayout_4.addWidget(del_item)

        main_window.ui.container_downloads_itens_page.insertWidget(0, download_item)

    @staticmethod
    def add_download_notification(main_windows, download_data, show_progress=True) -> QProgressBar:
        if main_windows:
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
            data_objeto = datetime.datetime.strptime(f'{download_data["download_time"]}', '%Y-%m-%d %H:%M:%S.%f')
            data_formatada = data_objeto.strftime('%d/%m/%Y %H:%M')
            download_name_list.setText(f"Nome: {download_data['name']}\nData: {data_formatada}")
            download_name_list.setObjectName(u"download_name_list")

            verticalLayout_3.addWidget(download_name_list)

            download_path_list = QLabel(download_item_list)
            download_path_list.setText(f"Path: {download_data['path']}")
            download_path_list.setObjectName(u"download_path_list")

            verticalLayout_3.addWidget(download_path_list)

            progressBar = QProgressBar(download_item_list)
            progressBar.setObjectName(u"progressBar")
            progressBar.setMaximum(100)
            progressBar.setValue(0)

            if not show_progress:
                progressBar.hide()

            verticalLayout_3.addWidget(progressBar)

            (main_windows['fields'].findChild(QLayout, 'container_download_notifications')
             .insertWidget(0, download_item_list))

            return progressBar


class Historic(QWidget):

    def __init__(self, parent=None, main_page=None):
        super().__init__(parent)
        self.ui = HistoricPage()
        self.ui.setup_ui(self)
        self.ui.arrow_left_back_historic.hide()
        self.main_page = main_page
        self.load_historic(self.main_page, self)

    @staticmethod
    def load_historic(main_window, historic_window):
        layout = historic_window.ui.container_historic_page.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        history = recover_historic()

        if bool(history):
            for site in history['Sites']:
                Historic.add_historic_item(main_window=main_window, historic_data=site, historic_page=historic_window)

    @staticmethod
    def load_direction_specific_historic(main_window, site: str, date_time: str, direc: str):
        tab = main_window.ui.tabs.currentWidget()
        site_procurado = recover_adjacent_historic(site, date_time, direc)
        if bool(site_procurado):
            webview = tab.findChildren(QWebEngineView)
            print(webview)
            if webview:
                webview[0].load(site_procurado)

    @staticmethod
    def open_historic_site(main_window, site):
        default_page = Default(main_window, main_window).ui.page
        main_window.ui.tabs.addTab(default_page, "Nova pagina")
        last_page = main_window.ui.tabs.count() - 1
        layout = main_window.ui.tabs.widget(last_page)
        webview = layout.findChildren(QWebEngineView)
        if webview:
            webview[0].load(site)

    @staticmethod
    def add_historic_item(main_window, historic_page, historic_data):
        if main_window:
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
            open_site.setText(f"Site: {historic_data['name']}\nData: {historic_data['date_time']}")
            open_site.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            open_site.setObjectName(u"open_site")
            sizePolicy.setHeightForWidth(open_site.sizePolicy().hasHeightForWidth())
            open_site.setSizePolicy(sizePolicy)
            open_site.clicked.connect(lambda: Historic.open_historic_site(main_window, historic_data['name']))
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
                lambda: remove_historic_item(site=historic_data['name'], date_time=historic_data['date_time'],
                                             remove_view=True, widget=historic_item,
                                             layout=main_window.ui.container_historic_page))
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
                                            "	transition: 1s;\n"
                                            "	transition-delay: 1s;\n"
                                            "	background-color: lightgray;\n"
                                            "}")
            del_item_historic.setIcon(icon6)

            horizontalLayout_7.addWidget(del_item_historic)

            historic_page.ui.container_historic_page.insertWidget(0, historic_item)
