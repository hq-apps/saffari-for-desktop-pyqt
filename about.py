#!/usr/bin/env python3
import sys
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton

class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ABOUT saffari!")
        self.setGeometry(300, 300, 400, 200)

        layout = QVBoxLayout()

        about_label = QLabel("Saffari For desktop\nVersion [alpha]\n\n")
        layout.addWidget(about_label)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = AboutDialog()
    dialog.exec()
