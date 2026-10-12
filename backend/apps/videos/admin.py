from django.contrib import admin

from .models import ShowSuggestion


@admin.register(ShowSuggestion)
class ShowSuggestionAdmin(admin.ModelAdmin):
    list_display = ("title", "cefr_level", "platform", "has_image")
    list_filter = ("cefr_level", "platform")
    search_fields = ("title", "description")

    @admin.display(boolean=True, description="Artwork")
    def has_image(self, obj) -> bool:
        """Optional. When blank the UI draws a platform tile instead."""
        return bool(obj.image_url)
