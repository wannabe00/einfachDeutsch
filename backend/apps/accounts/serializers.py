from dj_rest_auth.serializers import UserDetailsSerializer as BaseUserDetailsSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    """Username + password login. Accounts are created via Google/GitHub OAuth;
    the password is set during onboarding so this fallback works too."""

    username = serializers.CharField()
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    def validate(self, attrs):
        invalid = serializers.ValidationError("Unable to log in with the provided credentials.")
        user = User.objects.filter(username__iexact=attrs["username"].strip()).first()
        if not user or not user.check_password(attrs["password"]):
            raise invalid
        if not user.is_active:
            raise serializers.ValidationError("This account is disabled.")
        attrs["user"] = user
        return attrs


class UserDetailsSerializer(BaseUserDetailsSerializer):
    """Profile fields surfaced on GET /api/auth/user/."""

    cefr_level = serializers.CharField(source="profile.cefr_level", read_only=True)
    role = serializers.CharField(source="profile.role", read_only=True)
    level_set = serializers.BooleanField(source="profile.level_set", read_only=True)
    profile_complete = serializers.BooleanField(source="profile.profile_complete", read_only=True)
    birthday = serializers.DateField(source="profile.birthday", read_only=True)
    avatar_url = serializers.URLField(source="profile.avatar_url", read_only=True)
    preferences = serializers.JSONField(source="profile.preferences", read_only=True)

    class Meta(BaseUserDetailsSerializer.Meta):
        fields = (
            *BaseUserDetailsSerializer.Meta.fields,
            "cefr_level",
            "role",
            "level_set",
            "profile_complete",
            "birthday",
            "avatar_url",
            "preferences",
        )
