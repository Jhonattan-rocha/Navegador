from PySide6.QtWidgets import QLineEdit


class CustomLineEdit(QLineEdit):
    def keyPressEvent(self, event):
        super().keyPressEvent(event)
