from PySide2.QtWidgets import QDialog, QLabel, QPushButton, QLineEdit, QVBoxLayout
from utils import get_stylesheet
from const import proj_path
from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QPixmap, QImage


class LoginWindow(QDialog):

    style = 'login.qss'

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle('Авторизация')
        self.setFixedSize(500, 500)
        self.logo_pixmap = QPixmap(QImage(str(proj_path / 'images/logo-login.png')))
        self.logo = QLabel(self)
        self.logo.setFixedSize(100, 100)
        self.logo.move(200, 20)
        self.logo.setPixmap(self.logo_pixmap)
        self.err_label = QLabel()
        self.err_label.setObjectName('ErrLabel')
        self.err_label.setVisible(False)
        self.err_label.setWordWrap(True)
        self.err_label.setFixedSize(200, 25)
        self.login_row = QLineEdit(self)
        self.login_row.setPlaceholderText('Логин')
        self.pwd_row = QLineEdit(self)
        self.pwd_row.setPlaceholderText('Пароль')
        self.pwd_row.setEchoMode(QLineEdit.Password)
        self.login_row.setFixedSize(200, 30)
        self.pwd_row.setFixedSize(200, 30)
        self.auth_btn = QPushButton('Войти', self)
        self.v_box = QVBoxLayout()
        self.v_box.setSpacing(10)
        self.v_box.setAlignment(Qt.AlignCenter)
        self.v_box.addWidget(self.login_row)
        self.v_box.addWidget(self.pwd_row)
        self.v_box.addWidget(self.err_label)
        self.v_box.addWidget(self.auth_btn)
        self.setStyleSheet(get_stylesheet(self.style))
        self.setLayout(self.v_box)
        self.auth_btn.clicked.connect(self.auth)

    def auth(self):
        self.err_label.setVisible(False)
        user = self.login_row.text()
        password = self.pwd_row.text()
        if not user:
            self.has_error('Введите ваш логин')
        elif not password:
            self.has_error('Введите ваш пароль')
        else:
            self.has_error('Неверное имя пользователя или пароль')

    def has_error(self, error):
        self.err_label.setText(error)
        self.err_label.setVisible(True)