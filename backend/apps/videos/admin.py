from django.contrib import admin

from .models import ShowSuggestion


@admin.register(ShowSuggestion)
class ShowSuggestionAdmin(admin.ModelAdmin):
    list_display = ("title", "cefr_level", "platform", "has_image")
    list_filter = ("cefr_level", "platform")
    search_fields = ("title", "description")

    @admin.display(boolean=True, description="Artwork")
    def has_image(self, obj) -> bool:
        """Blank is fine — the UI falls back to a generated platform tile."""
        return bool(obj.image_url)
