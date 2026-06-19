from django.db import models

from apps.books.models import Chapter


class GrammarRule(models.Model):
    CATEGORY_CHOICES = [
        ("articles", "Articles (der/die/das)"),
        ("cases", "Cases (Nominativ, Akkusativ, etc.)"),
        ("verbs", "Verbs & Conjugation"),
        ("sentence_structure", "Sentence Structure"),
        ("pronouns", "Pronouns"),
        ("adjectives", "Adjectives"),
        ("other", "Other"),
    ]

    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="grammar_rules")
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="other")
    content = models.TextField()  # Markdown supported
    example_sentences = models.TextField(blank=True)  # one per line
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
