import os

from PySide6.QtGui import QSurfaceFormat
from PySide6.QtWebEngineCore import QWebEngineProfile


class CustomWebEngineProfile(QWebEngineProfile):

    def __init__(self, profile=None, parent=None):
        super().__init__(profile, parent)
        self.setPersistentCookiesPolicy(self.PersistentCookiesPolicy.ForcePersistentCookies)
        self.setHttpCacheType(self.HttpCacheType.DiskHttpCache)
        self.setPersistentStoragePath(os.path.abspath("Cookies"))
        self.setCachePath(os.path.abspath("PersistedDatas"))
        self.setDownloadPath(os.path.abspath("PersistedDatas"))
        self.setHttpUserAgent(
            ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
             "Chrome/96.0.4664.110 Safari/537.36"))
        # self.initialize_opengl()
        self.settings().setAttribute(self.settings().WebAttribute.LocalStorageEnabled, True)
        self.settings().setAttribute(self.settings().WebAttribute.ScreenCaptureEnabled, True)
        self.settings().setAttribute(self.settings().WebAttribute.PluginsEnabled, True)
        # self.settings().setAttribute(self.settings().WebAttribute.WebGLEnabled, True)
        # self.settings().setAttribute(self.settings().WebAttribute.Accelerated2dCanvasEnabled, True)

    def initialize_opengl(self):
        # Configura o formato do OpenGL
        format = QSurfaceFormat()
        format.setRenderableType(QSurfaceFormat.OpenGL)
        format.setProfile(QSurfaceFormat.CoreProfile)
        format.setSwapBehavior(QSurfaceFormat.DoubleBuffer)
        self.setPersistentCookiesPolicy(self.PersistentCookiesPolicy.ForcePersistentCookies)
        QSurfaceFormat.setDefaultFormat(format)
