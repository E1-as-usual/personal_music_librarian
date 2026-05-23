class LogRepository:
    def __init__(self, connection) -> None:
        self.connection = connection

    def write(
        self,
        operation_type: str,
        item_type: str,
        item_id: int | None,
        old_value_json: str | None,
        new_value_json: str | None,
        status: str,
        message: str | None,
    ) -> int:
        cursor = self.connection.execute(
            """
            INSERT INTO operation_logs (
                operation_type,
                timestamp,
                item_type,
                item_id,
                old_value_json,
                new_value_json,
                status,
                message
            ) VALUES (?, datetime('now'), ?, ?, ?, ?, ?, ?)
            """,
            (
                operation_type,
                item_type,
                item_id,
                old_value_json,
                new_value_json,
                status,
                message,
            ),
        )
        return int(cursor.lastrowid)

    def recent(self, limit: int = 100):
        cursor = self.connection.execute(
            """
            SELECT * FROM operation_logs
            ORDER BY timestamp DESC, id DESC
            LIMIT ?
            """,
            (limit,),
        )
        return cursor.fetchall()
