from const import categories_lvl
from custom import BaseDataWidget
from PySide2.QtWidgets import QLabel, QHBoxLayout, QComboBox
from sql.query import GET_SPECIALIZATION, ADD_DOCTOR, ADD_SPECIALIST


class Doctor(BaseDataWidget):

    window_label = 'Добавить врача'
    specializations = {}

    def __init__(self):
        BaseDataWidget.__init__(self)
        self.header.setObjectName('DoctorLabel')
        self.set_header_label(self.window_label)

        # Specialization
        self.specializationBox = QHBoxLayout()
        self.specializationLabel = QLabel('Специализация:')
        self.specializationSelect = QComboBox()
        self.specializationSelect.addItem('')
        self.specializationSelect.setFixedWidth(260)
        self.specializationBox.addWidget(self.specializationLabel)
        self.specializationBox.addWidget(self.specializationSelect)

        # Category LVL
        self.catLvlBox = QHBoxLayout()
        self.catLvlLabel = QLabel('Категория:')
        self.catLvlSelect = QComboBox()
        self.catLvlSelect.addItems(categories_lvl)
        self.catLvlSelect.setFixedWidth(260)
        self.catLvlBox.addWidget(self.catLvlLabel)
        self.catLvlBox.addWidget(self.catLvlSelect)

        # QFormLayout add rows
        self.formBox.addRow(self.header)
        self.formBox.addRow(self.surnameBox)
        self.formBox.addRow(self.nameBox)
        self.formBox.addRow(self.patronymicBox)
        self.formBox.addRow(self.specializationBox)
        self.formBox.addRow(self.catLvlBox)
        self.formBox.addRow(self.bdBox)
        self.formBox.addRow(self.err_label)
        self.formBox.addRow(self.formBtnBox)

        # Signals
        self._clean.clicked.connect(self.clear_form)
        self.submit.clicked.connect(self.save_data)

    def clear_form(self):
        self.surnameRow.clear()
        self.nameRow.clear()
        self.patronymicRow.clear()
        self.specializationSelect.setCurrentIndex(0)
        self.catLvlSelect.setCurrentIndex(0)

    def onload(self):
        self.clear_form()
        if not self.specializations:
            self.update_specialization()

    def save_data(self):
        self.err_label.setVisible(False)
        if self.is_valid():
            param = (self.surnameRow.text(),
                     self.nameRow.text(),
                     self.patronymicRow.text(),
                     self.bdRow.date().toPython(),)
            q = self.db.exec_query(ADD_DOCTOR, param=param, retrieve_id=True)
            if not q:
                self.err_label.has_error('Ошибка вставки записи')
                return
            self.db.exec_query(ADD_SPECIALIST, param=(self.specializations.get(self.specializationSelect.currentText()),
                                                      q, self.catLvlSelect.currentText()))
            self.clear_form()

    def is_valid(self):
        self.err_label.refresh()
        if not self.surnameRow.text():
            self.err_label.has_error('Заполните фамилию')
        elif not self.nameRow.text():
            self.err_label.has_error('Заполните имя')
        elif not self.patronymicRow.text():
            self.err_label.has_error('Заполните отчество')
        elif self.specializationSelect.currentIndex() == 0:
            self.err_label.has_error('Укажите специализацию')
        return self.err_label.is_error

    def update_specialization(self):
        data = self.db.exec_query(GET_SPECIALIZATION)
        if data:
            for k, v in data:
                self.specializations[v] = k
                self.specializationSelect.addItem(v)
