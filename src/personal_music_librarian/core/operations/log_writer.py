from personal_music_librarian.core.models.operation_log import OperationLog


class LogWriter:
    def __init__(self, connection) -> None:
        self.connection = connection

    def write(self, log: OperationLog) -> int:
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
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                log.operation_type,
                log.timestamp,
                log.item_type,
                log.item_id,
                log.old_value_json,
                log.new_value_json,
                log.status,
                log.message,
            ),
        )

        return int(cursor.lastrowid)
