from django.db import models

from apps.accounts.levels import STARTER_LEVEL
from apps.accounts.models import CEFR_LEVELS


class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="chapters")
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # The chapter's CEFR level. Its words and grammar rules inherit it, so the
    # level rule is a single join. A chapter is one Lektion (one path Unit),
    # which is why the level lives here and not on each word.
    cefr_level = models.CharField(
        max_length=2, choices=[(STARTER_LEVEL, "Grundlagen"), *CEFR_LEVELS], default="A1"
    )

    class Meta:
        ordering = ["number"]
        unique_together = ["book", "number"]

    def __str__(self):
        return f"Chapter {self.number}: {self.title}"
