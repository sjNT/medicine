from menu import Menu
from const import proj_path
from PySide2.QtCore import Qt, SIGNAL
from login import LoginWindow
from utils import get_stylesheet
from database import DatabaseExecutor
from PySide2.QtWidgets import QMainWindow, QApplication, QStackedWidget, QDialog, QWidget
from doctor import Doctor
from patient import Patient
from ap_new import AppointmentCreateRecord
from ap_records import AppointmentRecords
from patient_table import PatientRecords, LoadPatient
from reception import ReceptionWidget

# https://www.flaticon.com/ru/packs/pharmaceutical-3/2?k=1614430300833

stack_indexes = {'DoctorWidget': 1, 'PatientWidget': 2, 'CreateAppointmentWidget': 3, 'AllAppointmentWidget': 4,
                 'ViewPatientWidget': 5, 'ReceptionWidget': 6}


class MainWindow(QMainWindow):

    style = 'main.qss'
    db = DatabaseExecutor

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setMinimumSize(1000, 700)
        self.setWindowTitle('Поликлиника №123')
        self.stack = QStackedWidget()
        self._menu = Menu()
        self.addToolBar(Qt.LeftToolBarArea, self._menu)
        self.setStyleSheet(get_stylesheet(self.style))
        self.mainWidget = QWidget()
        self.doctorWidget = Doctor()
        self.patientWidget = Patient()
        self.newAppointment = AppointmentCreateRecord()
        self.allAppointment = AppointmentRecords()
        self.allPatient = PatientRecords()
        self.reception = ReceptionWidget()
        self.stack.addWidget(self.mainWidget)
        self.stack.addWidget(self.doctorWidget)
        self.stack.addWidget(self.patientWidget)
        self.stack.addWidget(self.newAppointment)
        self.stack.addWidget(self.allAppointment)
        self.stack.addWidget(self.allPatient)
        self.stack.addWidget(self.reception)
        self.setCentralWidget(self.stack)

        self.connect(self.allPatient.patientLoad, SIGNAL('patient_index(int)'), self.load_patient)
        self.connect(self.allAppointment.print_talon, SIGNAL('talon_index(int)'), self.print_talon)
        # signals
        self._menu.addDoctorBtn.triggered.connect(self.switch_widget)
        self._menu.addPatientBtn.triggered.connect(self.switch_widget)
        self._menu.addRecordBtn.triggered.connect(self.switch_widget)
        self._menu.viewRecordsBtn.triggered.connect(self.switch_widget)
        self._menu.patientViewBtn.triggered.connect(self.switch_widget)
        self._menu.receptionBtn.triggered.connect(self.switch_widget)
        self._menu.viewRecordsBtn.click()

    def switch_widget(self):
        sender = self.sender()
        senderStackIndex = stack_indexes.get(sender.objectName())
        self.stack.setCurrentIndex(senderStackIndex)
        self.stack.widget(senderStackIndex).onload()

    def load_patient(self, idx):
        self.patientWidget.load_patient(idx)
        self.stack.setCurrentIndex(self.stack.indexOf(self.patientWidget))

    def print_talon(self, idx):
        self.newAppointment.render_template(idx)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    login = LoginWindow()
    """
    if login.exec_() == QDialog.Accepted:
        main = MainWindow()
        main.show()
    """
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
