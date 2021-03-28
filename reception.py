from PySide2.QtCore import Qt
from utils import get_stylesheet
from database import DatabaseExecutor
from PySide2.QtWidgets import QMainWindow, QLabel, QHBoxLayout, QLineEdit, QFormLayout, QWidget, \
    QPushButton, QComboBox
from PySide2.QtGui import QIcon
from sql.query import GET_RECEPTION_PATIENT, START_APPOINTMENT, END_APPOINTMENT, RECEPTION_CONTEXT, DIAGNOSIS_CONTEXT
from const import proj_path, auth_user
from custom import DiagnoseCustom, AnalysisCustom
from docxtpl import DocxTemplate
import os


class ReceptionWidget(QMainWindow):

    style = 'main.qss'
    db = DatabaseExecutor
    window_label = 'Прием пациента'
    appointment_details = {}
    current_appointment_id = None
    patient_id = None
    patient_b_date = None
    patient_fullname = None

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
        self.diagnoseWidget = DiagnoseCustom()
        self.analysisWidget = AnalysisCustom()

        # Patient
        self.patientWidget = QWidget()
        self.patientSelectBox = QHBoxLayout()
        self.patientSelectLabel = QLabel('Выбор пациента:')
        self.patientSelect = QComboBox()
        self.patientSelectBox.addWidget(self.patientSelectLabel)
        self.patientSelectBox.addWidget(self.patientSelect)
        self.patientSelectBox.setAlignment(Qt.AlignLeft)
        self.patientWidget.setLayout(self.patientSelectBox)
        self.patientSelect.setFixedWidth(300)

        self.receptionWidget = QWidget()
        self.receptionWidgetBox = QFormLayout()

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
        self.diagnosisAddBtn = QPushButton('Внести диагноз')
        self.diagnosisAddBtn.setIcon(QIcon(str(proj_path / 'images/plus.png')))
        self.diagnosisBox.addWidget(self.diagnosisLabel)
        self.diagnosisBox.addWidget(self.diagnosisAddBtn)
        self.diagnosisBox.setAlignment(Qt.AlignLeft)

        # Analysis
        self.analysisBox = QHBoxLayout()
        self.analysisLabel = QLabel('Анализы:')
        self.analysisAddBtn = QPushButton('Назначить анализы')
        self.analysisAddBtn.setIcon(QIcon(str(proj_path / 'images/plus.png')))
        self.analysisBox.addWidget(self.analysisLabel)
        self.analysisBox.addWidget(self.analysisAddBtn)
        self.analysisBox.setAlignment(Qt.AlignLeft)

        # Reception accept
        self.accept_btn = QPushButton('Начать прием')
        self.accept_btn.setFixedWidth(100)

        # Reception end
        self.end_btn = QPushButton('Закончить прием')
        self.end_btn.setFixedWidth(150)

        # Print result
        self.print_result = QPushButton('Распечатать данные приема')
        self.print_result.setMinimumWidth(200)

        self.receptionWidgetBox.addRow(self.complaintBox)
        self.receptionWidgetBox.addRow(self.diagnosisBox)
        self.receptionWidgetBox.addRow(self.analysisBox)
        self.receptionWidgetBox.addRow(self.print_result)
        self.receptionWidgetBox.addRow(self.end_btn)
        self.receptionWidget.setLayout(self.receptionWidgetBox)

        self.formBox.addRow(self.header)
        self.formBox.addRow(self.patientWidget)
        self.formBox.addRow(self.accept_btn)
        self.formBox.addRow(self.receptionWidget)
        self.receptionWidget.setVisible(False)

        self.formBox.setAlignment(Qt.AlignLeft)
        self.formBox.setContentsMargins(20, 20, 20, 20)
        self.formBox.setVerticalSpacing(20)
        self.formBox.setHorizontalSpacing(20)
        self.receptionWidgetBox.setContentsMargins(20, 20, 20, 20)
        self.receptionWidgetBox.setVerticalSpacing(20)
        self.receptionWidgetBox.setHorizontalSpacing(20)
        self.receptionWidgetBox.setAlignment(Qt.AlignLeft)
        self.formWidget.setLayout(self.formBox)
        self.formWidget.setMaximumWidth(500)
        self.setStyleSheet(get_stylesheet(self.style))
        self.setCentralWidget(self.formWidget)

        # signals
        self.accept_btn.clicked.connect(self.reception_accept)
        self.end_btn.clicked.connect(self.reception_end)
        self.diagnosisAddBtn.clicked.connect(self.diagnosis_w)
        self.analysisAddBtn.clicked.connect(self.analysis_w)
        self.print_result.clicked.connect(self.print_reception)

    def onload(self):
        self.patientSelect.clear()
        self.appointment_details.clear()
        self.accept_btn.setVisible(True)
        self.patientWidget.setVisible(True)
        self.receptionWidget.setVisible(False)
        q = self.db.exec_query(GET_RECEPTION_PATIENT, param=(auth_user.specialist_id, ))
        if not q:
            return
        for r in range(len(q)):
            self.appointment_details[r] = {'id': q[r][3], 'patient_id': q[r][0], 'b_date': q[r][1], 'fullname': q[r][2]}
            self.patientSelect.addItem(f'{q[r][2]}, {q[r][1].year} г.р. ')

    def reception_accept(self):
        if self.patientSelect.currentText() == '':
            return None
        self.accept_btn.setVisible(False)
        self.receptionWidget.setVisible(True)
        self.current_appointment_id = self.appointment_details[self.patientSelect.currentIndex()]['id']
        self.patient_id = self.appointment_details[self.patientSelect.currentIndex()]['patient_id']
        self.patient_b_date = self.appointment_details[self.patientSelect.currentIndex()]['b_date']
        self.patient_fullname = self.appointment_details[self.patientSelect.currentIndex()]['fullname']
        self.db.exec_query(START_APPOINTMENT, param=(self.current_appointment_id, ))
        self.patientWidget.setVisible(False)

    def reception_end(self):
        self.db.exec_query(END_APPOINTMENT, param=(self.current_appointment_id, ))
        self.onload()

    def diagnosis_w(self):
        sender = self.sender()
        widget = self.diagnoseWidget
        widget.update_title(sender.text())
        widget.load(self.current_appointment_id)

    def analysis_w(self):
        sender = self.sender()
        widget = self.analysisWidget
        widget.update_title(sender.text())
        widget.load(self.current_appointment_id, auth_user.specialist_id)

    def print_reception(self):
        template = DocxTemplate(str(proj_path / 'templates/template_reception.docx'))
        context = self.db.exec_query(RECEPTION_CONTEXT, param=(self.current_appointment_id,), dictionary=True)[0]
        print(context)
        diag = self.db.exec_query(DIAGNOSIS_CONTEXT, param=(self.current_appointment_id, ))
        context['diag'] = []
        context['therapy'] = []
        for d in range(len(diag)):
            context['diag'].append(diag[d][0])
            context['therapy'].append(diag[d][1])
        template.render(context=context)
        filename = str(proj_path / 'reception/reception.docx')
        template.save(filename)
        os.startfile(filename, 'print')