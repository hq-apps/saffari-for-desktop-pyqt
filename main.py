import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class DownloadManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DOwnluds!")
        self.resize(600, 400)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.download_list = QListWidget()
        self.layout.addWidget(self.download_list)

    def add_download(self, download_item):
        download_name = download_item.url().fileName()
        download_status = QListWidgetItem(f"Downloading {download_name}...")
        self.download_list.addItem(download_status)

        download_item.finished.connect(lambda: self.update_download_status(download_status, download_item))

    def update_download_status(self, item, download_item):
        if download_item.isFinished():
            item.setText(f"Download complete: {download_item.path()}")
        else:
            item.setText(f"Download failed: {download_item.url().fileName()}")

class BrowserTab(QWidget):
    def __init__(self, browser):
        super().__init__()
        self.browser = browser
        self.layout = QVBoxLayout()
        self.browser_view = QWebEngineView()
        self.layout.addWidget(self.browser_view)
        self.setLayout(self.layout)

        self.browser_view.urlChanged.connect(self.update_url_bar)
        self.browser_view.page().profile().downloadRequested.connect(self.start_download)
        self.browser_view.loadFinished.connect(self.update_tab_title)

    def navigate_to_url(self, url):
        if not (url.startswith("http://") or url.startswith("https://")):
            url = "https://" + url
        self.browser_view.setUrl(QUrl(url))

    def update_url_bar(self, q):
        self.browser.url_bar.setText(q.toString())

    def start_download(self, download: QWebEngineDownloadItem):
        default_download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        save_path, _ = QFileDialog.getSaveFileName(self, "Save File", os.path.join(default_download_dir, download.url().fileName()))
        if save_path:
            download.setPath(save_path)
            download.accept()
            self.browser.download_manager.add_download(download)

    def update_tab_title(self):
        title = self.browser_view.page().title()
        if title:
            index = self.browser.tabs.indexOf(self)
            self.browser.tabs.setTabText(index, title)
        else:
            self.browser.tabs.setTabText(self.browser.tabs.indexOf(self), "New Tab")

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("saffari For decstop")
        self.resize(1200, 800)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        self.setCentralWidget(self.tabs)

        self.navbar = QToolBar()
        self.addToolBar(self.navbar)

        back_button = QAction("←", self)
        back_button.triggered.connect(self.go_back)
        self.navbar.addAction(back_button)

        forward_button = QAction("→", self)
        forward_button.triggered.connect(self.go_forward)
        self.navbar.addAction(forward_button)

        reload_button = QAction("🔄", self)
        reload_button.triggered.connect(self.reload_page)
        self.navbar.addAction(reload_button)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.navbar.addWidget(self.url_bar)

        new_tab_button = QAction("+", self)
        new_tab_button.triggered.connect(self.add_new_tab)
        self.navbar.addAction(new_tab_button)

        downloads_button = QAction("Downloads", self)
        downloads_button.triggered.connect(self.show_downloads)
        self.navbar.addAction(downloads_button)

        self.download_manager = DownloadManager()

        self.add_new_tab()

    def add_new_tab(self):
        new_tab = BrowserTab(self)
        new_tab.navigate_to_url("https://www.google.com")
        self.tabs.addTab(new_tab, "New Tab")
        self.tabs.setCurrentWidget(new_tab)

    def close_current_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def navigate_to_url(self):
        current_tab = self.tabs.currentWidget()
        url = self.url_bar.text()
        current_tab.navigate_to_url(url)

    def go_back(self):
        current_tab = self.tabs.currentWidget()
        current_tab.browser_view.back()

    def go_forward(self):
        current_tab = self.tabs.currentWidget()
        current_tab.browser_view.forward()

    def reload_page(self):
        current_tab = self.tabs.currentWidget()
        current_tab.browser_view.reload()

    def show_downloads(self):
        self.download_manager.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())
