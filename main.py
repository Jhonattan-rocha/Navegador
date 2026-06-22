# This Python file uses the following encoding: utf-8
import sys

# DEVE vir antes de qualquer import do QtWebEngine: ajusta flags do Chromium
# (ex.: caminho do Widevine CDM) que são lidas na inicialização do motor.
from configs.media_env import configure_media_env
configure_media_env()

from PySide6.QtCore import Qt, QCoreApplication, QUrl
from PySide6.QtGui import QIcon
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QLineEdit, QHBoxLayout)
from PySide6.QtQuick import QQuickWindow, QSGRendererInterface
from Pages.Dialogs.ConfigPage import Configuracoes
from Pages.Dialogs.FindInPage import FindInPage
from Pages.Implementation import ConsolePageImplementation, DefaultSearchPageImplementation, HistoricoImplementation, DownloadImplementation
from Pages.ShortCuts import ShortcutManager
from Pages.main_page import Main_page
from configs.Config import settings_app
import ctypes

QQuickWindow.setGraphicsApi(QSGRendererInterface.GraphicsApi.Direct3D11Rhi)
QQuickWindow.setSceneGraphBackend("rhi")
myappid = u'mycompany.myproduct.subproduct.version.1' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class Main(QWidget):

    def __init__(self, parent=None, new_tab=True):
        super().__init__(parent)
        self.consoles = []
        self.configuracao = None
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

        self.short_cuts.register_shortcut(self, Qt.CTRL | Qt.Key.Key_N, lambda: self.add_search_tab())

        self.short_cuts.register_shortcut(self, Qt.CTRL | Qt.Key.Key_H, lambda: (self.ui.tabs.addTab(
            HistoricoImplementation(self.ui.tabs, self).ui.historic, "Histórico"), self.ui.tabs.setTabsClosable(True)))

        self.short_cuts.register_shortcut(self, Qt.CTRL | Qt.Key.Key_D, lambda: (self.ui.tabs.addTab(
            DownloadImplementation(self.ui.tabs, self).ui.downloads, "Downloads"), self.ui.tabs.setTabsClosable(True)))

        self.short_cuts.register_shortcut(self, Qt.CTRL | Qt.Key.Key_F, lambda: self.find_in_page_short_cut())
    
        self.short_cuts.register_shortcut(self, "Ctrl+Shift+i", lambda: self.console_page())
        
        self.short_cuts.register_shortcut(self, "Ctrl+Shift+c", lambda: self.config_page())

        # Ctrl+T: nova aba | Ctrl+W: fechar aba atual (padrão de navegador)
        self.short_cuts.register_shortcut(self, Qt.CTRL | Qt.Key.Key_T, lambda: self.add_search_tab())
        self.short_cuts.register_shortcut(self, Qt.CTRL | Qt.Key.Key_W, lambda: self.close_current_tab())

        # Botão "+" visível para abrir nova aba, ao lado das abas.
        self._new_tab_button = QPushButton("+")
        self._new_tab_button.setFixedSize(28, 28)
        self._new_tab_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._new_tab_button.setToolTip("Nova aba (Ctrl+T)")
        self._new_tab_button.setStyleSheet(
            "QPushButton { border: none; font-size: 18px; font-weight: bold; }"
            "QPushButton:hover { background-color: lightgray; border-radius: 14px; }")
        self._new_tab_button.clicked.connect(self.add_search_tab)
        self.ui.tabs.setCornerWidget(self._new_tab_button, Qt.Corner.TopRightCorner)

        # Toolbar de navegação a NÍVEL DE JANELA, que controla sempre a aba atual
        # (substitui a barra repetida em cada aba).
        self._build_window_toolbar()
        self.ui.tabs.currentChanged.connect(lambda _i: self.sync_toolbar())

    def _build_window_toolbar(self):
        bar = QWidget()
        lay = QHBoxLayout(bar)
        lay.setContentsMargins(6, 4, 6, 4)
        lay.setSpacing(4)

        def mkbtn(icon_path, tip, slot):
            b = QPushButton()
            b.setIcon(QIcon(icon_path))
            b.setFixedSize(30, 30)
            b.setToolTip(tip)
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.setStyleSheet("QPushButton { border: none; border-radius: 15px; }"
                            "QPushButton:hover { background-color: lightgray; }")
            b.clicked.connect(slot)
            return b

        self.tb_back = mkbtn("figs/l-arrow.png", "Voltar", self._nav_back)
        self.tb_forward = mkbtn("figs/r-arrow.png", "Avançar", self._nav_forward)
        self.tb_reload = mkbtn("figs/t-arrow.png", "Recarregar", self.reload_page)
        self.tb_home = mkbtn("figs/site.png", "Página inicial", self._nav_home)
        self.tb_url = QLineEdit()
        self.tb_url.setPlaceholderText("Pesquise ou digite uma URL")
        self.tb_url.setStyleSheet(
            "QLineEdit { border: 1px solid #ccc; border-radius: 15px; padding: 4px 10px; }")
        self.tb_url.returnPressed.connect(self._nav_go)
        self.tb_fav = mkbtn("figs/star_out.png", "Favoritar", self._toolbar_fav)
        self.tb_download = mkbtn("figs/download.png", "Downloads", self._toolbar_downloads)
        self.tb_options = mkbtn("figs/dotdotdot.png", "Opções", self._toolbar_options)

        for w in (self.tb_back, self.tb_forward, self.tb_reload, self.tb_home):
            lay.addWidget(w)
        lay.addWidget(self.tb_url)
        for w in (self.tb_fav, self.tb_download, self.tb_options):
            lay.addWidget(w)

        self.ui.verticalLayout_2.insertWidget(0, bar)
        self._window_toolbar = bar

    # --- helpers da toolbar: sempre operam na aba atual ---
    def current_impl(self):
        w = self.ui.tabs.currentWidget()
        return getattr(w, "implementation", None) if w else None

    def current_web_view(self):
        impl = self.current_impl()
        ui = getattr(impl, "ui", None)
        return getattr(ui, "webEngineView", None) if ui else None

    def _nav_back(self):
        v = self.current_web_view()
        if v:
            v.back()

    def _nav_forward(self):
        v = self.current_web_view()
        if v:
            v.forward()

    def _nav_home(self):
        v = self.current_web_view()
        if v:
            home = settings_app.value("GeneralSettings/HomePage",
                                      defaultValue="https://www.google.com/", type=str)
            v.load(QUrl(home))

    def _nav_go(self):
        impl = self.current_impl()
        if impl and hasattr(impl, "search"):
            impl.search(impl.ui.webEngineView, self.tb_url.text())

    def _toolbar_fav(self):
        impl = self.current_impl()
        if impl and hasattr(impl, "addfavoritie"):
            impl.addfavoritie()

    def _toolbar_downloads(self):
        impl = self.current_impl()
        if impl and hasattr(impl, "open_dialog_download"):
            impl.open_dialog_download()

    def _toolbar_options(self):
        impl = self.current_impl()
        if impl and hasattr(impl, "open_dialog_ops"):
            impl.open_dialog_ops()

    def sync_toolbar(self, impl=None):
        """Reflete o estado da aba atual na toolbar. `impl`, se passado, só
        atualiza quando for a aba atual (evita uma aba de fundo mexer na barra)."""
        if not hasattr(self, "tb_url"):
            return
        if impl is not None and impl is not self.current_impl():
            return
        v = self.current_web_view()
        has_view = v is not None
        for b in (self.tb_reload, self.tb_home, self.tb_fav, self.tb_download, self.tb_options):
            b.setEnabled(has_view)
        self.tb_url.setEnabled(has_view)
        if has_view:
            self.tb_back.setEnabled(v.history().canGoBack())
            self.tb_forward.setEnabled(v.history().canGoForward())
            self.tb_url.setText(v.url().toString())
            self.tb_url.setCursorPosition(0)
        else:
            self.tb_back.setEnabled(False)
            self.tb_forward.setEnabled(False)
            self.tb_url.clear()

    def add_search_tab(self):
        """Cria uma aba de navegação, foca nela e devolve a implementação."""
        tab = DefaultSearchPageImplementation(self.ui.tabs, self)
        index = self.ui.tabs.addTab(tab.ui.page, "Nova Página")
        self.ui.tabs.setTabsClosable(True)
        self.ui.tabs.setCurrentIndex(index)
        return tab

    def close_current_tab(self):
        index = self.ui.tabs.currentIndex()
        if index >= 0:
            self.close_tab(index)

    def config_page(self):
        if not self.configuracao:
            self.configuracao = Configuracoes()
            self.configuracao.load_ini_file(self.configuracao.default_path)
            self.configuracao.show()
        else:
            self.configuracao.show()
            
    
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
        tabs = self.ui.tabs.count()
        tab = self.ui.tabs.widget(index)
        if tabs > 1:
            self.ui.tabs.removeTab(index)
            self._dispose_tab(tab)
            QCoreApplication.processEvents()
            if self.ui.tabs.count() == 1:
                self.ui.tabs.setTabsClosable(False)
        else:
            self.ui.tabs.setTabsClosable(False)

    @staticmethod
    def _dispose_tab(tab) -> None:
        """Desconecta sinais e agenda a remoção de uma aba com segurança."""
        if not tab:
            return
        impl = getattr(tab, "implementation", None)
        if impl is not None:
            try:
                impl.disconnect_signals()
            except Exception:
                pass
            impl.deleteLater()

    def closeEvent(self, event):
        # Itera de trás para frente: remover por índice crescente pula widgets.
        for i in reversed(range(self.ui.tabs.count())):
            tab = self.ui.tabs.widget(i)
            self.ui.tabs.removeTab(i)
            self._dispose_tab(tab)
        QCoreApplication.processEvents()
        for console in self.consoles:
            try:
                console.close()
            except Exception:
                pass
        self.consoles.clear()
        QCoreApplication.processEvents()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Main()
    ShortcutManager().shortcuts[Qt.CTRL | Qt.Key.Key_N].activated.emit()
    widget.show()
    sys.exit(app.exec())
