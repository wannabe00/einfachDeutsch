"""Backfill part_of_speech for words that predate the field (Phase 23.9).

The Word Bank groups by part of speech, so rows created before the field must be
classified. Uses the same heuristic as `Word.save`; it's a guess and is
correctable in the admin. Reversible as a no-op (the column is simply dropped by
the preceding migration on unapply).
"""

from django.db import migrations

from apps.vocabulary.pos import guess_part_of_speech

BATCH = 500


def backfill(apps, schema_editor):
    Word = apps.get_model("vocabulary", "Word")
    # Historical models have no custom save(), so classify explicitly.
    pending = []
    for word in Word.objects.filter(part_of_speech="").iterator():
        word.part_of_speech = guess_part_of_speech(word.german)
        pending.append(word)
        if len(pending) >= BATCH:
            Word.objects.bulk_update(pending, ["part_of_speech"])
            pending.clear()
    if pending:
        Word.objects.bulk_update(pending, ["part_of_speech"])


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [("vocabulary", "0006_word_part_of_speech")]

    operations = [migrations.RunPython(backfill, noop)]
