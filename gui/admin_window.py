import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget, QTableWidget, QTableWidgetItem,
    QMessageBox, QHBoxLayout, QGridLayout, QFormLayout, QDialog, QLineEdit, QComboBox
)
from PyQt6.QtGui import QFont, QPalette, QPixmap, QBrush
from PyQt6.QtCore import Qt
from utils.db_utils import execute_query, fetch_all


class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Администратор')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.set_background()

        layout = QGridLayout()

        self.label_company = QLabel('Авто запчасть трейд')
        self.label_company.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        self.label_company.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_company.setStyleSheet("color: brown;")
        layout.addWidget(self.label_company, 0, 0, 1, 2)

        self.button_manage_employees = self.create_button('Управление сотрудниками')
        self.button_manage_employees.clicked.connect(self.manage_employees)
        layout.addWidget(self.button_manage_employees, 1, 0)

        self.button_manage_parts = self.create_button('Управление запчастями')
        self.button_manage_parts.clicked.connect(self.manage_parts)
        layout.addWidget(self.button_manage_parts, 1, 1)

        self.button_view_order_info = self.create_button('Просмотр информации заказов')
        self.button_view_order_info.clicked.connect(self.view_order_info)
        layout.addWidget(self.button_view_order_info, 2, 0)

        self.button_view_sales_statistics = self.create_button('Просмотр статистики продаж')
        self.button_view_sales_statistics.clicked.connect(self.view_sales_statistics)
        layout.addWidget(self.button_view_sales_statistics, 2, 1)

        self.button_view_parts_quantity = self.create_button('Просмотр количества запчастей')
        self.button_view_parts_quantity.clicked.connect(self.view_parts_quantity)
        layout.addWidget(self.button_view_parts_quantity, 3, 0)

        self.button_manage_tables = self.create_button('Управление таблицами')
        self.button_manage_tables.clicked.connect(self.manage_tables)
        layout.addWidget(self.button_manage_tables, 3, 1)

        self.button_back = self.create_button('Назад')
        self.button_back.clicked.connect(self.back)
        layout.addWidget(self.button_back, 4, 0, 1, 2)

        self.central_widget.setLayout(layout)

    def set_background(self):
        palette = QPalette()
        pixmap = QPixmap("img/backfon1.jpg")
        palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
        self.setPalette(palette)

    def create_button(self, text):
        button = QPushButton(text)
        button.setFont(QFont('Arial', 14))
        button.setStyleSheet(
            "background-color: #9370DB; color: white; border-radius: 15px; padding: 10px;"
        )
        return button

    def manage_employees(self):
        self.employees_window = ManageEmployeesWindow()
        self.employees_window.show()

    def manage_parts(self):
        self.parts_window = ManagePartsWindow()
        self.parts_window.show()

    def view_order_info(self):
        orders = fetch_all("SELECT * FROM orders")
        self.order_info_window = OrderInfoWindow(orders)
        self.order_info_window.show()

    def view_sales_statistics(self):
        statistics = fetch_all(
            "SELECT part_name, COUNT(*) as count FROM order_details JOIN parts ON order_details.part_id = parts.part_id GROUP BY part_name ORDER BY count DESC")
        self.statistics_window = StatisticsWindow(statistics)
        self.statistics_window.show()

    def view_parts_quantity(self):
        parts_quantity = fetch_all("SELECT part_name, quantity_in_stock FROM parts")
        self.parts_quantity_window = PartsQuantityWindow(parts_quantity)
        self.parts_quantity_window.show()

    def manage_tables(self):
        self.tables_window = TablesWindow()
        self.tables_window.show()

    def back(self):
        self.close()


class ManageEmployeesWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Управление сотрудниками')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.set_background()

        layout = QVBoxLayout()

        self.label_title = QLabel('Управление сотрудниками')
        self.label_title.setFont(QFont('Arial', 20))
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setStyleSheet("color: brown;")
        layout.addWidget(self.label_title)

        self.table = QTableWidget()
        self.table.setStyleSheet("background: transparent;")
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['ID', 'Имя', 'Фамилия', 'Должность', 'Зарплата'])
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

        self.button_add = self.create_button('Добавить сотрудника')
        self.button_add.clicked.connect(lambda: self.show_employee_dialog(is_edit=False))
        layout.addWidget(self.button_add)

        self.button_update = self.create_button('Изменить сотрудника')
        self.button_update.clicked.connect(lambda: self.show_employee_dialog(is_edit=True))
        layout.addWidget(self.button_update)

        self.button_delete = self.create_button('Удалить сотрудника')
        self.button_delete.clicked.connect(self.delete_employee)
        layout.addWidget(self.button_delete)

        self.button_back = self.create_button('Назад')
        self.button_back.clicked.connect(self.back)
        layout.addWidget(self.button_back)

        self.central_widget.setLayout(layout)
        self.load_employees()

    def set_background(self):
        palette = QPalette()
        pixmap = QPixmap("img/backfon1.jpg")
        palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
        self.setPalette(palette)

    def create_button(self, text):
        button = QPushButton(text)
        button.setFont(QFont('Arial', 14))
        button.setStyleSheet(
            "background-color: #9370DB; color: white; border-radius: 15px; padding: 10px;"
        )
        return button

    def load_employees(self):
        employees = fetch_all("SELECT * FROM employees")
        self.table.setRowCount(len(employees))

        for row_index, row_data in enumerate(employees):
            for col_index, col_data in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

    def show_employee_dialog(self, is_edit=False):
        selected_row = self.table.currentRow() if is_edit else None
        if is_edit and selected_row < 0:
            QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, выберите сотрудника для редактирования')
            return

        dialog = QDialog(self)
        dialog.setWindowTitle('Изменить сотрудника' if is_edit else 'Добавить сотрудника')
        dialog.setGeometry(100, 100, 300, 200)

        layout = QFormLayout()

        if is_edit:
            employee_id = self.table.item(selected_row, 0).text()
            first_name = self.table.item(selected_row, 1).text()
            last_name = self.table.item(selected_row, 2).text()
            position = self.table.item(selected_row, 3).text()
            salary = self.table.item(selected_row, 4).text()
        else:
            employee_id = None
            first_name = ""
            last_name = ""
            position = ""
            salary = ""

        self.input_first_name = QLineEdit(first_name)
        self.input_last_name = QLineEdit(last_name)
        self.input_position = QLineEdit(position)
        self.input_salary = QLineEdit(salary)

        layout.addRow('Имя:', self.input_first_name)
        layout.addRow('Фамилия:', self.input_last_name)
        layout.addRow('Должность:', self.input_position)
        layout.addRow('Зарплата:', self.input_salary)

        button_save = QPushButton('Обновить' if is_edit else 'Добавить')
        button_save.clicked.connect(lambda: self.save_employee(dialog, employee_id))
        layout.addWidget(button_save)

        dialog.setLayout(layout)
        dialog.exec()

    def save_employee(self, dialog, employee_id):
        first_name = self.input_first_name.text()
        last_name = self.input_last_name.text()
        position = self.input_position.text()
        salary = self.input_salary.text()

        if not first_name or not last_name or not position or not salary:
            QMessageBox.warning(self, 'Ошибка', 'Все поля должны быть заполнены')
            return

        if employee_id:
            execute_query("UPDATE employees SET first_name = ?, last_name = ?, position = ?, salary = ? WHERE employee_id = ?",
                          (first_name, last_name, position, salary, employee_id))
            QMessageBox.information(self, 'Успех', 'Сотрудник обновлен')
        else:
            execute_query("INSERT INTO employees (first_name, last_name, position, salary) VALUES (?, ?, ?, ?)",
                          (first_name, last_name, position, salary))
            QMessageBox.information(self, 'Успех', 'Сотрудник добавлен')

        dialog.accept()
        self.load_employees()

    def delete_employee(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, выберите сотрудника для удаления')
            return

        employee_id = self.table.item(selected_row, 0).text()

        execute_query("DELETE FROM employees WHERE employee_id = ?", (employee_id,))
        QMessageBox.information(self, 'Успех', 'Сотрудник удален')
        self.load_employees()

    def back(self):
        self.close()


class ManagePartsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Управление запчастями')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.set_background()

        layout = QVBoxLayout()

        self.label_title = QLabel('Управление запчастями')
        self.label_title.setFont(QFont('Arial', 20))
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setStyleSheet("color: brown;")
        layout.addWidget(self.label_title)

        self.table = QTableWidget()
        self.table.setStyleSheet("background: transparent;")
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ['ID', 'Название', 'Производитель', 'Модель', 'Цена', 'Количество на складе'])
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

        self.button_add = self.create_button('Добавить запчасть')
        self.button_add.clicked.connect(lambda: self.show_part_dialog(is_edit=False))
        layout.addWidget(self.button_add)

        self.button_delete = self.create_button('Удалить запчасть')
        self.button_delete.clicked.connect(self.delete_part)
        layout.addWidget(self.button_delete)

        self.button_update = self.create_button('Изменить запчасть')
        self.button_update.clicked.connect(lambda: self.show_part_dialog(is_edit=True))
        layout.addWidget(self.button_update)

        self.button_back = self.create_button('Назад')
        self.button_back.clicked.connect(self.back)
        layout.addWidget(self.button_back)

        self.central_widget.setLayout(layout)
        self.load_parts()

    def set_background(self):
        palette = QPalette()
        pixmap = QPixmap("img/backfon1.jpg")
        palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
        self.setPalette(palette)

    def create_button(self, text):
        button = QPushButton(text)
        button.setFont(QFont('Arial', 14))
        button.setStyleSheet(
            "background-color: #9370DB; color: white; border-radius: 15px; padding: 10px;"
        )
        return button

    def load_parts(self):
        parts = fetch_all("SELECT * FROM parts")
        self.table.setRowCount(len(parts))

        for row_index, row_data in enumerate(parts):
            for col_index, col_data in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

    def show_part_dialog(self, is_edit=False):
        selected_row = self.table.currentRow() if is_edit else None
        if is_edit and selected_row < 0:
            QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, выберите запчасть для редактирования')
            return

        dialog = QDialog(self)
        dialog.setWindowTitle('Изменить запчасть' if is_edit else 'Добавить запчасть')
        dialog.setGeometry(100, 100, 300, 200)

        layout = QFormLayout()

        if is_edit:
            part_id = self.table.item(selected_row, 0).text()
            part_name = self.table.item(selected_row, 1).text()
            manufacturer = self.table.item(selected_row, 2).text()
            car_model = self.table.item(selected_row, 3).text()
            price = self.table.item(selected_row, 4).text()
            quantity_in_stock = self.table.item(selected_row, 5).text()
        else:
            part_id = None
            part_name = ""
            manufacturer = ""
            car_model = ""
            price = ""
            quantity_in_stock = ""

        self.input_part_name = QLineEdit(part_name)
        self.input_manufacturer = QLineEdit(manufacturer)
        self.input_car_model = QLineEdit(car_model)
        self.input_price = QLineEdit(price)
        self.input_quantity_in_stock = QLineEdit(quantity_in_stock)

        layout.addRow('Название:', self.input_part_name)
        layout.addRow('Производитель:', self.input_manufacturer)
        layout.addRow('Модель:', self.input_car_model)
        layout.addRow('Цена:', self.input_price)
        layout.addRow('Количество на складе:', self.input_quantity_in_stock)

        button_save = QPushButton('Обновить' if is_edit else 'Добавить')
        button_save.clicked.connect(lambda: self.save_part(dialog, part_id))
        layout.addWidget(button_save)

        dialog.setLayout(layout)
        dialog.exec()

    def save_part(self, dialog, part_id):
        part_name = self.input_part_name.text()
        manufacturer = self.input_manufacturer.text()
        car_model = self.input_car_model.text()
        price = self.input_price.text()
        quantity_in_stock = self.input_quantity_in_stock.text()

        if not part_name or not manufacturer or not car_model or not price or not quantity_in_stock:
            QMessageBox.warning(self, 'Ошибка', 'Все поля должны быть заполнены')
            return

        if part_id:
            execute_query(
                "UPDATE parts SET part_name = ?, manufacturer = ?, car_model = ?, price = ?, quantity_in_stock = ? WHERE part_id = ?",
                (part_name, manufacturer, car_model, price, quantity_in_stock, part_id))
            QMessageBox.information(self, 'Успех', 'Запчасть обновлена')
        else:
            execute_query(
                "INSERT INTO parts (part_name, manufacturer, car_model, price, quantity_in_stock) VALUES (?, ?, ?, ?, ?)",
                (part_name, manufacturer, car_model, price, quantity_in_stock))
            QMessageBox.information(self, 'Успех', 'Запчасть добавлена')

        dialog.accept()
        self.load_parts()

    def delete_part(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, 'Ошибка', 'Выберите строку для удаления')
            return

        part_id = self.table.item(row, 0).text()
        execute_query("DELETE FROM parts WHERE part_id = ?", (part_id,))
        QMessageBox.information(self, 'Успех', 'Запчасть удалена')
        self.load_parts()

    def back(self):
        self.close()


class OrderInfoWindow(QMainWindow):
    def __init__(self, orders):
        super().__init__()
        self.setWindowTitle('Просмотр информации заказов')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.set_background()

        layout = QVBoxLayout()

        self.label_title = QLabel('Информация о заказах')
        self.label_title.setFont(QFont('Arial', 20))
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setStyleSheet("color: brown;")
        layout.addWidget(self.label_title)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['ID', 'Customer ID', 'Order Date', 'Status'])
        self.table.setRowCount(len(orders))
        self.table.setStyleSheet("background: transparent;")
        self.table.verticalHeader().setVisible(False)

        for row_index, row_data in enumerate(orders):
            for col_index, col_data in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

        layout.addWidget(self.table)

        self.button_back = self.create_button('Назад')
        layout.addWidget(self.button_back)

        self.central_widget.setLayout(layout)

    def set_background(self):
        palette = QPalette()
        pixmap = QPixmap("img/backfon1.jpg")
        palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
        self.setPalette(palette)

    def create_button(self, text):
        button = QPushButton(text)
        button.setFont(QFont('Arial', 14))
        button.setStyleSheet(
            "background-color: #9370DB; color: white; border-radius: 15px; padding: 10px;"
        )
        button.clicked.connect(self.back)
        return button

    def back(self):
        self.close()


class StatisticsWindow(QMainWindow):
    def __init__(self, statistics):
        super().__init__()
        self.setWindowTitle('Статистика продаж')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.set_background()

        layout = QVBoxLayout()

        self.label_title = QLabel('Часто покупаемые товары')
        self.label_title.setFont(QFont('Arial', 20))
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setStyleSheet("color: brown;")
        layout.addWidget(self.label_title)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Название товара', 'Количество заказов'])
        self.table.setRowCount(len(statistics))
        self.table.setStyleSheet("background: transparent;")
        self.table.verticalHeader().setVisible(False)

        for row_index, row_data in enumerate(statistics):
            for col_index, col_data in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

        layout.addWidget(self.table)

        self.button_back = self.create_button('Назад')
        layout.addWidget(self.button_back)

        self.central_widget.setLayout(layout)

    def set_background(self):
        palette = QPalette()
        pixmap = QPixmap("img/backfon1.jpg")
        palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
        self.setPalette(palette)

    def create_button(self, text):
        button = QPushButton(text)
        button.setFont(QFont('Arial', 14))
        button.setStyleSheet(
            "background-color: #9370DB; color: white; border-radius: 15px; padding: 10px;"
        )
        button.clicked.connect(self.back)
        return button

    def back(self):
        self.close()


class PartsQuantityWindow(QMainWindow):
    def __init__(self, parts_quantity):
        super().__init__()
        self.setWindowTitle('Количество запчастей')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.set_background()

        layout = QVBoxLayout()

        self.label_title = QLabel('Количество запчастей')
        self.label_title.setFont(QFont('Arial', 20))
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setStyleSheet("color: brown;")
        layout.addWidget(self.label_title)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Название запчасти', 'Количество на складе'])
        self.table.setRowCount(len(parts_quantity))
        self.table.setStyleSheet("background: transparent;")
        self.table.verticalHeader().setVisible(False)

        for row_index, row_data in enumerate(parts_quantity):
            for col_index, col_data in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

        layout.addWidget(self.table)

        self.button_back = self.create_button('Назад')
        layout.addWidget(self.button_back)

        self.central_widget.setLayout(layout)

    def set_background(self):
        palette = QPalette()
        pixmap = QPixmap("img/backfon1.jpg")
        palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
        self.setPalette(palette)

    def create_button(self, text):
        button = QPushButton(text)
        button.setFont(QFont('Arial', 14))
        button.setStyleSheet(
            "background-color: #9370DB; color: white; border-radius: 15px; padding: 10px;"
        )
        button.clicked.connect(self.back)
        return button

    def back(self):
        self.close()


class TablesWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Управление таблицами')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.set_background()

        layout = QVBoxLayout()

        self.label_title = QLabel('Управление таблицами')
        self.label_title.setFont(QFont('Arial', 20))
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setStyleSheet("color: brown;")
        layout.addWidget(self.label_title)

        self.combo_tables = QComboBox()
        self.combo_tables.addItems(
            ['employees', 'suppliers', 'parts', 'customers', 'orders', 'order_details', 'deliveries', 'payments'])
        layout.addWidget(self.combo_tables)

        self.button_load_table = self.create_button('Загрузить таблицу')
        self.button_load_table.clicked.connect(self.load_table)
        layout.addWidget(self.button_load_table)

        self.table = QTableWidget()
        self.table.setStyleSheet("background: transparent;")
        layout.addWidget(self.table)

        self.button_add_row = self.create_button('Добавить строку')
        self.button_add_row.clicked.connect(self.add_row)
        layout.addWidget(self.button_add_row)

        self.button_delete_row = self.create_button('Удалить строку')
        self.button_delete_row.clicked.connect(self.delete_row)
        layout.addWidget(self.button_delete_row)

        self.button_update_row = self.create_button('Обновить строку')
        self.button_update_row.clicked.connect(self.update_row)
        layout.addWidget(self.button_update_row)

        self.button_back = self.create_button('Назад')
        layout.addWidget(self.button_back)

        self.central_widget.setLayout(layout)

    def set_background(self):
        palette = QPalette()
        pixmap = QPixmap("img/backfon1.jpg")
        palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
        self.setPalette(palette)

    def create_button(self, text):
        button = QPushButton(text)
        button.setFont(QFont('Arial', 14))
        button.setStyleSheet(
            "background-color: #9370DB; color: white; border-radius: 15px; padding: 10px;"
        )
        button.clicked.connect(self.back)
        return button

    def load_table(self):
        table_name = self.combo_tables.currentText()
        data = fetch_all(f"SELECT * FROM {table_name}")
        if data:
            headers = [description[0] for description in fetch_all(f"PRAGMA table_info({table_name})")]
            self.table.setColumnCount(len(headers))
            self.table.setRowCount(len(data))
            self.table.setHorizontalHeaderLabels(headers)

            for row_index, row_data in enumerate(data):
                for col_index, col_data in enumerate(row_data):
                    self.table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))
        else:
            self.table.setColumnCount(0)
            self.table.setRowCount(0)

    def add_row(self):
        table_name = self.combo_tables.currentText()
        column_count = self.table.columnCount()
        columns = ', '.join([self.table.horizontalHeaderItem(i).text() for i in range(column_count)])
        placeholders = ', '.join(['?' for _ in range(column_count)])
        row_data = [self.table.item(self.table.rowCount() - 1, i).text() for i in range(column_count)]

        execute_query(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", tuple(row_data))
        QMessageBox.information(self, 'Успех', 'Строка добавлена')
        self.load_table()

    def delete_row(self):
        table_name = self.combo_tables.currentText()
        row = self.table.currentRow()
        primary_key = self.table.horizontalHeaderItem(0).text()
        primary_key_value = self.table.item(row, 0).text()

        execute_query(f"DELETE FROM {table_name} WHERE {primary_key} = ?", (primary_key_value,))
        QMessageBox.information(self, 'Успех', 'Строка удалена')
        self.load_table()

    def update_row(self):
        table_name = self.combo_tables.currentText()
        row = self.table.currentRow()
        column_count = self.table.columnCount()
        primary_key = self.table.horizontalHeaderItem(0).text()
        primary_key_value = self.table.item(row, 0).text()
        set_clause = ', '.join([f"{self.table.horizontalHeaderItem(i).text()} = ?" for i in range(1, column_count)])
        row_data = [self.table.item(row, i).text() for i in range(1, column_count)]

        execute_query(f"UPDATE {table_name} SET {set_clause} WHERE {primary_key} = ?", (*row_data, primary_key_value))
        QMessageBox.information(self, 'Успех', 'Строка обновлена')
        self.load_table()

    def back(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AdminWindow()
    window.show()
    sys.exit(app.exec())
