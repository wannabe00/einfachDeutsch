"""Fetch the listening tasks' German as recordings by native speakers.

Covers the Grundlagen starter units (`hear` / `dictate` in content/a0.py). Each
word comes from Wikimedia Commons' pronunciation files ("De-<word>.ogg", free
licences); a spelled name ("M. A. X.") is the letters' files joined with short
pauses. Each becomes frontend/public/speech/<hash>.mp3 (ffmpeg), the licences
go to frontend/public/speech/CREDITS.txt (CC BY-SA needs the credit), and
content/speech_audio.json is rewritten. A text Commons doesn't have is listed
and skipped: the lesson then falls back to the browser's voice, so reword it.

    manage.py make_speech_audio            # everything that's missing
    manage.py make_speech_audio --redo     # fetch every file again
"""

import html
import json
import re
import subprocess
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.curriculum.content.levels import STARTER
from apps.curriculum.speech import MANIFEST, clip_name, spoken_text

AUDIO_DIR = settings.BASE_DIR.parent / "frontend" / "public" / "speech"
CREDITS = AUDIO_DIR / "CREDITS.txt"
API = "https://commons.wikimedia.org/w/api.php"
# Wikimedia asks every client to name itself.
HEADERS = {
    "User-Agent": "einfachDeutsch/1.0 (https://einfach-deutsch.vercel.app; audio credits kept)"
}
SPELLED = re.compile(r"^(?:[A-Z]\.?\s*)+$")
GAP = 0.35  # seconds of silence between spelled letters


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


def words_of(text: str) -> list[str]:
    """The Commons words a text is made of: its letters if spelled, else itself."""
    if SPELLED.match(text):
        return [c for c in text if c.isalpha()]
    return [text.rstrip("!?.")]


def candidates(word: str) -> list[str]:
    """Commons titles to try for a word, most likely first."""
    forms = dict.fromkeys([word, word.lower(), word[:1].upper() + word[1:]])
    return [f"File:De-{f}.{ext}" for f in forms for ext in ("ogg", "oga", "wav", "mp3")]


def fetch(url: str) -> bytes:
    """GET with Wikimedia's rate limit in mind: on 429, wait as asked and retry."""
    for attempt in range(8):
        try:
            with urllib.request.urlopen(
                urllib.request.Request(url, headers=HEADERS), timeout=60
            ) as r:
                return r.read()
        except urllib.error.HTTPError as err:
            if err.code != 429 or attempt == 7:
                raise
            time.sleep(int(err.headers.get("Retry-After") or 0) or 10 * (attempt + 1))
    raise AssertionError("unreachable")


def lookup(titles: list[str]) -> dict:
    """{title: {"url", "license", "artist"}} for the titles that exist."""
    found = {}
    for i in range(0, len(titles), 50):
        query = urllib.parse.urlencode(
            {
                "action": "query",
                "format": "json",
                "titles": "|".join(titles[i : i + 50]),
                "prop": "imageinfo",
                "iiprop": "url|extmetadata",
            }
        )
        pages = json.loads(fetch(f"{API}?{query}"))["query"]["pages"].values()
        for page in pages:
            if "imageinfo" not in page:
                continue
            info = page["imageinfo"][0]
            meta = info.get("extmetadata", {})
            artist = re.sub(r"<[^>]+>", "", meta.get("Artist", {}).get("value", ""))
            found[page["title"]] = {
                "url": info["url"].split("?")[0],
                "license": meta.get("LicenseShortName", {}).get("value", ""),
                "artist": html.unescape(artist).strip() or "unknown",
            }
        time.sleep(2)  # stay well under the API's rate limit
    return found


def download(url: str, dest: Path) -> None:
    dest.write_bytes(fetch(url))
    time.sleep(3)


def to_mp3(sources: list[Path], dest: Path) -> None:
    """Join the sources (with a short pause between) into one quiet-trimmed MP3."""
    inputs, filters = [], []
    for i, src in enumerate(sources):
        inputs += ["-i", str(src)]
        # Trim leading/trailing silence and even out the volume of each recording.
        filters.append(
            f"[{i}:a]aformat=sample_rates=24000:channel_layouts=mono,"
            "silenceremove=start_periods=1:start_threshold=-45dB,"
            "areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
            f"loudnorm=I=-18:TP=-2,apad=pad_dur={GAP if i < len(sources) - 1 else 0.15}[a{i}]"
        )
    joined = "".join(f"[a{i}]" for i in range(len(sources)))
    graph = ";".join(filters) + f";{joined}concat=n={len(sources)}:v=0:a=1,adelay=150[out]"
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", graph,
         "-map", "[out]", "-ac", "1", "-b:a", "64k", str(dest)],
        check=True,
    )  # fmt: skip


class Command(BaseCommand):
    help = "Fetch native recordings for the starter units from Wikimedia Commons. Safe to re-run."

    def add_arguments(self, parser):
        parser.add_argument("--redo", action="store_true", help="Fetch every file again.")

    def handle(self, *args, redo=False, **options):
        AUDIO_DIR.mkdir(parents=True, exist_ok=True)
        texts = all_texts()
        words = list(dict.fromkeys(w for t in texts for w in words_of(t)))
        found = lookup(sorted({c for w in words for c in candidates(w)}))
        source = {w: next((c for c in candidates(w) if c in found), None) for w in words}

        missing = [t for t in texts if not all(source[w] for w in words_of(t))]
        with tempfile.TemporaryDirectory() as tmp:
            cache: dict[str, Path] = {}
            for text in texts:
                dest = AUDIO_DIR / f"{clip_name(text)}.mp3"
                if text in missing or (dest.exists() and not redo):
                    continue
                files = []
                for w in words_of(text):
                    title = source[w]
                    if title not in cache:
                        cache[title] = Path(tmp) / f"{len(cache)}{Path(title).suffix}"
                        download(found[title]["url"], cache[title])
                    files.append(cache[title])
                to_mp3(files, dest)
                self.stdout.write(f"  {text}")

        used = sorted({source[w] for t in texts if t not in missing for w in words_of(t)})
        CREDITS.write_text(
            "Pronunciation recordings from Wikimedia Commons, converted to MP3.\n"
            "Each file keeps its licence; CC BY-SA files may be shared under the same licence.\n\n"
            + "".join(
                f"{t.removeprefix('File:')}: {found[t]['artist']}, {found[t]['license']}, "
                f"https://commons.wikimedia.org/wiki/{urllib.parse.quote(t.replace(' ', '_'))}\n"
                for t in used
            )
        )
        done = sorted(
            clip_name(t) for t in texts if (AUDIO_DIR / f"{clip_name(t)}.mp3").exists()
            and t not in missing
        )  # fmt: skip
        MANIFEST.write_text(json.dumps(done, indent=1) + "\n")
        for text in missing:
            self.stdout.write(self.style.WARNING(f"Not on Commons, reword it: {text}"))
        self.stdout.write(self.style.SUCCESS(f"{len(done)}/{len(texts)} have a native recording."))
