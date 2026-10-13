"""Modul 2: Lektion 4 (Der Tisch ist schön!), 5 (Was ist das?),
6 (Ich brauche kein Büro)."""

from ..dsl import (
    bank,
    conj,
    fill,
    grammar,
    lesson,
    match,
    mc,
    order,
    review,
    rule,
    sections,
    tr,
    unit,
    vocab_lessons,
)

# ============================================================================
# Lektion 4: Der Tisch ist schön!
# ============================================================================

L4_WORDS = [
    ("the furniture", "die Möbel", "noun", "plural only"),
    ("the table", "der Tisch", "noun", "Pl. die Tische"),
    ("the bed", "das Bett", "noun", "Pl. die Betten"),
    ("the armchair", "der Sessel", "noun", "Pl. die Sessel"),
    ("the lamp", "die Lampe", "noun", "Pl. die Lampen"),
    ("the chair", "der Stuhl", "noun", "Pl. die Stühle"),
    ("the sofa", "das Sofa", "noun", "Pl. die Sofas"),
    ("the couch", "die Couch", "noun", "Pl. die Couchs"),
    ("the wardrobe / cupboard", "der Schrank", "noun", "Pl. die Schränke"),
    ("the carpet / rug", "der Teppich", "noun", "Pl. die Teppiche"),
    ("the room", "das Zimmer", "noun", "Pl. die Zimmer"),
    ("the euro", "der Euro", "noun", "Pl. die Euro"),
    ("the cent", "der Cent", "noun", "Pl. die Cent"),
    ("the price", "der Preis", "noun", "Pl. die Preise"),
    ("the offer", "das Angebot", "noun", "Pl. die Angebote"),
    ("the special offer", "das Sonderangebot", "noun", "Pl. die Sonderangebote"),
    ("the help", "die Hilfe", "noun"),
    ("beautiful / nice", "schön", "adjective"),
    ("ugly", "hässlich", "adjective"),
    ("modern", "modern", "adjective"),
    ("practical", "praktisch", "adjective"),
    ("big / tall", "groß", "adjective"),
    ("small / short (person)", "klein", "adjective"),
    ("long", "lang", "adjective"),
    ("short", "kurz", "adjective"),
    ("light (not heavy) / easy", "leicht", "adjective"),
    ("heavy / difficult", "schwer", "adjective"),
    ("expensive", "teuer", "adjective"),
    ("cheap", "billig", "adjective"),
    ("good value / affordable", "günstig", "adjective"),
    ("bad", "schlecht", "adjective"),
    ("great", "toll", "adjective"),
    ("too (too expensive)", "zu", "adverb"),
    ("really", "wirklich", "adverb"),
    ("to cost", "kosten", "verb"),
    ("to find / to think (an opinion)", "finden", "verb", "du findest, er findet"),
    ("to say", "sagen", "verb"),
    ("to ask", "fragen", "verb"),
    ("a thousand", "tausend", "other"),
    ("a million", "eine Million", "phrase"),
    ("How much does … cost?", "Wie viel kostet …?", "phrase"),
    ("Can I help you?", "Kann ich Ihnen helfen?", "phrase"),
    ("That's too expensive.", "Das ist zu teuer.", "phrase"),
    ("I think so too.", "Das finde ich auch.", "phrase"),
]

L4_RULES = [
    rule(
        "der, das, die",
        "articles",
        """
Every German noun has a gender, shown by its article. Learn each noun **with** its article.

| masculine | neuter | feminine | plural |
|---|---|---|---|
| **der** Tisch | **das** Bett | **die** Lampe | **die** Möbel |

The plural article is always **die**, whatever the gender.
""",
        [
            "Der Stuhl ist neu.",
            "Das Sofa ist modern.",
            "Die Lampe ist teuer.",
            "Die Möbel sind schön.",
        ],
    ),
    rule(
        "er, es, sie",
        "pronouns",
        """
When you refer back to a thing, the pronoun matches the noun's **gender**, not "it":

- **der** Tisch → **er**: *Der Tisch? **Er** ist praktisch.*
- **das** Bett → **es**: *Das Bett? **Es** ist bequem.*
- **die** Lampe → **sie**: *Die Lampe? **Sie** kostet 39 Euro.*
- **die** Stühle (plural) → **sie**: *Die Stühle? **Sie** sind neu.*
""",
        [
            "Wie findest du den Schrank? Er ist zu groß.",
            "Wie viel kostet das Sofa? Es kostet 499 Euro.",
        ],
    ),
    rule(
        "Adjektive nach sein",
        "adjectives",
        """
After *sein* (and *finden*), an adjective takes **no ending**:

- *Der Tisch ist **schön**.* (not *schöner*)
- *Ich finde das Bett **praktisch**.*

Make it stronger or weaker with **sehr**, **zu**, **nicht**:
*sehr schön* (very), *zu teuer* (too), *nicht schlecht* (not bad).
""",
        ["Die Lampe ist sehr modern.", "Der Teppich ist zu teuer.", "Das finde ich nicht schön."],
    ),
    rule(
        "Preise und große Zahlen",
        "other",
        """
- 100 *(ein)hundert*, 200 *zweihundert*, 1.000 *(ein)tausend*, 1.000.000 *eine Million*
- Build big numbers left to right: 1.478 = *(ein)tausend · vierhundert · achtundsiebzig*
- German writes a **comma** for decimals and a **dot** for thousands: 1.478,50 €
- Say prices as euros, then cents: 9,99 € = *neun Euro neunundneunzig*; 0,50 € = *fünfzig Cent*
""",
        ["Der Tisch kostet 1.478 Euro.", "Was kostet die Lampe? 19,90 Euro."],
    ),
]

L4_LESSONS = [
    lesson(
        "Möbel",
        review("die Möbel"),
        review("der Tisch"),
        mc("You sleep in a …", "Bett", "Schrank", "Teppich"),
        mc("You put your clothes in a …", "Schrank", "Stuhl", "Sessel"),
        mc("It lies on the floor:", "der Teppich", "die Lampe", "der Tisch"),
        mc("It gives light:", "die Lampe", "das Sofa", "der Stuhl"),
        fill("Ich sitze auf dem ___. (chair)", "Stuhl"),
        tr("The room is big.", "Das Zimmer ist groß."),
    ),
    lesson(
        "der, das, die",
        grammar("der, das, die"),
        match(
            [
                ("Tisch", "der"),
                ("Lampe", "die"),
                ("Bett", "das"),
                ("Stuhl", "der"),
                ("Couch", "die"),
                ("Sofa", "das"),
            ],
            "Which article does each noun take?",
        ),
        fill("___ Schrank ist groß.", "Der"),
        fill("___ Zimmer ist klein.", "Das"),
        fill("___ Möbel sind modern.", "Die"),
        mc("___ Sessel ist bequem.", "Der", "Die", "Das"),
        mc("___ Teppich ist hässlich.", "Der", "Die", "Das"),
    ),
    lesson(
        "er, es, sie",
        grammar("er, es, sie"),
        mc("Der Tisch? ___ ist praktisch.", "Er", "Es", "Sie"),
        mc("Das Bett? ___ ist zu teuer.", "Es", "Er", "Sie"),
        mc("Die Lampe? ___ kostet 49 Euro.", "Sie", "Er", "Es"),
        mc("Die Stühle? ___ sind neu.", "Sie", "Er", "Es"),
        fill("Wie viel kostet das Sofa? ___ kostet 899 Euro.", "Es"),
        fill("Wie findest du den Teppich? ___ ist schön.", "Er"),
        fill("Ist die Couch neu? Ja, ___ ist neu.", "sie"),
        tr("The chair? It is cheap.", "Der Stuhl? Er ist billig."),
    ),
    lesson(
        "Wie ist der Tisch?",
        grammar("Adjektive nach sein"),
        match(
            [
                ("teuer", "billig"),
                ("groß", "klein"),
                ("schön", "hässlich"),
                ("lang", "kurz"),
                ("leicht", "schwer"),
                ("gut", "schlecht"),
            ],
            "Match the opposites.",
        ),
        mc(
            "Which sentence is correct?",
            "Der Tisch ist schön.",
            "Der Tisch ist schöner.",
            "Der Tisch ist schöne.",
        ),
        fill("Das Sofa kostet 3.000 Euro. Es ist ___ teuer! (too)", "zu"),
        fill("Der Schrank ist nicht teuer. Er ist ___. (cheap)", "billig|günstig"),
        order("Die Lampe ist sehr modern."),
        tr("The carpet is too expensive.", "Der Teppich ist zu teuer."),
    ),
    lesson(
        "Was kostet das?",
        grammar("Preise und große Zahlen"),
        match(
            [
                ("9,99 €", "neun Euro neunundneunzig"),
                ("0,50 €", "fünfzig Cent"),
                ("19,90 €", "neunzehn Euro neunzig"),
                ("120 €", "hundertzwanzig Euro"),
            ],
            "Match the prices.",
        ),
        mc("1.000 in words:", "tausend", "hundert", "eine Million"),
        mc("350 in words:", "dreihundertfünfzig", "dreihundertfünfundzwanzig", "dreifünfzig"),
        mc("1.200 in words:", "tausendzweihundert", "zwölfhundertzwei", "tausendzwanzig"),
        fill("200 = ___hundert", "zwei"),
        fill("1.000.000 = eine ___", "Million"),
        order("Wie viel kostet der Sessel?", "Build the question."),
        tr("What does the table cost?", "Was kostet der Tisch?|Wie viel kostet der Tisch?"),
    ),
    lesson(
        "Im Möbelhaus",
        review("Kann ich Ihnen helfen?"),
        bank(
            "Guten Tag! Kann ich Ihnen ___? Ja, bitte. Wie viel ___ das Bett? 299 Euro. "
            "Es ist ein ___. Oh, das ist ___!",
            ["helfen", "kostet", "Sonderangebot", "günstig"],
            "teuer",
            "Preis",
        ),
        mc(
            "The shop assistant asks: Kann ich Ihnen helfen? You answer:",
            "Ja, bitte.",
            "Nein, bitte.",
            "Gute Nacht.",
        ),
        mc(
            "The sofa costs 2.500 €. You think:",
            "Das ist zu teuer.",
            "Das ist zu billig.",
            "Das ist ein Teppich.",
        ),
        mc(
            "Das ist ein Sonderangebot. This means:",
            "It is on special offer.",
            "It is sold out.",
            "It is broken.",
        ),
        order("Das Bett ist ein Sonderangebot."),
        tr("Do you need help? (formal)", "Brauchen Sie Hilfe?"),
    ),
    lesson(
        "Das finde ich …",
        review("Das finde ich auch."),
        conj("finden", "du", "findest"),
        conj("finden", "er", "findet"),
        mc(
            "Ich finde die Lampe schön. You agree:",
            "Das finde ich auch.",
            "Das finde ich nicht.",
            "Findest du?",
        ),
        mc(
            "Ich finde den Tisch hässlich. You disagree:",
            "Das finde ich nicht.",
            "Das finde ich auch.",
            "Ja, genau.",
        ),
        fill("Wie ___ du das Sofa? (finden)", "findest"),
        order("Ich finde den Schrank sehr praktisch."),
        tr("I find the armchair really great.", "Ich finde den Sessel wirklich toll."),
    ),
    lesson(
        "Lektion 4: Test",
        mc("___ Bett ist neu.", "Das", "Der", "Die"),
        mc("Die Couch? ___ ist bequem.", "Sie", "Er", "Es"),
        fill("Der Stuhl ist nicht leicht. Er ist ___. (heavy)", "schwer"),
        mc(
            "2.450 in words:",
            "zweitausendvierhundertfünfzig",
            "zweitausendvierhundertfünfundzwanzig",
            "zweivierfünfzig",
        ),
        tr("The lamp costs 30 euros.", "Die Lampe kostet dreißig Euro.|Die Lampe kostet 30 Euro."),
        order("Wie findest du das Zimmer?", "Build the question."),
        mc("Which is NOT furniture?", "der Preis", "der Schrank", "das Sofa", "der Sessel"),
    ),
]

LEKTION_4 = unit(
    4,
    "Der Tisch ist schön!",
    "Möbel und Preise",
    L4_WORDS,
    L4_RULES,
    sections(L4_LESSONS, vocab_lessons(L4_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 5: Was ist das? Das ist ein F.
# ============================================================================

L5_WORDS = [
    ("the pen", "der Stift", "noun", "Pl. die Stifte"),
    ("the pencil", "der Bleistift", "noun", "Pl. die Bleistifte"),
    ("the ballpoint pen", "der Kugelschreiber", "noun", "Pl. die Kugelschreiber"),
    ("the key", "der Schlüssel", "noun", "Pl. die Schlüssel"),
    ("the bag", "die Tasche", "noun", "Pl. die Taschen"),
    ("the clock / watch", "die Uhr", "noun", "Pl. die Uhren"),
    ("the glasses", "die Brille", "noun", "Pl. die Brillen"),
    ("the book", "das Buch", "noun", "Pl. die Bücher"),
    ("the notebook", "das Notizbuch", "noun", "Pl. die Notizbücher"),
    ("the paper", "das Papier", "noun"),
    ("the photo", "das Foto", "noun", "Pl. die Fotos"),
    ("the stamp", "die Briefmarke", "noun", "Pl. die Briefmarken"),
    ("the newspaper", "die Zeitung", "noun", "Pl. die Zeitungen"),
    ("the letter (mail)", "der Brief", "noun", "Pl. die Briefe"),
    ("the wood", "das Holz", "noun"),
    ("the glass (material)", "das Glas", "noun", "Pl. die Gläser (drinking glasses)"),
    ("the metal", "das Metall", "noun"),
    ("the plastic", "das Plastik", "noun"),
    ("the colour", "die Farbe", "noun", "Pl. die Farben"),
    ("red", "rot", "adjective"),
    ("blue", "blau", "adjective"),
    ("yellow", "gelb", "adjective"),
    ("green", "grün", "adjective"),
    ("brown", "braun", "adjective"),
    ("black", "schwarz", "adjective"),
    ("white", "weiß", "adjective"),
    ("grey", "grau", "adjective"),
    ("round", "rund", "adjective"),
    ("angular / square", "eckig", "adjective"),
    ("new", "neu", "adjective"),
    ("no / not a", "kein", "other", "kein / keine"),
    ("What is that?", "Was ist das?", "phrase"),
    ("What is that called in German?", "Wie heißt das auf Deutsch?", "phrase"),
    ("How do you spell that?", "Wie schreibt man das?", "phrase"),
    ("Once more, please.", "Noch einmal, bitte.", "phrase"),
    ("Many thanks.", "Vielen Dank.", "phrase"),
    ("You're welcome. / Here you are.", "Bitte schön.", "phrase"),
    ("No problem.", "Kein Problem.", "phrase"),
]

L5_RULES = [
    rule(
        "ein, eine",
        "articles",
        """
**ein / eine** means "a / an". Use it for something new or not specific.

| masculine | neuter | feminine | plural |
|---|---|---|---|
| **ein** Stift | **ein** Buch | **eine** Tasche | (no article) Bücher |

Something already known gets **der / das / die**:
*Das ist **ein** Schlüssel. **Der** Schlüssel ist neu.*
""",
        [
            "Was ist das? Das ist eine Uhr.",
            "Das ist ein Buch. Das Buch ist rot.",
            "Das sind Briefmarken.",
        ],
    ),
    rule(
        "kein, keine",
        "articles",
        """
**kein / keine** means "no / not a". It negates a noun with *ein* or no article.

| masculine | neuter | feminine | plural |
|---|---|---|---|
| **kein** Stift | **kein** Buch | **keine** Tasche | **keine** Bücher |

- *Das ist **kein** Bleistift, das ist ein Kugelschreiber.*
- *Das sind **keine** Fotos.*
""",
        ["Ist das eine Uhr? Nein, das ist keine Uhr.", "Das ist kein Holz, das ist Plastik."],
    ),
    rule(
        "Plural",
        "articles",
        """
Plural endings vary, so learn each noun's plural with it. The plural article is always **die**.

| ending | example |
|---|---|
| -e | der Stift → die Stift**e** |
| ¨-e | der Stuhl → die St**ü**hl**e** |
| -(e)n | die Tasche → die Tasche**n**, die Uhr → die Uhr**en** |
| -s | das Foto → die Foto**s** |
| ¨-er | das Buch → die B**ü**ch**er** |
| no ending | der Schlüssel → die Schlüssel |

Feminine nouns very often take **-(e)n**; words from English often take **-s**.
""",
        ["Ich habe zwei Bücher.", "Die Taschen sind neu.", "Wo sind die Schlüssel?"],
    ),
]

L5_LESSONS = [
    lesson(
        "Was ist das?",
        review("Was ist das?"),
        grammar("ein, eine"),
        mc("Das ist ___ Stift.", "ein", "eine"),
        mc("Das ist ___ Tasche.", "eine", "ein"),
        mc("Das ist ___ Buch.", "ein", "eine"),
        fill("Was ist das? Das ist ___ Uhr.", "eine"),
        fill("Das ist ___ Schlüssel.", "ein"),
        fill("Das ist ___ Brille.", "eine"),
        tr("That is a book.", "Das ist ein Buch."),
    ),
    lesson(
        "ein oder der?",
        mc("Das ist ein Foto. ___ Foto ist schön.", "Das", "Ein", "Der"),
        mc("Das ist eine Lampe. ___ Lampe ist neu.", "Die", "Eine", "Der"),
        fill("Das ist ein Kugelschreiber. ___ Kugelschreiber ist blau.", "Der"),
        fill("Das ist eine Zeitung. ___ Zeitung ist von heute.", "Die"),
        bank(
            "Das ist ___ Notizbuch. ___ Notizbuch ist rot. Und das ist ___ Brief.",
            ["ein", "Das", "ein"],
            "eine",
            "Der",
        ),
        order("Das ist ein Bleistift."),
        tr("That is a key. The key is new.", "Das ist ein Schlüssel. Der Schlüssel ist neu."),
    ),
    lesson(
        "kein, keine",
        grammar("kein, keine"),
        mc("Ist das ein Stift? Nein, das ist ___ Stift.", "kein", "keine"),
        mc("Ist das eine Uhr? Nein, das ist ___ Uhr.", "keine", "kein"),
        mc("Sind das Briefmarken? Nein, das sind ___ Briefmarken.", "keine", "kein"),
        fill("Das ist ___ Buch, das ist ein Notizbuch.", "kein"),
        fill("Das ist ___ Tasche, das ist eine Brille.", "keine"),
        order("Das ist kein Bleistift."),
        tr("That is not a newspaper.", "Das ist keine Zeitung."),
        mc(
            "Which sentence is correct?",
            "Das ist keine Lampe.",
            "Das ist nicht eine Lampe.",
            "Das ist kein Lampe.",
        ),
    ),
    lesson(
        "Farben",
        review("die Farbe"),
        match(
            [
                ("rot", "red"),
                ("blau", "blue"),
                ("gelb", "yellow"),
                ("grün", "green"),
                ("schwarz", "black"),
                ("weiß", "white"),
            ]
        ),
        mc("Das Gras ist …", "grün", "rot", "blau"),
        mc("Die Sonne ist …", "gelb", "schwarz", "grün"),
        mc("Kaffee ist …", "braun", "weiß", "gelb"),
        fill("Milch ist ___. (white)", "weiß"),
        order("Der Kugelschreiber ist blau."),
        tr("The bag is black.", "Die Tasche ist schwarz."),
    ),
    lesson(
        "Holz, Glas, Metall",
        match(
            [
                ("das Holz", "wood"),
                ("das Glas", "glass"),
                ("das Metall", "metal"),
                ("das Plastik", "plastic"),
            ]
        ),
        mc("Ein Bleistift ist meistens aus …", "Holz", "Glas", "Metall"),
        mc("Eine Brille ist oft aus Glas und …", "Plastik", "Papier", "Holz"),
        mc("Die Uhr ist nicht eckig. Sie ist …", "rund", "lang", "grün"),
        fill("Der Schlüssel ist aus ___. (metal)", "Metall"),
        fill("Das Buch ist nicht rund. Es ist ___. (angular)", "eckig"),
        bank(
            "Das ist eine Brille. Sie ist ___ und ___. Sie ist aus ___.",
            ["rund", "schwarz", "Plastik"],
            "eckig",
            "Holz",
            prompt="Describe the glasses: round, black, made of plastic.",
        ),
    ),
    lesson(
        "Plural",
        grammar("Plural"),
        mc("der Stift, die …", "Stifte", "Stiften", "Stifts"),
        mc("das Buch, die …", "Bücher", "Buchs", "Buchen"),
        mc("die Tasche, die …", "Taschen", "Tasches", "Täsche"),
        mc("das Foto, die …", "Fotos", "Fotoen", "Föter"),
        fill("die Uhr, die ___", "Uhren"),
        fill("der Schlüssel, die ___", "Schlüssel"),
        fill("die Briefmarke, die ___", "Briefmarken"),
        fill("das Notizbuch, die ___", "Notizbücher"),
        mc("der Stuhl, die …", "Stühle", "Stuhle", "Stühlen"),
    ),
    lesson(
        "Plural üben",
        match(
            [
                ("der Brief", "die Briefe"),
                ("die Zeitung", "die Zeitungen"),
                ("die Brille", "die Brillen"),
                ("der Bleistift", "die Bleistifte"),
                ("der Tisch", "die Tische"),
            ],
            "Match singular and plural.",
        ),
        fill("Ich habe zwei ___. (Buch)", "Bücher"),
        fill("Wo sind die ___? (Schlüssel)", "Schlüssel"),
        fill("Die ___ sind neu. (Lampe)", "Lampen"),
        order("Das sind keine Fotos."),
        tr("The bags are red.", "Die Taschen sind rot."),
    ),
    lesson(
        "Wie heißt das auf Deutsch?",
        review("Wie heißt das auf Deutsch?"),
        mc(
            "You don't know the German word. You ask:",
            "Wie heißt das auf Deutsch?",
            "Wie geht's?",
            "Wo wohnst du?",
        ),
        mc(
            "You didn't hear well. You say:", "Noch einmal, bitte.", "Vielen Dank.", "Kein Problem."
        ),
        mc(
            "You want the spelling. You ask:",
            "Wie schreibt man das?",
            "Was kostet das?",
            "Wer ist das?",
        ),
        mc(
            "Someone says Vielen Dank! You answer:",
            "Bitte schön.",
            "Noch einmal, bitte.",
            "Wie bitte?",
        ),
        bank(
            "Wie heißt das auf ___? Das ist ein Radiergummi. ___ schreibt man das? R-A-D-I-E-R-G-U-M-M-I. "
            "Vielen ___! Kein ___.",
            ["Deutsch", "Wie", "Dank", "Problem"],
            "Englisch",
            "Was",
        ),
        order("Wie schreibt man das?", "Build the question."),
    ),
    lesson(
        "Lektion 5: Test",
        mc("Das ist ___ Brille.", "eine", "ein", "kein"),
        fill("Das ist kein Tisch, das ist ___ Stuhl.", "ein"),
        fill("die Farbe, die ___", "Farben"),
        mc("Ist das Papier? Nein, das ist ___ Papier.", "kein", "keine", "nicht"),
        tr("Those are not keys.", "Das sind keine Schlüssel."),
        mc("Which colour is grau?", "grey", "green", "brown"),
        order("Die Uhr ist rund und weiß."),
    ),
]

LEKTION_5 = unit(
    5,
    "Was ist das? Das ist ein F.",
    "Gegenstände, Farben, Plural",
    L5_WORDS,
    L5_RULES,
    sections(L5_LESSONS, vocab_lessons(L5_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 6: Ich brauche kein Büro.
# ============================================================================

L6_WORDS = [
    ("the office", "das Büro", "noun", "Pl. die Büros"),
    ("the workplace / desk job", "der Arbeitsplatz", "noun", "Pl. die Arbeitsplätze"),
    ("the computer", "der Computer", "noun", "Pl. die Computer"),
    ("the laptop", "der Laptop", "noun", "Pl. die Laptops"),
    ("the screen / monitor", "der Bildschirm", "noun", "Pl. die Bildschirme"),
    ("the keyboard", "die Tastatur", "noun", "Pl. die Tastaturen"),
    ("the mouse", "die Maus", "noun", "Pl. die Mäuse"),
    ("the printer", "der Drucker", "noun", "Pl. die Drucker"),
    ("the telephone", "das Telefon", "noun", "Pl. die Telefone"),
    ("the mobile phone", "das Handy", "noun", "Pl. die Handys"),
    ("the desk", "der Schreibtisch", "noun", "Pl. die Schreibtische"),
    ("the folder / binder", "der Ordner", "noun", "Pl. die Ordner"),
    ("the calendar", "der Kalender", "noun", "Pl. die Kalender"),
    ("the bill / invoice", "die Rechnung", "noun", "Pl. die Rechnungen"),
    ("the form (to fill in)", "das Formular", "noun", "Pl. die Formulare"),
    ("the appointment", "der Termin", "noun", "Pl. die Termine"),
    ("the company", "die Firma", "noun", "Pl. die Firmen"),
    ("the boss", "der Chef", "noun", "f. die Chefin"),
    ("the e-mail", "die E-Mail", "noun", "Pl. die E-Mails"),
    ("the text message", "die SMS", "noun", "Pl. die SMS"),
    ("the greeting", "der Gruß", "noun", "Pl. die Grüße"),
    ("the stress", "der Stress", "noun"),
    ("to need", "brauchen", "verb"),
    ("to look for", "suchen", "verb"),
    ("today", "heute", "adverb"),
    ("here", "hier", "adverb"),
    ("Watch out! / Attention!", "Achtung!", "phrase"),
    ("Best wishes (end of a message)", "Schöne Grüße", "phrase"),
    ("This is … speaking. (on the phone)", "Hier ist …", "phrase"),
    ("I have a question.", "Ich habe eine Frage.", "phrase"),
]

L6_RULES = [
    rule(
        "Akkusativ",
        "cases",
        """
The **direct object** (what you need, have, look for) is in the accusative.
Only the **masculine** article changes:

| | nominative | accusative |
|---|---|---|
| masculine | der / ein / kein Drucker | **den / einen / keinen** Drucker |
| neuter | das / ein / kein Büro | das / ein / kein Büro |
| feminine | die / eine / keine Maus | die / eine / keine Maus |
| plural | die / – / keine Ordner | die / – / keine Ordner |

Verbs that take the accusative here: **brauchen, haben, suchen, finden**.
""",
        [
            "Ich brauche einen Computer.",
            "Ich suche den Kalender.",
            "Wir haben kein Büro.",
            "Hast du eine Maus?",
        ],
    ),
    rule(
        "kein oder nicht?",
        "sentence_structure",
        """
- **kein** negates a **noun** that would have *ein* or no article:
  *Ich habe **keinen** Laptop. Wir haben **keine** Zeit. Das ist **kein** Problem.*
- **nicht** negates everything else: a verb, an adjective, a noun with *der/das/die*:
  *Ich arbeite heute **nicht**. Der Drucker ist **nicht** neu. Ich finde **den** Schlüssel **nicht**.*
""",
        [
            "Ich brauche keinen Drucker.",
            "Der Computer ist nicht teuer.",
            "Ich finde die Rechnung nicht.",
        ],
    ),
    rule(
        "Am Telefon",
        "other",
        """
- Start a call with your name: ***Hier ist** Müller.* / *Guten Tag, hier ist Anna Roth.*
- Answer the phone: *Firma Becker, Weber, guten Tag.*
- Ask: *Ich habe eine Frage.* / *Ist Frau Schmidt da?*
- End: ***Auf Wiederhören!*** (not *Auf Wiedersehen*, because you don't see each other)

End a written message with **Schöne Grüße** or **Viele Grüße** + your name.
""",
        [
            "Guten Tag, hier ist Jonas Becker.",
            "Vielen Dank! Auf Wiederhören.",
            "Schöne Grüße, Anna",
        ],
    ),
]

L6_LESSONS = [
    lesson(
        "Im Büro",
        review("das Büro"),
        review("der Computer"),
        match(
            [
                ("der Bildschirm", "you look at it"),
                ("die Tastatur", "you type on it"),
                ("der Drucker", "it prints"),
                ("das Handy", "you call with it"),
                ("der Kalender", "it shows the dates"),
            ]
        ),
        mc("You keep papers in a …", "Ordner", "Drucker", "Termin"),
        mc("A company sends you a …", "Rechnung", "Maus", "Tastatur"),
        mc("You fill in a …", "Formular", "Bildschirm", "Gruß"),
        fill("Der Laptop ist auf dem ___. (desk)", "Schreibtisch"),
    ),
    lesson(
        "Akkusativ",
        grammar("Akkusativ"),
        mc("Ich brauche ___ Drucker. (a)", "einen", "ein", "eine"),
        mc("Ich brauche ___ Büro. (a)", "ein", "einen", "eine"),
        mc("Ich brauche ___ Maus. (a)", "eine", "einen", "ein"),
        mc("Ich suche ___ Kalender. (the)", "den", "der", "das"),
        mc("Ich suche ___ Rechnung. (the)", "die", "den", "der"),
        fill("Hast du ___ Laptop? (a)", "einen"),
        fill("Wir suchen ___ Chef. (the)", "den"),
        fill("Sie hat ___ Handy. (a)", "ein"),
    ),
    lesson(
        "den, einen, keinen",
        fill("Ich habe ___ Computer. (no)", "keinen"),
        fill("Wir haben ___ Drucker. (no)", "keinen"),
        fill("Ich brauche ___ Formular. (no)", "kein"),
        fill("Er hat ___ Zeit. (no)", "keine"),
        mc("Der Bildschirm ist neu. Ich finde ___ Bildschirm toll.", "den", "der", "einen"),
        mc(
            "Which sentence is correct?",
            "Ich suche den Schlüssel.",
            "Ich suche der Schlüssel.",
            "Ich suche dem Schlüssel.",
        ),
        bank(
            "Ich brauche ___ Laptop, ___ Maus und ___ Bildschirm.",
            ["einen", "eine", "einen"],
            "ein",
            "der",
        ),
        tr("I need a printer.", "Ich brauche einen Drucker."),
        tr("We don't have a computer.", "Wir haben keinen Computer."),
    ),
    lesson(
        "Was brauchst du?",
        review("brauchen"),
        conj("brauchen", "du", "brauchst"),
        conj("suchen", "er", "sucht"),
        conj("brauchen", "ihr", "braucht"),
        order("Was brauchst du?", "Build the question."),
        order("Ich brauche keinen Kalender."),
        order("Wir suchen eine Firma in Berlin."),
        mc("Was brauchst du? Which answer fits?", "Einen Stift, bitte.", "Ja, gern.", "In Köln."),
        tr("He is looking for the key.", "Er sucht den Schlüssel."),
    ),
    lesson(
        "kein oder nicht?",
        grammar("kein oder nicht?"),
        mc("Ich arbeite heute ___.", "nicht", "kein"),
        mc("Ich habe ___ Termin.", "keinen", "nicht"),
        mc("Der Drucker ist ___ teuer.", "nicht", "kein"),
        mc("Das ist ___ Problem.", "kein", "nicht"),
        fill("Wir haben ___ Büro. Wir arbeiten zu Hause.", "kein"),
        fill("Ich finde den Ordner ___.", "nicht"),
        fill("Das Handy ist ___ neu.", "nicht"),
        tr("I don't have time today.", "Ich habe heute keine Zeit.|Heute habe ich keine Zeit."),
    ),
    lesson(
        "Termine und Nachrichten",
        review("der Termin"),
        bank(
            "Hallo Paul, der ___ mit Frau Weber ist ___ um 10 Uhr. Bitte bring die ___ mit. "
            "Schöne ___, Lisa",
            ["Termin", "heute", "Rechnung", "Grüße"],
            "Gruß",
            "hier",
        ),
        mc("How do you end a short message?", "Schöne Grüße", "Guten Morgen", "Achtung!"),
        mc("Achtung! means:", "Watch out!", "Thank you!", "Goodbye!"),
        fill("Ich schreibe eine ___ an den Chef. (e-mail)", "E-Mail"),
        tr("The appointment is today.", "Der Termin ist heute."),
        order("Ich habe heute viel Stress."),
    ),
    lesson(
        "Am Telefon",
        grammar("Am Telefon"),
        mc(
            "You call a company. You start with:",
            "Guten Tag, hier ist Anna Roth.",
            "Auf Wiederhören, Anna Roth.",
            "Tschüs, hier Anna.",
        ),
        mc(
            "You end a phone call politely:",
            "Vielen Dank. Auf Wiederhören!",
            "Vielen Dank. Auf Wiedersehen!",
            "Gute Nacht!",
        ),
        bank(
            "Firma Becker, guten Tag. Guten Tag, ___ ist Müller. Ich habe eine ___. "
            "Ist Frau Schmidt ___? Nein, leider nicht. Gut, vielen Dank. Auf ___!",
            ["hier", "Frage", "da", "Wiederhören"],
            "Wiedersehen",
            "Termin",
        ),
        order("Ich habe eine Frage."),
        tr("This is Peter Klein speaking.", "Hier ist Peter Klein."),
    ),
    lesson(
        "Lektion 6: Test",
        mc("Ich brauche ___ Tastatur.", "eine", "einen", "ein"),
        fill("Hast du ___ Kalender? (a)", "einen"),
        fill("Ich habe ___ Handy. (no)", "kein"),
        mc("Der Computer funktioniert ___.", "nicht", "kein"),
        mc("die Maus, die …", "Mäuse", "Mause", "Mäusen"),
        tr("I am looking for the printer.", "Ich suche den Drucker."),
        order("Wir brauchen keinen Chef."),
    ),
    lesson(
        "Modul 2: Wiederholung",
        mc("___ Sofa ist modern.", "Das", "Der", "Die"),
        mc("Der Schrank? ___ ist zu groß.", "Er", "Es", "Sie"),
        fill("Das ist kein Stift, das ist ___ Schlüssel.", "ein"),
        fill("das Buch, die ___", "Bücher"),
        mc("Ich brauche ___ Stuhl.", "einen", "ein", "eine"),
        mc("Ich habe ___ Zeit.", "keine", "nicht", "kein"),
        bank(
            "Was ___ der Tisch? Er kostet 120 Euro. Das ist ___ teuer! Brauchen Sie ___ Tisch? "
            "Nein, ich brauche ___ Stuhl.",
            ["kostet", "zu", "einen", "einen"],
            "ein",
            "nicht",
        ),
        tr("The lamp is not expensive.", "Die Lampe ist nicht teuer."),
        order("Ich finde die Uhr sehr schön."),
        mc(
            "4.500 in words:", "viertausendfünfhundert", "vierhundertfünftausend", "vierfünfhundert"
        ),
    ),
]

LEKTION_6 = unit(
    6,
    "Ich brauche kein Büro.",
    "Büro und Akkusativ",
    L6_WORDS,
    L6_RULES,
    sections(L6_LESSONS, vocab_lessons(L6_WORDS, "Wörter")),
)


UNITS = [LEKTION_4, LEKTION_5, LEKTION_6]
