from django.contrib import admin, messages

from .images import find_image, queries_for
from .models import CustomHistoryLesson, HistoryLesson, UserHistoryProgress


@admin.action(description="Change picture (find another free one)")
def change_picture(modeladmin, request, queryset):
    """Search the free sources again, skipping the current picture."""
    changed = 0
    for lesson in queryset:
        url, credit = find_image(*queries_for(lesson), exclude={lesson.image_url})
        if url:
            lesson.image_url, lesson.image_credit = url, credit
            lesson.save(update_fields=["image_url", "image_credit"])
            changed += 1
    level = messages.SUCCESS if changed == len(queryset) else messages.WARNING
    modeladmin.message_user(request, f"New picture for {changed} of {len(queryset)}.", level)


@admin.register(HistoryLesson)
class HistoryLessonAdmin(admin.ModelAdmin):
    list_display = ("order", "title", "era", "cefr_level", "has_image")
    list_editable = ("title", "era", "cefr_level")
    list_filter = ("cefr_level", "era")
    ordering = ("order", "id")
    actions = [change_picture]

    @admin.display(boolean=True, description="Image")
    def has_image(self, obj) -> bool:
        """When blank the card draws an era tile instead."""
        return bool(obj.image_url)


@admin.register(CustomHistoryLesson)
class CustomHistoryLessonAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "cefr_level", "has_image", "created_at")
    list_filter = ("cefr_level",)
    search_fields = ("title", "topic")
    raw_id_fields = ("user",)
    actions = [change_picture]

    @admin.display(boolean=True, description="Image")
    def has_image(self, obj) -> bool:
        return bool(obj.image_url)


@admin.register(UserHistoryProgress)
class UserHistoryProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "lesson", "score", "completed_at")
    list_filter = ("completed_at",)
    raw_id_fields = ("user", "lesson")
