from PySide6.QtWidgets import QApplication

from personal_music_librarian.ui.main_window import MainWindow


def run() -> None:
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
