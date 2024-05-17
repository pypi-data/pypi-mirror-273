from PyQt5 import uic
from PyQt5.QtWidgets import *


class MyGui(QMainWindow):
    def __init__(self):
        super(MyGui, self).__init__()
        uic.loadUi("login_form.ui", self)
        self.show()

        self.login_button.clicked.connect(self.login)
        self.send_button.clicked.connect(self.message)
        self.action_close.triggered.connect(exit)

    def login(self):
        if self.login_field.text() == "User" and self.password_field.text() == "123":
            self.message_text.setEnabled(True)
            self.send_button.setEnabled(True)
        else:
            message = QMessageBox()
            message.setText("Invalid username or password")
            message.setWindowTitle("Invalid Input")
            message.exec_()

    def message(self):
        message = QMessageBox()
        message.setText("Your message send successfully")
        message.setWindowTitle("Message")
        message.exec_()
