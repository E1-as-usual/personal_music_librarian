from dataclasses import dataclass
from pathlib import Path
import os
import platform


APP_DIR_NAME = "FLACLibraryManager"


@dataclass(slots=True)
class AppPaths:
    data_dir: Path
    config_dir: Path
    log_dir: Path
    export_dir: Path

    @classmethod
    def resolve(cls) -> "AppPaths":
        system = platform.system().lower()

        if system == "windows":
            base = Path(os.environ.get("APPDATA", Path.home()))
            data_dir = base / APP_DIR_NAME
        elif system == "darwin":
            data_dir = (
                Path.home()
                / "Library"
                / "Application Support"
                / APP_DIR_NAME
            )
        else:
            base = Path(
                os.environ.get(
                    "XDG_DATA_HOME",
                    Path.home() / ".local" / "share",
                )
            )
            data_dir = base / APP_DIR_NAME

        config_dir = data_dir
        log_dir = data_dir / "logs"
        export_dir = data_dir / "exports"

        for path in [data_dir, config_dir, log_dir, export_dir]:
            path.mkdir(parents=True, exist_ok=True)

        return cls(
            data_dir=data_dir,
            config_dir=config_dir,
            log_dir=log_dir,
            export_dir=export_dir,
        )
