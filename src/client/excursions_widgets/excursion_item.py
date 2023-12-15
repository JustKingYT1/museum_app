from typing import Optional
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
from src.client.tools import get_pixmap_path


class ExcursionItem(QtWidgets.QWidget):
    def __init__(self, parent: QWidget) -> None:
        super(ExcursionItem, self).__init__(parent)
        self.parent = parent
        self.__init_ui()
        self.__setting_ui()
    
    def __init_ui(self) -> None:
        self.main_h_layout = QtWidgets.QHBoxLayout()
        self.id = QtWidgets.QLabel()
        self.city = QtWidgets.QLabel()
        self.name = QtWidgets.QLabel()
        self.cost = QtWidgets.QLabel()

    def __setting_ui(self) -> None:
        self.setLayout(self.main_h_layout)
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        
        self.main_h_layout.addWidget(self.id)
        self.main_h_layout.addWidget(self.city)
        self.main_h_layout.addWidget(self.name)
        self.main_h_layout.addWidget(self.cost)

        self.id.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.city.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.name.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.cost.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.id.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.city.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.name.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.cost.setFrameShape(QtWidgets.QFrame.Shape.Box)

        self.city.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.name.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.id.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.cost.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)

        self.setFixedHeight(70)

    def set_excursion_info(self, city: str, name: str, cost: str, id: str) -> None:
        self.id.setText(str(id))
        self.city.setText(str(city))
        self.name.setText(str(name))
        self.cost.setText(str(cost))
