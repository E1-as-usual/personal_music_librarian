from PySide6.QtWidgets import QCheckBox
from PySide6.QtWidgets import QFormLayout
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QSpinBox
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from personal_music_librarian.core.database.db import Database
from personal_music_librarian.core.database.repositories.track_repo import TrackRepository
from personal_music_librarian.core.services.metadata_service import MetadataService


class MetadataEditorPage(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.database = Database()
        self.database.initialize()
        self.metadata_service = MetadataService(self.database)
        self.current_track_id: int | None = None

        self.track_id_box = QSpinBox()
        self.track_id_box.setMaximum(10_000_000)

        self.load_button = QPushButton("Load Track")
        self.load_button.clicked.connect(self.load_track)

        topbar = QHBoxLayout()
        topbar.addWidget(QLabel("Track ID:"))
        topbar.addWidget(self.track_id_box)
        topbar.addWidget(self.load_button)
        topbar.addStretch(1)

        self.title_edit = QLineEdit()
        self.artist_edit = QLineEdit()
        self.albumartist_edit = QLineEdit()
        self.album_edit = QLineEdit()
        self.genre_edit = QLineEdit()
        self.date_edit = QLineEdit()
        self.year_box = QSpinBox()
        self.year_box.setMaximum(9999)
        self.tracknumber_box = QSpinBox()
        self.tracknumber_box.setMaximum(9999)
        self.discnumber_box = QSpinBox()
        self.discnumber_box.setMaximum(999)

        self.write_to_file_checkbox = QCheckBox("Write changes to FLAC file")
        self.write_to_file_checkbox.setChecked(True)

        form = QFormLayout()
        form.addRow("Title", self.title_edit)
        form.addRow("Artist", self.artist_edit)
        form.addRow("Album Artist", self.albumartist_edit)
        form.addRow("Album", self.album_edit)
        form.addRow("Genre", self.genre_edit)
        form.addRow("Date", self.date_edit)
        form.addRow("Year", self.year_box)
        form.addRow("Track Number", self.tracknumber_box)
        form.addRow("Disc Number", self.discnumber_box)

        self.save_button = QPushButton("Save Metadata")
        self.save_button.clicked.connect(self.save_metadata)

        self.status_label = QLabel("Load a track to edit metadata")

        layout = QVBoxLayout(self)
        layout.addLayout(topbar)
        layout.addLayout(form)
        layout.addWidget(self.write_to_file_checkbox)
        layout.addWidget(self.save_button)
        layout.addWidget(self.status_label)
        layout.addStretch(1)

    def load_track(self) -> None:
        track_id = self.track_id_box.value()

        with self.database.connection() as connection:
            track = TrackRepository(connection).get_by_id(track_id)

        if track is None:
            QMessageBox.warning(self, "Track Not Found", "No track exists with that ID")
            self.current_track_id = None
            return

        self.current_track_id = track_id
        self.title_edit.setText(track["title"] or "")
        self.artist_edit.setText(track["artist"] or "")
        self.albumartist_edit.setText(track["albumartist"] or "")
        self.album_edit.setText(track["album"] or "")
        self.genre_edit.setText(track["genre"] or "")
        self.date_edit.setText(track["date"] or "")
        self.year_box.setValue(track["year"] or 0)
        self.tracknumber_box.setValue(track["tracknumber"] or 0)
        self.discnumber_box.setValue(track["discnumber"] or 0)
        self.status_label.setText(f"Loaded track {track_id}")

    def save_metadata(self) -> None:
        if self.current_track_id is None:
            QMessageBox.warning(self, "No Track Loaded", "Load a track before saving")
            return

        if not self.title_edit.text().strip():
            QMessageBox.warning(self, "Validation Error", "Title cannot be empty")
            return

        self.metadata_service.update_track_metadata(
            track_id=self.current_track_id,
            values={
                "title": self.title_edit.text().strip(),
                "artist": self.artist_edit.text().strip(),
                "albumartist": self.albumartist_edit.text().strip(),
                "album": self.album_edit.text().strip(),
                "genre": self.genre_edit.text().strip(),
                "date": self.date_edit.text().strip(),
                "year": self.year_box.value(),
                "tracknumber": self.tracknumber_box.value(),
                "discnumber": self.discnumber_box.value(),
            },
            write_to_file=self.write_to_file_checkbox.isChecked(),
        )

        self.status_label.setText(f"Saved metadata for track {self.current_track_id}")
        QMessageBox.information(self, "Metadata Saved", "Track metadata updated")
