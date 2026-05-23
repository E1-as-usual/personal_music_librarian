from personal_music_librarian.core.database.query_builder import QueryBuilder
from personal_music_librarian.core.models.track import Track


TRACK_SELECT = """
SELECT
    t.*,
    f.path,
    f.size_bytes,
    f.file_hash,
    f.is_missing
FROM tracks t
JOIN files f ON t.file_id = f.id
"""


class TrackRepository:
    def __init__(self, connection) -> None:
        self.connection = connection

    def upsert(self, track: Track) -> int:
        existing = self.get_by_file_id(track.file_id)

        if existing is None:
            return self.insert(track)

        self.connection.execute(
            """
            UPDATE tracks SET
                title = ?,
                artist = ?,
                albumartist = ?,
                album = ?,
                date = ?,
                year = ?,
                genre = ?,
                tracknumber = ?,
                totaltracks = ?,
                discnumber = ?,
                totaldiscs = ?,
                duration = ?,
                sample_rate = ?,
                bit_depth = ?,
                channels = ?
            WHERE file_id = ?
            """,
            (
                track.title,
                track.artist,
                track.albumartist,
                track.album,
                track.date,
                track.year,
                track.genre,
                track.tracknumber,
                track.totaltracks,
                track.discnumber,
                track.totaldiscs,
                track.duration,
                track.sample_rate,
                track.bit_depth,
                track.channels,
                track.file_id,
            ),
        )

        return int(existing["id"])

    def insert(self, track: Track) -> int:
        cursor = self.connection.execute(
            """
            INSERT INTO tracks (
                file_id,
                title,
                artist,
                albumartist,
                album,
                date,
                year,
                genre,
                tracknumber,
                totaltracks,
                discnumber,
                totaldiscs,
                duration,
                sample_rate,
                bit_depth,
                channels
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                track.file_id,
                track.title,
                track.artist,
                track.albumartist,
                track.album,
                track.date,
                track.year,
                track.genre,
                track.tracknumber,
                track.totaltracks,
                track.discnumber,
                track.totaldiscs,
                track.duration,
                track.sample_rate,
                track.bit_depth,
                track.channels,
            ),
        )

        return int(cursor.lastrowid)

    def get_all(self):
        cursor = self.connection.execute(
            TRACK_SELECT + "ORDER BY artist, album, discnumber, tracknumber"
        )
        return cursor.fetchall()

    def get_by_id(self, track_id: int):
        cursor = self.connection.execute(
            TRACK_SELECT + "WHERE t.id = ?",
            (track_id,),
        )
        return cursor.fetchone()

    def get_by_file_id(self, file_id: int):
        cursor = self.connection.execute(
            "SELECT * FROM tracks WHERE file_id = ?",
            (file_id,),
        )
        return cursor.fetchone()

    def search(
        self,
        artist: str | None = None,
        album: str | None = None,
        year: int | None = None,
        missing_title: bool = False,
    ):
        query = QueryBuilder()
        query.like("t.artist", artist)
        query.like("t.album", album)
        query.equals("t.year", year)
        query.is_null_or_empty("t.title", missing_title)

        where = query.build()

        sql = TRACK_SELECT + f"{where.sql} ORDER BY artist, album, discnumber, tracknumber"

        cursor = self.connection.execute(sql, where.params)
        return cursor.fetchall()
