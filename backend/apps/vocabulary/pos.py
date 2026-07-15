"""Part of speech for vocabulary (Phase 23.9).

The Word Bank groups by **Level → part of speech**, so every word needs one.
Seeded/curated content sets it explicitly; anything else (legacy rows, words a
user adds) falls back to `guess_part_of_speech`, which exploits two reliable
facts about German:

  - nouns are **capitalised** and usually carry der/die/das
  - infinitives end in **-en / -eln / -ern** and are lowercase

It's a *guess*, not a parser: it can't tell an adjective from an adverb, so both
land in "other", and it's correctable in the admin. Explicit values always win
(see `Word.save`).
"""

NOUN = "noun"
VERB = "verb"
ADJECTIVE = "adjective"
ADVERB = "adverb"
PHRASE = "phrase"
OTHER = "other"

PART_OF_SPEECH_CHOICES = [
    (NOUN, "Noun"),
    (VERB, "Verb"),
    (ADJECTIVE, "Adjective"),
    (ADVERB, "Adverb"),
    (PHRASE, "Phrase"),
    (OTHER, "Other"),
]

ARTICLES = ("der ", "die ", "das ")

# Common lowercase words ending in -en that are NOT infinitives, so the verb
# rule doesn't swallow them.
_NOT_VERBS = {
    "oben",
    "unten",
    "innen",
    "außen",
    "hinten",
    "vorn",
    "vorne",
    "neben",
    "eben",
    "gegen",
    "übermorgen",
    "morgen",
    "wegen",
    "drinnen",
    "draußen",
    "gern",
    "gerne",
    "gestern",
    "sondern",
}

# -eln/-ern don't end in "en", so they're listed separately. They also need a
# length floor: "gern"/"gestern" are adverbs, not infinitives.
_VERB_SUFFIXES = ("en",)
_VERB_SUFFIXES_LONG = ("eln", "ern")
_MIN_VERB_LEN = 4
_MIN_LONG_VERB_LEN = 6


def guess_part_of_speech(german: str) -> str:
    """Best-effort part of speech for a German headword."""
    text = (german or "").strip()
    if not text:
        return OTHER

    lowered = text.lower()

    # "der Hund" / "die Katze" / "das Haus" — unambiguous.
    if lowered.startswith(ARTICLES):
        return NOUN

    # A multi-word entry without an article reads as a phrase ("Guten Tag").
    if " " in text:
        return PHRASE

    # German capitalises nouns.
    if text[0].isupper():
        return NOUN

    if lowered in _NOT_VERBS:
        return OTHER

    if len(lowered) >= _MIN_VERB_LEN and lowered.endswith(_VERB_SUFFIXES):
        return VERB
    if len(lowered) >= _MIN_LONG_VERB_LEN and lowered.endswith(_VERB_SUFFIXES_LONG):
        return VERB

    return OTHER
