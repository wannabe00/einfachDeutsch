from django.db import migrations

# cefr, order, required_lessons, required_reviews, description
LEVELS = [
    ("A1", 1, 10, 150, "Beginner — basic phrases and everyday expressions."),
    ("A2", 2, 12, 300, "Elementary — simple, routine exchanges."),
    ("B1", 3, 14, 500, "Intermediate — handle most travel/work situations."),
    ("B2", 4, 16, 800, "Upper-intermediate — fluent, spontaneous interaction."),
    ("C1", 5, 18, 1200, "Advanced — flexible, effective language use."),
    ("C2", 6, 0, 0, "Mastery — top level."),
]


def seed(apps, schema_editor):
    LevelDefinition = apps.get_model("accounts", "LevelDefinition")
    for cefr, order, lessons, reviews, desc in LEVELS:
        LevelDefinition.objects.update_or_create(
            cefr_level=cefr,
            defaults={
                "order": order,
                "required_lessons": lessons,
                "required_reviews": reviews,
                "description": desc,
            },
        )


def unseed(apps, schema_editor):
    LevelDefinition = apps.get_model("accounts", "LevelDefinition")
    LevelDefinition.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0003_leveldefinition_userlessonprogress"),
    ]

    operations = [migrations.RunPython(seed, unseed)]
