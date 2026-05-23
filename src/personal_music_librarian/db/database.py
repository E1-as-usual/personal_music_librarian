from pathlib import Path
import sqlite3


DATABASE_NAME = "library.db"


SCHEMA = """
CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY,
    path TEXT UNIQUE NOT NULL,
    filename TEXT,
    size_bytes INTEGER,
    modified_time REAL,
    file_hash TEXT,
    codec TEXT,
    last_scanned TEXT
);

CREATE TABLE IF NOT EXISTS tracks (
    id INTEGER PRIMARY KEY,
    file_id INTEGER NOT NULL,
    title TEXT,
    artist TEXT,
    albumartist TEXT,
    album TEXT,
    date TEXT,
    genre TEXT,
    tracknumber TEXT,
    discnumber TEXT,
    duration REAL,
    sample_rate INTEGER,
    bit_depth INTEGER,
    FOREIGN KEY(file_id) REFERENCES files(id)
);
"""


class Database:
    def __init__(self, root: Path | None = None) -> None:
        self.root = root or Path.cwd()
        self.path = self.root / DATABASE_NAME

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    def initialize(self) -> None:
        with self.connect() as connection:
            connection.executescript(SCHEMA)
            connection.commit()
