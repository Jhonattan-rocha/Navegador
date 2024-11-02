import os

from PySide6.QtWebEngineCore import QWebEngineProfile
from configs.Config import settings_app
# from PySide6.QtWidgets import QApplication
# from PySide6.QtGui import QSurfaceFormat

class CustomWebEngineProfile(QWebEngineProfile):

    def __init__(self, name=None, parent=None, cache_path=""):
        super().__init__(name, parent)
        self.setPushServiceEnabled(True)
        self.setPersistentCookiesPolicy(self.PersistentCookiesPolicy.ForcePersistentCookies)
        self.setHttpCacheType(self.HttpCacheType.DiskHttpCache)
        self.setPersistentStoragePath(os.path.join(os.path.abspath("./cookies")))
        self.setCachePath(os.path.join(os.path.abspath("./cache"), cache_path))
        self.setDownloadPath(os.path.join(os.path.abspath("./cache"), cache_path, "downloads"))
        self.setHttpUserAgent(
            ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
             "Chrome/96.0.4664.110 Safari/537.36"))
        self.settings().setAttribute(self.settings().WebAttribute.LocalStorageEnabled, settings_app.value("GeneralSettings/LocalStorageEnabled", defaultValue=True, type=bool))
        self.settings().setAttribute(self.settings().WebAttribute.ScreenCaptureEnabled, settings_app.value("GeneralSettings/ScreenCaptureEnabled", defaultValue=True, type=bool))
        self.settings().setAttribute(self.settings().WebAttribute.PluginsEnabled, settings_app.value("GeneralSettings/PluginsEnabled", defaultValue=True, type=bool))
        self.settings().setAttribute(self.settings().WebAttribute.WebGLEnabled, settings_app.value("GeneralSettings/WebGLEnabled", defaultValue=True, type=bool))
        self.settings().setAttribute(self.settings().WebAttribute.Accelerated2dCanvasEnabled, settings_app.value("GeneralSettings/Accelerated2dCanvasEnabled", defaultValue=True, type=bool))
        self.settings().setAttribute(self.settings().WebAttribute.JavascriptEnabled, settings_app.value("GeneralSettings/JavascriptEnabled", defaultValue=True, type=bool))
        self.settings().setAttribute(self.settings().WebAttribute.PdfViewerEnabled, settings_app.value("GeneralSettings/PdfViewerEnabled", defaultValue=False, type=bool))
        self.settings().setAttribute(self.settings().WebAttribute.JavascriptCanAccessClipboard, settings_app.value("GeneralSettings/JavascriptCanAccessClipboard", defaultValue=True, type=bool))
        self.settings().setAttribute(self.settings().WebAttribute.PlaybackRequiresUserGesture, settings_app.value("GeneralSettings/PlaybackRequiresUserGesture", defaultValue=True, type=bool))
        self.settings().setAttribute(self.settings().WebAttribute.ForceDarkMode, settings_app.value("GeneralSettings/ForceDarkMode", defaultValue=True, type=bool))
        self.settings().setAttribute(self.settings().WebAttribute.PlaybackRequiresUserGesture, False)

        self.settings().setDefaultTextEncoding("utf8")
        # format = QSurfaceFormat()
        # format.setVersion(3, 2)  # Versão do OpenGL
        # format.setProfile(format.OpenGLContextProfile.CompatibilityProfile)
        # format.setOption(format.FormatOption.ProtectedContent)
