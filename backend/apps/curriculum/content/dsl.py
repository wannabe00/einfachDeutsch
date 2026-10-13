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


def interleave(authored, vocab) -> list[dict]:
    """Alternate hand-written lessons with generated vocabulary lessons, so new
    words and grammar are practised side by side."""
    out = []
    for i in range(max(len(authored), len(vocab))):
        out.extend(authored[i : i + 1])
        out.extend(vocab[i : i + 1])
    return out
