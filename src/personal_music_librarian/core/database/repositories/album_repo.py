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

    def get_all_with_stats(
        self,
        text: str | None = None,
        genre: str | None = None,
        year: int | None = None,
    ):
        clauses = []
        params = []

        if text:
            clauses.append(
                "(a.albumartist LIKE ? OR a.album LIKE ? OR a.folder_path LIKE ?)"
            )
            pattern = f"%{text}%"
            params.extend([pattern, pattern, pattern])

        if genre:
            clauses.append("a.genre LIKE ?")
            params.append(f"%{genre}%")

        if year:
            clauses.append("a.year = ?")
            params.append(year)

        where_sql = ""
        if clauses:
            where_sql = "WHERE " + " AND ".join(clauses)

        cursor = self.connection.execute(
            f"""
            SELECT
                a.*,
                COUNT(t.id) AS track_count,
                COALESCE(SUM(t.duration), 0) AS total_duration,
                COALESCE(SUM(f.size_bytes), 0) AS total_size_bytes,
                MAX(t.sample_rate) AS max_sample_rate,
                MAX(t.bit_depth) AS max_bit_depth,
                SUM(CASE WHEN f.is_missing = 1 THEN 1 ELSE 0 END) AS missing_count
            FROM albums a
            LEFT JOIN tracks t ON t.album_id = a.id
            LEFT JOIN files f ON f.id = t.file_id
            {where_sql}
            GROUP BY a.id
            ORDER BY a.albumartist, a.year, a.album
            """,
            tuple(params),
        )

        return cursor.fetchall()

    def get_tracks(self, album_id: int):
        cursor = self.connection.execute(
            """
            SELECT
                t.*,
                f.path,
                f.size_bytes,
                f.is_missing
            FROM tracks t
            JOIN files f ON f.id = t.file_id
            WHERE t.album_id = ?
            ORDER BY t.discnumber, t.tracknumber
            """,
            (album_id,),
        )

        return cursor.fetchall()
