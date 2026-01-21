import sys
from PySide6.QtWidgets import QApplication
from view.main.main_window_view import MainWindow


class Main:
    def __init__(self, open_path=""):
        super().__init__()
        self.main_window = MainWindow(open_path)

    def start(self):
        self.main_window.set_defaults()
        self.main_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    if len(sys.argv) > 1:
        start_path = sys.argv[1]
    else:
        start_path = ""

    main = Main(start_path)
    main.start()
    app.exec()
