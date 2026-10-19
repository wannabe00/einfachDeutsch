"""Settings from the security audit."""

from django.conf import settings
from django.test import SimpleTestCase


class AuditSettingsTests(SimpleTestCase):
    def test_reset_links_and_admin_sessions_are_short_lived(self):
        self.assertEqual(settings.PASSWORD_RESET_TIMEOUT, 3600)
        self.assertEqual(settings.SESSION_COOKIE_AGE, 8 * 3600)
