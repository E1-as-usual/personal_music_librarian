from pathlib import Path

from personal_music_librarian.core.database.db import Database
from personal_music_librarian.core.database.repositories.log_repo import LogRepository
from personal_music_librarian.core.metadata.cover_art import CoverArtManager


class CoverArtService:
    def __init__(self, database: Database) -> None:
        self.database = database

    def get_track_path(self, track_id: int) -> Path | None:
        with self.database.connection() as connection:
            row = connection.execute(
                """
                SELECT f.path
                FROM tracks t
                JOIN files f ON t.file_id = f.id
                WHERE t.id = ?
                """,
                (track_id,),
            ).fetchone()

        if row is None:
            return None

        return Path(row["path"])

    def extract_cover(self, track_id: int) -> bytes | None:
        path = self.get_track_path(track_id)
        if path is None:
            return None
        return CoverArtManager.extract_first_cover(path)

    def replace_cover(self, track_id: int, image_path: Path) -> None:
        path = self.get_track_path(track_id)
        if path is None:
            raise FileNotFoundError("Track path not found")

        CoverArtManager.replace_front_cover(path, image_path)

        with self.database.connection() as connection:
            LogRepository(connection).write(
                operation_type="cover_art_replace",
                item_type="track",
                item_id=track_id,
                old_value_json=None,
                new_value_json=str({"image_path": str(image_path)}),
                status="applied",
                message="Front cover replaced",
            )
