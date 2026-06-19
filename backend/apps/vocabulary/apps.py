from django.apps import AppConfig


class VocabularyConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.vocabulary"
    label = "vocabulary"

    def ready(self):
        # Register signal handlers (post_save → auto-create WordProgress).
        from . import signals  # noqa: F401
