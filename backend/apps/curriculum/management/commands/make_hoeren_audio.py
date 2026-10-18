"""Generate the Hören recordings once from the scripts in content/<level>/hoeren.py.

Each missing clip is spoken by Azure or Gemini (`llm.synthesize_speech`), turned into a
64 kbit/s mono MP3 with the local ffmpeg, and saved to frontend/public/hoeren/.
The free API tier is rate-limited, so the command stops cleanly at the quota;
run it again later and it continues with the clips that are still missing.
It then rewrites content/hoeren_audio.json, which decides which sets go live.

    manage.py make_hoeren_audio                 # everything that's missing
    manage.py make_hoeren_audio --limit 3       # just a few, to listen first
    manage.py make_hoeren_audio --redo seed-a1-hoeren-m1-t1-0   # remake one
"""

import hashlib
import json
import re
import subprocess
import time
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

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


def _version(sound: str, name: str):
    """One of a sound's versions (`cafe.mp3`, `cafe-2.mp3`, ...), picked from the
    clip's name, so clips vary but each always gets the same one. Without any
    version, the plain name (which is then reported as missing)."""
    versions = sorted(SCENE_DIR.glob(f"{sound}.mp3")) + sorted(SCENE_DIR.glob(f"{sound}-*.mp3"))
    if not versions:
        return SCENE_DIR / f"{sound}.mp3"
    return versions[int(hashlib.sha1(name.encode()).hexdigest(), 16) % len(versions)]


def sound_files(recording: dict, name: str) -> list:
    """The background and gong files the recording `name` needs (they must exist)."""
    files = [_version(recording["scene"], name)] if recording.get("scene") else []
    return files + ([_version("gong", name)] if recording.get("gong") else [])


# Made by ffmpeg itself, nothing to download: the German ring tone (425 Hz,
# 1 s on, 1 s off, twice) and an answering machine's beep with a short gap.
RING = "aevalsrc='0.3*sin(2*PI*425*t)*lt(mod(t\\,2)\\,1)':d=3.4:s=44100"
BEEP = "aevalsrc='0.25*sin(2*PI*1000*t)*lt(t\\,0.4)':d=0.9:s=44100"
# How the voice is heard: on the phone, over a loudspeaker (with a gong), on the radio.
VOICE_FX = {
    "phone": "highpass=f=300,lowpass=f=3400",
    "pa": "highpass=f=250,lowpass=f=4500,acompressor=threshold=-20dB:ratio=4,"
    "aecho=0.8:0.5:45|90:0.25|0.15",
    "radio": "highpass=f=120,lowpass=f=7500,acompressor=threshold=-18dB:ratio=3:makeup=2",
}


def mix_filter(recording: dict) -> str:
    """ffmpeg filters. Phone calls start with the ring (a voicemail, one speaker,
    also with the beep) and sound thin; announcements start with the gong and
    sound like a loudspeaker; radio sounds like a radio. A scene starts alone,
    then fades to a quiet bed under everything."""
    fx = "phone" if recording.get("phone") else "pa" if recording.get("gong") else ""
    fx = fx or ("radio" if recording.get("radio") else "")
    # Level after the effect (the loudspeaker one alone takes ~17 dB off). loudnorm
    # works at 192 kHz, so resample after it and restart the timestamps.
    level = "loudnorm=I=-16:TP=-1.5,aresample=44100,asetpts=N/SR/TB"
    chain = ["[0:a]" + (f"{VOICE_FX[fx]}," if fx else "") + level + "[v]"]
    intro = []
    if recording.get("phone"):
        chain.append(f"{RING}[ring]")
        intro.append("[ring]")
        if len({speaker for speaker, _ in recording["script"]}) == 1:
            chain.append(f"{BEEP}[beep]")
            intro.append("[beep]")
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
            f"[{n}:a]aformat=channel_layouts=mono,loudnorm=I=-28:TP=-6,aresample=44100,asetpts=N/SR/TB[g]"
        )
        intro.append("[g]")
    if intro:
        chain.append(f"{''.join(intro)}[v]concat=n={len(intro) + 1}:v=0:a=1[v]")
    if scene:
        chain.append("[v]adelay=1800:all=1,apad=pad_dur=1[v]")
        chain.append("[v][bg]amix=inputs=2:duration=first:normalize=0,asetpts=N/SR/TB[out]")
    else:
        chain.append("[v]apad=pad_dur=0.3[out]")
    return ";".join(chain)


def to_mp3(pcm: bytes, path, recording: dict) -> None:
    inputs = ["-f", "s16le", "-ar", "24000", "-ac", "1", "-i", "pipe:0"]
    for f in sound_files(recording, Path(path).stem):
        loop = [] if f.stem.startswith("gong") else ["-stream_loop", "-1"]
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
        # --redo remakes just those clips; without it, every missing one.
        todo = (
            [c for c in clips if c[0] in redo]
            if redo
            else [c for c in clips if not (AUDIO_DIR / f"{c[0]}.mp3").exists()]
        )
        if limit:
            todo = todo[:limit]
        made = 0
        for name, recording, lvl in todo:
            missing = [f.name for f in sound_files(recording, name) if not f.exists()]
            if missing:  # never record a scene without its background
                self.stdout.write(self.style.WARNING(f"  {name}: needs {', '.join(missing)}"))
                continue
            if made:
                time.sleep(pause)
            try:
                pcm = llm.synthesize_speech(recording["script"], slow=lvl in SLOW_LEVELS)
            except llm.AIQuotaError as err:
                # The free tier allows a few recordings a day; Google says when to retry.
                wait = re.search(r"retry in ([\dhm]*\d+)", str(err))  # "13h3m42.3s" -> "13h3m42"
                when = f" Try again in {wait[1]}s." if wait else " Run again later."
                self.stdout.write(self.style.WARNING(f"Quota reached.{when}"))
                break
            except llm.AIResponseError as err:
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
