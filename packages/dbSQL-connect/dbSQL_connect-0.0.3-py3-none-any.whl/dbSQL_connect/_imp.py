# Переключение
# между
# формами
#
# from win3 import Ui_meneger
#
#
# def openWindow1(self):
#     self.window = QtWidgets.QMainWindow()
#     self.ui = Ui_meneger()
#     self.ui.setupUi(self.window)
#     self.window.show()
#
#
# -----------------------------------------------------------------------------------------------------------
#
# Вывод
# в
# данных
#
# import pymysql.cursors
#
# self.uptable()
#
#
# def uptable(self):
#     bd = pymysql.connect(host='localhost', user='root', passwd='', db='sklad',
#                          cursorclass=pymysql.cursors.DictCursor)
#     cursor = bd.cursor()
#     sql = "select * from gruz"
#     cursor.execute(sql)
#     result = cursor.fetchall()
#
#     self.tableWidget.setRowCount(len(result))
#     self.tableWidget.setColumnCount(4)
#
#     for row_index, row_data in enumerate(result):
#         for col_index, col_data in enumerate(row_data.values()):
#             item = QtWidgets.QTableWidgetItem(str(col_data))
#             self.tableWidget.setItem(row_index, col_index, item)
#
#     cursor.close()
#     bd.close()
#
#
# ------------------------------------------------------------------------------------------------------------
#
# удаление
# данных
#
# self.pushButton.clicked.connect(self.deleteData)
#
#
# def deleteData(self):
#     # Get selected rows
#     selected_rows = self.tableWidget.selectionModel().selectedRows()
#
#     if not selected_rows:
#         QtWidgets.QMessageBox.warning(None, "Warning", "Выберите строки для удаления")
#         return
#
#     rows_to_delete = []
#     for row in selected_rows:
#         rows_to_delete.append(row.row())
#
#     bd = pymysql.connect(host='localhost', user='root', passwd='', db='sklad',
#                          cursorclass=pymysql.cursors.DictCursor)
#     cursor = bd.cursor()
#
#     try:
#         # Delete rows from the database
#         for row in rows_to_delete:
#             item_id = self.tableWidget.item(row, 0).text()
#             sql = "DELETE FROM pokup WHERE id=%s"
#             cursor.execute(sql, (item_id,))
#             bd.commit()
#
#         # Update the table after deletion
#         self.uptable()
#         QtWidgets.QMessageBox.information(None, "Success", "Данные успешно удалены")
#     except Exception as e:
#         bd.rollback()
#         QtWidgets.QMessageBox.critical(None, "Error", f"Ошибка удаления данных: {str(e)}")
#
#     cursor.close()
#     bd.close()
#
#
# -------------------------------------------------------------------------------------------------------------------------------------
#
# Добавление
# данных
#
# self.pushButton.clicked.connect(self.update)
#
#
# def update(self):
#     name = self.textEdit.toPlainText()
#     phone = self.textEdit_2.toPlainText()
#     bik = self.textEdit_3.toPlainText()
#     lic = self.textEdit_4.toPlainText()
#
#     try:
#
#         bd = pymysql.connect(host='localhost', user='root', passwd='',
#                              db='sklad', cursorclass=pymysql.cursors.DictCursor)
#         cursor = bd.cursor()
#         sql = "Insert into pokup values(NULL,%s,%s,%s,%s)"
#         val = (name, phone, bik, lic)
#         cursor.execute(sql, val)
#         bd.commit()
#
#         print("Успешно")
#
#     except Exception as e:
#         print(e)
#
#     finally:
#         cursor.close()
#         bd.close()
#
#
# -------------------------------------------------------------------------------------------------------------------------

