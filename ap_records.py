from PySide2.QtWidgets import QMainWindow, QFormLayout, QWidget, QLabel
from custom import TableWidget, ErrorLabel
from utils import get_stylesheet
from PySide2.QtCore import Qt


class AppointmentRecords(QMainWindow):

    window_label = 'Записи'
    headers = ['#', 'Дата', 'Пациент', 'Специалист']
    style = 'main.qss'

    def __init__(self):
        QMainWindow.__init__(self)
        self.formBox = QFormLayout()
        self.table = TableWidget()
        self.table.update_headers(self.headers)
        self.formWidget = QWidget()
        self.err_label = ErrorLabel()
        self.header = QLabel(self.window_label)
        self.header.setObjectName('AllAppointmentLabel')
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
        pass