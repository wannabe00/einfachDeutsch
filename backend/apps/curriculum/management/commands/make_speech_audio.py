"""Record the listening tasks' German once with Azure (`llm.speak_german`).

Covers the Grundlagen starter units (`hear` / `dictate` in content/a0.py). Each
missing text becomes frontend/public/speech/<hash>.mp3, then
content/speech_audio.json is rewritten so the lessons send the recording
instead of falling back to the browser's voice. The free tier is rate-limited,
so the command stops cleanly at the quota; run it again and it continues.

    manage.py make_speech_audio            # everything that's missing
    manage.py make_speech_audio --limit 3  # just a few, to listen first
"""

import json
import time

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.ai_assistant import llm
from apps.curriculum.content.levels import STARTER
from apps.curriculum.speech import MANIFEST, clip_name, spoken_text

AUDIO_DIR = settings.BASE_DIR.parent / "frontend" / "public" / "speech"
PAUSE = 3.5  # seconds between requests: the free tier allows about 20 a minute


def all_texts() -> list[str]:
    """Every text a starter lesson reads aloud, each once."""
    texts = []
    for u in STARTER["units"]:
        for les in u["lessons"]:
            for item in les["items"]:
                if item["kind"] != "exercise":
                    continue
                for part in item.get("parts", [item]):
                    if text := spoken_text(part):
                        texts.append(text)
    return list(dict.fromkeys(texts))


class Command(BaseCommand):
    help = "Record the starter units' listening tasks with Azure (free tier). Safe to re-run."

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, help="Record at most this many.")

    def handle(self, *args, limit=None, **options):
        AUDIO_DIR.mkdir(parents=True, exist_ok=True)
        texts = all_texts()
        missing = [t for t in texts if not (AUDIO_DIR / f"{clip_name(t)}.mp3").exists()]
        if limit is not None:
            missing = missing[:limit]
        self.stdout.write(f"{len(texts)} texts, recording {len(missing)}.")
        try:
            for i, text in enumerate(missing):
                if i:
                    time.sleep(PAUSE)
                (AUDIO_DIR / f"{clip_name(text)}.mp3").write_bytes(llm.speak_german(text))
                self.stdout.write(f"  {text}")
        except llm.AIQuotaError:
            self.stdout.write(self.style.WARNING("Quota reached: run again later to continue."))
        finally:
            done = sorted(
                clip_name(t) for t in texts if (AUDIO_DIR / f"{clip_name(t)}.mp3").exists()
            )
            MANIFEST.write_text(json.dumps(done, indent=1) + "\n")
            self.stdout.write(self.style.SUCCESS(f"{len(done)}/{len(texts)} recorded."))
