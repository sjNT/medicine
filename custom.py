from PySide2.QtCore import Qt
from utils import get_stylesheet
from database import DatabaseExecutor
from PySide2.QtWidgets import QMainWindow, QLabel, QHBoxLayout, QLineEdit, QFormLayout, QWidget, \
    QPushButton, QDateEdit, QTableWidget, QHeaderView, QVBoxLayout, QComboBox, QTextEdit, QTableWidgetItem
from sql.query import GET_TEL_TYPES, INSERT_CONTACTS, INSERT_DIAGNOSIS, ANALYSIS_CONTEXT, ANALYSIS_INSERT
from docxtpl import DocxTemplate
import os
from const import proj_path


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
            self.phone_type_idx.clear()
            self.phone_type.clear()
            for i in data:
                self.phone_type_idx[i[0]] = i[1]
                self.phone_type.addItem(i[1])

    def load(self, patient_idx):
        # if patient_idx:
        self.update_phone_types()
        self.show()
        # data = self.db.exec_query(GET_PATIENT_CONTACTS, param=(patient_idx, ))
        # if data:

    def insert_contacts(self, patient_idx):
        if self.phone_type.currentText() != '' and self.phoneBox.text() != '':
            self.db.exec_query(INSERT_CONTACTS, param=(self.phoneBox.text(),
                                                       self.phone_type_idx.get(self.phone_type.currentText()),
                                                       patient_idx))


class DiagnoseCustom(QWidget):

    style = 'main.qss'
    db = DatabaseExecutor
    idx = None

    def __init__(self):
        QWidget.__init__(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowModal | Qt.ApplicationModal)
        self.formBox = QFormLayout()
        self.valueBox = QHBoxLayout()
        self.valueLabel = QLabel('Введите данные диагноза:')
        self.valueText = QTextEdit()
        self.valueText.setFixedHeight(70)
        self.valueBox.addWidget(self.valueLabel)
        self.valueBox.addWidget(self.valueText)
        self.therapyBox = QHBoxLayout()
        self.therapyLabel = QLabel('Введите терапевтические данные:')
        self.therapy_value = QTextEdit()
        self.therapyBox.addWidget(self.therapyLabel)
        self.therapyBox.addWidget(self.therapy_value)
        self.valueBoxAccept = QPushButton('Сохранить')
        self.valueBoxAccept.setObjectName('SubmitBtn')
        self.formBox.addRow(self.valueBox)
        self.formBox.addRow(self.therapyBox)
        self.formBox.addRow(self.valueBoxAccept)
        self.formBox.setAlignment(Qt.AlignLeft)
        self.formBox.setContentsMargins(20, 20, 20, 20)
        self.formBox.setVerticalSpacing(20)
        self.formBox.setHorizontalSpacing(20)
        self.setLayout(self.formBox)
        self.setMinimumSize(400, 400)
        self.setStyleSheet(get_stylesheet(self.style))

        self.valueBoxAccept.clicked.connect(self.save_data)

    def update_title(self, title):
        self.setWindowTitle(title)

    def load(self, idx=None):
        self.show()
        self.valueText.clear()
        self.therapy_value.clear()
        self.idx = idx

    def save_data(self):
        if self.idx and self.valueText.toPlainText() != '' and self.therapy_value.toPlainText() != '':
            q = self.db.exec_query(INSERT_DIAGNOSIS, param=(self.valueText.toPlainText(),
                                                            self.idx,
                                                            self.therapy_value.toPlainText()), retrieve_id=True)
            if q:
                self.close()


class AnalysisCustom(QWidget):

    style = 'main.qss'
    db = DatabaseExecutor
    idx = None
    spec_id = None

    def __init__(self):
        QWidget.__init__(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowModal | Qt.ApplicationModal)
        self.formBox = QFormLayout()
        self.valueBox = QHBoxLayout()
        self.valueLabel = QLabel('Введите наименование анализа:')
        self.valueText = QLineEdit()
        self.valueBox.addWidget(self.valueLabel)
        self.valueBox.addWidget(self.valueText)
        self.print_dest = QPushButton('Сохранить и распечатать направление')
        self.print_dest.setObjectName('SubmitBtn')
        self.formBox.addRow(self.valueBox)
        self.formBox.addRow(self.print_dest)
        self.formBox.setAlignment(Qt.AlignLeft)
        self.formBox.setContentsMargins(20, 20, 20, 20)
        self.formBox.setVerticalSpacing(20)
        self.formBox.setHorizontalSpacing(20)
        self.setLayout(self.formBox)
        self.setMinimumSize(400, 400)
        self.setStyleSheet(get_stylesheet(self.style))
        self.print_dest.clicked.connect(self.print_template)

    def update_title(self, title):
        self.setWindowTitle(title)

    def load(self, idx=None, spec_id=None):
        self.show()
        self.valueText.clear()
        self.idx = idx
        self.spec_id = spec_id
        print(self.spec_id, self.idx)

    def save_data(self):

        self.db.exec_query(ANALYSIS_INSERT, param=(self.valueText.text(), self.spec_id, self.idx, ))

    def print_template(self):
        if self.idx and self.valueText.text() != '':
            self.save_data()
            template = DocxTemplate(str(proj_path / 'templates/template_analysis.docx'))
            context = self.db.exec_query(ANALYSIS_CONTEXT, param=(self.idx,), dictionary=True)[0]
            template.render(context=context)
            filename = str(proj_path / 'analysis/analysis.docx')
            template.save(filename)
            os.startfile(filename, 'print')
        self.close()

