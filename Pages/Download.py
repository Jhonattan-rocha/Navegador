from PySide6.QtCore import (QRect,
                            QSize, Qt)
from PySide6.QtGui import (QCursor,
                           QFont, QIcon)
from PySide6.QtWidgets import (QAbstractScrollArea, QCommandLinkButton, QGroupBox,
                               QHBoxLayout, QLabel, QLayout, QLineEdit,
                               QScrollArea, QSizePolicy, QWidget)
from PySide6.QtWidgets import (QPushButton,
                               QVBoxLayout)


class DownloadsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("downloads")

    def setup_ui(self, widget):
        sizePolicyExpanding = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicyExpanding.setHorizontalStretch(0)
        sizePolicyExpanding.setVerticalStretch(0)

        widget.setWindowTitle("Downloads")
        icon1 = QIcon()
        icon1.addFile(u"figs/l-arrow.png", QSize(), QIcon.Normal, QIcon.Off)
        icon4 = QIcon()
        icon4.addFile(u"figs/dotdotdot.png", QSize(), QIcon.Normal, QIcon.Off)

        self.downloads = QWidget(widget)
        self.downloads.implementation = widget
        self.setSizePolicy(sizePolicyExpanding)
        self.downloads.setObjectName(u"downloads")
        self.downloads.setSizePolicy(sizePolicyExpanding)
        self.container_principal_donwload = QVBoxLayout(self.downloads)
        self.container_principal_donwload.setSpacing(0)
        self.container_principal_donwload.setSizeConstraint(QVBoxLayout.SizeConstraint.SetDefaultConstraint)
        self.container_principal_donwload.setObjectName(u"container_principal_donwload")
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
        self.horizontalLayout_3.setSizeConstraint(QHBoxLayout.SizeConstraint.SetDefaultConstraint)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setSizeConstraint(QHBoxLayout.SizeConstraint.SetDefaultConstraint)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.arrow_left_back = QPushButton(self.hotbar)
        self.arrow_left_back.setObjectName(u"arrow_left_back")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
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

        self.search_input = QLineEdit(self.hotbar)
        self.search_input.setObjectName(u"search_input")
        self.search_input.setMinimumSize(QSize(0, 30))
        self.search_input.setStyleSheet(u"QLineEdit {\n"
                                    "	border: none;\n"
                                    "	border-radius: 15px;\n"
                                    "	padding-left: 10px;\n"
                                    "	padding-right: 10px;\n"
                                    "}")

        self.horizontalLayout_2.addWidget(self.search_input)

        self.options_donwload = QPushButton(self.hotbar)
        self.options_donwload.setObjectName(u"options_donwload")
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

        self.container_principal_donwload.addWidget(self.hotbar)

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
        self.scrollAreaDownloadContents.setSizePolicy(sizePolicyExpanding)
        self.scrollAreaDownloadContents.setStyleSheet(u"")
        self.container_downloads_itens_page = QVBoxLayout(self.scrollAreaDownloadContents)
        self.container_downloads_itens_page.setObjectName(u"container_downloads_itens_page")
        self.container_downloads_itens_page.setSizeConstraint(QLayout.SetMinAndMaxSize)
        self.container_downloads_itens_page.setContentsMargins(-1, 20, -1, -1)
        self.download_item = QGroupBox(self.scrollAreaDownloadContents)
        self.download_item.setObjectName(u"download_item")
        self.download_item.setMinimumSize(QSize(400, 100))
        self.download_item.setMaximumSize(QSize(16777215, 100))
        self.download_item.setStyleSheet(u"QGroupBox {\n"
                                         "	border: 1px solid lightgray;\n"
                                         "	border-radius: 20px;\n"
                                         "	width: 100%;\n"
                                         "}")
        self.download_item.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.horizontalLayout_4 = QHBoxLayout(self.download_item)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.group_icon = QGroupBox(self.download_item)
        self.group_icon.setObjectName(u"group_icon")
        self.group_icon.setSizePolicy(sizePolicyExpanding)
        self.group_icon.setMinimumSize(QSize(60, 0))
        self.group_icon.setMaximumSize(QSize(60, 16777215))
        self.verticalLayout_5 = QVBoxLayout(self.group_icon)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.icon_item = QLabel(self.group_icon)
        self.icon_item.setObjectName(u"icon_item")
        self.icon_item.setSizePolicy(sizePolicyExpanding)

        self.verticalLayout_5.addWidget(self.icon_item)

        self.horizontalLayout_4.addWidget(self.group_icon)

        self.group_dados = QGroupBox(self.download_item)
        self.group_dados.setObjectName(u"group_dados")
        self.group_dados.setSizePolicy(sizePolicyExpanding)
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
        self.groupBox.setSizePolicy(sizePolicyExpanding)
        self.groupBox.setStyleSheet(u"")
        self.verticalLayout_11 = QVBoxLayout(self.groupBox)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(10, 0, 0, 0)
        self.name_arquivo = QLabel(self.groupBox)
        self.name_arquivo.setObjectName(u"name_arquivo")
        self.name_arquivo.setSizePolicy(sizePolicyExpanding)

        self.verticalLayout_11.addWidget(self.name_arquivo)

        self.path_arquivo = QLabel(self.groupBox)
        self.path_arquivo.setObjectName(u"path_arquivo")
        self.path_arquivo.setSizePolicy(sizePolicyExpanding)
        self.path_arquivo.setStyleSheet(u"QLabel {\n"
                                        "	width: '100%';\n"
                                        "}")

        self.verticalLayout_11.addWidget(self.path_arquivo)

        self.status = QLabel(self.groupBox)
        self.status.setObjectName(u"status")
        self.status.setSizePolicy(sizePolicyExpanding)

        self.verticalLayout_11.addWidget(self.status)

        self.open_file_path = QCommandLinkButton(self.groupBox)
        self.open_file_path.setObjectName(u"open_file_path")
        self.open_file_path.setSizePolicy(sizePolicyExpanding)
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

        self.container_principal_donwload.addWidget(self.scrollAreaDownloads)
