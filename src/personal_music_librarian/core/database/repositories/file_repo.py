from pathlib import Path

from personal_music_librarian.core.models.file_entry import FileEntry


class FileRepository:
    def __init__(self, connection) -> None:
        self.connection = connection

    def upsert(self, file_entry: FileEntry) -> int:
        existing = self.get_by_path(file_entry.path)

        if existing is not None:
            self.connection.execute(
                """
                UPDATE files SET
                    parent_folder = ?,
                    filename = ?,
                    extension = ?,
                    size_bytes = ?,
                    modified_time = ?,
                    file_hash = ?,
                    audio_hash = ?,
                    codec = ?,
                    is_missing = ?,
                    last_scanned = datetime('now')
                WHERE path = ?
                """,
                (
                    file_entry.parent_folder,
                    file_entry.filename,
                    file_entry.extension,
                    file_entry.size_bytes,
                    file_entry.modified_time,
                    file_entry.file_hash,
                    file_entry.audio_hash,
                    file_entry.codec,
                    int(file_entry.is_missing),
                    str(file_entry.path),
                ),
            )

            return int(existing["id"])

        cursor = self.connection.execute(
            """
            INSERT INTO files (
                path,
                parent_folder,
                filename,
                extension,
                size_bytes,
                modified_time,
                file_hash,
                audio_hash,
                codec,
                is_missing,
                last_scanned
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
            """,
            (
                str(file_entry.path),
                file_entry.parent_folder,
                file_entry.filename,
                file_entry.extension,
                file_entry.size_bytes,
                file_entry.modified_time,
                file_entry.file_hash,
                file_entry.audio_hash,
                file_entry.codec,
                int(file_entry.is_missing),
            ),
        )

        return int(cursor.lastrowid)

    def get_by_path(self, path: Path):
        cursor = self.connection.execute(
            "SELECT * FROM files WHERE path = ?",
            (str(path),),
        )
        return cursor.fetchone()

    def mark_all_missing(self) -> None:
        self.connection.execute(
            "UPDATE files SET is_missing = 1"
        )

    def clear_missing(self, path: Path) -> None:
        self.connection.execute(
            "UPDATE files SET is_missing = 0 WHERE path = ?",
            (str(path),),
        )

    def mark_missing(self, path: Path) -> None:
        self.connection.execute(
            "UPDATE files SET is_missing = 1 WHERE path = ?",
            (str(path),),
        )
