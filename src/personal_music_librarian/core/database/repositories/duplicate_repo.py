class DuplicateRepository:
    def __init__(self, connection) -> None:
        self.connection = connection

    def find_exact_duplicates(self):
        cursor = self.connection.execute(
            """
            SELECT
                f.file_hash,
                COUNT(*) as duplicate_count
            FROM files f
            WHERE f.file_hash IS NOT NULL
            GROUP BY f.file_hash
            HAVING COUNT(*) > 1
            ORDER BY duplicate_count DESC
            """
        )

        return cursor.fetchall()

    def get_duplicate_tracks(self, file_hash: str):
        cursor = self.connection.execute(
            """
            SELECT
                t.id,
                t.title,
                t.artist,
                t.album,
                t.tracknumber,
                t.discnumber,
                f.path,
                f.size_bytes,
                f.file_hash
            FROM tracks t
            JOIN files f ON t.file_id = f.id
            WHERE f.file_hash = ?
            ORDER BY t.artist, t.album, t.discnumber, t.tracknumber
            """,
            (file_hash,),
        )

        return cursor.fetchall()
