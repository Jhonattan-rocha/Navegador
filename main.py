# This Python file uses the following encoding: utf-8
import os
import shutil
import sys

from PySide6.QtCore import Qt, QCoreApplication, QTimer
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QWidget)

from Pages.FindInPage import FindInPage
from Pages.Implementation import ConsolePageImplementation, DefaultSearchPageImplementation, HistoricoImplementation, DownloadImplementation
from Pages.ShortCuts import ShortcutManager
from Pages.main_page import Main_page
from PySide6.QtQuick import QQuickWindow, QSGRendererInterface
import ctypes

QQuickWindow.setGraphicsApi(QSGRendererInterface.GraphicsApi.Direct3D11Rhi)
QQuickWindow.setSceneGraphBackend("rhi")
myappid = u'mycompany.myproduct.subproduct.version.1' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class Main(QWidget):
    
    consoles = []
    
    def __init__(self, parent=None, new_tab=True):
        super().__init__(parent)
        self.ui = Main_page()
        self.ui.setupUi(self)
        self.dialog_ops = None
        self.dialog_download = None
        self.ui.tabs.tabCloseRequested.connect(self.close_tab)
        
        self.short_cuts = ShortcutManager()

        self.short_cuts.register_shortcut(self, Qt.Key.Key_F5, lambda: self.reload_page())

        self.short_cuts.register_shortcut(self, Qt.Key.Key_Tab | Qt.CTRL, lambda: self.next_page())

        self.short_cuts.register_shortcut(self, "Ctrl+Shift+tab",
                                          lambda: self.previous_page()) 

        self.short_cuts.register_shortcut(self, Qt.CTRL | Qt.Key.Key_N, lambda: (self.ui.tabs.addTab(
            DefaultSearchPageImplementation(self.ui.tabs, self).ui.page, 'Nova Página'), self.ui.tabs.setTabsClosable(True)))

        self.short_cuts.register_shortcut(self, Qt.CTRL | Qt.Key.Key_H, lambda: (self.ui.tabs.addTab(
            HistoricoImplementation(self.ui.tabs, self).ui.historic, "Histórico"), self.ui.tabs.setTabsClosable(True)))

        self.short_cuts.register_shortcut(self, Qt.CTRL | Qt.Key.Key_D, lambda: (self.ui.tabs.addTab(
            DownloadImplementation(self.ui.tabs, self).ui.downloads, "Downloads"), self.ui.tabs.setTabsClosable(True)))

        self.short_cuts.register_shortcut(self, Qt.CTRL | Qt.Key.Key_F, lambda: self.find_in_page_short_cut())
    
        self.short_cuts.register_shortcut(self, "Ctrl+Shift+i", lambda: self.console_page())
    
    def console_page(self):
        tab = self.ui.tabs.currentWidget()
        imp = tab.implementation
        console = ConsolePageImplementation(None, self, imp.ui.webEngineView)
        console.show()
        self.consoles.append(console)    
        
    def find_in_page_short_cut(self):
        tab = self.ui.tabs.currentWidget()
        if 'page' in tab.objectName():
            find = FindInPage(webView=tab.implementation.ui.webEngineView)
            find.show()

    def previous_page(self):
        tabs = self.ui.tabs.count() - 1
        currentIndex = self.ui.tabs.currentIndex()

        if currentIndex == 0:
            self.ui.tabs.setCurrentIndex(tabs)
        elif currentIndex <= tabs:
            self.ui.tabs.setCurrentIndex(currentIndex - 1)

    def next_page(self):
        tabs = self.ui.tabs.count() - 1
        currentIndex = self.ui.tabs.currentIndex()

        if currentIndex == tabs:
            self.ui.tabs.setCurrentIndex(0)
        elif currentIndex < tabs:
            self.ui.tabs.setCurrentIndex(currentIndex + 1)

    def reload_page(self):
        index = self.ui.tabs.currentIndex()
        page = self.ui.tabs.widget(index)
        name = page.objectName().lower()
        if 'page' in name:
            web = page.findChildren(QWebEngineView)
            if bool(web):
                web[0].reload()
        elif 'historic' in name:
            page.implementation.load_historic(10)
        elif 'downloads' in name:
            page.implementation.load_download_historic(10)

    def close_tab(self, index) -> None:
        print('close tab')
        tabs = self.ui.tabs.count()
        tab = self.ui.tabs.widget(index)
        if tabs > 1:
            self.ui.tabs.removeTab(index)
            tab.implementation.disconnect_signals()
            tab.implementation.deleteLater()
            tab.implementation.ui.deleteLater()
            tab.deleteLater()
            tabs = self.ui.tabs.count()
            if tabs == 1:
                self.ui.tabs.setTabsClosable(False)
            if "page" in tab.objectName().lower():
                QTimer.singleShot(1000, lambda: shutil.rmtree(".\\cache\\"+tab.implementation.identification+"\\", ignore_errors=False))
        else:
            self.ui.tabs.setTabsClosable(False)
        QCoreApplication.processEvents()


    def closeEvent(self, event):
        print('main close')
        count = self.ui.tabs.count()
        for tab_index in range(count):
            tab = self.ui.tabs.widget(tab_index)
            tab.implementation.disconnect_signals()
            tab.implementation.deleteLater()
            tab.implementation.ui.deleteLater()
            tab.deleteLater()
        for console in self.consoles:
            try:
                console.close()
            except Exception as e:
                pass
        self.ui.deleteLater()
        self.deleteLater()
        QCoreApplication.processEvents()
        self.clear_cache()
        self.consoles.clear()
        event.accept()
    
    def clear_cache(self):
        pastas = os.listdir("./cache")
        for pasta in pastas:
            shutil.rmtree(".\\cache\\"+pasta, ignore_errors=True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Main()
    ShortcutManager().shortcuts[Qt.CTRL | Qt.Key.Key_N].activated.emit()
    widget.show()
    sys.exit(app.exec())
