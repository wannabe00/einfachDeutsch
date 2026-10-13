from django.db import models

CEFR_CHOICES = [(lvl, lvl) for lvl in ("A1", "A2", "B1", "B2", "C1", "C2")]


class ShowSuggestion(models.Model):
    """A hand-curated watch/listen suggestion tagged by CEFR level.

    Shared/global content (no per-user FK), written in `videos/content.py` and
    loaded with `manage.py seed_videos`. Surfaced to users once they unlock
    video suggestions.
    """

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)  # what it is
    audience = models.CharField(max_length=200, blank=True)  # who it's for
    format = models.CharField(max_length=160, blank=True)  # e.g. "10-20 min, weekly"
    cost = models.CharField(max_length=80, blank=True)  # e.g. "Free"
    tips = models.JSONField(default=list, blank=True)  # how to learn with it
    url = models.URLField()
    platform = models.CharField(max_length=60, blank=True)  # e.g. YouTube, DW, ARD
    cefr_level = models.CharField(max_length=2, choices=CEFR_CHOICES)
    # Optional artwork for the card; when blank the UI draws a platform tile.
    # YouTube picks use a video thumbnail from i.ytimg.com (allowed by the
    # production CSP, as are 'self', data:, Unsplash and Cloudinary).
    image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # CEFR codes sort correctly as plain strings (A1 < A2 < B1 < … < C2).
        ordering = ["cefr_level", "title"]

    def __str__(self):
        return f"[{self.cefr_level}] {self.title}"
