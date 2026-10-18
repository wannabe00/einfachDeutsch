from django.contrib import admin

from .models import Talk


@admin.register(Talk)
class TalkAdmin(admin.ModelAdmin):
    list_display = ("user", "level", "started_at", "ended_at", "removed_at")
    list_filter = ("level",)
    readonly_fields = ("transcript", "report")
