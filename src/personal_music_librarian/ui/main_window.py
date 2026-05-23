from PySide6.QtWidgets import QMainWindow

from personal_music_librarian.ui.pages.library_page import LibraryPage


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Personal Music Librarian")
        self.resize(1400, 900)

        self.library_page = LibraryPage()

        self.setCentralWidget(self.library_page)
