from PySide6 import QtWidgets
import settings


def get_pixmap_path(pixmap: str) -> str:
    return f'{settings.IMAGE_DIR}/{pixmap}'

def include_widgets(power_level: int,  elements: dict[str, QtWidgets.QWidget], count: int = 0) -> None:
    for key, item in elements.items():
        if not issubclass(type(item), QtWidgets.QWidget) or issubclass(type(item), QtWidgets.QMainWindow):
            count += 1
            continue

        if item.property('power_level') is not None:
            item.show() if power_level >= item.property('power_level') else item.hide()
        if count < 50:
            include_widgets(power_level=power_level, elements=item.__dict__, count=count)
