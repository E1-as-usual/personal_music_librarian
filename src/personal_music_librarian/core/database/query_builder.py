from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class WhereClause:
    sql: str
    params: tuple[Any, ...]


class QueryBuilder:
    def __init__(self) -> None:
        self._clauses: list[str] = []
        self._params: list[Any] = []

    def equals(self, column: str, value: Any | None) -> "QueryBuilder":
        if value is not None:
            self._clauses.append(f"{column} = ?")
            self._params.append(value)
        return self

    def like(self, column: str, value: str | None) -> "QueryBuilder":
        if value:
            self._clauses.append(f"{column} LIKE ?")
            self._params.append(f"%{value}%")
        return self

    def is_null_or_empty(self, column: str, enabled: bool) -> "QueryBuilder":
        if enabled:
            self._clauses.append(f"({column} IS NULL OR {column} = '')")
        return self

    def build(self) -> WhereClause:
        if not self._clauses:
            return WhereClause(sql="", params=())

        return WhereClause(
            sql="WHERE " + " AND ".join(self._clauses),
            params=tuple(self._params),
        )
