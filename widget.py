# This Python file uses the following encoding: utf-8
import datetime
import os.path
import re
import sys

import requests
from PySide6.QtCore import (QFile)
from PySide6.QtCore import (QRect,
                            QSize, QUrl, Qt)
from PySide6.QtGui import (QCursor,
                           QFont, QIcon)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QGroupBox, QHBoxLayout,
                               QLabel, QLayout, QLineEdit, QPushButton,
                               QScrollArea, QSizePolicy, QTabWidget,
                               QVBoxLayout, QWidget)
from PySide6.QtWidgets import (QDialog, QFileDialog)

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
        self.ui.webEngineView.load(self.ui.url.text())
        self.ui.webEngineView.urlChanged.connect(
            lambda url, url_input=self.ui.url: self.update_url(url_input, url))
        self.ui.webEngineView.titleChanged.connect(
            lambda title, index=self.ui.tabs.currentIndex(), tabs=self.ui.tabs: self.update_title(title, index, tabs))
        self.ui.options.clicked.connect(self.open_dialog_ops)
        self.ui.download_buttton.clicked.connect(self.open_dialog_download)
        self.ui.options_donwload.clicked.connect(self.open_dialog_ops)
        self.ui.tabs.tabCloseRequested.connect(self.close_tab)
        self.ui.url.returnPressed.connect(
            lambda web=self.ui.webEngineView, search=self.ui.url: self.search(web_loader=web,
                                                                              search_text=search.text()))
        self.ui.arrow_left_back.clicked.connect(lambda: self.ui.stacked_pages.setCurrentIndex(0))
        self.ui.webEngineView.page().profile().downloadRequested.connect(self.download_file)

    def update_url(self, url_input: QLineEdit, url: QUrl):
        url_input.setText(url.toString())
        url_input.setCursorPosition(0)

    def limit_string(self, text, limit):
        if len(text) > limit:
            return text[:limit - 3] + "..."  # Corta o texto e adiciona "..." no final
        return text

    def update_title(self, text: str, index: int, tabs: QTabWidget):
        tabs.setTabText(index, self.limit_string(text, 30))

    def is_valid_url(self, url_string):
        url_pattern = re.compile(
            r'^(https?:\/\/)?' +  # validar protocolo
            r'((([a-z\d]([a-z\d-]*[a-z\d])*)\.)+[a-z]{2,}|' +  # validar nome de domínio
            r'((\d{1,3}\.){3}\d{1,3}))' +  # validar OU endereço IP (v4)
            r'(:\d+)?(\/[-a-z\d%_.~+]*)*' +  # validar porta e caminho
            r'(\?[;&a-z\d%_.~+=-]*)?' +  # validar string de consulta
            r'(#[-a-z\d_]*)?$',  # validar fragmento
            re.IGNORECASE  # ignora case sensitivity
        )
        return bool(re.match(url_pattern, url_string))

    def search(self, web_loader: QWebEngineView, search_text: str):
        if self.is_valid_url(search_text):
            url = f"{search_text}"

            if 'https://' not in search_text:
                url = f"https://{search_text}"

            web_loader.load(QUrl(url))
            return
        search_url = "https://www.google.com/search?q=" + search_text.replace(" ", "+")
        web_loader.load(QUrl(search_url))

    def close_tab(self, index):
        tabs = self.ui.tabs.count()
        if tabs > 1:
            self.ui.tabs.removeTab(index)
            tabs = self.ui.tabs.count()
            if tabs == 1:
                self.ui.tabs.setTabsClosable(False)
        else:
            self.ui.tabs.setTabsClosable(False)

    def open_dialog_ops(self):
        loader = QUiLoader()
        ui_file = QFile("dialog_ops.ui")
        ui_file.open(QFile.ReadOnly)
        dialog_widget = loader.load(ui_file)
        ui_file.close()

        add_page = dialog_widget.findChild(QPushButton, 'add_page')
        add_page.clicked.connect(self.add_new_page)

        download_page = dialog_widget.findChild(QPushButton, 'donwloads_page')
        download_page.clicked.connect(lambda: self.ui.stacked_pages.setCurrentIndex(1))

        # Criar o diálogo
        dialog = QDialog(self)
        dialog.setWindowTitle("Opções")
        dialog.setModal(False)  # Permitir interação com a janela principal
        layout = QVBoxLayout(dialog)
        layout.addWidget(dialog_widget)

        # Exibir o diálogo modalmente
        dialog.exec()

    def open_dialog_download(self):
        loader = QUiLoader()
        ui_file = QFile("dialog_downloads.ui")
        ui_file.open(QFile.ReadOnly)
        dialog_widget = loader.load(ui_file)
        ui_file.close()

        # Criar o diálogo
        dialog = QDialog(self)
        dialog.setWindowTitle("Opções")
        dialog.setModal(False)  # Permitir interação com a janela principal
        layout = QVBoxLayout(dialog)
        layout.addWidget(dialog_widget)

        # Exibir o diálogo modalmente
        dialog.exec()

    def download_file(self, download_item):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        folder_path = QFileDialog.getExistingDirectory(self, "Selecionar pasta de destino", options=options)
        suggested_file_name = download_item.suggestedFileName()
        file_name = os.path.join(folder_path, suggested_file_name)

        with requests.get(download_item.url().toString(), stream=True) as r:
            # Verificando se a requisição foi bem sucedida
            if r.status_code == 200:
                total_size = int(r.headers.get('content-length', 0))  # Tamanho total do arquivo
                bytes_so_far = 0  # Inicializando a quantidade de bytes baixados
                chunk_size = 8192  # Tamanho do chunk

                # Abrindo o arquivo para escrita em modo binário
                with open(file_name, 'wb') as f:
                    # Iterando sobre os chunks recebidos e escrevendo no arquivo
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)
                            bytes_so_far += len(chunk)
                            # Calculando a porcentagem de progresso
                            if total_size > 0:  # Verificando se o tamanho total é conhecido
                                percent = (bytes_so_far / total_size) * 100
                                print(f'Progresso: {percent:.2f}%')
                            else:
                                print('Progresso: Tamanho total desconhecido')
                self.register_download_history(suggested_file_name, folder_path, 'Concluido')
                print(f'Download completo: {file_name}')
            else:
                self.register_download_history(suggested_file_name, folder_path, 'Erro')
                print('Falha ao baixar o arquivo. Código de status:', r.status_code)

    def register_download_history(self, suggested_file_name: str, folder_path: str, status: str):
        with open(os.path.abspath(os.path.join('.', 'configs', 'download_history.json')), 'rb') as file:
            json_file = {}
            if not file.read():
                json_file = {"Files": [{"name": f"{suggested_file_name}", "path": f"{folder_path}",
                                        "download_time": f"{datetime.datetime.now()}", "status": f"{status}"}]}
            else:
                json_file["Files"].append(
                    {"name": f"{suggested_file_name}", "path": f"{folder_path}",
                     "download_time": f"{datetime.datetime.now()}", "status": f"{status}"})

            with open(os.path.abspath(os.path.join('.', 'configs', 'download_history.json')), 'wb') as file2:
                file2.write(str(json_file).encode('utf8'))

    def add_download_history(self):
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
        name_arquivo.setText("Nome: ")
        name_arquivo.setObjectName(u"name_arquivo")
        sizePolicy.setHeightForWidth(name_arquivo.sizePolicy().hasHeightForWidth())
        name_arquivo.setSizePolicy(sizePolicy)

        verticalLayout_11.addWidget(name_arquivo)

        path_arquivo = QLabel(groupBox)
        path_arquivo.setText('Path:')
        path_arquivo.setObjectName(u"path_arquivo")
        sizePolicy.setHeightForWidth(path_arquivo.sizePolicy().hasHeightForWidth())
        path_arquivo.setSizePolicy(sizePolicy)
        path_arquivo.setStyleSheet(u"QLabel {\n"
                                        "	width: '100%';\n"
                                        "}")

        verticalLayout_11.addWidget(path_arquivo)

        status = QLabel(groupBox)
        status.setText("Status: ")
        status.setObjectName(u"status")
        sizePolicy.setHeightForWidth(status.sizePolicy().hasHeightForWidth())
        status.setSizePolicy(sizePolicy)

        verticalLayout_11.addWidget(status)

        open_in_explorer = QLabel(groupBox)
        open_in_explorer.setText('Abrir no explorer: ')
        open_in_explorer.setObjectName(u"open_in_explorer")
        sizePolicy.setHeightForWidth(open_in_explorer.sizePolicy().hasHeightForWidth())
        open_in_explorer.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(10)
        font.setBold(False)
        font.setUnderline(True)
        open_in_explorer.setFont(font)
        open_in_explorer.setCursor(QCursor(Qt.PointingHandCursor))

        verticalLayout_11.addWidget(open_in_explorer)

        verticalLayout_10.addWidget(groupBox)

        horizontalLayout_4.addWidget(group_dados)

        del_item = QPushButton(download_item)
        del_item.setObjectName(u"del_item")
        sizePolicy.setHeightForWidth(del_item.sizePolicy().hasHeightForWidth())
        del_item.setSizePolicy(sizePolicy)
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

        self.ui.verticalLayout_8.addWidget(download_item)

    def add_new_page(self):
        self.ui.tabs.setTabsClosable(True)
        page = QWidget()
        page.setObjectName(u"page")
        verticalLayout_3 = QVBoxLayout(page)
        verticalLayout_3.setObjectName(u"verticalLayout_3")
        verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        hot_bar = QGroupBox(page)
        hot_bar.setObjectName(u"hot_bar")
        hot_bar.setMaximumSize(QSize(16777215, 40))
        hot_bar.setStyleSheet(u"QGroupBox {\n"
                              "	border: none;\n"
                              "	margin: 0;\n"
                              "	padding: 0;\n"
                              "}")
        horizontalLayout = QHBoxLayout(hot_bar)
        horizontalLayout.setSpacing(0)
        horizontalLayout.setObjectName(u"horizontalLayout")
        horizontalLayout.setContentsMargins(0, 5, 0, 0)
        arrow_left = QPushButton(hot_bar)
        arrow_left.setObjectName(u"arrow_left")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(arrow_left.sizePolicy().hasHeightForWidth())
        arrow_left.setSizePolicy(sizePolicy)
        arrow_left.setMaximumSize(QSize(30, 30))
        arrow_left.setStyleSheet(u"QPushButton {\n"
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
        icon1 = QIcon()
        icon1.addFile(u"figs/109618.png", QSize(), QIcon.Normal, QIcon.Off)
        arrow_left.setIcon(icon1)

        horizontalLayout.addWidget(arrow_left)

        arrow_right = QPushButton(hot_bar)
        arrow_right.setObjectName(u"arrow_right")
        sizePolicy.setHeightForWidth(arrow_right.sizePolicy().hasHeightForWidth())
        arrow_right.setSizePolicy(sizePolicy)
        arrow_right.setMaximumSize(QSize(30, 30))
        arrow_right.setStyleSheet(u"QPushButton {\n"
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
        icon2 = QIcon()
        icon2.addFile(u"figs/r-arrow.png", QSize(), QIcon.Normal, QIcon.Off)
        arrow_right.setIcon(icon2)

        horizontalLayout.addWidget(arrow_right)

        url = QLineEdit(hot_bar)
        url.setText("https://www.google.com/")
        url.setObjectName(u"url")
        sizePolicy.setHeightForWidth(url.sizePolicy().hasHeightForWidth())
        url.setSizePolicy(sizePolicy)
        url.setStyleSheet(u"QLineEdit {\n"
                          "	border: none;\n"
                          "	border-radius: 15px;\n"
                          "	padding-left: 5px;\n"
                          "	padding-right: 5px;\n"
                          "}")

        horizontalLayout.addWidget(url)

        download_buttton = QPushButton(hot_bar)
        download_buttton.setObjectName(u"download_buttton")
        sizePolicy.setHeightForWidth(download_buttton.sizePolicy().hasHeightForWidth())
        download_buttton.setSizePolicy(sizePolicy)
        download_buttton.setCursor(QCursor(Qt.PointingHandCursor))
        download_buttton.clicked.connect(self.open_dialog_download)
        download_buttton.setMaximumSize(QSize(30, 30))
        download_buttton.setStyleSheet(u"QPushButton {\n"
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
        icon3 = QIcon()
        icon3.addFile(u"figs/download.png", QSize(), QIcon.Normal, QIcon.Off)
        download_buttton.setIcon(icon3)

        horizontalLayout.addWidget(download_buttton)

        options = QPushButton(hot_bar)
        options.setObjectName(u"options")
        sizePolicy.setHeightForWidth(options.sizePolicy().hasHeightForWidth())
        options.setSizePolicy(sizePolicy)
        options.clicked.connect(self.open_dialog_ops)
        options.setMaximumSize(QSize(30, 30))
        options.setCursor(QCursor(Qt.PointingHandCursor))
        options.setStyleSheet(u"QPushButton {\n"
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
        icon3 = QIcon()
        icon3.addFile(u"figs/61140.png", QSize(), QIcon.Normal, QIcon.Off)
        options.setIcon(icon3)

        horizontalLayout.addWidget(options)

        verticalLayout_3.addWidget(hot_bar)

        webEngineView = QWebEngineView(page)
        webEngineView.setObjectName(u"webEngineView")
        webEngineView.setUrl(QUrl(u"about:blank"))

        verticalLayout_3.addWidget(webEngineView)

        webEngineView.load("https://www.google.com/")
        url.returnPressed.connect(
            lambda web=webEngineView, search=url: self.search(web_loader=web, search_text=search.text()))
        webEngineView.page().profile().downloadRequested.connect(self.download_file)
        self.ui.tabs.addTab(page, self.limit_string(webEngineView.url().toString(), 30))

        webEngineView.urlChanged.connect(
            lambda site, url_input=url: self.update_url(url_input, site))
        webEngineView.titleChanged.connect(
            lambda title, index=self.ui.tabs.indexOf(page), tabs=self.ui.tabs: self.update_title(title, index, tabs))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    widget.add_download_history()
    sys.exit(app.exec())
