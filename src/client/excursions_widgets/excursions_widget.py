from typing import Optional
from PySide6 import QtWidgets, QtCore, QtGui
import PySide6.QtCore
import PySide6.QtGui
import PySide6.QtWidgets
from src.client.tools import get_pixmap_path, include_widgets
from src.client.excursions_widgets.excursion_item import ExcursionItem
from src.client.api.resolvers import search_excursions, get_all_excursions, get_city_per_id
import time
import threading


class ExcursionList(QtWidgets.QWidget):
    stop_flag = None
    add_excursion_signal = QtCore.Signal(int, str, str, float)
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super(ExcursionList, self).__init__(parent)
        self.parent = parent
        self.__init_ui()
        self.__setting_ui()
        self.update_excursions()

    def __init_ui(self) -> None:
        self.last_keypress_time = 0
        self.keypress_interval = 0.2
        self.main_v_layout = QtWidgets.QVBoxLayout()
        self.tools_h_layout = QtWidgets.QHBoxLayout()
        self.expedition_search_line_edit = QtWidgets.QLineEdit()
        self.search_button = QtWidgets.QPushButton()
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_v_layout = QtWidgets.QVBoxLayout()
        self.status_label = ExcursionItem(self)

    def __setting_ui(self) -> None:
        self.setLayout(self.main_v_layout)
        self.main_v_layout.setContentsMargins(0, 0, 0, 0)
        self.tools_h_layout.setContentsMargins(10, 10, 10, 0)
        self.main_v_layout.addLayout(self.tools_h_layout)
        self.main_v_layout.addWidget(self.scroll_area)
        self.tools_h_layout.addWidget(self.expedition_search_line_edit)
        self.tools_h_layout.addWidget(self.search_button)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_widget.setLayout(self.scroll_v_layout)
        self.scroll_area.setWidgetResizable(True)

        self.scroll_area.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.scroll_area.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)

        self.scroll_v_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        self.scroll_v_layout.addWidget(self.status_label)

        self.status_label.set_excursion_info(id='ID', city='City', name='Name', cost='Cost')

        self.search_button.setIcon(QtGui.QPixmap(get_pixmap_path('search.png')))
        self.search_button.setFixedSize(24, 24)

        self.search_button.clicked.connect(self.on_find_button_click)
        self.add_excursion_signal.connect(self.add_excursion_slot)

    def on_find_button_click(self) -> None:
        excursions = search_excursions(name=self.expedition_search_line_edit.text())
        self.update_excursions(excursions=excursions)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        current_time = time.time()
        if event.key() == QtCore.Qt.Key.Key_Return and ((current_time - self.last_keypress_time) >= self.keypress_interval):
            self.last_keypress_time = current_time
            self.on_find_button_click()
    
    def update_excursions(self, excursions=get_all_excursions()['result']) -> None:
        self.clear_excursions()
        if excursions:
            threading.Thread(target=self.load_excursions, args=(excursions,)).start()

    def load_excursions(self, excursions) -> None:
        for excursion in excursions['result']:
            if self.stop_flag:
                exit()

            self.add_excursion_signal.emit(
                excursion['id'],
                get_city_per_id(excursion['city'])['result']['name'],
                excursion['name'],
                excursion['cost']
            )
        
    def add_excursion(self, id: int, city: str, name: str, cost: float) -> None:
        new_excursion = ExcursionItem(self)
        self.scroll_widget.__dict__.update({id: new_excursion})
        new_excursion.set_excursion_info(id=str(id), city=str(city), name=str(name), cost=str(cost))
        self.scroll_v_layout.addWidget(new_excursion)

    def clear_excursions(self) -> None:
        for excursion in dict(self.scroll_widget.__dict__):
            if type(self.scroll_widget.__dict__[excursion]) == ExcursionItem:
                self.scroll_widget.__dict__[excursion].close()
                self.scroll_widget.__dict__.pop(excursion)
    
    QtCore.Slot(int, str, str, float)
    def add_excursion_slot(self, id, city, name, cost) -> None:
        self.add_excursion(id=id, city=city, name=name, cost=cost)
        include_widgets(self.parent.session.user.power_level, elements=self.__dict__)
