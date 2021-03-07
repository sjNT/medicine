from PySide2.QtWidgets import QMainWindow, QFormLayout, QWidget, QLabel, QTableWidgetItem, QPushButton
from custom import TableWidget, ErrorLabel
from utils import get_stylesheet
from PySide2.QtCore import Qt
from database import DatabaseExecutor
from sql.query import GET_PATIENT_LIST


class PatientRecords(QMainWindow):

    window_label = 'Пациенты'
    headers = ['#', 'ФИО', 'Дата рождения', 'Серия полиса', 'Номер полиса', '']
    style = 'main.qss'
    db = DatabaseExecutor

    def __init__(self):
        QMainWindow.__init__(self)
        self.formBox = QFormLayout()
        self.table = TableWidget()
        self.table.update_headers(self.headers)
        self.formWidget = QWidget()
        self.err_label = ErrorLabel()
        self.header = QLabel(self.window_label)
        self.header.setObjectName('AllPatientLabel')
        self.header.setMinimumWidth(200)
        self.header.setContentsMargins(0, 0, 0, 50)

        self.formBox = QFormLayout()
        self.formBox.addRow(self.header)
        self.formBox.addRow(self.table)
        self.formBox.addRow(self.err_label)
        # QFormLayout settings
        self.formBox.setContentsMargins(20, 20, 20, 20)
        self.formBox.setVerticalSpacing(20)
        self.formBox.setHorizontalSpacing(20)
        self.formBox.setAlignment(Qt.AlignLeft)
        self.formWidget.setLayout(self.formBox)
        self.setStyleSheet(get_stylesheet(self.style))
        self.setCentralWidget(self.formWidget)

    def onload(self):
        data = self.db.exec_query(GET_PATIENT_LIST)
        self.table.setRowCount(0)
        self.table.setRowCount(len(data))
        print(data)
        for row in range(len(data)):
            for column in range(len(data[row])):
                print(str(data[row][column]))
                self.table.setItem(row, column, QTableWidgetItem(str(data[row][column])))
            editBtn = QPushButton('Редактировать')
            editBtn.setProperty("row", data[row][0])
            editBtn.clicked.connect(self.edit_patient)

            # editBtn.setObjectName(f'editPatient#{data[row][0]}')
            self.table.setCellWidget(row, 5, editBtn)

                #self.table.item(row, column).setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

    def edit_patient(self):
        sender = self.sender()
        patient_idx = sender.property("row")

