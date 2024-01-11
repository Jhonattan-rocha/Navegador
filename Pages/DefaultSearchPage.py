import os

from PySide6.QtCore import (QSize, QUrl, Qt)
from PySide6.QtGui import (QCursor, QFont, QIcon, QMovie)
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QGroupBox, QHBoxLayout, QLineEdit, QSizePolicy, QWidget, QLabel)
from PySide6.QtWidgets import (QPushButton, QLayout, QProgressBar, QVBoxLayout)

from CustomElements.CustomProfile import CustomWebEngineProfile


class DefaultSearchPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("default_page")

    def update_progress(self, progress):
        # Atualizar o valor da barra de progresso com base no progresso do carregamento da página
        self.progress_bar.setValue(progress)

    def setup_ui(self, widget):
        sizePolicyExpanding = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicyExpanding.setHorizontalStretch(1)
        sizePolicyExpanding.setVerticalStretch(1)
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
        self.page = QWidget(parent=widget)
        self.page.implementation = widget
        self.page.setObjectName(u"page")
        self.setSizePolicy(sizePolicyExpanding)
        self.page.setSizePolicy(sizePolicyExpanding)
        self.page.setMaximumSize(QSize(16777215, 16777215))
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setMinimumHeight(5)
        self.progress_bar.setMaximumHeight(10)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setSizePolicy(sizePolicyExpanding)
        self.container_tab = QVBoxLayout(self.page)
        self.container_tab.setObjectName(u"container_tab")
        self.container_tab.setContentsMargins(0, 0, 0, 0)
        self.container_tab.setSizeConstraint(QVBoxLayout.SizeConstraint.SetDefaultConstraint)
        self.container_tab.addWidget(self.progress_bar)
        self.hot_bar = QGroupBox(self.page)
        self.hot_bar.setObjectName(u"hot_bar")
        self.hot_bar.setMinimumSize(QSize(300, 40))
        self.hot_bar.setMaximumSize(QSize(16777215, 40))
        self.hot_bar.setSizePolicy(sizePolicyExpanding)
        self.hot_bar.setStyleSheet(u"QGroupBox {\n"
                                   "	border: none;\n"
                                   "	margin: 0;\n"
                                   "	padding: 0;\n"
                                   "	width: 100%;\n"
                                   "}")
        self.horizontalLayout = QHBoxLayout(self.hot_bar)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 5, 0, 0)
        self.horizontalLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.arrow_left_historic = QPushButton(self.hot_bar)
        self.arrow_left_historic.setObjectName(u"arrow_left_historic")
        self.arrow_left_historic.setSizePolicy(sizePolicyExpanding)
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
        icon1.addFile(u"figs/l-arrow.png", QSize(), QIcon.Normal, QIcon.Off)
        self.arrow_left_historic.setIcon(icon1)

        self.horizontalLayout.addWidget(self.arrow_left_historic)

        self.arrow_right_historic = QPushButton(self.hot_bar)
        self.arrow_right_historic.setObjectName(u"arrow_right_historic")
        self.arrow_right_historic.setSizePolicy(sizePolicyExpanding)
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

        self.movie = QMovie(os.path.abspath(os.path.join("figs", 'load.gif')))
        self.movie.setScaledSize(QSize(30, 30))
        self.label_movie = QLabel(self.hot_bar)
        self.label_movie.setSizePolicy(sizePolicyExpanding)
        self.label_movie.setMaximumSize(QSize(40, 40))
        self.label_movie.setMovie(self.movie)
        self.label_movie.hide()

        iconPush = QIcon()
        iconPush.addFile(os.path.abspath(os.path.join("figs", 'site.png')), QSize(25, 25), QIcon.Normal, QIcon.Off)
        pixmap = iconPush.pixmap(QSize(20, 20))
        self.label_icon_site = QLabel()
        self.label_icon_site.setPixmap(pixmap)
        self.label_icon_site.setMaximumSize(QSize(25, 25))
        self.label_icon_site.setSizePolicy(sizePolicyExpanding)
        self.label_icon_site.setStyleSheet(u"QPushButton {\n"
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
        self.label_icon_site.hide()
        self.horizontalLayout.addWidget(self.label_movie)
        self.horizontalLayout.addWidget(self.label_icon_site)

        # -----------

        self.url = QLineEdit()
        self.url.setObjectName(u"url")
        self.url.setSizePolicy(sizePolicyExpanding)
        self.url.setStyleSheet(u"QLineEdit {\n"
                               "	border: none;\n"
                               "	border-radius: 15px;\n"
                               "	padding-left: 5px;\n"
                               "	padding-right: 5px;\n"
                               "}")

        self.horizontalLayout.addWidget(self.url)

        self.download_buttton = QPushButton(self.hot_bar)
        self.download_buttton.setObjectName(u"download_buttton")
        self.download_buttton.setSizePolicy(sizePolicyExpanding)
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
        self.options.setSizePolicy(sizePolicyExpanding)
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
        icon4.addFile(u"figs/dotdotdot.png", QSize(), QIcon.Normal, QIcon.Off)
        self.options.setIcon(icon4)

        self.horizontalLayout.addWidget(self.options)

        self.container_tab.addWidget(self.hot_bar)

        self.profile = CustomWebEngineProfile(self)
        self.page_web = QWebEnginePage(self.profile, widget)
        self.page_web.setObjectName("page_web")
        self.webEngineView = QWebEngineView(self.page)
        self.webEngineView.setPage(self.page_web)
        self.webEngineView.setObjectName(u"webEngineView")
        self.webEngineView.setSizePolicy(sizePolicyExpanding)
        self.webEngineView.setMinimumSize(QSize(0, 0))
        self.webEngineView.setMaximumSize(QSize(16777215, 16777215))
        self.webEngineView.setUrl(QUrl(u"about:blank"))
        self.webEngineView.loadProgress.connect(self.update_progress)
        self.webEngineView.load("https://www.google.com/")
        self.container_tab.addWidget(self.webEngineView)
