from PySide6 import QtWidgets, QtGui, QtCore
import PySide6.QtCore
import PySide6.QtGui
from src.client.tools import get_pixmap_path
from typing import Callable


class MenuItem(QtWidgets.QFrame):
    connection_def = None
    widget: QtWidgets.QWidget = None

    def __init__(self, parent, power_level) -> None:
        super(MenuItem, self).__init__(parent)
        self.setProperty('power_level', power_level)
        self.__init_ui()
        self.__setting_ui()
    
    def __init_ui(self) -> None:
        self.main_h_layout = QtWidgets.QHBoxLayout()
        self.container_widget = QtWidgets.QWidget()
        self.container_layout = QtWidgets.QHBoxLayout()
        
        self.icon = QtWidgets.QLabel()
        self.title = QtWidgets.QLabel()

    def __setting_ui(self) -> None:
        self.setLayout(self.main_h_layout)

        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Maximum)

        self.title.setStyleSheet('color: black')

        self.main_h_layout.addWidget(self.container_widget)
        self.container_widget.setLayout(self.container_layout)
        
        self.container_layout.addWidget(self.icon)
        self.container_layout.addWidget(self.title)

        self.icon.setFixedSize(32, 32)

    def setup(self, icon_name: str, title: str) -> None:
        self.set_icon(icon_name)
        self.set_title(title)

    def set_icon(self, icon_name: str) -> None:
        self.icon.setPixmap(QtGui.QPixmap(get_pixmap_path(pixmap=icon_name)))
    
    def set_title(self, title: str) -> None:
        self.title.setText(title)
    
    def bind_widget(self, widget: QtWidgets.QWidget) -> None:
        self.widget = widget

    def connect_func(self, func: Callable) -> None:
        self.connection_def = func
    
    def on_mouse_enter(self) -> None:
        self.setStyleSheet('QFrame{background-color: darkgray; border-radius: 15px}')
        self.title.setStyleSheet('color: white')

    def on_mouse_leave(self) -> None:
        self.setStyleSheet('QFrame{background-color: none; border-radius: 15px}')
        self.title.setStyleSheet('color: black')

    def on_mouse_clicked(self) -> None:
        self.switch_page()
        if self.connection_def:
            self.connection_def()

    def enterEvent(self, event: QtGui.QEnterEvent) -> None:
        self.on_mouse_enter()

    def leaveEvent(self, event: QtCore.QEvent) -> None:
        self.on_mouse_leave()

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        self.on_mouse_clicked()

    def switch_page(self) -> None:
        for item in self.parent().__dict__:
            page: MenuItem = self.parent().__dict__[item]
            if type(page) == MenuItem:
                page.widget.show() if page == self else page.widget.hide()

    
    
