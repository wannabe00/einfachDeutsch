"""Modul 1 (A2.1): Lektion 1 (Mein Opa war auch schon Bäcker.), 2 (Wohin mit
der Kommode?), 3 (Hier finden Sie Ruhe und Erholung.)."""

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
# Lektion 1: Mein Opa war auch schon Bäcker.
# ============================================================================

L1_WORDS = [
    ("the uncle", "der Onkel", "noun", "Pl. die Onkel"),
    ("the aunt", "die Tante", "noun", "Pl. die Tanten"),
    ("the cousin (male)", "der Cousin", "noun", "Pl. die Cousins"),
    ("the cousin (female)", "die Cousine", "noun", "Pl. die Cousinen"),
    ("the father-in-law", "der Schwiegervater", "noun", "Pl. die Schwiegerväter"),
    ("the mother-in-law", "die Schwiegermutter", "noun", "Pl. die Schwiegermütter"),
    ("the baker", "der Bäcker", "noun", "f. die Bäckerin"),
    ("the bakery", "die Bäckerei", "noun", "Pl. die Bäckereien"),
    ("the childhood", "die Kindheit", "noun"),
    ("the youth (time of life)", "die Jugend", "noun"),
    ("the young person", "der Jugendliche", "noun", "Pl. die Jugendlichen"),
    ("the story / history", "die Geschichte", "noun", "Pl. die Geschichten"),
    ("the doll", "die Puppe", "noun", "Pl. die Puppen"),
    ("the thing / matter", "die Sache", "noun", "Pl. die Sachen"),
    ("the game", "das Spiel", "noun", "Pl. die Spiele"),
    ("the joke", "der Witz", "noun", "Pl. die Witze"),
    ("the beginning", "der Anfang", "noun", "am Anfang"),
    ("the end", "das Ende", "noun", "am Ende"),
    ("the conclusion", "der Schluss", "noun", "zum Schluss"),
    ("the point / full stop", "der Punkt", "noun", "Pl. die Punkte"),
    ("the sentence", "der Satz", "noun", "Pl. die Sätze"),
    ("to grow up", "aufwachsen", "verb", "ist aufgewachsen"),
    ("to open", "aufmachen", "verb", "hat aufgemacht"),
    ("to look after / to pay attention", "aufpassen", "verb", "aufpassen auf + Akk."),
    ("to work out (succeed)", "klappen", "verb", "Das hat geklappt."),
    ("to climb", "klettern", "verb", "ist geklettert"),
    ("to call / to shout", "rufen", "verb", "hat gerufen"),
    ("to collect", "sammeln", "verb", "hat gesammelt"),
    ("to argue", "streiten", "verb", "hat gestritten"),
    ("to stay overnight", "übernachten", "verb", "hat übernachtet"),
    ("to sell", "verkaufen", "verb", "hat verkauft"),
    ("to draw", "zeichnen", "verb", "hat gezeichnet"),
    ("to remember", "erinnern", "verb", "sich erinnern an + Akk."),
    ("crazy", "verrückt", "adjective"),
    ("simple", "einfach", "adjective"),
    ("complicated", "kompliziert", "adjective"),
    ("single (not married)", "ledig", "adjective"),
    ("born", "geboren", "adjective", "Ich bin 1990 geboren."),
    ("When I was little, ...", "Als ich klein war, ...", "phrase"),
    ("What was it like for you back then?", "Wie war das früher bei dir?", "phrase"),
]

L1_RULES = [
    rule(
        "Präteritum: war und hatte",
        "verbs",
        """
To describe how things **were** in the past, German mostly uses the Präteritum of
*sein* and *haben*, not the Perfekt:

| | sein | haben |
|---|---|---|
| ich | war | hatte |
| du | warst | hattest |
| er / sie / es | war | hatte |
| wir | waren | hatten |
| ihr | wart | hattet |
| sie / Sie | waren | hatten |

- *ich* and *er/sie/es* have the **same** form: *ich war, er war*.
- For actions, use the Perfekt: *Mein Opa **hat** Brot **verkauft**.*
""",
        [
            "Mein Opa war Bäcker.",
            "Wir hatten früher einen Garten.",
            "Als Kind hatte ich keine Puppe, aber viele Bücher.",
            "Wart ihr gestern zu Hause?",
        ],
    ),
    rule(
        "Possessivartikel im Dativ",
        "articles",
        """
After **mit, bei, von, zu, aus, nach** (and other dative words) the possessive
article takes dative endings:

| | masculine | feminine | neuter | plural |
|---|---|---|---|---|
| Nominativ | mein | meine | mein | meine |
| Akkusativ | meinen | meine | mein | meine |
| Dativ | **meinem** | **meiner** | **meinem** | **meinen** + -n |

The same endings work for *dein, sein, ihr, unser, euer, Ihr*:
*mit **unserem** Onkel, bei **eurer** Tante, mit **ihren** Kindern*.

*euer* drops an **e** when it gets an ending: *eure, eurem, eurer*.
""",
        [
            "Ich wohne bei meiner Tante.",
            "Er spricht oft mit seinem Opa.",
            "Wir fahren mit unseren Kindern ans Meer.",
            "Wie geht es eurer Cousine?",
        ],
    ),
    rule(
        "Zeitangaben: früher, damals, als Kind",
        "sentence_structure",
        """
Time words set the scene for a story. In a main clause the **verb stays in
position 2**, even when the sentence starts with the time:

- ***Früher** war meine Familie sehr groß.*
- ***Als Kind** hatte ich einen Hund.*
- ***Vor zehn Jahren** bin ich nach Berlin gezogen.*
- ***Im Jahr 1998** / **1998** ist mein Bruder geboren.* (never *in 1998*)

To order the events: ***am Anfang**, dann, später, **am Ende**, **zum Schluss***.
""",
        [
            "Damals hatten wir kein Auto.",
            "Am Anfang war alles schwer, am Ende hat es geklappt.",
            "1975 hat mein Opa die Bäckerei aufgemacht.",
        ],
    ),
]

L1_LESSONS = [
    lesson(
        "Meine Familie",
        review("die Tante"),
        review("der Cousin"),
        match(
            [
                ("der Bruder von meiner Mutter", "der Onkel"),
                ("die Schwester von meinem Vater", "die Tante"),
                ("der Sohn von meiner Tante", "der Cousin"),
                ("die Tochter von meinem Onkel", "die Cousine"),
                ("der Vater von meinem Mann", "der Schwiegervater"),
            ],
            "Who is it?",
        ),
        mc(
            "Sie ist nicht verheiratet. Sie ist ...",
            "ledig",
            "geschieden",
            "geboren",
        ),
        fill("Meine Tante ist 1962 ___. (born)", "geboren"),
        fill("Mein Opa hat Brot ___. (sold)", "verkauft"),
        tr("My uncle was a baker.", "Mein Onkel war Bäcker."),
    ),
    lesson(
        "war und hatte",
        grammar("Präteritum: war und hatte"),
        conj("sein", "du", "warst"),
        conj("sein", "wir", "waren"),
        conj("sein", "ihr", "wart"),
        conj("haben", "ich", "hatte"),
        conj("haben", "du", "hattest"),
        conj("haben", "ihr", "hattet"),
        fill("Als Kind ___ ich viele Puppen. (haben)", "hatte"),
        fill("Meine Großeltern ___ sehr fleißig. (sein)", "waren"),
        mc(
            "Which sentence is correct?",
            "Früher war mein Opa Bäcker.",
            "Früher mein Opa war Bäcker.",
            "Früher ist mein Opa Bäcker gewesen war.",
        ),
        order("Wir hatten damals keinen Fernseher."),
        tr("Were you at home yesterday? (du)", "Warst du gestern zu Hause?"),
    ),
    lesson(
        "Mit meinem Opa",
        grammar("Possessivartikel im Dativ"),
        fill("Ich wohne bei ___ Tante. (mein)", "meiner"),
        fill("Er spricht mit ___ Opa. (sein)", "seinem"),
        fill("Sie telefoniert mit ___ Schwester. (ihr)", "ihrer"),
        fill("Wir fahren mit ___ Kindern in Urlaub. (unser)", "unseren"),
        fill("Wie geht es ___ Cousine? (euer)", "eurer"),
        fill("Das Geschenk ist von ___ Onkel. (dein)", "deinem"),
        mc(
            "mit ___ Eltern (my)",
            "meinen",
            "meine",
            "meinem",
            "meiner",
        ),
        mc(
            "bei ___ Schwiegermutter (his)",
            "seiner",
            "seinem",
            "seine",
            "seinen",
        ),
        tr(
            "I often go to the cinema with my cousin (female).",
            "Ich gehe oft mit meiner Cousine ins Kino.",
        ),
    ),
    lesson(
        "Früher und heute",
        grammar("Zeitangaben: früher, damals, als Kind"),
        mc(
            "Which sentence is correct?",
            "Als Kind hatte ich einen Hund.",
            "Als Kind ich hatte einen Hund.",
            "Ich als Kind hatte einen Hund.",
        ),
        mc(
            "My brother was born in 1998:",
            "Mein Bruder ist 1998 geboren.",
            "Mein Bruder ist in 1998 geboren.",
            "Mein Bruder ist am 1998 geboren.",
        ),
        fill("___ zehn Jahren bin ich nach Wien gezogen. (ago)", "Vor"),
        fill("Am ___ war es schwer, aber am Ende hat es geklappt. (beginning)", "Anfang"),
        fill("Zum ___ haben wir zusammen gegessen. (finally)", "Schluss"),
        order("Damals hatte meine Familie eine Bäckerei."),
        tr("Back then we had a big garden.", "Damals hatten wir einen großen Garten."),
    ),
    lesson(
        "Meine Kindheit",
        match(
            [
                ("aufwachsen", "ist aufgewachsen"),
                ("klettern", "ist geklettert"),
                ("streiten", "hat gestritten"),
                ("rufen", "hat gerufen"),
                ("zeichnen", "hat gezeichnet"),
            ],
            "Match the Perfekt forms.",
        ),
        fill("Ich bin auf dem Land ___. (aufwachsen)", "aufgewachsen"),
        fill("Wir haben als Kinder Briefmarken ___. (sammeln)", "gesammelt"),
        fill("Mein Bruder und ich haben oft ___. (streiten)", "gestritten"),
        mc(
            "Als Kind ___ ich oft auf Bäume geklettert.",
            "bin",
            "habe",
            "war",
        ),
        mc(
            "Ein Witz ist ...",
            "etwas Lustiges",
            "ein Spiel mit Puppen",
            "ein langer Satz",
        ),
        tr("Did you often argue? (ihr)", "Habt ihr oft gestritten?"),
    ),
    lesson(
        "Eine Familiengeschichte",
        bank(
            "Mein Opa ___ Bäcker. 1965 hat er eine kleine Bäckerei ___. Er ist jeden Morgen "
            "um drei Uhr ___. Meine Oma ___ im Laden Brot und Kuchen verkauft. Am ___ war es "
            "schwer, aber später hat alles gut ___.",
            ["war", "aufgemacht", "aufgestanden", "hat", "Anfang", "geklappt"],
            "hatte",
            "Ende",
        ),
        mc(
            "What did the grandmother do?",
            "She sold bread and cake in the shop.",
            "She baked bread at three o'clock.",
            "She worked in a school.",
        ),
        mc(
            "Wie war das früher bei dir? means:",
            "What was it like for you back then?",
            "Where were you yesterday?",
            "What did you eat early?",
        ),
        order("Mein Opa hat die Bäckerei 1965 aufgemacht."),
        tr(
            "When I was little, I always looked after my sister.",
            "Als ich klein war, habe ich immer auf meine Schwester aufgepasst.",
        ),
    ),
    lesson(
        "Lektion 1: Test",
        fill("Meine Großeltern ___ früher einen Hund. (haben)", "hatten"),
        fill("Ich spreche oft mit ___ Onkel. (mein)", "meinem"),
        mc("Wo ___ du gestern?", "warst", "wart", "war"),
        mc("___ ich ein Kind war, ...", "Als", "Wenn", "Wann"),
        fill("Das hat gut ___. (klappen)", "geklappt"),
        order("Wir sind in einem kleinen Dorf aufgewachsen."),
        tr("My aunt is single.", "Meine Tante ist ledig."),
        tr("We had a lot of games.", "Wir hatten viele Spiele."),
    ),
]

LEKTION_1 = unit(
    1,
    "Mein Opa war auch schon Bäcker.",
    "Familie und Kindheit",
    L1_WORDS,
    L1_RULES,
    sections(L1_LESSONS, vocab_lessons(L1_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 2: Wohin mit der Kommode?
# ============================================================================

L2_WORDS = [
    ("the chest of drawers", "die Kommode", "noun", "Pl. die Kommoden"),
    ("the shelf", "das Regal", "noun", "Pl. die Regale"),
    ("the cushion", "das Kissen", "noun", "Pl. die Kissen"),
    ("the mirror", "der Spiegel", "noun", "Pl. die Spiegel"),
    ("the curtain", "der Vorhang", "noun", "Pl. die Vorhänge"),
    ("the wall", "die Wand", "noun", "Pl. die Wände"),
    ("the corner", "die Ecke", "noun", "Pl. die Ecken"),
    ("the door", "die Tür", "noun", "Pl. die Türen"),
    ("the ceiling", "die Decke", "noun", "also: the blanket"),
    ("the picture / poster", "das Poster", "noun", "Pl. die Poster"),
    ("the television set", "das Fernsehgerät", "noun", "Pl. die Fernsehgeräte"),
    ("the desk (at school)", "das Pult", "noun", "Pl. die Pulte"),
    ("the thing", "das Ding", "noun", "Pl. die Dinge"),
    ("the object", "der Gegenstand", "noun", "Pl. die Gegenstände"),
    ("the furnishing", "die Einrichtung", "noun"),
    ("the move (to a new home)", "der Umzug", "noun", "Pl. die Umzüge"),
    ("the tool", "das Werkzeug", "noun", "Pl. die Werkzeuge"),
    ("the space / room", "der Platz", "noun", "Wir brauchen mehr Platz."),
    ("to put (upright)", "stellen", "verb", "hat gestellt"),
    ("to lay / to put (flat)", "legen", "verb", "hat gelegt"),
    ("to lie (be lying)", "liegen", "verb", "hat gelegen"),
    ("to hang", "hängen", "verb", "hat gehängt / hat gehangen"),
    ("to sit", "sitzen", "verb", "hat gesessen"),
    ("to seat / to put", "setzen", "verb", "hat gesetzt"),
    ("to furnish", "einrichten", "verb", "hat eingerichtet"),
    ("to renovate", "renovieren", "verb", "hat renoviert"),
    ("to discuss", "diskutieren", "verb", "hat diskutiert"),
    ("to hide", "verstecken", "verb", "hat versteckt"),
    ("to move (furniture around)", "umstellen", "verb", "hat umgestellt"),
    ("careful", "vorsichtig", "adjective"),
    ("Where should the chest of drawers go?", "Wohin soll die Kommode?", "phrase"),
    ("That doesn't fit.", "Das passt nicht.", "phrase"),
]

L2_RULES = [
    rule(
        "Wechselpräpositionen: Wo? und Wohin?",
        "cases",
        """
Nine prepositions can take **two cases**: *an, auf, hinter, in, neben, über,
unter, vor, zwischen*.

| Question | Meaning | Case | Example |
|---|---|---|---|
| **Wo?** | where something is | **Dativ** | *Die Lampe steht **auf dem** Tisch.* |
| **Wohin?** | where something goes | **Akkusativ** | *Ich stelle die Lampe **auf den** Tisch.* |

Short forms: *an dem = **am**, in dem = **im**, an das = **ans**, in das = **ins***.

In the dative plural the noun gets **-n**: *zwischen den Fenster**n***.
""",
        [
            "Das Bild hängt an der Wand.",
            "Ich hänge das Bild an die Wand.",
            "Die Katze schläft unter dem Sofa.",
            "Die Katze läuft unter das Sofa.",
        ],
    ),
    rule(
        "stellen, legen, hängen",
        "verbs",
        """
German says **how** something is placed. The action verbs (Wohin? + Akkusativ)
are regular; the position verbs (Wo? + Dativ) are irregular:

| Action: Wohin? | Position: Wo? |
|---|---|
| stellen (upright): *Ich stelle die Flasche auf den Tisch.* | stehen: *Die Flasche steht auf dem Tisch.* |
| legen (flat): *Ich lege das Buch auf das Bett.* | liegen: *Das Buch liegt auf dem Bett.* |
| hängen: *Ich hänge den Spiegel an die Wand.* | hängen: *Der Spiegel hängt an der Wand.* |
| setzen: *Ich setze das Kind auf den Stuhl.* | sitzen: *Das Kind sitzt auf dem Stuhl.* |

Perfekt: *hat gestellt, hat gelegt, hat gehängt* (action) · *hat gestanden,
hat gelegen, hat gehangen, hat gesessen* (position).
""",
        [
            "Stell die Kommode bitte neben das Bett!",
            "Das Kissen liegt auf dem Sofa.",
            "Wir haben den Vorhang ans Fenster gehängt.",
        ],
    ),
]

L2_LESSONS = [
    lesson(
        "Im Zimmer",
        review("die Kommode"),
        review("das Regal"),
        match(
            [
                ("der Spiegel", "the mirror"),
                ("der Vorhang", "the curtain"),
                ("das Kissen", "the cushion"),
                ("die Wand", "the wall"),
                ("die Ecke", "the corner"),
            ]
        ),
        mc(
            "Was hängt vor dem Fenster?",
            "der Vorhang",
            "das Kissen",
            "die Kommode",
        ),
        mc(
            "Bei einem Umzug ...",
            "zieht man in eine neue Wohnung.",
            "kauft man ein neues Auto.",
            "geht man ins Kino.",
        ),
        fill("Wir müssen das Zimmer neu ___. (furnish)", "einrichten"),
        tr("We need more space.", "Wir brauchen mehr Platz."),
    ),
    lesson(
        "Wo oder wohin?",
        grammar("Wechselpräpositionen: Wo? und Wohin?"),
        mc("Das Bild hängt an ___ Wand. (Wo?)", "der", "die", "den"),
        mc("Ich hänge das Bild an ___ Wand. (Wohin?)", "die", "der", "dem"),
        mc("Die Katze liegt unter ___ Tisch.", "dem", "den", "der"),
        mc("Die Katze läuft unter ___ Tisch.", "den", "dem", "der"),
        fill("Der Teppich liegt vor ___ Sofa. (das)", "dem"),
        fill("Stell die Lampe auf ___ Kommode! (die)", "die"),
        fill("Das Regal steht zwischen ___ Fenstern. (die)", "den"),
        fill("Wir gehen ___ Wohnzimmer. (in das)", "ins"),
        tr("The mirror is hanging on the wall.", "Der Spiegel hängt an der Wand."),
    ),
    lesson(
        "stellen oder stehen?",
        grammar("stellen, legen, hängen"),
        mc("Die Flasche ___ auf dem Tisch.", "steht", "stellt", "legt"),
        mc("Ich ___ das Buch auf das Bett.", "lege", "liege", "stehe"),
        mc("Das Kind ___ auf dem Stuhl.", "sitzt", "setzt", "stellt"),
        mc("Er ___ den Spiegel an die Wand.", "hängt", "steht", "liegt"),
        fill("Das Handy ___ unter dem Kissen. (liegen)", "liegt"),
        fill("___ die Kommode bitte in die Ecke! (stellen, du)", "Stell|Stelle"),
        fill("Wir haben das Poster an die Tür ___. (hängen)", "gehängt"),
        fill("Das Buch hat auf dem Boden ___. (liegen)", "gelegen"),
        order("Leg das Kissen bitte auf das Sofa!"),
    ),
    lesson(
        "Der Umzug",
        bank(
            "Morgen ist unser ___! Die Kommode ___ wir neben das Bett. Das Regal kommt in die "
            "___. Den Spiegel hängen wir an die ___. Und das Fernsehgerät? Das ___ im "
            "Wohnzimmer. Sei bitte ___ mit dem Spiegel!",
            ["Umzug", "stellen", "Ecke", "Wand", "steht", "vorsichtig"],
            "liegt",
            "Decke",
        ),
        mc(
            "Wohin soll die Kommode? Answer:",
            "Neben das Bett.",
            "Neben dem Bett.",
            "Im Bett.",
        ),
        mc(
            "Wo ist der Schlüssel? Answer:",
            "Unter dem Kissen.",
            "Unter das Kissen.",
            "Unter den Kissen auf.",
        ),
        fill("Das ___ nicht. Der Schrank ist zu groß. (fit)", "passt"),
        order("Wohin soll das Regal?", "Build the question."),
        tr(
            "Put the cushion on the sofa! (du)",
            "Leg das Kissen auf das Sofa!|Lege das Kissen auf das Sofa!",
        ),
    ),
    lesson(
        "Wohnung einrichten",
        mc(
            "Was macht man mit Werkzeug?",
            "Man repariert etwas.",
            "Man isst etwas.",
            "Man schläft.",
        ),
        mc(
            "Die Kinder ___ die Geschenke hinter dem Sofa.",
            "verstecken",
            "diskutieren",
            "renovieren",
        ),
        fill("Wir haben die Küche ___. (renovieren)", "renoviert"),
        fill("Lass uns die Möbel ___! (move around)", "umstellen"),
        fill("Wir haben lange über das Sofa ___. (diskutieren)", "diskutiert"),
        tr("The picture hangs above the sofa.", "Das Bild hängt über dem Sofa."),
        tr("I'm putting the bottle in the fridge.", "Ich stelle die Flasche in den Kühlschrank."),
    ),
    lesson(
        "Lektion 2: Test",
        mc("Der Spiegel hängt ___ der Tür.", "an", "auf", "unter"),
        fill("Ich lege die Zeitung auf ___ Tisch. (der)", "den"),
        fill("Die Zeitung liegt auf ___ Tisch. (der)", "dem"),
        mc("Die Kinder ___ auf dem Boden.", "sitzen", "setzen", "stellen"),
        fill("Wir ___ das Regal an die Wand. (stellen)", "stellen"),
        order("Die Lampe steht zwischen dem Sofa und dem Sessel."),
        tr("Where should the shelf go?", "Wohin soll das Regal?"),
    ),
]

LEKTION_2 = unit(
    2,
    "Wohin mit der Kommode?",
    "Möbel und Wechselpräpositionen",
    L2_WORDS,
    L2_RULES,
    sections(L2_LESSONS, vocab_lessons(L2_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 3: Hier finden Sie Ruhe und Erholung.
# ============================================================================

L3_WORDS = [
    ("the village", "das Dorf", "noun", "Pl. die Dörfer"),
    ("the cat", "die Katze", "noun", "Pl. die Katzen"),
    ("the plant", "die Pflanze", "noun", "Pl. die Pflanzen"),
    ("the animal", "das Tier", "noun", "Pl. die Tiere"),
    ("the bird", "der Vogel", "noun", "Pl. die Vögel"),
    ("the air", "die Luft", "noun"),
    ("the quiet / peace", "die Ruhe", "noun"),
    ("the rest / recovery", "die Erholung", "noun"),
    ("the shore / riverbank", "das Ufer", "noun", "Pl. die Ufer"),
    ("the lake", "der See", "noun", "Pl. die Seen"),
    ("the view", "die Aussicht", "noun", "Pl. die Aussichten"),
    ("the destination", "das Reiseziel", "noun", "Pl. die Reiseziele"),
    ("the accommodation", "die Unterkunft", "noun", "Pl. die Unterkünfte"),
    ("the guesthouse", "die Pension", "noun", "Pl. die Pensionen"),
    ("the campsite", "der Campingplatz", "noun", "Pl. die Campingplätze"),
    ("the trip / ride", "die Fahrt", "noun", "Pl. die Fahrten"),
    ("the map / card", "die Karte", "noun", "Pl. die Karten"),
    ("the service", "der Service", "noun"),
    ("the experience", "die Erfahrung", "noun", "Pl. die Erfahrungen"),
    ("to hike", "wandern", "verb", "ist gewandert"),
    ("to offer", "anbieten", "verb", "hat angeboten"),
    ("to advise", "beraten", "verb", "berät, hat beraten"),
    ("to begin", "beginnen", "verb", "hat begonnen"),
    ("to end", "enden", "verb", "hat geendet"),
    ("to book", "buchen", "verb", "hat gebucht"),
    ("to take part", "mitmachen", "verb", "hat mitgemacht"),
    ("to recommend", "empfehlen", "verb", "empfiehlt, hat empfohlen"),
    ("to relax / to recover", "erholen", "verb", "sich erholen"),
    ("different", "anders", "adjective"),
    ("good value", "preiswert", "adjective"),
    ("central", "zentral", "adjective"),
    ("comfortable", "komfortabel", "adjective"),
    ("Here you'll find peace and relaxation.", "Hier finden Sie Ruhe und Erholung.", "phrase"),
    ("What can you recommend?", "Was können Sie empfehlen?", "phrase"),
    ("I'm for it.", "Ich bin dafür.", "phrase"),
]

L3_RULES = [
    rule(
        "Adjektive nach der, die, das",
        "adjectives",
        """
After a **definite article** (der, die, das, dieser ...) an adjective ends in
**-e** or **-en**:

| | masculine | feminine | neuter | plural |
|---|---|---|---|---|
| Nominativ | der ruhig**e** See | die schön**e** Aussicht | das klein**e** Dorf | die alt**en** Häuser |
| Akkusativ | den ruhig**en** See | die schön**e** Aussicht | das klein**e** Dorf | die alt**en** Häuser |
| Dativ | dem ruhig**en** See | der schön**en** Aussicht | dem klein**en** Dorf | den alt**en** Häuser**n** |

Easy rule: **-e** only in the five "simple" places (nominative singular, and
accusative feminine and neuter); everywhere else **-en**.

After *sein* there is no ending: *Der See ist ruhig.*
""",
        [
            "Die kleine Pension liegt direkt am See.",
            "Wir wandern durch den schönen Wald.",
            "Im alten Dorf gibt es eine Bäckerei.",
        ],
    ),
    rule(
        "Im Urlaub: am Meer, ans Meer",
        "cases",
        """
Holiday places follow the **Wo? / Wohin?** rule:

| Wo? (Dativ) | Wohin? (Akkusativ) |
|---|---|
| **am** Meer / **am** See | **ans** Meer / **an den** See |
| **in den** Bergen | **in die** Berge |
| **auf dem** Land | **aufs** Land |
| **im** Wald | **in den** Wald |
| **in** Österreich / **in der** Schweiz | **nach** Österreich / **in die** Schweiz |

Recommending something politely:
*Ich empfehle Ihnen ... · Sie können hier ... · Hier finden Sie ...*
""",
        [
            "Wir fahren im Sommer ans Meer.",
            "Im Urlaub waren wir in den Bergen.",
            "Ich empfehle Ihnen die Pension am See.",
        ],
    ),
]

L3_LESSONS = [
    lesson(
        "Natur und Ruhe",
        review("die Erholung"),
        review("die Unterkunft"),
        match(
            [
                ("der Vogel", "the bird"),
                ("die Pflanze", "the plant"),
                ("das Ufer", "the shore"),
                ("das Dorf", "the village"),
                ("die Aussicht", "the view"),
            ]
        ),
        mc(
            "Eine Pension ist ...",
            "ein kleines Hotel.",
            "ein großer See.",
            "ein Tier.",
        ),
        mc(
            "Hier gibt es keine Autos und keinen Lärm. Hier finden Sie ...",
            "Ruhe.",
            "Werkzeug.",
            "Service.",
        ),
        fill("Am Wochenende ___ wir in den Bergen. (wandern)", "wandern"),
        tr("The air is very clean here.", "Die Luft ist hier sehr sauber."),
    ),
    lesson(
        "Der ruhige See",
        grammar("Adjektive nach der, die, das"),
        fill("Der ___ See ist sehr schön. (ruhig)", "ruhige"),
        fill("Wir buchen die ___ Pension. (klein)", "kleine"),
        fill("Siehst du den ___ Vogel? (bunt)", "bunten"),
        fill("Wir wohnen in dem ___ Dorf. (alt)", "alten"),
        fill("Die ___ Zimmer sind sehr komfortabel. (neu)", "neuen"),
        mc(
            "Ich empfehle Ihnen das ___ Hotel.",
            "zentrale",
            "zentralen",
            "zentraler",
        ),
        mc("mit der ___ Aussicht", "schönen", "schöne", "schöner"),
        mc("Die Pension ist ___.", "preiswert", "preiswerte", "preiswerten"),
        tr("We are hiking through the green forest.", "Wir wandern durch den grünen Wald."),
    ),
    lesson(
        "Ans Meer oder in die Berge?",
        grammar("Im Urlaub: am Meer, ans Meer"),
        mc("Wir fahren im Sommer ___ Meer.", "ans", "am", "im"),
        mc("Letztes Jahr waren wir ___ Meer.", "am", "ans", "ins"),
        mc("Fahrt ihr ___ Berge?", "in die", "in den", "nach"),
        mc("Ich mache Urlaub ___ Land.", "auf dem", "auf das", "aufs"),
        fill("Wir fahren ___ Österreich. (to)", "nach"),
        fill("Im Winter fahren wir in ___ Schweiz. (die)", "die"),
        fill("Wir campen direkt am ___. (lake)", "See"),
        order("Ich empfehle Ihnen die Pension am See."),
        tr("We were in the mountains on holiday.", "Im Urlaub waren wir in den Bergen."),
    ),
    lesson(
        "Im Reisebüro",
        bank(
            "Guten Tag, ich möchte Urlaub machen. Was können Sie ___? Wir haben eine schöne "
            "Pension direkt am ___. Die Zimmer sind ___ und nicht teuer. Morgens ___ die "
            "Pension Wanderungen an. Gut, das ___ ich!",
            ["empfehlen", "See", "komfortabel", "bietet", "buche"],
            "beginnt",
            "Dorf",
        ),
        mc(
            "Wie viel kostet eine Übernachtung? asks about ...",
            "the price of one night",
            "the start of the trip",
            "the view from the room",
        ),
        mc(
            "Ich bin dafür. means:",
            "I'm for it.",
            "I'm there.",
            "I'm against it.",
        ),
        fill("Die Fahrt ___ um acht Uhr. (beginnen)", "beginnt"),
        fill("Der Kurs ___ um 17 Uhr. (enden)", "endet"),
        fill("Können Sie mich ___? (advise)", "beraten"),
        tr("Can I take part too?", "Kann ich auch mitmachen?"),
    ),
    lesson(
        "Erfahrungen im Urlaub",
        mc(
            "Die Unterkunft war ___ als im letzten Jahr.",
            "preiswerter",
            "preiswert",
            "am preiswertesten",
        ),
        mc(
            "Hier ist alles ___. Ich kenne das nicht.",
            "anders",
            "zentral",
            "preiswert",
        ),
        fill("Wir haben uns gut ___. (relaxed: erholen)", "erholt"),
        fill("Habt ihr die Reise schon ___? (buchen)", "gebucht"),
        order("Hier finden Sie Ruhe und Erholung."),
        tr("What can you recommend?", "Was können Sie empfehlen?"),
    ),
    lesson(
        "Lektion 3: Test",
        fill("Die ___ Luft ist gesund. (frisch)", "frische"),
        fill("Wir fahren in ___ Berge. (die)", "die"),
        mc("Wir wohnen ___ Land.", "auf dem", "aufs", "ins"),
        fill("Der Reiseleiter ___ uns gut. (beraten)", "berät"),
        mc("der Campingplatz:", "Man schläft im Zelt.", "Man kauft Brot.", "Man lernt Deutsch."),
        order("Wir haben eine Pension am See gebucht."),
        tr("The village is very quiet.", "Das Dorf ist sehr ruhig."),
        tr("I recommend the small hotel to you. (Sie)", "Ich empfehle Ihnen das kleine Hotel."),
    ),
    lesson(
        "Modul 1: Wiederholung",
        fill("Als Kind ___ ich einen Hund. (haben)", "hatte"),
        fill("Meine Eltern ___ damals sehr jung. (sein)", "waren"),
        fill("Ich fahre mit ___ Tante in Urlaub. (meine)", "meiner"),
        mc("Das Bild hängt ___ der Wand.", "an", "auf"),
        mc("Ich stelle die Vase ___ den Tisch.", "auf", "an"),
        fill("Das Buch ___ auf dem Regal. (liegen)", "liegt"),
        fill("Wir fahren ___ Meer. (an das)", "ans"),
        fill("Die ___ Aussicht ist toll. (schön)", "schöne"),
        bank(
            "Früher ___ meine Familie sehr groß. Wir ___ einen großen Garten. "
            "Heute wohnen wir in der Stadt, aber im Urlaub fahren wir immer ___ Land.",
            ["war", "hatten", "aufs"],
            "waren",
            "ans",
        ),
        tr(
            "Put the chest of drawers in the corner! (du)",
            "Stell die Kommode in die Ecke!|Stelle die Kommode in die Ecke!",
        ),
        order("Früher waren wir oft am See."),
    ),
]

LEKTION_3 = unit(
    3,
    "Hier finden Sie Ruhe und Erholung.",
    "Tourismus und Natur",
    L3_WORDS,
    L3_RULES,
    sections(L3_LESSONS, vocab_lessons(L3_WORDS, "Wörter")),
)


UNITS = [LEKTION_1, LEKTION_2, LEKTION_3]
