from personal_music_librarian.core.database.query_builder import QueryBuilder
from personal_music_librarian.core.models.track import Track


class TrackRepository:
    def __init__(self, connection) -> None:
        self.connection = connection

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
            "SELECT * FROM tracks ORDER BY artist, album, discnumber, tracknumber"
        )
        return cursor.fetchall()

    def get_by_id(self, track_id: int):
        cursor = self.connection.execute(
            "SELECT * FROM tracks WHERE id = ?",
            (track_id,),
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
        query.like("artist", artist)
        query.like("album", album)
        query.equals("year", year)
        query.is_null_or_empty("title", missing_title)

        where = query.build()

        sql = (
            "SELECT * FROM tracks "
            f"{where.sql} "
            "ORDER BY artist, album, discnumber, tracknumber"
        )

        cursor = self.connection.execute(sql, where.params)
        return cursor.fetchall()
