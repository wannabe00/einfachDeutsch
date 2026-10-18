"""Create (or reset) a ready-to-use username/password account.

Accounts are normally created through Google or GitHub, which usually isn't set
up on localhost. This command creates a user with onboarding already done
(profile_complete and level_set), so you can log in at `/login` and go straight
into the app. Re-running updates the same user.

    python manage.py create_dev_user
    python manage.py create_dev_user --username tester --password hunter2 --level A2
    python manage.py create_dev_user --superuser        # also gets Django admin
    python manage.py create_dev_user --premium          # premium with no end date

Against production, always pass your own --password.
"""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.accounts.models import CEFR_LEVELS

User = get_user_model()

VALID_LEVELS = {code for code, _ in CEFR_LEVELS}


class Command(BaseCommand):
    help = "Create/reset a local dev account (username+password, onboarding done)."

    def add_arguments(self, parser):
        parser.add_argument("--username", default="dev")
        parser.add_argument("--password", default="dev12345")
        parser.add_argument("--email", default="dev@example.com")
        parser.add_argument(
            "--level",
            default="B1",
            help=f"CEFR level to start at (one of {', '.join(sorted(VALID_LEVELS))}). Default B1.",
        )
        parser.add_argument(
            "--superuser",
            action="store_true",
            help="Also grant staff + superuser (Django admin access).",
        )
        parser.add_argument(
            "--premium",
            action="store_true",
            help="Grant premium with no end date (unlimited energy, AI, Talk to AI).",
        )

    def handle(self, *args, **options):
        username = options["username"]
        password = options["password"]
        level = options["level"].upper()

        if level not in VALID_LEVELS:
            self.stderr.write(
                self.style.ERROR(f"Invalid level {level!r}. Choose one of {sorted(VALID_LEVELS)}.")
            )
            return

        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": options["email"], "first_name": username.capitalize()},
        )
        user.email = options["email"]
        user.set_password(password)
        if options["superuser"]:
            user.is_staff = True
            user.is_superuser = True
        user.save()

        # The post_save signal already created the profile; complete onboarding so
        # the app doesn't bounce us to /welcome or /onboarding.
        profile = user.profile
        profile.cefr_level = level
        profile.profile_complete = True
        profile.level_set = True
        if options["premium"]:
            profile.is_premium = True
            profile.premium_until = None  # no end date = premium until revoked
        profile.save()

        action = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"{action} dev account:"))
        self.stdout.write(f"  username: {username}")
        self.stdout.write(f"  password: {password}")
        self.stdout.write(f"  level:    {level}")
        if options["superuser"]:
            self.stdout.write("  admin:    yes (/admin)")
        if options["premium"]:
            self.stdout.write("  premium:  yes")
        self.stdout.write("Log in at /login (username + password).")
