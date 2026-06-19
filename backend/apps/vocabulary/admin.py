from django.contrib import admin

from .models import Word, WordProgress


class WordProgressInline(admin.StackedInline):
    model = WordProgress
    extra = 0
    can_delete = False


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ["english", "german", "chapter"]
    list_filter = ["chapter"]
    search_fields = ["english", "german"]
    inlines = [WordProgressInline]


@admin.register(WordProgress)
class WordProgressAdmin(admin.ModelAdmin):
    list_display = ["word", "repetitions", "interval", "next_review"]
    list_filter = ["next_review"]
