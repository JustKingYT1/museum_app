from typing import Optional
from PySide6 import QtWidgets, QtCore, QtGui
import PySide6.QtCore
import PySide6.QtWidgets
from src.client.dialog_forms import register_form, login_form


class AuthorizationMenu(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)
        self.parent = parent
        self.__init_ui()
        self.__setting_ui()
        
    def __init_ui(self) -> None:
        self.main_h_layout = QtWidgets.QHBoxLayout()
        self.login_button = QtWidgets.QPushButton(text='Login')
        self.register_button = QtWidgets.QPushButton(text='Register')

    def __setting_ui(self) -> None:
        self.setLayout(self.main_h_layout)
        self.setMaximumWidth(120)

        self.main_h_layout.addWidget(self.login_button)
        self.main_h_layout.addWidget(self.register_button)

        self.main_h_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom)

        self.login_button.clicked.connect(slot=self.on_login_button_click)
        self.register_button.clicked.connect(slot=self.on_register_button_click)
    
    def on_register_button_click(self) -> None:
        self.open_register_dialog()

    def open_login_dialog(self) -> None:
        login_form.LoginWindow(self.parent)

    def open_register_dialog(self) -> None:
        register_form.RegisterWindow(self.parent)
    
    def on_login_button_click(self) -> None:
        self.open_login_dialog()