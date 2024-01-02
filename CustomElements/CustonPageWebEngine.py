import os

from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile
from PySide6.QtWebEngineWidgets import QWebEngineView


class CustomWebEnginePage(QWebEnginePage):
    external_windows = []

    def __init__(self, parent=None):
        super().__init__(parent)
        self.profile().setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)
        self.profile().setHttpCacheType(self.profile().HttpCacheType.DiskHttpCache)
        self.profile().setPersistentStoragePath(os.path.abspath("Cookies"))
        self.profile().setCachePath(os.path.abspath("PersistedDatas"))
        self.profile().setDownloadPath(os.path.abspath("PersistedDatas"))
        self.profile().settings().setAttribute(self.profile().settings().WebAttribute.LocalStorageEnabled, True)
        self.profile().settings().setAttribute(self.profile().settings().WebAttribute.ScreenCaptureEnabled, True)

    def acceptNavigationRequest(self, url, _type, isMainFrame):
        if _type == QWebEnginePage.NavigationType.NavigationTypeLinkClicked:
            # Verifica se a URL corresponde a um padrão específico (por exemplo, um login OAuth)
            if "oauth" in url.toString():
                new_view = QWebEngineView()
                new_view.setUrl(url)
                new_view.show()
                return False  # Permite a navegação para essa URL
        return super().acceptNavigationRequest(url, _type, isMainFrame)
