"""The course ends at B1: anyone set above it moves to B1, where content exists."""

from django.db import migrations


def cap(apps, schema_editor):
    UserProfile = apps.get_model("accounts", "UserProfile")
    UserProfile.objects.filter(cefr_level__in=["B2", "C1", "C2"]).update(cefr_level="B1")


class Migration(migrations.Migration):
    dependencies = [("accounts", "0013_stripe_ids")]

    operations = [migrations.RunPython(cap, migrations.RunPython.noop)]
