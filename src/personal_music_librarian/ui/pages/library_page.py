from pathlib import Path

from PySide6.QtCore import QThread
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QProgressBar
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QTableView
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from personal_music_librarian.core.database.db import Database
from personal_music_librarian.core.database.repositories.track_repo import TrackRepository
from personal_music_librarian.ui.models.track_table_model import TrackTableModel
from personal_music_librarian.workers.scan_worker import ScanWorker


class LibraryPage(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.database = Database()
        self.database.initialize()

        self.scan_thread: QThread | None = None
        self.scan_worker: ScanWorker | None = None
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
        self.current_file_label = QLabel("")

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)

        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setSortingEnabled(True)

        layout = QVBoxLayout(self)
        layout.addLayout(toolbar)
        layout.addWidget(self.table)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.status_label)
        layout.addWidget(self.current_file_label)

        self.reload_tracks()

    def scan_library(self) -> None:
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Music Library",
        )

        if not folder:
            return

        self.scan_button.setEnabled(False)
        self.status_label.setText("Preparing scan...")
        self.current_file_label.setText("")
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)

        self.scan_thread = QThread()
        self.scan_worker = ScanWorker(Path(folder))
        self.scan_worker.moveToThread(self.scan_thread)

        self.scan_thread.started.connect(self.scan_worker.run)
        self.scan_worker.status.connect(self.status_label.setText)
        self.scan_worker.progress.connect(self.on_scan_progress)
        self.scan_worker.finished.connect(self.on_scan_finished)
        self.scan_worker.failed.connect(self.on_scan_failed)
        self.scan_worker.finished.connect(self.scan_thread.quit)
        self.scan_worker.failed.connect(self.scan_thread.quit)
        self.scan_thread.finished.connect(self.cleanup_scan_thread)

        self.scan_thread.start()

    def on_scan_progress(self, done: int, total: int, path: str) -> None:
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(done)
        self.status_label.setText(f"Scanning {done} of {total}")
        self.current_file_label.setText(path)

    def on_scan_finished(self, result: dict) -> None:
        self.scan_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.current_file_label.setText("")
        self.status_label.setText(
            f"Scanned {result['scanned']} tracks | Invalid: {result['invalid']}"
        )
        self.reload_tracks()

    def on_scan_failed(self, error: str) -> None:
        self.scan_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_label.setText(f"Scan failed: {error}")

    def cleanup_scan_thread(self) -> None:
        if self.scan_worker is not None:
            self.scan_worker.deleteLater()
            self.scan_worker = None

        if self.scan_thread is not None:
            self.scan_thread.deleteLater()
            self.scan_thread = None

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
