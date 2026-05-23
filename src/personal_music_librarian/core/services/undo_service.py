import json
from pathlib import Path
import shutil

from personal_music_librarian.core.database.db import Database
from personal_music_librarian.core.database.repositories.file_repo import FileRepository
from personal_music_librarian.core.database.repositories.log_repo import LogRepository
from personal_music_librarian.core.services.history_service import HistoryService


class UndoService:
    def __init__(self, database: Database) -> None:
        self.database = database
        self.history = HistoryService(database)

    def undo_last_operation(self) -> dict[str, str]:
        with self.database.connection() as connection:
            logs = LogRepository(connection)
            file_repo = FileRepository(connection)

            operation = logs.latest_reversible()

            if operation is None:
                return {
                    'status': 'none',
                    'message': 'No reversible operations found',
                }

            old_data = json.loads(operation['old_value_json'])
            new_data = json.loads(operation['new_value_json'])

            source = Path(new_data['path'])
            target = Path(old_data['path'])

            if not source.exists():
                return {
                    'status': 'failed',
                    'message': 'Current file no longer exists',
                }

            if target.exists() and target != source:
                return {
                    'status': 'failed',
                    'message': 'Original path already occupied',
                }

            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), str(target))
            file_repo.update_path(source, target)

            self.history.log_rename(
                source,
                target,
                status='undo_applied',
                message='Undo operation executed',
            )

            return {
                'status': 'applied',
                'message': f'Undo restored {target.name}',
            }
