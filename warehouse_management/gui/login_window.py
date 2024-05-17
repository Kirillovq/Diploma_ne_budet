import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from gui.admin_window import AdminWindow
from gui.user_window import UserWindow
from gui.employee_window import EmployeeWindow
from utils.db_utils import fetch_one


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Авторизация')
        self.setGeometry(100, 100, 400, 250)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.label_title = QLabel('Вход в систему')
        self.label_title.setFont(QFont('Arial', 16))
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_title)

        self.label_login = QLabel('Логин:')
        layout.addWidget(self.label_login)

        self.input_login = QLineEdit()
        layout.addWidget(self.input_login)

        self.label_password = QLabel('Пароль:')
        layout.addWidget(self.label_password)

        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.input_password)

        self.button_login = QPushButton('Войти')
        self.button_login.setFont(QFont('Arial', 14))
        self.button_login.clicked.connect(self.check_credentials)
        layout.addWidget(self.button_login)

        self.central_widget.setLayout(layout)

    def check_credentials(self):
        login = self.input_login.text()
        password = self.input_password.text()

        print(f"Login: {login}, Password: {password}")  # Отладочное сообщение

        try:
            result = fetch_one("SELECT post_id FROM users WHERE login=? AND password=?", (login, password))
            print(f"DB Result: {result}")  # Отладочное сообщение
        except Exception as e:
            print(f"Database error: {e}")  # Отладочное сообщение
            QMessageBox.critical(self, 'Ошибка', 'Ошибка подключения к базе данных')
            return

        if result:
            post_id = result[0]
            print(f"User found: {post_id}")  # Отладочное сообщение
            if post_id == 1:
                self.admin_window = AdminWindow()
                self.admin_window.show()
            elif post_id == 2:
                self.user_window = UserWindow()
                self.user_window.show()
            elif post_id == 3:
                self.employee_window = EmployeeWindow()
                self.employee_window.show()
            self.hide()  # Скрываем окно авторизации, вместо закрытия
        else:
            print("Invalid credentials")  # Отладочное сообщение
            QMessageBox.warning(self, 'Ошибка', 'Неверный логин или пароль')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())
