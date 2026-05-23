from pathlib import Path

from personal_music_librarian.core.database.db import Database


def test_database_initializes(tmp_path: Path):
    database = Database(root=tmp_path)
    database.initialize()

    assert database.path.exists()

    with database.connection() as connection:
        tables = connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()

    table_names = {row['name'] for row in tables}

    assert 'files' in table_names
    assert 'tracks' in table_names
    assert 'duplicate_groups' in table_names
