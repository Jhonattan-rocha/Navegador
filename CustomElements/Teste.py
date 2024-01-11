import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView


class LiveStreamWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Exemplo de Live Stream")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.webview = QWebEngineView()
        layout.addWidget(self.webview)

        # Carregando uma página web com um stream de vídeo ao vivo
        self.webview.load(
            "https://www.youtube.com/embed/LIVE_VIDEO_ID")  # Substitua LIVE_VIDEO_ID pelo ID do vídeo ao vivo


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LiveStreamWindow()
    window.show()
    sys.exit(app.exec())
