from personal_music_librarian.core.metadata.tags import REQUIRED_TAGS


class MetadataValidator:
    @staticmethod
    def missing_required(tags: dict[str, str | None]) -> list[str]:
        missing: list[str] = []

        for tag in REQUIRED_TAGS:
            value = tags.get(tag)
            if value is None or str(value).strip() == "":
                missing.append(tag)

        return missing

    @staticmethod
    def is_valid(tags: dict[str, str | None]) -> bool:
        return len(MetadataValidator.missing_required(tags)) == 0
