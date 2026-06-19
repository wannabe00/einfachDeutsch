from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Word, WordProgress


@receiver(post_save, sender=Word)
def create_word_progress(sender, instance, created, **kwargs):
    """Auto-create the SM-2 progress row the first time a Word is saved."""
    if created:
        WordProgress.objects.create(word=instance)
