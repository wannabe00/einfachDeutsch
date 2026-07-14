from django.contrib import admin

from .models import EnergyState, Lesson, LessonItem, PathLessonProgress, Unit


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0


class LessonItemInline(admin.TabularInline):
    model = LessonItem
    extra = 0


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ("cefr_level", "order", "title", "theme")
    list_filter = ("cefr_level",)
    ordering = ("cefr_level", "order")
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "unit", "order", "xp_reward")
    list_filter = ("unit__cefr_level",)
    ordering = ("unit", "order")
    inlines = [LessonItemInline]


@admin.register(PathLessonProgress)
class PathLessonProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "lesson", "completed_at", "crown", "best_score")
    list_filter = ("crown",)
    search_fields = ("user__username",)


@admin.register(EnergyState)
class EnergyStateAdmin(admin.ModelAdmin):
    list_display = ("user", "balance", "last_refill_at")
    search_fields = ("user__username",)
