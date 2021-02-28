from custom import BaseDataWidget
from PySide2.QtWidgets import QLabel, QHBoxLayout, QComboBox, QLineEdit
from sql.query import ADD_PATIENT


class Patient(BaseDataWidget):

    window_label = 'Добавить пациента'

    def __init__(self):
        BaseDataWidget.__init__(self)
        self.header.setObjectName('PatientLabel')
        self.set_header_label(self.window_label)

        # Gender
        self.genderBox = QHBoxLayout()
        self.genderLabel = QLabel('Пол:')
        self.genderSelect = QComboBox()
        self.genderSelect.addItems(['', 'М', 'Ж'])
        self.genderSelect.setFixedWidth(260)
        self.genderBox.addWidget(self.genderLabel)
        self.genderBox.addWidget(self.genderSelect)

        # Doc series
        self.seriesBox = QHBoxLayout(self)
        self.seriesLabel = QLabel('Серия полиса:')
        self.seriesRow = QLineEdit()
        self.seriesRow.setFixedWidth(280)
        self.seriesBox.addWidget(self.seriesLabel)
        self.seriesBox.addWidget(self.seriesRow)

        # Doc number
        self.numberBox = QHBoxLayout(self)
        self.numberLabel = QLabel('Номер полиса:')
        self.numberRow = QLineEdit()
        self.numberRow.setFixedWidth(280)
        self.numberBox.addWidget(self.numberLabel)
        self.numberBox.addWidget(self.numberRow)

        # QFormLayout add rows
        self.formBox.addRow(self.header)
        self.formBox.addRow(self.surnameBox)
        self.formBox.addRow(self.nameBox)
        self.formBox.addRow(self.patronymicBox)
        self.formBox.addRow(self.bdBox)
        self.formBox.addRow(self.genderBox)
        self.formBox.addRow(self.seriesBox)
        self.formBox.addRow(self.numberBox)
        self.formBox.addRow(self.err_label)
        self.formBox.addRow(self.formBtnBox)

        # Signals
        self._clean.clicked.connect(self.clear_form)
        self.submit.clicked.connect(self.save_data)

    def onload(self):
        self.clear_form()

    def clear_form(self):
        self.surnameRow.clear()
        self.nameRow.clear()
        self.patronymicRow.clear()
        self.bdRow.clear()
        self.genderSelect.setCurrentIndex(0)
        self.seriesRow.clear()
        self.numberRow.clear()

    def save_data(self):
        self.err_label.setVisible(False)
        if self.is_valid():
            param = (self.surnameRow.text(),
                     self.nameRow.text(),
                     self.bdRow.date().toPython(),
                     self.genderSelect.currentText(),
                     self.seriesRow.text(),
                     self.numberRow.text(),)
            q = self.db.exec_query(ADD_PATIENT, param=param, retrieve_id=True)
            if not q:
                self.err_label.has_error('Ошибка создания пациента')
                return
            self.clear_form()

    def is_valid(self):
        self.err_label.refresh()
        if not self.surnameRow.text():
            self.err_label.has_error('Заполните фамилию')
        elif not self.nameRow.text():
            self.err_label.has_error('Заполните имя')
        elif not self.patronymicRow.text():
            self.err_label.has_error('Заполните отчество')
        elif self.genderSelect.currentIndex() == 0:
            self.err_label.has_error('Укажите пол пациента')
        elif self.seriesRow.text() == '':
            self.err_label.has_error('Заполните серию полиса')
        elif self.numberRow.text() == '':
            self.err_label.has_error('Заполните номер полиса')
        return self.err_label.is_error
