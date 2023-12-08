from typing import Optional
from PySide6 import QtWidgets, QtCore, QtGui
import PySide6.QtCore
import PySide6.QtGui
import PySide6.QtWidgets


class LoginWindow(QtWidgets.QDialog):
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super(LoginWindow, self).__init__(parent)
        self.parent = parent
        self.__init_ui()
        self.__setting_ui()
        self.show()

    def __init_ui(self) -> None:
        self.main_h_layout = QtWidgets.QHBoxLayout()            
        self.labels_on_line_edits_h_layout = QtWidgets.QHBoxLayout()
        self.labels_v_layout = QtWidgets.QVBoxLayout()
        self.line_edits_v_layout = QtWidgets.QVBoxLayout()

        self.login = QtWidgets.QLabel(text='Login')
        self.password = QtWidgets.QLabel(text='Password')

        self.login_line_edit = QtWidgets.QLineEdit()
        self.password_line_edit = QtWidgets.QLineEdit()

        self.login_button = QtWidgets.QPushButton(text='Login')
    
    def __setting_ui(self) -> None:
        self.setLayout(self.main_h_layout)
        self.setWindowTitle('Log in')

        self.main_h_layout.addLayout(self.labels_on_line_edits_h_layout)

        self.labels_on_line_edits_h_layout.addLayout(self.labels_v_layout)
        self.labels_on_line_edits_h_layout.addLayout(self.line_edits_v_layout)

        self.labels_v_layout.addWidget(self.login)
        self.labels_v_layout.addWidget(self.password)
        
        self.line_edits_v_layout.addWidget(self.login_line_edit)
        self.line_edits_v_layout.addWidget(self.password_line_edit)

        self.main_h_layout.addWidget(self.login_button)

        self.password_line_edit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.login_button.clicked.connect(slot=self.login_button_clicked)

    def data_is_valid(self) -> bool:
        for x in (self.login_line_edit, self.password_line_edit):
            if x.text() == "":
                self.parent.show_message(text="One or more fields are empty", error=True, parent=self)
                return False
            
        return True
    
    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        self.login_button_clicked()

    def login_button_clicked(self) -> None:
        if not self.data_is_valid():
            return
        
        self.parent.session.login(log_in=self.login_line_edit.text(), password=self.password_line_edit.text())

        if self.parent.session.error:
            return self.parent.show_message(
                text=self.parent.session.error,
                error=True,
                parent=self
            )
        
        if self.parent.session.auth:
            self.parent.show_message(
                text='Successful login',
                error=False,
                parent=self
            )

        self.parent.authorization()

        self.close()