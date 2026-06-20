from django.contrib import admin

from .models import RecitationAttempt


@admin.register(RecitationAttempt)
class RecitationAttemptAdmin(admin.ModelAdmin):
    list_display = ("user", "coverage_score", "created_at")
    list_filter = ("created_at",)
    raw_id_fields = ("user",)
    readonly_fields = (
        "user",
        "source_text",
        "transcript",
        "coverage_score",
        "feedback",
        "created_at",
    )
