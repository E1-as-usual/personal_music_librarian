# Personal Music Librarian

A safe desktop FLAC library manager for scanning, organizing, deduplicating, renaming, exporting, and eventually converting a music library for SD-card use on FiiO DAPs and similar players.

## Project principle

The FLAC files remain the source of truth. SQLite is used for speed, filtering, planning, duplicate review, export jobs, and history. Risky actions must follow this workflow:

```text
Scan -> Preview -> Confirm -> Apply -> Log
```

No destructive file operation should happen without a preview and an operation log.

## Version 0.1 target

- Select a library folder.
- Scan FLAC files recursively.
- Read FLAC metadata with `mutagen`.
- Store file and track records in SQLite.
- Display/filter a track table.
- Batch select tracks.
- Preview rename/move plans using templates.
- Apply rename/move only after confirmation.
- Detect exact duplicate files by hash.
- Export selected albums/tracks to a folder without conversion.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -e .[dev]
```

Run the app:

```bash
python -m personal_music_librarian
```

Run tests:

```bash
pytest
```
