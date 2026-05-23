from pathlib import Path

from personal_music_librarian.core.models.file_entry import FileEntry


class FileRepository:
    def __init__(self, connection) -> None:
        self.connection = connection

    def upsert(self, file_entry: FileEntry) -> int:
        cursor = self.connection.execute(
            """
            INSERT OR REPLACE INTO files (
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

    def mark_missing(self, path: Path) -> None:
        self.connection.execute(
            "UPDATE files SET is_missing = 1 WHERE path = ?",
            (str(path),),
        )
