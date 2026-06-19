from django.contrib import admin

from .models import Word, WordProgress


class WordProgressInline(admin.TabularInline):
    model = WordProgress
    extra = 0
    can_delete = False
    fields = ["user", "repetitions", "interval", "next_review", "last_reviewed"]
    readonly_fields = ["user"]


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ["english", "german", "chapter"]
    list_filter = ["chapter"]
    search_fields = ["english", "german"]
    inlines = [WordProgressInline]


@admin.register(WordProgress)
class WordProgressAdmin(admin.ModelAdmin):
    list_display = ["word", "user", "repetitions", "interval", "next_review"]
    list_filter = ["next_review", "user"]
    raw_id_fields = ["word", "user"]
