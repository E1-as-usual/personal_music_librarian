from dataclasses import asdict
from dataclasses import dataclass
from pathlib import Path
import json

from personal_music_librarian.config.defaults import DEFAULT_ADVANCED_MODE
from personal_music_librarian.config.defaults import DEFAULT_LIBRARY_FOLDERS
from personal_music_librarian.config.defaults import DEFAULT_THEME


@dataclass(slots=True)
class Settings:
    library_folders: list[str]
    theme: str
    advanced_mode: bool

    @classmethod
    def default(cls) -> "Settings":
        return cls(
            library_folders=DEFAULT_LIBRARY_FOLDERS.copy(),
            theme=DEFAULT_THEME,
            advanced_mode=DEFAULT_ADVANCED_MODE,
        )

    @classmethod
    def load(cls, path: Path) -> "Settings":
        if not path.exists():
            return cls.default()

        data = json.loads(path.read_text(encoding="utf-8"))

        return cls(
            library_folders=data.get("library_folders", []),
            theme=data.get("theme", DEFAULT_THEME),
            advanced_mode=data.get(
                "advanced_mode",
                DEFAULT_ADVANCED_MODE,
            ),
        )

    def save(self, path: Path) -> None:
        path.write_text(
            json.dumps(asdict(self), indent=2),
            encoding="utf-8",
        )
