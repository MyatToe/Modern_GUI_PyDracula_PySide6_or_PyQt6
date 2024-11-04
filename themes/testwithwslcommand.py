import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

class WSLGui(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.open_wsl_button = QPushButton('Open WSL', self)
        self.open_wsl_button.clicked.connect(self.open_wsl)

        layout.addWidget(self.open_wsl_button)
        self.setLayout(layout)

        self.setWindowTitle('WSL GUI')
        self.show()

    def open_wsl(self):
        subprocess.run(['start', 'cmd', '/k', 'wsl.exe -d Ubuntu-20.04 -- bash -c'], shell=True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WSLGui()
    sys.exit(app.exec_())