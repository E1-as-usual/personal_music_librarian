from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QListWidget
from PySide6.QtWidgets import QListWidgetItem, QPushButton, QSpinBox
from PySide6.QtWidgets import QTextEdit, QVBoxLayout, QWidget

from personal_music_librarian.core.database.db import Database
from personal_music_librarian.core.database.repositories.album_repo import AlbumRepository


class AlbumsPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.database = Database()
        self.database.initialize()
        self.albums = []

        self.refresh_button = QPushButton("Refresh Albums")
        self.refresh_button.clicked.connect(self.load_albums)

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search albums, artists, folders...")
        self.search_box.textChanged.connect(self.load_albums)

        self.genre_box = QLineEdit()
        self.genre_box.setPlaceholderText("Genre")
        self.genre_box.textChanged.connect(self.load_albums)

        self.year_box = QSpinBox()
        self.year_box.setMaximum(9999)
        self.year_box.setSpecialValueText("Any year")
        self.year_box.valueChanged.connect(self.load_albums)

        self.summary_label = QLabel("No albums loaded")

        self.album_list = QListWidget()
        self.album_list.currentRowChanged.connect(self.show_album)

        self.detail_box = QTextEdit()
        self.detail_box.setReadOnly(True)

        toolbar = QHBoxLayout()
        toolbar.addWidget(self.refresh_button)
        toolbar.addWidget(self.search_box)
        toolbar.addWidget(self.genre_box)
        toolbar.addWidget(self.year_box)
        toolbar.addWidget(self.summary_label)
        toolbar.addStretch(1)

        content = QHBoxLayout()
        content.addWidget(self.album_list, 1)
        content.addWidget(self.detail_box, 2)

        layout = QVBoxLayout(self)
        layout.addLayout(toolbar)
        layout.addLayout(content)

        self.load_albums()

    def load_albums(self) -> None:
        self.album_list.clear()
        self.detail_box.clear()

        text = self.search_box.text().strip() or None
        genre = self.genre_box.text().strip() or None
        year = self.year_box.value() or None

        with self.database.connection() as connection:
            repo = AlbumRepository(connection)
            self.albums = repo.get_all_with_stats(
                text=text,
                genre=genre,
                year=year,
            )

        for album in self.albums:
            artist = album["albumartist"] or "Unknown Artist"
            title = album["album"] or "Unknown Album"
            year_value = album["year"] or ""
            tracks = album["track_count"] or 0

            prefix = f"{year_value} | " if year_value else ""
            suffix = f" [{tracks} tracks]"

            self.album_list.addItem(
                QListWidgetItem(f"{prefix}{artist} - {title}{suffix}")
            )

        self.summary_label.setText(f"{len(self.albums)} albums")

        if self.albums:
            self.album_list.setCurrentRow(0)

    def show_album(self, row: int) -> None:
        if row < 0 or row >= len(self.albums):
            self.detail_box.clear()
            return

        album = self.albums[row]

        with self.database.connection() as connection:
            repo = AlbumRepository(connection)
            tracks = repo.get_tracks(int(album["id"]))

        total_duration = int(album["total_duration"] or 0)
        minutes = total_duration // 60
        seconds = total_duration % 60

        total_size_bytes = int(album["total_size_bytes"] or 0)
        total_size_mb = total_size_bytes / (1024 * 1024)

        lines = [
            album["album"] or "Unknown Album",
            "",
            f"Album artist: {album['albumartist'] or 'Unknown Artist'}",
            f"Date: {album['date'] or ''}",
            f"Year: {album['year'] or ''}",
            f"Genre: {album['genre'] or ''}",
            f"Folder: {album['folder_path'] or ''}",
            "",
            "Statistics:",
            f"  Tracks: {album['track_count'] or 0}",
            f"  Runtime: {minutes}:{seconds:02d}",
            f"  Size: {total_size_mb:.1f} MB",
            f"  Max sample rate: {album['max_sample_rate'] or ''}",
            f"  Max bit depth: {album['max_bit_depth'] or ''}",
            f"  Missing files: {album['missing_count'] or 0}",
            "",
            "Track list:",
        ]

        for track in tracks:
            disc = track["discnumber"] or 1
            number = track["tracknumber"] or "?"
            title = track["title"] or "Unknown Title"
            artist = track["artist"] or "Unknown Artist"

            duration = int(track["duration"] or 0)
            track_minutes = duration // 60
            track_seconds = duration % 60

            lines.append(
                f"  {disc}.{number} - {artist} - {title} [{track_minutes}:{track_seconds:02d}]"
            )

        self.detail_box.setPlainText("\n".join(lines))
