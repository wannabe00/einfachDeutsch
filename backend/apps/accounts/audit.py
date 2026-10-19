"""A log line for each security-relevant event (sign-ins, password and 2FA
changes, account removal), on the "security" logger: one place to look when
something seems wrong with an account. User ids, not names or e-mails."""

import logging

from rest_framework.throttling import AnonRateThrottle

log = logging.getLogger("security")


def audit(event: str, request=None, *, user=None, level=logging.INFO, **details) -> None:
    user = user or getattr(request, "user", None)
    user_id = user.pk if user is not None and user.is_authenticated else "-"
    # The same client address the rate limits use (NUM_PROXIES aware).
    ip = AnonRateThrottle().get_ident(request) if request is not None else "-"
    extra = "".join(f" {key}={value}" for key, value in details.items())
    log.log(level, "%s user=%s ip=%s%s", event, user_id, ip, extra)
