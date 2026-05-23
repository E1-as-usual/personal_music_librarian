from pathlib import Path

from PySide6.QtCore import QObject
from PySide6.QtCore import Signal

from personal_music_librarian.core.database.db import Database
from personal_music_librarian.core.services.scan_service import ScanService


class ScanWorker(QObject):
    finished = Signal(dict)
    failed = Signal(str)
    status = Signal(str)
    progress = Signal(int, int, str)

    def __init__(self, folder: Path) -> None:
        super().__init__()

        self.folder = folder
        self.cancel_requested = False

    def cancel(self) -> None:
        self.cancel_requested = True

    def is_cancelled(self) -> bool:
        return self.cancel_requested

    def run(self) -> None:
        try:
            self.status.emit("Scanning library...")

            database = Database()
            database.initialize()

            service = ScanService(database)
            result = service.scan_library(
                self.folder,
                progress_callback=self._on_progress,
                cancel_callback=self.is_cancelled,
            )

            self.finished.emit(result)

        except Exception as error:
            self.failed.emit(str(error))

    def _on_progress(self, done: int, total: int, path: Path) -> None:
        self.progress.emit(done, total, str(path))
