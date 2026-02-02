import sys
from PyQt5.QtWidgets import QApplication, QDialog
from ui.dashboard import Dashboard
from ui.login import LoginDialog

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Show Login
    login = LoginDialog()
    if login.exec_() == QDialog.Accepted:
        # Proceed regardless of input for now, or validate if API supports it
        window = Dashboard()
        window.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)
