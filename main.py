import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTableWidgetItem, QComboBox, \
    QTextEdit, QPlainTextEdit


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.loadTable("coffee.db")
        self.pushButton.clicked.connect(self.edit)

    def edit(self):
        self.edit = EditWidget("coffee.db", self)
        self.edit.show()

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


class EditWidget(QWidget):

    def __init__(self, db, parent):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.db_name = db
        self.db = sqlite3.connect(db)
        cur = self.db.cursor()
        self.rows = cur.execute("SELECT * FROM coffee ORDER BY id").fetchall()
        self.comboBox.addItems(["Новый"] + list(map(lambda x: str(x[0]), self.rows)))
        self.comboBox_2.addItems(["Молотый", "Зерна"])
        self.comboBox.currentIndexChanged[int].connect(self.load_data)
        self.pushButton.clicked.connect(self.save)
        self.par = parent

    def clear_fields(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.comboBox_2.setCurrentIndex(0)
        self.textEdit.clear()
        QTest.qWait(200)
        self.update()

    def save(self):
        cur = self.db.cursor()
        if self.comboBox.currentIndex():
            cur.execute("""UPDATE coffee SET name=?, degree=?, type=?, description=?, price=?,
                         size=? WHERE id=?""", (self.lineEdit.text(),
                                                self.lineEdit_3.text(),
                                                self.comboBox_2.currentText(),
                                                self.textEdit.toPlainText(),
                                                self.lineEdit_2.text(),
                                                self.lineEdit_4.text(),
                                                self.comboBox.currentText(),))
        else:
            cur.execute("""INSERT INTO coffee(name, degree, type, description, price, size)
                         VALUES(?, ?, ?, ?, ?, ?)""", (self.lineEdit.text(),
                                                       self.lineEdit_3.text(),
                                                       self.comboBox_2.currentText(),
                                                       self.textEdit.toPlainText(),
                                                       self.lineEdit_2.text(),
                                                       self.lineEdit_4.text(),))
        self.db.commit()
        self.clear_fields()
        self.db.close()
        self.close()
        self.par.loadTable(self.db_name)

    def load_data(self, ind):
        if ind:
            data = self.rows[ind - 1]
            self.lineEdit.setText(data[1])
            self.lineEdit_2.setText(str(data[5]))
            self.lineEdit_3.setText(data[2])
            self.lineEdit_4.setText(str(data[6]))
            self.comboBox_2.setCurrentIndex(data[3] == "зерна")
            self.textEdit.setText(data[4])
            QTest.qWait(100)
            self.update()
        else:
            self.clear_fields()


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
