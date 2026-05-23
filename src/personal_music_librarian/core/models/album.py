from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class Album:
    id: int | None
    albumartist: str | None
    album: str | None
    date: str | None
    year: int | None
    totaldiscs: int | None
    genre: str | None
    folder_path: Path | None

    def display_name(self) -> str:
        if self.albumartist and self.album:
            return f"{self.albumartist} - {self.album}"

        if self.album:
            return self.album

        if self.albumartist:
            return f"{self.albumartist} - Unknown Album"

        return "Unknown Album"

    def identity_key(self) -> tuple[str, str, str]:
        return (
            self.albumartist or "",
            self.album or "",
            self.date or "",
        )
