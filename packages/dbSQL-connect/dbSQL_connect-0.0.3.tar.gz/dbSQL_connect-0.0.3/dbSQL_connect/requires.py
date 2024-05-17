# from PyQt5 import QtCore, QtGui, QtWidgets
# import pymysql.cursors
# from PyQt5.QtWidgets import QTableWidgetItem
#
# def update(self):
#     try:
#         bd = pymysql.connect(host='localhost', user='root', password='', db='sklad', cursorclass=pymysql.cursors.DictCursor)
#         cursor = bd.cursor()
#         sql = 'SELECT * FROM sklad'
#         cursor.execute(sql)
#         result = cursor.fetchall()
#
#         self.QtablrWidget.setRowCount(len(result))
#         self.QtablrWidget.setColumnCount(4)
#
#         for row_index, row_data in enumerate(result):
#             col_index = 0
#             for key, col_data in row_data.items():
#                 if key != 'id':
#                     item = QTableWidgetItem(str(col_data))
#                     self.QtablrWidget.setItem(row_index, col_index, item)
#                     col_index += 1
#
#     except pymysql.Error as e:
#         print("Error while connecting to MySQL", e)
#     finally:
#         cursor.close()
#         bd.close()
#
#
# from PyQt5 import QtCore, QtGui, QtWidgets
# from win2 import Ui_kadov
# from win3 import Ui_meneger
#
# class Ui_MainWindow(object):
#
#
#     def openWindow1(self):
#         self.window = QtWidgets.QMainWindow()
#         self.ui = Ui_meneger()
#         self.ui.setupUi(self.window)
#         self.window.show()
#
#     def openWindow(self):
#         self.window = QtWidgets.QMainWindow()
#         self.ui = Ui_kadov()
#         self.ui.setupUi(self.window)
#         self.window.show()
#
#     def setupUi(self, MainWindow):
#         MainWindow.setObjectName("MainWindow")
#         MainWindow.resize(435, 191)
#         self.centralwidget = QtWidgets.QWidget(MainWindow)
#         self.centralwidget.setObjectName("centralwidget")
#         self.pushButton = QtWidgets.QPushButton(self.centralwidget)
#         self.pushButton.setGeometry(QtCore.QRect(50, 50, 121, 51))
#         self.pushButton.setObjectName("pushButton")
#         self.pushButton.clicked.connect(self.openWindow)
#         self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
#         self.pushButton_2.setGeometry(QtCore.QRect(270, 50, 131, 51))
#         self.pushButton_2.setObjectName("pushButton_2")
#         self.pushButton_2.clicked.connect(self.openWindow1)
#         MainWindow.setCentralWidget(self.centralwidget)
#         self.menubar = QtWidgets.QMenuBar(MainWindow)
#         self.menubar.setGeometry(QtCore.QRect(0, 0, 435, 26))
#         self.menubar.setObjectName("menubar")
#         MainWindow.setMenuBar(self.menubar)
#         self.statusbar = QtWidgets.QStatusBar(MainWindow)
#         self.statusbar.setObjectName("statusbar")
#         MainWindow.setStatusBar(self.statusbar)
#
#         self.retranslateUi(MainWindow)
#         QtCore.QMetaObject.connectSlotsByName(MainWindow)
#
#     def retranslateUi(self, MainWindow):
#         _translate = QtCore.QCoreApplication.translate
#         MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
#         self.pushButton.setText(_translate("MainWindow", "страница 1"))
#         self.pushButton_2.setText(_translate("MainWindow", "Страница 2"))
#
#
# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())
#
#
# from PyQt5 import QtCore, QtGui, QtWidgets
#
# import pymysql.cursors
# class Ui_kadov(object):
#     def setupUi(self, kadov):
#         kadov.setObjectName("kadov")
#         kadov.resize(567, 454)
#         self.centralwidget = QtWidgets.QWidget(kadov)
#         self.centralwidget.setObjectName("centralwidget")
#         self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
#         self.tableWidget.setGeometry(QtCore.QRect(0, 0, 511, 192))
#         self.tableWidget.setObjectName("tableWidget")
#         self.tableWidget.setColumnCount(4)
#         self.tableWidget.setRowCount(0)
#         item = QtWidgets.QTableWidgetItem()
#         self.tableWidget.setHorizontalHeaderItem(0, item)
#         item = QtWidgets.QTableWidgetItem()
#         self.tableWidget.setHorizontalHeaderItem(1, item)
#         item = QtWidgets.QTableWidgetItem()
#         self.tableWidget.setHorizontalHeaderItem(2, item)
#         item = QtWidgets.QTableWidgetItem()
#         self.tableWidget.setHorizontalHeaderItem(3, item)
#         self.pushButton = QtWidgets.QPushButton(self.centralwidget)
#         self.pushButton.setGeometry(QtCore.QRect(120, 350, 111, 31))
#         self.pushButton.setObjectName("pushButton")
#         self.pushButton.clicked.connect(self.tranz)
#         self.label = QtWidgets.QLabel(self.centralwidget)
#         self.label.setGeometry(QtCore.QRect(20, 230, 81, 20))
#         self.label.setObjectName("label")
#         self.label_2 = QtWidgets.QLabel(self.centralwidget)
#         self.label_2.setGeometry(QtCore.QRect(30, 270, 81, 20))
#         self.label_2.setObjectName("label_2")
#         self.label_3 = QtWidgets.QLabel(self.centralwidget)
#         self.label_3.setGeometry(QtCore.QRect(40, 310, 61, 20))
#         self.label_3.setObjectName("label_3")
#         self.comboBox = QtWidgets.QComboBox(self.centralwidget)
#         self.comboBox.setGeometry(QtCore.QRect(120, 230, 131, 22))
#         self.comboBox.setObjectName("comboBox")
#         self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
#         self.comboBox_2.setGeometry(QtCore.QRect(120, 270, 131, 22))
#         self.comboBox_2.setObjectName("comboBox_2")
#         self.comboBox_3 = QtWidgets.QComboBox(self.centralwidget)
#         self.comboBox_3.setGeometry(QtCore.QRect(120, 310, 131, 22))
#         self.comboBox_3.setObjectName("comboBox_3")
#         kadov.setCentralWidget(self.centralwidget)
#         self.menubar = QtWidgets.QMenuBar(kadov)
#         self.menubar.setGeometry(QtCore.QRect(0, 0, 567, 26))
#         self.menubar.setObjectName("menubar")
#         kadov.setMenuBar(self.menubar)
#         self.statusbar = QtWidgets.QStatusBar(kadov)
#         self.statusbar.setObjectName("statusbar")
#         kadov.setStatusBar(self.statusbar)
#
#         self.retranslateUi(kadov)
#         QtCore.QMetaObject.connectSlotsByName(kadov)
#
#
#         self.uptable()
#         self.combobox()
#     def retranslateUi(self, kadov):
#         _translate = QtCore.QCoreApplication.translate
#         kadov.setWindowTitle(_translate("kadov", "MainWindow"))
#         item = self.tableWidget.horizontalHeaderItem(0)
#         item.setText(_translate("kadov", "Номер груза"))
#         item = self.tableWidget.horizontalHeaderItem(1)
#         item.setText(_translate("kadov", "Дата поступления "))
#         item = self.tableWidget.horizontalHeaderItem(2)
#         item.setText(_translate("kadov", "New Column"))
#         item = self.tableWidget.horizontalHeaderItem(3)
#         item.setText(_translate("kadov", "Место на складе "))
#         self.pushButton.setText(_translate("kadov", "Отправить груз "))
#         self.label.setText(_translate("kadov", "Номер груза: "))
#         self.label_2.setText(_translate("kadov", "Покупатель:"))
#         self.label_3.setText(_translate("kadov", "Машина: "))
#
#
#
#     def tranz(self):
#
#         id_gruz = self.comboBox.currentText()
#         id_pok = self.comboBox_3.currentText()
#         id_auto = self.comboBox_2.currentText()
#
#         try:
#             bd = pymysql.connect(host='localhost', user='root', passwd='',
#                              db='sklad', cursorclass=pymysql.cursors.DictCursor)
#             cursor = bd.cursor()
#             sql = "INSERT INTO tranzakt VALUES (NULL,%s,%s,%s)"
#             val =(id_gruz,id_pok,id_auto)
#             cursor.execute(sql,val)
#
#             bd.commit()
#
#             print("Усспешно")
#
#         except Exception as e:
#             print(e)
#
#         finally:
#             cursor.close()
#             bd.close()
#
#     def combobox(self):
#         try:
#             bd = pymysql.connect(host='localhost', user='root', passwd='',
#                                  db='sklad', cursorclass=pymysql.cursors.DictCursor)
#             cursor = bd.cursor()
#
#             sql = "SELECT id FROM gruz"
#             cursor.execute(sql)
#             result = cursor.fetchall()
#             for item in result:
#                 self.comboBox.addItem(str(item['id']))
#
#             sql2 = "SELECT id, name FROM pokup"
#             cursor.execute(sql2)
#             result2 = cursor.fetchall()
#             for item in result2:
#                 self.comboBox_2.addItem(str(item['id']) + item['name'])
#
#             sql4 = "SELECT id, num_auto FROM auto"
#             cursor.execute(sql4)
#             result3 = cursor.fetchall()
#             for item in result3:
#                 self.comboBox_3.addItem(str(item['id']) + item['num_auto'])
#
#         except Exception as e:
#             print("Error:", e)
#
#         finally:
#             cursor.close()
#             bd.close()
#
#     def uptable(self):
#         bd = pymysql.connect(host='localhost', user='root', passwd='', db='sklad',
#                              cursorclass=pymysql.cursors.DictCursor)
#         cursor = bd.cursor()
#         sql = "select * from gruz"
#         cursor.execute(sql)
#         result = cursor.fetchall()
#
#         self.tableWidget.setRowCount(len(result))
#         self.tableWidget.setColumnCount(4)
#
#         for row_index, row_data in enumerate(result):
#             for col_index, col_data in enumerate(row_data.values()):
#                 item = QtWidgets.QTableWidgetItem(str(col_data))
#                 self.tableWidget.setItem(row_index, col_index, item)
#
#         cursor.close()
#         bd.close()
#
#
#
#
# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     kadov = QtWidgets.QMainWindow()
#     ui = Ui_kadov()
#     ui.setupUi(kadov)
#     kadov.show()
#     ui.combobox()
#     sys.exit(app.exec_())
#
#
# from PyQt5 import QtCore, QtGui, QtWidgets
# import pymysql.cursors
# from win4 import Ui_pok
# class Ui_meneger(object):
#     def openWindow(self):
#         self.window = QtWidgets.QMainWindow()
#         self.ui = Ui_pok()
#         self.ui.setupUi(self.window)
#         self.window.show()
#     def setupUi(self, meneger):
#         meneger.setObjectName("meneger")
#         meneger.resize(567, 454)
#         self.centralwidget = QtWidgets.QWidget(meneger)
#         self.centralwidget.setObjectName("centralwidget")
#         self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
#         self.tableWidget.setGeometry(QtCore.QRect(0, 0, 511, 192))
#         self.tableWidget.setObjectName("tableWidget")
#         self.tableWidget.setColumnCount(4)
#         self.tableWidget.setRowCount(0)
#         item = QtWidgets.QTableWidgetItem()
#         self.tableWidget.setHorizontalHeaderItem(0, item)
#         item = QtWidgets.QTableWidgetItem()
#         self.tableWidget.setHorizontalHeaderItem(1, item)
#         item = QtWidgets.QTableWidgetItem()
#         self.tableWidget.setHorizontalHeaderItem(2, item)
#         item = QtWidgets.QTableWidgetItem()
#         self.tableWidget.setHorizontalHeaderItem(3, item)
#         self.pushButton = QtWidgets.QPushButton(self.centralwidget)
#         self.pushButton.setGeometry(QtCore.QRect(380, 350, 151, 31))
#         self.pushButton.setObjectName("pushButton")
#         self.pushButton.clicked.connect(self.openWindow)
#         self.label = QtWidgets.QLabel(self.centralwidget)
#         self.label.setGeometry(QtCore.QRect(20, 240, 91, 16))
#         self.label.setObjectName("label")
#         self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
#         self.textEdit.setGeometry(QtCore.QRect(120, 230, 131, 31))
#         self.textEdit.setObjectName("textEdit")
#         self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
#         self.pushButton_2.clicked.connect(self.serch)
#         self.pushButton_2.setGeometry(QtCore.QRect(140, 280, 93, 28))
#         self.pushButton_2.setObjectName("pushButton_2")
#         meneger.setCentralWidget(self.centralwidget)
#         self.menubar = QtWidgets.QMenuBar(meneger)
#         self.menubar.setGeometry(QtCore.QRect(0, 0, 567, 26))
#         self.menubar.setObjectName("menubar")
#         meneger.setMenuBar(self.menubar)
#         self.statusbar = QtWidgets.QStatusBar(meneger)
#         self.statusbar.setObjectName("statusbar")
#         meneger.setStatusBar(self.statusbar)
#
#         self.retranslateUi(meneger)
#         QtCore.QMetaObject.connectSlotsByName(meneger)
#
#         self.uptable()
#
#     def retranslateUi(self, meneger):
#         _translate = QtCore.QCoreApplication.translate
#         meneger.setWindowTitle(_translate("meneger", "MainWindow"))
#         item = self.tableWidget.horizontalHeaderItem(0)
#         item.setText(_translate("meneger", "Номер груза"))
#         item = self.tableWidget.horizontalHeaderItem(1)
#         item.setText(_translate("meneger", "Дата поступления "))
#         item = self.tableWidget.horizontalHeaderItem(2)
#         item.setText(_translate("meneger", "Вес"))
#         item = self.tableWidget.horizontalHeaderItem(3)
#         item.setText(_translate("meneger", "Место на складе "))
#         self.pushButton.setText(_translate("meneger", "Добавить покупателя "))
#         self.label.setText(_translate("meneger", "Номер груза "))
#         self.pushButton_2.setText(_translate("meneger", "Поиск"))
#
#     def uptable(self):
#         bd = pymysql.connect(host='localhost', user='root', passwd='',
#                              db='sklad', cursorclass=pymysql.cursors.DictCursor)
#         cursor = bd.cursor()
#         sql = "select * from gruz"
#         cursor.execute(sql)
#         result = cursor.fetchall()
#
#         self.tableWidget.setRowCount(len(result))
#         self.tableWidget.setColumnCount(4)
#
#         for row_index, row_data in enumerate(result):
#             col_index = 0
#
#             for key, col_data in row_data.items():
#
#                 if key != 'id':
#                     item = QtWidgets.QTableWidgetItem(str(col_data))
#                     self.tableWidget.setItem(row_index, col_index, item)
#                     col_index += 1
#
#         cursor.close()
#         bd.close()
#
#     def serch(self):
#         num = self.textEdit.toPlainText()
#         try:
#             bd = pymysql.connect(host='localhost', user='root', passwd='',
#                                  database='sklad', cursorclass=pymysql.cursors.DictCursor)
#             cursor = bd.cursor()
#             sql = "select * from gruz where num = %s"
#             cursor.execute(sql, (num,))
#             result = cursor.fetchall()
#             self.tableWidget.setRowCount(len(result))
#             self.tableWidget.setColumnCount(4)
#             for row_index, row_data in enumerate(result):
#                 col_index = 0
#                 for key, col_data in row_data.items():
#                     if key != 'id':
#                         item = QtWidgets.QTableWidgetItem(str(col_data))
#                         self.tableWidget.setItem(row_index, col_index, item)
#                         col_index += 1
#             if not result:
#                 self.textEdit.setText("Такого номера нет")
#             else:
#                 self.textEdit.setText(str(num))
#         except Exception as e:
#             print("Error:", e)
#         finally:
#             cursor.close()
#             bd.close()
#
#
#
# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     meneger = QtWidgets.QMainWindow()
#     ui = Ui_meneger()
#     ui.setupUi(meneger)
#     meneger.show()
#     sys.exit(app.exec_())
#
#
# import pymysql
# from PyQt5 import QtCore, QtGui, QtWidgets
# import pymysql.cursors
#
# class Ui_pok(object):
#     def setupUi(self, pok):
#         pok.setObjectName("pok")
#         pok.resize(403, 332)
#         self.centralwidget = QtWidgets.QWidget(pok)
#         self.centralwidget.setObjectName("centralwidget")
#         self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
#         self.textEdit.setGeometry(QtCore.QRect(170, 50, 131, 31))
#         self.textEdit.setObjectName("textEdit")
#         self.label = QtWidgets.QLabel(self.centralwidget)
#         self.label.setGeometry(QtCore.QRect(100, 60, 61, 20))
#         self.label.setObjectName("label")
#         self.label_2 = QtWidgets.QLabel(self.centralwidget)
#         self.label_2.setGeometry(QtCore.QRect(100, 110, 61, 20))
#         self.label_2.setObjectName("label_2")
#         self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
#         self.textEdit_2.setGeometry(QtCore.QRect(170, 100, 131, 31))
#         self.textEdit_2.setObjectName("textEdit_2")
#         self.label_3 = QtWidgets.QLabel(self.centralwidget)
#         self.label_3.setGeometry(QtCore.QRect(110, 160, 41, 20))
#         self.label_3.setObjectName("label_3")
#         self.textEdit_3 = QtWidgets.QTextEdit(self.centralwidget)
#         self.textEdit_3.setGeometry(QtCore.QRect(170, 150, 131, 31))
#         self.textEdit_3.setObjectName("textEdit_3")
#         self.label_4 = QtWidgets.QLabel(self.centralwidget)
#         self.label_4.setGeometry(QtCore.QRect(90, 200, 71, 20))
#         self.label_4.setObjectName("label_4")
#         self.textEdit_4 = QtWidgets.QTextEdit(self.centralwidget)
#         self.textEdit_4.setGeometry(QtCore.QRect(170, 190, 131, 31))
#         self.textEdit_4.setObjectName("textEdit_4")
#         self.pushButton = QtWidgets.QPushButton(self.centralwidget)
#         self.pushButton.setGeometry(QtCore.QRect(190, 240, 93, 28))
#         self.pushButton.setObjectName("pushButton")
#         self.pushButton.clicked.connect(self.update)
#         pok.setCentralWidget(self.centralwidget)
#         self.menubar = QtWidgets.QMenuBar(pok)
#         self.menubar.setGeometry(QtCore.QRect(0, 0, 403, 26))
#         self.menubar.setObjectName("menubar")
#         pok.setMenuBar(self.menubar)
#         self.statusbar = QtWidgets.QStatusBar(pok)
#         self.statusbar.setObjectName("statusbar")
#         pok.setStatusBar(self.statusbar)
#
#         self.retranslateUi(pok)
#         QtCore.QMetaObject.connectSlotsByName(pok)
#
#     def retranslateUi(self, pok):
#         _translate = QtCore.QCoreApplication.translate
#         pok.setWindowTitle(_translate("pok", "MainWindow"))
#         self.label.setText(_translate("pok", "Название"))
#         self.label_2.setText(_translate("pok", "Телефон"))
#         self.label_3.setText(_translate("pok", "БИК"))
#         self.label_4.setText(_translate("pok", "Лиц.Счет"))
#         self.pushButton.setText(_translate("pok", "Добавить"))
#
#
#
#     def update(self):
#         name = self.textEdit.toPlainText()
#         phone = self.textEdit_2.toPlainText()
#         bik = self.textEdit_3.toPlainText()
#         lic = self.textEdit_4.toPlainText()
#
#         try:
#
#
#
#             bd = pymysql.connect(host='localhost', user='root', passwd='',
#                              db='sklad',cursorclass=pymysql.cursors.DictCursor)
#             cursor = bd.cursor()
#             sql = "Insert into pokup values(NULL,%s,%s,%s,%s)"
#             val = (name, phone, bik, lic)
#             cursor.execute(sql, val)
#             bd.commit()
#
#             print("Успешно")
#
#         except Exception as e:
#             print(e)
#
#         finally:
#             cursor.close()
#             bd.close()
#
#
# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     pok = QtWidgets.QMainWindow()
#     ui = Ui_pok()
#     ui.setupUi(pok)
#     pok.show()
#     sys.exit(app.exec_())
#
#
# from PyQt5 import QtCore, QtGui, QtWidgets
# import pymysql.cursors
#
#
# class Ui_MainWindow(object):
#     def setupUi(self, MainWindow):
#         MainWindow.setObjectName("MainWindow")
#         MainWindow.resize(649, 407)
#         self.centralwidget = QtWidgets.QWidget(MainWindow)
#         self.centralwidget.setObjectName("centralwidget")
#         self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
#         self.tableWidget.setGeometry(QtCore.QRect(30, 0, 561, 231))
#         self.tableWidget.setObjectName("tableWidget")
#         self.tableWidget.setColumnCount(0)
#         self.tableWidget.setRowCount(0)
#         self.pushButton = QtWidgets.QPushButton(self.centralwidget)
#         self.pushButton.setGeometry(QtCore.QRect(370, 270, 93, 28))
#         self.pushButton.setObjectName("pushButton")
#         self.pushButton.clicked.connect(self.deleteData)  # Connect button click to deleteData method
#         MainWindow.setCentralWidget(self.centralwidget)
#         self.menubar = QtWidgets.QMenuBar(MainWindow)
#         self.menubar.setGeometry(QtCore.QRect(0, 0, 649, 26))
#         self.menubar.setObjectName("menubar")
#         MainWindow.setMenuBar(self.menubar)
#         self.statusbar = QtWidgets.QStatusBar(MainWindow)
#         self.statusbar.setObjectName("statusbar")
#         MainWindow.setStatusBar(self.statusbar)
#
#         self.retranslateUi(MainWindow)
#         QtCore.QMetaObject.connectSlotsByName(MainWindow)
#
#         self.uptable()
#
#     def retranslateUi(self, MainWindow):
#         _translate = QtCore.QCoreApplication.translate
#         MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
#         self.pushButton.setText(_translate("MainWindow", "Удалить"))
#
#     def uptable(self):
#         bd = pymysql.connect(host='localhost', user='root', passwd='', db='sklad',
#                              cursorclass=pymysql.cursors.DictCursor)
#         cursor = bd.cursor()
#         sql = "select * from pokup"
#         cursor.execute(sql)
#         result = cursor.fetchall()
#
#         self.tableWidget.setRowCount(len(result))
#         self.tableWidget.setColumnCount(4)
#
#         for row_index, row_data in enumerate(result):
#             for col_index, col_data in enumerate(row_data.values()):
#                 item = QtWidgets.QTableWidgetItem(str(col_data))
#                 self.tableWidget.setItem(row_index, col_index, item)
#
#         cursor.close()
#         bd.close()
#
#     def deleteData(self):
#         # Get selected rows
#         selected_rows = self.tableWidget.selectionModel().selectedRows()
#
#         if not selected_rows:
#             QtWidgets.QMessageBox.warning(None, "Warning", "Выберите строки для удаления")
#             return
#
#         rows_to_delete = []
#         for row in selected_rows:
#             rows_to_delete.append(row.row())
#
#
#         bd = pymysql.connect(host='localhost', user='root', passwd='', db='sklad',
#                              cursorclass=pymysql.cursors.DictCursor)
#         cursor = bd.cursor()
#
#         try:
#             # Delete rows from the database
#             for row in rows_to_delete:
#                 item_id = self.tableWidget.item(row, 0).text()
#                 sql = "DELETE FROM pokup WHERE id=%s"
#                 cursor.execute(sql, (item_id,))
#                 bd.commit()
#
#             # Update the table after deletion
#             self.uptable()
#             QtWidgets.QMessageBox.information(None, "Success", "Данные успешно удалены")
#         except Exception as e:
#             bd.rollback()
#             QtWidgets.QMessageBox.critical(None, "Error", f"Ошибка удаления данных: {str(e)}")
#
#         cursor.close()
#         bd.close()
#
#
# if __name__ == "__main__":
#     import sys
#
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())
#
#
#
# from PyQt5 import QtCore, QtGui, QtWidgets
# import pymysql.cursors
#
# class Ui_MainWindow(object):
#     def setupUi(self, MainWindow):
#         MainWindow.setObjectName("MainWindow")
#         MainWindow.resize(649, 407)
#         self.centralwidget = QtWidgets.QWidget(MainWindow)
#         self.centralwidget.setObjectName("centralwidget")
#         self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
#         self.textEdit.setGeometry(QtCore.QRect(190, 40, 131, 41))
#         self.textEdit.setObjectName("textEdit")
#         self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
#         self.textEdit_2.setGeometry(QtCore.QRect(190, 100, 131, 41))
#         self.textEdit_2.setObjectName("textEdit_2")
#         self.textEdit_3 = QtWidgets.QTextEdit(self.centralwidget)
#         self.textEdit_3.setGeometry(QtCore.QRect(190, 160, 131, 41))
#         self.textEdit_3.setObjectName("textEdit_3")
#         self.textEdit_4 = QtWidgets.QTextEdit(self.centralwidget)
#         self.textEdit_4.setGeometry(QtCore.QRect(190, 210, 131, 41))
#         self.textEdit_4.setObjectName("textEdit_4")
#         self.pushButton = QtWidgets.QPushButton(self.centralwidget)
#         self.pushButton.setGeometry(QtCore.QRect(212, 300, 111, 28))
#         self.pushButton.setObjectName("pushButton")
#         self.pushButton.clicked.connect(self.update)
#         MainWindow.setCentralWidget(self.centralwidget)
#         self.menubar = QtWidgets.QMenuBar(MainWindow)
#         self.menubar.setGeometry(QtCore.QRect(0, 0, 649, 26))
#         self.menubar.setObjectName("menubar")
#         MainWindow.setMenuBar(self.menubar)
#         self.statusbar = QtWidgets.QStatusBar(MainWindow)
#         self.statusbar.setObjectName("statusbar")
#         MainWindow.setStatusBar(self.statusbar)
#
#         self.retranslateUi(MainWindow)
#         QtCore.QMetaObject.connectSlotsByName(MainWindow)
#
#     def retranslateUi(self, MainWindow):
#         _translate = QtCore.QCoreApplication.translate
#         MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
#         self.pushButton.setText(_translate("MainWindow", "PushButton"))
#
#
#
#     def update(self):
#         name = self.textEdit.toPlainText()
#         phone = self.textEdit_2.toPlainText()
#         bik = self.textEdit_3.toPlainText()
#         lic = self.textEdit_4.toPlainText()
#
#         try:
#
#
#
#             bd = pymysql.connect(host='localhost', user='root', passwd='',
#                              db='sklad',cursorclass=pymysql.cursors.DictCursor)
#             cursor = bd.cursor()
#             sql = "Insert into pokup values(NULL,%s,%s,%s,%s)"
#             val = (name, phone, bik, lic)
#             cursor.execute(sql, val)
#             bd.commit()
#
#             print("Успешно")
#
#         except Exception as e:
#             print(e)
#
#         finally:
#             cursor.close()
#             bd.close()
#
#
#
#
# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())
#
#
#
# from PyQt5 import QtCore, QtGui, QtWidgets
# import pymysql.cursors
#
# class Ui_MainWindow(object):
#     def setupUi(self, MainWindow):
#         MainWindow.setObjectName("MainWindow")
#         MainWindow.resize(649, 407)
#         self.centralwidget = QtWidgets.QWidget(MainWindow)
#         self.centralwidget.setObjectName("centralwidget")
#         self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
#         self.tableWidget.setGeometry(QtCore.QRect(10, 0, 501, 211))
#         self.tableWidget.setObjectName("tableWidget")
#         self.tableWidget.setColumnCount(0)
#         self.tableWidget.setRowCount(0)
#         MainWindow.setCentralWidget(self.centralwidget)
#         self.menubar = QtWidgets.QMenuBar(MainWindow)
#         self.menubar.setGeometry(QtCore.QRect(0, 0, 649, 26))
#         self.menubar.setObjectName("menubar")
#         MainWindow.setMenuBar(self.menubar)
#         self.statusbar = QtWidgets.QStatusBar(MainWindow)
#         self.statusbar.setObjectName("statusbar")
#         MainWindow.setStatusBar(self.statusbar)
#
#         self.retranslateUi(MainWindow)
#         QtCore.QMetaObject.connectSlotsByName(MainWindow)
#
#         self.uptable()
#
#
#     def retranslateUi(self, MainWindow):
#         _translate = QtCore.QCoreApplication.translate
#         MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
#
#
#     def uptable(self):
#         bd = pymysql.connect(host='localhost', user='root', passwd='', db='sklad',
#                              cursorclass=pymysql.cursors.DictCursor)
#         cursor = bd.cursor()
#         sql = "select * from gruz"
#         cursor.execute(sql)
#         result = cursor.fetchall()
#
#         self.tableWidget.setRowCount(len(result))
#         self.tableWidget.setColumnCount(4)
#
#         for row_index, row_data in enumerate(result):
#             for col_index, col_data in enumerate(row_data.values()):
#                 item = QtWidgets.QTableWidgetItem(str(col_data))
#                 self.tableWidget.setItem(row_index, col_index, item)
#
#         cursor.close()
#         bd.close()
#
#
#
#
#
#
# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())

#SQL

# -- phpMyAdmin SQL Dump
# -- version 5.2.0
# -- https://www.phpmyadmin.net/
# --
# -- Хост: 127.0.0.1:3306
# -- Время создания: Май 15 2024 г., 18:24
# -- Версия сервера: 5.5.62-log
# -- Версия PHP: 7.2.34
#
# SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
# START TRANSACTION;
# SET time_zone = "+00:00";
#
#
# /*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
# /*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
# /*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
# /*!40101 SET NAMES utf8mb4 */;
#
# --
# -- База данных: `sklad`
# --
#
# -- --------------------------------------------------------
#
# --
# -- Структура таблицы `auto`
# --
#
# CREATE TABLE `auto` (
#   `id` int(11) NOT NULL,
#   `num_auto` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
#
# --
# -- Дамп данных таблицы `auto`
# --
#
# INSERT INTO `auto` (`id`, `num_auto`) VALUES
# (1, 'В 277 ОУ 72 rus'),
# (2, 'В 345 ОУ 76 rus');
#
# -- --------------------------------------------------------
#
# --
# -- Структура таблицы `gruz`
# --
#
# CREATE TABLE `gruz` (
#   `id` int(11) NOT NULL,
#   `num` varchar(11) COLLATE utf8mb4_unicode_ci NOT NULL,
#   `data` date NOT NULL,
#   `ves` varchar(12) COLLATE utf8mb4_unicode_ci NOT NULL,
#   `kol-vo` int(11) NOT NULL,
#   `id_kat` int(11) NOT NULL
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
#
# --
# -- Дамп данных таблицы `gruz`
# --
#
# INSERT INTO `gruz` (`id`, `num`, `data`, `ves`, `kol-vo`, `id_kat`) VALUES
# (1, '1', '2012-02-20', '300', 10, 1),
# (2, '2', '0000-00-00', '150', 15, 2),
# (3, 'Четыре', '0000-00-00', 'двести кг', 10, 1);
#
# -- --------------------------------------------------------
#
# --
# -- Структура таблицы `kat_gruz`
# --
#
# CREATE TABLE `kat_gruz` (
#   `id` int(11) NOT NULL,
#   `name` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
#
# --
# -- Дамп данных таблицы `kat_gruz`
# --
#
# INSERT INTO `kat_gruz` (`id`, `name`) VALUES
# (1, 'Рассыпной'),
# (2, 'Жидкий ');
#
# -- --------------------------------------------------------
#
# --
# -- Структура таблицы `pokup`
# --
#
# CREATE TABLE `pokup` (
#   `id` int(11) NOT NULL,
#   `name` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
#   `phone` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
#   `bik` int(11) NOT NULL,
#   `lic_schet` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
#
# --
# -- Дамп данных таблицы `pokup`
# --
#
# INSERT INTO `pokup` (`id`, `name`, `phone`, `bik`, `lic_schet`) VALUES
# (2, 'ООО \"Цементум\"', '8-800-555-35-35', 55566678, '04326543546754'),
# (3, 'ИП \"Металиум\"', '8-800-333-23-88', 33366631, '04326543547543'),
# (5, 'ООО\"Горизонт\"', '8-800-766-64-54', 55588822, '75412464324233');
#
# -- --------------------------------------------------------
#
# --
# -- Структура таблицы `tranzakt`
# --
#
# CREATE TABLE `tranzakt` (
#   `id` int(11) NOT NULL,
#   `id_gruz` int(11) NOT NULL,
#   `id_auto` int(11) NOT NULL,
#   `id_pok` int(11) NOT NULL
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
#
# --
# -- Дамп данных таблицы `tranzakt`
# --
#
# INSERT INTO `tranzakt` (`id`, `id_gruz`, `id_auto`, `id_pok`) VALUES
# (2, 1, 2, 3),
# (5, 1, 1, 2),
# (8, 2, 2, 5),
# (9, 3, 2, 2);
#
# --
# -- Индексы сохранённых таблиц
# --
#
# --
# -- Индексы таблицы `auto`
# --
# ALTER TABLE `auto`
#   ADD PRIMARY KEY (`id`);
#
# --
# -- Индексы таблицы `gruz`
# --
# ALTER TABLE `gruz`
#   ADD PRIMARY KEY (`id`),
#   ADD KEY `id_kat` (`id_kat`);
#
# --
# -- Индексы таблицы `kat_gruz`
# --
# ALTER TABLE `kat_gruz`
#   ADD PRIMARY KEY (`id`);
#
# --
# -- Индексы таблицы `pokup`
# --
# ALTER TABLE `pokup`
#   ADD PRIMARY KEY (`id`);
#
# --
# -- Индексы таблицы `tranzakt`
# --
# ALTER TABLE `tranzakt`
#   ADD PRIMARY KEY (`id`),
#   ADD KEY `id_gruz` (`id_gruz`),
#   ADD KEY `id_auto` (`id_auto`),
#   ADD KEY `id_pok` (`id_pok`);
#
# --
# -- AUTO_INCREMENT для сохранённых таблиц
# --
#
# --
# -- AUTO_INCREMENT для таблицы `auto`
# --
# ALTER TABLE `auto`
#   MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
#
# --
# -- AUTO_INCREMENT для таблицы `gruz`
# --
# ALTER TABLE `gruz`
#   MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
#
# --
# -- AUTO_INCREMENT для таблицы `kat_gruz`
# --
# ALTER TABLE `kat_gruz`
#   MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
#
# --
# -- AUTO_INCREMENT для таблицы `pokup`
# --
# ALTER TABLE `pokup`
#   MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
#
# --
# -- AUTO_INCREMENT для таблицы `tranzakt`
# --
# ALTER TABLE `tranzakt`
#   MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
#
# --
# -- Ограничения внешнего ключа сохраненных таблиц
# --
#
# --
# -- Ограничения внешнего ключа таблицы `gruz`
# --
# ALTER TABLE `gruz`
#   ADD CONSTRAINT `gruz_ibfk_1` FOREIGN KEY (`id_kat`) REFERENCES `kat_gruz` (`id`);
#
# --
# -- Ограничения внешнего ключа таблицы `tranzakt`
# --
# ALTER TABLE `tranzakt`
#   ADD CONSTRAINT `tranzakt_ibfk_1` FOREIGN KEY (`id_auto`) REFERENCES `auto` (`id`),
#   ADD CONSTRAINT `tranzakt_ibfk_2` FOREIGN KEY (`id_gruz`) REFERENCES `gruz` (`id`),
#   ADD CONSTRAINT `tranzakt_ibfk_3` FOREIGN KEY (`id_pok`) REFERENCES `pokup` (`id`);
# COMMIT;
#
# /*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
# /*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
# /*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
