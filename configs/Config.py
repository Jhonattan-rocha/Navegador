from PySide6.QtCore import QSettings

settings_app = QSettings("./configs/config.conf", QSettings.Format.IniFormat)
