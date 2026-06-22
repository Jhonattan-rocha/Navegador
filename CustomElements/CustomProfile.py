import os

from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings

from configs.Config import settings_app

# User-agent moderno; mantém compatibilidade com sites que checam Chrome recente.
_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

# Referência viva pelo tempo de vida do app. O perfil DEVE sobreviver a todas as
# QWebEnginePage que o usam — por isso é um singleton de módulo, sem parent Qt.
_shared_profile: QWebEngineProfile | None = None


def _flag(key: str, default: bool) -> bool:
    return settings_app.value(f"GeneralSettings/{key}", defaultValue=default, type=bool)


def _apply_web_settings(profile: QWebEngineProfile) -> None:
    s = profile.settings()
    WA = QWebEngineSettings.WebAttribute
    s.setAttribute(WA.LocalStorageEnabled, _flag("LocalStorageEnabled", True))
    s.setAttribute(WA.ScreenCaptureEnabled, _flag("ScreenCaptureEnabled", True))
    s.setAttribute(WA.PluginsEnabled, _flag("PluginsEnabled", True))
    s.setAttribute(WA.WebGLEnabled, _flag("WebGLEnabled", True))
    s.setAttribute(WA.Accelerated2dCanvasEnabled, _flag("Accelerated2dCanvasEnabled", True))
    s.setAttribute(WA.JavascriptEnabled, _flag("JavascriptEnabled", True))
    s.setAttribute(WA.PdfViewerEnabled, _flag("PdfViewerEnabled", True))
    s.setAttribute(WA.JavascriptCanAccessClipboard, _flag("JavascriptCanAccessClipboard", True))
    s.setAttribute(WA.PlaybackRequiresUserGesture, _flag("PlaybackRequiresUserGesture", True))
    s.setAttribute(WA.FullScreenSupportEnabled, True)
    s.setAttribute(WA.DnsPrefetchEnabled, True)
    # ForceDarkMode default DESLIGADO: forçar dark em todo site quebra o layout de
    # muitas páginas. Continua configurável via config.conf para quem quiser.
    if hasattr(WA, "ForceDarkMode"):
        s.setAttribute(WA.ForceDarkMode, _flag("ForceDarkMode", False))
    s.setDefaultTextEncoding("utf-8")


def shared_web_profile() -> QWebEngineProfile:
    """Perfil único e persistente usado por todas as abas/janelas.

    Compartilhar um único perfil é o que faz login, cookies e sessão valerem
    entre abas — e evita os crashes de ciclo de vida que apareciam quando cada
    aba criava (e destruía) o próprio perfil.
    """
    global _shared_profile
    if _shared_profile is None:
        profile = QWebEngineProfile("surfease")  # nome => perfil em disco (persistente)
        profile.setPersistentCookiesPolicy(
            QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies
        )
        profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.DiskHttpCache)
        profile.setPersistentStoragePath(os.path.abspath("./cookies"))
        profile.setCachePath(os.path.abspath("./cache"))
        profile.setDownloadPath(os.path.abspath("./downloads"))
        profile.setHttpUserAgent(_USER_AGENT)
        try:
            profile.setPushServiceEnabled(True)
        except (AttributeError, RuntimeError):
            pass
        _apply_web_settings(profile)
        _shared_profile = profile
    return _shared_profile
