import sys
import os
import subprocess
from PyQt5.QtCore import Qt, QProcess, QUrl
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QTextEdit, QFileSystemModel, QTreeView, QStackedWidget, QMainWindow, QSplitter, QLineEdit, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView
import win32com.client

RETRO_STYLE = """
    QWidget {
        background-color: black;
        color: #00FFFF;
    }
    QComboBox, QPushButton, QTreeView {
        background-color: black;
        color: #00FFFF;
        border: 1px solid #00FFFF;
    }
    QTextEdit, QLineEdit {
        background-color: black;
        color: #00FFFF;
        border: 1px solid #00FFFF;
    }
    QTreeView::item:selected {
        background-color: #00FFFF;
        color: black;
    }
"""

if getattr(sys, 'frozen', False):  # Check if running as an executable
    base_path = sys._MEIPASS  # Directory where PyInstaller bundles files
else:
    base_path = os.path.dirname(os.path.abspath(__file__))  # Directory of the script


file_path = os.path.join(base_path, "music.mp3")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Desktop Environment")
        self.setGeometry(0, 0, 1920, 1080)
        self.setStyleSheet(RETRO_STYLE)

        self.music_player = win32com.client.Dispatch("WMPlayer.OCX")
        self.music_player.URL = os.path.join(base_path, "media/music.mp3")
        self.music_player.settings.volume = 100
        self.is_muted = False
        self.process = None
        self.music_player.settings.setMode("loop", True)
        self.music_player.controls.play()

        self.create_taskbar()
        self.create_browser_media_player_window()
        self.create_file_explorer_window()
        self.create_terminal_window()
        self.arrange_layout()
        
    def closeEvent(self, event):
        self.cleanup()
        event.accept()

    def cleanup(self):
        if self.process and self.process.state() == QProcess.Running:
            self.process.terminate()
            self.process.waitForFinished(10)
        if self.process:
            self.process.deleteLater()

    def create_taskbar(self):
        self.taskbar = QWidget(self)
        self.taskbar.setStyleSheet("background-color: #333333; height: 50px;")
        self.taskbar_layout = QHBoxLayout(self.taskbar)

        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.web_browser_back)
        self.taskbar_layout.addWidget(self.back_button)

        self.forward_button = QPushButton("Forward", self)
        self.forward_button.clicked.connect(self.web_browser_forward)
        self.taskbar_layout.addWidget(self.forward_button)

        self.mute_button = QPushButton("Mute", self)
        self.mute_button.clicked.connect(self.toggle_mute)
        self.taskbar_layout.addWidget(self.mute_button)

        self.toggle_button = QPushButton("Toggle Web Browser/Media Player", self)
        self.toggle_button.clicked.connect(self.toggle_browser_media_player)
        self.taskbar_layout.addWidget(self.toggle_button)

        self.power_off_button = QPushButton("Power Off", self)
        self.power_off_button.clicked.connect(self.close)
        self.taskbar_layout.addWidget(self.power_off_button)

    def toggle_mute(self):
        self.is_muted = not self.is_muted
        self.music_player.settings.mute = self.is_muted
        self.mute_button.setText("Unmute" if self.is_muted else "Mute")

    def web_browser_back(self):
        if self.web_browser_window.history().canGoBack():
            self.web_browser_window.back()

    def web_browser_forward(self):
        if self.web_browser_window.history().canGoForward():
            self.web_browser_window.forward()
            
    def create_browser_media_player_window(self):
        self.stacked_widget = QStackedWidget(self)

        self.web_browser_window = QWebEngineView(self)
        self.web_browser_window.setUrl(QUrl("https://www.google.com"))
        self.stacked_widget.addWidget(self.web_browser_window)

        self.media_player_window = QLabel(self)
        self.media_player_window.setText("Media Player - Placeholder")
        self.stacked_widget.addWidget(self.media_player_window)

    def create_file_explorer_window(self):
        self.file_explorer_view = QTreeView(self)
        self.file_system_model = QFileSystemModel()

        script_directory = os.path.dirname(os.path.abspath(__file__))
        self.file_system_model.setRootPath(script_directory)

        self.file_explorer_view.setModel(self.file_system_model)
        self.file_explorer_view.setRootIndex(self.file_system_model.index(script_directory))
        self.file_explorer_view.setSelectionMode(QTreeView.SingleSelection)
        self.file_explorer_view.clicked.connect(self.file_explorer_item_clicked)

    def create_terminal_window(self):
        self.terminal_window = QTextEdit(self)
        self.terminal_window.setReadOnly(True)

        self.terminal_input = QLineEdit(self)
        self.terminal_input.setPlaceholderText("Type a command and press Enter...")

        terminal_layout = QVBoxLayout()
        terminal_layout.addWidget(self.terminal_window)
        terminal_layout.addWidget(self.terminal_input)

        self.terminal_container = QWidget(self)
        self.terminal_container.setLayout(terminal_layout)

        self.start_terminal()

        self.terminal_input.returnPressed.connect(self.send_command_to_terminal)

    def start_terminal(self):
        self.process = QProcess(self)

        if os.name == "nt":
            script_path = os.path.join(base_path, "terminal.py")

            if not os.path.exists(script_path):
                print(f"Error: {script_path} not found!")
                return

            self.process.setProgram("cmd.exe")
            self.process.setArguments(["/c", "python", script_path])

        else:
            script_path = os.path.join(base_path, "terminal.py")
            self.process.setProgram("bash")
            self.process.setArguments(["-c", f"python {script_path}"])

        self.process.readyReadStandardOutput.connect(self.read_terminal_output)
        self.process.readyReadStandardError.connect(self.read_terminal_output)
        self.process.start()

    def read_terminal_output(self):
        output = self.process.readAllStandardOutput().data()
        error = self.process.readAllStandardError().data()

        output_decoded = self.safe_decode(output)
        error_decoded = self.safe_decode(error)

        self.terminal_window.append(output_decoded + error_decoded)

    def safe_decode(self, byte_data):
        try:
            return byte_data.decode('utf-8')
        except UnicodeDecodeError:
            return byte_data.decode('utf-8', errors='ignore')

    def send_command_to_terminal(self):
        command = self.terminal_input.text().strip()
        if command:
            self.process.write((command + "\n").encode('utf-8'))
            self.terminal_input.clear()

    def arrange_layout(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        main_layout.addWidget(self.taskbar)

        vertical_splitter = QSplitter(Qt.Vertical)

        top_splitter = QSplitter(Qt.Horizontal)

        top_splitter.addWidget(self.stacked_widget)

        top_splitter.addWidget(self.terminal_container)
        top_splitter.setSizes([1500, 500])

        vertical_splitter.addWidget(top_splitter)

        self.file_explorer_view.setMaximumHeight(300)
        vertical_splitter.addWidget(self.file_explorer_view)

        vertical_splitter.setSizes([1500, 300])

        main_layout.addWidget(vertical_splitter)

    def toggle_browser_media_player(self):
        current_index = self.stacked_widget.currentIndex()
        next_index = 1 if current_index == 0 else 0
        self.stacked_widget.setCurrentIndex(next_index)

    def file_explorer_item_clicked(self, index):
        file_path = self.file_system_model.filePath(index)

        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            self.show_image_in_media_player(file_path)
        elif file_path.lower().endswith(('.mp3', '.mp4', '.avi', '.mov')):
            self.play_media(file_path)

    def show_image_in_media_player(self, file_path):
        pixmap = QPixmap(file_path)
        media_player_size = self.media_player_window.size()

        scaled_pixmap = pixmap.scaled(media_player_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.media_player_window.setPixmap(scaled_pixmap)

    def play_media(self, file_path):
        try:
            wmp = win32com.client.Dispatch("WMPlayer.OCX")
            wmp.URL = file_path
            wmp.controls.play()
        except Exception as e:
            print(f"Error playing media: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showFullScreen()
    sys.exit(app.exec_())
