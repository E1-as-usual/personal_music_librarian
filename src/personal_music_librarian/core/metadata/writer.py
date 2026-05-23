from pathlib import Path

from mutagen.flac import FLAC


class TagWriteError(Exception):
    pass


class TagWriter:
    @staticmethod
    def write_tags(path: Path, tags: dict[str, str | int | None]) -> None:
        try:
            audio = FLAC(path)

            for key, value in tags.items():
                if value is None:
                    continue

                text = str(value).strip()
                if text == "":
                    continue

                audio[key.upper()] = [text]

            audio.save()

        except Exception as error:
            raise TagWriteError(str(error)) from error
