from PySide2.QtWidgets import QMainWindow, QFormLayout, QWidget, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, \
    QComboBox, QDateEdit, QPushButton
from custom import ErrorLabel
from utils import get_stylesheet
from PySide2.QtCore import Qt


class AppointmentCreateRecord(QMainWindow):

    window_label = 'Запись пациента'
    style = 'main.qss'

    def __init__(self):
        QMainWindow.__init__(self)
        self.formBox = QFormLayout()
        self.formWidget = QWidget()
        self.err_label = ErrorLabel()
        self.header = QLabel(self.window_label)
        self.header.setObjectName('CrtAppointmentLabel')
        self.header.setMinimumWidth(200)
        self.header.setContentsMargins(0, 0, 0, 50)
        self.formBox = QFormLayout()

        # Patient search
        self.searchBox = QHBoxLayout()
        self.searchLabel = QLabel('Поиск пациента:')
        self.searchRow = QLineEdit()
        self.searchRow.setPlaceholderText('Введите фамилию')
        self.searchRow.setFixedWidth(180)
        self.searchLabelResult = QLabel('Найдено 1000 записей')
        self.searchLabelResult.setObjectName('SearchResultLabel')
        self.searchBox.addWidget(self.searchLabel)
        self.searchBox.addWidget(self.searchRow)
        self.searchBox.addWidget(self.searchLabelResult)
        self.searchBox.setSpacing(10)

        # Patient select
        self.patientBox = QHBoxLayout()
        self.patientLabel = QLabel('Выберите пациента:')
        self.patientLabel.setFixedWidth(120)
        self.patientSelect = QComboBox()
        self.patientSelect.setFixedWidth(260)
        self.patientBox.addWidget(self.patientLabel)
        self.patientBox.addWidget(self.patientSelect)
        self.patientBox.setSpacing(20)

        # Specialist select
        self.specialistBox = QHBoxLayout()
        self.specialistLabel = QLabel('Выберите специалиста:')
        self.specialistLabel.setFixedWidth(120)
        self.specialistSelect = QComboBox()
        self.specialistSelect.setFixedWidth(260)
        self.specialistBox.addWidget(self.specialistLabel)
        self.specialistBox.addWidget(self.specialistSelect)
        self.specialistBox.setSpacing(20)

        # Date select
        self.dateBox = QHBoxLayout()
        self.dateLabel = QLabel('Выберите дату приема:')
        self.dateLabel.setFixedWidth(120)
        self.dateSelect = QDateEdit()
        self.dateSelect.setFixedWidth(260)
        self.dateBox.addWidget(self.dateLabel)
        self.dateBox.addWidget(self.dateSelect)
        self.dateBox.setSpacing(20)

        self.formBtnBox = QHBoxLayout()

        # Submit and print
        self.submit = QPushButton('Сохранить и распечатать талон')
        self.submit.setObjectName('SubmitBtn')
        self.submit.setFixedSize(250, 30)
        self.submit.setCursor(Qt.PointingHandCursor)
        self.formBtnBox.addWidget(self.submit)

        self.formBox.addRow(self.header)
        self.formBox.addRow(self.searchBox)
        self.formBox.addRow(self.patientBox)
        self.formBox.addRow(self.specialistBox)
        self.formBox.addRow(self.dateBox)
        self.formBox.addRow(self.err_label)
        self.formBox.addRow(self.formBtnBox)

        # QFormLayout settings
        self.formBox.setContentsMargins(20, 20, 20, 20)
        self.formBox.setVerticalSpacing(20)
        self.formBox.setHorizontalSpacing(20)
        self.formBox.setAlignment(Qt.AlignLeft)
        self.formWidget.setLayout(self.formBox)
        self.formWidget.setMaximumWidth(500)
        self.setStyleSheet(get_stylesheet(self.style))
        self.setCentralWidget(self.formWidget)

        # Signals
        self.searchRow.textChanged.connect(self.on_search_event)

    def onload(self):
        pass

    def on_search_event(self, q):
        print('qqq', q)
        pass

    def update_search_result(self, data):
        self.patientSelect.addItems(['', 'М', 'Ж'])
        pass


