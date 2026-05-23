from pathlib import Path

from personal_music_librarian.core.renamer.rename_plan import RenamePlan


class ConflictChecker:
    @staticmethod
    def check(plans: list[RenamePlan]) -> list[RenamePlan]:
        seen: set[Path] = set()

        for plan in plans:
            if plan.target_path in seen:
                plan.conflict = True
                plan.reason = 'Duplicate target path in rename plan'
                continue

            if plan.target_path.exists() and plan.target_path != plan.source_path:
                plan.conflict = True
                plan.reason = 'Target file already exists'
                continue

            seen.add(plan.target_path)

        return plans
