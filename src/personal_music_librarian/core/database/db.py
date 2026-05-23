from contextlib import contextmanager
from pathlib import Path
from typing import Iterator
import sqlite3

from personal_music_librarian.config.paths import AppPaths


DATABASE_NAME = "library.db"
SCHEMA_FILE = "schema.sql"


class Database:
    def __init__(self, root: Path | None = None) -> None:
        self.root = root or AppPaths.resolve().data_dir
        self.root.mkdir(parents=True, exist_ok=True)
        self.path = self.root / DATABASE_NAME

    @contextmanager
    def connection(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA journal_mode = WAL")

        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def initialize(self) -> None:
        schema_path = Path(__file__).with_name(SCHEMA_FILE)
        schema = schema_path.read_text(encoding="utf-8")

        with self.connection() as connection:
            connection.executescript(schema)
