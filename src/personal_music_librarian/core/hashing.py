from pathlib import Path

from blake3 import blake3


CHUNK_SIZE = 1024 * 1024


class FileHasher:
    @staticmethod
    def hash_file(path: Path) -> str:
        hasher = blake3()

        with path.open("rb") as handle:
            while chunk := handle.read(CHUNK_SIZE):
                hasher.update(chunk)

        return hasher.hexdigest()
