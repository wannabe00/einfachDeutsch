from django.core.management import call_command
from django.db import migrations


def create_cache_table(apps, schema_editor):
    # The database cache (settings.CACHES) needs its table; this runs with
    # `migrate`, so no deploy needs an extra step. Safe to run again.
    call_command("createcachetable", verbosity=0)


class Migration(migrations.Migration):
    dependencies = [("accounts", "0011_two_factor")]

    operations = [migrations.RunPython(create_cache_table, migrations.RunPython.noop)]
