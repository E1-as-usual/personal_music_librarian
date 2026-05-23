from pathlib import Path

from mutagen.flac import FLAC


class MetadataReader:
    @staticmethod
    def read(path: Path) -> dict:
        audio = FLAC(path)

        return {
            "title": _first(audio.get("TITLE")),
            "artist": _first(audio.get("ARTIST")),
            "albumartist": _first(audio.get("ALBUMARTIST")),
            "album": _first(audio.get("ALBUM")),
            "date": _first(audio.get("DATE")),
            "genre": _first(audio.get("GENRE")),
            "tracknumber": _first(audio.get("TRACKNUMBER")),
            "discnumber": _first(audio.get("DISCNUMBER")),
            "duration": audio.info.length,
            "sample_rate": audio.info.sample_rate,
            "bit_depth": audio.info.bits_per_sample,
        }


def _first(values: list | None) -> str | None:
    if not values:
        return None

    return str(values[0])
