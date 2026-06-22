"""Tela de configurações do navegador.

Substitui o antigo editor genérico de INI (exemplo "Settings Editor" do Qt) por
preferências de verdade, gravadas em ``settings_app`` (configs/config.conf).

Mantém o nome ``Configuracoes``, o atributo ``default_path`` e o método
``load_ini_file`` para continuar compatível com main.py.
"""
import os

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QCheckBox, QComboBox, QFileDialog, QFormLayout, QGroupBox,
                               QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget)

from configs.Config import settings_app

# (nome exibido, template de URL com {} no lugar da consulta)
SEARCH_ENGINES = [
    ("Google", "https://www.google.com/search?q={}"),
    ("Bing", "https://www.bing.com/search?q={}"),
    ("DuckDuckGo", "https://duckduckgo.com/?q={}"),
]
DEFAULT_HOME = "https://www.google.com/"
DEFAULT_SEARCH = SEARCH_ENGINES[0][1]


def _get_bool(key, default):
    return settings_app.value(f"GeneralSettings/{key}", defaultValue=default, type=bool)


def _get_str(key, default):
    return settings_app.value(f"GeneralSettings/{key}", defaultValue=default, type=str)


class Configuracoes(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.default_path = os.path.join(".", "configs", "config.conf")
        self.setWindowTitle("Configurações")
        icon = QIcon()
        icon.addFile("./figs/config.png", QSize(), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.resize(540, 540)
        self._build_ui()
        self.load_ini_file()

    def _build_ui(self):
        root = QVBoxLayout(self)

        geral = QGroupBox("Geral")
        form = QFormLayout(geral)
        self.home_edit = QLineEdit()
        self.home_edit.setPlaceholderText("https://...")
        form.addRow("Página inicial:", self.home_edit)
        self.search_combo = QComboBox()
        for name, _tpl in SEARCH_ENGINES:
            self.search_combo.addItem(name)
        form.addRow("Mecanismo de busca:", self.search_combo)
        root.addWidget(geral)

        downloads = QGroupBox("Downloads")
        dlf = QFormLayout(downloads)
        self.ask_where = QCheckBox("Perguntar onde salvar cada download")
        dlf.addRow(self.ask_where)
        path_row = QHBoxLayout()
        self.download_path = QLineEdit()
        browse = QPushButton("Procurar...")
        browse.clicked.connect(self._browse_download_path)
        path_row.addWidget(self.download_path)
        path_row.addWidget(browse)
        dlf.addRow("Pasta padrão:", path_row)
        root.addWidget(downloads)

        conteudo = QGroupBox("Conteúdo e privacidade")
        cf = QVBoxLayout(conteudo)
        self.js = QCheckBox("Habilitar JavaScript")
        self.darkmode = QCheckBox("Forçar modo escuro nos sites")
        self.plugins = QCheckBox("Habilitar plugins")
        self.gesture = QCheckBox("Exigir interação do usuário para tocar mídia (autoplay desligado)")
        for w in (self.js, self.darkmode, self.plugins, self.gesture):
            cf.addWidget(w)
        nota = QLabel("As opções de conteúdo passam a valer ao reiniciar o navegador.")
        nota.setStyleSheet("color: gray; font-style: italic;")
        cf.addWidget(nota)
        root.addWidget(conteudo)

        root.addStretch(1)

        btns = QHBoxLayout()
        btns.addStretch(1)
        cancel = QPushButton("Cancelar")
        cancel.clicked.connect(self.close)
        save = QPushButton("Salvar")
        save.setDefault(True)
        save.clicked.connect(self._save)
        btns.addWidget(cancel)
        btns.addWidget(save)
        root.addLayout(btns)

    def _browse_download_path(self):
        start = self.download_path.text() or os.path.abspath(".")
        chosen = QFileDialog.getExistingDirectory(self, "Pasta padrão de downloads", start)
        if chosen:
            self.download_path.setText(chosen)

    def load_ini_file(self, path=None):
        # `path` mantido por compatibilidade com main.py; settings_app já aponta
        # o arquivo de configuração.
        self.home_edit.setText(_get_str("HomePage", DEFAULT_HOME))
        current_tpl = _get_str("SearchEngine", DEFAULT_SEARCH)
        idx = next((i for i, (_n, tpl) in enumerate(SEARCH_ENGINES) if tpl == current_tpl), 0)
        self.search_combo.setCurrentIndex(idx)
        self.ask_where.setChecked(_get_bool("AskWhereSaveDownload", False))
        self.download_path.setText(_get_str("DownloadPath", os.path.abspath("./downloads")))
        self.js.setChecked(_get_bool("JavascriptEnabled", True))
        self.darkmode.setChecked(_get_bool("ForceDarkMode", False))
        self.plugins.setChecked(_get_bool("PluginsEnabled", True))
        self.gesture.setChecked(_get_bool("PlaybackRequiresUserGesture", True))

    def _save(self):
        s = settings_app
        s.setValue("GeneralSettings/HomePage", self.home_edit.text().strip() or DEFAULT_HOME)
        s.setValue("GeneralSettings/SearchEngine",
                   SEARCH_ENGINES[self.search_combo.currentIndex()][1])
        s.setValue("GeneralSettings/AskWhereSaveDownload", self.ask_where.isChecked())
        s.setValue("GeneralSettings/DownloadPath", self.download_path.text().strip())
        s.setValue("GeneralSettings/JavascriptEnabled", self.js.isChecked())
        s.setValue("GeneralSettings/ForceDarkMode", self.darkmode.isChecked())
        s.setValue("GeneralSettings/PluginsEnabled", self.plugins.isChecked())
        s.setValue("GeneralSettings/PlaybackRequiresUserGesture", self.gesture.isChecked())
        s.sync()
        self.close()
