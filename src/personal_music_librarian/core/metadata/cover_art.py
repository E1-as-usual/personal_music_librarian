from pathlib import Path

from mutagen.flac import FLAC
from mutagen.flac import Picture


class CoverArtError(Exception):
    pass


class CoverArtManager:
    @staticmethod
    def extract_first_cover(path: Path) -> bytes | None:
        try:
            audio = FLAC(path)
            if not audio.pictures:
                return None
            return audio.pictures[0].data
        except Exception as error:
            raise CoverArtError(str(error)) from error

    @staticmethod
    def replace_front_cover(path: Path, image_path: Path) -> None:
        try:
            audio = FLAC(path)
            image_data = image_path.read_bytes()

            picture = Picture()
            picture.type = 3
            picture.mime = _guess_mime(image_path)
            picture.desc = "Cover"
            picture.data = image_data

            audio.clear_pictures()
            audio.add_picture(picture)
            audio.save()
        except Exception as error:
            raise CoverArtError(str(error)) from error


def _guess_mime(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".jpg", ".jpeg"}:
        return "image/jpeg"
    if suffix == ".png":
        return "image/png"
    return "application/octet-stream"
