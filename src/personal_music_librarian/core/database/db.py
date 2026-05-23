from pathlib import Path
import sqlite3


DATABASE_NAME = "library.db"
SCHEMA_FILE = "schema.sql"


class Database:
    def __init__(self, root: Path | None = None) -> None:
        self.root = root or Path.cwd()
        self.path = self.root / DATABASE_NAME

    def connection(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    def initialize(self) -> None:
        schema_path = Path(__file__).with_name(SCHEMA_FILE)
        schema = schema_path.read_text(encoding="utf-8")

        with self.connection() as connection:
            connection.executescript(schema)
            connection.commit()
