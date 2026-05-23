class MetadataNormalizer:
    @staticmethod
    def normalize_text(value: str | None) -> str | None:
        if value is None:
            return None

        normalized = " ".join(value.strip().split())
        return normalized or None

    @staticmethod
    def normalize_number(value: str | int | None) -> int | None:
        if value is None:
            return None

        if isinstance(value, int):
            return value

        cleaned = value.split("/")[0].strip()
        if not cleaned.isdigit():
            return None

        return int(cleaned)

    @staticmethod
    def normalize_year(value: str | None) -> int | None:
        if not value:
            return None

        year = value[:4]
        if not year.isdigit():
            return None

        return int(year)
