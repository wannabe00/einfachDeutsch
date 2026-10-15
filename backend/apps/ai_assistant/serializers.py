from rest_framework import serializers

from .models import AISettings, Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "role", "content", "created_at"]


class ConversationListSerializer(serializers.ModelSerializer):
    """Sidebar row: title + when it was last touched."""

    class Meta:
        model = Conversation
        fields = ["id", "title", "pinned", "mode", "created_at", "updated_at"]


class ConversationDetailSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ["id", "title", "pinned", "mode", "created_at", "updated_at", "messages"]


class AISettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AISettings
        fields = ["reply_language", "tone", "corrections", "interests", "about"]
