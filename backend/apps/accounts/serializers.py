from allauth.account.utils import user_pk_to_url_str
from dj_rest_auth.serializers import (
    PasswordResetConfirmSerializer as BasePasswordResetConfirmSerializer,
)
from dj_rest_auth.serializers import PasswordResetSerializer as BasePasswordResetSerializer
from dj_rest_auth.serializers import UserDetailsSerializer as BaseUserDetailsSerializer
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    """Username + password login. Accounts are created via Google/GitHub OAuth;
    the password is set during onboarding so this fallback works too."""

    username = serializers.CharField()
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    # The authenticator (or backup) code, once the password was right and the
    # account has two-factor login on. Asked for with a `code` error.
    code = serializers.CharField(required=False, allow_blank=True, write_only=True)

    def validate(self, attrs):
        from .views.twofactor import second_factor_ok

        invalid = serializers.ValidationError("Unable to log in with the provided credentials.")
        user = User.objects.filter(username__iexact=attrs["username"].strip()).first()
        if not user or not user.check_password(attrs["password"]):
            raise invalid
        if not user.is_active:
            raise serializers.ValidationError("This account is disabled.")
        profile = getattr(user, "profile", None)
        if profile and profile.totp_enabled:
            code = (attrs.get("code") or "").strip()
            if not code:
                raise serializers.ValidationError(
                    {"code": "Enter the 6-digit code from your authenticator app."}
                )
            if not second_factor_ok(profile, code):
                raise serializers.ValidationError({"code": "That code isn't right."})
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
    two_factor = serializers.BooleanField(source="profile.totp_enabled", read_only=True)
    # The UI should gate on `has_premium`: it combines the paid flag, an
    # active trial and the expiry date.
    has_premium = serializers.BooleanField(source="profile.has_premium", read_only=True)
    premium_until = serializers.DateTimeField(source="profile.premium_until", read_only=True)
    trial_started_at = serializers.DateTimeField(source="profile.trial_started_at", read_only=True)
    # Only hides the shared-content tools in the UI; the API checks it itself.
    is_staff = serializers.BooleanField(read_only=True)

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
            "two_factor",
            "has_premium",
            "premium_until",
            "trial_started_at",
            "is_staff",
        )


def frontend_reset_url(request, user, temp_key) -> str:
    """The link in the reset e-mail opens the app's reset page, not the API."""
    return f"{settings.FRONTEND_URL}/reset-password/{user_pk_to_url_str(user)}/{temp_key}"


class PasswordResetSerializer(BasePasswordResetSerializer):
    """Same as dj-rest-auth (no hint whether the e-mail exists), with the app's link."""

    def get_email_options(self):
        return {"url_generator": frontend_reset_url}


class PasswordResetConfirmSerializer(BasePasswordResetConfirmSerializer):
    """After a reset, sign the account out everywhere: whoever knew the old
    password may still hold a login token."""

    def save(self):
        from rest_framework.authtoken.models import Token

        super().save()
        Token.objects.filter(user=self.user).delete()
