# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QCommandLinkButton, QGroupBox,
    QHBoxLayout, QLabel, QLayout, QLineEdit,
    QPushButton, QScrollArea, QSizePolicy, QStackedWidget,
    QTabWidget, QVBoxLayout, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(800, 600)
        icon = QIcon()
        icon.addFile(u"figs/icon.png", QSize(), QIcon.Normal, QIcon.Off)
        Widget.setWindowIcon(icon)
        self.verticalLayout_2 = QVBoxLayout(Widget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.stacked_pages = QStackedWidget(Widget)
        self.stacked_pages.setObjectName(u"stacked_pages")
        self.stacked_pages.setEnabled(True)
        self.default_page = QWidget()
        self.default_page.setObjectName(u"default_page")
        self.default_page.setEnabled(True)
        self.verticalLayout_4 = QVBoxLayout(self.default_page)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.tabs = QTabWidget(self.default_page)
        self.tabs.setObjectName(u"tabs")
        self.tabs.setEnabled(True)
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setElideMode(Qt.ElideMiddle)
        self.tabs.setTabsClosable(False)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.container_tab = QVBoxLayout(self.page)
        self.container_tab.setObjectName(u"container_tab")
        self.container_tab.setContentsMargins(0, 0, 0, 0)
        self.hot_bar = QGroupBox(self.page)
        self.hot_bar.setObjectName(u"hot_bar")
        self.hot_bar.setMinimumSize(QSize(0, 40))
        self.hot_bar.setMaximumSize(QSize(16777215, 40))
        self.hot_bar.setStyleSheet(u"QGroupBox {\n"
"	border: none;\n"
"	margin: 0;\n"
"	padding: 0;\n"
"}")
        self.horizontalLayout = QHBoxLayout(self.hot_bar)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 5, 0, 0)
        self.arrow_left_historic = QPushButton(self.hot_bar)
        self.arrow_left_historic.setObjectName(u"arrow_left_historic")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.arrow_left_historic.sizePolicy().hasHeightForWidth())
        self.arrow_left_historic.setSizePolicy(sizePolicy)
        self.arrow_left_historic.setMaximumSize(QSize(30, 30))
        self.arrow_left_historic.setStyleSheet(u"QPushButton {\n"
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
        self.arrow_left_historic.setIcon(icon1)

        self.horizontalLayout.addWidget(self.arrow_left_historic)

        self.arrow_right_historic = QPushButton(self.hot_bar)
        self.arrow_right_historic.setObjectName(u"arrow_right_historic")
        sizePolicy.setHeightForWidth(self.arrow_right_historic.sizePolicy().hasHeightForWidth())
        self.arrow_right_historic.setSizePolicy(sizePolicy)
        self.arrow_right_historic.setMaximumSize(QSize(30, 30))
        self.arrow_right_historic.setStyleSheet(u"QPushButton {\n"
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
        self.arrow_right_historic.setIcon(icon2)

        self.horizontalLayout.addWidget(self.arrow_right_historic)

        self.url = QLineEdit(self.hot_bar)
        self.url.setObjectName(u"url")
        sizePolicy.setHeightForWidth(self.url.sizePolicy().hasHeightForWidth())
        self.url.setSizePolicy(sizePolicy)
        self.url.setStyleSheet(u"QLineEdit {\n"
"	border: none;\n"
"	border-radius: 15px;\n"
"	padding-left: 5px;\n"
"	padding-right: 5px;\n"
"}")

        self.horizontalLayout.addWidget(self.url)

        self.download_buttton = QPushButton(self.hot_bar)
        self.download_buttton.setObjectName(u"download_buttton")
        sizePolicy.setHeightForWidth(self.download_buttton.sizePolicy().hasHeightForWidth())
        self.download_buttton.setSizePolicy(sizePolicy)
        self.download_buttton.setMaximumSize(QSize(30, 30))
        self.download_buttton.setCursor(QCursor(Qt.PointingHandCursor))
        self.download_buttton.setStyleSheet(u"QPushButton {\n"
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
        self.download_buttton.setIcon(icon3)

        self.horizontalLayout.addWidget(self.download_buttton)

        self.options = QPushButton(self.hot_bar)
        self.options.setObjectName(u"options")
        sizePolicy.setHeightForWidth(self.options.sizePolicy().hasHeightForWidth())
        self.options.setSizePolicy(sizePolicy)
        self.options.setMaximumSize(QSize(30, 30))
        self.options.setCursor(QCursor(Qt.PointingHandCursor))
        self.options.setStyleSheet(u"QPushButton {\n"
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
        icon4 = QIcon()
        icon4.addFile(u"figs/61140.png", QSize(), QIcon.Normal, QIcon.Off)
        self.options.setIcon(icon4)

        self.horizontalLayout.addWidget(self.options)


        self.container_tab.addWidget(self.hot_bar)

        self.webEngineView = QWebEngineView(self.page)
        self.webEngineView.setObjectName(u"webEngineView")
        sizePolicy.setHeightForWidth(self.webEngineView.sizePolicy().hasHeightForWidth())
        self.webEngineView.setSizePolicy(sizePolicy)
        self.webEngineView.setUrl(QUrl(u"about:blank"))

        self.container_tab.addWidget(self.webEngineView)

        self.tabs.addTab(self.page, "")

        self.verticalLayout_4.addWidget(self.tabs)

        self.stacked_pages.addWidget(self.default_page)
        self.downloads = QWidget()
        self.downloads.setObjectName(u"downloads")
        self.verticalLayout_6 = QVBoxLayout(self.downloads)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.container_principal = QVBoxLayout()
        self.container_principal.setSpacing(0)
        self.container_principal.setObjectName(u"container_principal")
        self.hotbar = QGroupBox(self.downloads)
        self.hotbar.setObjectName(u"hotbar")
        self.hotbar.setMinimumSize(QSize(0, 40))
        self.hotbar.setMaximumSize(QSize(16777215, 120))
        self.hotbar.setStyleSheet(u"QGroupBox {\n"
"	border: none;\n"
"	margin: 0;\n"
"	padding: 0;\n"
"}")
        self.horizontalLayout_3 = QHBoxLayout(self.hotbar)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.arrow_left_back = QPushButton(self.hotbar)
        self.arrow_left_back.setObjectName(u"arrow_left_back")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.arrow_left_back.sizePolicy().hasHeightForWidth())
        self.arrow_left_back.setSizePolicy(sizePolicy1)
        self.arrow_left_back.setMaximumSize(QSize(30, 30))
        self.arrow_left_back.setStyleSheet(u"QPushButton {\n"
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
        self.arrow_left_back.setIcon(icon1)

        self.horizontalLayout_2.addWidget(self.arrow_left_back)

        self.lineEdit = QLineEdit(self.hotbar)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(0, 30))
        self.lineEdit.setStyleSheet(u"QLineEdit {\n"
"	border: none;\n"
"	border-radius: 15px;\n"
"	padding-left: 10px;\n"
"	padding-right: 10px;\n"
"}")

        self.horizontalLayout_2.addWidget(self.lineEdit)

        self.options_donwload = QPushButton(self.hotbar)
        self.options_donwload.setObjectName(u"options_donwload")
        sizePolicy1.setHeightForWidth(self.options_donwload.sizePolicy().hasHeightForWidth())
        self.options_donwload.setSizePolicy(sizePolicy1)
        self.options_donwload.setMaximumSize(QSize(33, 30))
        self.options_donwload.setCursor(QCursor(Qt.PointingHandCursor))
        self.options_donwload.setStyleSheet(u"QPushButton {\n"
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
        self.options_donwload.setIcon(icon4)

        self.horizontalLayout_2.addWidget(self.options_donwload)


        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)


        self.container_principal.addWidget(self.hotbar)

        self.scrollAreaDownloads = QScrollArea(self.downloads)
        self.scrollAreaDownloads.setObjectName(u"scrollAreaDownloads")
        self.scrollAreaDownloads.setStyleSheet(u"QScrollArea {\n"
"	border: none;\n"
"}")
        self.scrollAreaDownloads.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.scrollAreaDownloads.setWidgetResizable(True)
        self.scrollAreaDownloadContents = QWidget()
        self.scrollAreaDownloadContents.setObjectName(u"scrollAreaDownloadContents")
        self.scrollAreaDownloadContents.setGeometry(QRect(0, 0, 778, 538))
        sizePolicy.setHeightForWidth(self.scrollAreaDownloadContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaDownloadContents.setSizePolicy(sizePolicy)
        self.scrollAreaDownloadContents.setStyleSheet(u"")
        self.container_downloads_itens_page = QVBoxLayout(self.scrollAreaDownloadContents)
        self.container_downloads_itens_page.setObjectName(u"container_downloads_itens_page")
        self.container_downloads_itens_page.setSizeConstraint(QLayout.SetMinAndMaxSize)
        self.container_downloads_itens_page.setContentsMargins(-1, 20, -1, -1)
        self.download_item = QGroupBox(self.scrollAreaDownloadContents)
        self.download_item.setObjectName(u"download_item")
        sizePolicy.setHeightForWidth(self.download_item.sizePolicy().hasHeightForWidth())
        self.download_item.setSizePolicy(sizePolicy)
        self.download_item.setMinimumSize(QSize(400, 100))
        self.download_item.setMaximumSize(QSize(16777215, 100))
        self.download_item.setStyleSheet(u"QGroupBox {\n"
"	border: 1px solid lightgray;\n"
"	border-radius: 20px;\n"
"	width: 100%;\n"
"}")
        self.download_item.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.horizontalLayout_4 = QHBoxLayout(self.download_item)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.group_icon = QGroupBox(self.download_item)
        self.group_icon.setObjectName(u"group_icon")
        sizePolicy.setHeightForWidth(self.group_icon.sizePolicy().hasHeightForWidth())
        self.group_icon.setSizePolicy(sizePolicy)
        self.group_icon.setMinimumSize(QSize(60, 0))
        self.group_icon.setMaximumSize(QSize(60, 16777215))
        self.verticalLayout_5 = QVBoxLayout(self.group_icon)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.icon_item = QLabel(self.group_icon)
        self.icon_item.setObjectName(u"icon_item")
        sizePolicy.setHeightForWidth(self.icon_item.sizePolicy().hasHeightForWidth())
        self.icon_item.setSizePolicy(sizePolicy)

        self.verticalLayout_5.addWidget(self.icon_item)


        self.horizontalLayout_4.addWidget(self.group_icon)

        self.group_dados = QGroupBox(self.download_item)
        self.group_dados.setObjectName(u"group_dados")
        self.group_dados.setStyleSheet(u"QGroupBox {\n"
"	border: none;\n"
"	margin: 0;\n"
"	padding: 0;\n"
"}")
        self.verticalLayout_10 = QVBoxLayout(self.group_dados)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.groupBox = QGroupBox(self.group_dados)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setStyleSheet(u"")
        self.verticalLayout_11 = QVBoxLayout(self.groupBox)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(10, 0, 0, 0)
        self.name_arquivo = QLabel(self.groupBox)
        self.name_arquivo.setObjectName(u"name_arquivo")
        sizePolicy.setHeightForWidth(self.name_arquivo.sizePolicy().hasHeightForWidth())
        self.name_arquivo.setSizePolicy(sizePolicy)

        self.verticalLayout_11.addWidget(self.name_arquivo)

        self.path_arquivo = QLabel(self.groupBox)
        self.path_arquivo.setObjectName(u"path_arquivo")
        sizePolicy.setHeightForWidth(self.path_arquivo.sizePolicy().hasHeightForWidth())
        self.path_arquivo.setSizePolicy(sizePolicy)
        self.path_arquivo.setStyleSheet(u"QLabel {\n"
"	width: '100%';\n"
"}")

        self.verticalLayout_11.addWidget(self.path_arquivo)

        self.status = QLabel(self.groupBox)
        self.status.setObjectName(u"status")
        sizePolicy.setHeightForWidth(self.status.sizePolicy().hasHeightForWidth())
        self.status.setSizePolicy(sizePolicy)

        self.verticalLayout_11.addWidget(self.status)

        self.open_file_path = QCommandLinkButton(self.groupBox)
        self.open_file_path.setObjectName(u"open_file_path")
        sizePolicy.setHeightForWidth(self.open_file_path.sizePolicy().hasHeightForWidth())
        self.open_file_path.setSizePolicy(sizePolicy)
        self.open_file_path.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setBold(True)
        font.setUnderline(True)
        self.open_file_path.setFont(font)
        icon5 = QIcon()
        icon5.addFile(u"figs/file.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.open_file_path.setIcon(icon5)

        self.verticalLayout_11.addWidget(self.open_file_path)


        self.verticalLayout_10.addWidget(self.groupBox)


        self.horizontalLayout_4.addWidget(self.group_dados)

        self.del_item = QPushButton(self.download_item)
        self.del_item.setObjectName(u"del_item")
        sizePolicy.setHeightForWidth(self.del_item.sizePolicy().hasHeightForWidth())
        self.del_item.setSizePolicy(sizePolicy)
        self.del_item.setMaximumSize(QSize(40, 40))
        self.del_item.setStyleSheet(u"QPushButton {\n"
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
        icon6 = QIcon()
        icon6.addFile(u"figs/x.png", QSize(), QIcon.Normal, QIcon.Off)
        self.del_item.setIcon(icon6)

        self.horizontalLayout_4.addWidget(self.del_item)


        self.container_downloads_itens_page.addWidget(self.download_item)

        self.scrollAreaDownloads.setWidget(self.scrollAreaDownloadContents)

        self.container_principal.addWidget(self.scrollAreaDownloads)


        self.verticalLayout_6.addLayout(self.container_principal)

        self.stacked_pages.addWidget(self.downloads)
        self.historic = QWidget()
        self.historic.setObjectName(u"historic")
        self.verticalLayout_8 = QVBoxLayout(self.historic)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.container_principal_historic_sites = QVBoxLayout()
        self.container_principal_historic_sites.setSpacing(0)
        self.container_principal_historic_sites.setObjectName(u"container_principal_historic_sites")
        self.hotbar_historic = QGroupBox(self.historic)
        self.hotbar_historic.setObjectName(u"hotbar_historic")
        self.hotbar_historic.setMinimumSize(QSize(0, 40))
        self.hotbar_historic.setMaximumSize(QSize(16777215, 120))
        self.hotbar_historic.setStyleSheet(u"QGroupBox {\n"
"	border: none;\n"
"	margin: 0;\n"
"	padding: 0;\n"
"}")
        self.horizontalLayout_5 = QHBoxLayout(self.hotbar_historic)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.arrow_left_back_historic = QPushButton(self.hotbar_historic)
        self.arrow_left_back_historic.setObjectName(u"arrow_left_back_historic")
        sizePolicy1.setHeightForWidth(self.arrow_left_back_historic.sizePolicy().hasHeightForWidth())
        self.arrow_left_back_historic.setSizePolicy(sizePolicy1)
        self.arrow_left_back_historic.setMaximumSize(QSize(30, 30))
        self.arrow_left_back_historic.setStyleSheet(u"QPushButton {\n"
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
        self.arrow_left_back_historic.setIcon(icon1)

        self.horizontalLayout_6.addWidget(self.arrow_left_back_historic)

        self.lineEdit_2 = QLineEdit(self.hotbar_historic)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setMinimumSize(QSize(0, 30))
        self.lineEdit_2.setStyleSheet(u"QLineEdit {\n"
"	border: none;\n"
"	border-radius: 15px;\n"
"	padding-left: 10px;\n"
"	padding-right: 10px;\n"
"}")

        self.horizontalLayout_6.addWidget(self.lineEdit_2)

        self.options_historic_sites = QPushButton(self.hotbar_historic)
        self.options_historic_sites.setObjectName(u"options_historic_sites")
        sizePolicy1.setHeightForWidth(self.options_historic_sites.sizePolicy().hasHeightForWidth())
        self.options_historic_sites.setSizePolicy(sizePolicy1)
        self.options_historic_sites.setMaximumSize(QSize(33, 30))
        self.options_historic_sites.setCursor(QCursor(Qt.PointingHandCursor))
        self.options_historic_sites.setStyleSheet(u"QPushButton {\n"
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
        self.options_historic_sites.setIcon(icon4)

        self.horizontalLayout_6.addWidget(self.options_historic_sites)


        self.horizontalLayout_5.addLayout(self.horizontalLayout_6)


        self.container_principal_historic_sites.addWidget(self.hotbar_historic)

        self.scrollAreaHistoric = QScrollArea(self.historic)
        self.scrollAreaHistoric.setObjectName(u"scrollAreaHistoric")
        self.scrollAreaHistoric.setStyleSheet(u"QScrollArea {\n"
"	border: none;\n"
"}")
        self.scrollAreaHistoric.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.scrollAreaHistoric.setWidgetResizable(True)
        self.scrollAreaHistoricContents = QWidget()
        self.scrollAreaHistoricContents.setObjectName(u"scrollAreaHistoricContents")
        self.scrollAreaHistoricContents.setGeometry(QRect(0, 0, 778, 538))
        sizePolicy.setHeightForWidth(self.scrollAreaHistoricContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaHistoricContents.setSizePolicy(sizePolicy)
        self.scrollAreaHistoricContents.setStyleSheet(u"")
        self.container_historic_page = QVBoxLayout(self.scrollAreaHistoricContents)
        self.container_historic_page.setObjectName(u"container_historic_page")
        self.container_historic_page.setSizeConstraint(QLayout.SetMinAndMaxSize)
        self.container_historic_page.setContentsMargins(-1, 20, -1, -1)
        self.historic_item = QGroupBox(self.scrollAreaHistoricContents)
        self.historic_item.setObjectName(u"historic_item")
        sizePolicy.setHeightForWidth(self.historic_item.sizePolicy().hasHeightForWidth())
        self.historic_item.setSizePolicy(sizePolicy)
        self.historic_item.setMinimumSize(QSize(400, 50))
        self.historic_item.setMaximumSize(QSize(16777215, 60))
        self.historic_item.setStyleSheet(u"QGroupBox {\n"
"	border: 1px solid lightgray;\n"
"	border-radius: 20px;\n"
"	width: 100%;\n"
"}")
        self.historic_item.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.horizontalLayout_7 = QHBoxLayout(self.historic_item)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.group_dados_historic_site = QGroupBox(self.historic_item)
        self.group_dados_historic_site.setObjectName(u"group_dados_historic_site")
        self.group_dados_historic_site.setStyleSheet(u"QGroupBox {\n"
"	border: none;\n"
"	margin: 0;\n"
"	padding: 0;\n"
"}")
        self.verticalLayout_12 = QVBoxLayout(self.group_dados_historic_site)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.groupBox_2 = QGroupBox(self.group_dados_historic_site)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setStyleSheet(u"")
        self.verticalLayout_13 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(10, 0, 0, 0)
        self.open_site = QCommandLinkButton(self.groupBox_2)
        self.open_site.setObjectName(u"open_site")
        sizePolicy.setHeightForWidth(self.open_site.sizePolicy().hasHeightForWidth())
        self.open_site.setSizePolicy(sizePolicy)
        self.open_site.setMaximumSize(QSize(16777215, 16777215))
        self.open_site.setFont(font)
        self.open_site.setIcon(icon5)

        self.verticalLayout_13.addWidget(self.open_site)


        self.verticalLayout_12.addWidget(self.groupBox_2)


        self.horizontalLayout_7.addWidget(self.group_dados_historic_site)

        self.del_item_historic = QPushButton(self.historic_item)
        self.del_item_historic.setObjectName(u"del_item_historic")
        sizePolicy.setHeightForWidth(self.del_item_historic.sizePolicy().hasHeightForWidth())
        self.del_item_historic.setSizePolicy(sizePolicy)
        self.del_item_historic.setMaximumSize(QSize(40, 40))
        self.del_item_historic.setStyleSheet(u"QPushButton {\n"
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
        self.del_item_historic.setIcon(icon6)

        self.horizontalLayout_7.addWidget(self.del_item_historic)


        self.container_historic_page.addWidget(self.historic_item)

        self.scrollAreaHistoric.setWidget(self.scrollAreaHistoricContents)

        self.container_principal_historic_sites.addWidget(self.scrollAreaHistoric)


        self.verticalLayout_8.addLayout(self.container_principal_historic_sites)

        self.stacked_pages.addWidget(self.historic)

        self.verticalLayout.addWidget(self.stacked_pages)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(Widget)

        self.stacked_pages.setCurrentIndex(0)
        self.tabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"SurfEase", None))
        self.arrow_left_historic.setText("")
        self.arrow_right_historic.setText("")
        self.url.setText(QCoreApplication.translate("Widget", u"https://google.com", None))
        self.download_buttton.setText("")
        self.options.setText("")
        self.tabs.setTabText(self.tabs.indexOf(self.page), QCoreApplication.translate("Widget", u"Tab 1", None))
        self.hotbar.setTitle("")
        self.arrow_left_back.setText("")
        self.options_donwload.setText("")
        self.download_item.setTitle("")
        self.group_icon.setTitle("")
        self.icon_item.setText("")
        self.group_dados.setTitle("")
        self.groupBox.setTitle("")
        self.name_arquivo.setText(QCoreApplication.translate("Widget", u"TextLabel", None))
        self.path_arquivo.setText(QCoreApplication.translate("Widget", u"TextLabel", None))
        self.status.setText(QCoreApplication.translate("Widget", u"TextLabel", None))
        self.open_file_path.setText(QCoreApplication.translate("Widget", u"Abrir no local do arquivo", None))
        self.del_item.setText("")
        self.hotbar_historic.setTitle("")
        self.arrow_left_back_historic.setText("")
        self.options_historic_sites.setText("")
        self.historic_item.setTitle("")
        self.group_dados_historic_site.setTitle("")
        self.groupBox_2.setTitle("")
        self.open_site.setText(QCoreApplication.translate("Widget", u"Site visitado", None))
        self.del_item_historic.setText("")
    # retranslateUi

