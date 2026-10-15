"""Seed only the A1 path: the same as `seed_path --level A1`."""

from .seed_path import Command as SeedPath
from .seed_path import exercise_fields  # noqa: F401 (kept for older imports)


class Command(SeedPath):
    help = "Seed the A1 learning path (same as seed_path --level A1). Safe to re-run."

    def handle(self, *args, **options):
        options["level"] = ["A1"]
        super().handle(*args, **options)
