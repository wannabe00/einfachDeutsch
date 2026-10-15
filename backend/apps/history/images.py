"""Find a freely licensed picture for a history lesson.

Sources are tried in order and the first acceptable picture wins:

1. Wikimedia Commons: public domain, CC0, CC BY, CC BY-SA.
2. Art Institute of Chicago: public-domain works only (CC0).
3. The Met Open Access: public-domain objects only.
4. Openverse (Creative Commons search): the same licences as Commons; the
   picture is served through Openverse's thumbnail proxy, so one host covers
   them all. It is slow, so it comes after the museums.
5. Pexels, only when `PEXELS_API_KEY` is set (free licence, credited).

Each query is tried in a few forms (as given, then shorter), across the
sources, within an overall time limit so a lesson request never hangs; a
source that errors (down, too slow) is skipped for the rest of the search. Every
picture is credited. Any failure means "no picture"; the reader then draws its
era tile. Picture hosts must be allowed by the CSP in frontend/vercel.json.
"""

import html
import json
import re
import time
import urllib.parse
import urllib.request

from django.conf import settings

HEADERS = {"User-Agent": "einfachDeutsch/1.0 (German-learning app; history lessons)"}
TIMEOUT = 6
DEADLINE = 25  # seconds for the whole search
MIN_WIDTH = 600

WIKIMEDIA = "https://commons.wikimedia.org/w/api.php"
WIKIMEDIA_HOSTS = ("https://upload.wikimedia.org/", "https://thumb.wikimedia.org/")
OPENVERSE = "https://api.openverse.org/v1/images/"
OPENVERSE_LICENSES = {"cc0": "CC0", "pdm": "Public domain", "by": "CC BY", "by-sa": "CC BY-SA"}
MET = "https://collectionapi.metmuseum.org/public/collection"
AIC = "https://api.artic.edu/api/v1/artworks/search"
PEXELS = "https://api.pexels.com/v1/search"


def _free_license(name: str) -> bool:
    name = name.strip().lower()
    return name in ("public domain", "cc0") or name.startswith(("cc by ", "cc by-sa "))


def _get(url: str, params: dict, headers: dict | None = None) -> dict:
    full = f"{url}?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(full, headers={**HEADERS, **(headers or {})})
    with urllib.request.urlopen(request, timeout=TIMEOUT) as r:
        return json.load(r)


def _mentions(query: str, text: str) -> bool:
    """Museum searches match loosely (an artist named Luther for "Luther"), so
    a museum picture must name one of the query's words in its own title."""
    words = {w for w in re.findall(r"\w{4,}", query.lower())}
    return bool(words & set(re.findall(r"\w{4,}", (text or "").lower())))


def _plain(value: str) -> str:
    return " ".join(re.sub(r"<[^>]+>", "", html.unescape(value or "")).split())


# ---- sources: each returns (url, credit) for the first acceptable picture ----


def _wikimedia(query: str, exclude: set) -> tuple[str, str]:
    found = _get(
        WIKIMEDIA,
        {
            "format": "json",
            "action": "query",
            "generator": "search",
            "gsrsearch": f"{query} filetype:bitmap",
            "gsrnamespace": "6",
            "gsrlimit": "10",
            "prop": "imageinfo",
            "iiprop": "url|extmetadata|mime|size",
            "iiurlwidth": "1000",
        },
    )
    pages = sorted(
        found.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 0)
    )
    for page in pages:
        info = (page.get("imageinfo") or [{}])[0]
        meta = info.get("extmetadata", {})
        license_name = meta.get("LicenseShortName", {}).get("value", "")
        url = info.get("thumburl", "").split("?")[0]  # drop Wikimedia's tracking parameters
        if (
            info.get("mime") in ("image/jpeg", "image/png")
            and info.get("width", 0) >= MIN_WIDTH
            and _free_license(license_name)
            and url.startswith(WIKIMEDIA_HOSTS)
            and url not in exclude
        ):
            artist = _plain(meta.get("Artist", {}).get("value", "")) or "Unknown author"
            return url, f"{artist[:120]}, {license_name}, Wikimedia Commons"
    return "", ""


def _openverse(query: str, exclude: set) -> tuple[str, str]:
    found = _get(
        OPENVERSE,
        {"q": query, "license": ",".join(OPENVERSE_LICENSES), "page_size": "10", "mature": "false"},
    )
    for item in found.get("results", []):
        license_name = OPENVERSE_LICENSES.get(item.get("license", ""))
        url = item.get("thumbnail") or ""
        if (
            license_name
            and url.startswith(OPENVERSE)
            and (item.get("width") or MIN_WIDTH) >= MIN_WIDTH
            and url not in exclude
        ):
            version = item.get("license_version") or ""
            if license_name.startswith("CC BY") and version:
                license_name = f"{license_name} {version}"
            creator = _plain(item.get("creator") or "") or "Unknown author"
            source = item.get("source") or item.get("provider") or "Openverse"
            return url, f"{creator[:120]}, {license_name}, via Openverse ({source})"
    return "", ""


def _met(query: str, exclude: set) -> tuple[str, str]:
    found = _get(f"{MET}/v1.1/search", {"q": query, "hasImages": "true", "limit": "5"})
    for object_id in found.get("objectIDs") or []:
        item = _get(f"{MET}/v1/objects/{int(object_id)}", {})
        url = item.get("primaryImageSmall") or ""
        if item.get("isPublicDomain") and url.startswith("https://images.metmuseum.org/"):
            if url in exclude or not _mentions(query, item.get("title")):
                continue
            artist = item.get("artistDisplayName") or "Unknown artist"
            title = (item.get("title") or "")[:80]
            return url, f"{artist[:80]}, {title}, public domain, The Metropolitan Museum of Art"
    return "", ""


def _aic(query: str, exclude: set) -> tuple[str, str]:
    found = _get(
        AIC,
        {
            "q": query,
            "query[term][is_public_domain]": "true",
            "limit": "5",
            "fields": "id,title,image_id,artist_title,is_public_domain",
        },
        {"AIC-User-Agent": HEADERS["User-Agent"]},
    )
    for item in found.get("data", []):
        if not (item.get("is_public_domain") and item.get("image_id")):
            continue
        if not _mentions(query, item.get("title")):
            continue
        url = f"https://www.artic.edu/iiif/2/{item['image_id']}/full/843,/0/default.jpg"
        if url in exclude:
            continue
        artist = item.get("artist_title") or "Unknown artist"
        title = (item.get("title") or "")[:80]
        return url, f"{artist[:80]}, {title}, CC0, Art Institute of Chicago"
    return "", ""


def _pexels(query: str, exclude: set) -> tuple[str, str]:
    key = getattr(settings, "PEXELS_API_KEY", "")
    if not key:
        return "", ""
    found = _get(PEXELS, {"query": query, "per_page": "5"}, {"Authorization": key})
    for photo in found.get("photos", []):
        url = (photo.get("src") or {}).get("large") or ""
        if url.startswith("https://images.pexels.com/") and url not in exclude:
            return url, f"Photo by {photo.get('photographer') or 'unknown'} on Pexels"
    return "", ""


SOURCES = (_wikimedia, _aic, _met, _openverse, _pexels)


def _variants(queries) -> list[str]:
    """Each query as given, then shorter (long phrases often match nothing)."""
    out = []
    for query in queries:
        words = (query or "").split()
        out += [" ".join(words), " ".join(words[:3]), " ".join(words[:2])]
    return [q for q in dict.fromkeys(out) if q]


def find_image(*queries: str, exclude=()) -> tuple[str, str]:
    """(image url, credit) for the first free picture matching any of
    `queries` (best first), skipping URLs in `exclude`; ("", "") if none."""
    exclude = set(exclude)
    variants = _variants(queries)
    stop = time.monotonic() + DEADLINE
    for source in SOURCES:
        for query in variants:
            if time.monotonic() > stop:
                return "", ""
            try:
                found = source(query, exclude)
            except OSError:
                break  # down or slow: don't spend the time limit on it, try the next source
            except (ValueError, KeyError, TypeError):
                continue
            if found[0]:
                return found
    return "", ""


def queries_for(lesson) -> list[str]:
    """Search phrases for an existing lesson: its title, then era and title."""
    return [lesson.title, f"{lesson.era} {lesson.title}".strip(), "Germany history " + lesson.era]
