from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


class ExpiringTokenAuthentication(TokenAuthentication):
    """DRF's plain tokens never expire — a stolen token works forever. This
    subclass rejects (and deletes) tokens older than TOKEN_TTL_DAYS, forcing a
    fresh login. The frontend's 401 interceptor already bounces expired
    sessions to the login page."""

    def authenticate_credentials(self, key):
        user, token = super().authenticate_credentials(key)
        max_age = timedelta(days=settings.TOKEN_TTL_DAYS)
        if timezone.now() - token.created > max_age:
            token.delete()
            raise AuthenticationFailed("Session expired. Please log in again.")
        return user, token
