# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtCore import Qt
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QWidget)

from Pages.Implementation import Default, Historic, Download
from Pages.ShortCuts import ShortcutManager
# Important:
# You need to run the following command to generate the main_page.py file
#     pyside6-uic form.ui -o main_page.py, or
#     pyside2-uic form.ui -o main_page.py
from Pages.main_page import Main_page


class Main(QWidget):
    def __init__(self, parent=None, new_tab=True):
        super().__init__(parent)
        self.ui = Main_page()
        self.ui.setupUi(self)
        self.dialog_ops = None
        self.dialog_download = None
        self.site_atual: dict = {}
        if new_tab:
            self.ui.tabs.addTab(Default(self, main_window=self).ui.page, "Nova Página")
        self.ui.tabs.tabCloseRequested.connect(self.close_tab)
        self.short_cuts = ShortcutManager()

        self.short_cuts.register_shortcut(self, Qt.Key.Key_F5, lambda: self.reload_page())

        self.short_cuts.register_shortcut(self, Qt.Key.Key_Tab | Qt.CTRL, lambda: self.next_page())

        self.short_cuts.register_shortcut(self, "Ctrl+Shift+tab",
                                          lambda: self.previous_page())

        self.short_cuts.register_shortcut(self, Qt.CTRL | Qt.Key.Key_N, lambda: (self.ui.tabs.addTab(
            Default(self, self).ui.page, 'Nova Página'), self.ui.tabs.setTabsClosable(True)))

        self.short_cuts.register_shortcut(self, Qt.CTRL | Qt.Key.Key_H, lambda: (self.ui.tabs.addTab(
            Historic(self, self).ui.historic, "Histórico"), self.ui.tabs.setTabsClosable(True)))

        self.short_cuts.register_shortcut(self, Qt.CTRL | Qt.Key.Key_D, lambda: (self.ui.tabs.addTab(
            Download(self, self).ui.downloads, "Downloads"), self.ui.tabs.setTabsClosable(True)))

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
        tabs = self.ui.tabs.count()
        if tabs > 1:
            self.ui.tabs.removeTab(index)
            tabs = self.ui.tabs.count()
            if tabs == 1:
                self.ui.tabs.setTabsClosable(False)
        else:
            self.ui.tabs.setTabsClosable(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Main()
    widget.show()
    sys.exit(app.exec())
