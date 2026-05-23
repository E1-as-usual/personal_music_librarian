from pathlib import Path

from personal_music_librarian.core.renamer.rename_plan import RenamePlan
from personal_music_librarian.core.renamer.sanitizer import sanitize_segment


class TemplateEngine:
    @staticmethod
    def render(track: dict, template: str, library_root: Path) -> RenamePlan:
        values = {
            'title': sanitize_segment(track.get('title')),
            'artist': sanitize_segment(track.get('artist')),
            'albumartist': sanitize_segment(track.get('albumartist')),
            'album': sanitize_segment(track.get('album')),
            'tracknumber': track.get('tracknumber') or 0,
            'discnumber': track.get('discnumber') or 0,
        }

        relative = template.format(**values)

        return RenamePlan(
            source_path=Path(track['path']),
            target_path=library_root / relative,
        )
