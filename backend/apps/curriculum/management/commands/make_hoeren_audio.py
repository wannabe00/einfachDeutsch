"""Generate the Hören recordings once from the scripts in content/<level>/hoeren.py.

Each missing clip is spoken by Gemini (`llm.synthesize_speech`), turned into a
64 kbit/s mono MP3 with the local ffmpeg, and saved to frontend/public/hoeren/.
The free API tier is rate-limited, so the command stops cleanly at the quota;
run it again later and it continues with the clips that are still missing.
It then rewrites content/hoeren_audio.json, which decides which sets go live.

    manage.py make_hoeren_audio                 # everything that's missing
    manage.py make_hoeren_audio --limit 3       # just a few, to listen first
    manage.py make_hoeren_audio --redo seed-a1-hoeren-m1-t1-0   # remake one
"""

import json
import re
import subprocess
import time

from django.conf import settings
from django.core.management.base import BaseCommand
from google.genai import errors

from apps.ai_assistant import llm
from apps.curriculum.content.levels import LEVELS
from apps.curriculum.hoeren import MANIFEST, content_clips

AUDIO_DIR = settings.BASE_DIR.parent / "frontend" / "public" / "hoeren"
SLOW_LEVELS = {"A1"}  # beginners hear a slower pace


def all_clips(levels) -> list[tuple[str, dict, str]]:
    """(file name, clip, level) for every recording in the content."""
    out = []
    for level in levels:
        for modul, teile in LEVELS[level].get("hoeren", {}).items():
            for teil, item in enumerate(teile, start=1):
                out += [(n, c, level) for n, c in content_clips(level, modul, teil, item)]
    return out


def to_mp3(pcm: bytes, path) -> None:
    subprocess.run(
        ["ffmpeg", "-loglevel", "error", "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", "pipe:0"]
        + ["-codec:a", "libmp3lame", "-b:a", "64k", "-y", str(path)],
        input=pcm,
        check=True,
    )


class Command(BaseCommand):
    help = "Generate missing Hören audio with Gemini TTS (resumable; stops at the quota)."

    def add_arguments(self, parser):
        parser.add_argument("--level", action="append", choices=list(LEVELS))
        parser.add_argument("--redo", action="append", default=[], help="A clip to remake.")
        parser.add_argument("--limit", type=int, default=0, help="At most this many clips.")
        parser.add_argument("--pause", type=float, default=7, help="Seconds between calls.")

    def handle(self, *args, level=None, redo=(), limit=0, pause=7, **options):
        AUDIO_DIR.mkdir(parents=True, exist_ok=True)
        clips = all_clips(level or list(LEVELS))
        todo = [c for c in clips if c[0] in redo or not (AUDIO_DIR / f"{c[0]}.mp3").exists()]
        if limit:
            todo = todo[:limit]
        made = 0
        for i, (name, recording, lvl) in enumerate(todo):
            if i:
                time.sleep(pause)
            try:
                pcm = llm.synthesize_speech(recording["script"], slow=lvl in SLOW_LEVELS)
            except errors.APIError as err:
                if getattr(err, "code", None) == 429:
                    # The free tier allows about 10 recordings a day; Google says when to retry.
                    wait = re.search(
                        r"retry in ([\dhm]*\d+)", str(err)
                    )  # "13h3m42.3s" -> "13h3m42"
                    when = f" Try again in {wait[1]}s." if wait else " Run again later."
                    self.stdout.write(self.style.WARNING(f"Quota reached.{when}"))
                    break
                self.stdout.write(self.style.ERROR(f"{name}: {err}"))
                continue
            to_mp3(pcm, AUDIO_DIR / f"{name}.mp3")
            made += 1
            self.stdout.write(f"  {name}.mp3")

        # Every clip whose file exists, from all levels (not only the ones run now).
        every = [n for n, _, _ in all_clips(list(LEVELS))]
        have = sorted(n for n in every if (AUDIO_DIR / f"{n}.mp3").exists())
        MANIFEST.write_text(json.dumps(have, indent=1) + "\n")
        left = len(every) - len(have)
        self.stdout.write(
            self.style.SUCCESS(f"Made {made}. {len(have)} recorded, {left} still missing.")
        )
