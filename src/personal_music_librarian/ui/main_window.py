from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Personal Music Librarian")
        self.resize(1400, 900)

        self.setCentralWidget(
            QLabel("Personal Music Librarian v0.1")
        )
