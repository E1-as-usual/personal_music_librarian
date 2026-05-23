from PySide6.QtCore import QAbstractTableModel
from PySide6.QtCore import QModelIndex
from PySide6.QtCore import Qt


COLUMNS = [
    "Title",
    "Artist",
    "Album Artist",
    "Album",
    "Year",
    "Disc",
    "Track",
    "Duration",
    "Sample Rate",
    "Bit Depth",
    "Path",
]


class TrackTableModel(QAbstractTableModel):
    def __init__(self) -> None:
        super().__init__()
        self._rows: list[dict] = []

    def set_rows(self, rows) -> None:
        self.beginResetModel()
        self._rows = [dict(row) for row in rows]
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return len(self._rows)

    def columnCount(self, parent=QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return len(COLUMNS)

    def data(self, index: QModelIndex, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None

        row = self._rows[index.row()]
        column = index.column()

        if column == 0:
            return row.get("title") or ""
        if column == 1:
            return row.get("artist") or ""
        if column == 2:
            return row.get("albumartist") or ""
        if column == 3:
            return row.get("album") or ""
        if column == 4:
            return row.get("year") or ""
        if column == 5:
            return row.get("discnumber") or ""
        if column == 6:
            return row.get("tracknumber") or ""
        if column == 7:
            duration = row.get("duration")
            if duration is None:
                return ""
            minutes = int(duration) // 60
            seconds = int(duration) % 60
            return f"{minutes}:{seconds:02d}"
        if column == 8:
            return row.get("sample_rate") or ""
        if column == 9:
            return row.get("bit_depth") or ""
        if column == 10:
            return row.get("path") or ""

        return None

    def headerData(self, section: int, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole:
            return None

        if orientation == Qt.Orientation.Horizontal:
            return COLUMNS[section]

        return section + 1
