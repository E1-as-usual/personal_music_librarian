from personal_music_librarian.core.metadata.normalizer import MetadataNormalizer
from personal_music_librarian.core.models.track import Track
from personal_music_librarian.core.metadata.tags import ALBUM
from personal_music_librarian.core.metadata.tags import ALBUMARTIST
from personal_music_librarian.core.metadata.tags import ARTIST
from personal_music_librarian.core.metadata.tags import DATE
from personal_music_librarian.core.metadata.tags import DISCNUMBER
from personal_music_librarian.core.metadata.tags import GENRE
from personal_music_librarian.core.metadata.tags import TITLE
from personal_music_librarian.core.metadata.tags import TOTALDISCS
from personal_music_librarian.core.metadata.tags import TOTALTRACKS
from personal_music_librarian.core.metadata.tags import TRACKNUMBER


class TrackMapper:
    @staticmethod
    def from_tags(
        file_id: int,
        tags: dict[str, str | None],
        audio_properties: dict,
    ) -> Track:
        return Track(
            id=None,
            file_id=file_id,
            title=MetadataNormalizer.normalize_text(tags.get(TITLE)),
            artist=MetadataNormalizer.normalize_text(tags.get(ARTIST)),
            albumartist=MetadataNormalizer.normalize_text(
                tags.get(ALBUMARTIST)
            ),
            album=MetadataNormalizer.normalize_text(tags.get(ALBUM)),
            date=MetadataNormalizer.normalize_text(tags.get(DATE)),
            year=MetadataNormalizer.normalize_year(tags.get(DATE)),
            genre=MetadataNormalizer.normalize_text(tags.get(GENRE)),
            tracknumber=MetadataNormalizer.normalize_number(
                tags.get(TRACKNUMBER)
            ),
            totaltracks=MetadataNormalizer.normalize_number(
                tags.get(TOTALTRACKS)
            ),
            discnumber=MetadataNormalizer.normalize_number(
                tags.get(DISCNUMBER)
            ),
            totaldiscs=MetadataNormalizer.normalize_number(
                tags.get(TOTALDISCS)
            ),
            duration=audio_properties.get("duration"),
            sample_rate=audio_properties.get("sample_rate"),
            bit_depth=audio_properties.get("bit_depth"),
            channels=audio_properties.get("channels"),
        )
