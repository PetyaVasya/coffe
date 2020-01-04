import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.loadTable("coffee.db")
        # self.tableWidget.clicked.connect(self.run)

    # def run(self):
    #     self.label.setText("OK")

    def loadTable(self, db):
        self.db = sqlite3.connect(db)
        cur = self.db.cursor()
        rows = cur.execute("SELECT * FROM coffee ORDER BY id")
        top = list(map(lambda x: x[0], rows.description))
        rows = rows.fetchall()
        # print(rows)
        # self.attr.clear()
        # self.attr.addItems(top[1:])
        self.tableWidget.setColumnCount(len(top))
        self.tableWidget.setHorizontalHeaderLabels(top)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(rows):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
