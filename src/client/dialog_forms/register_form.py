from typing import Optional
from PySide6 import QtWidgets, QtCore, QtGui
import PySide6.QtGui
import PySide6.QtWidgets


class RegisterWindow(QtWidgets.QDialog):
    def __init__(self, parent) -> None:
        super().__init__(parent=parent)
        self.__init_ui()
        self.__setting_ui()
        self.show()

    
    def __init_ui(self) -> None:
        self.main_v_layout = QtWidgets.QVBoxLayout()
        self.label_line_edit_h_layout = QtWidgets.QHBoxLayout()
        self.label_v_layout = QtWidgets.QVBoxLayout()
        self.line_edit_v_layout = QtWidgets.QVBoxLayout()

        self.label_login = QtWidgets.QLabel()
        self.label_password = QtWidgets.QLabel()
        self.label_confirm = QtWidgets.QLabel()
        self.label_type_id = QtWidgets.QLabel()

        self.spacer = QtWidgets.QSpacerItem(0, 10)

        self.line_edit_login = QtWidgets.QLineEdit()
        self.line_edit_password = QtWidgets.QLineEdit()
        self.line_edit_confirm = QtWidgets.QLineEdit()
        self.line_edit_type_id = QtWidgets.QLineEdit()

        self.register_button = QtWidgets.QPushButton()

    
    def __setting_ui(self) -> None:
        self.setWindowTitle("Sign up")

        self.setLayout(self.main_v_layout)
        self.main_v_layout.addLayout(self.label_line_edit_h_layout)
        self.label_line_edit_h_layout.addLayout(self.label_v_layout)
        self.label_line_edit_h_layout.addLayout(self.line_edit_v_layout)

        self.label_v_layout.addWidget(self.label_type_id)
        self.label_v_layout.addSpacerItem(self.spacer)
        self.label_v_layout.addWidget(self.label_login)
        self.label_v_layout.addWidget(self.label_password)
        self.label_v_layout.addWidget(self.label_confirm)

        self.line_edit_v_layout.addWidget(self.line_edit_type_id)
        self.line_edit_v_layout.addSpacerItem(self.spacer)
        self.line_edit_v_layout.addWidget(self.line_edit_login)
        self.line_edit_v_layout.addWidget(self.line_edit_password)
        self.line_edit_v_layout.addWidget(self.line_edit_confirm)

        self.main_v_layout.addWidget(self.register_button)

        self.label_type_id.setText("Type ID")
        self.label_login.setText("Login")
        self.label_password.setText("Password")
        self.label_confirm.setText("Confirm password")

        self.register_button.setText("Sign up")

        self.line_edit_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.line_edit_confirm.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.register_button.clicked.connect(self.on_register_button_clicked)

    
    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == QtCore.Qt.Key.Key_Return:
            self.register()

    def data_is_valid(self) -> bool:
        if self.line_edit_password.text() != self.line_edit_confirm.text():
            self.parent().show_message(text="Incorrect confirm password", error=True, parent=self)
            return False
        
        for x in (self.line_edit_login, self.line_edit_password):
            if x.text() == "":
                self.parent().show_message(text="One or more fields are empty", error=True, parent=self)
                return False
            
        return True
    
    def on_register_button_clicked(self) -> None:
        self.register()

    def register(self) -> None:
        if not self.data_is_valid():
            return
        
        self.parent().session.register(type_id=self.line_edit_type_id.text(), login=self.line_edit_login.text(), password=self.line_edit_password.text()),

        if self.parent().session.error:
            return self.parent().show_message(
                text=self.parent().session.error,
                error=True,
                parent=self
            )

        if self.parent().session.auth:
            self.parent().show_message(
                text='Successful register',
                error=False,
                parent=self
            )
        
        self.parent().authorization_menu.open_login_dialog()
        self.close()
        