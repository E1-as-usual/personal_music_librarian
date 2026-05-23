from personal_music_librarian.core.database.db import Database
from personal_music_librarian.core.database.repositories.log_repo import LogRepository


class MetadataService:
    def __init__(self, database: Database) -> None:
        self.database = database

    def update_track_metadata(
        self,
        track_id: int,
        values: dict[str, str | int | None],
    ) -> None:
        allowed = {
            "title",
            "artist",
            "albumartist",
            "album",
            "date",
            "year",
            "genre",
            "tracknumber",
            "discnumber",
        }
        updates = {key: value for key, value in values.items() if key in allowed}

        if not updates:
            return

        assignments = ", ".join(f"{key} = ?" for key in updates)
        params = list(updates.values()) + [track_id]

        with self.database.connection() as connection:
            before = connection.execute(
                "SELECT * FROM tracks WHERE id = ?",
                (track_id,),
            ).fetchone()

            connection.execute(
                f"UPDATE tracks SET {assignments} WHERE id = ?",
                params,
            )

            LogRepository(connection).write(
                operation_type="metadata_edit",
                item_type="track",
                item_id=track_id,
                old_value_json=str(dict(before)) if before else None,
                new_value_json=str(updates),
                status="applied",
                message="Database metadata updated",
            )
