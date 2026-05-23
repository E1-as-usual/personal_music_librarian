from pathlib import Path

from personal_music_librarian.core.database.db import Database
from personal_music_librarian.core.database.repositories.log_repo import LogRepository
from personal_music_librarian.core.metadata.writer import TagWriter


TAG_MAP = {
    "title": "TITLE",
    "artist": "ARTIST",
    "albumartist": "ALBUMARTIST",
    "album": "ALBUM",
    "date": "DATE",
    "genre": "GENRE",
    "tracknumber": "TRACKNUMBER",
    "discnumber": "DISCNUMBER",
}


class MetadataService:
    def __init__(self, database: Database) -> None:
        self.database = database

    def update_track_metadata(
        self,
        track_id: int,
        values: dict[str, str | int | None],
        write_to_file: bool = True,
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
                """
                SELECT t.*, f.path
                FROM tracks t
                JOIN files f ON t.file_id = f.id
                WHERE t.id = ?
                """,
                (track_id,),
            ).fetchone()

            if before is None:
                return

            connection.execute(
                f"UPDATE tracks SET {assignments} WHERE id = ?",
                params,
            )

            if write_to_file:
                flac_tags = {
                    TAG_MAP[key]: value
                    for key, value in updates.items()
                    if key in TAG_MAP
                }
                TagWriter.write_tags(Path(before["path"]), flac_tags)

            LogRepository(connection).write(
                operation_type="metadata_edit",
                item_type="track",
                item_id=track_id,
                old_value_json=str(dict(before)),
                new_value_json=str(updates),
                status="applied",
                message="Metadata updated in database and FLAC file"
                if write_to_file
                else "Metadata updated in database only",
            )
