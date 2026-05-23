from pathlib import Path

from PySide6.QtCore import QObject
from PySide6.QtCore import Signal

from personal_music_librarian.core.database.db import Database
from personal_music_librarian.core.services.scan_service import ScanService


class ScanWorker(QObject):
    finished = Signal(dict)
    failed = Signal(str)
    status = Signal(str)

    def __init__(self, folder: Path) -> None:
        super().__init__()

        self.folder = folder

    def run(self) -> None:
        try:
            self.status.emit("Scanning library...")

            database = Database()
            database.initialize()

            service = ScanService(database)
            result = service.scan_library(self.folder)

            self.finished.emit(result)

        except Exception as error:
            self.failed.emit(str(error))
