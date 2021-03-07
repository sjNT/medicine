from PySide2.QtCore import Qt
from utils import get_stylesheet
from database import DatabaseExecutor
from PySide2.QtWidgets import QMainWindow, QLabel, QHBoxLayout, QLineEdit, QFormLayout, QWidget, \
    QPushButton, QDateEdit, QTableWidget, QHeaderView, QVBoxLayout, QComboBox
from sql.query import GET_TEL_TYPES, GET_PATIENT_CONTACTS, INSERT_CONTACTS


class ErrorLabel(QLabel):

    is_error = True

    def __init__(self):
        QLabel.__init__(self)
        self.setObjectName('ErrLabel')
        self.setVisible(False)
        self.setWordWrap(True)
        self.setFixedSize(200, 25)

    def has_error(self, error):
        self.setText(error)
        self.setVisible(True)
        self.is_error = False

    def refresh(self):
        self.setText('')
        self.setVisible(False)
        self.is_error = True


class BaseDataWidget(QMainWindow):

    style = 'main.qss'
    db = DatabaseExecutor

    def __init__(self):
        QMainWindow.__init__(self)
        self.formWidget = QWidget()
        self.err_label = ErrorLabel()
        self.header = QLabel()
        self.header.setMinimumWidth(200)
        self.header.setContentsMargins(0, 0, 0, 50)
        self.setStyleSheet(get_stylesheet(self.style))
        self.formBox = QFormLayout()

        # Surname
        self.surnameBox = QHBoxLayout(self)
        self.surnameLabel = QLabel('Фамилия:')
        self.surnameRow = QLineEdit()
        self.surnameRow.setFixedWidth(280)
        self.surnameBox.addWidget(self.surnameLabel)
        self.surnameBox.addWidget(self.surnameRow)

        # Name
        self.nameBox = QHBoxLayout(self)
        self.nameLabel = QLabel('Имя:')
        self.nameRow = QLineEdit()
        self.nameRow.setFixedWidth(280)
        self.nameBox.addWidget(self.nameLabel)
        self.nameBox.addWidget(self.nameRow)

        # Patronymic
        self.patronymicBox = QHBoxLayout()
        self.patronymicLabel = QLabel('Отчество:')
        self.patronymicRow = QLineEdit()
        self.patronymicRow.setFixedWidth(280)
        self.patronymicBox.addWidget(self.patronymicLabel)
        self.patronymicBox.addWidget(self.patronymicRow)

        # Birth date
        self.bdBox = QHBoxLayout()
        self.bdLabel = QLabel('Дата рождения:')
        self.bdRow = QDateEdit()
        self.bdBox.addWidget(self.bdLabel)
        self.bdBox.addWidget(self.bdRow)

        self.formBtnBox = QHBoxLayout()
        self.formBtnBox.setAlignment(Qt.AlignRight)

        # Submit
        self.submit = QPushButton('Сохранить')
        self.submit.setObjectName('SubmitBtn')
        self.submit.setFixedSize(100, 30)
        self.submit.setCursor(Qt.PointingHandCursor)
        self.formBtnBox.addWidget(self.submit)

        # Clean form
        self._clean = QPushButton('Очистить')
        self._clean.setObjectName('CleanBtn')
        self._clean.setFixedSize(100, 30)
        self._clean.setCursor(Qt.PointingHandCursor)
        self.formBtnBox.addWidget(self._clean)

        # QFormLayout settings
        self.formBox.setContentsMargins(20, 20, 20, 20)
        self.formBox.setVerticalSpacing(20)
        self.formBox.setHorizontalSpacing(20)
        self.formBox.setAlignment(Qt.AlignLeft)
        self.formWidget.setMaximumWidth(420)
        self.formWidget.setLayout(self.formBox)
        self.setCentralWidget(self.formWidget)

    def set_header_label(self, label):
        self.header.setText(label)


class TableWidget(QTableWidget):

    style = 'main.qss'

    def __init__(self):
        QTableWidget.__init__(self)
        self.tabHeaders = self.horizontalHeader()
        self.verticalHeader().setVisible(False)
        self.tabHeaders.setDefaultAlignment(Qt.AlignTop | Qt.AlignVCenter | Qt.AlignCenter)
        """
        self.tabHeaders.setResizeMode(0, QHeaderView.ResizeToContents)
        self.tabHeaders.setResizeMode(1, QHeaderView.Stretch)
        """
        self.setStyleSheet(get_stylesheet(self.style))

    def update_headers(self, headers):
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        for i in range(len(headers)):
            self.tabHeaders.setSectionResizeMode(i, QHeaderView.Stretch)


class ContactWidget(QWidget):

    style = 'main.qss'
    db = DatabaseExecutor
    phone_type_idx = {}

    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('Добавить контакт')
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowModal | Qt.ApplicationModal)
        self.formBox = QFormLayout()

        # Phone type
        self.phone_typeBox = QHBoxLayout()
        self.phone_typeLabel = QLabel('Тип телефона:')
        self.phone_type = QComboBox()
        self.phone_type.setFixedWidth(280)
        self.phone_typeBox.addWidget(self.phone_typeLabel)
        self.phone_typeBox.addWidget(self.phone_type)

        # Phone
        self.phoneBox = QHBoxLayout()
        self.phoneLabel = QLabel('Телефон:')
        self.phoneRow = QLineEdit()
        self.phoneRow.setFixedWidth(280)
        self.phoneBox.addWidget(self.phoneLabel)
        self.phoneBox.addWidget(self.phoneRow)

        # Save
        self.savebtn = QPushButton('Сохранить')
        self.savebtn.setObjectName('SubmitBtn')

        self.formBox.addRow(self.phone_typeBox)
        self.formBox.addRow(self.phoneBox)
        self.formBox.addRow(self.savebtn)
        self.setLayout(self.formBox)
        self.setStyleSheet(get_stylesheet(self.style))
        # self.setFixedWidth(400)

    def update_phone_types(self):
        data = self.db.exec_query(GET_TEL_TYPES)
        if data:
            print(data)
            self.phone_type_idx.clear()
            self.phone_type.clear()
            for i in data:
                self.phone_type_idx[i[0]] = i[1]
                self.phone_type.addItem(i[1])
            print(self.phone_type_idx)

    def load(self, patient_idx):
        #if patient_idx:
        self.update_phone_types()
        self.show()
        # data = self.db.exec_query(GET_PATIENT_CONTACTS, param=(patient_idx, ))
        #if data:

    def insert_contacts(self, patient_idx):
        if self.phone_type.currentText() != '' and self.phoneBox.text() != '':
            self.db.exec_query(INSERT_CONTACTS, param=(self.phoneBox.text(),
                                                       self.phone_type_idx.get(self.phone_type.currentText()),
                                                       patient_idx))
