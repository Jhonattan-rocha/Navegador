import sys

from cefpython3 import cefpython as cef


from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QApplication, QFrame, QGridLayout, QMainWindow, QVBoxLayout, QWidget

# from navbar import NavigationBar


class ChromiumApplication(QApplication):
    def __init__(self):
        super().__init__([])
        self.timer = self.create_timer()

    def create_timer(self):
        timer = QTimer()
        timer.timeout.connect(self.on_timeout)
        timer.start(10)
        return timer

    def on_timeout(self):
        cef.MessageLoopWork()


class ChromiumBrowserWindow(QMainWindow):
    DEFAULT_TITLE = "Chromium Browser"
    DEFAULT_WIDTH = 800
    DEFAULT_HEIGHT = 600

    def __init__(self):
        super().__init__()
        self.chrome = None
        self.web_view = None
        self.setWindowTitle(self.DEFAULT_TITLE)
        self.init_window()
        self.show()

    def init_window(self):
        self.resize(self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT)

        self.web_view = WebViewWidget()
        # self.chrome = NavigationBar(parent=self, browser=self.web_view.browser)

        frame = QFrame()
        self.setCentralWidget(frame)
        layout = QGridLayout(frame)
        # layout.addWidget(self.chrome, 0, 0)
        layout.setColumnStretch(0, 1)

        layout.addWidget(self.web_view, 1, 0)
        layout.setRowStretch(1, 2)

        layout.setContentsMargins(0, 0, 0, 0)

    def closeEvent(self, event):
        if self.web_view.browser is not None:
            self.web_view.browser.CloseBrowser(True)
            del self.web_view.browser


class WebViewWidget(QWidget):
    DEFAULT_URL = "https://www.google.com"
    HANDLERS = []

    def __init__(self, parent=None):
        super().__init__(parent)
        self._browser = None
        self._browser_widget = None
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        self.init_browser()

    @property
    def browser(self):
        return self._browser

    @browser.deleter
    def browser(self):
        self._browser = None

    def init_browser(self):
        browser_window = QWindow()
        window_config = cef.WindowInfo()
        window_config.SetAsChild(
            int(browser_window.winId()), list(self.rect().getRect())
        )
        self._browser = cef.CreateBrowserSync(window_config, url=self.DEFAULT_URL)
        self._browser_widget = QWidget.createWindowContainer(browser_window)
        self.layout().addWidget(self._browser_widget)
        self.set_handlers()

    def set_handlers(self):
        for handler in self.HANDLERS:
            self.browser.SetClientHanlder(handler(self))

    def resizeEvent(self, event):
        if self.browser and self._browser_widget:
            self.browser.SetBounds(*self._browser_widget.geometry().getRect())
            self.browser.NotifyMoveOrResizeStarted()


if __name__ == "__main__":
    sys.excepthook = cef.ExceptHook
    cef.Initialize()
    app = ChromiumApplication()
    window = ChromiumBrowserWindow()
    app.exec()
    app.timer.stop()
    cef.Shutdown()