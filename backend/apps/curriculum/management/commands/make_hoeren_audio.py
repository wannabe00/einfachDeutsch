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
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from google.genai import errors

from apps.ai_assistant import llm
from apps.curriculum.content.levels import LEVELS
from apps.curriculum.hoeren import MANIFEST, content_clips

AUDIO_DIR = settings.BASE_DIR.parent / "frontend" / "public" / "hoeren"
# Background recordings (CC0 / free licence, see the README there) and the gong.
SCENE_DIR = Path(__file__).resolve().parents[2] / "content" / "hoeren_scenes"
SLOW_LEVELS = {"A1"}  # beginners hear a slower pace


def all_clips(levels) -> list[tuple[str, dict, str]]:
    """(file name, clip, level) for every recording in the content, including the
    Moduls waiting to replace a live one (`hoeren_next`)."""
    out = []
    for level in levels:
        spec = LEVELS[level]
        for modul, teile in [*spec.get("hoeren", {}).items(), *spec.get("hoeren_next", {}).items()]:
            for teil, item in enumerate(teile, start=1):
                out += [(n, c, level) for n, c in content_clips(level, modul, teil, item)]
    # The same recording in two places has one name (a hash of it): make it once.
    return list({name: (name, c, lvl) for name, c, lvl in out}.values())


def sound_files(recording: dict) -> list:
    """The background and gong files a recording needs (they must exist)."""
    files = [SCENE_DIR / f"{recording['scene']}.mp3"] if recording.get("scene") else []
    return files + ([SCENE_DIR / "gong.mp3"] if recording.get("gong") else [])


def mix_filter(recording: dict) -> str:
    """ffmpeg filters: the voice (thin like a telephone for `phone`), after a gong
    if asked; a scene starts alone, then fades to a quiet bed under the voice."""
    # loudnorm works at 192 kHz, so resample after it and restart the timestamps.
    voice = "[0:a]loudnorm=I=-16:TP=-1.5,aresample=44100,asetpts=N/SR/TB"
    if recording.get("phone"):
        voice += ",highpass=f=300,lowpass=f=3400"
    chain = [voice + "[v]"]
    n = 1
    scene = recording.get("scene")
    if scene:
        chain.append(
            f"[{n}:a]aformat=channel_layouts=mono,loudnorm=I=-20,aresample=44100,asetpts=N/SR/TB,"
            "volume='if(lt(t,1.5),1,max(0.12,1-(t-1.5)*0.8))':eval=frame[bg]"
        )
        n += 1
    if recording.get("gong"):
        chain.append(
            f"[{n}:a]aformat=channel_layouts=mono,aresample=44100,asetpts=N/SR/TB,volume=0.7[g]"
        )
        chain.append("[g][v]concat=n=2:v=0:a=1[v]")
    if scene:
        chain.append("[v]adelay=1800:all=1,apad=pad_dur=1[v]")
        chain.append("[v][bg]amix=inputs=2:duration=first:normalize=0,asetpts=N/SR/TB[out]")
    else:
        chain.append("[v]apad=pad_dur=0.3[out]")
    return ";".join(chain)


def to_mp3(pcm: bytes, path, recording: dict) -> None:
    inputs = ["-f", "s16le", "-ar", "24000", "-ac", "1", "-i", "pipe:0"]
    for f in sound_files(recording):
        loop = ["-stream_loop", "-1"] if f.stem != "gong" else []
        inputs += [*loop, "-i", str(f)]
    subprocess.run(
        ["ffmpeg", "-loglevel", "error", *inputs, "-filter_complex", mix_filter(recording)]
        + ["-map", "[out]", "-ac", "1", "-codec:a", "libmp3lame", "-b:a", "64k", "-y", str(path)],
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
        for name, recording, lvl in todo:
            missing = [f.name for f in sound_files(recording) if not f.exists()]
            if missing:  # never record a scene without its background
                self.stdout.write(self.style.WARNING(f"  {name}: needs {', '.join(missing)}"))
                continue
            if made:
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
            to_mp3(pcm, AUDIO_DIR / f"{name}.mp3", recording)
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
