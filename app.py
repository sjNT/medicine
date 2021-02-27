from login import LoginWindow
from sql.query import *
from PySide2.QtWidgets import QMainWindow, QApplication, QDialog


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setMinimumSize(500, 500)
        self.setWindowTitle('')


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    login = LoginWindow()
    if login.exec_() == QDialog.Accepted:
        main = MainWindow()
        main.show()
    sys.exit(app.exec_())
