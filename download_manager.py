import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QFileDialog
from PyQt5.QtWebEngineWidgets import QWebEngineDownloadItem

class DownloadManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DOwnluds!")
        self.resize(600, 400)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.download_list = QListWidget()
        self.layout.addWidget(self.download_list)

    def add_download(self, download_item: QWebEngineDownloadItem):
        download_name = download_item.url().fileName()
        download_status = QListWidgetItem(f"Downloading {download_name}...")
        self.download_list.addItem(download_status)

        download_item.finished.connect(lambda: self.update_download_status(download_status, download_item))

    def update_download_status(self, item: QListWidgetItem, download_item: QWebEngineDownloadItem):
        if download_item.isFinished():
            item.setText(f"Download complete: {download_item.path()}")
        else:
            item.setText(f"Download failed: {download_item.url().fileName()}")

    def start_download(self, download: QWebEngineDownloadItem):
        default_download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        save_path, _ = QFileDialog.getSaveFileName(self, "Save File", os.path.join(default_download_dir, download.url().fileName()))
        if save_path:
            download.setPath(save_path)
            download.accept()
            self.add_download(download)
