"""Helpers for writing path content.

Each helper returns the plain dict that `seed_path` understands, so a lesson
reads as a list of one-line exercises. Anything shuffled (options, word tiles,
word banks) is shuffled deterministically from the exercise text, so seeding
twice gives identical rows.

Words are `(english, german, part_of_speech)` or, for nouns, optionally
`(english, german, "noun", "Pl. die Tische")` with the plural as a note.
"""

import hashlib
import random

ARTICLES = ("der", "die", "das")


def _rng(key: str) -> random.Random:
    return random.Random(int(hashlib.md5(key.encode()).hexdigest(), 16))


def _shuffled(items, key: str) -> list:
    """A stable shuffle that never returns the original order (if it can)."""
    items = list(items)
    if len(set(items)) < 2:
        return items
    rng = _rng(key)
    for _ in range(20):
        out = items[:]
        rng.shuffle(out)
        if out != items:
            return out
    return items[::-1]


def _exercise(etype: str, prompt: str, hint: str = "", **fields) -> dict:
    return {"kind": "exercise", "type": etype, "prompt": prompt, "hint": hint, **fields}


# ---- exercises -------------------------------------------------------------


def mc(prompt: str, answer: str, *wrong: str, hint: str = "") -> dict:
    """Multiple choice. The right answer is mixed in with the wrong ones."""
    options = _shuffled([answer, *wrong], prompt + answer)
    return _exercise("multiple_choice", prompt, hint, options=options, answer=answer)


def fill(prompt: str, answer: str, hint: str = "") -> dict:
    """Type the missing word. `answer` may list alternatives as "a|b"."""
    return _exercise("fill_blank", prompt, hint, answer=answer)


def tr(english: str, german: str, hint: str = "") -> dict:
    """Translate English into German. `german` may list alternatives as "a|b"."""
    return _exercise("translation", f"Translate: “{english}”", hint, answer=german)


def art(noun: str, hint: str = "") -> dict:
    """Which article? `noun` is written with its article, e.g. "der Tisch"."""
    article, bare = noun.split(" ", 1)
    assert article in ARTICLES, noun
    return _exercise("article", f"___ {bare}", hint, answer=article)


def conj(verb: str, pronoun: str, form: str, hint: str = "") -> dict:
    """Conjugate `verb` for `pronoun`."""
    return _exercise("conjugation", f"{verb}: {pronoun} ___", hint, answer=form)


def order(sentence: str, prompt: str = "Put the words in order.", hint: str = "") -> dict:
    """Rebuild a sentence from shuffled words. Final punctuation is dropped."""
    words = sentence.rstrip(".?!").split()
    return _exercise(
        "sentence_order", prompt, hint, answer=words, tokens=_shuffled(words, sentence)
    )


def bank(text: str, answers, *distractors: str, prompt: str = "Fill the gaps.", hint="") -> dict:
    """Fill each `___` in `text` from a bank of words (answers plus distractors)."""
    answers = list(answers)
    assert text.count("___") == len(answers), text
    words = _shuffled([*answers, *distractors], text)
    return _exercise("word_bank", prompt, hint, text=text, bank=words, answers=answers)


def match(pairs, prompt: str = "Match the pairs.", hint: str = "") -> dict:
    """Match each left item to its partner. Left items must be unique."""
    pairs = [list(p) for p in pairs]
    assert len({p[0] for p in pairs}) == len(pairs), pairs
    return _exercise("matching", prompt, hint, pairs=pairs)


def group(prompt: str, *parts: dict, hint: str = "") -> dict:
    """Several exercises on one screen, like a workbook task: "write the new
    words in these five sentences". Each part is built with the helpers above
    and is checked on its own; the lesson score counts parts."""
    assert len(parts) >= 2, prompt
    assert all(p["kind"] == "exercise" and p["type"] != "group" for p in parts), prompt
    return _exercise("group", prompt, hint, parts=list(parts))


# ---- non-exercise items ----------------------------------------------------


def review(german: str) -> dict:
    """A flashcard for one of this unit's words."""
    return {"kind": "review", "word": german}


def grammar(title: str) -> dict:
    """The explanation card for one of this unit's grammar topics."""
    return {"kind": "grammar", "grammar": title}


def rule(title: str, category: str, content: str, examples) -> dict:
    """A grammar topic. `examples` is a list of example sentences."""
    return {
        "title": title,
        "category": category,
        "content": content.strip(),
        "examples": "\n".join(examples),
    }


def lesson(title: str, *items: dict, teaches=()) -> dict:
    """`teaches` lists the German of the words this lesson introduces. Words no
    lesson claims are assigned by `unit()`."""
    return {"title": title, "items": list(items), "teaches": list(teaches)}


# ---- vocabulary drills generated from a word list ---------------------------


def _german_head(german: str) -> str:
    return german.split(" ", 1)[1] if german.split(" ", 1)[0] in ARTICLES else german


def vocab_lessons(words, title: str, group_size: int = 6) -> list[dict]:
    """Lessons that practise every word in `words`, `group_size` at a time.

    Each lesson matches the batch German to English, asks the article of each
    noun, the meaning of two words, and a translation of up to two nouns or
    verbs. Distractors come from the same word list.
    """
    words = list(words)
    lessons = []
    for start in range(0, len(words), group_size):
        batch = words[start : start + group_size]
        if len(batch) < 3:  # fold a tiny remainder into the previous lesson
            lessons[-1]["items"].append(match([(w[1], w[0]) for w in batch]))
            lessons[-1]["teaches"].extend(w[1] for w in batch)
            continue
        n = len(lessons) + 1
        items = [match([(w[1], w[0]) for w in batch], "Match the German to the English.")]
        articles = [
            art(w[1], hint=w[0])
            for w in batch
            if w[2] == "noun" and w[1].split(" ", 1)[0] in ARTICLES and len(w[1].split()) == 2
        ]
        if len(articles) >= 2:
            items.append(group("Choose the article.", *articles))
        else:
            items.extend(articles)
        others = [w[0] for w in words]
        for w in batch[:2]:
            rng = _rng(title + w[1])
            pool = [e for e in others if e != w[0]]
            wrong = rng.sample(pool, min(3, len(pool)))
            items.append(mc(f"What does “{w[1]}” mean?", w[0], *wrong))
        translatable = [w for w in batch[2:] if w[2] in ("noun", "verb")][:2]
        for w in translatable:
            items.append(tr(w[0], w[1]))
        lessons.append(lesson(f"{title} {n}", *items, teaches=[w[1] for w in batch]))
    return lessons


def _assign_taught_words(words, lessons) -> None:
    """Give every word exactly one teaching lesson: the first lesson that
    names it in `teaches` or shows its flashcard, else the unit's last lesson."""
    owner = {}
    for les in lessons:
        mentioned = les["teaches"] + [i["word"] for i in les["items"] if i["kind"] == "review"]
        for german in mentioned:
            owner.setdefault(german, les)
    for les in lessons:
        les["teaches"] = []
    for w in words:
        owner.get(w[1], lessons[-1])["teaches"].append(w[1])


def unit(order: int, title: str, theme: str, words, rules, lessons) -> dict:
    """One Lektion. Lessons are numbered in the order given."""
    for i, les in enumerate(lessons, start=1):
        les["order"] = i
    _assign_taught_words(words, lessons)
    return {
        "order": order,
        "title": title,
        "theme": theme,
        "accent_color": f"--section-{(order - 1) % 6 + 1}",
        "words": list(words),
        "grammar": list(rules),
        "lessons": list(lessons),
    }


# ---- turning a Lektion into 2-3 lessons ---------------------------------------

# What a group of same-type exercises asks for.
GROUP_PROMPTS = {
    "multiple_choice": "Choose the right answer.",
    "fill_blank": "Fill in the missing word.",
    "conjugation": "Write the right form of the verb.",
    "translation": "Translate into German.",
    "article": "Write the article: der, die or das.",
    "sentence_order": "Put the words in order.",
    "word_bank": "Fill the gaps.",
}
# Most parts per group, so one screen stays readable. Matching blocks are big
# already and stay one per screen.
MAX_PARTS = {"word_bank": 2, "sentence_order": 4, "translation": 6}
DEFAULT_MAX_PARTS = 8
# A third lesson smaller than this is folded into the Grammatik lesson.
MIN_LESSON_PARTS = 15
LESSON_XP = 30


def _chunks(items: list, size: int) -> list[list]:
    """Split into as few chunks of at most `size` as possible, evenly sized."""
    count = -(-len(items) // size)
    base, extra = divmod(len(items), count)
    out, start = [], 0
    for i in range(count):
        end = start + base + (1 if i < extra else 0)
        out.append(items[start:end])
        start = end
    return out


def _grouped(exercises: list[dict]) -> list[dict]:
    """Same-type exercises merged into multi-part groups, in the order each type
    first appears. Existing groups are opened up and merged by type too."""
    by_type: dict[str, list[dict]] = {}
    for ex in exercises:
        for part in ex["parts"] if ex["type"] == "group" else [ex]:
            by_type.setdefault(part["type"], []).append(part)

    out = []
    for etype, parts in by_type.items():
        if etype == "matching":
            out.extend(parts)
            continue
        for chunk in _chunks(parts, MAX_PARTS.get(etype, DEFAULT_MAX_PARTS)):
            if len(chunk) == 1:
                out.append(chunk[0])
                continue
            if etype == "translation":
                # Under "Translate into German." each part only needs the English.
                chunk = [{**p, "prompt": p["prompt"].removeprefix("Translate: ")} for p in chunk]
            out.append(group(GROUP_PROMPTS[etype], *chunk))
    return out


def _topic_blocks(sources: list[dict]) -> list[list[dict]]:
    """Source lessons by topic: a lesson with a grammar explanation starts a
    block, and lessons without one join the topic before them."""
    blocks: list[list[dict]] = []
    for src in sources:
        starts_topic = any(i["kind"] == "grammar" for i in src["items"])
        if starts_topic or not blocks:
            blocks.append([src])
        else:
            blocks[-1].append(src)
    return blocks


def _lesson_from(title: str, blocks: list[list[dict]]) -> dict:
    """One lesson made of blocks of source lessons. Each block shows its
    flashcards and explanations first, then its exercises grouped by type."""
    items = []
    for block in blocks:
        block_items = [i for s in block for i in s["items"]]
        items += [i for i in block_items if i["kind"] != "exercise"]
        items += _grouped([i for i in block_items if i["kind"] == "exercise"])
    teaches = [g for block in blocks for s in block for g in s["teaches"]]
    out = lesson(title, *items, teaches=teaches)
    out["xp"] = LESSON_XP
    return out


def _parts(lessons: list[dict]) -> int:
    return sum(
        len(i.get("parts", [i])) for les in lessons for i in les["items"] if i["kind"] == "exercise"
    )


def sections(authored: list[dict], vocab: list[dict]) -> list[dict]:
    """A Lektion's lessons as they're played: 2 or 3 lessons, like a class.

    1. Wortschatz: the hand-written lessons before the first grammar topic,
       then the unit's words, two batches at a time: matched, then drilled.
    2. Grammatik: from the first lesson with a grammar explanation to the last
       one, each topic followed by its practice.
    3. Kommunikation und Wiederholung: everything after (dialogues, the
       Lektion test, the Modul review). Folded into Grammatik when it's small.

    Same-type exercises are grouped into multi-part exercises throughout.
    """
    has_rule = [any(i["kind"] == "grammar" for i in les["items"]) for les in authored]
    first = has_rule.index(True)
    last = len(has_rule) - 1 - has_rule[::-1].index(True)
    words, rules, talk = authored[:first], authored[first : last + 1], authored[last + 1 :]

    if _parts(talk) < MIN_LESSON_PARTS:
        rules, talk = rules + talk, []
    word_blocks = ([words] if words else []) + [vocab[i : i + 2] for i in range(0, len(vocab), 2)]
    out = [
        _lesson_from("Wortschatz", word_blocks),
        _lesson_from("Grammatik", _topic_blocks(rules)),
    ]
    if talk:
        out.append(_lesson_from("Kommunikation und Wiederholung", _topic_blocks(talk)))
    return out
