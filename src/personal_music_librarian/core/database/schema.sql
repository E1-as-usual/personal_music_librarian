CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY,
    path TEXT UNIQUE NOT NULL,
    parent_folder TEXT,
    filename TEXT,
    extension TEXT,
    size_bytes INTEGER,
    modified_time REAL,
    file_hash TEXT,
    audio_hash TEXT,
    codec TEXT,
    is_missing INTEGER DEFAULT 0,
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
    year INTEGER,
    genre TEXT,
    tracknumber INTEGER,
    totaltracks INTEGER,
    discnumber INTEGER,
    totaldiscs INTEGER,
    duration REAL,
    sample_rate INTEGER,
    bit_depth INTEGER,
    channels INTEGER,
    FOREIGN KEY(file_id) REFERENCES files(id)
);

CREATE TABLE IF NOT EXISTS operation_logs (
    id INTEGER PRIMARY KEY,
    operation_type TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    item_type TEXT NOT NULL,
    item_id INTEGER,
    old_value_json TEXT,
    new_value_json TEXT,
    status TEXT,
    message TEXT
);

CREATE INDEX IF NOT EXISTS idx_files_path
ON files(path);

CREATE INDEX IF NOT EXISTS idx_files_hash
ON files(file_hash);

CREATE INDEX IF NOT EXISTS idx_tracks_artist
ON tracks(artist);

CREATE INDEX IF NOT EXISTS idx_tracks_album
ON tracks(album);
