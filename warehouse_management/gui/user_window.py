from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget, QTableWidget, QTableWidgetItem, \
    QLineEdit, QMessageBox
from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtCore import Qt
from utils.db_utils import execute_query, fetch_all


class UserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Пользователь')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.central_widget.setStyleSheet("background-color: #E6E6FA;")

        layout = QVBoxLayout()

        self.label_title = QLabel('Функции пользователя')
        self.label_title.setFont(QFont('Arial', 20))
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_title)

        self.button_view_parts = self.create_button('Просмотр запчастей')
        self.button_view_parts.clicked.connect(self.view_parts)
        layout.addWidget(self.button_view_parts)

        self.button_create_order = self.create_button('Создать заказ')
        self.button_create_order.clicked.connect(self.create_order)
        layout.addWidget(self.button_create_order)

        self.button_view_orders = self.create_button('Просмотр заказов')
        self.button_view_orders.clicked.connect(self.view_orders)
        layout.addWidget(self.button_view_orders)

        self.button_update_user = self.create_button('Обновление данных о пользователе')
        self.button_update_user.clicked.connect(self.update_user)
        layout.addWidget(self.button_update_user)

        self.button_view_customers = self.create_button('Просмотр информации о клиентах')
        self.button_view_customers.clicked.connect(self.view_customers)
        layout.addWidget(self.button_view_customers)

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

    def view_parts(self):
        parts = fetch_all("SELECT * FROM parts")
        self.parts_window = PartsWindow(parts)
        self.parts_window.show()

    def create_order(self):
        self.new_order_window = NewOrderWindow()
        self.new_order_window.show()

    def view_orders(self):
        orders = fetch_all("SELECT * FROM orders")
        self.orders_window = OrdersWindow(orders)
        self.orders_window.show()

    def update_user(self):
        self.update_user_window = UpdateUserWindow()
        self.update_user_window.show()

    def view_customers(self):
        customers = fetch_all("SELECT * FROM customers")
        self.customers_window = CustomersWindow(customers)
        self.customers_window.show()

    def back(self):
        self.close()


class PartsWindow(QMainWindow):
    def __init__(self, parts):
        super().__init__()
        self.setWindowTitle('Просмотр запчастей')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.central_widget.setStyleSheet("background-color: #E6E6FA;")

        layout = QVBoxLayout()

        self.label_title = QLabel('Запчасти')
        self.label_title.setFont(QFont('Arial', 20))
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_title)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ['ID', 'Название', 'Производитель', 'Модель', 'Цена', 'Количество на складе'])
        self.table.setRowCount(len(parts))

        for row_index, row_data in enumerate(parts):
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


class NewOrderWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Создать заказ')
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.central_widget.setStyleSheet("background-color: #E6E6FA;")

        layout = QVBoxLayout()

        self.label_customer_id = QLabel('ID клиента:')
        layout.addWidget(self.label_customer_id)

        self.input_customer_id = QLineEdit()
        layout.addWidget(self.input_customer_id)

        self.label_part_id = QLabel('ID запчасти:')
        layout.addWidget(self.label_part_id)

        self.input_part_id = QLineEdit()
        layout.addWidget(self.input_part_id)

        self.label_quantity = QLabel('Количество:')
        layout.addWidget(self.label_quantity)

        self.input_quantity = QLineEdit()
        layout.addWidget(self.input_quantity)

        self.button_create = QPushButton('Создать')
        self.button_create.setStyleSheet(
            "background-color: #9370DB; color: white; border-radius: 15px; padding: 10px;"
        )
        self.button_create.clicked.connect(self.create_order_in_db)
        layout.addWidget(self.button_create)

        self.button_back = QPushButton('Назад')
        self.button_back.setStyleSheet(
            "background-color: #9370DB; color: white; border-radius: 15px; padding: 10px;"
        )
        self.button_back.clicked.connect(self.back)
        layout.addWidget(self.button_back)

        self.central_widget.setLayout(layout)

    def create_order_in_db(self):
        customer_id = self.input_customer_id.text()
        part_id = self.input_part_id.text()
        quantity = self.input_quantity.text()

        execute_query(
            "INSERT INTO orders (customer_id, order_date, order_status) VALUES (?, date('now'), 'В обработке')",
            (customer_id,))
        order_id = fetch_one("SELECT last_insert_rowid()")[0]
        execute_query("INSERT INTO order_details (order_id, part_id, quantity) VALUES (?, ?, ?)",
                      (order_id, part_id, quantity))
        QMessageBox.information(self, 'Успех', 'Заказ создан')
        self.close()

    def back(self):
        self.close()


class OrdersWindow(QMainWindow):
    def __init__(self, orders):
        super().__init__()
        self.setWindowTitle('Просмотр заказов')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.central_widget.setStyleSheet("background-color: #E6E6FA;")

        layout = QVBoxLayout()

        self.label_title = QLabel('Заказы')
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


class UpdateUserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Обновление данных о пользователе')
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.central_widget.setStyleSheet("background-color: #E6E6FA;")

        layout = QVBoxLayout()

        self.label_login = QLabel('Новый логин:')
        layout.addWidget(self.label_login)

        self.input_login = QLineEdit()
        layout.addWidget(self.input_login)

        self.label_password = QLabel('Новый пароль:')
        layout.addWidget(self.label_password)

        self.input_password = QLineEdit()
        layout.addWidget(self.input_password)

        self.button_update = QPushButton('Обновить')
        self.button_update.setStyleSheet(
            "background-color: #9370DB; color: white; border-radius: 15px; padding: 10px;"
        )
        self.button_update.clicked.connect(self.update_user_in_db)
        layout.addWidget(self.button_update)

        self.button_back = QPushButton('Назад')
        self.button_back.setStyleSheet(
            "background-color: #9370DB; color: white; border-radius: 15px; padding: 10px;"
        )
        self.button_back.clicked.connect(self.back)
        layout.addWidget(self.button_back)

        self.central_widget.setLayout(layout)

    def update_user_in_db(self):
        login = self.input_login.text()
        password = self.input_password.text()

        # Тут необходимо указать текущего пользователя для обновления данных
        current_user_id = 2  # Пример: ID текущего пользователя

        execute_query("UPDATE users SET login=?, password=? WHERE id=?", (login, password, current_user_id))
        QMessageBox.information(self, 'Успех', 'Данные пользователя обновлены')
        self.close()

    def back(self):
        self.close()


class CustomersWindow(QMainWindow):
    def __init__(self, customers):
        super().__init__()
        self.setWindowTitle('Просмотр информации о клиентах')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.central_widget.setStyleSheet("background-color: #E6E6FA;")

        layout = QVBoxLayout()

        self.label_title = QLabel('Клиенты')
        self.label_title.setFont(QFont('Arial', 20))
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_title)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['ID', 'Имя', 'Фамилия', 'Адрес', 'Телефон', 'Email'])
        self.table.setRowCount(len(customers))

        for row_index, row_data in enumerate(customers):
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
