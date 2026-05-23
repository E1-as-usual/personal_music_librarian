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
