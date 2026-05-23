from pathlib import Path
import shutil

from personal_music_librarian.core.database.db import Database
from personal_music_librarian.core.database.repositories.duplicate_repo import DuplicateRepository
from personal_music_librarian.core.database.repositories.file_repo import FileRepository


class DuplicateActionService:
    def __init__(self, database: Database) -> None:
        self.database = database

    def move_non_keepers_to_review(
        self,
        file_hash: str,
        keeper_track_id: int,
        review_root: Path,
    ) -> dict[str, int]:
        moved = 0
        skipped = 0
        failed = 0

        review_root.mkdir(parents=True, exist_ok=True)

        with self.database.connection() as connection:
            duplicate_repo = DuplicateRepository(connection)
            file_repo = FileRepository(connection)
            tracks = duplicate_repo.get_duplicate_tracks(file_hash)

            for track in tracks:
                if int(track["id"]) == keeper_track_id:
                    skipped += 1
                    continue

                source = Path(track["path"])

                if not source.exists():
                    file_repo.mark_missing(source)
                    failed += 1
                    continue

                destination = self._unique_destination(
                    review_root / source.name
                )

                try:
                    shutil.move(str(source), str(destination))
                    file_repo.mark_missing(source)
                    moved += 1
                except Exception:
                    failed += 1

        return {
            "moved": moved,
            "skipped": skipped,
            "failed": failed,
        }

    def _unique_destination(self, destination: Path) -> Path:
        if not destination.exists():
            return destination

        stem = destination.stem
        suffix = destination.suffix
        parent = destination.parent
        counter = 1

        while True:
            candidate = parent / f"{stem} ({counter}){suffix}"
            if not candidate.exists():
                return candidate
            counter += 1
