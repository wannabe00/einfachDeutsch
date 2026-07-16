from django.contrib import admin

from .models import HistoryLesson, UserHistoryProgress


@admin.register(HistoryLesson)
class HistoryLessonAdmin(admin.ModelAdmin):
    list_display = ("order", "title", "era", "cefr_level", "has_image")
    list_editable = ("title", "era", "cefr_level")
    list_filter = ("cefr_level", "era")
    ordering = ("order", "id")

    @admin.display(boolean=True, description="Image")
    def has_image(self, obj) -> bool:
        """Blank is fine — the card falls back to a drawn era tile."""
        return bool(obj.image_url)


@admin.register(UserHistoryProgress)
class UserHistoryProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "lesson", "score", "completed_at")
    list_filter = ("completed_at",)
    raw_id_fields = ("user", "lesson")
