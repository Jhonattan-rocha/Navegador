# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import (QApplication, QWidget)

from Pages.Implementaion import Default
# Important:
# You need to run the following command to generate the main_page.py file
#     pyside6-uic form.ui -o main_page.py, or
#     pyside2-uic form.ui -o main_page.py
from Pages.main_page import Main_page


class Main(QWidget):
    def __init__(self, parent=None, new_tab: Default = None, title: str = ""):
        super().__init__(parent)
        self.ui = Main_page()
        self.ui.setupUi(self)
        self.dialog_ops = None
        self.dialog_download = None
        self.site_atual: dict = {}

        if not new_tab:
            self.ui.tabs.addTab(Default(self, main_window=self).ui.page, "Nova Página")
        else:
            self.ui.tabs.addTab(new_tab.ui.page, title)
        self.ui.tabs.tabCloseRequested.connect(self.close_tab)

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
