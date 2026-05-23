from dataclasses import dataclass


@dataclass(slots=True)
class Track:
    id: int | None
    file_id: int
    title: str | None
    artist: str | None
    albumartist: str | None
    album: str | None
    date: str | None
    year: int | None
    genre: str | None
    tracknumber: int | None
    totaltracks: int | None
    discnumber: int | None
    totaldiscs: int | None
    duration: float | None
    sample_rate: int | None
    bit_depth: int | None
    channels: int | None
