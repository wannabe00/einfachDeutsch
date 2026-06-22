"""Delete user accounts (and everything that cascades from them: profiles,
progress, tokens, email addresses). Superusers are kept by default so admin
access survives the wipe. Requires --yes to actually run.

    python manage.py wipe_users --yes                 # keep superusers
    python manage.py wipe_users --yes --include-superusers
"""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Delete all users (keeps superusers unless --include-superusers)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--yes",
            action="store_true",
            help="Confirm the deletion (without this, only a dry-run count is shown).",
        )
        parser.add_argument(
            "--include-superusers",
            action="store_true",
            help="Also delete superusers (default: keep them).",
        )

    def handle(self, *args, **options):
        qs = User.objects.all()
        if not options["include_superusers"]:
            qs = qs.filter(is_superuser=False)

        count = qs.count()
        if not options["yes"]:
            self.stdout.write(
                self.style.WARNING(
                    f"Dry run: {count} user(s) would be deleted. Re-run with --yes to proceed."
                )
            )
            return

        deleted, _ = qs.delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {count} user(s) (rows removed: {deleted})."))
