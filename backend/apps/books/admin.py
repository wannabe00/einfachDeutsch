from django.contrib import admin

from .models import Book, Chapter


class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 1


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "created_at"]
    search_fields = ["title"]
    inlines = [ChapterInline]


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ["number", "title", "book"]
    list_filter = ["book"]
    ordering = ["book", "number"]
