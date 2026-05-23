# Personal Music Librarian

A safe, offline-first desktop FLAC library manager for organizing, cleaning, tagging, renaming, deduplicating, exporting, and converting music libraries for SD-card playback on devices like FiiO DAPs.

The project is designed for users with large music collections, multiple album versions, loose tracks, discographies, and duplicate-heavy archives who want to build a clean, structured, portable music library.

---

# Core Design Principles

## FLAC files are the source of truth

The application is not just a database frontend.

- FLAC files remain the real music library.
- SQLite is used for indexing, filtering, duplicate grouping, export jobs, and operation history.
- Metadata edits must always be written back to the FLAC files themselves.

## Safety-first workflow

Every risky operation must follow:

```text
SCAN -> PREVIEW -> CONFIRM -> APPLY -> LOG -> UNDO
```

The application must never silently modify or delete files.

### Non-destructive by default

- Duplicate tracks are moved to `_Duplicates_Review/`
- Deletes use `send2trash`
- Renames are reversible
- Metadata edits store old values
- Exports never modify source files

---

# Offline-First and Shareable

The application must work fully offline by default.

- No login required
- No cloud dependency
- No telemetry
- No remote database
- All scanning, hashing, metadata editing, duplicate detection, exporting, and conversion happen locally
- SQLite database, settings, logs, and exports stay on the user's machine

Internet access may only be used by optional future features, and those features must be disabled by default.

## Shareability

Libraries should be easy to copy, archive, back up, and move between systems.

The application should support exporting:

- SD-card-ready music folders
- playlists
- operation logs
- export manifests
- backup packages
- portable staging folders

without requiring cloud synchronization.

---

# Main Features

## Library Scanning

- Recursive FLAC discovery
- Vorbis comment parsing via `mutagen`
- Album grouping
- Rescanning and change detection
- File metadata indexing
- SQLite-backed filtering and search

## Metadata Management

- Single-track editing
- Batch metadata editing
- Album-level editing
- Cover art embedding and extraction
- Metadata normalization and validation

## Duplicate Detection

Supports multiple duplicate detection levels:

1. Exact file hash duplicates
2. Same decoded audio duplicates
3. Fuzzy track duplicates
4. Album-position duplicates

The app never auto-deletes duplicates.

## Batch Renaming and Organization

- Template-driven folder structures
- Rename previews
- Conflict detection
- Cross-platform filename sanitization
- SD-card-safe path generation

## Export and Conversion

- Export albums, artists, playlists, or selections
- Optional FFmpeg conversion
- Export presets
- Size estimation
- Verification after export
- SD-card builder workflow

---

# Planned Application Screens

1. Library
2. Albums
3. Artists
4. Tracks
5. Duplicates
6. Metadata Fixer
7. Batch Rename Preview
8. Export / Convert Queue
9. SD Card Builder
10. Settings
11. Logs

---

# Architecture

The project follows a strict layered architecture.

```text
core/      -> business logic only
ui/        -> PySide6 widgets and pages
workers/   -> threaded background jobs
config/    -> settings and platform paths
resources/ -> icons, styles, bundled assets
tests/     -> automated tests
```

## Critical dependency rules

```text
core/ never imports ui/
workers/ never import ui/
ui/ communicates with workers via Qt signals only
core/models contains pure dataclasses only
```

All business logic must remain testable without launching the UI.

---

# Technology Stack

## Core

- Python 3.11+
- SQLite
- PySide6
- mutagen
- FFmpeg
- xxhash or blake3
- rapidfuzz
- send2trash

## Testing and Tooling

- pytest
- pytest-qt
- ruff
- mypy

---

# Current Development Status

The repository currently contains the initial V0.1 foundation:

- Python package structure
- PySide6 application bootstrap
- SQLite initialization layer
- FLAC metadata reader
- Recursive library scanner
- Hashing utilities
- Early service-layer foundation

The next major milestones are:

1. Repository/database abstraction layer
2. Track dataclasses and models
3. Scan persistence pipeline
4. Qt table models
5. Rename planning engine
6. Operation logging and undo support
7. Duplicate detection pipeline
8. Worker-thread infrastructure

---

# Version Roadmap

## Version 0.1

- Select library folder
- Scan FLAC files
- Read metadata
- Store tracks in SQLite
- Display/filter tracks
- Batch selection
- Rename preview system
- Exact duplicate detection
- Basic export system

## Version 0.2

- Metadata editor
- Cover art support
- Duplicate review UI
- Duplicate review folder workflow
- Export by artist/album
- Export size estimation

## Version 0.3

- FFmpeg conversion
- Export presets
- SD-card builder
- Export queue
- Better duplicate detection

## Version 1.0

- Stable desktop UI
- Undo support
- Audio fingerprinting
- Playlist support
- ReplayGain support
- Full export workflow
- Settings profiles

---

# Development Setup

## Create virtual environment

```bash
python -m venv .venv
```

### Linux/macOS

```bash
source .venv/bin/activate
```

### Windows

```powershell
.venv\Scripts\activate
```

## Install dependencies

```bash
pip install -e .[dev]
```

## Run the application

```bash
python -m personal_music_librarian
```

## Run tests

```bash
pytest
```

---

# Long-Term Goal

The long-term goal is to build a professional-grade offline desktop music library manager focused on:

- safety
- transparency
- portability
- duplicate management
- metadata quality
- SD-card export workflows
- large local music collections
