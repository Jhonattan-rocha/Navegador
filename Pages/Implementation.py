import datetime
import os.path
import re
import threading
import uuid

from PySide6.QtCore import (QFile, QStringListModel, Slot, QSize, QUrl, Qt, QPoint, QTimer)
from PySide6.QtGui import (QCursor, QDesktopServices, QPainter, QRegion, QPageSize, QPageRanges, 
                           QFont, QIcon, QPixmap, QTextCursor, QAction, QPageLayout)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWebEngineCore import QWebEngineDownloadRequest, QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QDialog, QCompleter, QMenu, QFileDialog, QGroupBox, QHBoxLayout, QCommandLinkButton,
                               QSizePolicy, QLayout, QProgressBar, QLabel, QWidget, QPushButton, QVBoxLayout, QLabel)
from PySide6.QtWebEngineCore import QWebEngineCertificateError
from PySide6.QtPrintSupport import QPrinter, QPrintPreviewDialog

from bs4 import BeautifulSoup
from colorama import init
from uuid import uuid4
from DataOperations.TRIEManager import Trie
from DataOperations.register_recover import recover_download_historic, recover_historic, \
    remove_download_historic_item, register_console_historic
from DataOperations.register_recover import register_download_historic, register_historic, remove_historic_item
from DownloaderManager import Downloader
from Pages.ConsolePage import ConsolePage
from Pages.DefaultSearchPage import DefaultSearchPage
from Pages.Download import DownloadsPage
from Pages.FindInPage import FindInPage
from Pages.Historico import HistoricoPage
from Pages.LoadPage import LoadPage

init(autoreset=True)

class DefaultSearchPageImplementation(QWidget):
    downloads = []

    def __init__(self, parent=None, main_page=None):
        super().__init__(parent)
        self.trie = None
        self.identification = str(uuid.uuid4())
        self.ui = DefaultSearchPage()
        self.ui.setup_ui(self)
        self.main_page = main_page
        self.ui.webEngineView.contextMenuEvent = self.handle_context_menu
        if not self.main_page.dialog_download or not self.main_page.dialog_ops:
            self.open_dialog_ops(view=False)
            self.open_dialog_download(view=False)
        self.site_atual: dict = {}
        self.sites_visitados: list = []
        self.connect_signals()
            
    def print_page(self):
        if self.ui.label_movie.isHidden():
            filename = str(uuid4())
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setPageSize(QPageSize.PageSizeId.A4)
            printer.setCopyCount(1)
            printer.setPrintRange(QPrinter.PrintRange.AllPages)
            printer.setPaperSource(QPrinter.PaperSource.MaxPageSource)
            printer.setPageOrientation(QPageLayout.Orientation.Portrait)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setDocName(f"temp_{filename}.pdf")
            printer.setFullPage(True)
            printer.setOutputFileName(os.path.join(".", "cache_aux", f"temp_{filename}.pdf"))
            printer.setFontEmbeddingEnabled(True)
            printer.setResolution(max(printer.supportedResolutions()))

            painter = QPainter(printer)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            rg = QRegion()
            self.ui.webEngineView.render(painter, QPoint(), rg)
            painter.end()

    def handle_context_menu(self, event):
        # Obtendo o menu de contexto padrão
        default_menu = self.ui.webEngineView.createStandardContextMenu()

        # Criando uma ação personalizada
        custom_action = default_menu.addAction("Print page...")
        custom_action.triggered.connect(lambda args: self.print_page())

        # Exibindo o menu de contexto modificado
        default_menu.exec_(event.globalPos())
    
    def showContextMenu(self, pos):
        menu = QMenu(self)

        history = self.ui.webEngineView.history()
        for i in range(min(history.count(), 10)):  # Obter os últimos 10 itens do histórico
            action = QAction(history.itemAt(i).title(), self)
            action.setData(history.itemAt(i).url())  # Armazenar a URL como dados da ação
            action.triggered.connect(lambda event: self.search(self.ui.webEngineView, history.itemAt(i).url().toString()))
            menu.addAction(action)
            
        menu.exec_(self.ui.arrow_left_historic.mapToGlobal(pos))

    def closeEvent(self, event):
        super().closeEvent(event)

    def connect_signals(self):
        self.ui.arrow_left_historic.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.arrow_right_historic.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.arrow_left_historic.customContextMenuRequested.connect(self.showContextMenu)
        self.ui.arrow_right_historic.customContextMenuRequested.connect(self.showContextMenu)
        self.ui.page_web.profile().downloadRequested.connect(self.download_file)
        self.ui.page_web.certificateError.connect(self.handle_certificate_error)
        self.ui.arrow_left_historic.clicked.connect(
            lambda: self.load_direction_specific_historic('ant'))
        self.ui.arrow_right_historic.clicked.connect(
            lambda: self.load_direction_specific_historic('prox'))
        self.ui.url.returnPressed.connect(
            lambda: self.search(web_loader=self.ui.webEngineView,
                                search_text=self.ui.url.text()))

        self.ui.webEngineView.urlChanged.connect(self.update_url)
        self.ui.webEngineView.urlChanged.connect(self.update_title)

        self.ui.webEngineView.loadStarted.connect(
            lambda: (self.ui.movie.start(), self.ui.label_movie.show(), self.ui.label_icon_site.hide()))
        self.ui.webEngineView.loadFinished.connect(
            lambda: (self.ui.movie.stop(), self.ui.label_movie.hide(), self.ui.label_icon_site.show()))
        self.ui.webEngineView.iconChanged.connect(self.handle_icon_changed)
        self.ui.options.clicked.connect(lambda: self.open_dialog_ops())
        self.ui.download_buttton.clicked.connect(
            lambda: self.open_dialog_download())

        self.trie = Trie()

        completer = QCompleter()
        self.ui.url.setCompleter(completer)
        self.ui.url.textChanged.connect(self.on_text_changed)

    def disconnect_signals(self):
        self.ui.arrow_left_historic.customContextMenuRequested.disconnect()
        self.ui.arrow_right_historic.customContextMenuRequested.disconnect()
        self.ui.page_web.profile().downloadRequested.disconnect()
        self.ui.page_web.certificateError.disconnect()
        self.ui.arrow_left_historic.clicked.disconnect()
        self.ui.arrow_right_historic.clicked.disconnect()
        self.ui.url.returnPressed.disconnect()
        self.ui.webEngineView.urlChanged.disconnect()
        self.ui.webEngineView.loadStarted.disconnect()
        self.ui.webEngineView.loadFinished.disconnect()
        self.ui.webEngineView.iconChanged.disconnect()
        self.ui.options.clicked.disconnect()
        self.ui.download_buttton.clicked.disconnect()
        self.trie.root = None
        self.ui.url.textChanged.disconnect()

    def handle_icon_changed(self, iconUrl):
        icon = self.ui.webEngineView.icon()
        if not icon.isNull():
            pixmap = icon.pixmap(25, 25)  # Tamanho do ícone desejado
            self.ui.label_icon_site.setPixmap(pixmap)  # Exibir o ícone em um QLabel
            self.main_page.ui.tabs.setTabIcon(self.main_page.ui.tabs.indexOf(self.ui.page), QIcon(pixmap))

    def inputs(self):
        js = """
        let qtd = document.getElementsByTagName("input").length

        alert("inputs: " + qtd)
        """
        # self.ui.webEngineView.page().runJavaScript(js)

    def load_historic_in_trie(self):
        historic = recover_historic()

        if bool(historic):
            for his in historic['Sites']:
                self.trie.insert(his['name'])

    def on_text_changed(self, text):
        autocomplete_suggestions = self.trie.search(text.lower())
        completer = self.ui.url.completer()
        model = QStringListModel()
        model.setStringList([""] if not autocomplete_suggestions else autocomplete_suggestions)
        completer.setModel(model)
        self.ui.url.setCompleter(completer)

    # Método para atualizar o estado dos botões de navegação
    def update_navigation_buttons(self):
        current_page = self.ui.webEngineView.url().toString()
        current_index = self.sites_visitados.index(current_page) if current_page in self.sites_visitados else -1

        # Verifica se é possível retroceder ou avançar
        can_go_back = current_index > 0
        can_go_forward = current_index < len(self.sites_visitados) - 1

        # Desabilita e ajusta visualmente os botões se não for possível retroceder ou avançar
        self.ui.arrow_left_historic.setEnabled(can_go_back)
        self.ui.arrow_left_historic.setStyleSheet(
            "color: rgba(255, 255, 255, 0.5);" if not can_go_back else "")

        self.ui.arrow_right_historic.setEnabled(can_go_forward)
        self.ui.arrow_right_historic.setStyleSheet(
            "color: rgba(255, 255, 255, 0.5);" if not can_go_forward else "")

    def load_direction_specific_historic(self, direc: str):
        if direc == 'ant':
            self.ui.webEngineView.back()
        elif direc == 'prox':
            self.ui.webEngineView.forward()
        self.update_navigation_buttons()
    
    def open_dialog_download(self, view=True):
        if not self.main_page.dialog_download:
            loader = QUiLoader()
            ui_file = QFile(os.path.abspath(os.path.join("Pages", "dialog_downloads.ui")))
            ui_file.open(QFile.ReadOnly)
            dialog_widget = loader.load(ui_file)
            ui_file.close()

            # Criar o diálogo
            dialog = QDialog(self.main_page)
            dialog.setWindowModality(Qt.WindowModality.NonModal)
            dialog.setWindowTitle("Downloads")
            dialog.setModal(True)  # Permitir interação com a janela principal
            layout = QVBoxLayout(dialog)
            layout.addWidget(dialog_widget)

            self.main_page.dialog_download = dialog

            if view:
                dialog.exec()
        else:
            self.main_page.dialog_download.exec()

    def open_dialog_ops(self, view=True):
        if not self.main_page.dialog_ops:
            self.main_page.ui.tabs.setTabsClosable(True)
            loader = QUiLoader()
            ui_file = QFile(os.path.abspath(os.path.join("Pages", "dialog_ops.ui")))
            ui_file.open(QFile.ReadOnly)
            dialog_widget = loader.load(ui_file)
            ui_file.close()

            add_page = dialog_widget.findChild(QPushButton, 'add_page')
            add_page.clicked.connect(
                lambda: self.main_page.ui.tabs.addTab(DefaultSearchPageImplementation(self.main_page.ui.tabs, self.main_page).ui.page,
                                                      "Nova Página"))

            download_page = dialog_widget.findChild(QPushButton, 'donwloads_page')
            download_page.clicked.connect(
                lambda: self.main_page.ui.tabs.addTab(DownloadImplementation(self.main_page, self.main_page).ui.downloads,
                                                      "Downloads"))

            historic_page = dialog_widget.findChild(QPushButton, 'historic_page')
            historic_page.clicked.connect(
                lambda: self.main_page.ui.tabs.addTab(HistoricoImplementation(self.main_page, self.main_page).ui.historic,
                                                      "Histórico"))

            config_page = dialog_widget.findChild(QPushButton, "configs")
            config_page.clicked.connect(
                lambda: self.main_page.ui.tabs.addTab(
                    LoadPageImplementation(self.main_page, self.main_page, title="Configurações",
                                           html="http://localhost:3000/config/").ui.load_page, "Configurações"))
            find_page = dialog_widget.findChild(QPushButton, 'findpage')
            find = FindInPage(webView=self.ui.webEngineView)
            find_page.clicked.connect(lambda: find.show())

            # Criar o diálogo
            dialog = QDialog(self.main_page)
            dialog.setWindowModality(Qt.WindowModality.NonModal)
            dialog.setWindowTitle("Opções")
            dialog.setModal(True)  # Permitir interação com a janela principal
            layout = QVBoxLayout(dialog)
            layout.addWidget(dialog_widget)

            # Exibir o diálogo modalmente
            self.main_page.dialog_ops = dialog
            if view:
                dialog.exec()
        else:
            self.main_page.ui.tabs.setTabsClosable(True)
            self.main_page.dialog_ops.exec()

    def update_url(self, url_c) -> None:
        url = url_c.toString()
        data = datetime.datetime.now()
        id = register_historic(url, [], data) - 1
        self.site_atual = {"id": id, "name": url, "cookies": [], "date_time": f"{data}"}

        page = self.ui.webEngineView.url().toString()
        if page not in self.sites_visitados:
            self.sites_visitados.append(page)

        self.ui.url.setText(url)
        self.ui.url.setCursorPosition(0)
        self.update_navigation_buttons()

    def limit_string(self, text: str, limit: int) -> str:
        if len(text) > limit:
            return text[:limit - 3] + "..."  # Corta o texto e adiciona "..." no final
        return text

    def update_title(self, url_c: QUrl) -> None:
        index = self.main_page.ui.tabs.indexOf(self.ui.page)
        text = self.ui.webEngineView.title()
        self.main_page.ui.tabs.setTabText(index, self.limit_string(text, 30))

    @staticmethod
    def is_valid_url(url_string: str) -> bool:
        url_pattern = re.compile(
            r'^(https?://)?' +  # validar protocolo opcional
            r'(?:(?:([a-z\d]([a-z\d-]*[a-z\d])*)\.)+[a-z]{2,}|' +  # validar nome de domínio
            r'(?:\d{1,3}\.){3}\d{1,3})' +  # validar endereço IP (v4)
            r'(:\d+)?' +  # validar porta opcional
            r'(/[-a-z\d%_.~+]*)*' +  # validar caminho
            r'(\?[;&a-z\d%_.~+=-]*)?' +  # validar string de consulta
            r'(#[-a-z\d_]*)?$',  # validar fragmento
            re.IGNORECASE  # ignora case sensitivity
        )
        return bool(re.match(url_pattern, url_string))
    
    @Slot(QWebEngineCertificateError)
    def handle_certificate_error(self, error):
        url = error.url()
        # Verifica se a URL é HTTPS e tenta carregar usando HTTP
        if url.scheme() == 'https':
            new_url = QUrl(url.toString().replace('https://', 'http://'))
            self.ui.webEngineView.load(new_url)
            return True  # Ignora o erro de certificado original
        return False  # Não ignora outros erros de certificado


    def search(self, web_loader: QWebEngineView, search_text: str) -> None:
        if self.is_valid_url(search_text):
            url = f"{search_text}"
            
            if 'localhost:' in search_text:
                web_loader.load(QUrl(url))
                return
            
            if 'https://' not in search_text:
                url = f"https://{search_text}"

            web_loader.load(QUrl(url))
            return

        if 'file:///' in search_text:
            web_loader.load(QUrl.fromLocalFile(search_text.replace('file:///', "")))
            return

        search_url = "https://www.google.com/search?q=" + search_text.replace(" ", "+")

        web_loader.load(QUrl(search_url))

    @Slot(QWebEngineDownloadRequest)
    def download_file(self, download_item: QWebEngineDownloadRequest) -> None:
        if download_item.url().toString() not in self.downloads:
            url_download = download_item.url().toString()
            self.downloads.append(url_download)

            folder_path = QFileDialog.getExistingDirectory(self, "Selecionar pasta de destino",
                                                           options=QFileDialog.Option.ShowDirsOnly)
            suggested_file_name = download_item.suggestedFileName()
            progress_bar = DownloadImplementation.add_download_notification(main_pages=self.main_page.dialog_download,
                                                              download_data={'download_time': datetime.datetime.now(),
                                                                             'name': suggested_file_name,
                                                                             'path': os.path.join(folder_path,
                                                                                                  suggested_file_name)})
            downloader = Downloader.Downloader(self.main_page)
            downloader.download_finished.connect(
                lambda suggested_file_name_arg, folder_path_arg: self.handle_download_finished(suggested_file_name_arg,
                                                                                               folder_path_arg,
                                                                                               url_download),
                                                Qt.ConnectionType.QueuedConnection)
            downloader.download_failed.connect(self.handle_download_failed,
                                                Qt.ConnectionType.QueuedConnection)
            downloader.progress_update.connect(lambda percent, progress=progress_bar: self.handle_progress(percent, progress),
                                                Qt.ConnectionType.QueuedConnection)
            downloader.download_file(download_item.url().toString(), folder_path, suggested_file_name)

    @staticmethod
    def handle_progress(percent: float, progress_bar: QProgressBar):
        try:
            progress_bar.setValue(percent)
        except Exception as e:
            print(e)

    def handle_download_finished(self, suggested_file_name, folder_path, url):
        self.downloads.remove(url)
        threading.Thread(target=register_download_historic,
                         args=(suggested_file_name, folder_path, 'Concluido',
                               datetime.datetime.now())).start()

    @staticmethod
    def handle_download_failed(suggested_file_name, folder_path):
        threading.Thread(target=register_download_historic,
                         args=(suggested_file_name, folder_path, 'Erro', datetime.datetime.now())).start()


class DownloadImplementation(QWidget):

    def __init__(self, parent=None, main_page=None):
        super().__init__(parent)
        self.identification = str(uuid.uuid4())
        self.ui = DownloadsPage()
        self.ui.setup_ui(self)
        self.ui.arrow_left_back.hide()
        self.main_page = main_page
        self.load_download_historic(limit=10)
        self.loaded_items = 0
        self.items_per_load = 10  # Número de itens a serem carregados a cada vez
        self.connect_signals()
        
    def connect_signals(self):
        self.ui.scrollAreaDownloads.verticalScrollBar().valueChanged.connect(self.scroll_event)
        self.ui.search_input.textChanged.connect(lambda txt: self.load_download_historic(10, txt))

    def disconnect_signals(self):
        self.ui.scrollAreaDownloads.verticalScrollBar().valueChanged.disconnect()
        self.ui.search_input.textChanged.disconnect()
    
    def load_more_items(self, f: str = ""):
        downloads = recover_download_historic(f=f)
        items_to_load = downloads['Files'][self.loaded_items:self.loaded_items + self.items_per_load]

        for download_data in items_to_load:
            DownloadImplementation.add_download_history(main_page=self, download_data=download_data)

        self.loaded_items += self.items_per_load

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
        history = recover_download_historic(f=f)

        self.loaded_items = 0
        self.items_per_load = 10

        if bool(history):
            cont = 0
            for download in history['Files']:
                if cont <= limit:
                    DownloadImplementation.add_download_history(main_page=self, download_data=download)
                    cont += 1

    @staticmethod
    def load_download_notificatios(main_page):
        layout = main_page['fields'].findChild(QLayout, 'container_download_notifications')
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                layout.removeWidget(child.widget())
                child.widget().deleteLater()
                layout.update()

        history = recover_download_historic(file_saved='download_notifications.json')
        if bool(history):
            for download in history['Files']:
                DownloadImplementation.add_download_notification(main_pages=main_page, download_data=download,
                                                   show_progress=False)

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

            (main_pages.findChild(QLayout, 'container_download_notifications')
             .addWidget(download_item_list))

            return progressBar


class HistoricoImplementation(QWidget):

    def __init__(self, parent=None, main_page=None):
        super().__init__(parent)
        self.identification = str(uuid.uuid4())
        self.ui = HistoricoPage()
        self.ui.setup_ui(self)
        self.ui.arrow_left_back_historic.hide()
        self.main_page = main_page
        self.load_historic(10)
        self.connect_signals()
        self.loaded_items = 0
        self.items_per_load = 10  # Número de itens a serem carregados a cada vez

        
    def connect_signals(self):
        self.ui.scrollAreaHistoric.verticalScrollBar().valueChanged.connect(self.scroll_event)
        self.ui.search_input.textChanged.connect(lambda txt: self.load_historic(10, txt))

    def disconnect_signals(self):
        self.ui.scrollAreaHistoric.verticalScrollBar().valueChanged.disconnect()
        self.ui.search_input.textChanged.disconnect()
    
    def load_more_items(self, f: str):
        history = recover_historic(f=f)
        items_to_load = history['Sites'][self.loaded_items:self.loaded_items + self.items_per_load]

        for site in items_to_load:
            self.add_historic_item(historic_data=site)

        self.loaded_items += self.items_per_load

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
        history = recover_historic(f=f)

        self.loaded_items = 0
        self.items_per_load = 10

        if bool(history):
            cont = 0
            for site in history['Sites']:
                if cont <= limit:
                    self.add_historic_item(historic_data=site)
                    cont += 1
                else:
                    break

    def open_historic_site(self, site):
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
            open_site.setText(f"Site: {historic_data['name']}\nData: {historic_data['date_time']}")
            open_site.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            open_site.setObjectName(u"open_site")
            sizePolicy.setHeightForWidth(open_site.sizePolicy().hasHeightForWidth())
            open_site.setSizePolicy(sizePolicy)
            open_site.clicked.connect(lambda: self.open_historic_site(historic_data['name']))
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
                lambda: remove_historic_item(id=historic_data['id'],
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


class LoadPageImplementation(QWidget):
    def __init__(self, parent=None, main_page=None, title="SurfEase", html=""):
        super().__init__(parent)
        self.main_page = main_page
        self.title = title
        self.html = html
        self.identification = str(uuid.uuid4())
        self.ui = LoadPage(parent=None, main_page=main_page, title=title, html=html, cache_path=self.identification)
        self.ui.setupUi(self)
    
    def disconnect_signals(self):
        pass


class ConsolePageImplementation(QWidget):

    def __init__(self, parent=None, main_page=None, webEngine: QWebEngineView = None):
        super().__init__(parent)
        self.main_page = main_page
        self.webEngine = webEngine
        self.identification = str(uuid.uuid4())
        self.ui = ConsolePage()
        self.ui.setupUi(self)
        self.connect_signals()

        # configurando

        self.webEngine.urlChanged.connect(self.update_title)
        self.webEngine.page().javaScriptConsoleMessage = self.javascriptConsoleMessage
        self.ui.console_input.returnPressed.connect(self.exec_js_input)

    def update_title(self, url):
        self.ui.title = "Console - " + self.webEngine.title()
        self.window().setWindowTitle(self.ui.title)

    def exec_js_input(self):
        command = self.ui.console_input.text()
        threading.Thread(target=register_console_historic, args=(command,)).start()
        self.webEngine.page().runJavaScript(command)
        self.ui.console_input.setText("")

    def javascriptConsoleMessage(self, level, message, lineNumber, sourceID):
        level_mes = ""
        back_color = None
        font_color = None

        if level == QWebEnginePage.JavaScriptConsoleMessageLevel.InfoMessageLevel:
            level_mes = "Info"
            back_color = "white"
            font_color = "black"
        elif level == QWebEnginePage.JavaScriptConsoleMessageLevel.WarningMessageLevel:
            level_mes = "Warning"
            back_color = "yellow"
            font_color = "black"
        elif level == QWebEnginePage.JavaScriptConsoleMessageLevel.ErrorMessageLevel:
            level_mes = "Error"
            back_color = "red"
            font_color = "white"
        else:
            level_mes = "Info"
            back_color = "white"
            font_color = "black"

        new_txt = f'\n<span style="background-color: {back_color}; color:{font_color}">Console {level_mes} at {lineNumber}, SourceId: {sourceID}: {message}</span><br>'
        cursor = self.ui.console_output.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertHtml(new_txt)
        cursor.movePosition(QTextCursor.End)

    def connect_signals(self):
        self.webEngine.page().loadFinished.connect(self.update_html)
        self.webEngine.page().contentsSizeChanged.connect(self.update_html)
        self.update_html()
    
    def disconnect_signals(self):
        self.webEngine.page().loadFinished.disconnect(self.update_html)
        self.webEngine.page().contentsSizeChanged.disconnect(self.update_html)

    def update_html(self):
        self.webEngine.page().toHtml(lambda html: self.format_txt_html(html))

    def format_txt_html(self, html):
        self.ui.script.setPlainText(html)
        self.highlight_html(html)

    def highlight_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        formatted_html = soup.prettify()
        self.ui.script.setPlainText(formatted_html)
