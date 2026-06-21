from django.db import migrations

# title, cefr_level, platform, url, description
SUGGESTIONS = [
    ("Nico's Weg – A1", "A1", "DW", "https://learngerman.dw.com/en/nicos-weg/c-36519789",
     "Free video drama course for absolute beginners."),
    ("Easy German", "A1", "YouTube", "https://www.youtube.com/@EasyGerman",
     "Street interviews with subtitles — start with the Super Easy episodes."),
    ("DW Learn German", "A1", "YouTube", "https://www.youtube.com/@dwlearngerman",
     "Bite-size lessons and series from Deutsche Welle."),
    ("Logo! – Kindernachrichten", "A2", "ZDF", "https://www.zdf.de/kinder/logo",
     "Slow, clear daily news made for kids — great listening at A2."),
    ("Dinge Erklärt – Kurzgesagt", "A2", "YouTube", "https://www.youtube.com/@dingeerklart",
     "Animated explainers in clear German (turn on subtitles)."),
    ("Nico's Weg – A2", "A2", "DW", "https://learngerman.dw.com/en/nicos-weg/c-36519789",
     "Continue the Nico's Weg story at the A2 level."),
    ("Easy German Podcast", "B1", "YouTube", "https://www.youtube.com/@EasyGerman",
     "Conversational podcast at a natural pace, with transcripts."),
    ("Deutschland-Labor", "B1", "DW", "https://learngerman.dw.com",
     "Short documentary clips about everyday life in Germany."),
    ("Nico's Weg – B1", "B1", "DW", "https://learngerman.dw.com/en/nicos-weg/c-36519789",
     "The B1 chapter of the Nico's Weg course."),
    ("Tagesschau", "B2", "ARD", "https://www.tagesschau.de",
     "Germany's main daily news — authentic, fast listening."),
    ("Dark", "B2", "Netflix", "https://www.netflix.com/title/80100172",
     "Gripping German sci-fi thriller (use German audio + subtitles)."),
    ("Y-Kollektiv", "B2", "YouTube", "https://www.youtube.com/@ykollektiv",
     "Immersive documentary reportage on real-world topics."),
    ("heute-show", "C1", "ZDF", "https://www.zdf.de/comedy/heute-show",
     "Satirical weekly news — fast, idiomatic German."),
    ("Tatort", "C1", "ARD", "https://www.ardmediathek.de",
     "Long-running crime series with rich, natural dialogue."),
]


def seed(apps, schema_editor):
    ShowSuggestion = apps.get_model("videos", "ShowSuggestion")
    for title, level, platform, url, desc in SUGGESTIONS:
        ShowSuggestion.objects.update_or_create(
            title=title,
            defaults={
                "cefr_level": level,
                "platform": platform,
                "url": url,
                "description": desc,
            },
        )


def unseed(apps, schema_editor):
    ShowSuggestion = apps.get_model("videos", "ShowSuggestion")
    ShowSuggestion.objects.filter(title__in=[s[0] for s in SUGGESTIONS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("videos", "0001_initial"),
    ]

    operations = [migrations.RunPython(seed, unseed)]
