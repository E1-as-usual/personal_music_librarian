from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class FileEntry:
    id: int | None
    path: Path
    parent_folder: str
    filename: str
    extension: str
    size_bytes: int
    modified_time: float
    file_hash: str | None
    audio_hash: str | None
    codec: str
    is_missing: bool
    has_cover: bool = False
    cover_mime: str | None = None
    cover_size_bytes: int | None = None
