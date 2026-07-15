from rest_framework import serializers

from .models import ShowSuggestion


class ShowSuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowSuggestion
        fields = ["id", "title", "description", "url", "platform", "cefr_level", "image_url"]
