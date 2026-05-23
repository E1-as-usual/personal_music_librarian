from pathlib import Path

from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QListWidget
from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QTextEdit
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from personal_music_librarian.config.paths import AppPaths
from personal_music_librarian.core.database.db import Database
from personal_music_librarian.core.database.repositories.duplicate_repo import DuplicateRepository
from personal_music_librarian.core.services.duplicate_action_service import DuplicateActionService


class DuplicatesPage(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.database = Database()
        self.database.initialize()
        self.action_service = DuplicateActionService(self.database)

        self.hashes: list[str] = []
        self.current_tracks = []

        self.refresh_button = QPushButton("Refresh Exact Duplicates")
        self.refresh_button.clicked.connect(self.load_duplicates)

        self.move_button = QPushButton("Move Non-Keepers")
        self.move_button.clicked.connect(self.move_non_keepers)
        self.move_button.setEnabled(False)

        self.summary_label = QLabel("No duplicate scan loaded")

        self.group_list = QListWidget()
        self.group_list.currentRowChanged.connect(self.show_group)

        self.keeper_combo = QComboBox()

        self.detail_box = QTextEdit()
        self.detail_box.setReadOnly(True)

        toolbar = QHBoxLayout()
        toolbar.addWidget(self.refresh_button)
        toolbar.addWidget(self.move_button)
        toolbar.addWidget(QLabel("Keeper:"))
        toolbar.addWidget(self.keeper_combo)
        toolbar.addWidget(self.summary_label)
        toolbar.addStretch(1)

        content = QHBoxLayout()
        content.addWidget(self.group_list, 1)
        content.addWidget(self.detail_box, 2)

        layout = QVBoxLayout(self)
        layout.addLayout(toolbar)
        layout.addLayout(content)

        self.load_duplicates()

    def load_duplicates(self) -> None:
        self.group_list.clear()
        self.detail_box.clear()
        self.keeper_combo.clear()
        self.hashes = []
        self.current_tracks = []
        self.move_button.setEnabled(False)

        with self.database.connection() as connection:
            repo = DuplicateRepository(connection)
            groups = repo.find_exact_duplicates()

        for group in groups:
            file_hash = group["file_hash"]
            count = group["duplicate_count"]
            self.hashes.append(file_hash)
            item = QListWidgetItem(f"{count} files | {file_hash[:16]}")
            self.group_list.addItem(item)

        self.summary_label.setText(f"{len(groups)} exact duplicate groups")

        if groups:
            self.group_list.setCurrentRow(0)

    def show_group(self, row: int) -> None:
        self.keeper_combo.clear()
        self.current_tracks = []

        if row < 0 or row >= len(self.hashes):
            self.detail_box.clear()
            self.move_button.setEnabled(False)
            return

        file_hash = self.hashes[row]

        with self.database.connection() as connection:
            repo = DuplicateRepository(connection)
            tracks = repo.get_duplicate_tracks(file_hash)

        self.current_tracks = tracks

        lines = [f"Exact duplicate hash: {file_hash}", ""]

        for index, track in enumerate(tracks, start=1):
            label = (
                f"{track['artist'] or 'Unknown'} - "
                f"{track['title'] or 'Unknown'}"
            )
            self.keeper_combo.addItem(label, track["id"])

            lines.extend(
                [
                    f"{index}. {track['title'] or 'Unknown Title'}",
                    f"   Artist: {track['artist'] or 'Unknown Artist'}",
                    f"   Album: {track['album'] or 'Unknown Album'}",
                    f"   Track: {track['tracknumber'] or ''}",
                    f"   Size: {track['size_bytes'] or 0} bytes",
                    f"   Path: {track['path']}",
                    "",
                ]
            )

        self.move_button.setEnabled(len(tracks) > 1)
        self.detail_box.setPlainText("\n".join(lines))

    def move_non_keepers(self) -> None:
        row = self.group_list.currentRow()

        if row < 0 or row >= len(self.hashes):
            return

        confirmation = QMessageBox.question(
            self,
            "Move Duplicates",
            "Move all non-keeper files to the review folder?",
        )

        if confirmation != QMessageBox.StandardButton.Yes:
            return

        file_hash = self.hashes[row]
        keeper_track_id = self.keeper_combo.currentData()

        review_root = (
            AppPaths.resolve().data_dir / "_Duplicates_Review"
        )

        result = self.action_service.move_non_keepers_to_review(
            file_hash=file_hash,
            keeper_track_id=int(keeper_track_id),
            review_root=review_root,
        )

        QMessageBox.information(
            self,
            "Duplicate Action Complete",
            (
                f"Moved: {result['moved']}\n"
                f"Skipped: {result['skipped']}\n"
                f"Failed: {result['failed']}"
            ),
        )

        self.load_duplicates()
