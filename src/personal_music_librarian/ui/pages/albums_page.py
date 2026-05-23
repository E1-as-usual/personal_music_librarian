from PySide6.QtWidgets import QHBoxLayout, QLabel, QListWidget, QListWidgetItem
from PySide6.QtWidgets import QPushButton, QTextEdit, QVBoxLayout, QWidget

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
        self.summary_label = QLabel("No albums loaded")
        self.album_list = QListWidget()
        self.album_list.currentRowChanged.connect(self.show_album)
        self.detail_box = QTextEdit()
        self.detail_box.setReadOnly(True)

        toolbar = QHBoxLayout()
        toolbar.addWidget(self.refresh_button)
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
        with self.database.connection() as connection:
            repo = AlbumRepository(connection)
            self.albums = repo.get_all()

        for album in self.albums:
            artist = album["albumartist"] or "Unknown Artist"
            title = album["album"] or "Unknown Album"
            year = album["year"] or ""
            prefix = f"{year} | " if year else ""
            self.album_list.addItem(QListWidgetItem(f"{prefix}{artist} - {title}"))

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

        lines = [
            album["album"] or "Unknown Album",
            "",
            f"Album artist: {album['albumartist'] or 'Unknown Artist'}",
            f"Date: {album['date'] or ''}",
            f"Year: {album['year'] or ''}",
            f"Genre: {album['genre'] or ''}",
            f"Folder: {album['folder_path'] or ''}",
            f"Tracks: {len(tracks)}",
            "",
            "Track list:",
        ]

        for track in tracks:
            disc = track["discnumber"] or 1
            number = track["tracknumber"] or "?"
            title = track["title"] or "Unknown Title"
            artist = track["artist"] or "Unknown Artist"
            lines.append(f"  {disc}.{number} - {artist} - {title}")

        self.detail_box.setPlainText("\n".join(lines))
