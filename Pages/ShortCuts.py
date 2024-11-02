from PySide6.QtGui import QKeySequence, QShortcut


class ShortcutManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ShortcutManager, cls).__new__(cls)
            cls._instance.shortcuts = {}
        return cls._instance

    def register_shortcut(self, widget, key_sequence, callback):
        shortcut = QShortcut(QKeySequence(key_sequence), widget)
        shortcut.activated.connect(callback)
        self.shortcuts[key_sequence] = shortcut

    def unregister_shortcut(self, key_sequence):
        if key_sequence in self.shortcuts:
            self.shortcuts[key_sequence].setEnabled(False)
            del self.shortcuts[key_sequence]

    def clear_shortcuts(self):
        for key_sequence, shortcut in self.shortcuts.items():
            shortcut.setEnabled(False)
        self.shortcuts.clear()
