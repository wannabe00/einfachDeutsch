from django.contrib import admin

from .models import AIUsage, Conversation, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ("role", "content", "created_at")


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "updated_at")
    search_fields = ("title", "user__username")
    raw_id_fields = ("user",)
    inlines = [MessageInline]


@admin.register(AIUsage)
class AIUsageAdmin(admin.ModelAdmin):
    """How much of each paid AI service the site used per day (read-only)."""

    list_display = ("day", "feature", "amount")
    list_filter = ("feature",)
    date_hierarchy = "day"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
