from PySide2.QtWidgets import QMainWindow, QFormLayout, QWidget, QLabel, QTableWidgetItem, QHeaderView, QHBoxLayout, \
    QPushButton
from PySide2.QtGui import QIcon
from custom import TableWidget, ErrorLabel
from utils import get_stylesheet
from PySide2.QtCore import Qt, QObject, Signal, SIGNAL
from database import DatabaseExecutor
from sql.query import GET_APPOINTMENTS, DEL_APPOINTMENTS
from const import proj_path


class AppointmentRecords(QMainWindow):

    window_label = 'Записи'
    headers = ['#', 'Дата', 'Пациент', 'Специалист', '']
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
        self.print_talon = PrintTalon()
        self.setCentralWidget(self.formWidget)

    def onload(self):
        data = self.db.exec_query(GET_APPOINTMENTS)
        self.table.setRowCount(0)
        self.table.setRowCount(len(data))
        for row in range(len(data)):
            for column in range(len(data[row])):
                self.table.setItem(row, column, QTableWidgetItem(str(data[row][column])))
            self.action_widget = QWidget()
            self.action_box = QHBoxLayout()
            self.action_box.setSpacing(5)
            self.action_box.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            remove = QPushButton('Удалить')
            remove.setIcon(QIcon(str(proj_path / 'images/delete.png')))
            print = QPushButton('Печать')
            remove.setFixedHeight(20)
            print.setFixedHeight(20)
            print.setIcon(QIcon(str(proj_path / 'images/print.png')))
            self.action_box.addWidget(remove)
            self.action_box.addWidget(print)
            self.action_widget.setLayout(self.action_box)
            self.table.setCellWidget(row, 4, self.action_widget)
            remove.setProperty("delrow", data[row][0])
            remove.clicked.connect(self.delete_records)
            print.setProperty("printrow", data[row][0])
            print.clicked.connect(self.print_record)
        self.table.tabHeaders.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.tabHeaders.setSectionResizeMode(4, QHeaderView.ResizeToContents)

    def delete_records(self):
        sender = self.sender()
        removed_idx = sender.property("delrow")
        self.db.exec_query(DEL_APPOINTMENTS, param=(removed_idx, ))
        self.onload()

    def print_record(self):
        sender = self.sender()
        removed_idx = sender.property("printrow")
        self.print_talon.talon_index.emit(removed_idx)


class PrintTalon(QObject):
    talon_index = Signal(int)
