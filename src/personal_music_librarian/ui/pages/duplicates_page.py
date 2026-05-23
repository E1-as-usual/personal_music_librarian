from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QListWidget
from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QTextEdit
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from personal_music_librarian.core.database.db import Database
from personal_music_librarian.core.database.repositories.duplicate_repo import DuplicateRepository


class DuplicatesPage(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.database = Database()
        self.database.initialize()
        self.hashes: list[str] = []

        self.refresh_button = QPushButton("Refresh Exact Duplicates")
        self.refresh_button.clicked.connect(self.load_duplicates)

        self.summary_label = QLabel("No duplicate scan loaded")

        self.group_list = QListWidget()
        self.group_list.currentRowChanged.connect(self.show_group)

        self.detail_box = QTextEdit()
        self.detail_box.setReadOnly(True)

        toolbar = QHBoxLayout()
        toolbar.addWidget(self.refresh_button)
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
        self.hashes = []

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
        if row < 0 or row >= len(self.hashes):
            self.detail_box.clear()
            return

        file_hash = self.hashes[row]

        with self.database.connection() as connection:
            repo = DuplicateRepository(connection)
            tracks = repo.get_duplicate_tracks(file_hash)

        lines = [f"Exact duplicate hash: {file_hash}", ""]

        for index, track in enumerate(tracks, start=1):
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

        self.detail_box.setPlainText("\n".join(lines))
