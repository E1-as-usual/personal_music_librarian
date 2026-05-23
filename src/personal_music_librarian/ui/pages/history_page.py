from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QTableView
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from personal_music_librarian.core.database.db import Database
from personal_music_librarian.core.database.repositories.log_repo import LogRepository
from personal_music_librarian.ui.models.history_table_model import HistoryTableModel


class HistoryPage(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.database = Database()
        self.database.initialize()
        self.model = HistoryTableModel()

        self.refresh_button = QPushButton("Refresh History")
        self.refresh_button.clicked.connect(self.load_history)

        self.summary_label = QLabel("No history loaded")

        toolbar = QHBoxLayout()
        toolbar.addWidget(self.refresh_button)
        toolbar.addWidget(self.summary_label)
        toolbar.addStretch(1)

        self.table = QTableView()
        self.table.setModel(self.model)

        layout = QVBoxLayout(self)
        layout.addLayout(toolbar)
        layout.addWidget(self.table)

        self.load_history()

    def load_history(self) -> None:
        with self.database.connection() as connection:
            rows = LogRepository(connection).recent(limit=500)

        self.model.set_rows(rows)
        self.summary_label.setText(f"{len(rows)} operations")
