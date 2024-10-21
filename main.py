#!/usr/bin/env python3
import sys
from PyQt6.QtCore import QUrl, pyqtSlot, QObject
from PyQt6.QtWidgets import QMainWindow, QTabWidget, QToolBar, QLineEdit, QApplication, QWidget, QVBoxLayout, QMenu, QToolButton
from PyQt6.QtGui import QAction
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineDownloadRequest
from PyQt6.QtQml import QQmlApplicationEngine
from download_manager import DownloadManager
from about import AboutDialog
from settings import SettingsManager

class BrowserTab(QWidget):
    def __init__(self, browser, homepage):
        super().__init__()
        self.browser = browser
        self.layout = QVBoxLayout()
        self.browser_view = QWebEngineView()
        self.layout.addWidget(self.browser_view)
        self.setLayout(self.layout)

        self.browser_view.urlChanged.connect(self.update_url_bar)
        self.browser_view.page().profile().downloadRequested.connect(self.start_download)
        self.browser_view.loadFinished.connect(self.update_tab_title)

        self.navigate_to_url(homepage)

    def navigate_to_url(self, url):
        if not (url.startswith("http://") or url.startswith("https://")):
            url = "https://" + url
        self.browser_view.setUrl(QUrl(url))

    def update_url_bar(self, q):
        self.browser.url_bar.setText(q.toString())

    def start_download(self, download: QWebEngineDownloadRequest):
        self.browser.download_manager.start_download(download)

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
        self.setWindowTitle("Saffari For Desktop")
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
        downloads_action = QAction("Download Manager", self)
        settings_action = QAction("Settings...", self)
        about_action = QAction("About Saffari For Desktop", self)
        
        downloads_action.triggered.connect(self.show_downloads)
        settings_action.triggered.connect(self.show_settings)
        about_action.triggered.connect(self.show_about_dialog)
        
        hamburger_menu.addAction(downloads_action)
        hamburger_menu.addAction(settings_action)
        hamburger_menu.addAction(about_action)

        hamburger_button = QToolButton(self)
        hamburger_button.setText("☰")
        hamburger_button.setMenu(hamburger_menu)
        hamburger_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        hamburger_button.clicked.connect(lambda: hamburger_menu.exec(hamburger_button.mapToGlobal(hamburger_button.rect().bottomLeft())))
        self.navbar.addWidget(hamburger_button)

    def add_new_tab(self):
        homepage = settings_manager.load_homepage()
        if not homepage:
            homepage = "https://saffaristart.pages.dev"
        new_tab = BrowserTab(self, homepage)
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

    def show_settings(self):
        self.settings_engine = QQmlApplicationEngine()
        self.settings_engine.rootContext().setContextProperty("settingsManager", settings_manager)
        self.settings_engine.load(QUrl.fromLocalFile('settings.qml'))

    def show_about_dialog(self):
        about_dialog = AboutDialog()
        about_dialog.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    settings_manager = SettingsManager()
    window = Browser()
    window.show()
    sys.exit(app.exec())
