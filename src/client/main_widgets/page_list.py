from typing import Optional
from PySide6 import QtWidgets, QtGui, QtCore
import PySide6.QtCore
import PySide6.QtWidgets
from src.client.main_widgets.menu_item import MenuItem


class PageList(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super(PageList, self).__init__(parent)
        self.__init_ui()
        self.__setting_ui()

    def __init_ui(self) -> None:
        self.main_h_layout = QtWidgets.QHBoxLayout()
        self.excursion_item = MenuItem(self, -1)

    def __setting_ui(self) -> None:
        self.setLayout(self.main_h_layout)
        self.setMaximumWidth(140)

        self.main_h_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.main_h_layout.setContentsMargins(5, 5, 5, 5)

        self.opened_widget = self.excursion_item

        self.excursion_item.setup(icon_name='excursions', title='Excursions')

        self.main_h_layout.addWidget(self.excursion_item)