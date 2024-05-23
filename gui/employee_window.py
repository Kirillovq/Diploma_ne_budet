import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget, QTableWidget, QTableWidgetItem,
    QMessageBox, QGridLayout, QLineEdit, QFormLayout, QDialog, QDialogButtonBox
)
from PyQt6.QtGui import QFont, QPalette, QBrush, QPixmap
from PyQt6.QtCore import Qt
from utils.db_utils import execute_query, fetch_all, get_table_info
import sqlite3


class EmployeeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Сотрудник')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.set_background("img/backfon1.jpg")

        layout = QGridLayout()

        self.label_company = QLabel('Авто запчасть трейд')
        self.label_company.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        self.label_company.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_company.setStyleSheet("color: brown;")
        layout.addWidget(self.label_company, 0, 0, 1, 2)

        self.button_manage_parts = self.create_button('Управление запчастями')
        self.button_manage_parts.clicked.connect(self.manage_parts)
        layout.addWidget(self.button_manage_parts, 1, 0)

        self.button_view_orders = self.create_button('Заказы')
        self.button_view_orders.clicked.connect(self.view_orders)
        layout.addWidget(self.button_view_orders, 1, 1)

        self.button_order_status = self.create_button('Статус заказа')
        self.button_order_status.clicked.connect(self.view_order_status)
        layout.addWidget(self.button_order_status, 2, 0)

        self.button_view_parts_quantity = self.create_button('Наличие товара')
        self.button_view_parts_quantity.clicked.connect(self.view_parts_quantity)
        layout.addWidget(self.button_view_parts_quantity, 2, 1)

        self.button_back = self.create_button('Назад')
        self.button_back.clicked.connect(self.back)
        layout.addWidget(self.button_back, 3, 0, 1, 2)

        self.central_widget.setLayout(layout)

    def set_background(self, image_path):
        palette = QPalette()
        pixmap = QPixmap(image_path)
        palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
        self.setPalette(palette)

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

    def view_orders(self):
        self.orders_window = OrdersWindow()
        self.orders_window.show()

    def view_order_status(self):
        self.order_status_window = OrderStatusWindow()
        self.order_status_window.show()

    def view_parts_quantity(self):
        parts_quantity = fetch_all("SELECT part_name, quantity_in_stock FROM parts")
        self.parts_quantity_window = PartsQuantityWindow(parts_quantity)
        self.parts_quantity_window.show()

    def back(self):
        from gui.login_window import LoginWindow  # Отложенный импорт для избежания циклического импорта
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()


class ManagePartsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Управление запчастями')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.set_background("img/backfon1.jpg")

        layout = QVBoxLayout()

        self.label_title = QLabel('Управление запчастями')
        self.label_title.setFont(QFont('Arial', 20))
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setStyleSheet("color: brown;")
        layout.addWidget(self.label_title)

        self.table = QTableWidget()
        self.table.setStyleSheet("background: transparent;")
        layout.addWidget(self.table)

        self.button_add = self.create_button('Добавить запчасть')
        self.button_add.clicked.connect(self.open_add_part_dialog)
        layout.addWidget(self.button_add)

        self.button_delete = self.create_button('Удалить запчасть')
        self.button_delete.clicked.connect(self.delete_part)
        layout.addWidget(self.button_delete)

        self.button_back = self.create_button('Назад')
        self.button_back.clicked.connect(self.back)
        layout.addWidget(self.button_back)

        self.central_widget.setLayout(layout)
        self.load_parts()

    def set_background(self, image_path):
        palette = QPalette()
        pixmap = QPixmap(image_path)
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
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ['ID', 'Название', 'Производитель', 'Модель', 'Цена', 'Количество на складе'])
        self.table.verticalHeader().setVisible(False)

        for row_index, row_data in enumerate(parts):
            for col_index, col_data in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

    def open_add_part_dialog(self):
        dialog = AddPartDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                part_name, manufacturer, model, price, quantity = dialog.get_part_details()
                execute_query(
                    "INSERT INTO parts (part_name, manufacturer, car_model, price, quantity_in_stock) VALUES (?, ?, ?, ?, ?)",
                    (part_name, manufacturer, model, price, quantity))
                self.load_parts()
            except sqlite3.Error as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось добавить запчасть: {e}')

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


class AddPartDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Добавить запчасть')

        layout = QFormLayout()

        self.part_name_input = QLineEdit()
        self.manufacturer_input = QLineEdit()
        self.model_input = QLineEdit()
        self.price_input = QLineEdit()
        self.quantity_input = QLineEdit()

        layout.addRow('Название:', self.part_name_input)
        layout.addRow('Производитель:', self.manufacturer_input)
        layout.addRow('Модель:', self.model_input)
        layout.addRow('Цена:', self.price_input)
        layout.addRow('Количество:', self.quantity_input)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def get_part_details(self):
        return (self.part_name_input.text(), self.manufacturer_input.text(), self.model_input.text(),
                self.price_input.text(), self.quantity_input.text())


class OrdersWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Заказы')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.set_background("img/backfon1.jpg")

        layout = QVBoxLayout()

        self.label_title = QLabel('Поиск заказов')
        self.label_title.setFont(QFont('Arial', 20))
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setStyleSheet("color: brown;")
        layout.addWidget(self.label_title)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Введите имя клиента или номер заказа')
        layout.addWidget(self.search_input)

        self.search_button = self.create_button('Поиск')
        self.search_button.clicked.connect(self.search_orders)
        layout.addWidget(self.search_button)

        self.table = QTableWidget()
        self.table.setStyleSheet("background: transparent;")
        layout.addWidget(self.table)

        self.button_back = self.create_button('Назад')
        self.button_back.clicked.connect(self.back)
        layout.addWidget(self.button_back)

        self.central_widget.setLayout(layout)

    def set_background(self, image_path):
        palette = QPalette()
        pixmap = QPixmap(image_path)
        palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
        self.setPalette(palette)

    def create_button(self, text):
        button = QPushButton(text)
        button.setFont(QFont('Arial', 14))
        button.setStyleSheet(
            "background-color: #9370DB; color: white; border-radius: 15px; padding: 10px;"
        )
        return button

    def search_orders(self):
        search_term = self.search_input.text()
        query = f"""
            SELECT orders.order_id, customers.first_name || ' ' || customers.last_name AS name, orders.order_date, orders.order_status
            FROM orders
            JOIN customers ON orders.customer_id = customers.customer_id
            WHERE customers.first_name LIKE ? OR customers.last_name LIKE ? OR orders.order_id LIKE ?
        """
        search_term = f"%{search_term}%"
        try:
            orders = fetch_all(query, (search_term, search_term, search_term))
            self.table.setRowCount(len(orders))
            self.table.setColumnCount(4)
            self.table.setHorizontalHeaderLabels(['ID', 'Имя клиента', 'Дата заказа', 'Статус'])
            self.table.verticalHeader().setVisible(False)

            for row_index, row_data in enumerate(orders):
                for col_index, col_data in enumerate(row_data):
                    self.table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

            self.table.cellDoubleClicked.connect(self.view_order_details)
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")

        # Вывод структуры таблицы customers для отладки
        customer_info = get_table_info("customers")
        print("Customers table info:", customer_info)

    def view_order_details(self, row, column):
        order_id = self.table.item(row, 0).text()
        self.order_details_window = OrderDetailsWindow(order_id)
        self.order_details_window.show()

    def back(self):
        self.close()


class OrderDetailsWindow(QMainWindow):
    def __init__(self, order_id):
        super().__init__()
        self.setWindowTitle(f'Детали заказа {order_id}')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.set_background("img/backfon1.jpg")

        layout = QVBoxLayout()

        self.label_title = QLabel(f'Детали заказа {order_id}')
        self.label_title.setFont(QFont('Arial', 20))
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setStyleSheet("color: brown;")
        layout.addWidget(self.label_title)

        self.table = QTableWidget()
        self.table.setStyleSheet("background: transparent;")
        layout.addWidget(self.table)

        self.button_back = self.create_button('Назад')
        self.button_back.clicked.connect(self.back)
        layout.addWidget(self.button_back)

        self.central_widget.setLayout(layout)
        self.load_order_details(order_id)

    def set_background(self, image_path):
        palette = QPalette()
        pixmap = QPixmap(image_path)
        palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
        self.setPalette(palette)

    def create_button(self, text):
        button = QPushButton(text)
        button.setFont(QFont('Arial', 14))
        button.setStyleSheet(
            "background-color: #9370DB; color: white; border-radius: 15px; padding: 10px;"
        )
        return button

    def load_order_details(self, order_id):
        query = """
            SELECT parts.part_name, parts.manufacturer, order_details.quantity, parts.price
            FROM order_details
            JOIN parts ON order_details.part_id = parts.part_id
            WHERE order_details.order_id = ?
        """
        order_details = fetch_all(query, (order_id,))
        self.table.setRowCount(len(order_details))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Название запчасти', 'Производитель', 'Количество', 'Цена'])
        self.table.verticalHeader().setVisible(False)

        for row_index, row_data in enumerate(order_details):
            for col_index, col_data in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

    def back(self):
        self.close()


class OrderStatusWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Статус заказа')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.set_background("img/backfon1.jpg")

        layout = QVBoxLayout()

        self.label_title = QLabel('Статус заказа')
        self.label_title.setFont(QFont('Arial', 20))
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setStyleSheet("color: brown;")
        layout.addWidget(self.label_title)

        self.table = QTableWidget()
        self.table.setStyleSheet("background: transparent;")
        layout.addWidget(self.table)

        self.button_back = self.create_button('Назад')
        self.button_back.clicked.connect(self.back)
        layout.addWidget(self.button_back)

        self.central_widget.setLayout(layout)
        self.load_order_status()

    def set_background(self, image_path):
        palette = QPalette()
        pixmap = QPixmap(image_path)
        palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
        self.setPalette(palette)

    def create_button(self, text):
        button = QPushButton(text)
        button.setFont(QFont('Arial', 14))
        button.setStyleSheet(
            "background-color: #9370DB; color: white; border-radius: 15px; padding: 10px;"
        )
        return button

    def load_order_status(self):
        orders = fetch_all("SELECT * FROM orders")
        self.table.setRowCount(len(orders))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['ID', 'Customer ID', 'Order Date', 'Status'])
        self.table.verticalHeader().setVisible(False)

        for row_index, row_data in enumerate(orders):
            for col_index, col_data in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

    def back(self):
        self.close()


class PartsQuantityWindow(QMainWindow):
    def __init__(self, parts_quantity):
        super().__init__()
        self.setWindowTitle('Наличие товара')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.set_background("img/backfon1.jpg")

        layout = QVBoxLayout()

        self.label_title = QLabel('Наличие товара')
        self.label_title.setFont(QFont('Arial', 20))
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setStyleSheet("color: brown;")
        layout.addWidget(self.label_title)

        self.table = QTableWidget()
        self.table.setStyleSheet("background: transparent;")
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Название запчасти', 'Количество на складе'])
        self.table.setRowCount(len(parts_quantity))

        for row_index, row_data in enumerate(parts_quantity):
            for col_index, col_data in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

        layout.addWidget(self.table)

        self.button_back = self.create_button('Назад')
        self.button_back.clicked.connect(self.back)
        layout.addWidget(self.button_back)

        self.central_widget.setLayout(layout)

    def set_background(self, image_path):
        palette = QPalette()
        pixmap = QPixmap(image_path)
        palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
        self.setPalette(palette)

    def create_button(self, text):
        button = QPushButton(text)
        button.setFont(QFont('Arial', 14))
        button.setStyleSheet(
            "background-color: #9370DB; color: white; border-radius: 15px; padding: 10px;"
        )
        return button

    def back(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EmployeeWindow()
    window.show()
    sys.exit(app.exec())
