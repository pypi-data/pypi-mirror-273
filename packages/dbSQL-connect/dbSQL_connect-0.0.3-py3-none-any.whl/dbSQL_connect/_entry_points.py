# ДОБАВЛЕНИЕ, РЕДАКТИРОВАНИЕ, УДАЛЕНИЕ
#pymysql
#mysql.connector
#pymysql.cursor
#pyqt5

# import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox
# import mysql.connector
#
# class DatabaseApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Информация из базы данных")
#         self.layout = QVBoxLayout()
#         self.setLayout(self.layout)
#
#         # Устанавливаем соединение с базой данных
#         self.db_connection = mysql.connector.connect(
#             host='localhost',
#             user='root',
#             password='',
#             database='nepoceda'
#         )
#         self.cursor = self.db_connection.cursor()
#
#         # Получаем данные из таблицы pedagog
#         self.cursor.execute("SELECT * FROM pedagog;")
#         self.data = self.cursor.fetchall()
#
#         for row in self.data:
#             row_str = ' | '.join(map(str, row))
#             self.layout.addWidget(QLabel(row_str))
#
#         edit_button = QPushButton('Редактирование')
#         edit_button.clicked.connect(self.edit_data_window)
#         self.layout.addWidget(edit_button)
#
#         add_button = QPushButton('Добавление')
#         add_button.clicked.connect(self.add_data_window)
#         self.layout.addWidget(add_button)
#
#         delete_button = QPushButton('Удаление')
#         delete_button.clicked.connect(self.delete_data)
#         self.layout.addWidget(delete_button)
#
#     # Редактирование
#     def edit_data_window(self):
#         edit_window = QWidget()
#         edit_window.setWindowTitle("Редактирование данных")
#         edit_layout = QVBoxLayout(edit_window)
#
#         input_fields = {}
#
#         for column, value in zip(self.cursor.column_names, self.data[0]):
#             label = QLabel(column)
#             edit_layout.addWidget(label)
#             line_edit = QLineEdit(str(value))
#             edit_layout.addWidget(line_edit)
#             input_fields[column] = line_edit
#
#         save_button = QPushButton('Сохранить')
#         save_button.clicked.connect(lambda: self.save_data(input_fields, edit_window))
#         edit_layout.addWidget(save_button)
#
#         edit_window.show()
#
#     def add_data_window(self):
#         add_window = QWidget()
#         add_window.setWindowTitle("Добавление данных")
#         add_layout = QVBoxLayout(add_window)
#
#         input_fields = {}
#
#         for column in self.cursor.column_names:
#             label = QLabel(column)
#             add_layout.addWidget(label)
#             line_edit = QLineEdit()
#             add_layout.addWidget(line_edit)
#             input_fields[column] = line_edit
#
#         add_button = QPushButton('Добавить')
#         add_button.clicked.connect(lambda: self.add_data(input_fields, add_window))
#         add_layout.addWidget(add_button)
#
#         add_window.show()
#
#     def save_data(self, input_fields, edit_window):
#         new_data = [input_fields[column].text() for column in self.cursor.column_names]
#
#         update_query = "UPDATE pedagog SET {} WHERE {}".format(
#             ", ".join("{} = %s".format(column) for column in self.cursor.column_names),
#             " AND ".join("{} = %s".format(column) for column in self.cursor.column_names))
#
#         self.cursor.execute(update_query, (*new_data, *self.data[0]))
#         self.db_connection.commit()
#
#         QMessageBox.information(self, "Сохранение", "Данные успешно сохранены!")
#         edit_window.close()
#         self.refresh_data()
#
#     def add_data(self, input_fields, add_window):
#         new_data = [input_fields[column].text() for column in self.cursor.column_names]
#
#         insert_query = "INSERT INTO pedagog ({}) VALUES ({})".format(
#             ", ".join(self.cursor.column_names),
#             ", ".join(["%s"] * len(self.cursor.column_names)))
#
#         self.cursor.execute(insert_query, new_data)
#         self.db_connection.commit()
#
#         QMessageBox.information(self, "Добавление", "Данные успешно добавлены!")
#         add_window.close()
#         self.refresh_data()
#
#     def delete_data(self):
#         confirm = QMessageBox.question(self, 'Подтверждение', 'Вы уверены, что хотите удалить всю информацию из таблицы pedagog?',
#                                        QMessageBox.Yes | QMessageBox.No)
#         if confirm == QMessageBox.Yes:
#             delete_query = "DELETE FROM pedagog"
#             self.cursor.execute(delete_query)
#             self.db_connection.commit()
#
#             QMessageBox.information(self, "Удаление", "Вся информация успешно удалена!")
#             self.refresh_data()
#
#     def refresh_data(self):
#         for i in reversed(range(self.layout.count())):
#             widget = self.layout.itemAt(i).widget()
#             if widget is not None:
#                 widget.deleteLater()
#
#         self.cursor.execute("SELECT * FROM pedagog;")
#         self.data = self.cursor.fetchall()
#
#         for row in self.data:
#             row_str = ' | '.join(map(str, row))
#             self.layout.addWidget(QLabel(row_str))
#
#     def closeEvent(self, event):
#         self.cursor.close()
#         self.db_connection.close()
#         event.accept()
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = DatabaseApp()
#     window.show()
#     sys.exit(app.exec_())


