from pathlib import Path

from mutagen.flac import FLAC

from personal_music_librarian.core.models.file_entry import FileEntry


COVER_FILENAMES = {
    "cover.jpg",
    "cover.jpeg",
    "cover.png",
    "folder.jpg",
    "folder.jpeg",
    "folder.png",
    "front.jpg",
    "front.jpeg",
    "front.png",
}


def read_file_entry(path: Path) -> FileEntry:
    stat = path.stat()

    has_cover = False
    cover_mime = None
    cover_size_bytes = None

    audio = FLAC(path)

    if audio.pictures:
        picture = audio.pictures[0]
        has_cover = True
        cover_mime = picture.mime
        cover_size_bytes = len(picture.data)
    else:
        for candidate in COVER_FILENAMES:
            cover_path = path.parent / candidate
            if cover_path.exists():
                has_cover = True
                cover_size_bytes = cover_path.stat().st_size

                suffix = cover_path.suffix.lower()
                if suffix in {".jpg", ".jpeg"}:
                    cover_mime = "image/jpeg"
                elif suffix == ".png":
                    cover_mime = "image/png"

                break

    return FileEntry(
        id=None,
        path=path,
        parent_folder=str(path.parent),
        filename=path.name,
        extension=path.suffix.lower(),
        size_bytes=stat.st_size,
        modified_time=stat.st_mtime,
        file_hash=None,
        audio_hash=None,
        codec="FLAC",
        is_missing=False,
        has_cover=has_cover,
        cover_mime=cover_mime,
        cover_size_bytes=cover_size_bytes,
    )


def read_audio_properties(path: Path) -> dict[str, int | float | None]:
    audio = FLAC(path)

    return {
        "duration": audio.info.length,
        "sample_rate": audio.info.sample_rate,
        "bit_depth": audio.info.bits_per_sample,
        "channels": audio.info.channels,
    }
