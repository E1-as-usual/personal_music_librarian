from PySide6.QtCore import QAbstractTableModel
from PySide6.QtCore import QModelIndex
from PySide6.QtCore import Qt


COLUMNS = [
    "Time",
    "Operation",
    "Item",
    "Status",
    "Message",
]


class HistoryTableModel(QAbstractTableModel):
    def __init__(self) -> None:
        super().__init__()
        self._rows = []

    def set_rows(self, rows) -> None:
        self.beginResetModel()
        self._rows = [dict(row) for row in rows]
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self._rows)

    def columnCount(self, parent=QModelIndex()) -> int:
        return 0 if parent.isValid() else len(COLUMNS)

    def data(self, index: QModelIndex, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None

        row = self._rows[index.row()]
        column = index.column()

        if column == 0:
            return row.get("timestamp") or ""
        if column == 1:
            return row.get("operation_type") or ""
        if column == 2:
            return row.get("item_type") or ""
        if column == 3:
            return row.get("status") or ""
        if column == 4:
            return row.get("message") or ""

        return None

    def headerData(self, section: int, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole:
            return None

        if orientation == Qt.Orientation.Horizontal:
            return COLUMNS[section]

        return section + 1
