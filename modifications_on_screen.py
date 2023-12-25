import datetime

from PySide6.QtCore import (QFile)
from PySide6.QtCore import (QSize, QUrl, Qt)
from PySide6.QtGui import (QCursor, QDesktopServices,
                           QFont, QIcon, QPixmap)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QDialog, QLabel)
from PySide6.QtWidgets import (QGroupBox, QHBoxLayout, QCommandLinkButton,
                               QLineEdit, QSizePolicy, QWidget, QProgressBar, QLayout)
from PySide6.QtWidgets import (QPushButton,
                               QVBoxLayout)

from register_recover import recover_download_historic, remove_download_historic_item, recover_historic, \
    remove_historic_item, recover_adjacent_historic


def open_dialog_ops(main_window, view=True):
    if not main_window.dialog_ops:
        loader = QUiLoader()
        ui_file = QFile("dialog_ops.ui")
        ui_file.open(QFile.ReadOnly)
        dialog_widget = loader.load(ui_file)
        ui_file.close()

        add_page = dialog_widget.findChild(QPushButton, 'add_page')
        add_page.clicked.connect(lambda: add_new_page(main_window))

        download_page = dialog_widget.findChild(QPushButton, 'donwloads_page')
        download_page.clicked.connect(lambda: main_window.ui.stacked_pages.setCurrentIndex(1))

        historic_page = dialog_widget.findChild(QPushButton, 'historic_page')
        historic_page.clicked.connect(lambda: main_window.ui.stacked_pages.setCurrentIndex(2))

        # Criar o diálogo
        dialog = QDialog(main_window)
        dialog.setWindowTitle("Opções")
        dialog.setModal(True)  # Permitir interação com a janela principal
        layout = QVBoxLayout(dialog)
        layout.addWidget(dialog_widget)

        # Exibir o diálogo modalmente
        main_window.dialog_ops = {"fields": dialog_widget, "view": dialog}
        if view:
            dialog.exec()
    else:
        main_window.dialog_ops['view'].exec()


def open_dialog_download(main_window, view=True):
    if not main_window.dialog_download:
        loader = QUiLoader()
        ui_file = QFile("dialog_downloads.ui")
        ui_file.open(QFile.ReadOnly)
        dialog_widget = loader.load(ui_file)
        ui_file.close()

        # Criar o diálogo
        dialog = QDialog(main_window)
        dialog.setWindowTitle("Downloads")
        dialog.setModal(True)  # Permitir interação com a janela principal
        layout = QVBoxLayout(dialog)
        layout.addWidget(dialog_widget)

        # Exibir o diálogo modalmente
        main_window.dialog_download = {"fields": dialog_widget, "view": dialog}
        if view:
            dialog.exec()
    else:
        main_window.dialog_download['view'].exec()


def add_new_page(main_window):
    main_window.ui.tabs.setTabsClosable(True)
    page = QWidget()
    page.setObjectName(u"page")
    container_tab = QVBoxLayout(page)
    container_tab.setObjectName(u"container_tab")
    container_tab.setContentsMargins(0, 0, 0, 0)
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
    arrow_left_historic = QPushButton(hot_bar)
    arrow_left_historic.setObjectName(u"arrow_left_historic")
    sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(arrow_left_historic.sizePolicy().hasHeightForWidth())
    arrow_left_historic.setSizePolicy(sizePolicy)
    arrow_left_historic.setMaximumSize(QSize(30, 30))
    arrow_left_historic.setStyleSheet(u"QPushButton {\n"
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
    arrow_left_historic.setIcon(icon1)

    horizontalLayout.addWidget(arrow_left_historic)

    arrow_right_historic = QPushButton(hot_bar)
    arrow_right_historic.setObjectName(u"arrow_right_historic")
    sizePolicy.setHeightForWidth(arrow_right_historic.sizePolicy().hasHeightForWidth())
    arrow_right_historic.setSizePolicy(sizePolicy)
    arrow_right_historic.setMaximumSize(QSize(30, 30))
    arrow_right_historic.setStyleSheet(u"QPushButton {\n"
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
    arrow_right_historic.setIcon(icon2)

    horizontalLayout.addWidget(arrow_right_historic)

    main_window.arrow_left_historic.clicked.connect(
        lambda: load_direction_specific_historic(main_window, main_window.site_atual['name'], main_window.site_atual['date_time'],
                                                 'ant'))
    main_window.arrow_right_historic.clicked.connect(
        lambda: load_direction_specific_historic(main_window, main_window.site_atual['name'], main_window.site_atual['date_time'],
                                                 'prox'))

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
    download_buttton.clicked.connect(lambda: open_dialog_download(main_window))
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
    options.clicked.connect(lambda: open_dialog_ops(main_window))
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

    container_tab.addWidget(hot_bar)

    webEngineView = QWebEngineView(page)
    webEngineView.setObjectName(u"webEngineView")
    webEngineView.setUrl(QUrl(u"about:blank"))

    container_tab.addWidget(webEngineView)

    webEngineView.load("https://www.google.com/")
    url.returnPressed.connect(
        lambda web=webEngineView, search=url: main_window.search(web_loader=web, search_text=search.text()))
    webEngineView.page().profile().downloadRequested.connect(main_window.download_file)
    main_window.ui.tabs.addTab(page, main_window.limit_string(webEngineView.url().toString(), 30))

    webEngineView.urlChanged.connect(
        lambda site, url_input=url: main_window.update_url(url_input, site))
    webEngineView.titleChanged.connect(
        lambda title, index=main_window.ui.tabs.indexOf(page), tabs=main_window.ui.tabs: main_window.update_title(title,
                                                                                                                  index,
                                                                                                                  tabs))


def add_download_history(main_window, download_data):
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
                                                                   main_window.ui.container_downloads_itens_page))
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

    main_window.ui.container_downloads_itens_page.insertWidget(download_item)


def add_download_notification(main_windows, download_data, show_progress=True) -> QProgressBar:
    if main_windows:
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

        main_windows['fields'].findChild(QLayout, 'container_download_notifications').insertWidget(0,
                                                                                                   download_item_list)

        return progressBar


def open_historic_site(main_window, site):
    add_new_page(main_window)
    last_page = main_window.ui.tabs.count() - 1
    layout = main_window.ui.tabs.widget(last_page)
    webview = layout.findChildren(QWebEngineView)
    if webview:
        webview[0].load(site)


def add_historic_item(main_window, historic_data):
    if main_window:
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
        open_site.clicked.connect(lambda: open_historic_site(main_window, historic_data['name']))
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
            lambda: remove_historic_item(site=historic_data['name'], date_time=historic_data['date_time'],
                                         remove_view=True, widget=historic_item,
                                         layout=main_window.ui.container_historic_page))
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
                                        "	transition: 1s;\n"
                                        "	transition-delay: 1s;\n"
                                        "	background-color: lightgray;\n"
                                        "}")
        del_item_historic.setIcon(icon6)

        horizontalLayout_7.addWidget(del_item_historic)

        main_window.ui.container_historic_page.insertWidget(0, historic_item)


def load_download_historic(main_window):
    layout = main_window.ui.container_downloads_itens_page.layout()
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()
    history = recover_download_historic()

    if bool(history):
        for download in history['Files']:
            add_download_history(main_window=main_window, download_data=download)


def load_download_notificatios(main_window):
    layout = main_window['fields'].findChild(QLayout, 'container_download_notifications')
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()
    history = recover_download_historic(file_saved='download_notifications.json')
    if bool(history):
        for download in history['Files']:
            add_download_notification(main_windows=main_window, download_data=download, show_progress=False)


def load_historic(main_window):
    layout = main_window.ui.container_historic_page.layout()
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()
    history = recover_historic()

    if bool(history):
        for site in history['Sites']:
            add_historic_item(main_window=main_window, historic_data=site)


def load_direction_specific_historic(main_window, site: str, date_time: str, direc: str):
    tab = main_window.ui.tabs.currentWidget()
    site_procurado = recover_adjacent_historic(site, date_time, direc)
    if bool(site_procurado):
        webview = tab.findChildren(QWebEngineView)
        print(webview)
        if webview:
            webview[0].load(site_procurado)
