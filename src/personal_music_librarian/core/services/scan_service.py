from pathlib import Path
import logging

from personal_music_librarian.core.database.db import Database
from personal_music_librarian.core.database.repositories.file_repo import FileRepository
from personal_music_librarian.core.database.repositories.track_repo import TrackRepository
from personal_music_librarian.core.hashing import FileHasher
from personal_music_librarian.core.metadata.validator import MetadataValidator
from personal_music_librarian.core.scanner.file_reader import read_audio_properties
from personal_music_librarian.core.scanner.file_reader import read_file_entry
from personal_music_librarian.core.scanner.tag_reader import TagReader
from personal_music_librarian.core.scanner.track_mapper import TrackMapper


logger = logging.getLogger(__name__)


class ScanService:
    def __init__(self, database: Database) -> None:
        self.database = database

    def scan_library(
        self,
        root: Path,
        progress_callback=None,
        cancel_callback=None,
    ) -> dict[str, int]:
        scanned = 0
        invalid = 0
        cancelled = 0
        failed = 0

        paths = list(root.rglob("*.flac"))
        total = len(paths)

        with self.database.connection() as connection:
            file_repo = FileRepository(connection)
            track_repo = TrackRepository(connection)

            file_repo.mark_all_missing()

            for path in paths:
                if cancel_callback is not None and cancel_callback():
                    cancelled = 1
                    break

                try:
                    file_entry = read_file_entry(path)
                    file_entry.file_hash = FileHasher.hash_file(path)

                    file_id = file_repo.upsert(file_entry)
                    file_repo.clear_missing(path)

                    tags = TagReader.read(path)

                    if not MetadataValidator.is_valid(tags):
                        invalid += 1

                    audio_properties = read_audio_properties(path)

                    track = TrackMapper.from_tags(
                        file_id=file_id,
                        tags=tags,
                        audio_properties=audio_properties,
                    )

                    track_repo.upsert(track)

                    scanned += 1

                    if progress_callback is not None:
                        progress_callback(scanned, total, path)

                except Exception as error:
                    failed += 1
                    logger.exception(
                        "Failed scanning file: %s",
                        path,
                        exc_info=error,
                    )

        logger.info(
            "Scan complete | scanned=%s invalid=%s failed=%s total=%s cancelled=%s",
            scanned,
            invalid,
            failed,
            total,
            cancelled,
        )

        return {
            "scanned": scanned,
            "invalid": invalid,
            "failed": failed,
            "total": total,
            "cancelled": cancelled,
        }
