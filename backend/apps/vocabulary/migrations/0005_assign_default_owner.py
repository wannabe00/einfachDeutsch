from django.db import migrations


def assign_default_owner(apps, schema_editor):
    """Migrate the app's pre-existing single-user progress to a default owner.

    Before Phase 13.2 the app was single-user: WordProgress/ReviewLog/
    ExerciseAttempt had no user. We assign all such rows to the first user
    (the owner). If no user account exists yet (fresh DB), the orphaned rows are
    unreachable in the per-user model, so we drop them — shared content (Word,
    GrammarRule, Exercise, ...) is left untouched.
    """
    User = apps.get_model("auth", "User")
    WordProgress = apps.get_model("vocabulary", "WordProgress")
    ReviewLog = apps.get_model("vocabulary", "ReviewLog")
    ExerciseAttempt = apps.get_model("exercises", "ExerciseAttempt")

    owner = User.objects.order_by("id").first()
    if owner is None:
        WordProgress.objects.filter(user__isnull=True).delete()
        ReviewLog.objects.filter(user__isnull=True).delete()
        ExerciseAttempt.objects.filter(user__isnull=True).delete()
        return

    WordProgress.objects.filter(user__isnull=True).update(user=owner)
    ReviewLog.objects.filter(user__isnull=True).update(user=owner)
    ExerciseAttempt.objects.filter(user__isnull=True).update(user=owner)


class Migration(migrations.Migration):
    dependencies = [
        ("vocabulary", "0004_reviewlog_user_wordprogress_user_and_more"),
        ("exercises", "0003_exerciseattempt_user"),
    ]

    operations = [
        migrations.RunPython(assign_default_owner, migrations.RunPython.noop),
    ]
