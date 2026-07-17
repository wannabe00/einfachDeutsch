"""Original A1 curriculum content for the learning path (Phase 23.3 / 23.3b).

Structure follows Menschen A1.1 Module 1 (Lektionen 1-3: greetings & introducing
yourself, family & languages, free time) — but ALL items here are authored
original, not copied from the book (copyright rule: books supply structure /
themes / wordlists / exercise types only, never their text).

Depth target (23.3b): each Lektion ≈ a real book Lektion — ~26 Wortschatz
entries, **2 grammar points**, and ~4 day-sized Lessons of ~6 mixed items.

Consumed by `manage.py seed_a1_path`. Each Unit → a Chapter (holds its Words/
Exercises/Grammar) + Lessons; each Lesson is an ordered list of items:
  - {"kind": "exercise", "type": ..., "prompt": ..., ...}
  - {"kind": "review", "word": "<german>"}   (a vocab card from this unit)
  - {"kind": "grammar", "grammar": "<title>"} (a grammar topic from this unit)

Words are `(english, german, part_of_speech)`.

Only the exercise types the lesson player can render are used:
  simple  (translation/fill_blank/article/conjugation): needs "answer"
    ("answer" may list `|`-separated accepted alternatives)
  multiple_choice: needs "answer" + "options"
  sentence_order:  needs "answer" (list) + "tokens" (a shuffle of it)
"""

A1_LEVEL = "A1"

A1_UNITS = [
    # ======================================================================
    # UNIT 1 — Hallo! (greetings & introducing yourself)
    # ======================================================================
    {
        "order": 1,
        "title": "Hallo!",
        "theme": "Begrüßung & Vorstellung",
        "accent_color": "--section-1",
        "words": [
            ("hello", "Hallo", "phrase"),
            ("good morning", "Guten Morgen", "phrase"),
            ("good day / hello", "Guten Tag", "phrase"),
            ("good evening", "Guten Abend", "phrase"),
            ("good night", "Gute Nacht", "phrase"),
            ("bye (informal)", "Tschüss", "phrase"),
            ("goodbye", "Auf Wiedersehen", "phrase"),
            ("How are you? (informal)", "Wie geht's?", "phrase"),
            ("thank you", "Danke", "phrase"),
            ("please / you're welcome", "Bitte", "phrase"),
            ("yes", "ja", "other"),
            ("no", "nein", "other"),
            ("how", "wie", "other"),
            ("where from", "woher", "other"),
            ("where", "wo", "other"),
            ("to be called", "heißen", "verb"),
            ("to come", "kommen", "verb"),
            ("to live / reside", "wohnen", "verb"),
            ("to be", "sein", "verb"),
            ("Germany", "Deutschland", "noun"),
            ("Austria", "Österreich", "noun"),
            ("Switzerland", "die Schweiz", "noun"),
            ("the name", "der Name", "noun"),
            ("the woman / Mrs", "die Frau", "noun"),
            ("the man / Mr", "der Mann", "noun"),
            ("the city", "die Stadt", "noun"),
        ],
        "grammar": [
            {
                "title": "sein — Personalpronomen",
                "category": "verbs",
                "content": (
                    "**sein** (to be) is irregular — learn it by heart:\n\n"
                    "- ich **bin** — I am\n"
                    "- du **bist** — you are (informal)\n"
                    "- er/sie **ist** — he/she is\n"
                    "- wir **sind** — we are\n"
                    "- ihr **seid** — you are (plural)\n"
                    "- sie/Sie **sind** — they are / you are (formal)"
                ),
                "examples": "Ich bin Anna.\nDu bist aus Berlin.\nWir sind hier.",
            },
            {
                "title": "W-Fragen & Aussagesatz",
                "category": "sentence_structure",
                "content": (
                    "In a statement and a W-question the **verb is in second "
                    "position**:\n\n"
                    "- **Wie** heißt du? — What's your name?\n"
                    "- **Woher** kommst du? — Where are you from?\n"
                    "- **Wo** wohnst du? — Where do you live?\n\n"
                    "Statement: *Ich* **heiße** *Anna.* — the verb still comes second."
                ),
                "examples": "Wie heißt du?\nWoher kommst du?\nIch wohne in Wien.",
            },
        ],
        "lessons": [
            {
                "order": 1,
                "title": "Begrüßung",
                "items": [
                    {"kind": "review", "word": "Hallo"},
                    {"kind": "review", "word": "Guten Morgen"},
                    {
                        "kind": "exercise",
                        "type": "multiple_choice",
                        "prompt": "How do you say goodbye informally?",
                        "options": ["Tschüss", "Danke", "Hallo", "Guten Abend"],
                        "answer": "Tschüss",
                    },
                    {
                        "kind": "exercise",
                        "type": "multiple_choice",
                        "prompt": "It's 8 p.m. — how do you greet someone?",
                        "options": ["Guten Abend", "Guten Morgen", "Gute Nacht", "Tschüss"],
                        "answer": "Guten Abend",
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
                        "prompt": "Wie ___'s? (How are you?)",
                        "answer": "geht",
                    },
                ],
            },
            {
                "order": 2,
                "title": "Ich heiße …",
                "items": [
                    {"kind": "grammar", "grammar": "sein — Personalpronomen"},
                    {"kind": "review", "word": "heißen"},
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
                        "type": "fill_blank",
                        "prompt": "Er ___ aus Berlin.",
                        "answer": "ist",
                    },
                    {
                        "kind": "exercise",
                        "type": "multiple_choice",
                        "prompt": "Wie ___ du?",
                        "options": ["heißt", "heiße", "heißen", "heiß"],
                        "answer": "heißt",
                    },
                ],
            },
            {
                "order": 3,
                "title": "Woher kommst du?",
                "items": [
                    {"kind": "grammar", "grammar": "W-Fragen & Aussagesatz"},
                    {"kind": "review", "word": "kommen"},
                    {"kind": "review", "word": "Deutschland"},
                    {
                        "kind": "exercise",
                        "type": "fill_blank",
                        "prompt": "Ich komme ___ Österreich. (from)",
                        "answer": "aus",
                    },
                    {
                        "kind": "exercise",
                        "type": "multiple_choice",
                        "prompt": "___ kommst du? (Where are you from?)",
                        "options": ["Woher", "Wo", "Wie", "Wer"],
                        "answer": "Woher",
                    },
                    {
                        "kind": "exercise",
                        "type": "sentence_order",
                        "prompt": "Build the question:",
                        "answer": ["Woher", "kommst", "du"],
                        "tokens": ["kommst", "du", "Woher"],
                    },
                ],
            },
            {
                "order": 4,
                "title": "Wo wohnst du?",
                "items": [
                    {"kind": "review", "word": "wohnen"},
                    {"kind": "review", "word": "die Schweiz"},
                    {
                        "kind": "exercise",
                        "type": "conjugation",
                        "prompt": "wohnen — ich ___",
                        "answer": "wohne",
                    },
                    {
                        "kind": "exercise",
                        "type": "multiple_choice",
                        "prompt": "Ich wohne ___ Berlin.",
                        "options": ["in", "aus", "an", "zu"],
                        "answer": "in",
                    },
                    {
                        "kind": "exercise",
                        "type": "translation",
                        "prompt": "Translate: “I live in Munich.”",
                        "answer": "Ich wohne in München",
                    },
                    {
                        "kind": "exercise",
                        "type": "sentence_order",
                        "prompt": "Build the sentence:",
                        "answer": ["Ich", "wohne", "in", "Berlin"],
                        "tokens": ["in", "Ich", "Berlin", "wohne"],
                    },
                ],
            },
        ],
    },
    # ======================================================================
    # UNIT 2 — Familie & Sprachen (family & languages)
    # ======================================================================
    {
        "order": 2,
        "title": "Familie & Sprachen",
        "theme": "Familie & Sprachkenntnisse",
        "accent_color": "--section-2",
        "words": [
            ("the family", "die Familie", "noun"),
            ("the parents", "die Eltern", "noun"),
            ("the mother", "die Mutter", "noun"),
            ("the father", "der Vater", "noun"),
            ("the sister", "die Schwester", "noun"),
            ("the brother", "der Bruder", "noun"),
            ("the child", "das Kind", "noun"),
            ("the son", "der Sohn", "noun"),
            ("the daughter", "die Tochter", "noun"),
            ("the grandma", "die Oma", "noun"),
            ("the grandpa", "der Opa", "noun"),
            ("the friend (f)", "die Freundin", "noun"),
            ("to speak", "sprechen", "verb"),
            ("to understand", "verstehen", "verb"),
            ("to learn", "lernen", "verb"),
            ("to have", "haben", "verb"),
            ("German (language)", "Deutsch", "noun"),
            ("English", "Englisch", "noun"),
            ("Spanish", "Spanisch", "noun"),
            ("the language", "die Sprache", "noun"),
            ("married", "verheiratet", "adjective"),
            ("single", "ledig", "adjective"),
            ("small / little", "klein", "adjective"),
            ("big / tall", "groß", "adjective"),
            ("the number", "die Nummer", "noun"),
            ("the job / profession", "der Beruf", "noun"),
        ],
        "grammar": [
            {
                "title": "Possessivartikel: mein/dein/sein/ihr",
                "category": "pronouns",
                "content": (
                    "Possessives agree with the noun's gender (Nominativ):\n\n"
                    "- **mein** Vater (m), **meine** Mutter (f), **mein** Kind (n)\n"
                    "- **dein** Bruder — your brother\n"
                    "- **sein** Sohn — his son · **ihr** Sohn — her son\n\n"
                    "Feminine and plural nouns take **-e** (meine, deine, seine…)."
                ),
                "examples": "Das ist meine Mutter.\nWie heißt dein Bruder?\nIhr Vater ist Arzt.",
            },
            {
                "title": "haben (Präsens)",
                "category": "verbs",
                "content": (
                    "**haben** (to have) is slightly irregular:\n\n"
                    "- ich **habe**\n- du **hast**\n- er/sie **hat**\n"
                    "- wir **haben**\n\n"
                    "Use it for family and age: *Ich habe zwei Kinder.*"
                ),
                "examples": "Ich habe eine Schwester.\nHast du Geschwister?\nSie hat zwei Kinder.",
            },
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
                        "prompt": "___ Bruder",
                        "answer": "der",
                    },
                    {
                        "kind": "exercise",
                        "type": "article",
                        "prompt": "___ Schwester",
                        "answer": "die",
                    },
                    {"kind": "exercise", "type": "article", "prompt": "___ Kind", "answer": "das"},
                    {
                        "kind": "exercise",
                        "type": "multiple_choice",
                        "prompt": "Das ist ___ Mutter. (my)",
                        "options": ["meine", "mein", "deine", "dein"],
                        "answer": "meine",
                    },
                ],
            },
            {
                "order": 2,
                "title": "Possessivartikel",
                "items": [
                    {"kind": "grammar", "grammar": "Possessivartikel: mein/dein/sein/ihr"},
                    {"kind": "review", "word": "der Sohn"},
                    {
                        "kind": "exercise",
                        "type": "fill_blank",
                        "prompt": "Das ist ___ Vater. (my)",
                        "answer": "mein",
                    },
                    {
                        "kind": "exercise",
                        "type": "multiple_choice",
                        "prompt": "Wie heißt ___ Bruder? (your)",
                        "options": ["dein", "deine", "mein", "meine"],
                        "answer": "dein",
                    },
                    {
                        "kind": "exercise",
                        "type": "translation",
                        "prompt": "Translate: “That is my father.”",
                        "answer": "Das ist mein Vater",
                    },
                    {
                        "kind": "exercise",
                        "type": "sentence_order",
                        "prompt": "Build the sentence:",
                        "answer": ["Das", "ist", "meine", "Familie"],
                        "tokens": ["meine", "Das", "Familie", "ist"],
                    },
                ],
            },
            {
                "order": 3,
                "title": "Ich habe …",
                "items": [
                    {"kind": "grammar", "grammar": "haben (Präsens)"},
                    {"kind": "review", "word": "haben"},
                    {
                        "kind": "exercise",
                        "type": "conjugation",
                        "prompt": "haben — ich ___",
                        "answer": "habe",
                    },
                    {
                        "kind": "exercise",
                        "type": "conjugation",
                        "prompt": "haben — du ___",
                        "answer": "hast",
                    },
                    {
                        "kind": "exercise",
                        "type": "fill_blank",
                        "prompt": "Sie ___ zwei Kinder. (she has)",
                        "answer": "hat",
                    },
                    {
                        "kind": "exercise",
                        "type": "multiple_choice",
                        "prompt": "___ du Geschwister?",
                        "options": ["Hast", "Habe", "Hat", "Haben"],
                        "answer": "Hast",
                    },
                ],
            },
            {
                "order": 4,
                "title": "Sprachen",
                "items": [
                    {"kind": "review", "word": "sprechen"},
                    {"kind": "review", "word": "die Sprache"},
                    {
                        "kind": "exercise",
                        "type": "translation",
                        "prompt": "Translate: “I speak German.”",
                        "answer": "Ich spreche Deutsch",
                    },
                    {
                        "kind": "exercise",
                        "type": "conjugation",
                        "prompt": "sprechen — du ___ (careful: e→i!)",
                        "answer": "sprichst",
                    },
                    {
                        "kind": "exercise",
                        "type": "multiple_choice",
                        "prompt": "Welche ___ sprichst du?",
                        "options": ["Sprache", "Familie", "Nummer", "Stadt"],
                        "answer": "Sprache",
                    },
                    {
                        "kind": "exercise",
                        "type": "sentence_order",
                        "prompt": "Build the sentence:",
                        "answer": ["Ich", "lerne", "gern", "Deutsch"],
                        "tokens": ["gern", "Deutsch", "Ich", "lerne"],
                    },
                ],
            },
        ],
    },
    # ======================================================================
    # UNIT 3 — Freizeit (free time)
    # ======================================================================
    {
        "order": 3,
        "title": "Freizeit",
        "theme": "Freizeitaktivitäten",
        "accent_color": "--section-3",
        "words": [
            ("the free time", "die Freizeit", "noun"),
            ("the hobby", "das Hobby", "noun"),
            ("to play", "spielen", "verb"),
            ("football", "Fußball", "noun"),
            ("the music", "die Musik", "noun"),
            ("to listen (to)", "hören", "verb"),
            ("to read", "lesen", "verb"),
            ("the book", "das Buch", "noun"),
            ("to swim", "schwimmen", "verb"),
            ("to dance", "tanzen", "verb"),
            ("to cook", "kochen", "verb"),
            ("to make / do", "machen", "verb"),
            ("the sport", "der Sport", "noun"),
            ("the film / movie", "der Film", "noun"),
            ("the friend (m)", "der Freund", "noun"),
            ("gladly / like to", "gern", "adverb"),
            ("often", "oft", "adverb"),
            ("always", "immer", "adverb"),
            ("never", "nie", "adverb"),
            ("today", "heute", "adverb"),
            ("tomorrow", "morgen", "adverb"),
            ("Monday", "Montag", "noun"),
            ("Saturday", "Samstag", "noun"),
            ("Sunday", "Sonntag", "noun"),
            ("the week", "die Woche", "noun"),
            ("the weekend", "das Wochenende", "noun"),
        ],
        "grammar": [
            {
                "title": "Regelmäßige Verben im Präsens",
                "category": "verbs",
                "content": (
                    "Regular verbs take these present-tense endings "
                    "(stem = **spiel-**):\n\n"
                    "- ich spiel**e**\n- du spiel**st**\n- er/sie spiel**t**\n"
                    "- wir spiel**en**\n\n"
                    "Add **gern** after the verb to say you like doing it: "
                    "*Ich spiele gern Fußball.*"
                ),
                "examples": "Ich höre gern Musik.\nDu spielst Fußball.\nSie kocht gern.",
            },
            {
                "title": "Ja/Nein-Fragen",
                "category": "sentence_structure",
                "content": (
                    "A yes/no question puts the **verb first** (before the "
                    "subject):\n\n"
                    "- **Spielst** du Fußball? — Do you play football?\n"
                    "- **Kochst** du gern? — Do you like cooking?\n\n"
                    "Answer with **Ja** or **Nein**. (Compare a W-question, where "
                    "a question word comes first.)"
                ),
                "examples": "Spielst du Fußball? — Ja.\nHörst du gern Musik? — Nein.",
            },
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
                    {"kind": "exercise", "type": "article", "prompt": "___ Buch", "answer": "das"},
                ],
            },
            {
                "order": 2,
                "title": "Ich lese gern",
                "items": [
                    {"kind": "grammar", "grammar": "Regelmäßige Verben im Präsens"},
                    {"kind": "review", "word": "lesen"},
                    {"kind": "review", "word": "das Buch"},
                    {
                        "kind": "exercise",
                        "type": "translation",
                        "prompt": "Translate: “I read a book.”",
                        "answer": "Ich lese ein Buch",
                    },
                    {
                        "kind": "exercise",
                        "type": "multiple_choice",
                        "prompt": "Was ___ du in der Freizeit?",
                        "options": ["machst", "mache", "macht", "machen"],
                        "answer": "machst",
                    },
                    {
                        "kind": "exercise",
                        "type": "sentence_order",
                        "prompt": "Build the sentence:",
                        "answer": ["Ich", "höre", "gern", "Musik"],
                        "tokens": ["gern", "Ich", "Musik", "höre"],
                    },
                ],
            },
            {
                "order": 3,
                "title": "Fragen stellen",
                "items": [
                    {"kind": "grammar", "grammar": "Ja/Nein-Fragen"},
                    {"kind": "review", "word": "schwimmen"},
                    {
                        "kind": "exercise",
                        "type": "fill_blank",
                        "prompt": "___ du Fußball? (Do you play …? — verb first)",
                        "answer": "Spielst",
                    },
                    {
                        "kind": "exercise",
                        "type": "multiple_choice",
                        "prompt": "Which is a correct yes/no question?",
                        "options": [
                            "Kochst du gern?",
                            "Du kochst gern?",
                            "Gern du kochst?",
                            "Kochen du gern?",
                        ],
                        "answer": "Kochst du gern?",
                    },
                    {
                        "kind": "exercise",
                        "type": "translation",
                        "prompt": "Translate: “Do you play football?”",
                        "answer": "Spielst du Fußball",
                    },
                    {
                        "kind": "exercise",
                        "type": "sentence_order",
                        "prompt": "Build the question:",
                        "answer": ["Spielst", "du", "gern", "Fußball"],
                        "tokens": ["gern", "Spielst", "Fußball", "du"],
                    },
                ],
            },
            {
                "order": 4,
                "title": "Meine Woche",
                "items": [
                    {"kind": "review", "word": "Montag"},
                    {"kind": "review", "word": "das Wochenende"},
                    {"kind": "exercise", "type": "article", "prompt": "___ Woche", "answer": "die"},
                    {
                        "kind": "exercise",
                        "type": "fill_blank",
                        "prompt": "Ich spiele ___ Fußball. (gladly)",
                        "answer": "gern",
                    },
                    {
                        "kind": "exercise",
                        "type": "translation",
                        "prompt": "Translate: “I often listen to music.”",
                        "answer": "Ich höre oft Musik",
                    },
                    {
                        "kind": "exercise",
                        "type": "sentence_order",
                        "prompt": "Build the sentence:",
                        "answer": ["Ich", "spiele", "oft", "Fußball"],
                        "tokens": ["oft", "Fußball", "Ich", "spiele"],
                    },
                ],
            },
        ],
    },
]
