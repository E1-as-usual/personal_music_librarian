from dataclasses import dataclass


@dataclass(slots=True)
class OperationLog:
    id: int | None
    operation_type: str
    timestamp: str
    item_type: str
    item_id: int | None
    old_value_json: str | None
    new_value_json: str | None
    status: str
    message: str | None
