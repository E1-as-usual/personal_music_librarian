from pathlib import Path

from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QTableView
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from personal_music_librarian.core.database.db import Database
from personal_music_librarian.core.database.repositories.track_repo import TrackRepository
from personal_music_librarian.core.services.scan_service import ScanService
from personal_music_librarian.ui.models.track_table_model import TrackTableModel


class LibraryPage(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.database = Database()
        self.database.initialize()

        self.scan_service = ScanService(self.database)
        self.model = TrackTableModel()

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search artist or album...")
        self.search_box.textChanged.connect(self.reload_tracks)

        self.scan_button = QPushButton("Scan Library")
        self.scan_button.clicked.connect(self.scan_library)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.reload_tracks)

        toolbar = QHBoxLayout()
        toolbar.addWidget(self.scan_button)
        toolbar.addWidget(self.refresh_button)
        toolbar.addWidget(self.search_box)

        self.status_label = QLabel("Ready")

        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setSortingEnabled(True)

        layout = QVBoxLayout(self)
        layout.addLayout(toolbar)
        layout.addWidget(self.table)
        layout.addWidget(self.status_label)

        self.reload_tracks()

    def scan_library(self) -> None:
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Music Library",
        )

        if not folder:
            return

        result = self.scan_service.scan_library(Path(folder))

        self.status_label.setText(
            f"Scanned {result['scanned']} tracks | Invalid: {result['invalid']}"
        )

        self.reload_tracks()

    def reload_tracks(self) -> None:
        search = self.search_box.text().strip()

        with self.database.connection() as connection:
            repo = TrackRepository(connection)

            if search:
                rows = repo.search(artist=search)
                if not rows:
                    rows = repo.search(album=search)
            else:
                rows = repo.get_all()

            self.model.set_rows(rows)
