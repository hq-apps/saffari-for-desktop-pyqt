import subprocess
import sys
import webbrowser

# Shared strings
error_message = (
    "OH NOTZ! it looks like saffari for decstop crashed!!! were so sorry and hope this will not hapen again!! :((\n"
    "plz copy the crash log and open a gh issue so we can inestigate ur problem and fix it :) \n"
    "thx u so much!!\n"
)
github_issue_url = "https://github.com/hq-apps/saffari-for-desktop-pyqt/issues/new?title={title}&body={body}"

# Window titles
tkinter_window_title = "SAFFARI crash reporter!! were so sorry!! :(( (Tkinter mode)"
pyqt6_window_title = "SAFFARI crash reporter!! were so sorry!! :(( (PyQt6 mode)"

def run_script():
    try:
        result = subprocess.run([sys.executable, 'browser.py'], cwd='browser', capture_output=True, text=True)
        if result.returncode != 0:
            show_logs(result.stdout, result.stderr)
    except Exception as e:
        show_logs("", str(e))

def show_logs(stdout, stderr):
    print("saffari crashed, opening crash reporter...")
    try:
        import tkinter as tk
        from tkinter import scrolledtext, messagebox

        print("crash reporter: opening in tkinter mode")

        def show_warning_popup():
            messagebox.showwarning("Privacy Warning", "Make sure that the crash report doesn't contain any personal information before submitting it. It could, for example, contain information like your user name in file paths.")

        class CrashReporter(tk.Tk):
            def __init__(self, stdout, stderr):
                super().__init__()
                self.title(tkinter_window_title)
                self.geometry("800x650")

                error_label = tk.Label(self, text=error_message, justify=tk.LEFT)
                error_label.pack(pady=10)

                text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=100, height=30)
                text_area.pack(padx=10, pady=10)
                text_area.insert(tk.END, "Standard Output:\n" + stdout + "\n")
                text_area.insert(tk.END, "Standard Error:\n" + stderr + "\n")
                text_area.config(state=tk.DISABLED)

                copy_button = tk.Button(self, text="copy text", command=lambda: self.copy_to_clipboard(stdout, stderr), width=50)
                copy_button.pack(pady=5, fill=tk.X)

                open_issue_button = tk.Button(self, text="open gh issue in default browser", command=lambda: self.open_github_issue(stdout, stderr), width=50)
                open_issue_button.pack(pady=5, fill=tk.X)

                relaunch_button = tk.Button(self, text="relaunch saffari", command=self.relaunch_script, width=50, bg="lightblue")
                relaunch_button.pack(pady=5, fill=tk.X)

            def copy_to_clipboard(self, stdout, stderr):
                self.clipboard_clear()
                self.clipboard_append(f"Standard Output:\n{stdout}\nStandard Error:\n{stderr}\n")
                messagebox.showinfo("Copied", "Crash log copied to clipboard!")

            def open_github_issue(self, stdout, stderr):
                show_warning_popup()
                title = "Crash Report"
                body = f"**Steps to reproduce:**\n\n**Standard Output:**\n{stdout}\n\n**Standard Error:**\n{stderr}"
                formatted_url = github_issue_url.format(title=title, body=body)
                webbrowser.open(formatted_url)

            def relaunch_script(self):
                self.destroy()
                subprocess.Popen([sys.executable, __file__])

        app = CrashReporter(stdout, stderr)
        app.mainloop()

    except ImportError:
        from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton, QLabel, QMessageBox
        from PyQt6.QtGui import QFont, QGuiApplication

        print("crash reporter: falling back to pyqt6 mode since tkinter isn't configured on your system. ")

        def show_warning_popup():
            QMessageBox.warning(None, "Privacy Warning", "Make sure that the crash report doesn't contain any personal information before submitting it. It could, for example, contain information like your user name in file paths.")

        class CrashReporter(QMainWindow):
            def __init__(self, stdout, stderr):
                super().__init__()
                self.setWindowTitle(pyqt6_window_title)
                self.setGeometry(100, 100, 800, 650)

                layout = QVBoxLayout()

                error_label = QLabel(error_message)
                layout.addWidget(error_label)

                text_edit = QTextEdit()
                text_edit.setReadOnly(True)

                font = QFont()
                font.setStyleHint(QFont.StyleHint.Monospace)
                font.setFamily("Courier New, Courier, monospace")
                text_edit.setFont(font)

                text_edit.append("Standard Output:\n" + stdout + "\n")
                text_edit.append("Standard Error:\n" + stderr + "\n")

                layout.addWidget(text_edit)

                copy_button = QPushButton("copy text")
                copy_button.clicked.connect(lambda: self.copy_to_clipboard(stdout, stderr))
                layout.addWidget(copy_button)

                open_issue_button = QPushButton("open gh issue in default browser")
                open_issue_button.clicked.connect(lambda: self.open_github_issue(stdout, stderr))
                layout.addWidget(open_issue_button)

                relaunch_button = QPushButton("relaunch saffari")
                relaunch_button.clicked.connect(self.relaunch_script)
                relaunch_button.setDefault(True)
                layout.addWidget(relaunch_button)

                container = QWidget()
                container.setLayout(layout)
                self.setCentralWidget(container)

            def copy_to_clipboard(self, stdout, stderr):
                clipboard = QGuiApplication.clipboard()
                clipboard.setText(f"Standard Output:\n{stdout}\nStandard Error:\n{stderr}\n")
                QMessageBox.information(self, "Copied", "Crash log copied to clipboard!")

            def open_github_issue(self, stdout, stderr):
                show_warning_popup()
                title = "Crash Report"
                body = f"**Steps to reproduce:**\n\n**Standard Output:**\n{stdout}\n\n**Standard Error:**\n{stderr}"
                formatted_url = github_issue_url.format(title=title, body=body)
                webbrowser.open(formatted_url)

            def relaunch_script(self):
                self.close()
                subprocess.Popen([sys.executable, __file__])

        app = QApplication(sys.argv)
        reporter = CrashReporter(stdout, stderr)
        reporter.show()
        sys.exit(app.exec())

if __name__ == "__main__":
    run_script()
