from PySide6 import QtWidgets, QtCore, QtGui


class UserProfile(QtWidgets.QWidget):
    def __init__(self, parent) -> None:
        super(UserProfile, self).__init__(parent)
        self.parent = parent
        self.__init_ui()
        self.__setting_ui()

    def __init_ui(self) -> None:
        self.main_h_layout = QtWidgets.QVBoxLayout()
        self.id_h_layout = QtWidgets.QHBoxLayout()
        self.power_level_h_layout = QtWidgets.QHBoxLayout()
        self.login_h_layout = QtWidgets.QHBoxLayout()
        self.password_h_layout = QtWidgets.QHBoxLayout()
        self.confirm_h_layout = QtWidgets.QHBoxLayout()
        self.buttons_h_layout = QtWidgets.QHBoxLayout()

        self.id_label = QtWidgets.QLabel(text='ID:')
        self.power_level_label = QtWidgets.QLabel(text='Power level:')
        self.login_label = QtWidgets.QLabel(text='Login:')
        self.password_label = QtWidgets.QLabel(text='Password:')
        self.confirm_password_label = QtWidgets.QLabel(text='Confirm:')

        self.spacer = QtWidgets.QSpacerItem(0, 10)

        self.id_line_edit = QtWidgets.QLineEdit()
        self.power_level_line_edit = QtWidgets.QLineEdit()
        self.login_line_edit = QtWidgets.QLineEdit()
        self.password_line_edit = QtWidgets.QLineEdit()
        self.confirm_password_line_edit = QtWidgets.QLineEdit()

        self.allow_button = QtWidgets.QPushButton(text='Allow')
        self.edit_button = QtWidgets.QPushButton(text='Edit')
        self.leave_button = QtWidgets.QPushButton(text='Leave')
        self.delete_button = QtWidgets.QPushButton(text='Delete')

    def __setting_ui(self) -> None:
        self.setLayout(self.main_h_layout)
        self.setContentsMargins(0, 0, 0, 0)
        self.main_h_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.setMaximumWidth(250)

        self.main_h_layout.addLayout(self.id_h_layout)
        self.main_h_layout.addLayout(self.power_level_h_layout)
        self.main_h_layout.addSpacerItem(self.spacer)
        self.main_h_layout.addLayout(self.login_h_layout)
        self.main_h_layout.addLayout(self.password_h_layout)
        self.main_h_layout.addLayout(self.confirm_h_layout)
        self.main_h_layout.addSpacerItem(self.spacer)
        self.main_h_layout.addLayout(self.buttons_h_layout)

        self.id_h_layout.addWidget(self.id_label)
        self.power_level_h_layout.addWidget(self.power_level_label)
        self.login_h_layout.addWidget(self.login_label)
        self.password_h_layout.addWidget(self.password_label)
        self.confirm_h_layout.addWidget(self.confirm_password_label)
        
        self.id_h_layout.addWidget(self.id_line_edit)
        self.power_level_h_layout.addWidget(self.power_level_line_edit)
        self.login_h_layout.addWidget(self.login_line_edit)
        self.password_h_layout.addWidget(self.password_line_edit)
        self.confirm_h_layout.addWidget(self.confirm_password_line_edit)

        self.buttons_h_layout.addWidget(self.delete_button)
        self.buttons_h_layout.addWidget(self.leave_button)
        self.buttons_h_layout.addWidget(self.edit_button)
        self.buttons_h_layout.addWidget(self.allow_button)

        self.id_line_edit.setFixedWidth(150)
        self.power_level_line_edit.setFixedWidth(150)
        self.login_line_edit.setFixedWidth(150)
        self.password_line_edit.setFixedWidth(150)
        self.confirm_password_line_edit.setFixedWidth(150)
        
        [line_edit.setEnabled(False) for line_edit in (self.id_line_edit, self.power_level_line_edit, self.login_line_edit, self.password_line_edit, self.confirm_password_line_edit)]

        self.password_line_edit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.confirm_password_line_edit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.allow_button.setEnabled(False)

        self.allow_button.clicked.connect(slot=self.on_allow_button_clicked)
        self.edit_button.clicked.connect(slot=self.on_edit_button_clicked)
        self.leave_button.clicked.connect(slot=self.on_leave_button_clicked)
        self.delete_button.clicked.connect(slot=self.on_delete_button_click)

    def fill_line_edits(self) -> None:
        self.id_line_edit.setText(str(self.parent.session.user.userID))
        self.power_level_line_edit.setText(str(self.parent.session.user.power_level))
        self.login_line_edit.setText(self.parent.session.user.login)
    
    def delete_my_account(self) -> None:
        if QtWidgets.QMessageBox.question(self, 'Info', 'Are you sure?') != QtWidgets.QMessageBox.StandardButton.Yes:
            return
        self.parent.session.delete()
        self.parent.leave()
        self.parent.show_message(text='Succesfully delete account', parent=self)
    
    def on_delete_button_click(self) -> None:
        self.delete_my_account()

    def data_is_valid(self) -> bool:
        if self.password_line_edit.text() != self.confirm_password_line_edit.text():
            self.parent.show_message(text="Incorrect confirm password", error=True, parent=self)
            return False
        
        for x in (self.password_line_edit, self.confirm_password_line_edit):
            if x.text() == "":
                self.parent.show_message(text="One or more fields are empty", error=True, parent=self)
                return False
            
        return True
    
    def on_edit_button_clicked(self) -> None:
        self.parent
        self.switch_on_or_off_line_edits(True)
        self.allow_button.setEnabled(True)
        self.edit_button.setEnabled(False)

    def on_allow_button_clicked(self) -> None:
        if not self.data_is_valid():
            return
        
        self.parent.session.update(login=self.login_line_edit.text(), password=self.password_line_edit.text())

        if self.parent.session.error:
            self.parent.show_message(text=self.parent.session.error, error=True, parent=self)
        else:
            self.parent.show_message(text='Successfully', parent=self)

        self.edit_button.setEnabled(True)
        self.allow_button.setEnabled(False)

        self.password_line_edit.setText('')
        self.confirm_password_line_edit.setText('')

        self.switch_on_or_off_line_edits(False)

    def on_leave_button_clicked(self) -> None:
        self.parent.leave()

    def switch_on_or_off_line_edits(self, param: bool) -> None:
        self.password_line_edit.setEnabled(param)
        self.confirm_password_line_edit.setEnabled(param)
    
