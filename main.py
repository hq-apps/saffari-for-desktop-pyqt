#!/usr/bin/env python3
import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QToolBar, QAction, QLineEdit, QApplication, QWidget, QVBoxLayout, QMenu, QToolButton
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineDownloadItem
from download_manager import DownloadManager # Requires download_manager.py to be in the same folder!
from about import AboutDialog  # Import the AboutDialog class

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
        self.browser.download_manager.start_download(download) # See download_manager.py

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
        self.setWindowTitle("Saffari For decstop")
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

        self.download_manager = DownloadManager()

        self.add_hamburger_menu()

        self.add_new_tab()

    def add_hamburger_menu(self):
        hamburger_menu = QMenu(self)
        downloads_action = QAction("downlod manager", self)  # Add Downloads action to the menu
        settings_action = QAction("Setting...", self)
        about_action = QAction("about saffari for decstop", self)
        downloads_action.triggered.connect(self.show_downloads)
        about_action.triggered.connect(self.show_about_dialog)  # Connect the About action
        hamburger_menu.addAction(downloads_action)  # Add Downloads action to the menu
        hamburger_menu.addAction(settings_action)
        hamburger_menu.addAction(about_action)

        hamburger_button = QToolButton(self)
        hamburger_button.setText("☰")
        hamburger_button.setMenu(hamburger_menu)
        hamburger_button.setPopupMode(QToolButton.InstantPopup)  # Show menu on button click
        hamburger_button.clicked.connect(lambda: hamburger_menu.exec_(hamburger_button.mapToGlobal(hamburger_button.rect().bottomLeft())))
        self.navbar.addWidget(hamburger_button)

    def add_new_tab(self):
        new_tab = BrowserTab(self)
        new_tab.navigate_to_url("https://saffaristart.pages.dev")
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

    def show_about_dialog(self):
        about_dialog = AboutDialog()
        about_dialog.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())
