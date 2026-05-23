from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget


class MetadataEditorPage(QWidget):
    def __init__(self) -> None:
        super().__init__()

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Metadata Editor"))
        layout.addWidget(QLabel("Track editing workflow coming next."))
        layout.addStretch(1)
