import json
from pathlib import Path

from personal_music_librarian.core.database.db import Database
from personal_music_librarian.core.database.repositories.log_repo import LogRepository


class HistoryService:
    def __init__(self, database: Database) -> None:
        self.database = database

    def log_rename(
        self,
        source: Path,
        target: Path,
        status: str,
        message: str | None = None,
    ) -> None:
        with self.database.connection() as connection:
            repo = LogRepository(connection)
            repo.write(
                operation_type="rename",
                item_type="file",
                item_id=None,
                old_value_json=json.dumps({"path": str(source)}),
                new_value_json=json.dumps({"path": str(target)}),
                status=status,
                message=message,
            )

    def log_duplicate_move(
        self,
        source: Path,
        target: Path,
        status: str,
        message: str | None = None,
    ) -> None:
        with self.database.connection() as connection:
            repo = LogRepository(connection)
            repo.write(
                operation_type="duplicate_move",
                item_type="file",
                item_id=None,
                old_value_json=json.dumps({"path": str(source)}),
                new_value_json=json.dumps({"path": str(target)}),
                status=status,
                message=message,
            )
