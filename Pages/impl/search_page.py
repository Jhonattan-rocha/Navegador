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

from Pages.impl.downloads_page import DownloadImplementation
from Pages.impl.historic_page import HistoricoImplementation
from Pages.impl.console_page import ConsolePageImplementation

class DefaultSearchPageImplementation(QWidget):

    def __init__(self, parent=None, main_page=None):
        super().__init__(parent)
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
            
    def console_page(self):
        console = ConsolePageImplementation(None, self.main_page, self.ui.webEngineView)
        console.show()
        self.main_page.consoles.append(console)
    
    def open_link_in_new_window(self, event: QWebEngineNewWindowRequest):
        # print(event.requestedUrl())
        # print(event.destination())
        
        if event.destination() == QWebEngineNewWindowRequest.DestinationType.InNewTab:
            tab = DefaultSearchPageImplementation(self.main_page.ui.tabs, self.main_page)
            tab.ui.webEngineView.load(event.requestedUrl())
            self.main_page.ui.tabs.addTab(tab.ui.page, tab.ui.webEngineView.page().title() or "Nova Página")
            self.main_page.ui.tabs.setTabsClosable(True)
            
        if event.destination() == QWebEngineNewWindowRequest.DestinationType.InNewWindow:
            from main import Main
            page = Main()
            tab = DefaultSearchPageImplementation(self.main_page.ui.tabs, self.main_page)
            tab.ui.webEngineView.load(event.requestedUrl())
            page.ui.tabs.addTab(tab.ui.page, tab.ui.webEngineView.page().title() or "Nova Página")
            page.show()
        
        if event.destination() == QWebEngineNewWindowRequest.DestinationType.InNewDialog:
            dialog = NewWindowDialog(url=event.requestedUrl().toString())
            dialog.exec()
            
    def handle_context_menu(self, event):
        # Obtendo o menu de contexto padrão
        default_menu = self.ui.webEngineView.createStandardContextMenu()

        for act in default_menu.actions():
            if "View page source".lower() == act.text().lower():
                act.triggered.disconnect()
                act.triggered.connect(lambda : self.console_page())
                
        # Criando uma ação personalizada
        custom_action_reload_tab = default_menu.addAction("Reload tab...")
        custom_action_reload_tab.triggered.disconnect()
        custom_action_reload_tab.triggered.connect(lambda args: self.realod_tab())
        
        custom_action_print = default_menu.addAction("Print page...")
        custom_action_print.triggered.disconnect()
        custom_action_print.triggered.connect(lambda args: self.print_page())

        custom_action_add_page = default_menu.addAction("Add Page...")
        custom_action_add_page.triggered.disconnect()
        custom_action_add_page.triggered.connect(lambda args: ShortcutManager().shortcuts[Qt.CTRL | Qt.Key.Key_N].activated.emit())
                
        custom_action_add_config_page = default_menu.addAction("Config Page...")
        custom_action_add_config_page.triggered.disconnect()
        custom_action_add_config_page.triggered.connect(lambda args: ShortcutManager().shortcuts["Ctrl+Shift+c"].activated.emit())
        
        # Exibindo o menu de contexto modificado
        default_menu.exec(event.globalPos())
    
    def realod_tab(self):
        tab = DefaultSearchPageImplementation(self.main_page.ui.tabs, self.main_page)
        current_index = self.main_page.ui.tabs.currentIndex()
        current_tab = self.main_page.ui.tabs.currentWidget()
        
        tab.ui.webEngineView.load(current_tab.implementation.ui.webEngineView.url())
        self.main_page.ui.tabs.removeTab(current_index)
        
        self.main_page.ui.tabs.addTab(tab.ui.page, "Nova Página")
    
    def showContextMenu(self, pos):
        menu = QMenu(self)

        history = self.ui.webEngineView.history()
        for i in range(min(history.count(), 10)):  # Obter os últimos 10 itens do histórico
            action = QAction(history.itemAt(i).title(), self)
            action.setData(history.itemAt(i).url())  # Armazenar a URL como dados da ação
            action.triggered.connect(lambda event: self.search(self.ui.webEngineView, history.itemAt(i).url().toString()))
            menu.addAction(action)
            
        menu.exec(self.ui.arrow_left_historic.mapToGlobal(pos))

    def closeEvent(self, event):
        super().closeEvent(event)
    
    def addfavoritie(self):
        historico = recover_historic(f=self.ui.url.text())

        icon_full = historico[0].fav
        if historico.count() > 0:
            for site in historico:
                update_historic(site=site.site, id=site.id, fav=not site.fav)
            
            icon_star = QIcon()
            icon_star.addFile(f"figs/star_{"full" if icon_full else "out"}.png", QSize(), QIcon.Normal, QIcon.Off)
            
            self.ui.favoritos_button.setIcon(icon_star)
            self.ui.favoritos.load_favorities()
        

    def connect_signals(self):
        self.ui.favoritos_button.clicked.connect(self.addfavoritie)
        self.ui.arrow_left_historic.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.arrow_right_historic.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.arrow_left_historic.customContextMenuRequested.connect(self.showContextMenu)
        self.ui.arrow_right_historic.customContextMenuRequested.connect(self.showContextMenu)
        self.ui.webEngineView.page().profile().downloadRequested.connect(self.download_file)
        self.ui.webEngineView.page().certificateError.connect(self.handle_certificate_error)
        self.ui.arrow_left_historic.clicked.connect(
            lambda: self.load_direction_specific_historic('ant'))
        self.ui.arrow_right_historic.clicked.connect(
            lambda: self.load_direction_specific_historic('prox'))
        self.ui.url.returnPressed.connect(
            lambda: self.search(web_loader=self.ui.webEngineView,
                                search_text=self.ui.url.text()))

        self.ui.webEngineView.urlChanged.connect(self.update_url)
        self.ui.webEngineView.urlChanged.connect(self.update_title)

        self.ui.webEngineView.page().newWindowRequested.connect(self.open_link_in_new_window)
        self.ui.webEngineView.loadStarted.connect(
            lambda: (self.ui.movie.start(), self.ui.label_movie.show(), self.ui.label_icon_site.hide()))
        self.ui.webEngineView.loadFinished.connect(
            lambda: (self.ui.movie.stop(), self.ui.label_movie.hide(), self.ui.label_icon_site.show(), self.ui.favoritos.load_favorities()))
        self.ui.webEngineView.iconChanged.connect(self.handle_icon_changed)
        self.ui.options.clicked.connect(lambda: self.open_dialog_ops())
        self.ui.download_buttton.clicked.connect(
            lambda: self.open_dialog_download())
        


        completer = QCompleter()
        completer.popup().setStyleSheet("""
            QListView {
                background-color: #f0f0f0;
                border: 1px solid #d4d4d4;
                color: #333;
                selection-background-color: #c2e0f9;
                selection-color: #333;
                padding: 5px;
                font-family: Arial;
                font-size: 12px;
                border-radius: 5px; /* Adiciona bordas arredondadas */
            }
        """)
        completer.popup().setMinimumWidth(200)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.ui.url.setCompleter(completer)
        self.ui.url.textChanged.connect(self.on_text_changed)

    def disconnect_signals(self):
        def _safe(disconnector):
            try:
                disconnector()
            except (RuntimeError, TypeError):
                pass

        _safe(self.ui.favoritos_button.clicked.disconnect)
        _safe(self.ui.arrow_left_historic.customContextMenuRequested.disconnect)
        _safe(self.ui.arrow_right_historic.customContextMenuRequested.disconnect)
        # downloadRequested vive no PERFIL compartilhado: desconectamos apenas o
        # NOSSO slot, senão derrubaríamos os downloads das outras abas.
        _safe(lambda: self.ui.webEngineView.page().profile().downloadRequested.disconnect(self.download_file))
        _safe(self.ui.webEngineView.page().certificateError.disconnect)
        _safe(self.ui.arrow_left_historic.clicked.disconnect)
        _safe(self.ui.arrow_right_historic.clicked.disconnect)
        _safe(self.ui.url.returnPressed.disconnect)
        _safe(self.ui.webEngineView.urlChanged.disconnect)
        _safe(self.ui.webEngineView.loadStarted.disconnect)
        _safe(self.ui.webEngineView.loadFinished.disconnect)
        _safe(self.ui.webEngineView.iconChanged.disconnect)
        _safe(self.ui.options.clicked.disconnect)
        _safe(self.ui.download_buttton.clicked.disconnect)
        _safe(self.ui.url.textChanged.disconnect)
        _safe(self.ui.webEngineView.page().newWindowRequested.disconnect)

    def handle_icon_changed(self, iconUrl):
        icon = self.ui.webEngineView.icon()
        if not icon.isNull():
            pixmap = icon.pixmap(25, 25)  # Tamanho do ícone desejado
            self.ui.label_icon_site.setPixmap(pixmap)  # Exibir o ícone em um QLabel
            self.main_page.ui.tabs.setTabIcon(self.main_page.ui.tabs.indexOf(self.ui.page), QIcon(pixmap))

    def on_text_changed(self, text: str):
        autocomplete_suggestions = recover_historic(text.lower())
        completer = self.ui.url.completer()
        model = QStringListModel()
        model.setStringList([suggestion.site for suggestion in autocomplete_suggestions])
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
            ui_file = QFile(os.path.abspath(os.path.join("Pages", "Dialogs", "dialog_downloads.ui")))
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
            ui_file = QFile(os.path.abspath(os.path.join("Pages", "Dialogs", "dialog_ops.ui")))
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
            config_page.clicked.connect(lambda args: ShortcutManager().shortcuts["Ctrl+Shift+c"].activated.emit())
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
        his = recover_historic(f=url, limit=10)
        if not his.count() > 0:
            register_historic(url, self.ui.webEngineView.title(), data)
        
        icon_star = QIcon()
        icon_star.addFile(f"figs/star_{"full" if his[0].fav else "out"}.png", QSize(), QIcon.Normal, QIcon.Off)
        
        self.ui.favoritos_button.setIcon(icon_star)
        
        page = self.ui.webEngineView.url().toString()
        if page not in self.sites_visitados:
            self.sites_visitados.append(page)

        self.ui.url.setText(url)
        self.ui.url.setCursorPosition(0)
        self.update_navigation_buttons()
        self.ui.favoritos.load_favorities()

    def limit_string(self, text: str, limit: int) -> str:
        if len(text) > limit:
            return text[:limit - 3] + "..."  # Corta o texto e adiciona "..." no final
        return text

    def update_title(self, url_c: QUrl) -> None:
        index = self.main_page.ui.tabs.indexOf(self.ui.page)
        text = self.ui.webEngineView.page().title()
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
    def handle_certificate_error(self, error: QWebEngineCertificateError):
        # NUNCA rebaixar HTTPS->HTTP automaticamente: isso era um vetor de
        # man-in-the-middle. Como um navegador de verdade, avisamos e deixamos
        # o usuário decidir se quer prosseguir.
        host = error.url().host()
        resposta = QMessageBox.warning(
            self,
            "Conexão não é segura",
            f"O certificado de '{host}' não pôde ser verificado.\n\n"
            f"{error.description()}\n\n"
            "Continuar mesmo assim? (não recomendado)",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if resposta == QMessageBox.StandardButton.Yes:
            error.acceptCertificate()
        else:
            error.rejectCertificate()


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
        # downloadRequested vive no perfil COMPARTILHADO, então todas as abas
        # recebem o mesmo item. A primeira que aceitar inicia o download; as
        # demais saem aqui (o estado deixou de ser "DownloadRequested").
        DownloadState = QWebEngineDownloadRequest.DownloadState
        if download_item.state() != DownloadState.DownloadRequested:
            return

        suggested_file_name = download_item.suggestedFileName()
        if settings_app.value("GeneralSettings/AskWhereSaveDownload", type=bool):
            folder_path = QFileDialog.getExistingDirectory(
                self, "Selecionar pasta de destino", options=QFileDialog.Option.ShowDirsOnly)
            if not folder_path:
                download_item.cancel()
                return
        else:
            folder_path = (settings_app.value("GeneralSettings/DownloadPath", type=str)
                           or os.path.abspath("./downloads"))

        # Download NATIVO do Qt: usa a sessão/cookies do próprio navegador, então
        # downloads de páginas logadas funcionam (o antigo refazia o GET com um
        # requests anônimo, sem sessão).
        download_item.setDownloadDirectory(folder_path)
        download_item.setDownloadFileName(suggested_file_name)

        download_data = register_download_historic(
            status="baixando", download_time=datetime.datetime.now(),
            folder_path=os.path.join(folder_path, suggested_file_name),
            suggested_file_name=suggested_file_name)
        progress_bar = DownloadImplementation.add_download_notification(
            main_pages=self.main_page.dialog_download, download_data=download_data)

        def on_progress():
            total = download_item.totalBytes()
            if total > 0 and progress_bar is not None:
                try:
                    progress_bar.setValue(int(download_item.receivedBytes() / total * 100))
                except RuntimeError:
                    pass

        def on_finished():
            concluido = download_item.state() == DownloadState.DownloadCompleted
            update_download_status(download_data.id, "Concluído" if concluido else "Erro")
            if progress_bar is not None:
                try:
                    progress_bar.setValue(100 if concluido else 0)
                except RuntimeError:
                    pass

        download_item.receivedBytesChanged.connect(on_progress)
        download_item.isFinishedChanged.connect(on_finished)
        download_item.accept()
