import os

from PySide6.QtWebEngineCore import QWebEngineProfile
# from PySide6.QtWidgets import QApplication
# from PySide6.QtGui import QSurfaceFormat

class CustomWebEngineProfile(QWebEngineProfile):

    def __init__(self, name=None, parent=None, cache_path=""):
        super().__init__(name, parent)
        self.setPersistentCookiesPolicy(self.PersistentCookiesPolicy.ForcePersistentCookies)
        self.setHttpCacheType(self.HttpCacheType.DiskHttpCache)
        self.setPersistentStoragePath(os.path.abspath("./cookies"))
        self.setCachePath(os.path.join(os.path.abspath("./cache"), cache_path))
        self.setDownloadPath(os.path.join(os.path.abspath("./cache"), cache_path, "downloads"))
        self.setHttpUserAgent(
            ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
             "Chrome/96.0.4664.110 Safari/537.36"))
        self.settings().setAttribute(self.settings().WebAttribute.LocalStorageEnabled, True)
        self.settings().setAttribute(self.settings().WebAttribute.ScreenCaptureEnabled, True)
        self.settings().setAttribute(self.settings().WebAttribute.PluginsEnabled, True)
        self.settings().setAttribute(self.settings().WebAttribute.WebGLEnabled, True)
        self.settings().setAttribute(self.settings().WebAttribute.Accelerated2dCanvasEnabled, True)
        self.settings().setAttribute(self.settings().WebAttribute.JavascriptEnabled, True)
        self.settings().setAttribute(self.settings().WebAttribute.PdfViewerEnabled, True)
        self.settings().setAttribute(self.settings().WebAttribute.JavascriptCanAccessClipboard, False)
        self.settings().setAttribute(self.settings().WebAttribute.PlaybackRequiresUserGesture, False)
        self.settings().setDefaultTextEncoding("utf8")
        # format = QSurfaceFormat()
        # format.setVersion(3, 2)  # Versão do OpenGL
        # format.setProfile(format.OpenGLContextProfile.CompatibilityProfile)
        # format.setOption(format.FormatOption.ProtectedContent)
