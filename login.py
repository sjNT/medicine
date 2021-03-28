from const import proj_path
from custom import ErrorLabel
from PySide2.QtCore import Qt
from types import SimpleNamespace
from sql.query import AUTH_USER, AUTH_USER_DETAILS
from utils import get_stylesheet
from database import DatabaseExecutor
from PySide2.QtGui import QPixmap, QImage
from PySide2.QtWidgets import QDialog, QLabel, QPushButton, QLineEdit, QVBoxLayout


class LoginWindow(QDialog):

    style = 'login.qss'
    db = DatabaseExecutor
    auth_user = {}
    auth_user_details = {}

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle('Авторизация')
        self.setFixedSize(500, 500)
        self.logo_pixmap = QPixmap(QImage(str(proj_path / 'images/logo-login.png')))
        self.logo = QLabel(self)
        self.logo.setFixedSize(100, 100)
        self.logo.move(200, 20)
        self.logo.setPixmap(self.logo_pixmap)
        self.err_label = ErrorLabel()
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
        self.login_row.setText('burnov')
        self.pwd_row.setText('burnov')
        self.auth_btn.clicked.connect(self.auth)

    def auth(self):
        self.err_label.setVisible(False)
        username = self.login_row.text()
        password = self.pwd_row.text()
        user = self.db.exec_query(query=AUTH_USER, param=(username, password,), fetchone=True)
        if not user:
            self.err_label.has_error('Неверное имя пользователя или пароль')
            return False
        self.auth_user['username'] = username
        user_details = self.db.exec_query(AUTH_USER_DETAILS, param=(user[0], ), fetchone=True)
        self.auth_user['user_id'] = user_details[0]
        self.auth_user['user_fullname'] = user_details[1]
        self.auth_user['specialist_id'] = user_details[2]
        self.auth_user_details = SimpleNamespace(**self.auth_user)
        self.accept()
