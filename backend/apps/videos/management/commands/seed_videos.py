"""Load the curated video suggestions from `apps/videos/content.py`.

    python manage.py seed_videos

Safe to re-run: picks are matched on (title, level), updated in place, and
picks the content no longer lists are deleted.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.videos.content import VIDEOS
from apps.videos.models import ShowSuggestion

FIELDS = ("platform", "url", "description", "audience", "format", "cost", "tips", "image_url")


class Command(BaseCommand):
    help = "Load the curated video suggestions. Safe to re-run."

    @transaction.atomic
    def handle(self, *args, **options):
        keep = []
        for video in VIDEOS:
            obj, _ = ShowSuggestion.objects.update_or_create(
                title=video["title"],
                cefr_level=video["cefr_level"],
                defaults={field: video.get(field, "") for field in FIELDS},
            )
            keep.append(obj.id)
        removed, _ = ShowSuggestion.objects.exclude(id__in=keep).delete()
        self.stdout.write(self.style.SUCCESS(f"Videos: {len(keep)} loaded, {removed} removed."))
