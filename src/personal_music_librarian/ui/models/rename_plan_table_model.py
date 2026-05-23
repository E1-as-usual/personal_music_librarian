from PySide6.QtCore import QAbstractTableModel
from PySide6.QtCore import QModelIndex
from PySide6.QtCore import Qt


COLUMNS = ["Current Path", "New Path", "Status"]


class RenamePlanTableModel(QAbstractTableModel):
    def __init__(self) -> None:
        super().__init__()
        self._plans = []

    def set_plans(self, plans) -> None:
        self.beginResetModel()
        self._plans = list(plans)
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self._plans)

    def columnCount(self, parent=QModelIndex()) -> int:
        return 0 if parent.isValid() else len(COLUMNS)

    def data(self, index: QModelIndex, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None

        plan = self._plans[index.row()]
        column = index.column()

        if column == 0:
            return str(plan.source_path)
        if column == 1:
            return str(plan.target_path)
        if column == 2:
            if plan.conflict:
                return f"Conflict: {plan.reason}"
            return "Ready"

        return None

    def headerData(self, section: int, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole:
            return None

        if orientation == Qt.Orientation.Horizontal:
            return COLUMNS[section]

        return section + 1
