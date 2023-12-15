from typing import Optional
from PySide6 import QtCore, QtWidgets, QtGui
import PySide6.QtCore
import PySide6.QtWidgets
from src.client.api.session import Session 
import multiprocessing
from server import start_server
from src.client.main_widgets.page_list import PageList
from src.client.tools import include_widgets
from src.client.main_widgets.authorization_menu import AuthorizationMenu
from src.client.main_widgets.user_profile import UserProfile
from src.client.excursions_widgets.excursions_widget import ExcursionList


class MainWindow(QtWidgets.QMainWindow):

    session: Session = Session()

    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.start_server_process()
        if not self.session.server_available:
            self.show_message(text='Server is not available', error=True, parent=self)
            self.close_func()

        self.__init_ui()
        self.__setting_ui()
            
        self.show()
    
    def start_server_process(self) -> None:
        self.server_process = multiprocessing.Process(target=start_server)
        self.server_process.start()
        while self.session.server_available == False:
            self.session.check_connect()

    def __init_ui(self) -> None:
        self.central_widget = QtWidgets.QWidget(self)
        self.main_h_layout = QtWidgets.QHBoxLayout()
        self.widget_container = QtWidgets.QWidget(self)
        self.widget_container_v_layout = QtWidgets.QVBoxLayout()
        self.page_list = PageList(self)
        self.authorization_menu = AuthorizationMenu(self)
        self.user_profile = UserProfile(self)
        self.excursion_list = ExcursionList(self)

    def __setting_ui(self) -> None: 
        self.resize(930, 615)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.main_h_layout)
        self.widget_container.setLayout(self.widget_container_v_layout)
        self.main_h_layout.setContentsMargins(0, 0, 0, 0)
        self.widget_container_v_layout.setContentsMargins(0, 0, 0, 0)        
        self.widget_container_v_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

        self.main_h_layout.addWidget(self.page_list)
        self.main_h_layout.addWidget(self.widget_container)
        self.main_h_layout.addWidget(self.authorization_menu)
        self.main_h_layout.addWidget(self.user_profile)

        self.widget_container_v_layout.addWidget(self.excursion_list)
        self.page_list.excursion_item.bind_widget(self.excursion_list)

        self.user_profile.hide()

        include_widgets(power_level=self.session.user.power_level, elements=self.__dict__)

    def authorization(self) -> None:
        self.authorization_menu.hide()
        self.user_profile.show()
        self.user_profile.fill_line_edits()

        include_widgets(self.session.user.power_level, elements=self.__dict__)

    def leave(self) -> None:
        self.authorization_menu.show()
        self.user_profile.hide()
        self.session.leave()
        
        include_widgets(power_level=self.session.user.power_level, elements=self.__dict__)
        
    def show_message(self, text: str, error: bool = False, parent=None) -> None:
        message_box = QtWidgets.QMessageBox(parent=self if not parent else parent)
        message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        message_box.setWindowTitle('Error' if error else 'Information')
        message_box.setText(text)
        message_box.setIcon(QtWidgets.QMessageBox.Icon.Critical if error else QtWidgets.QMessageBox.Icon.Information)
        message_box.exec_()

    def close_func(self) -> None:
        self.expedition_stop_flag = True
        self.server_process.terminate()
        self.close()
        exit()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.close_func()