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
