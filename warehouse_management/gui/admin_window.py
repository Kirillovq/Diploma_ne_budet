from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget, QTableWidget, QTableWidgetItem, QLineEdit,
    QMessageBox, QHBoxLayout, QComboBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from utils.db_utils import execute_query, fetch_all, fetch_one


class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Администратор')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.central_widget.setStyleSheet("background-color: #E6E6FA;")

        layout = QVBoxLayout()

        self.label_title = QLabel('Функции администратора')
        self.label_title.setFont(QFont('Arial', 20))
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_title)

        self.button_manage_employees = self.create_button('Управление сотрудниками')
        self.button_manage_employees.clicked.connect(self.manage_employees)
        layout.addWidget(self.button_manage_employees)

        self.button_manage_parts = self.create_button('Управление запчастями')
        self.button_manage_parts.clicked.connect(self.manage_parts)
        layout.addWidget(self.button_manage_parts)

        self.button_view_order_quantity = self.create_button('Просмотр количества заказов')
        self.button_view_order_quantity.clicked.connect(self.view_order_quantity)
        layout.addWidget(self.button_view_order_quantity)

        self.button_view_order_info = self.create_button('Просмотр информации заказов')
        self.button_view_order_info.clicked.connect(self.view_order_info)
        layout.addWidget(self.button_view_order_info)

        self.button_view_sales_statistics = self.create_button('Просмотр статистики продаж')
        self.button_view_sales_statistics.clicked.connect(self.view_sales_statistics)
        layout.addWidget(self.button_view_sales_statistics)

        self.button_view_parts_quantity = self.create_button('Просмотр количества запчастей')
        self.button_view_parts_quantity.clicked.connect(self.view_parts_quantity)
        layout.addWidget(self.button_view_parts_quantity)

        self.button_manage_tables = self.create_button('Управление таблицами')
        self.button_manage_tables.clicked.connect(self.manage_tables)
        layout.addWidget(self.button_manage_tables)

        self.button_back = self.create_button('Назад')
        self.button_back.clicked.connect(self.back)
        layout.addWidget(self.button_back)

        self.central_widget.setLayout(layout)

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

    def view_order_quantity(self):
        orders = fetch_all("SELECT COUNT(*) FROM orders")
        QMessageBox.information(self, 'Количество заказов', f"Количество заказов: {orders[0][0]}")

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

        self.central_widget.setStyleSheet("background-color: #E6E6FA;")

        layout = QVBoxLayout()

        self.label_title = QLabel('Управление сотрудниками')
        self.label_title.setFont(QFont('Arial', 20))
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_title)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.button_add = self.create_button('Добавить сотрудника')
        self.button_add.clicked.connect(self.add_employee)
        layout.addWidget(self.button_add)

        self.button_delete = self.create_button('Удалить сотрудника')
        self.button_delete.clicked.connect(self.delete_employee)
        layout.addWidget(self.button_delete)

        self.button_update = self.create_button('Изменить сотрудника')
        self.button_update.clicked.connect(self.update_employee)
        layout.addWidget(self.button_update)

        self.button_load = self.create_button('Загрузить сотрудников')
        self.button_load.clicked.connect(self.load_employees)
        layout.addWidget(self.button_load)

        self.button_back = self.create_button('Назад')
        self.button_back.clicked.connect(self.back)
        layout.addWidget(self.button_back)

        self.central_widget.setLayout(layout)
        self.load_employees()

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
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['ID', 'Имя', 'Фамилия', 'Должность', 'Зарплата'])

        for row_index, row_data in enumerate(employees):
            for col_index, col_data in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

    def add_employee(self):
        first_name, ok = QInputDialog.getText(self, 'Имя сотрудника', 'Введите имя:')
        if not ok or not first_name:
            return
        last_name, ok = QInputDialog.getText(self, 'Фамилия сотрудника', 'Введите фамилию:')
        if not ok or not last_name:
            return
        position, ok = QInputDialog.getText(self, 'Должность сотрудника', 'Введите должность:')
        if not ok or not position:
            return
        salary, ok = QInputDialog.getInt(self, 'Зарплата сотрудника', 'Введите зарплату:')
        if not ok or not salary:
            return

        execute_query("INSERT INTO employees (first_name, last_name, position, salary) VALUES (?, ?, ?, ?)",
                      (first_name, last_name, position, salary))
        QMessageBox.information(self, 'Успех', 'Сотрудник добавлен')
        self.load_employees()

    def delete_employee(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, 'Ошибка', 'Выберите строку для удаления')
            return

        employee_id = self.table.item(row, 0).text()
        execute_query("DELETE FROM employees WHERE employee_id = ?", (employee_id,))
        QMessageBox.information(self, 'Успех', 'Сотрудник удален')
        self.load_employees()

    def update_employee(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, 'Ошибка', 'Выберите строку для изменения')
            return

        employee_id = self.table.item(row, 0).text()
        first_name, ok = QInputDialog.getText(self, 'Имя сотрудника', 'Введите имя:',
                                              text=self.table.item(row, 1).text())
        if not ok or not first_name:
            return
        last_name, ok = QInputDialog.getText(self, 'Фамилия сотрудника', 'Введите фамилию:',
                                             text=self.table.item(row, 2).text())
        if not ok or not last_name:
            return
        position, ok = QInputDialog.getText(self, 'Должность сотрудника', 'Введите должность:',
                                            text=self.table.item(row, 3).text())
        if not ok or not position:
            return
        salary, ok = QInputDialog.getInt(self, 'Зарплата сотрудника', 'Введите зарплату:',
                                         value=int(self.table.item(row, 4).text()))
        if not ok or not salary:
            return

        execute_query(
            "UPDATE employees SET first_name = ?, last_name = ?, position = ?, salary = ? WHERE employee_id = ?",
            (first_name, last_name, position, salary, employee_id))
        QMessageBox.information(self, 'Успех', 'Сотрудник изменен')
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

        self.central_widget.setStyleSheet("background-color: #E6E6FA;")

        layout = QVBoxLayout()

        self.label_title = QLabel('Управление запчастями')
        self.label_title.setFont(QFont('Arial', 20))
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_title)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.button_add = self.create_button('Добавить запчасть')
        self.button_add.clicked.connect(self.add_part)
        layout.addWidget(self.button_add)

        self.button_delete = self.create_button('Удалить запчасть')
        self.button_delete.clicked.connect(self.delete_part)
        layout.addWidget(self.button_delete)

        self.button_update = self.create_button('Изменить запчасть')
        self.button_update.clicked.connect(self.update_part)
        layout.addWidget(self.button_update)

        self.button_load = self.create_button('Загрузить запчасти')
        self.button_load.clicked.connect(self.load_parts)
        layout.addWidget(self.button_load)

        self.button_back = self.create_button('Назад')
        self.button_back.clicked.connect(self.back)
        layout.addWidget(self.button_back)

        self.central_widget.setLayout(layout)
        self.load_parts()

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
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ['ID', 'Название', 'Производитель', 'Модель', 'Цена', 'Количество на складе'])

        for row_index, row_data in enumerate(parts):
            for col_index, col_data in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

    def add_part(self):
        part_name, ok = QInputDialog.getText(self, 'Название запчасти', 'Введите название:')
        if not ok or not part_name:
            return
        manufacturer, ok = QInputDialog.getText(self, 'Производитель', 'Введите производителя:')
        if not ok or not manufacturer:
            return
        car_model, ok = QInputDialog.getText(self, 'Модель автомобиля', 'Введите модель автомобиля:')
        if not ok or not car_model:
            return
        price, ok = QInputDialog.getInt(self, 'Цена', 'Введите цену:')
        if not ok or not price:
            return
        quantity_in_stock, ok = QInputDialog.getInt(self, 'Количество на складе', 'Введите количество на складе:')
        if not ok or not quantity_in_stock:
            return

        execute_query(
            "INSERT INTO parts (part_name, manufacturer, car_model, price, quantity_in_stock) VALUES (?, ?, ?, ?, ?)",
            (part_name, manufacturer, car_model, price, quantity_in_stock))
        QMessageBox.information(self, 'Успех', 'Запчасть добавлена')
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

    def update_part(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, 'Ошибка', 'Выберите строку для изменения')
            return

        part_id = self.table.item(row, 0).text()
        part_name, ok = QInputDialog.getText(self, 'Название запчасти', 'Введите название:',
                                             text=self.table.item(row, 1).text())
        if not ok or not part_name:
            return
        manufacturer, ok = QInputDialog.getText(self, 'Производитель', 'Введите производителя:',
                                                text=self.table.item(row, 2).text())
        if not ok or not manufacturer:
            return
        car_model, ok = QInputDialog.getText(self, 'Модель автомобиля', 'Введите модель автомобиля:',
                                             text=self.table.item(row, 3).text())
        if not ok or not car_model:
            return
        price, ok = QInputDialog.getInt(self, 'Цена', 'Введите цену:', value=int(self.table.item(row, 4).text()))
        if not ok or not price:
            return
        quantity_in_stock, ok = QInputDialog.getInt(self, 'Количество на складе', 'Введите количество на складе:',
                                                    value=int(self.table.item(row, 5).text()))
        if not ok or not quantity_in_stock:
            return

        execute_query(
            "UPDATE parts SET part_name = ?, manufacturer = ?, car_model = ?, price = ?, quantity_in_stock = ? WHERE part_id = ?",
            (part_name, manufacturer, car_model, price, quantity_in_stock, part_id))
        QMessageBox.information(self, 'Успех', 'Запчасть изменена')
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

        self.central_widget.setStyleSheet("background-color: #E6E6FA;")

        layout = QVBoxLayout()

        self.label_title = QLabel('Информация о заказах')
        self.label_title.setFont(QFont('Arial', 20))
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_title)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['ID', 'Customer ID', 'Order Date', 'Status'])
        self.table.setRowCount(len(orders))

        for row_index, row_data in enumerate(orders):
            for col_index, col_data in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

        layout.addWidget(self.table)

        self.button_back = QPushButton('Назад')
        self.button_back.setFont(QFont('Arial', 14))
        self.button_back.setStyleSheet(
            "background-color: #9370DB; color: white; border-radius: 15px; padding: 10px;"
        )
        self.button_back.clicked.connect(self.back)
        layout.addWidget(self.button_back)

        self.central_widget.setLayout(layout)

    def back(self):
        self.close()


class StatisticsWindow(QMainWindow):
    def __init__(self, statistics):
        super().__init__()
        self.setWindowTitle('Статистика продаж')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.central_widget.setStyleSheet("background-color: #E6E6FA;")

        layout = QVBoxLayout()

        self.label_title = QLabel('Часто покупаемые товары')
        self.label_title.setFont(QFont('Arial', 20))
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_title)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Название товара', 'Количество заказов'])
        self.table.setRowCount(len(statistics))

        for row_index, row_data in enumerate(statistics):
            for col_index, col_data in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

        layout.addWidget(self.table)

        self.button_back = QPushButton('Назад')
        self.button_back.setFont(QFont('Arial', 14))
        self.button_back.setStyleSheet(
            "background-color: #9370DB; color: white; border-radius: 15px; padding: 10px;"
        )
        self.button_back.clicked.connect(self.back)
        layout.addWidget(self.button_back)

        self.central_widget.setLayout(layout)

    def back(self):
        self.close()


class PartsQuantityWindow(QMainWindow):
    def __init__(self, parts_quantity):
        super().__init__()
        self.setWindowTitle('Количество запчастей')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.central_widget.setStyleSheet("background-color: #E6E6FA;")

        layout = QVBoxLayout()

        self.label_title = QLabel('Количество запчастей')
        self.label_title.setFont(QFont('Arial', 20))
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_title)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Название запчасти', 'Количество на складе'])
        self.table.setRowCount(len(parts_quantity))

        for row_index, row_data in enumerate(parts_quantity):
            for col_index, col_data in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

        layout.addWidget(self.table)

        self.button_back = QPushButton('Назад')
        self.button_back.setFont(QFont('Arial', 14))
        self.button_back.setStyleSheet(
            "background-color: #9370DB; color: white; border-radius: 15px; padding: 10px;"
        )
        self.button_back.clicked.connect(self.back)
        layout.addWidget(self.button_back)

        self.central_widget.setLayout(layout)

    def back(self):
        self.close()


class TablesWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Управление таблицами')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.central_widget.setStyleSheet("background-color: #E6E6FA;")

        layout = QVBoxLayout()

        self.label_title = QLabel('Управление таблицами')
        self.label_title.setFont(QFont('Arial', 20))
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_title)

        self.combo_tables = QComboBox()
        self.combo_tables.addItems(
            ['employees', 'suppliers', 'parts', 'customers', 'orders', 'order_details', 'deliveries', 'payments'])
        layout.addWidget(self.combo_tables)

        self.button_load_table = self.create_button('Загрузить таблицу')
        self.button_load_table.clicked.connect(self.load_table)
        layout.addWidget(self.button_load_table)

        self.table = QTableWidget()
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
        self.button_back.clicked.connect(self.back)
        layout.addWidget(self.button_back)

        self.central_widget.setLayout(layout)

    def create_button(self, text):
        button = QPushButton(text)
        button.setFont(QFont('Arial', 14))
        button.setStyleSheet(
            "background-color: #9370DB; color: white; border-radius: 15px; padding: 10px;"
        )
        return button

    def load_table(self):
        table_name = self.combo_tables.currentText()
        data = fetch_all(f"SELECT * FROM {table_name}")
        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(data[0]) if data else 0)
        self.table.setHorizontalHeaderLabels([description[0] for description in self.table.model().headerData])

        for row_index, row_data in enumerate(data):
            for col_index, col_data in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

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
