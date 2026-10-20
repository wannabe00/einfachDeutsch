"""Load the German-history lessons from `apps/history/content.py`.

    python manage.py seed_history

Safe to re-run: lessons are matched on `order`, updated in place, and lessons
the content no longer lists are deleted. Pictures are served by the frontend
from `public/history/`.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.history.content import LESSONS
from apps.history.models import HistoryLesson


class Command(BaseCommand):
    help = "Load the German-history lessons. Safe to re-run."

    @transaction.atomic
    def handle(self, *args, **options):
        for lesson in LESSONS:
            picture = {}
            if lesson.get("image"):
                picture = {
                    "image_url": f"/history/{lesson['image']}.jpg",
                    "image_credit": lesson["image_credit"],
                }
            # Without a bundled picture, keep the one backfill_history_images found.
            HistoryLesson.objects.update_or_create(
                order=lesson["order"],
                defaults={
                    **picture,
                    "cefr_level": lesson["level"],
                    "era": lesson["era"],
                    "title": lesson["title"],
                    "excerpt": lesson["excerpt"],
                    "body_de": lesson["body_de"].strip(),
                    "body_en": lesson["body_en"].strip(),
                    "quiz": lesson["quiz"],
                },
            )
        orders = [lesson["order"] for lesson in LESSONS]
        removed, _ = HistoryLesson.objects.exclude(order__in=orders).delete()
        self.stdout.write(
            self.style.SUCCESS(f"History: {len(LESSONS)} lessons loaded, {removed} removed.")
        )
