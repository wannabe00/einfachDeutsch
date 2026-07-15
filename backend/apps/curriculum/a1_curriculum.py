"""Original A1 curriculum content for the learning path (Phase 23.3).

Structure follows Menschen A1.1 Module 1 (Lektionen 1-3: greetings, family &
languages, free time) — but ALL items here are authored original, not copied
from the book (copyright rule: books provide structure/themes only).

Consumed by `manage.py seed_a1_path`. Each Unit → a Chapter (holds its Words/
Exercises/Grammar) + Lessons; each Lesson is an ordered list of items:
  - {"kind": "exercise", "type": ..., "prompt": ..., ...}
  - {"kind": "review", "word": "<german>"}   (a vocab card from this unit)
  - {"kind": "grammar", "grammar": "<title>"} (a grammar topic from this unit)

Exercise item shapes (deterministically gradable):
  simple  (translation/fill_blank/article/conjugation): needs "answer"
  multiple_choice: needs "answer" + "options"
  sentence_order:  needs "answer" (list) + "tokens" (shuffled list)
"""

A1_LEVEL = "A1"

A1_UNITS = [
    {
        "order": 1,
        "title": "Hallo!",
        "theme": "Begrüßung & Vorstellung",
        "accent_color": "--section-1",
        "words": [
            ("hello", "Hallo", "phrase"),
            ("good day", "Guten Tag", "phrase"),
            ("good morning", "Guten Morgen", "phrase"),
            ("bye (informal)", "Tschüss", "phrase"),
            ("goodbye", "Auf Wiedersehen", "phrase"),
            ("thank you", "Danke", "phrase"),
            ("Germany", "Deutschland", "noun"),
            ("Austria", "Österreich", "noun"),
            ("Switzerland", "die Schweiz", "noun"),
        ],
        "grammar": [
            {
                "title": "sein & Personalpronomen",
                "category": "verbs",
                "content": (
                    "The verb **sein** (to be) is irregular:\n\n"
                    "- ich **bin** — I am\n- du **bist** — you are (informal)\n"
                    "- Sie **sind** — you are (formal)\n- er/sie **ist** — he/she is\n\n"
                    "Ask names with **Wie heißt du?** (informal) / **Wie heißen Sie?** (formal)."
                ),
                "examples": "Ich bin Anna.\nWie heißt du?\nEr ist aus Deutschland.",
            }
        ],
        "lessons": [
            {
                "order": 1,
                "title": "Begrüßung",
                "items": [
                    {"kind": "review", "word": "Hallo"},
                    {"kind": "review", "word": "Guten Tag"},
                    {
                        "kind": "exercise",
                        "type": "multiple_choice",
                        "prompt": "How do you say goodbye informally?",
                        "options": ["Tschüss", "Danke", "Hallo", "Guten Morgen"],
                        "answer": "Tschüss",
                    },
                    {
                        "kind": "exercise",
                        "type": "translation",
                        "prompt": "Translate to German: “thank you”",
                        "answer": "Danke",
                    },
                    {
                        "kind": "exercise",
                        "type": "fill_blank",
                        "prompt": "___ heißt du? (What is your name?)",
                        "answer": "Wie",
                        "hint": "question word for “how/what”",
                    },
                ],
            },
            {
                "order": 2,
                "title": "Ich bin …",
                "items": [
                    {"kind": "grammar", "grammar": "sein & Personalpronomen"},
                    {
                        "kind": "exercise",
                        "type": "fill_blank",
                        "prompt": "Ich ___ Anna.",
                        "answer": "bin",
                    },
                    {
                        "kind": "exercise",
                        "type": "fill_blank",
                        "prompt": "Du ___ Tom.",
                        "answer": "bist",
                    },
                    {
                        "kind": "exercise",
                        "type": "multiple_choice",
                        "prompt": "Ich komme ___ Deutschland. (I come from Germany.)",
                        "options": ["aus", "in", "an", "zu"],
                        "answer": "aus",
                    },
                    {"kind": "review", "word": "Deutschland"},
                ],
            },
        ],
    },
    {
        "order": 2,
        "title": "Familie & Sprachen",
        "theme": "Familie & Sprachkenntnisse",
        "accent_color": "--section-2",
        "words": [
            ("the family", "die Familie", "noun"),
            ("the mother", "die Mutter", "noun"),
            ("the father", "der Vater", "noun"),
            ("the sister", "die Schwester", "noun"),
            ("the brother", "der Bruder", "noun"),
            ("the child", "das Kind", "noun"),
            ("to speak", "sprechen", "verb"),
            ("English", "Englisch", "noun"),
            ("German", "Deutsch", "noun"),
        ],
        "grammar": [
            {
                "title": "Possessivartikel: mein/dein",
                "category": "pronouns",
                "content": (
                    "Possessives agree with the noun's gender:\n\n"
                    "- **mein** Vater (m), **meine** Mutter (f), **mein** Kind (n)\n"
                    "- **dein** Bruder (m), **deine** Schwester (f)\n\n"
                    "Feminine and plural take **-e**."
                ),
                "examples": "Das ist meine Mutter.\nWie heißt dein Bruder?",
            }
        ],
        "lessons": [
            {
                "order": 1,
                "title": "Meine Familie",
                "items": [
                    {"kind": "review", "word": "die Mutter"},
                    {"kind": "review", "word": "der Vater"},
                    {
                        "kind": "exercise",
                        "type": "article",
                        "prompt": "___ Bruder (choose the article)",
                        "answer": "der",
                    },
                    {
                        "kind": "exercise",
                        "type": "article",
                        "prompt": "___ Schwester (choose the article)",
                        "answer": "die",
                    },
                    {
                        "kind": "exercise",
                        "type": "multiple_choice",
                        "prompt": "Das ist ___ Mutter. (my mother)",
                        "options": ["mein", "meine", "dein", "deine"],
                        "answer": "meine",
                    },
                ],
            },
            {
                "order": 2,
                "title": "Sprachen",
                "items": [
                    {"kind": "grammar", "grammar": "Possessivartikel: mein/dein"},
                    {
                        "kind": "exercise",
                        "type": "translation",
                        "prompt": "Translate: “I speak German.”",
                        "answer": "Ich spreche Deutsch",
                    },
                    {
                        "kind": "exercise",
                        "type": "fill_blank",
                        "prompt": "Sprichst du ___? (English)",
                        "answer": "Englisch",
                    },
                    {"kind": "review", "word": "sprechen"},
                    {
                        "kind": "exercise",
                        "type": "sentence_order",
                        "prompt": "Put the words in order:",
                        "answer": ["Das", "ist", "meine", "Familie"],
                        "tokens": ["meine", "Das", "Familie", "ist"],
                    },
                ],
            },
        ],
    },
    {
        "order": 3,
        "title": "Freizeit",
        "theme": "Freizeitaktivitäten",
        "accent_color": "--section-3",
        "words": [
            ("free time", "die Freizeit", "noun"),
            ("to play", "spielen", "verb"),
            ("football", "Fußball", "noun"),
            ("the music", "die Musik", "noun"),
            ("to listen", "hören", "verb"),
            ("to read", "lesen", "verb"),
            ("the book", "das Buch", "noun"),
            ("to swim", "schwimmen", "verb"),
            ("gladly / like to", "gern", "adverb"),
        ],
        "grammar": [
            {
                "title": "Regelmäßige Verben im Präsens",
                "category": "verbs",
                "content": (
                    "Regular verbs take these present-tense endings (stem = **spiel-**):\n\n"
                    "- ich spiel**e**\n- du spiel**st**\n- er/sie spiel**t**\n"
                    "- wir spiel**en**\n\n"
                    "Add **gern** after the verb to say you like doing it."
                ),
                "examples": "Ich spiele gern Fußball.\nDu hörst Musik.",
            }
        ],
        "lessons": [
            {
                "order": 1,
                "title": "Hobbys",
                "items": [
                    {"kind": "review", "word": "spielen"},
                    {"kind": "review", "word": "die Musik"},
                    {
                        "kind": "exercise",
                        "type": "conjugation",
                        "prompt": "spielen — ich ___",
                        "answer": "spiele",
                    },
                    {
                        "kind": "exercise",
                        "type": "conjugation",
                        "prompt": "hören — du ___",
                        "answer": "hörst",
                    },
                    {
                        "kind": "exercise",
                        "type": "multiple_choice",
                        "prompt": "Ich ___ gern Fußball.",
                        "options": ["spiele", "spielst", "spielt", "spielen"],
                        "answer": "spiele",
                    },
                ],
            },
            {
                "order": 2,
                "title": "Ich mag …",
                "items": [
                    {"kind": "grammar", "grammar": "Regelmäßige Verben im Präsens"},
                    {
                        "kind": "exercise",
                        "type": "translation",
                        "prompt": "Translate: “I read a book.”",
                        "answer": "Ich lese ein Buch",
                    },
                    {
                        "kind": "exercise",
                        "type": "fill_blank",
                        "prompt": "___ du gern Musik? (Do you like listening to music?)",
                        "answer": "Hörst",
                    },
                    {"kind": "review", "word": "lesen"},
                    {
                        "kind": "exercise",
                        "type": "sentence_order",
                        "prompt": "Put the words in order:",
                        "answer": ["Ich", "spiele", "gern", "Fußball"],
                        "tokens": ["gern", "Ich", "Fußball", "spiele"],
                    },
                ],
            },
        ],
    },
]
