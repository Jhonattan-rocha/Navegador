# This Python file uses the following encoding: utf-8
import datetime
import os.path
import re
import sys
import threading

from PySide6.QtCore import (QUrl, Qt)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QLineEdit, QTabWidget,
                               QWidget)
from PySide6.QtWidgets import (QFileDialog)

import Downloader
from modifications_on_screen import open_dialog_download, open_dialog_ops, add_download_history, \
    load_download_history, add_download_notification, load_download_notificatios
from register_recover import register_download_history
# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_Widget


class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.dialog_ops = None
        self.dialog_download = None
        open_dialog_ops(main_window=self, view=False)
        open_dialog_download(main_window=self, view=False)
        self.ui.webEngineView.load(self.ui.url.text())
        self.ui.webEngineView.urlChanged.connect(
            lambda url, url_input=self.ui.url: self.update_url(url_input, url))
        self.ui.webEngineView.titleChanged.connect(
            lambda title, index=self.ui.tabs.currentIndex(), tabs=self.ui.tabs: self.update_title(title, index, tabs))
        self.ui.options.clicked.connect(lambda: open_dialog_ops(main_window=self))
        self.ui.download_buttton.clicked.connect(lambda: open_dialog_download(main_window=self))
        self.ui.options_donwload.clicked.connect(lambda: open_dialog_ops(main_window=self))
        self.ui.tabs.tabCloseRequested.connect(self.close_tab)
        self.ui.url.returnPressed.connect(
            lambda web=self.ui.webEngineView, search=self.ui.url: self.search(web_loader=web,
                                                                              search_text=search.text()))
        self.ui.arrow_left_back.clicked.connect(lambda: self.ui.stacked_pages.setCurrentIndex(0))
        self.ui.arrow_left_back_historic.clicked.connect(lambda: self.ui.stacked_pages.setCurrentIndex(0))
        self.ui.webEngineView.page().profile().downloadRequested.connect(self.download_file)

    def update_url(self, url_input: QLineEdit, url: QUrl) -> None:
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

    def close_tab(self, index) -> None:
        tabs = self.ui.tabs.count()
        if tabs > 1:
            self.ui.tabs.removeTab(index)
            tabs = self.ui.tabs.count()
            if tabs == 1:
                self.ui.tabs.setTabsClosable(False)
        else:
            self.ui.tabs.setTabsClosable(False)

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
        progress_bar = add_download_notification(main_windows=self.dialog_download,
                                                 download_data={'download_time': datetime.datetime.now(),
                                                                'name': suggested_file_name,
                                                                'path': os.path.join(folder_path,
                                                                                     suggested_file_name)})
        downloader.progress_update.connect(lambda percent: self.handle_progress(percent, progress_bar),
                                           Qt.ConnectionType.QueuedConnection)

        threading.Thread(target=register_download_history,
                         args=(suggested_file_name, folder_path, 'Baixando',
                               f'{datetime.datetime.now()}', 'download_notifications.json')).start()
        downloader.download_file(download_item.url().toString(), folder_path, suggested_file_name, progress_bar)

    def handle_progress(self, percent: float, progress_bar):
        progress_bar.setValue(percent)

    def handle_download_finished(self, suggested_file_name, folder_path):
        threading.Thread(target=register_download_history,
                         args=(suggested_file_name, folder_path, 'Concluido',
                               f'{datetime.datetime.now()}')).start()
        add_download_history(self, download_data={'name': suggested_file_name, 'path': folder_path,
                                                  'status': 'Concluido',
                                                  'download_time': f'{datetime.datetime.now()}'})

    def handle_download_failed(self, suggested_file_name, folder_path):
        threading.Thread(target=register_download_history,
                         args=(suggested_file_name, folder_path, 'Erro', f'{datetime.datetime.now()}')).start()
        add_download_history(self,
                             download_data={'name': suggested_file_name, 'path': folder_path, 'status': 'Erro',
                                            'download_time': f'{datetime.datetime.now()}'})


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    load_download_history(widget)
    load_download_notificatios(widget.dialog_download)
    sys.exit(app.exec())
