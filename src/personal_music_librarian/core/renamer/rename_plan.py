from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class RenamePlan:
    source_path: Path
    target_path: Path
    conflict: bool = False
    reason: str | None = None
