from django.contrib import admin

from .models import GrammarRule


@admin.register(GrammarRule)
class GrammarRuleAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "chapter"]
    list_filter = ["chapter", "category"]
    search_fields = ["title", "content"]
