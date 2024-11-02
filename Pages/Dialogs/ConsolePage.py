from PySide6.QtCore import (QSize)
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QGroupBox, QPlainTextEdit,
                               QSizePolicy, QVBoxLayout, QWidget)

from CustomElements.CustomLineEdit import CustomLineEdit


class ConsolePage(QWidget):

    def __init__(self, parent=None, title="Console"):
        super().__init__(parent)
        self.title = title

    def setupUi(self, Console: QWidget):
        if not Console.objectName():
            Console.setObjectName(u"Console")
        Console.resize(600, 500)
        iconWindow = QIcon()
        iconWindow.addFile(u"figs/console.png", QSize(), QIcon.Normal, QIcon.Off)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        Console.setWindowTitle(self.title)
        Console.setWindowIcon(iconWindow)
        self.container_page = QWidget(parent=Console)
        self.container_page.implementation = Console
        self.container_console_layout = QVBoxLayout(Console)
        self.container_console_layout.setObjectName(u"container_console_layout")
        self.groupBox = QGroupBox(self.container_page)
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.container_script = QGroupBox(self.groupBox)
        self.container_script.setObjectName(u"container_script")
        self.container_script.setSizePolicy(sizePolicy)
        self.container_script.setStyleSheet(u"QGroupBox {\n"
                                            "	border: 1px solid gray;\n"
                                            "	background-color: white;\n"
                                            "	border-radius: 20px;\n"
                                            "    padding: 10px;\n"
                                            "}")
        self.verticalLayout_4 = QVBoxLayout(self.container_script)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.script = QPlainTextEdit(self.container_script)
        self.script.setReadOnly(True)
        self.script.setSizePolicy(sizePolicy)
        self.script.setObjectName(u"script")
        self.script.setStyleSheet(u"QPlainTextEdit {\n"
                                  "	border: none;\n"
                                  "}")

        self.verticalLayout_4.addWidget(self.script)

        self.verticalLayout_2.addWidget(self.container_script)

        self.container_console = QGroupBox(self.groupBox)
        self.container_console.setObjectName(u"container_console")
        self.container_console.setSizePolicy(sizePolicy)
        self.container_console.setStyleSheet(u"QGroupBox {\n"
                                             "	border: 1px solid gray;\n"
                                             "	background-color: white;\n"
                                             "	border-radius: 10px;\n"
                                             "	padding: 20px;\n"
                                             "}")
        self.verticalLayout_3 = QVBoxLayout(self.container_console)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.console_output = QPlainTextEdit(self.container_console)
        self.console_output.setReadOnly(True)
        self.console_output.setSizePolicy(sizePolicy)
        self.console_output.setObjectName(u"console_output")
        self.console_output.setStyleSheet(u"QPlainTextEdit {\n"
                                          "	border: none;\n"
                                          "	border-bottom: 1px solid black;\n"
                                          "	border-bottom-right-radius: 10px;\n"
                                          "    border-bottom-left-radius: 10px;\n"
                                          "	padding: 10px;\n"
                                          "}")

        self.verticalLayout_3.addWidget(self.console_output)

        self.console_input = CustomLineEdit(self.container_console)
        self.console_input.setObjectName(u"console_input")
        self.console_input.setMinimumSize(QSize(0, 30))
        self.console_input.setMaximumSize(QSize(10000, 40))
        self.console_input.setSizePolicy(sizePolicy)
        self.console_input.setStyleSheet(u"QLineEdit {\n"
                                         "	border: 1px solid black;\n"
                                         "	border-radius: 10px;\n"
                                         "	padding-left: 5px;\n"
                                         "    padding-right: 5px;\n"
                                         "}")

        self.verticalLayout_3.addWidget(self.console_input)

        self.verticalLayout_2.addWidget(self.container_console)

        self.container_console_layout.addWidget(self.groupBox)
