import uuid

from dj_rest_auth.registration.serializers import (
    RegisterSerializer as BaseRegisterSerializer,
)
from dj_rest_auth.serializers import UserDetailsSerializer as BaseUserDetailsSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    """Email + password login (dj-rest-auth's default expects a username)."""

    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    def validate(self, attrs):
        invalid = serializers.ValidationError("Unable to log in with the provided credentials.")
        user = User.objects.filter(email__iexact=attrs["email"]).first()
        if not user or not user.check_password(attrs["password"]):
            raise invalid
        if not user.is_active:
            raise serializers.ValidationError("This account is disabled.")
        attrs["user"] = user
        return attrs


class RegisterSerializer(BaseRegisterSerializer):
    """Email + password only. The default User model still has a username column,
    so we auto-generate a unique value the user never sees."""

    username = None  # drop the username field from the API

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data["username"] = "u_" + uuid.uuid4().hex[:24]
        return data


class UserDetailsSerializer(BaseUserDetailsSerializer):
    """Adds the CEFR level to GET /api/auth/user/."""

    cefr_level = serializers.CharField(source="profile.cefr_level", read_only=True)

    class Meta(BaseUserDetailsSerializer.Meta):
        fields = (*BaseUserDetailsSerializer.Meta.fields, "cefr_level")
