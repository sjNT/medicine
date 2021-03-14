from PySide2.QtWidgets import QMainWindow, QFormLayout, QWidget, QLabel, QTableWidgetItem, QHeaderView, QHBoxLayout, \
    QPushButton, QDateEdit, QVBoxLayout
from PySide2.QtGui import QIcon
from custom import TableWidget, ErrorLabel
from utils import get_stylesheet
from PySide2.QtCore import Qt, QObject, Signal, SIGNAL
from database import DatabaseExecutor
from sql.query import GET_APPOINTMENTS, DEL_APPOINTMENTS, FILTER_APPOINTMENTS
from const import proj_path
import datetime
from docxtpl import Document
import time
import os


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
        self.report_btn = QPushButton('  Выгрузить отчёт')
        self.report_btn.setFixedSize(130, 30)
        self.report_icon = QIcon(str(proj_path / 'images/word.png'))
        self.report_btn.setIcon(self.report_icon)
        self.report_widget = ReportWindow()

        self.formBox = QFormLayout()
        self.formBox.addRow(self.header)
        self.formBox.addRow(self.report_btn)
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
        self.report_btn.clicked.connect(self.show_report_widget)

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

    def show_report_widget(self):
        self.report_widget.show()


class PrintTalon(QObject):
    talon_index = Signal(int)


class ReportWindow(QWidget):

    db = DatabaseExecutor

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setWindowTitle('Выгрузить отчет')
        self.setFixedSize(400, 200)
        self.record_date = QDateEdit()
        self.accept_btn = QPushButton('Получить')
        self.v_box = QVBoxLayout()
        self.date_h_box = QHBoxLayout()
        self.record_date_label = QLabel('Выберите дату:')
        self.date_h_box.addWidget(self.record_date_label)
        self.date_h_box.addWidget(self.record_date)
        self.v_box.addLayout(self.date_h_box)
        self.v_box.addWidget(self.accept_btn)
        self.record_date.setDate(datetime.datetime.now())
        self.setLayout(self.v_box)
        self.accept_btn.clicked.connect(self.get_records)

    def get_records(self):
        report = Document()

        date_row = self.record_date.date().toPython()
        dt = '%s-%s-%s' % (date_row.year, date_row.month, date_row.day)
        report.add_heading('Отчёт о записях %s' % dt, 0)
        data = self.db.exec_query(FILTER_APPOINTMENTS, param=(dt, ))
        table = report.add_table(rows=len(data), cols=5)
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Дата приема'
        hdr_cells[1].text = 'Пациент'
        hdr_cells[2].text = 'Специалист'
        filename = str(int(time.time()))
        for i in range(len(data)):
            row_cells = table.add_row().cells
            row_cells[0].text = '%s-%s-%s' % (data[i][0].year, data[i][0].month, data[i][0].day)
            row_cells[1].text = data[i][1]
            row_cells[2].text = data[i][2]
            report.save(str(proj_path / f'generate_docs/{filename}.docx'))
        os.startfile(str(proj_path / f'generate_docs/{filename}.docx'))
