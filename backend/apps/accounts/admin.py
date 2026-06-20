from django.contrib import admin

from .models import LevelDefinition, UserLessonProgress, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "cefr_level", "role", "level_set", "created_at")
    list_filter = ("cefr_level", "role", "level_set")


@admin.register(LevelDefinition)
class LevelDefinitionAdmin(admin.ModelAdmin):
    list_display = ("cefr_level", "order", "required_lessons", "required_reviews")
    ordering = ("order",)


@admin.register(UserLessonProgress)
class UserLessonProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "chapter", "score", "completed_at")
    list_filter = ("completed_at",)
    raw_id_fields = ("user", "chapter")
