"""Find a freely licensed picture on Wikimedia Commons for an AI-written lesson.

Only public-domain, CC0 and Creative Commons BY / BY-SA images are used, each
credited. The picture is loaded from Wikimedia's image hosts (allowed by the
CSP in frontend/vercel.json). Any failure means "no picture"; the reader then
draws its era tile.
"""

import html
import json
import re
import urllib.parse
import urllib.request

API = "https://commons.wikimedia.org/w/api.php"
HEADERS = {"User-Agent": "einfachDeutsch/1.0 (German-learning app; history lessons)"}
TIMEOUT = 10
WIDTH = "1000"
HOSTS = ("https://upload.wikimedia.org/", "https://thumb.wikimedia.org/")


def _free_license(name: str) -> bool:
    name = name.strip().lower()
    return name in ("public domain", "cc0") or name.startswith(("cc by ", "cc by-sa "))


def _get(params: dict) -> dict:
    url = f"{API}?{urllib.parse.urlencode({'format': 'json', **params})}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=TIMEOUT) as r:
        return json.load(r)


def _plain(value: str) -> str:
    return " ".join(re.sub(r"<[^>]+>", "", html.unescape(value or "")).split())


def find_image(query: str) -> tuple[str, str]:
    """(image url, credit) for the best free picture matching `query`, or
    ("", ""). Long phrases often match nothing, so shorter ones are tried too."""
    words = query.split()
    tries = dict.fromkeys([" ".join(words), " ".join(words[:3]), " ".join(words[:2])])
    for attempt in tries:
        if attempt:
            found = _search(attempt)
            if found[0]:
                return found
    return "", ""


def _search(query: str) -> tuple[str, str]:
    try:
        found = _get(
            {
                "action": "query",
                "generator": "search",
                "gsrsearch": f"{query} filetype:bitmap",
                "gsrnamespace": "6",
                "gsrlimit": "10",
                "prop": "imageinfo",
                "iiprop": "url|extmetadata|mime|size",
                "iiurlwidth": WIDTH,
            }
        )
    except (OSError, ValueError):
        return "", ""

    pages = sorted(
        found.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 0)
    )
    for page in pages:
        info = (page.get("imageinfo") or [{}])[0]
        meta = info.get("extmetadata", {})
        license_name = meta.get("LicenseShortName", {}).get("value", "")
        if (
            info.get("mime") in ("image/jpeg", "image/png")
            and info.get("width", 0) >= 600
            and _free_license(license_name)
            and info.get("thumburl", "").startswith(HOSTS)
        ):
            artist = _plain(meta.get("Artist", {}).get("value", "")) or "Unknown author"
            url = info["thumburl"].split("?")[0]  # drop Wikimedia's tracking parameters
            return url, f"{artist[:120]}, {license_name}, Wikimedia Commons"
    return "", ""
