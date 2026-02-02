from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from .api_client import APIClient

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login to Chemical Visualizer")
        self.resize(300, 150)
        self.api_client = None
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Username:"))
        self.user_input = QLineEdit()
        layout.addWidget(self.user_input)
        
        layout.addWidget(QLabel("Password:"))
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.pass_input)
        
        btn = QPushButton("Login")
        btn.clicked.connect(self.attempt_login)
        layout.addWidget(btn)
        
        self.setLayout(layout)

    def attempt_login(self):
        username = self.user_input.text()
        password = self.pass_input.text()
        
        client = APIClient()
        if client.login(username, password):
            self.api_client = client
            self.accept()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid credentials")
