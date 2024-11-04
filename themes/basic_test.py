import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QCheckBox,
    QPushButton, QMessageBox
)


class CommandRunnerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Command Runner')

        # Layout
        layout = QVBoxLayout()

        # Checkboxes for each command
        self.sitl_checkbox = QCheckBox("Run 'sudo make px4_sitl jsbsim_kp2'")
        self.qground_checkbox = QCheckBox("Run QGroundControl")
        self.python_checkbox = QCheckBox("Run Python Script")
        self.exe_checkbox = QCheckBox("Run Blocks.exe")

        layout.addWidget(self.sitl_checkbox)
        layout.addWidget(self.qground_checkbox)
        layout.addWidget(self.python_checkbox)
        layout.addWidget(self.exe_checkbox)

        # Button to run commands
        run_button = QPushButton("Run Selected Commands")
        run_button.clicked.connect(self.run_commands)

        layout.addWidget(run_button)

        self.setLayout(layout)

    def run_commands(self):
        commands = []

        # Use the specified path inside Docker for the PX4 command
        if self.sitl_checkbox.isChecked():
            commands.append('docker exec -it myat_vdt /bin/bash -c "cd /home/myattoe/PX4-Autopilot && sudo make px4_sitl jsbsim_kp2"')
        
        if self.qground_checkbox.isChecked():
            commands.append('start cmd /k "qgroundcontrol"')
        
        if self.python_checkbox.isChecked():
            commands.append('start cmd /k "python F:\\Demonstration-System\\Portal\\Multiple\\RealTimeACT_DIFF_VFR_POS_ATT.py"')
        
        if self.exe_checkbox.isChecked():
            commands.append('start cmd /k "F:\\Demonstration-System\\Unreal Engine executable\\without corridor\\20241022\\20241022\\WindowsNoEditor\\Blocks.exe"')

        if not commands:
            QMessageBox.warning(self, "No Selection", "Please select at least one command to run.")
            return

        for command in commands:
            subprocess.Popen(command, shell=True)

        QMessageBox.information(self, "Success", "Selected commands are running in separate terminals.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CommandRunnerApp()
    ex.resize(400, 200)
    ex.show()
    sys.exit(app.exec_())
