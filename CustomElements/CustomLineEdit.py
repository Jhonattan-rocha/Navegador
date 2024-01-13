from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLineEdit

from DataOperations.register_recover import recover_console_historic


class CustomLineEdit(QLineEdit):
    def keyPressEvent(self, event):
        key = event.key()

        match key:
            case Qt.Key.Key_Up:
                command = self.text()
                new_command = recover_console_historic(command=command, prev_next="next")
                self.setText(new_command)
            case Qt.Key.Key_Down:
                command = self.text()
                new_command = recover_console_historic(command=command, prev_next="prev")
                self.setText(new_command)
            case _:
                super().keyPressEvent(event)
