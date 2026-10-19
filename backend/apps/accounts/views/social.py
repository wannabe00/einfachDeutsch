"""Auth entry points: social login (Google/GitHub code exchange) and the
throttled username/password login."""

import logging
import smtplib

from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from dj_rest_auth.views import (
    LoginView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response

from ..throttles import LoginThrottle, PasswordChangeThrottle, PasswordResetThrottle


class ThrottledLoginView(LoginView):
    """Username/password login with a strict per-IP throttle. The global
    anonymous rate is far too generous for password guessing."""

    throttle_classes = [LoginThrottle]


class ThrottledPasswordChangeView(PasswordChangeView):
    """Change password; needs the current one (OLD_PASSWORD_FIELD_ENABLED)."""

    throttle_classes = [PasswordChangeThrottle]


class ThrottledPasswordResetView(PasswordResetView):
    """Send the reset e-mail, at most a few times per hour per IP. If the mail
    server fails (bad login, blocked port), answer with a clear 503 instead of
    a crash, and log the real error for the server logs."""

    throttle_classes = [PasswordResetThrottle]

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except (smtplib.SMTPException, OSError):
            logging.getLogger(__name__).exception("Password reset e-mail could not be sent")
            return Response(
                {"detail": "We couldn't send the e-mail right now. Please try again later."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


class ThrottledPasswordResetConfirmView(PasswordResetConfirmView):
    """Set the new password from the e-mail link, throttled the same way."""

    throttle_classes = [PasswordResetThrottle]


class GoogleLogin(SocialLoginView):
    """Exchange a Google OAuth `code` (sent by the SPA callback) for a DRF token.
    Creates the account on first sign-in (profile_complete stays False until
    onboarding)."""

    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = f"{settings.FRONTEND_URL.rstrip('/')}/auth/callback/google"
    throttle_classes = [LoginThrottle]


class GitHubLogin(SocialLoginView):
    """Exchange a GitHub OAuth `code` for a DRF token (same flow as Google)."""

    adapter_class = GitHubOAuth2Adapter
    client_class = OAuth2Client
    callback_url = f"{settings.FRONTEND_URL.rstrip('/')}/auth/callback/github"
    throttle_classes = [LoginThrottle]
