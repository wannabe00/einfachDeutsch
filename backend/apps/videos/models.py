from django.db import models

CEFR_CHOICES = [(lvl, lvl) for lvl in ("A1", "A2", "B1", "B2", "C1", "C2")]


class ShowSuggestion(models.Model):
    """A hand-curated watch/listen suggestion tagged by CEFR level (Phase 17).

    Shared/global content (no per-user FK). Curated in the Django admin; not an
    external API. Surfaced to users once they unlock video suggestions.
    """

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    url = models.URLField()
    platform = models.CharField(max_length=60, blank=True)  # e.g. YouTube, DW, ARD
    cefr_level = models.CharField(max_length=2, choices=CEFR_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # CEFR codes sort correctly as plain strings (A1 < A2 < B1 < … < C2).
        ordering = ["cefr_level", "title"]

    def __str__(self):
        return f"[{self.cefr_level}] {self.title}"
