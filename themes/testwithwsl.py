import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QPushButton, QMessageBox
from getpass import getpass

class CommandRunnerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Command Runner")
        layout = QVBoxLayout()

        self.sitl_checkbox = QCheckBox("Run PX4 SITL")
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

        # Use WSL for the PX4 command
        if self.sitl_checkbox.isChecked():
            password = getpass("Enter your sudo password: ")
            wsl_command = (
                'start cmd /k wsl.exe -d Ubuntu-20.04 -- bash -c '
                f'"cd /home/myattoe/PX4-Autopilot && echo \'{password}\' | sudo -S make px4_sitl jsbsim_kp2; exec bash"'
            )
            commands.append(wsl_command)

        # Introduce a delay before running QGroundControl
        if self.qground_checkbox.isChecked():
            qground_command = (
                'start cmd /k timeout 10 >nul && wsl.exe -d Ubuntu-20.04 bash -c "cd /home/myattoe && ./QGroundControl.AppImage; exec bash"'
            )
            commands.append(qground_command)
        
        if self.python_checkbox.isChecked():
            python_command = (
                'start cmd /k '
                '"python F:\\Demonstration-System\\Portal\\Multiple\\RealTimeACT_DIFF_VFR_POS_ATT.py & pause"'
            )
            commands.append(python_command)
        
        if self.exe_checkbox.isChecked():
            exe_command = (
                'start cmd /k '
                '"F:\\Demonstration-System\\Unreal Engine executable\\without corridor\\20241022\\20241022\\WindowsNoEditor\\Blocks.exe & pause"'
            )
            commands.append(exe_command)

        if not commands and not self.sitl_checkbox.isChecked():
            QMessageBox.warning(self, "No Selection", "Please select at least one command to run.")
            return

        # Run the commands in parallel
        processes = [subprocess.Popen(command, shell=True) for command in commands]

        QMessageBox.information(self, "Success", "Selected commands are running in separate terminals.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CommandRunnerApp()
    ex.resize(400, 200)
    ex.show()
    sys.exit(app.exec())