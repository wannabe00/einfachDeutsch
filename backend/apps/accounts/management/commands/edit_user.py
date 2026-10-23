"""Change one existing user's level and/or premium, for testing.

    python manage.py edit_user tester --level A2
    python manage.py edit_user tester --premium on
    python manage.py edit_user tester --premium off
    python manage.py edit_user tester --level A1 --premium off
    python manage.py edit_user someone@example.com --level A2 --premium on

Progress is kept: switching back to a level shows what was already done there.
The app picks the change up on the next page load.
"""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q

from apps.accounts.levels import COURSE_LEVELS

VALID_LEVELS = list(COURSE_LEVELS)


class Command(BaseCommand):
    help = "Set a user's CEFR level and/or turn premium on or off."

    def add_arguments(self, parser):
        parser.add_argument("username", help="Username or e-mail.")
        parser.add_argument("--level", choices=VALID_LEVELS, type=str.upper)
        parser.add_argument("--premium", choices=["on", "off"])

    def handle(self, *args, username, level=None, premium=None, **options):
        if level is None and premium is None:
            raise CommandError("Pass --level and/or --premium.")
        users = get_user_model().objects.filter(Q(username=username) | Q(email__iexact=username))
        if users.count() > 1:
            raise CommandError(f"More than one user matches {username!r}; use the username.")
        user = users.first()
        if user is None:
            raise CommandError(f"No user called {username!r}.")

        profile = user.profile
        if level:
            profile.cefr_level = level
            profile.level_set = True
        if premium:
            # on = premium with no end date; off also ends any trial.
            profile.is_premium = premium == "on"
            profile.premium_until = None
        profile.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"{username}: level {profile.cefr_level}, premium "
                f"{'on' if profile.has_premium else 'off'}"
            )
        )
