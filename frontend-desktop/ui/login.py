from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login to Chemical Visualizer")
        self.resize(300, 150)
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Username:"))
        self.user_input = QLineEdit()
        layout.addWidget(self.user_input)
        
        layout.addWidget(QLabel("Password:"))
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.pass_input)
        
        btn = QPushButton("Login")
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)
        
        self.setLayout(layout)
