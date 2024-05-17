from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget, QTableWidget, QTableWidgetItem, \
    QLineEdit, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from utils.db_utils import execute_query, fetch_all


class EmployeeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Сотрудник')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.central_widget.setStyleSheet("background-color: #E6E6FA;")

        layout = QVBoxLayout()

        self.label_title = QLabel('Функции сотрудника')
        self.label_title.setFont(QFont('Arial', 20))
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_title)

        self.button_manage_parts = self.create_button('Управление запчастями')
        self.button_manage_parts.clicked.connect(self.manage_parts)
        layout.addWidget(self.button_manage_parts)

        self.button_view_order_quantity = self.create_button('Просмотр количества заказов')
        self.button_view_order_quantity.clicked.connect(self.view_order_quantity)
        layout.addWidget(self.button_view_order_quantity)

        self.button_view_order_info = self.create_button('Просмотр информации заказов')
        self.button_view_order_info.clicked.connect(self.view_order_info)
        layout.addWidget(self.button_view_order_info)

        self.button_view_parts_quantity = self.create_button('Просмотр количества запчастей')
        self.button_view_parts_quantity.clicked.connect(self.view_parts_quantity)
        layout.addWidget(self.button_view_parts_quantity)

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

    def view_parts_quantity(self):
        parts_quantity = fetch_all("SELECT part_name, quantity_in_stock FROM parts")
        self.parts_quantity_window = PartsQuantityWindow(parts_quantity)
        self.parts_quantity_window.show()

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
