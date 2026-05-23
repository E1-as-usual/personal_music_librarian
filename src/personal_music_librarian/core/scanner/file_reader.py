from pathlib import Path

from mutagen.flac import FLAC

from personal_music_librarian.core.models.file_entry import FileEntry


def read_file_entry(path: Path) -> FileEntry:
    stat = path.stat()

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
    )


def read_audio_properties(path: Path) -> dict[str, int | float | None]:
    audio = FLAC(path)

    return {
        "duration": audio.info.length,
        "sample_rate": audio.info.sample_rate,
        "bit_depth": audio.info.bits_per_sample,
        "channels": audio.info.channels,
    }
