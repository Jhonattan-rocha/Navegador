import datetime
import os.path

import requests
from PySide6.QtCore import (QThread, Signal, QObject, Slot)

class DownloadThread(QThread):
    progress_update = Signal(float)
    download_finished = Signal(str, str)
    download_failed = Signal(str, str)

    def __init__(self, url, folder_path, suggested_file_name):
        super().__init__()
        self.url = url
        self.folder_path = folder_path
        self.suggested_file_name = suggested_file_name

    def run(self):
        file_name = os.path.join(self.folder_path, self.suggested_file_name)

        try:
            with requests.get(self.url, stream=True) as r:
                if r.status_code == 200:
                    total_size = int(r.headers.get('content-length', 0))
                    bytes_so_far = 0
                    chunk_size = 8192

                    with open(file_name, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=chunk_size):
                            if chunk:
                                f.write(chunk)
                                bytes_so_far += len(chunk)
                                if total_size > 0:
                                    percent = (bytes_so_far / total_size) * 100
                                    self.progress_update.emit(percent)
                    
                    self.progress_update.emit(100)
                    self.download_finished.emit(self.suggested_file_name, self.folder_path)
                else:
                    self.download_failed.emit(self.suggested_file_name, self.folder_path)
        except Exception as e:
            self.download_failed.emit(self.suggested_file_name, self.folder_path)


class Downloader(QObject):
    progress_update = Signal(float)
    download_finished = Signal(str, str)
    download_failed = Signal(str, str)
    downloads = []

    def __init__(self, parent=None):
        super().__init__(parent)
        self.download_thread = None

    @Slot(str, str, str)
    def download_file(self, url, folder_path, suggested_file_name):
        self.download_thread = DownloadThread(url, folder_path, suggested_file_name)
        self.downloads.append(self.download_thread)
        self.download_thread.progress_update.connect(lambda percent: self.handle_progress(percent))
        self.download_thread.download_finished.connect(self.handle_download_finished)
        self.download_thread.download_failed.connect(self.handle_download_failed)
        self.download_thread.start()

    def handle_progress(self, percent: float):
        self.progress_update.emit(percent)

    def handle_download_finished(self, suggested_file_name, folder_path):
        self.download_finished.emit(suggested_file_name, folder_path)

    def handle_download_failed(self, suggested_file_name, folder_path):
        self.download_failed.emit(suggested_file_name, folder_path)
