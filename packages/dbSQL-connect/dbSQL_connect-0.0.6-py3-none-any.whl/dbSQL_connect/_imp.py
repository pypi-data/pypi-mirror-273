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
# -- phpMyAdmin SQL Dump
# -- version 5.2.0
# -- https://www.phpmyadmin.net/
# --
# -- Хост: 127.0.0.1:3306
# -- Время создания: Май 17 2024 г., 10:53
# -- Версия сервера: 8.0.30
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
#   `id` int NOT NULL,
#   `num_auto` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL
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
#   `id` int NOT NULL,
#   `num` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
#   `data` date NOT NULL,
#   `ves` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
#   `kol-vo` int NOT NULL,
#   `id_kat` int NOT NULL
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
#   `id` int NOT NULL,
#   `name` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL
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
#   `id` int NOT NULL,
#   `name` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
#   `phone` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
#   `bik` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
#   `lic_schet` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
#
# --
# -- Дамп данных таблицы `pokup`
# --
#
# INSERT INTO `pokup` (`id`, `name`, `phone`, `bik`, `lic_schet`) VALUES
# (2, 'ООО \"Цементум\"', '8-800-555-35-35', '55566678', '04326543546754'),
# (3, 'ИП \"Металиум\"', '8-800-333-23-88', '33366631', '04326543547543'),
# (5, 'ООО\"Горизонт\"', '8-800-766-64-54', '55588822', '75412464324233');
#
# -- --------------------------------------------------------
#
# --
# -- Структура таблицы `tranzakt`
# --
#
# CREATE TABLE `tranzakt` (
#   `id` int NOT NULL,
#   `id_gruz` int NOT NULL,
#   `id_auto` int NOT NULL,
#   `id_pok` int NOT NULL
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
#   MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
#
# --
# -- AUTO_INCREMENT для таблицы `gruz`
# --
# ALTER TABLE `gruz`
#   MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
#
# --
# -- AUTO_INCREMENT для таблицы `kat_gruz`
# --
# ALTER TABLE `kat_gruz`
#   MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
#
# --
# -- AUTO_INCREMENT для таблицы `pokup`
# --
# ALTER TABLE `pokup`
#   MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;
#
# --
# -- AUTO_INCREMENT для таблицы `tranzakt`
# --
# ALTER TABLE `tranzakt`
#   MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
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

