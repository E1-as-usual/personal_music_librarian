# Personal Music Librarian

A safe, offline-first desktop FLAC library manager for scanning, organizing, deduplicating, renaming, exporting, and eventually converting a music library for SD-card use on FiiO DAPs and similar players.

## Project principle

The FLAC files remain the source of truth. SQLite is used for speed, filtering, planning, duplicate review, export jobs, and history. Risky actions must follow this workflow:

```text
Scan -> Preview -> Confirm -> Apply -> Log
```

No destructive file operation should happen without a preview and an operation log.

## Offline-first and shareable

The application must work fully offline by default.

- No login is required.
- No cloud service is required.
- No remote database is required.
- No telemetry is collected.
- Scanning, metadata editing, duplicate detection, renaming, exporting, and conversion run locally.
- SQLite databases, settings, logs, and export history stay local to the user's machine.
- Internet access may only be used by optional future features, and those features must be disabled by default.

Shareability is handled through local exports, not cloud sync. The app should support exporting SD-card-ready folders, playlists, logs, manifests, reports, and optional backup packages that can be copied or shared manually.

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
