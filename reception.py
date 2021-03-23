from PySide2.QtCore import Qt
from utils import get_stylesheet
from const import proj_path
from database import DatabaseExecutor
from PySide2.QtWidgets import QMainWindow, QLabel, QHBoxLayout, QLineEdit, QFormLayout, QWidget, \
    QPushButton, QDateEdit, QTableWidget, QHeaderView, QVBoxLayout, QComboBox, QTextEdit
from PySide2.QtGui import QIcon
from PySide2.QtCore import SIGNAL
from sql.query import GET_TEL_TYPES, GET_PATIENT_CONTACTS, INSERT_CONTACTS


class ReceptionWidget(QMainWindow):

    style = 'main.qss'
    db = DatabaseExecutor
    window_label = 'Прием пациента'

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.formWidget = QWidget()
        self.header = QLabel(self.window_label)
        self.header.setObjectName('ReceptionLabel')
        self.header.setMinimumWidth(200)
        self.header.setContentsMargins(0, 0, 0, 50)
        self.setStyleSheet(get_stylesheet(self.style))
        self.formBox = QFormLayout()
        self.formWidget = QWidget()

        # Patient
        self.patientSelectBox = QHBoxLayout()
        self.patientSelectLabel = QLabel('Выбор пациента:')
        self.patientSelect = QComboBox()
        self.patientSelectBox.addWidget(self.patientSelectLabel)
        self.patientSelectBox.addWidget(self.patientSelect)
        self.patientSelectBox.setAlignment(Qt.AlignLeft)

        # Complaint
        self.complaintBox = QHBoxLayout()
        self.complaintLabel = QLabel('Жалобы пациента:')
        self.complaintTextBox = QLineEdit()
        self.complaintTextBox.setMinimumHeight(100)
        self.complaintBox.addWidget(self.complaintLabel)
        self.complaintBox.addWidget(self.complaintTextBox)
        self.complaintTextBox.setAlignment(Qt.AlignTop)

        # Diagnosis
        self.diagnosisBox = QHBoxLayout()
        self.diagnosisLabel = QLabel('Диагноз:')
        self.diagnosisSearch = QLineEdit()
        self.diagnosisSearch.setPlaceholderText('Начните ввод диагноза')
        self.diagnosisAddBtn = QPushButton()
        self.diagnosisAddBtn.setIcon(QIcon(str(proj_path / 'images/plus.png')))
        self.diagnosisBox.addWidget(self.diagnosisLabel)
        self.diagnosisBox.addWidget(self.diagnosisSearch)
        self.diagnosisBox.addWidget(self.diagnosisAddBtn)

        self.formBox.addRow(self.header)
        self.formBox.addRow(self.patientSelectBox)
        self.formBox.addRow(self.complaintBox)
        self.formBox.addRow(self.diagnosisBox)
        self.formBox.setAlignment(Qt.AlignLeft)
        self.formBox.setContentsMargins(20, 20, 20, 20)
        self.formBox.setVerticalSpacing(20)
        self.formBox.setHorizontalSpacing(20)
        self.formWidget.setLayout(self.formBox)
        self.formWidget.setMaximumWidth(500)
        self.setStyleSheet(get_stylesheet(self.style))
        self.setCentralWidget(self.formWidget)

        # signals


    def onload(self):
        pass
