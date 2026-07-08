"""Auth entry points: social login (Google/GitHub code exchange) and the
throttled username/password login."""

from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from dj_rest_auth.views import LoginView
from django.conf import settings

from ..throttles import LoginThrottle


class CompatOAuth2Client(OAuth2Client):
    """dj-rest-auth 7.x passes `scope` positionally to OAuth2Client, but
    allauth 65.x removed that parameter. Absorb the extra positional arg to
    avoid `TypeError: got multiple values for argument 'scope_delimiter'`."""

    def __init__(
        self,
        request,
        consumer_key,
        consumer_secret,
        access_token_method,
        access_token_url,
        callback_url,
        scope,
        scope_delimiter=" ",
        headers=None,
        basic_auth=False,
    ):
        super().__init__(
            request,
            consumer_key,
            consumer_secret,
            access_token_method,
            access_token_url,
            callback_url,
            scope_delimiter,
            headers,
            basic_auth,
        )


class ThrottledLoginView(LoginView):
    """Username/password login with a strict per-IP throttle (S3 — the global
    anon rate is far too generous for password guessing)."""

    throttle_classes = [LoginThrottle]


class GoogleLogin(SocialLoginView):
    """Exchange a Google OAuth `code` (sent by the SPA callback) for a DRF token.
    Creates the account on first sign-in (profile_complete stays False until
    onboarding)."""

    adapter_class = GoogleOAuth2Adapter
    client_class = CompatOAuth2Client
    callback_url = f"{settings.FRONTEND_URL.rstrip('/')}/auth/callback/google"
    throttle_classes = [LoginThrottle]


class GitHubLogin(SocialLoginView):
    """Exchange a GitHub OAuth `code` for a DRF token (same flow as Google)."""

    adapter_class = GitHubOAuth2Adapter
    client_class = CompatOAuth2Client
    callback_url = f"{settings.FRONTEND_URL.rstrip('/')}/auth/callback/github"
    throttle_classes = [LoginThrottle]
