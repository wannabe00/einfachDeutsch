from django.contrib import admin

from .models import HistoryLesson, UserHistoryProgress


@admin.register(HistoryLesson)
class HistoryLessonAdmin(admin.ModelAdmin):
    list_display = ("order", "title", "era")
    list_editable = ("title", "era")
    ordering = ("order", "id")


@admin.register(UserHistoryProgress)
class UserHistoryProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "lesson", "score", "completed_at")
    list_filter = ("completed_at",)
    raw_id_fields = ("user", "lesson")
