from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings


class AccountAdapter(DefaultAccountAdapter):
    """Point the email-confirmation link at the SPA instead of a Django page.

    The frontend route /verify-email/<key> POSTs the key to
    /api/auth/registration/verify-email/ to complete verification.
    """

    def get_email_confirmation_url(self, request, emailconfirmation):
        base = settings.FRONTEND_URL.rstrip("/")
        return f"{base}/verify-email/{emailconfirmation.key}"
