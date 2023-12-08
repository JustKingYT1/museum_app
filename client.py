from src.client.main_widgets.main_window import MainWindow
from PySide6.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    root = MainWindow()
    app.exec()