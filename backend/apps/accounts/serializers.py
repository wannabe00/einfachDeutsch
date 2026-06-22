from allauth.account.models import EmailAddress
from dj_rest_auth.registration.serializers import (
    RegisterSerializer as BaseRegisterSerializer,
)
from dj_rest_auth.serializers import UserDetailsSerializer as BaseUserDetailsSerializer
from django.conf import settings
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

        # Block unverified accounts only when verification is mandatory.
        # Superusers (created via the CLI) and legacy accounts with no email
        # record predate verification, so they're always exempt.
        mandatory = settings.ACCOUNT_EMAIL_VERIFICATION == "mandatory"
        if mandatory and not user.is_superuser:
            emails = EmailAddress.objects.filter(user=user)
            if emails.exists() and not emails.filter(verified=True).exists():
                raise serializers.ValidationError(
                    "Please verify your email address before logging in. "
                    "Check your inbox for the confirmation link."
                )

        attrs["user"] = user
        return attrs


class RegisterSerializer(BaseRegisterSerializer):
    """Email + password + profile fields. Username is user-chosen (unique);
    name/surname go on the auth User; birthday/phone go on the UserProfile."""

    username = serializers.CharField(max_length=150)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    birthday = serializers.DateField(required=False, allow_null=True)
    phone = serializers.CharField(max_length=32, required=False, allow_blank=True)

    def validate_username(self, value):
        value = value.strip()
        if len(value) < 3:
            raise serializers.ValidationError("Username must be at least 3 characters.")
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("That username is already taken.")
        return value

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data["username"] = self.validated_data.get("username", "")
        data["first_name"] = self.validated_data.get("first_name", "")
        data["last_name"] = self.validated_data.get("last_name", "")
        return data

    def custom_signup(self, request, user):
        user.first_name = self.validated_data.get("first_name", "")
        user.last_name = self.validated_data.get("last_name", "")
        user.save(update_fields=["first_name", "last_name"])
        profile = user.profile
        profile.birthday = self.validated_data.get("birthday")
        profile.phone = self.validated_data.get("phone", "")
        profile.save(update_fields=["birthday", "phone"])


class UserDetailsSerializer(BaseUserDetailsSerializer):
    """Profile fields surfaced on GET /api/auth/user/."""

    cefr_level = serializers.CharField(source="profile.cefr_level", read_only=True)
    role = serializers.CharField(source="profile.role", read_only=True)
    level_set = serializers.BooleanField(source="profile.level_set", read_only=True)
    birthday = serializers.DateField(source="profile.birthday", read_only=True)
    phone = serializers.CharField(source="profile.phone", read_only=True)
    avatar_url = serializers.URLField(source="profile.avatar_url", read_only=True)
    preferences = serializers.JSONField(source="profile.preferences", read_only=True)

    class Meta(BaseUserDetailsSerializer.Meta):
        fields = (
            *BaseUserDetailsSerializer.Meta.fields,
            "cefr_level",
            "role",
            "level_set",
            "birthday",
            "phone",
            "avatar_url",
            "preferences",
        )
