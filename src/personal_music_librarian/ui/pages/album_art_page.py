from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QSpinBox
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from personal_music_librarian.core.database.db import Database
from personal_music_librarian.core.services.cover_art_service import CoverArtService


class AlbumArtPage(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.database = Database()
        self.database.initialize()
        self.cover_service = CoverArtService(self.database)
        self.current_track_id: int | None = None

        self.track_id_box = QSpinBox()
        self.track_id_box.setMaximum(10_000_000)

        self.load_button = QPushButton("Load Cover")
        self.load_button.clicked.connect(self.load_cover)

        self.replace_button = QPushButton("Replace Cover")
        self.replace_button.clicked.connect(self.replace_cover)
        self.replace_button.setEnabled(False)

        toolbar = QHBoxLayout()
        toolbar.addWidget(QLabel("Track ID:"))
        toolbar.addWidget(self.track_id_box)
        toolbar.addWidget(self.load_button)
        toolbar.addWidget(self.replace_button)
        toolbar.addStretch(1)

        self.cover_label = QLabel("No cover loaded")
        self.cover_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cover_label.setMinimumSize(400, 400)

        self.status_label = QLabel("Load a track to view embedded cover art")

        layout = QVBoxLayout(self)
        layout.addLayout(toolbar)
        layout.addWidget(self.cover_label)
        layout.addWidget(self.status_label)
        layout.addStretch(1)

    def load_cover(self) -> None:
        track_id = self.track_id_box.value()
        self.current_track_id = track_id

        try:
            data = self.cover_service.extract_cover(track_id)
        except Exception as error:
            QMessageBox.warning(self, "Cover Load Failed", str(error))
            return

        if data is None:
            self.cover_label.setText("No embedded cover found")
            self.cover_label.setPixmap(QPixmap())
            self.status_label.setText(f"Track {track_id} has no embedded cover")
            self.replace_button.setEnabled(True)
            return

        pixmap = QPixmap()
        pixmap.loadFromData(data)
        scaled = pixmap.scaled(
            500,
            500,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.cover_label.setPixmap(scaled)
        self.status_label.setText(f"Loaded cover for track {track_id}")
        self.replace_button.setEnabled(True)

    def replace_cover(self) -> None:
        if self.current_track_id is None:
            QMessageBox.warning(self, "No Track Loaded", "Load a track first")
            return

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Choose Cover Image",
            "",
            "Images (*.jpg *.jpeg *.png)",
        )

        if not filename:
            return

        confirmation = QMessageBox.question(
            self,
            "Replace Cover",
            "Replace the embedded FLAC cover art for this track?",
        )

        if confirmation != QMessageBox.StandardButton.Yes:
            return

        try:
            self.cover_service.replace_cover(
                self.current_track_id,
                Path(filename),
            )
        except Exception as error:
            QMessageBox.warning(self, "Cover Replace Failed", str(error))
            return

        self.status_label.setText("Cover replaced")
        self.load_cover()
