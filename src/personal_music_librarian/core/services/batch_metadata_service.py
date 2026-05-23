from personal_music_librarian.core.database.db import Database
from personal_music_librarian.core.services.metadata_service import MetadataService


class BatchMetadataService:
    def __init__(self, database: Database) -> None:
        self.database = database
        self.metadata_service = MetadataService(database)

    def update_tracks(
        self,
        track_ids: list[int],
        values: dict[str, str | int | None],
        write_to_file: bool = True,
    ) -> dict[str, int]:
        applied = 0
        skipped = 0
        failed = 0

        cleaned_values = {
            key: value
            for key, value in values.items()
            if value is not None and str(value).strip() != ""
        }

        if not cleaned_values:
            return {
                "applied": applied,
                "skipped": len(track_ids),
                "failed": failed,
            }

        for track_id in track_ids:
            try:
                self.metadata_service.update_track_metadata(
                    track_id=track_id,
                    values=cleaned_values,
                    write_to_file=write_to_file,
                )
                applied += 1
            except Exception:
                failed += 1

        return {
            "applied": applied,
            "skipped": skipped,
            "failed": failed,
        }
