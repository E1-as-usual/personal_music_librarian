from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QStackedWidget
from PySide6.QtWidgets import QToolBar

from personal_music_librarian.ui.pages.duplicates_page import DuplicatesPage
from personal_music_librarian.ui.pages.library_page import LibraryPage


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Personal Music Librarian")
        self.resize(1400, 900)

        self.library_page = LibraryPage()
        self.duplicates_page = DuplicatesPage()

        self.stack = QStackedWidget()
        self.stack.addWidget(self.library_page)
        self.stack.addWidget(self.duplicates_page)

        toolbar = QToolBar("Navigation")
        self.addToolBar(toolbar)

        library_action = toolbar.addAction("Library")
        library_action.triggered.connect(
            lambda: self.stack.setCurrentWidget(self.library_page)
        )

        duplicates_action = toolbar.addAction("Duplicates")
        duplicates_action.triggered.connect(
            lambda: self.stack.setCurrentWidget(self.duplicates_page)
        )

        self.setCentralWidget(self.stack)
