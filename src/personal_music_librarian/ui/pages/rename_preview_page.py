from pathlib import Path

from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QTableView
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from personal_music_librarian.core.database.db import Database
from personal_music_librarian.core.database.repositories.track_repo import TrackRepository
from personal_music_librarian.core.renamer.conflict_checker import ConflictChecker
from personal_music_librarian.core.renamer.template_engine import TemplateEngine
from personal_music_librarian.core.renamer.templates import DEFAULT_TEMPLATES
from personal_music_librarian.core.services.rename_service import RenameService
from personal_music_librarian.ui.models.rename_plan_table_model import RenamePlanTableModel


class RenamePreviewPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.database = Database()
        self.database.initialize()
        self.rename_service = RenameService(self.database)

        self.destination_root: Path | None = None
        self.current_plans = []
        self.model = RenamePlanTableModel()

        self.template_box = QComboBox()
        for name in DEFAULT_TEMPLATES:
            self.template_box.addItem(name)

        self.pick_root_button = QPushButton("Choose Root")
        self.pick_root_button.clicked.connect(self.choose_root)

        self.generate_button = QPushButton("Generate Preview")
        self.generate_button.clicked.connect(self.generate_preview)

        self.apply_button = QPushButton("Apply Rename Plan")
        self.apply_button.clicked.connect(self.apply_plan)
        self.apply_button.setEnabled(False)

        self.summary_label = QLabel("No preview generated")

        toolbar = QHBoxLayout()
        toolbar.addWidget(QLabel("Template:"))
        toolbar.addWidget(self.template_box)
        toolbar.addWidget(self.pick_root_button)
        toolbar.addWidget(self.generate_button)
        toolbar.addWidget(self.apply_button)
        toolbar.addWidget(self.summary_label)
        toolbar.addStretch(1)

        self.table = QTableView()
        self.table.setModel(self.model)

        layout = QVBoxLayout(self)
        layout.addLayout(toolbar)
        layout.addWidget(self.table)

    def choose_root(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Choose Destination Root")
        if folder:
            self.destination_root = Path(folder)
            self.summary_label.setText(str(self.destination_root))

    def generate_preview(self) -> None:
        root = self.destination_root or Path.cwd()
        template = DEFAULT_TEMPLATES[self.template_box.currentText()]

        with self.database.connection() as connection:
            tracks = TrackRepository(connection).get_all()

        plans = [
            TemplateEngine.render(dict(track), template, root)
            for track in tracks
        ]
        plans = ConflictChecker.check(plans)

        self.current_plans = plans
        self.model.set_plans(plans)
        self.apply_button.setEnabled(bool(plans))

        conflicts = sum(1 for plan in plans if plan.conflict)
        self.summary_label.setText(
            f"{len(plans)} planned | {conflicts} conflicts"
        )

    def apply_plan(self) -> None:
        confirmation = QMessageBox.question(
            self,
            "Apply Rename Plan",
            "Apply all non-conflicting rename operations?",
        )

        if confirmation != QMessageBox.StandardButton.Yes:
            return

        result = self.rename_service.apply_plans(self.current_plans)

        QMessageBox.information(
            self,
            "Rename Complete",
            (
                f"Applied: {result['applied']}\n"
                f"Skipped: {result['skipped']}\n"
                f"Failed: {result['failed']}"
            ),
        )
