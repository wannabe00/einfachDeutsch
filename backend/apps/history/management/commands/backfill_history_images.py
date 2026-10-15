"""Give every history lesson without a picture one from the free sources.

    python manage.py backfill_history_images [--dry-run]

Covers the shared lessons and the ones the AI wrote for users. Safe to re-run:
lessons that already have a picture are left alone.
"""

from django.core.management.base import BaseCommand

from apps.history.images import find_image, queries_for
from apps.history.models import CustomHistoryLesson, HistoryLesson


class Command(BaseCommand):
    help = "Find a free picture for every history lesson that has none."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help="Search, but save nothing.")

    def handle(self, *args, dry_run=False, **options):
        found = missing = 0
        for model in (HistoryLesson, CustomHistoryLesson):
            for lesson in model.objects.filter(image_url=""):
                url, credit = find_image(*queries_for(lesson))
                if not url:
                    missing += 1
                    self.stdout.write(self.style.WARNING(f"No picture: {lesson.title}"))
                    continue
                found += 1
                self.stdout.write(f"{lesson.title}: {credit}")
                if not dry_run:
                    lesson.image_url, lesson.image_credit = url, credit
                    lesson.save(update_fields=["image_url", "image_credit"])
        self.stdout.write(self.style.SUCCESS(f"Pictures found: {found}, still without: {missing}."))
