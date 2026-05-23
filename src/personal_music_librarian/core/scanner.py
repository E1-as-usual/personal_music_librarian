from pathlib import Path

from personal_music_librarian.core.metadata import MetadataReader


class LibraryScanner:
    def scan(self, root: Path) -> list[dict]:
        tracks: list[dict] = []

        for path in root.rglob("*.flac"):
            try:
                metadata = MetadataReader.read(path)
            except Exception as error:
                print(f"Failed to scan {path}: {error}")
                continue

            tracks.append(
                {
                    "path": str(path),
                    **metadata,
                }
            )

        return tracks
