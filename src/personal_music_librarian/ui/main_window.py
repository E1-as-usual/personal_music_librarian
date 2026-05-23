from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QStackedWidget
from PySide6.QtWidgets import QToolBar

from personal_music_librarian.ui.pages.album_art_page import AlbumArtPage
from personal_music_librarian.ui.pages.albums_page import AlbumsPage
from personal_music_librarian.ui.pages.duplicates_page import DuplicatesPage
from personal_music_librarian.ui.pages.history_page import HistoryPage
from personal_music_librarian.ui.pages.library_page import LibraryPage
from personal_music_librarian.ui.pages.metadata_editor_page import MetadataEditorPage
from personal_music_librarian.ui.pages.rename_preview_page import RenamePreviewPage


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Personal Music Librarian")
        self.resize(1400, 900)

        self.library_page = LibraryPage()
        self.albums_page = AlbumsPage()
        self.duplicates_page = DuplicatesPage()
        self.rename_preview_page = RenamePreviewPage()
        self.history_page = HistoryPage()
        self.metadata_editor_page = MetadataEditorPage()
        self.album_art_page = AlbumArtPage()

        self.stack = QStackedWidget()
        self.stack.addWidget(self.library_page)
        self.stack.addWidget(self.albums_page)
        self.stack.addWidget(self.duplicates_page)
        self.stack.addWidget(self.rename_preview_page)
        self.stack.addWidget(self.history_page)
        self.stack.addWidget(self.metadata_editor_page)
        self.stack.addWidget(self.album_art_page)

        toolbar = QToolBar("Navigation")
        self.addToolBar(toolbar)

        library_action = toolbar.addAction("Library")
        library_action.triggered.connect(
            lambda: self.stack.setCurrentWidget(self.library_page)
        )

        albums_action = toolbar.addAction("Albums")
        albums_action.triggered.connect(
            lambda: self.stack.setCurrentWidget(self.albums_page)
        )

        duplicates_action = toolbar.addAction("Duplicates")
        duplicates_action.triggered.connect(
            lambda: self.stack.setCurrentWidget(self.duplicates_page)
        )

        rename_action = toolbar.addAction("Rename Preview")
        rename_action.triggered.connect(
            lambda: self.stack.setCurrentWidget(self.rename_preview_page)
        )

        history_action = toolbar.addAction("History")
        history_action.triggered.connect(
            lambda: self.stack.setCurrentWidget(self.history_page)
        )

        metadata_action = toolbar.addAction("Metadata")
        metadata_action.triggered.connect(
            lambda: self.stack.setCurrentWidget(self.metadata_editor_page)
        )

        album_art_action = toolbar.addAction("Album Art")
        album_art_action.triggered.connect(
            lambda: self.stack.setCurrentWidget(self.album_art_page)
        )

        self.setCentralWidget(self.stack)
