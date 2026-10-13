"""Modul 7 (A1.2): Lektion 19 (Der hatte doch keinen Bauch!), 20 (Komm sofort
runter!), 21 (Bei Rot musst du stehen, bei Grün darfst du gehen)."""

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
# Lektion 19: Der hatte doch keinen Bauch!
# ============================================================================

L19_WORDS = [
    ("the appearance", "das Aussehen", "noun"),
    ("the character / personality", "der Charakter", "noun", "Pl. die Charaktere"),
    ("the beard", "der Bart", "noun", "Pl. die Bärte"),
    ("the hair", "die Haare", "noun", "plural: Er hat kurze Haare."),
    ("blond", "blond", "adjective"),
    ("fat", "dick", "adjective"),
    ("slim", "schlank", "adjective"),
    ("thin", "dünn", "adjective"),
    ("pretty", "hübsch", "adjective"),
    ("young", "jung", "adjective"),
    ("likeable", "sympathisch", "adjective"),
    ("unlikeable", "unsympathisch", "adjective"),
    ("friendly", "freundlich", "adjective"),
    ("unfriendly", "unfreundlich", "adjective"),
    ("cheerful", "fröhlich", "adjective"),
    ("sad", "traurig", "adjective"),
    ("unhappy", "unglücklich", "adjective"),
    ("odd / funny (strange)", "komisch", "adjective"),
    ("quiet / calm", "ruhig", "adjective"),
    ("to recognise", "erkennen", "verb", "hat erkannt"),
    ("to forget", "vergessen", "verb", "du vergisst; hat vergessen"),
    ("to apologise / to excuse", "entschuldigen", "verb", "sich entschuldigen; hat entschuldigt"),
    ("to complain", "beschweren", "verb", "sich beschweren; hat beschwert"),
    ("to tell (a story)", "erzählen", "verb", "hat erzählt"),
    ("to understand", "verstehen", "verb", "hat verstanden"),
    ("in the past / formerly", "früher", "adverb"),
    ("now", "jetzt", "adverb"),
    ("Oh, come on!", "Ach komm!", "phrase"),
    ("Really?", "Echt?", "phrase"),
    ("Amazing! / Crazy!", "Wahnsinn!", "phrase"),
    ("Oh dear!", "Ach du liebe Zeit!", "phrase"),
]

L19_RULES = [
    rule(
        "war und hatte",
        "verbs",
        """
For **sein** and **haben**, German usually uses the simple past (**Präteritum**), not the Perfekt:

| | sein | haben |
|---|---|---|
| ich | war | hatte |
| du | warst | hattest |
| er / sie | war | hatte |
| wir | waren | hatten |
| ihr | wart | hattet |
| sie / Sie | waren | hatten |

*ich* and *er/sie* have the same form: *Ich war müde. Er war müde.*
""",
        ["Früher hatte er lange Haare.", "Sie war Sekretärin.", "Wir hatten keine Zeit."],
    ),
    rule(
        "Partizip ohne ge-",
        "verbs",
        """
Verbs that start with **be-, emp-, ent-, er-, ge-, ver-, zer-** get **no ge-** in the Partizip II:

| infinitive | Partizip II |
|---|---|
| erkennen | erkannt |
| erzählen | erzählt |
| entschuldigen | entschuldigt |
| beschweren | beschwert |
| bekommen | bekommen |
| besuchen | besucht |
| bezahlen | bezahlt |
| vergessen | vergessen |
| verstehen | verstanden |
| gefallen | gefallen |

These prefixes are never separated and never stressed: *verGESsen, beKOMmen*.
""",
        [
            "Ich habe dich nicht erkannt!",
            "Er hat seinen Schlüssel vergessen.",
            "Die Nachbarn haben sich beschwert.",
        ],
    ),
    rule(
        "un- und Aussehen",
        "adjectives",
        """
**un-** turns many adjectives into their opposite:
*freundlich → **un**freundlich, glücklich → **un**glücklich, sympathisch → **un**sympathisch*

Describing people:
- *Er **hat** einen Bart / kurze Haare / blaue Augen.*
- *Sie **ist** schlank / blond / sehr freundlich.*
- *Er **sieht** sympathisch **aus**.* (He looks likeable.)
""",
        [
            "Früher war er ein bisschen dick.",
            "Sie sieht sehr fröhlich aus.",
            "Der Kellner war unfreundlich.",
        ],
    ),
]

L19_LESSONS = [
    lesson(
        "Aussehen",
        review("das Aussehen"),
        review("der Bart"),
        match(
            [
                ("dick", "schlank"),
                ("jung", "alt"),
                ("fröhlich", "traurig"),
                ("freundlich", "unfreundlich"),
                ("glücklich", "unglücklich"),
            ],
            "Match the opposites.",
        ),
        mc("He has hair on his chin and cheeks. He has a …", "Bart", "Brille", "Bauch"),
        mc("Her hair is very light, almost yellow. She is …", "blond", "schlank", "traurig"),
        fill("Er ___ einen Bart und kurze Haare. (haben)", "hat"),
        fill("Sie ___ sehr freundlich aus. (aussehen)", "sieht"),
    ),
    lesson(
        "war und hatte",
        grammar("war und hatte"),
        conj("sein (Präteritum)", "ich", "war"),
        conj("sein (Präteritum)", "du", "warst"),
        conj("sein (Präteritum)", "wir", "waren"),
        conj("sein (Präteritum)", "ihr", "wart"),
        conj("haben (Präteritum)", "ich", "hatte"),
        conj("haben (Präteritum)", "du", "hattest"),
        conj("haben (Präteritum)", "er", "hatte"),
        conj("haben (Präteritum)", "ihr", "hattet"),
    ),
    lesson(
        "Früher und heute",
        fill("Früher ___ er einen Bart. Heute hat er keinen. (haben)", "hatte"),
        fill("Früher ___ sie Sekretärin. Heute ist sie Chefin. (sein)", "war"),
        fill("Wo ___ du gestern? (sein)", "warst"),
        fill("Wir ___ keine Zeit. (haben)", "hatten"),
        mc("Früher ___ ich lange Haare.", "hatte", "war", "habe"),
        mc("Früher ___ er dick. Jetzt ist er schlank.", "war", "hatte", "ist"),
        order("Früher war er ein bisschen dick."),
        tr("Yesterday I was tired.", "Gestern war ich müde.|Ich war gestern müde."),
        tr("We had a dog.", "Wir hatten einen Hund."),
    ),
    lesson(
        "erkannt, vergessen",
        grammar("Partizip ohne ge-"),
        fill("erkennen → ___", "erkannt"),
        fill("vergessen → ___", "vergessen"),
        fill("bekommen → ___", "bekommen"),
        fill("entschuldigen → ___", "entschuldigt"),
        fill("verstehen → ___", "verstanden"),
        fill("erzählen → ___", "erzählt"),
        mc(
            "Which is correct?",
            "Ich habe dich nicht erkannt.",
            "Ich habe dich nicht geerkannt.",
            "Ich habe dich nicht erkennt.",
        ),
        mc(
            "Which is correct?",
            "Er hat das Geld bekommen.",
            "Er hat das Geld gebekommen.",
            "Er hat das Geld bekommt.",
        ),
        tr("I forgot my key.", "Ich habe meinen Schlüssel vergessen."),
    ),
    lesson(
        "Ach komm! Echt?",
        review("Echt?"),
        mc("You can't believe it. You say:", "Echt?", "Gute Besserung!", "Bis bald!"),
        mc("Something is amazing. You say:", "Wahnsinn!", "Schade!", "Ach so."),
        bank(
            "Schau mal, das ist Paul! ___ Paul? Der ___ doch keinen Bauch! Ja, ___ war er "
            "schlank. Heute ist er ein bisschen ___.",
            ["Echt?", "hatte", "früher", "dick"],
            "war",
            "jetzt",
        ),
        order("Wir haben uns lange nicht gesehen."),
        tr("He looks likeable.", "Er sieht sympathisch aus."),
    ),
    lesson(
        "Wie ist er? Wie sieht er aus?",
        grammar("un- und Aussehen"),
        mc("The opposite of sympathisch:", "unsympathisch", "nicht sympathisch", "ohnesympathisch"),
        fill("Der Kellner war nicht freundlich. Er war ___.", "unfreundlich"),
        fill("Sie ist nicht glücklich. Sie ist ___.", "unglücklich"),
        mc("Er ___ blaue Augen.", "hat", "ist", "sieht"),
        mc("Sie ___ sehr schlank.", "ist", "hat", "aussieht"),
        order("Mein Opa sieht sehr fröhlich aus."),
        tr("My sister has long hair.", "Meine Schwester hat lange Haare."),
    ),
    lesson(
        "Lektion 19: Test",
        mc("Gestern ___ ich krank.", "war", "hatte", "bin"),
        fill("Ihr ___ viel Glück! (haben, Präteritum)", "hattet"),
        fill("besuchen → ___", "besucht"),
        mc("The opposite of fröhlich:", "traurig", "freundlich", "ruhig"),
        order("Hast du ihn sofort erkannt?", "Build the question."),
        tr("She was a teacher.", "Sie war Lehrerin."),
        mc("Ach du liebe Zeit! means:", "Oh dear!", "Dear time!", "Have a nice time!"),
    ),
]

LEKTION_19 = unit(
    19,
    "Der hatte doch keinen Bauch!",
    "Aussehen, Charakter, war und hatte",
    L19_WORDS,
    L19_RULES,
    sections(L19_LESSONS, vocab_lessons(L19_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 20: Komm sofort runter!
# ============================================================================

L20_WORDS = [
    ("the household", "der Haushalt", "noun"),
    ("the housework", "die Hausarbeit", "noun", "Pl. die Hausarbeiten"),
    ("the dishes", "das Geschirr", "noun"),
    ("the laundry", "die Wäsche", "noun"),
    ("the dishwasher", "die Spülmaschine", "noun", "Pl. die Spülmaschinen"),
    ("the floor", "der Boden", "noun", "Pl. die Böden"),
    ("the mess", "die Unordnung", "noun"),
    ("the flatmate", "der Mitbewohner", "noun", "f. die Mitbewohnerin"),
    ("the shared flat", "die Wohngemeinschaft", "noun", "short: die WG"),
    ("the patience", "die Geduld", "noun"),
    ("to set (the table)", "decken", "verb", "den Tisch decken"),
    ("to wash up", "spülen", "verb", "das Geschirr spülen"),
    ("to dry (dishes)", "abtrocknen", "verb"),
    ("to wash", "waschen", "verb", "du wäschst, er wäscht"),
    ("to hang up", "aufhängen", "verb", "die Wäsche aufhängen"),
    ("to iron", "bügeln", "verb"),
    ("to take out", "rausbringen", "verb", "den Müll rausbringen"),
    ("to unload / to empty", "ausräumen", "verb", "die Spülmaschine ausräumen"),
    ("to mop / to wipe", "wischen", "verb", "den Boden wischen"),
    ("to hate", "hassen", "verb"),
    ("down (here)", "runter", "adverb", "Komm runter!"),
    ("tidy / orderly", "ordentlich", "adjective"),
    ("thorough(ly)", "gründlich", "adjective"),
    ("lazy", "faul", "adjective"),
    ("me (accusative)", "mich", "other"),
    ("you (accusative, informal)", "dich", "other"),
    ("him (accusative)", "ihn", "other"),
    ("Be a dear and …", "Sei so lieb und …", "phrase"),
]

L20_RULES = [
    rule(
        "Imperativ mit du",
        "verbs",
        """
To tell **one friend** what to do: take the *du* form, drop **-st** and the word *du*:

| du-form | imperative |
|---|---|
| du machst | **Mach** dein Bett! |
| du deckst | **Deck** den Tisch! |
| du räumst … auf | **Räum** dein Zimmer **auf**! |
| du vergisst | **Vergiss** das nicht! |
| du nimmst | **Nimm** den Müll mit! |
| du liest | **Lies** das! |

- Verbs with **ä** in the du-form drop the umlaut: *du fährst → **Fahr** langsam!*
- Irregular: *sein → **Sei** ruhig!*, *haben → **Hab** Geduld!*
""",
        ["Komm sofort runter!", "Bring bitte den Müll raus!", "Sei doch nicht so faul!"],
    ),
    rule(
        "Imperativ mit ihr",
        "verbs",
        """
To tell **several friends**: the *ihr* form **without** *ihr*:

- *ihr deckt → **Deckt** den Tisch!*
- *ihr räumt … aus → **Räumt** die Spülmaschine **aus**!*
- *ihr vergesst → **Vergesst** die Hausaufgaben nicht!*
- *sein → **Seid** leise!*, *haben → **Habt** Geduld!*

Soften any command with **bitte, doch, mal**: *Hilf mir **doch mal**!*
""",
        ["Kommt bitte essen!", "Spült das Geschirr!", "Seid nicht so laut!"],
    ),
    rule(
        "Personalpronomen im Akkusativ",
        "pronouns",
        """
| nominative | ich | du | er | es | sie | wir | ihr | sie / Sie |
|---|---|---|---|---|---|---|---|---|
| accusative | **mich** | **dich** | **ihn** | es | sie | uns | euch | sie / Sie |

- *Holst du **mich** ab?* (Will you pick me up?)
- *Kennst du Paul? Ja, ich kenne **ihn**.*
- *Wo ist die Wäsche? Ich habe **sie** aufgehängt.*

Compare the dative: *mir, dir, ihm*.
""",
        [
            "Ich rufe dich morgen an.",
            "Der Müll? Bring ihn bitte raus!",
            "Wir besuchen euch am Sonntag.",
        ],
    ),
]

L20_LESSONS = [
    lesson(
        "Hausarbeit",
        review("der Haushalt"),
        review("das Geschirr"),
        match(
            [
                ("den Tisch decken", "before the meal"),
                ("das Geschirr spülen", "after the meal"),
                ("die Wäsche waschen", "dirty clothes"),
                ("bügeln", "smooth shirts"),
                ("den Müll rausbringen", "full bin"),
            ]
        ),
        mc("Your room is a mess. You have to …", "aufräumen", "bügeln", "decken"),
        mc("Er macht nie Hausarbeit. Er ist …", "faul", "gründlich", "ordentlich"),
        conj("waschen", "du", "wäschst"),
        conj("waschen", "er", "wäscht"),
    ),
    lesson(
        "Imperativ mit du",
        grammar("Imperativ mit du"),
        fill("Du machst dein Bett. → ___ dein Bett!", "Mach"),
        fill("Du deckst den Tisch. → ___ den Tisch!", "Deck"),
        fill("Du vergisst den Schlüssel nicht. → ___ den Schlüssel nicht!", "Vergiss"),
        fill("Du nimmst den Müll mit. → ___ den Müll mit!", "Nimm"),
        fill("Du bist ruhig. → ___ ruhig!", "Sei"),
        fill("Du fährst langsam. → ___ langsam!", "Fahr"),
        mc(
            "Du räumst dein Zimmer auf. →",
            "Räum dein Zimmer auf!",
            "Aufräum dein Zimmer!",
            "Räumst dein Zimmer auf!",
        ),
        order("Komm sofort runter!"),
    ),
    lesson(
        "Imperativ mit ihr",
        grammar("Imperativ mit ihr"),
        fill("Ihr deckt den Tisch. → ___ den Tisch!", "Deckt"),
        fill("Ihr seid leise. → ___ leise!", "Seid"),
        fill("Ihr vergesst die Hausaufgaben nicht. → ___ die Hausaufgaben nicht!", "Vergesst"),
        fill("Ihr habt Geduld. → ___ Geduld!", "Habt"),
        mc(
            "Ihr räumt die Spülmaschine aus. →",
            "Räumt die Spülmaschine aus!",
            "Ausräumt die Spülmaschine!",
            "Räum die Spülmaschine aus!",
        ),
        mc(
            "To two children: wash your hands!",
            "Wascht eure Hände!",
            "Wasch deine Hände!",
            "Waschen Sie die Hände!",
        ),
        tr("Come and eat, please! (to several friends)", "Kommt bitte essen!|Kommt essen, bitte!"),
    ),
    lesson(
        "mich, dich, ihn",
        grammar("Personalpronomen im Akkusativ"),
        match(
            [
                ("ich", "mich"),
                ("du", "dich"),
                ("er", "ihn"),
                ("wir", "uns"),
                ("ihr (you all)", "euch"),
            ],
            "Match nominative and accusative.",
        ),
        mc("Holst du ___ ab? (me)", "mich", "mir", "ich"),
        mc("Kennst du Paul? Ja, ich kenne ___.", "ihn", "ihm", "er"),
        mc("Die Wäsche? Ich habe ___ aufgehängt.", "sie", "ihr", "ihn"),
        fill("Ich rufe ___ morgen an. (you, informal)", "dich"),
        fill("Wir besuchen ___ am Sonntag. (you all)", "euch"),
        fill("Der Müll? Bring ___ bitte raus!", "ihn"),
        tr("Can you pick me up? (informal)", "Kannst du mich abholen?"),
    ),
    lesson(
        "In der WG",
        review("die Wohngemeinschaft"),
        bank(
            "Hallo Leute! ___ bitte heute die Spülmaschine aus. Und ___ den Müll raus! "
            "Lukas, sei so ___ und wisch den Boden. Danke! Eure Mia",
            ["Räumt", "bringt", "lieb"],
            "Räum",
            "faul",
        ),
        mc("Sei so lieb und … means:", "Be a dear and …", "Be so loving …", "You are so dear …"),
        mc("Ich hasse Unordnung. means:", "I hate mess.", "I love tidying.", "I have a mess."),
        order("Kannst du mir bitte helfen?", "Build the question."),
        order("Hilf mir doch mal!"),
        fill("Er putzt das Bad sehr ___. (thoroughly)", "gründlich"),
    ),
    lesson(
        "Lektion 20: Test",
        fill("Du liest das Buch. → ___ das Buch!", "Lies"),
        fill("Ihr spült das Geschirr. → ___ das Geschirr!", "Spült"),
        mc("Ich sehe ___. (you, informal)", "dich", "dir", "du"),
        mc("To one friend: be quiet!", "Sei ruhig!", "Seid ruhig!", "Bist ruhig!"),
        order("Deck bitte den Tisch!"),
        tr("I'll call you. (informal)", "Ich rufe dich an."),
        mc("die Spülmaschine is a …", "dishwasher", "washing machine", "vacuum cleaner"),
    ),
]

LEKTION_20 = unit(
    20,
    "Komm sofort runter!",
    "Haushalt und Imperativ",
    L20_WORDS,
    L20_RULES,
    sections(L20_LESSONS, vocab_lessons(L20_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 21: Bei Rot musst du stehen, bei Grün darfst du gehen.
# ============================================================================

L21_WORDS = [
    ("the rule", "die Regel", "noun", "Pl. die Regeln"),
    ("the traffic", "der Verkehr", "noun"),
    ("the environment", "die Umwelt", "noun"),
    ("the pedestrian", "der Fußgänger", "noun", "f. die Fußgängerin"),
    ("the cyclist", "der Fahrradfahrer", "noun", "f. die Fahrradfahrerin"),
    ("the driver (car)", "der Autofahrer", "noun", "f. die Autofahrerin"),
    ("the motorcyclist", "der Motorradfahrer", "noun", "f. die Motorradfahrerin"),
    ("the helmet", "der Helm", "noun", "Pl. die Helme"),
    ("the seat belt", "der Gurt", "noun", "Pl. die Gurte"),
    ("the meadow / lawn", "die Wiese", "noun", "Pl. die Wiesen"),
    ("the hospital", "das Krankenhaus", "noun", "Pl. die Krankenhäuser"),
    ("the lead / leash", "die Leine", "noun", "Pl. die Leinen"),
    ("the sign", "das Schild", "noun", "Pl. die Schilder"),
    ("the dog", "der Hund", "noun", "Pl. die Hunde"),
    ("allowed", "erlaubt", "adjective"),
    ("forbidden", "verboten", "adjective"),
    ("quiet (not loud)", "leise", "adjective"),
    ("loud", "laut", "adjective"),
    ("dangerous", "gefährlich", "adjective"),
    ("bad / serious", "schlimm", "adjective"),
    ("okay / acceptable", "in Ordnung", "phrase"),
    ("to push", "schieben", "verb"),
    ("to honk", "hupen", "verb"),
    ("to wear / to carry", "tragen", "verb", "du trägst, er trägt"),
    ("to park", "parken", "verb"),
    ("to pay attention (to)", "achten", "verb", "auf etwas achten"),
    ("must / to have to", "müssen", "verb", "ich muss, du musst"),
    ("may / to be allowed to", "dürfen", "verb", "ich darf, du darfst"),
    ("one / people (in general)", "man", "other", "Man darf hier nicht rauchen."),
    ("for it / in favour", "dafür", "other"),
    ("against it", "dagegen", "other"),
]

L21_RULES = [
    rule(
        "müssen",
        "verbs",
        """
**müssen** = must / to have to:

| ich | du | er / sie | wir | ihr | sie / Sie |
|---|---|---|---|---|---|
| muss | musst | muss | müssen | müsst | müssen |

Like all modal verbs: **müssen** in position 2, the other verb at the end.
*Motorradfahrer **müssen** einen Helm **tragen**.*
""",
        ["Bei Rot musst du stehen.", "Ich muss heute arbeiten.", "Wir müssen leise sein."],
    ),
    rule(
        "dürfen",
        "verbs",
        """
**dürfen** = may / to be allowed to:

| ich | du | er / sie | wir | ihr | sie / Sie |
|---|---|---|---|---|---|
| darf | darfst | darf | dürfen | dürft | dürfen |

- *Bei Grün **darfst** du **gehen**.*
- *Hier **darf** man nicht **parken**.* = Parken ist hier **verboten**.
- *Hier **darf** man **parken**.* = Parken ist hier **erlaubt**.
""",
        [
            "Darf ich hier rauchen?",
            "Im Park dürfen Hunde nicht auf die Wiese.",
            "Kinder dürfen hier spielen.",
        ],
    ),
    rule(
        "man",
        "pronouns",
        """
**man** means people in general (one, you, they). It takes the **er/sie** verb form:

- ***Man muss** in der Bibliothek leise sein.*
- ***Man darf** im Bus nicht essen.*
- *Wie schreibt **man** das?*

Don't confuse **man** (people) with **der Mann** (the man).
""",
        ["Hier darf man nicht schwimmen.", "Im Krankenhaus muss man leise sein."],
    ),
    rule(
        "nicht dürfen oder nicht müssen?",
        "verbs",
        """
These are **not** the same:

- **nicht dürfen** = must not, it is forbidden:
  *Du **darfst** hier **nicht** rauchen.* (Smoking is not allowed.)
- **nicht müssen** = don't have to, it is not necessary:
  *Du **musst** heute **nicht** arbeiten.* (You don't need to work today.)
""",
        ["Wir müssen nicht früh aufstehen. Es ist Sonntag.", "Im Bus darf man nicht essen."],
    ),
]

L21_LESSONS = [
    lesson(
        "Im Verkehr",
        review("die Regel"),
        review("der Verkehr"),
        match(
            [
                ("der Fußgänger", "walks"),
                ("der Fahrradfahrer", "rides a bike"),
                ("der Autofahrer", "drives a car"),
                ("der Motorradfahrer", "rides a motorbike"),
            ],
            "Who does what?",
        ),
        mc("Motorcyclists wear it on their head:", "einen Helm", "einen Gurt", "eine Leine"),
        mc("In the car you put on your …", "Gurt", "Helm", "Schild"),
        mc("A dog walks on a …", "Leine", "Wiese", "Regel"),
        conj("tragen", "du", "trägst"),
        conj("tragen", "er", "trägt"),
    ),
    lesson(
        "müssen",
        grammar("müssen"),
        conj("müssen", "ich", "muss"),
        conj("müssen", "du", "musst"),
        conj("müssen", "wir", "müssen"),
        conj("müssen", "ihr", "müsst"),
        fill("Bei Rot ___ du stehen. (müssen)", "musst"),
        fill("Autofahrer ___ einen Gurt tragen. (müssen)", "müssen"),
        order("Ich muss heute lange arbeiten."),
        tr("I have to go home.", "Ich muss nach Hause gehen.|Ich muss nach Hause."),
    ),
    lesson(
        "dürfen",
        grammar("dürfen"),
        conj("dürfen", "ich", "darf"),
        conj("dürfen", "du", "darfst"),
        conj("dürfen", "er", "darf"),
        conj("dürfen", "ihr", "dürft"),
        fill("Bei Grün ___ du gehen. (dürfen)", "darfst"),
        fill("___ ich hier parken? (dürfen)", "Darf"),
        mc(
            "Parken verboten! =",
            "Hier darf man nicht parken.",
            "Hier muss man parken.",
            "Hier darf man parken.",
        ),
        mc(
            "Rauchen erlaubt =",
            "Hier darf man rauchen.",
            "Hier muss man rauchen.",
            "Hier darf man nicht rauchen.",
        ),
        tr("May I come in?", "Darf ich reinkommen?"),
    ),
    lesson(
        "man",
        grammar("man"),
        mc("In der Bibliothek ___ man leise sein.", "muss", "müssen", "musst"),
        mc("Im Bus ___ man nicht essen.", "darf", "dürfen", "darfst"),
        fill("Hier darf ___ nicht schwimmen. (one)", "man"),
        order("Im Krankenhaus muss man leise sein."),
        order("Hier darf man nicht hupen."),
        tr(
            "You're not allowed to smoke here. (use man)",
            "Hier darf man nicht rauchen.|Man darf hier nicht rauchen.",
        ),
    ),
    lesson(
        "nicht dürfen oder nicht müssen?",
        grammar("nicht dürfen oder nicht müssen?"),
        mc("It's Sunday. Du ___ nicht arbeiten. (not necessary)", "musst", "darfst"),
        mc("Rauchen ist verboten. Du ___ hier nicht rauchen.", "darfst", "musst"),
        mc("Kinder ___ nicht allein über die Straße gehen. (forbidden)", "dürfen", "müssen"),
        mc("Wir haben Zeit. Wir ___ nicht schnell fahren. (not necessary)", "müssen", "dürfen"),
        tr("You don't have to come. (informal)", "Du musst nicht kommen."),
    ),
    lesson(
        "Regeln: Was meinst du?",
        bank(
            "Im Park ___ Hunde nicht auf die Wiese. Sie ___ an der Leine gehen. Ich finde das ___. "
            "Mein Mann ist ___.",
            ["dürfen", "müssen", "richtig", "dagegen"],
            "darf",
            "erlaubt",
        ),
        mc("Ich bin dafür. means:", "I'm in favour.", "I'm against it.", "I'm there."),
        mc("Das ist gefährlich! means:", "That's dangerous!", "That's forbidden!", "That's quiet!"),
        fill("Das ist nicht so ___. Das macht nichts. (bad)", "schlimm"),
        order("Das finde ich nicht in Ordnung."),
        tr("Cyclists have to wear a helmet.", "Fahrradfahrer müssen einen Helm tragen."),
    ),
    lesson(
        "Lektion 21: Test",
        mc("Bei Rot ___ man stehen.", "muss", "darf"),
        fill("___ du heute arbeiten? (müssen)", "Musst"),
        mc("Hier ___ man nicht parken. Das ist verboten.", "darf", "muss"),
        conj("dürfen", "wir", "dürfen"),
        order("Darf ich hier fotografieren?", "Build the question."),
        tr("The music is too loud.", "Die Musik ist zu laut."),
        mc("man takes the verb form of …", "er / sie", "wir", "ich"),
    ),
    lesson(
        "Modul 7: Wiederholung",
        fill("Früher ___ ich keine Brille. (haben)", "hatte"),
        fill("Gestern ___ wir im Kino. (sein)", "waren"),
        fill("vergessen → ___", "vergessen"),
        fill("Du hilfst mir. → ___ mir!", "Hilf"),
        mc("Kennst du meine Schwester? Ja, ich kenne ___.", "sie", "ihr", "ihn"),
        mc("Im Krankenhaus ___ man leise sein.", "muss", "darf"),
        bank(
            "Gestern ___ ich bei meiner Oma. Sie ___ früher Lehrerin. Sie sagt immer: "
            "„___ nicht so faul! Du ___ jeden Tag lernen!“",
            ["war", "war", "Sei", "musst"],
            "hatte",
            "darfst",
        ),
        tr("Can you help me? (informal)", "Kannst du mir helfen?|Hilfst du mir?"),
        order("Hier darf man nicht laut sein."),
    ),
]

LEKTION_21 = unit(
    21,
    "Bei Rot musst du stehen, bei Grün darfst du gehen.",
    "Regeln, müssen und dürfen",
    L21_WORDS,
    L21_RULES,
    sections(L21_LESSONS, vocab_lessons(L21_WORDS, "Wörter")),
)


UNITS = [LEKTION_19, LEKTION_20, LEKTION_21]
