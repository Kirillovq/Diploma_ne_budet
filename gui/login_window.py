import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QMessageBox
)
from PyQt6.QtGui import QFont, QPixmap, QPalette, QBrush
from PyQt6.QtCore import Qt
from gui.admin_window import AdminWindow
from gui.user_window import UserWindow
from gui.employee_window import EmployeeWindow
from utils.db_utils import fetch_one

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Авторизация - Авто запчасть трейд')
        self.setGeometry(100, 100, 400, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Устанавливаем фон
        self.set_background()

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.label_company = QLabel('Авто запчасть трейд')
        self.label_company.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        self.label_company.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_company.setStyleSheet("color: brown;")
        layout.addWidget(self.label_company)

        self.label_title = QLabel('Вход в систему')
        self.label_title.setFont(QFont('Arial', 20))
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setStyleSheet("color: brown;")
        layout.addWidget(self.label_title)

        self.input_login = QLineEdit()
        self.input_login.setPlaceholderText('Логин')
        self.input_login.setFont(QFont('Arial', 14))
        self.input_login.setStyleSheet(
            "background-color: #FFFFFF; padding: 10px; border-radius: 15px;"
        )
        layout.addWidget(self.input_login)

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText('Пароль')
        self.input_password.setFont(QFont('Arial', 14))
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_password.setStyleSheet(
            "background-color: #FFFFFF; padding: 10px; border-radius: 15px;"
        )
        layout.addWidget(self.input_password)

        self.button_login = QPushButton('Войти')
        self.button_login.setFont(QFont('Arial', 16))
        self.button_login.setStyleSheet(
            "background-color: #9370DB; color: white; border-radius: 15px; padding: 10px;"
        )
        self.button_login.clicked.connect(self.check_credentials)
        layout.addWidget(self.button_login)

        self.central_widget.setLayout(layout)

    def set_background(self):
        palette = QPalette()
        pixmap = QPixmap("img/backfon1.jpg")  # Замените "path_to_your_image.jpg" на путь к вашему изображению
        palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
        self.setPalette(palette)

    def check_credentials(self):
        login = self.input_login.text()
        password = self.input_password.text()

        try:
            result = fetch_one("SELECT id, post_id FROM users WHERE login=? AND password=?", (login, password))
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', 'Ошибка подключения к базе данных')
            return

        if result:
            user_id, post_id = result
            if post_id == 1:
                self.admin_window = AdminWindow()
                self.admin_window.show()
            elif post_id == 2:
                self.user_window = UserWindow(user_id)
                self.user_window.show()
            elif post_id == 3:
                self.employee_window = EmployeeWindow()
                self.employee_window.show()
            self.hide()  # Скрываем окно авторизации, вместо закрытия
        else:
            QMessageBox.warning(self, 'Ошибка', 'Неверный логин или пароль')

    def back_to_login(self):
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())
