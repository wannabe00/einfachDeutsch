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
import textwrap

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


# ---- checks: the review and Modul tests (see apps.curriculum.checks) ---------
#
# Check content is written once per Lektion (gap sentences and translations)
# and once per Modul (the extra test formats). The difficulty ramp decides
# which format each piece takes, so the same sentence is a chip gap early on and
# a typed gap later.

# (first Lektion, stage) per level; a level not listed is stage 4 throughout.
RAMP = {"A1": [(1, 1), (7, 2), (13, 3)]}

# What each stage allows. Stage 1 recognises, stage 2 builds from tiles, stage 3
# types, stage 4 translates freely.
STAGES = {
    1: {
        "words": ("pick_de", "pick_en", "article"),
        "match_batches": True,
        "gap": "chips",
        "translate": "choose",
        "form": "choose",
        "extras": ("dialogue", "qa", "odd", "reading", "form"),
    },
    2: {
        "words": ("pick_de", "pick_en", "article", "listen"),
        "match_batches": True,
        "gap": "chips",
        "translate": "tiles",
        "form": "choose",
        "extras": ("dialogue", "qa", "odd", "reading", "form", "mistake"),
    },
    3: {
        "words": ("pick_de", "article", "listen", "type_de"),
        "match_batches": False,
        "gap": "typed",
        "translate": "tiles",
        "form": "typed",
        "extras": ("dialogue", "qa", "odd", "reading", "form", "mistake", "dictation"),
    },
    4: {
        "words": ("type_de", "listen", "article", "pick_en"),
        "match_batches": False,
        "gap": "typed",
        "translate": "typed",
        "form": "typed",
        "extras": ("dialogue", "qa", "odd", "reading", "form", "mistake", "dictation"),
    },
}


def stage_of(level: str, lektion: int) -> int:
    """The difficulty stage of a Lektion (1 easiest)."""
    steps = RAMP.get(level)
    if not steps:
        return 4
    return max(stage for first, stage in steps if lektion >= first)


def _gap_parts(sentence: str) -> tuple[str, list[str]]:
    """'Ich [heiße] Anna.' -> ('Ich ___ Anna.', ['heiße'])."""
    answers, text, rest = [], "", sentence
    while "[" in rest:
        before, _, after = rest.partition("[")
        answer, _, rest = after.partition("]")
        text += before + "___"
        answers.append(answer)
    return text + rest, answers


def _swap_variant(german: str) -> str:
    """A wrong version of a sentence for multiple choice: the verb moved out of
    position 2 (the most common A1 word-order mistake)."""
    words = german.rstrip(".?!").split()
    end = german[len(german.rstrip(".?!")) :]
    if len(words) < 3:
        return " ".join(reversed(words)) + end
    words[1], words[2] = words[2], words[1]
    return " ".join(words) + end


def gap_task(sentences, distractors=(), stage: int = 1) -> dict:
    """Gap sentences written as 'Ich [heiße] Anna.', or (sentence, hint) where
    typing needs a hint. Chips: one text with a shared word bank (answers plus
    distractors); typed: one part per sentence."""
    sentences = [s if isinstance(s, tuple) else (s, "") for s in sentences]
    hints = [h for _, h in sentences]
    parsed = [_gap_parts(s) for s, _ in sentences]
    if STAGES[stage]["gap"] == "chips":
        text = "\n".join(f"{i}. {t}" for i, (t, _) in enumerate(parsed, start=1))
        # A gap may accept alternatives ("[bin|heiße]"); the chip is the first.
        answers = [a.split("|")[0] for _, ans in parsed for a in ans]
        return bank(text, answers, *distractors, prompt="Fill the gaps with words you've learned.")
    assert all(len(ans) == 1 for _, ans in parsed), "typed gaps take one gap per sentence"
    parts = [fill(t, ans[0], hint=h) for (t, ans), h in zip(parsed, hints, strict=True)]
    return group("Write the missing word.", *parts) if len(parts) > 1 else parts[0]


def translate_task(pairs, stage: int = 1) -> dict:
    """English -> German. `pairs` are (english, german, *alternatives).
    choose: pick the right German; tiles: build it; typed: write it."""
    mode = STAGES[stage]["translate"]
    parts = []
    for i, (english, german, *alts) in enumerate(pairs):
        if mode == "choose":
            other = pairs[(i + 1) % len(pairs)][1]
            wrong = [_swap_variant(german)] + ([other] if other != german else [])
            parts.append(mc(english, german, *wrong))
        elif mode == "tiles":
            parts.append(order(german, prompt=english))
        else:
            parts.append(_exercise("translation", english, "", answer="|".join([german, *alts])))
    prompts = {
        "choose": "Which is the German for this?",
        "tiles": "Build the German sentence.",
        "typed": "Translate into German.",
    }
    return group(prompts[mode], *parts) if len(parts) > 1 else parts[0]


def dialogue_task(lines, answer: str, *wrong: str) -> dict:
    """A short dialogue with one line missing ('___'); choose the line."""
    context = "\n".join(lines)
    assert context.count("___") == 1, lines
    item = mc("Which line fits the gap?", answer, *wrong)
    item["context"] = context
    return item


def qa_task(pairs) -> dict:
    """Match each question to its answer."""
    return match(pairs, "Match each question to its answer.")


def odd_task(rows) -> dict:
    """Odd one out. Each row is (odd word, *the words that belong together)."""
    parts = [mc("", o, *rest) for o, *rest in rows]
    return group("Which word doesn't belong?", *parts)


def reading_task(text: str, statements) -> dict:
    """A short original text and (statement, is_true) pairs."""
    parts = [
        _exercise(
            "multiple_choice",
            s,
            "",
            options=["Richtig", "Falsch"],
            answer="Richtig" if ok else "Falsch",
        )
        for s, ok in statements
    ]
    item = group("Read the text. Richtig oder falsch?", *parts)
    item["context"] = " ".join(text.split())  # one paragraph, however it was wrapped
    return item


def form_task(rows, stage: int = 1) -> dict:
    """Form the word. Each row is (prompt with ___, answer, *wrong forms):
    chosen early on, typed later."""
    if STAGES[stage]["form"] == "choose":
        parts = [mc(p, a, *w) for p, a, *w in rows]
    else:
        parts = [fill(p, a) for p, a, *_ in rows]
    return group("Form the word.", *parts)


def mistake_task(rows) -> dict:
    """Find the mistake. Each row is a sentence with the wrong word in *stars*
    and the corrected sentence: ('Ich *heißt* Anna.', 'Ich heiße Anna.')."""
    parts = []
    for marked, corrected in rows:
        words = marked.split()
        wrong = [i for i, w in enumerate(words) if w.strip(".,?!").startswith("*")]
        assert len(wrong) == 1, marked
        tokens = [w.replace("*", "") for w in words]
        parts.append(
            _exercise(
                "error_spot",
                "",
                "",
                tokens=tokens,
                answer=str(wrong[0]),
                correction=corrected,
            )
        )
    return group("Tap the word that's wrong.", *parts)


def dictation_task(sentences) -> dict:
    """Listen and write what you hear (the browser reads the sentence)."""
    parts = [_exercise("dictation", "", "", answer=s) for s in sentences]
    return group("Listen and write what you hear.", *parts)


def lektion_check(level: str, lektion: int, gaps, translations, distractors=()) -> dict:
    """The authored part of a Lektion's review: one gap task, one translation task."""
    stage = stage_of(level, lektion)
    return {
        "gap": gap_task(gaps, distractors, stage),
        "translate": translate_task(translations, stage),
    }


def modul_check(level: str, last_lektion: int, **extras) -> dict:
    """The extra formats of a Modul test, as the ramp allows at its last Lektion.
    Keys: dialogue, qa, odd, reading, form, mistake, dictation."""
    stage = stage_of(level, last_lektion)
    allowed = STAGES[stage]["extras"]
    builders = {
        "dialogue": lambda v: dialogue_task(*v),
        "qa": qa_task,
        "odd": odd_task,
        "reading": lambda v: reading_task(*v),
        "form": lambda v: form_task(v, stage),
        "mistake": mistake_task,
        "dictation": dictation_task,
    }
    return {k: builders[k](v) for k, v in extras.items() if k in allowed}


# ---- Lesen (exam-style reading, see apps.curriculum.lesen) -----------------

RF = ("Richtig", "Falsch")


def _text(text: str) -> str:
    """An authored text with its line breaks kept (notes, signs, boards)."""
    return textwrap.dedent(text).strip()


def _rf(statement: str, is_true: bool, context: str = "") -> dict:
    part = _exercise("multiple_choice", statement, options=list(RF), answer=RF[0 if is_true else 1])
    if context:
        part["context"] = _text(context)
    return part


def _choice(question: str, answer: str, *wrong: str, context: str = "") -> dict:
    part = mc(question, answer, *wrong)
    if context:
        part["context"] = _text(context)
    return part


def lesen_notes(texts, statements, teil: int = 1) -> dict:
    """A1 Teil 1: short notes or e-mails, then (statement, is_true) pairs."""
    item = group(
        f"Teil {teil} · Read the texts. Richtig oder falsch?",
        *[_rf(s, ok) for s, ok in statements],
    )
    item["context"] = "\n\n".join(_text(t) for t in texts)
    return item


def lesen_adverts(rows, teil: int = 2) -> dict:
    """A1 Teil 2: each row is (situation, advert a, advert b, "a" or "b")."""
    parts = []
    for situation, a, b, right in rows:
        assert right in ("a", "b"), situation
        part = _exercise("multiple_choice", situation, options=["a", "b"], answer=right)
        part["context"] = f"a) {_text(a)}\n\nb) {_text(b)}"
        parts.append(part)
    return group(f"Teil {teil} · Read the adverts. Which one fits: a or b?", *parts)


def lesen_signs(rows, teil: int = 3) -> dict:
    """A1 Teil 3: each row is (sign or notice, statement, is_true)."""
    parts = [_rf(statement, ok, context=sign) for sign, statement, ok in rows]
    return group(f"Teil {teil} · Read the signs. Richtig oder falsch?", *parts)


def lesen_text(what: str, text: str, rows, teil: int) -> dict:
    """A2 Teil 1 / 3: one longer text (article, e-mail), then multiple choice.
    Each row is (question, right answer, *wrong answers)."""
    item = group(
        f"Teil {teil} · Read the {what}. Choose the right answer.",
        *[_choice(q, a, *w) for q, a, *w in rows],
    )
    item["context"] = _text(text)
    return item


def lesen_directory(board: str, rows, teil: int = 2) -> dict:
    """A2 Teil 2: a store directory or information board. Each row is
    (situation, right place, *wrong places)."""
    item = group(
        f"Teil {teil} · Read the board. Where do you go?",
        *[_choice(q, a, *w) for q, a, *w in rows],
    )
    item["context"] = _text(board)
    return item


def lesen_rf(what: str, text: str, statements, teil: int = 1) -> dict:
    """B1 Teil 1: one text (a blog post) and (statement, is_true) pairs."""
    item = group(
        f"Teil {teil} · Read the {what}. Richtig oder falsch?",
        *[_rf(s, ok) for s, ok in statements],
    )
    item["context"] = _text(text)
    return item


NO_AD = "0"  # B1 Teil 3: no advert fits this situation


def lesen_ads(ads: dict, rows, teil: int = 3) -> dict:
    """B1 Teil 3: adverts {letter: text} and (situation, letter or NO_AD) rows.
    Each advert fits one situation at most; at least one situation has none."""
    letters = sorted(ads)
    picked = [letter for _, letter in rows if letter != NO_AD]
    assert len(set(picked)) == len(picked) and NO_AD in [r for _, r in rows], rows
    assert all(letter in ads for letter in picked), rows
    parts = [
        _exercise("multiple_choice", situation, options=[*letters, NO_AD], answer=letter)
        for situation, letter in rows
    ]
    item = group(
        f"Teil {teil} · Read the adverts. Which one fits each situation? (0 = none fits)", *parts
    )
    item["context"] = "\n\n".join(f"{k}) {_text(ads[k])}" for k in letters)
    return item


def lesen_opinions(question: str, comments, teil: int = 4) -> dict:
    """B1 Teil 4: readers' comments on one question. Each comment is
    (name, text, is_for): is the person for it? Ja / Nein."""
    parts = []
    for name, text, is_for in comments:
        part = _exercise(
            "multiple_choice",
            f"{name}: {question}",
            options=["Ja", "Nein"],
            answer="Ja" if is_for else "Nein",
        )
        part["context"] = _text(text)
        parts.append(part)
    return group(f"Teil {teil} · Read the comments. Is the person for it? Ja oder nein?", *parts)


def lesen_people(ads: dict, people, teil: int = 4) -> dict:
    """A2 Teil 4: adverts {letter: text} and (person, letter) rows. There is
    one advert more than people, so the last one can't be guessed."""
    letters = sorted(ads)
    assert len(letters) > len(people), people
    parts = []
    for person, letter in people:
        assert letter in ads, person
        parts.append(_exercise("multiple_choice", person, options=letters, answer=letter))
    item = group(f"Teil {teil} · Read the adverts. Which one fits each person?", *parts)
    item["context"] = "\n\n".join(f"{k}) {_text(ads[k])}" for k in letters)
    return item


# ---- Schreiben (exam-style writing, see apps.curriculum.schreiben) ----------


def schreiben_form(situation: str, fields, teil: int = 1) -> dict:
    """A1 Teil 1: a short text about a person, then a form with five gaps.
    Each field is (label, answer); `answer` may list variants as "a|b"."""
    item = group(
        f"Teil {teil} · Read the text and fill in the form.",
        *[fill(label, answer) for label, answer in fields],
    )
    item["context"] = _text(situation)
    return item


def schreiben_text(
    what: str, situation: str, points, words, model: str, formal=False, teil=2, forum=False
):
    """Free writing: a situation, three points to write about, a word range
    (min, max) and an original model answer that's shown after the attempt.
    `forum`: a forum post (B1 Teil 2), so no greeting or sign-off is expected."""
    points = list(points)
    assert len(points) == 3, situation
    return _exercise(
        "free_text",
        f"Teil {teil} · {what}",
        situation=_text(situation),
        points=points,
        min_words=words[0],
        max_words=words[1],
        formal=formal,
        forum=forum,
        model=_text(model),
    )


# ---- Hören (exam-style listening, see apps.curriculum.hoeren) ---------------

SPEAKERS = ("Frau", "Mann", "Ansage")  # each has its own voice (llm.VOICES)
# Background recordings in content/hoeren_scenes/<scene>.mp3 (see make_hoeren_audio).
SCENES = ("bahnhof", "strasse", "cafe", "laden", "buero", "park")


def clip(
    *lines,
    plays: int = 2,
    scene: str = "",
    phone: bool = False,
    gong: bool = False,
    radio: bool = False,
):
    """A recording: (speaker, line) pairs, at most two speakers, heard `plays`
    times (1 or 2, as in the exam). The script is also the transcript. Optional:
    a `scene` playing quietly underneath, a `phone` call (ring, thin voice), a
    `gong` before a loudspeaker announcement, or the sound of the `radio`.
    Only the options given are stored, so a
    recording's file name (a hash of this dict) stays the same until it changes."""
    script = [list(line) for line in lines]
    speakers = {s for s, _ in script}
    # Three voices only for the B1 radio discussion (Azure speaks any number;
    # the Gemini fallback takes two).
    assert speakers <= set(SPEAKERS) and len(speakers) <= 3, script
    assert plays in (1, 2), plays
    assert not scene or scene in SCENES, scene
    assert phone + gong + radio <= 1, "one of phone, gong (loudspeaker) or radio"
    extra = {"scene": scene, "phone": phone, "gong": gong, "radio": radio}
    return {"script": script, "plays": plays, **{k: v for k, v in extra.items() if v}}


def hoeren_mc(recording: dict, question: str, answer: str, *wrong: str) -> dict:
    """One question with its own recording, a/b/c."""
    return {**mc(question, answer, *wrong), "clip": recording}


def hoeren_rf(recording: dict, statement: str, is_true: bool) -> dict:
    """One richtig/falsch statement with its own recording."""
    return {**_rf(statement, is_true), "clip": recording}


def hoeren_teil(teil: int, instruction: str, *parts: dict, recording: dict | None = None):
    """A Teil: questions with their own recordings, or (A2 Teil 2 and 4) one
    `recording` for all of them."""
    assert recording is not None or all("clip" in p for p in parts), instruction
    item = group(f"Teil {teil} · {instruction}", *parts)
    if recording is not None:
        item["clip"] = recording
    return item


def hoeren_yn(statement: str, is_true: bool) -> dict:
    """A ja/nein statement about the Teil's one recording (A2 Teil 4)."""
    return _exercise(
        "multiple_choice", statement, options=["Ja", "Nein"], answer="Ja" if is_true else "Nein"
    )


def hoeren_tf(statement: str, is_true: bool) -> dict:
    """A richtig/falsch statement about the Teil's recording (B1 Teil 1 and 3)."""
    return _rf(statement, is_true)


def hoeren_who(statement: str, answer: str, speakers) -> dict:
    """B1 Teil 4: who says it? `speakers` keep their order (moderator first)."""
    assert answer in speakers, statement
    return _exercise("multiple_choice", statement, options=list(speakers), answer=answer)


def hoeren_match(teil: int, instruction: str, recording: dict, choices: dict, rows) -> dict:
    """A2 Teil 2: one recording, choices {letter: text} and (item, letter) rows.
    Each letter fits one item at most, and there are more choices than items."""
    letters = sorted(choices)
    picked = [letter for _, letter in rows]
    assert len(set(picked)) == len(picked) and len(letters) > len(rows), rows
    parts = [
        _exercise("multiple_choice", item, options=letters, answer=letter) for item, letter in rows
    ]
    item = hoeren_teil(teil, instruction, *parts, recording=recording)
    item["context"] = "\n".join(f"{k}) {choices[k]}" for k in letters)
    return item
