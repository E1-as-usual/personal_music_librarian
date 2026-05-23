from pathlib import Path

from personal_music_librarian.core.models.album import Album


class AlbumRepository:
    def __init__(self, connection) -> None:
        self.connection = connection

    def upsert(self, album: Album) -> int:
        existing = self.get_by_identity(album)

        if existing is not None:
            self.connection.execute(
                """
                UPDATE albums SET
                    year = ?,
                    totaldiscs = ?,
                    genre = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (
                    album.year,
                    album.totaldiscs,
                    album.genre,
                    existing["id"],
                ),
            )

            return int(existing["id"])

        cursor = self.connection.execute(
            """
            INSERT INTO albums (
                albumartist,
                album,
                date,
                year,
                totaldiscs,
                genre,
                folder_path
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                album.albumartist,
                album.album,
                album.date,
                album.year,
                album.totaldiscs,
                album.genre,
                str(album.folder_path) if album.folder_path else None,
            ),
        )

        return int(cursor.lastrowid)

    def get_by_identity(self, album: Album):
        cursor = self.connection.execute(
            """
            SELECT * FROM albums
            WHERE albumartist IS ?
              AND album IS ?
              AND date IS ?
              AND folder_path IS ?
            """,
            (
                album.albumartist,
                album.album,
                album.date,
                str(album.folder_path) if album.folder_path else None,
            ),
        )

        return cursor.fetchone()

    def get_all(self):
        cursor = self.connection.execute(
            """
            SELECT * FROM albums
            ORDER BY albumartist, year, album
            """
        )

        return cursor.fetchall()

    def get_tracks(self, album_id: int):
        cursor = self.connection.execute(
            """
            SELECT * FROM tracks
            WHERE album_id = ?
            ORDER BY discnumber, tracknumber
            """,
            (album_id,),
        )

        return cursor.fetchall()
