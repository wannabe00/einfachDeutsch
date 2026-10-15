"""Change one existing user's level and/or premium, for testing.

    python manage.py edit_user tester --level A2
    python manage.py edit_user tester --premium on
    python manage.py edit_user tester --premium off
    python manage.py edit_user tester --level A1 --premium off

Progress is kept: switching back to a level shows what was already done there.
The app picks the change up on the next page load.
"""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from apps.accounts.models import CEFR_LEVELS

VALID_LEVELS = sorted(code for code, _ in CEFR_LEVELS)


class Command(BaseCommand):
    help = "Set a user's CEFR level and/or turn premium on or off."

    def add_arguments(self, parser):
        parser.add_argument("username")
        parser.add_argument("--level", choices=VALID_LEVELS, type=str.upper)
        parser.add_argument("--premium", choices=["on", "off"])

    def handle(self, *args, username, level=None, premium=None, **options):
        if level is None and premium is None:
            raise CommandError("Pass --level and/or --premium.")
        user = get_user_model().objects.filter(username=username).first()
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
