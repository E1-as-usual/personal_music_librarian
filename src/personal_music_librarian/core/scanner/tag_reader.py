from pathlib import Path

from mutagen.flac import FLAC

from personal_music_librarian.core.metadata.tags import ALBUM
from personal_music_librarian.core.metadata.tags import ALBUMARTIST
from personal_music_librarian.core.metadata.tags import DATE
from personal_music_librarian.core.metadata.tags import DISCNUMBER
from personal_music_librarian.core.metadata.tags import GENRE
from personal_music_librarian.core.metadata.tags import TITLE
from personal_music_librarian.core.metadata.tags import TOTALDISCS
from personal_music_librarian.core.metadata.tags import TOTALTRACKS
from personal_music_librarian.core.metadata.tags import TRACKNUMBER
from personal_music_librarian.core.metadata.tags import ARTIST


TAGS = [
    TITLE,
    ARTIST,
    ALBUMARTIST,
    ALBUM,
    DATE,
    GENRE,
    TRACKNUMBER,
    TOTALTRACKS,
    DISCNUMBER,
    TOTALDISCS,
]


class TagReader:
    @staticmethod
    def read(path: Path) -> dict[str, str | None]:
        audio = FLAC(path)

        tags: dict[str, str | None] = {}

        for tag in TAGS:
            values = audio.get(tag)
            tags[tag] = str(values[0]) if values else None

        return tags
