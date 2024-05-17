from PyQt5.QtWidgets import *

from apex_dojo.pyQt.login_form.login_form import MyGui


def main():
    app = QApplication([])
    window = MyGui()
    app.exec_()


if __name__ == "__main__":
    main()
