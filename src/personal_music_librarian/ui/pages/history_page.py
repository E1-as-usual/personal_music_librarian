from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QTableView
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from personal_music_librarian.core.database.db import Database
from personal_music_librarian.core.database.repositories.log_repo import LogRepository
from personal_music_librarian.core.services.undo_service import UndoService
from personal_music_librarian.ui.models.history_table_model import HistoryTableModel


class HistoryPage(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.database = Database()
        self.database.initialize()
        self.undo_service = UndoService(self.database)
        self.model = HistoryTableModel()

        self.refresh_button = QPushButton("Refresh History")
        self.refresh_button.clicked.connect(self.load_history)

        self.undo_button = QPushButton("Undo Last Operation")
        self.undo_button.clicked.connect(self.undo_last_operation)

        self.summary_label = QLabel("No history loaded")

        toolbar = QHBoxLayout()
        toolbar.addWidget(self.refresh_button)
        toolbar.addWidget(self.undo_button)
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

    def undo_last_operation(self) -> None:
        confirmation = QMessageBox.question(
            self,
            "Undo Last Operation",
            "Attempt to undo the latest reversible operation?",
        )

        if confirmation != QMessageBox.StandardButton.Yes:
            return

        result = self.undo_service.undo_last_operation()

        QMessageBox.information(
            self,
            "Undo Result",
            result['message'],
        )

        self.load_history()
