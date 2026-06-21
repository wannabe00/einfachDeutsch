from django.contrib import admin

from .models import ShowSuggestion


@admin.register(ShowSuggestion)
class ShowSuggestionAdmin(admin.ModelAdmin):
    list_display = ("title", "cefr_level", "platform")
    list_filter = ("cefr_level", "platform")
    search_fields = ("title", "description")
