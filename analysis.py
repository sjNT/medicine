from PySide2.QtWidgets import QMainWindow, QLabel, QHBoxLayout, QLineEdit, QFormLayout, QWidget, \
    QPushButton, QDateEdit, QTableWidget, QHeaderView, QVBoxLayout, QComboBox, QTextEdit, QTableWidgetItem
from PySide2.QtGui import QIcon
from utils import get_stylesheet
from database import DatabaseExecutor
from PySide2.QtCore import Qt
from custom import TableWidget
from sql.query import GET_ANALYSIS_LIST, UPDATE_ANALYSIS_RESULT, ANALYSIS_RESULT_CONTEXT
from const import proj_path
from docxtpl import DocxTemplate
import os


class AnalysisWidget(QMainWindow):

    style = 'main.qss'
    db = DatabaseExecutor
    window_label = 'Анализы пациентов'
    cur_idx = None

    def __init__(self):
        QMainWindow.__init__(self)
        self.formWidget = QWidget()
        self.header = QLabel(self.window_label)
        self.header.setObjectName('ReceptionLabel')
        self.header.setMinimumWidth(200)
        self.header.setContentsMargins(0, 0, 0, 50)
        self.formBox = QFormLayout()
        self.formWidget = QWidget()
        self.analysisTable = TableWidget()
        self.addResult = QWidget()
        self.resultValue = QTextEdit()
        self.submitResult = QPushButton('Сохранить')
        self.submitResult.setObjectName('SubmitBtn')
        self.submitResult.setFixedSize(100, 30)
        self.submitResult.setCursor(Qt.PointingHandCursor)
        self.resultVbox = QVBoxLayout()
        self.resultVbox.addWidget(self.resultValue)
        self.resultVbox.addWidget(self.submitResult)
        self.addResult.setWindowTitle('Внесение результатов анализа')
        self.addResult.setLayout(self.resultVbox)
        self.analysis_table_headers = ['Наименование', 'Пациент', 'Результат', '']

        self.formBox.addRow(self.header)
        self.formBox.addRow(self.analysisTable)

        self.formBox.setAlignment(Qt.AlignLeft)
        self.formBox.setContentsMargins(20, 20, 20, 20)
        self.formBox.setVerticalSpacing(20)
        self.formBox.setHorizontalSpacing(20)
        self.formWidget.setLayout(self.formBox)
        self.setStyleSheet(get_stylesheet(self.style))
        self.addResult.setStyleSheet(get_stylesheet(self.style))
        self.addResult.setFixedSize(400, 400)
        self.setCentralWidget(self.formWidget)
        self.submitResult.clicked.connect(self.submit_result)

    def onload(self):
        self.analysisTable.update_headers(self.analysis_table_headers)
        data = self.db.exec_query(GET_ANALYSIS_LIST)
        self.analysisTable.setRowCount(0)
        self.analysisTable.setRowCount(len(data))
        for row in range(len(data)):
            for column in range(len(data[row])-1):
                self.analysisTable.setItem(row, column, QTableWidgetItem(str(data[row][column])))
            self.action_widget = QWidget()
            self.action_box = QHBoxLayout()
            self.action_box.setSpacing(5)
            self.action_box.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            print = QPushButton('Печать')
            print.setFixedHeight(20)
            print.setIcon(QIcon(str(proj_path / 'images/print.png')))
            result = QPushButton('Внести результаты')
            result.setFixedHeight(20)
            result.setIcon(QIcon(str(proj_path / 'images/plus.png')))
            self.action_box.addWidget(print)
            self.action_box.addWidget(result)
            self.action_widget.setLayout(self.action_box)
            self.analysisTable.setCellWidget(row, 3, self.action_widget)
            print.setProperty("printrow", data[row][3])
            print.clicked.connect(self.print_record)
            result.setProperty("resultrow", data[row][3])
            result.clicked.connect(self.load_result_widget)
        # self.analysisTable.tabHeaders.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.analysisTable.tabHeaders.setSectionResizeMode(2, QHeaderView.ResizeToContents)

    def print_record(self):
        sender = self.sender()
        print_idx = sender.property("printrow")
        template = DocxTemplate(str(proj_path / 'templates/template_analysis_result.docx'))
        context = self.db.exec_query(ANALYSIS_RESULT_CONTEXT, param=(print_idx,), dictionary=True)[0]
        template.render(context=context)
        filename = str(proj_path / 'analisys result/analysis_result.docx')
        template.save(filename)
        os.startfile(filename, 'print')

    def load_result_widget(self):
        self.resultValue.clear()
        self.addResult.show()
        sender = self.sender()
        self.cur_idx = sender.property("resultrow")

    def submit_result(self):
        if self.resultValue.toPlainText() != '':
            self.db.exec_query(UPDATE_ANALYSIS_RESULT, param=(self.resultValue.toPlainText(), self.cur_idx), )
            self.addResult.close()
            self.onload()
