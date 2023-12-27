from PySide6.QtCore import (QCoreApplication, QMetaObject, QSize, Qt)
from PySide6.QtGui import (QIcon)
from PySide6.QtWidgets import (QStackedWidget, QTabWidget, QVBoxLayout, QWidget, QSizePolicy)

from CustomElements.DraggableTabWidget import DraggableTabWidget

class Main_page(QWidget):

    def setupUi(self, Widget):
        sizePolicyExpanding = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicyExpanding.setHorizontalStretch(0)
        sizePolicyExpanding.setVerticalStretch(0)

        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(800, 600)
        Widget.setContentsMargins(0, 0, 0, 0)
        icon = QIcon()
        icon.addFile(u"figs/icon.png", QSize(), QIcon.Normal, QIcon.Off)
        Widget.setWindowIcon(icon)
        Widget.setSizePolicy(sizePolicyExpanding)
        self.verticalLayout_2 = QVBoxLayout(Widget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSizeConstraint(QVBoxLayout.SizeConstraint.SetDefaultConstraint)
        self.stacked_pages = QStackedWidget(Widget)
        self.stacked_pages.setObjectName(u"stacked_pages")
        self.stacked_pages.setContentsMargins(0, 0, 0, 0)
        self.stacked_pages.setEnabled(True)
        self.default_page = QWidget()
        self.default_page.setObjectName(u"default_page")
        self.default_page.setEnabled(True)
        self.default_page.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4 = QVBoxLayout(self.default_page)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.tabs = DraggableTabWidget(self.default_page)
        self.tabs.setObjectName(u"tabs")
        self.tabs.setMovable(True)
        self.tabs.setEnabled(True)
        self.tabs.setTabPosition(QTabWidget.TabPosition.South)
        self.tabs.setElideMode(Qt.TextElideMode.ElideMiddle)
        self.tabs.setTabsClosable(False)

        self.verticalLayout_4.addWidget(self.tabs)

        self.stacked_pages.addWidget(self.default_page)

        self.verticalLayout_2.addWidget(self.stacked_pages)

        self.retranslateUi(Widget)

        self.stacked_pages.setCurrentIndex(0)
        self.tabs.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(Widget)

    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"SurfEase", None))

    # retranslateUi
