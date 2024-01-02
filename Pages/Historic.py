from PySide6.QtCore import (QRect,
                            QSize, Qt)
from PySide6.QtGui import (QCursor,
                           QIcon, QFont)
from PySide6.QtWidgets import (QAbstractScrollArea, QCommandLinkButton, QGroupBox,
                               QHBoxLayout, QLayout, QLineEdit,
                               QPushButton, QScrollArea, QSizePolicy, QVBoxLayout, QWidget)


class HistoricPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("historic")

    def setup_ui(self, widget):
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        widget.setWindowTitle("Histórico")
        icon1 = QIcon()
        icon1.addFile(u"figs/l-arrow.png", QSize(), QIcon.Normal, QIcon.Off)
        icon4 = QIcon()
        icon4.addFile(u"figs/dotdotdot.png", QSize(), QIcon.Normal, QIcon.Off)
        icon5 = QIcon()
        icon5.addFile(u"figs/file.ico", QSize(), QIcon.Normal, QIcon.Off)
        icon6 = QIcon()
        icon6.addFile(u"figs/x.png", QSize(), QIcon.Normal, QIcon.Off)
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setBold(True)
        font.setUnderline(True)

        self.historic = QWidget(widget)
        self.historic.implementation = widget
        self.historic.setObjectName(u"historic")
        self.container_historic_page_2 = QVBoxLayout(self.historic)
        self.container_historic_page_2.setSizeConstraint(QVBoxLayout.SizeConstraint.SetDefaultConstraint)
        self.container_historic_page_2.setObjectName(u"container_historic_page_2")
        self.container_principal_historic_sites = QVBoxLayout()
        self.container_principal_historic_sites.setSpacing(0)
        self.container_principal_historic_sites.setSizeConstraint(QVBoxLayout.SizeConstraint.SetDefaultConstraint)
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
        self.historic_item.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
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
        self.del_item_historic.setMinimumSize(QSize(40, 40))
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

        self.container_historic_page_2.addLayout(self.container_principal_historic_sites)
