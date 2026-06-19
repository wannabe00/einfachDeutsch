import uuid

from allauth.account.models import EmailAddress
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

        # Block unverified accounts. Superusers (created via the CLI) and legacy
        # accounts with no email record predate verification, so they're exempt.
        if not user.is_superuser:
            emails = EmailAddress.objects.filter(user=user)
            if emails.exists() and not emails.filter(verified=True).exists():
                raise serializers.ValidationError(
                    "Please verify your email address before logging in. "
                    "Check your inbox for the confirmation link."
                )

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
    """Adds profile fields (CEFR level, role, onboarding state) to
    GET /api/auth/user/."""

    cefr_level = serializers.CharField(source="profile.cefr_level", read_only=True)
    role = serializers.CharField(source="profile.role", read_only=True)
    level_set = serializers.BooleanField(source="profile.level_set", read_only=True)

    class Meta(BaseUserDetailsSerializer.Meta):
        fields = (
            *BaseUserDetailsSerializer.Meta.fields,
            "cefr_level",
            "role",
            "level_set",
        )
