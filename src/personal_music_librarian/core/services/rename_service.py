from pathlib import Path
import shutil

from personal_music_librarian.core.database.db import Database
from personal_music_librarian.core.database.repositories.file_repo import FileRepository
from personal_music_librarian.core.renamer.rename_plan import RenamePlan
from personal_music_librarian.core.services.history_service import HistoryService


class RenameService:
    def __init__(self, database: Database) -> None:
        self.database = database
        self.history = HistoryService(database)

    def apply_plans(self, plans: list[RenamePlan]) -> dict[str, int]:
        applied = 0
        skipped = 0
        failed = 0

        with self.database.connection() as connection:
            file_repo = FileRepository(connection)

            for plan in plans:
                if plan.conflict:
                    skipped += 1
                    self.history.log_rename(
                        plan.source_path,
                        plan.target_path,
                        status="skipped",
                        message=plan.reason,
                    )
                    continue

                source = plan.source_path
                target = plan.target_path

                if not source.exists():
                    file_repo.mark_missing(source)
                    self.history.log_rename(
                        source,
                        target,
                        status="failed",
                        message="Source file missing",
                    )
                    failed += 1
                    continue

                if target.exists() and target != source:
                    self.history.log_rename(
                        source,
                        target,
                        status="skipped",
                        message="Target already exists",
                    )
                    skipped += 1
                    continue

                try:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(source), str(target))
                    file_repo.update_path(source, target)

                    self.history.log_rename(
                        source,
                        target,
                        status="applied",
                    )

                    applied += 1
                except Exception as error:
                    self.history.log_rename(
                        source,
                        target,
                        status="failed",
                        message=str(error),
                    )
                    failed += 1

        return {
            "applied": applied,
            "skipped": skipped,
            "failed": failed,
        }
