"""Modul 8 (A1.2): Lektion 22 (Am besten sind seine Schuhe!), 23 (Ins Wasser
gefallen?), 24 (Ich würde am liebsten jeden Tag feiern)."""

from ..dsl import (
    bank,
    conj,
    fill,
    grammar,
    interleave,
    lesson,
    match,
    mc,
    order,
    review,
    rule,
    tr,
    unit,
    vocab_lessons,
)

# ============================================================================
# Lektion 22: Am besten sind seine Schuhe!
# ============================================================================

L22_WORDS = [
    ("the clothes / clothing", "die Kleidung", "noun"),
    ("the T-shirt", "das T-Shirt", "noun", "Pl. die T-Shirts"),
    ("the shirt", "das Hemd", "noun", "Pl. die Hemden"),
    ("the blouse", "die Bluse", "noun", "Pl. die Blusen"),
    ("the trousers", "die Hose", "noun", "Pl. die Hosen"),
    ("the skirt", "der Rock", "noun", "Pl. die Röcke"),
    ("the dress", "das Kleid", "noun", "Pl. die Kleider"),
    ("the jumper / sweater", "der Pullover", "noun", "Pl. die Pullover"),
    ("the coat", "der Mantel", "noun", "Pl. die Mäntel"),
    ("the jacket", "die Jacke", "noun", "Pl. die Jacken"),
    ("the shoe", "der Schuh", "noun", "Pl. die Schuhe"),
    ("the sock", "die Socke", "noun", "Pl. die Socken"),
    ("the stocking", "der Strumpf", "noun", "Pl. die Strümpfe"),
    ("the tights", "die Strumpfhose", "noun", "Pl. die Strumpfhosen"),
    ("the belt", "der Gürtel", "noun", "Pl. die Gürtel"),
    ("the woolly hat", "die Mütze", "noun", "Pl. die Mützen"),
    ("the hat", "der Hut", "noun", "Pl. die Hüte"),
    ("purple", "lila", "adjective"),
    ("pink", "rosa", "adjective"),
    ("beige", "beige", "adjective"),
    ("golden", "golden", "adjective"),
    ("sporty", "sportlich", "adjective"),
    ("elegant", "elegant", "adjective"),
    ("clever", "klug", "adjective"),
    ("to put on (clothes)", "anziehen", "verb", "Ich ziehe die Jacke an."),
    ("to have on / to wear", "anhaben", "verb", "Er hat einen Mantel an."),
    ("than", "als", "other", "größer als"),
    ("just as … as", "genauso … wie", "phrase"),
    ("at the moment", "zurzeit", "adverb"),
    ("totally", "total", "adverb"),
    ("incredibly", "wahnsinnig", "adverb"),
    ("Great!", "Klasse!", "phrase"),
]

L22_RULES = [
    rule(
        "Komparativ",
        "adjectives",
        """
To compare two things, add **-er** to the adjective, and use **als** (than):

- *schön → schön**er***: *Das Kleid ist schön**er als** der Rock.*
- *billig → billig**er***

Short adjectives with **a, o, u** usually take an umlaut:
*alt → **ä**lter, groß → gr**ö**ßer, kurz → k**ü**rzer, lang → l**ä**nger, jung → j**ü**nger, warm → w**ä**rmer, klug → kl**ü**ger*

Irregular: **gut → besser**, **viel → mehr**, **gern → lieber**, **hoch → höher**, *teuer → teurer*.
""",
        [
            "Der Mantel ist wärmer als die Jacke.",
            "Mein Bruder ist älter als ich.",
            "Ich trage lieber Hosen.",
        ],
    ),
    rule(
        "Superlativ",
        "adjectives",
        """
For "the most": **am** + adjective + **-(e)sten**:

| | comparative | superlative |
|---|---|---|
| schön | schöner | am schönsten |
| alt | älter | am ältesten |
| groß | größer | am größten |
| kurz | kürzer | am kürzesten |
| **gut** | **besser** | **am besten** |
| **gern** | **lieber** | **am liebsten** |
| **viel** | **mehr** | **am meisten** |

Adjectives ending in **-t, -s, -ß, -z** add **-esten**: *am ält**esten**, am kürz**esten***.
""",
        [
            "Am besten sind seine Schuhe.",
            "Im Winter ist es am kältesten.",
            "Am liebsten trage ich Jeans.",
        ],
    ),
    rule(
        "als oder wie?",
        "adjectives",
        """
- Different: comparative + **als**: *Die Hose ist teurer **als** das Hemd.*
- The same: **(genau)so** + adjective + **wie**: *Lila mag ich **genauso** gern **wie** Rosa.*

Make an opinion stronger with **sehr, total, richtig, wahnsinnig**:
*Das sieht **wahnsinnig** gut aus! Der Hut ist **total** schön.*
""",
        [
            "Er ist so groß wie sein Vater.",
            "Die Jacke ist billiger als der Mantel.",
            "Das Kleid ist richtig elegant.",
        ],
    ),
]

L22_LESSONS = [
    lesson(
        "Kleidung",
        review("die Kleidung"),
        review("das Hemd"),
        match(
            [
                ("der Hut", "on your head"),
                ("die Socke", "on your foot"),
                ("der Gürtel", "around your waist"),
                ("der Mantel", "over everything in winter"),
                ("die Mütze", "a warm hat"),
            ],
            "Where do you wear it?",
        ),
        mc("Only women usually wear a …", "Rock", "Gürtel", "Mantel"),
        mc("It is cold. You put on a …", "Pullover", "T-Shirt", "Hut"),
        fill("Ich ziehe meine Jacke ___. (anziehen)", "an"),
        fill("Er hat heute einen Anzug ___. (anhaben)", "an"),
    ),
    lesson(
        "Komparativ",
        grammar("Komparativ"),
        fill("schön → ___", "schöner"),
        fill("alt → ___", "älter"),
        fill("groß → ___", "größer"),
        fill("kurz → ___", "kürzer"),
        fill("gut → ___", "besser"),
        fill("viel → ___", "mehr"),
        mc("teuer → ?", "teurer", "teuerer", "täurer"),
        mc("Der Mantel ist ___ als die Jacke.", "wärmer", "warmer", "am wärmsten"),
        tr("My sister is younger than me.", "Meine Schwester ist jünger als ich."),
    ),
    lesson(
        "Superlativ",
        grammar("Superlativ"),
        fill("schön → am ___", "schönsten"),
        fill("alt → am ___", "ältesten"),
        fill("gut → am ___", "besten"),
        fill("gern → am ___", "liebsten"),
        fill("viel → am ___", "meisten"),
        mc("groß → ?", "am größten", "am großesten", "am größsten"),
        order("Am besten sind seine Schuhe."),
        tr(
            "I like the dress best.",
            "Das Kleid gefällt mir am besten.|Am besten gefällt mir das Kleid.",
        ),
    ),
    lesson(
        "als oder wie?",
        grammar("als oder wie?"),
        mc("Die Hose ist teurer ___ das Hemd.", "als", "wie"),
        mc("Er ist genauso groß ___ sein Vater.", "wie", "als"),
        mc("Ich mag Lila genauso gern ___ Rosa.", "wie", "als"),
        mc("Die Bluse ist schöner ___ der Rock.", "als", "wie"),
        fill("Der Hut ist nicht so schön ___ die Mütze.", "wie"),
        fill("Meine Schuhe sind älter ___ deine.", "als"),
        tr("The jacket is cheaper than the coat.", "Die Jacke ist billiger als der Mantel."),
    ),
    lesson(
        "Was ziehst du an?",
        mc(
            "Wie findest du das Kleid? Agree strongly:",
            "Das sieht wahnsinnig gut aus!",
            "Das geht gar nicht.",
            "Es geht.",
        ),
        mc("Gut, besser, …", "am besten", "am gutesten", "besten"),
        bank(
            "Wie findest du mein Outfit? Die Bluse ist ___ schön, aber der Rock geht gar nicht! "
            "Die Hose gefällt mir ___. Und ___ sind deine Schuhe!",
            ["total", "besser", "am schönsten"],
            "als",
            "mehr",
        ),
        conj("anziehen", "du", "ziehst an"),
        order("Ich trage lieber sportliche Kleidung."),
        tr("Great! The hat looks really elegant.", "Klasse! Der Hut sieht richtig elegant aus."),
    ),
    lesson(
        "Lektion 22: Test",
        fill("lang → ___", "länger"),
        fill("viel → mehr → am ___", "meisten"),
        mc("Tom ist ___ als Paul.", "klüger", "kluger", "am klügsten"),
        mc("Sie ist so alt ___ ich.", "wie", "als"),
        order("Welche Farbe magst du am liebsten?", "Build the question."),
        tr("The shirt is more expensive than the T-shirt.", "Das Hemd ist teurer als das T-Shirt."),
        mc("die Strumpfhose:", "tights", "socks", "trousers"),
    ),
]

LEKTION_22 = unit(
    22,
    "Am besten sind seine Schuhe!",
    "Kleidung, Komparativ und Superlativ",
    L22_WORDS,
    L22_RULES,
    interleave(L22_LESSONS, vocab_lessons(L22_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 23: Ins Wasser gefallen?
# ============================================================================

L23_WORDS = [
    ("the sun", "die Sonne", "noun"),
    ("the rain", "der Regen", "noun"),
    ("the snow", "der Schnee", "noun"),
    ("the wind", "der Wind", "noun", "Pl. die Winde"),
    ("the fog", "der Nebel", "noun"),
    ("the cloud", "die Wolke", "noun", "Pl. die Wolken"),
    ("the thunderstorm", "das Gewitter", "noun", "Pl. die Gewitter"),
    ("the storm", "der Sturm", "noun", "Pl. die Stürme"),
    ("the sky", "der Himmel", "noun"),
    ("the degree (temperature)", "das Grad", "noun", "Es sind 20 Grad."),
    ("the compass direction", "die Himmelsrichtung", "noun", "Pl. die Himmelsrichtungen"),
    ("the north", "der Norden", "noun"),
    ("the south", "der Süden", "noun"),
    ("the east", "der Osten", "noun"),
    ("the west", "der Westen", "noun"),
    ("the roof", "das Dach", "noun", "Pl. die Dächer"),
    ("the luck / happiness", "das Glück", "noun", "Glück haben"),
    ("the bad luck", "das Pech", "noun", "Pech haben"),
    ("the mood", "die Laune", "noun", "gute / schlechte Laune"),
    ("the guidebook", "der Reiseführer", "noun", "Pl. die Reiseführer"),
    ("the dream", "der Traum", "noun", "Pl. die Träume"),
    ("the motorhome", "das Wohnmobil", "noun", "Pl. die Wohnmobile"),
    ("the holiday flat", "die Ferienwohnung", "noun", "Pl. die Ferienwohnungen"),
    ("the beach", "der Strand", "noun", "Pl. die Strände"),
    ("to rain", "regnen", "verb", "Es regnet."),
    ("to snow", "schneien", "verb", "Es schneit."),
    ("to shine", "scheinen", "verb", "Die Sonne scheint."),
    ("to experience", "erleben", "verb"),
    ("sunny", "sonnig", "adjective"),
    ("windy", "windig", "adjective"),
    ("cloudy", "bewölkt", "adjective"),
    ("foggy", "neblig", "adjective"),
    ("cloudless", "wolkenlos", "adjective"),
    ("warm", "warm", "adjective"),
    ("hot", "heiß", "adjective"),
    ("cool", "kühl", "adjective"),
    ("terrible", "furchtbar", "adjective"),
    ("quite / rather", "ziemlich", "adverb"),
    ("because (joins two main clauses)", "denn", "other"),
    ("to fall through (plans)", "ins Wasser fallen", "phrase"),
]

L23_RULES = [
    rule(
        "Das Wetter",
        "other",
        """
Weather sentences use **es** as the subject:

- *Es regnet. Es schneit. Es ist windig / sonnig / bewölkt / neblig.*
- *Die Sonne scheint.*
- *Es ist warm / heiß / kühl / kalt.*
- *Es sind 25 Grad. Es sind minus zwei Grad.*

Ask: ***Wie ist das Wetter?***

Directions: *im Norden, im Süden, im Osten, im Westen*.
""",
        [
            "Im Süden ist es sonnig und warm.",
            "Heute regnet es den ganzen Tag.",
            "Morgen sind es nur fünf Grad.",
        ],
    ),
    rule(
        "denn",
        "sentence_structure",
        """
**denn** (because) joins two main clauses. The word order after *denn* does **not** change:

*Wir fahren nach Spanien, **denn** dort **ist** es warm.*

| clause 1 | | clause 2 (normal order) |
|---|---|---|
| Ich bleibe zu Hause, | denn | es regnet. |
| Der Urlaub war toll, | denn | wir hatten Traumwetter. |
""",
        [
            "Ich ziehe eine Jacke an, denn es ist kalt.",
            "Wir hatten Pech, denn es hat jeden Tag geregnet.",
        ],
    ),
    rule(
        "-los",
        "adjectives",
        """
**-los** after a noun means **without**:

- *die Wolke → wolken**los*** (cloudless)
- *die Arbeit → arbeits**los*** (unemployed)
- *das Problem → problem**los*** (without problems)
- *die Hoffnung → hoffnungs**los*** (hopeless)
""",
        ["Der Himmel war wolkenlos.", "Alles hat problemlos funktioniert."],
    ),
]

L23_LESSONS = [
    lesson(
        "Wie ist das Wetter?",
        review("die Sonne"),
        review("der Regen"),
        grammar("Das Wetter"),
        match(
            [
                ("Es regnet.", "it's raining"),
                ("Es schneit.", "it's snowing"),
                ("Die Sonne scheint.", "the sun is shining"),
                ("Es ist neblig.", "it's foggy"),
                ("Es ist bewölkt.", "it's cloudy"),
            ]
        ),
        mc("There are no clouds. The sky is …", "wolkenlos", "bewölkt", "neblig"),
        fill("Es ist sehr ___ heute. Ich brauche keine Jacke. (hot)", "heiß"),
        fill("Es ___ 30 Grad. (sein)", "sind"),
    ),
    lesson(
        "Norden, Süden, Osten, Westen",
        mc("Hamburg liegt im ___ von Deutschland.", "Norden", "Süden", "Osten"),
        mc("München liegt im ___ von Deutschland.", "Süden", "Norden", "Westen"),
        mc("The sun rises in the …", "Osten", "Westen", "Norden"),
        fill("Im ___ ist es oft kälter. (north)", "Norden"),
        order("Im Süden scheint oft die Sonne."),
        tr("In the west it's raining.", "Im Westen regnet es."),
    ),
    lesson(
        "denn",
        grammar("denn"),
        mc("Ich bleibe zu Hause, ___ es regnet.", "denn", "und", "oder"),
        mc(
            "Which is correct?",
            "Wir fahren ans Meer, denn dort ist es warm.",
            "Wir fahren ans Meer, denn dort es ist warm.",
            "Wir fahren ans Meer, denn ist es dort warm.",
        ),
        order("Ich ziehe eine Jacke an, denn es ist kalt."),
        bank(
            "Der Urlaub war ___, denn das Wetter war furchtbar. Es hat jeden Tag ___ "
            "und wir hatten schlechte ___.",
            ["schlecht", "geregnet", "Laune"],
            "gut",
            "geschneit",
        ),
        tr("We stay at home because it's snowing.", "Wir bleiben zu Hause, denn es schneit."),
    ),
    lesson(
        "-los",
        grammar("-los"),
        fill("die Wolke → ___", "wolkenlos"),
        fill("das Problem → ___", "problemlos"),
        fill("die Arbeit → ___", "arbeitslos"),
        mc("wolkenlos means:", "without clouds", "with many clouds", "cloudy"),
        tr("The sky was cloudless.", "Der Himmel war wolkenlos."),
    ),
    lesson(
        "Ins Wasser gefallen?",
        review("das Pech"),
        mc(
            "Unser Urlaub ist ins Wasser gefallen. means:",
            "Our holiday was ruined.",
            "We swam a lot on holiday.",
            "Our holiday was by the sea.",
        ),
        mc("Wir hatten Pech. means:", "We were unlucky.", "We were lucky.", "We had a dream."),
        mc(
            "Blog: Wir waren mit dem Wohnmobil an der Ostsee. Leider hat es jeden Tag geregnet "
            "und ein Sturm hat das Dach kaputt gemacht. What happened to the roof?",
            "A storm broke it.",
            "Snow fell on it.",
            "Nothing.",
        ),
        bank(
            "Liebe Grüße aus Italien! Das Wetter ist ___: Die Sonne scheint und es sind 30 ___. "
            "Wir sind jeden Tag am ___. Bis bald, Mia",
            ["wunderbar", "Grad", "Strand"],
            "furchtbar",
            "Regen",
        ),
        fill("Im Urlaub haben wir viel ___. (erleben)", "erlebt"),
        order("Wir hatten ziemlich viel Glück."),
    ),
    lesson(
        "Lektion 23: Test",
        mc("Es ___ heute.", "schneit", "Schnee", "schneien"),
        fill("Heute ___ die Sonne. (scheinen)", "scheint"),
        mc("Ich nehme einen Schirm mit, ___ es regnet.", "denn", "aber", "als"),
        mc("The opposite of Glück:", "Pech", "Traum", "Laune"),
        order("Wie ist das Wetter in Berlin?", "Build the question."),
        tr("It's windy and cool.", "Es ist windig und kühl."),
        fill("Der Himmel ist grau, es ist ___. (cloudy)", "bewölkt"),
    ),
]

LEKTION_23 = unit(
    23,
    "Ins Wasser gefallen?",
    "Wetter und Urlaub",
    L23_WORDS,
    L23_RULES,
    interleave(L23_LESSONS, vocab_lessons(L23_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 24: Ich würde am liebsten jeden Tag feiern.
# ============================================================================

L24_WORDS = [
    ("the invitation", "die Einladung", "noun", "Pl. die Einladungen"),
    ("Easter", "Ostern", "noun"),
    ("Christmas", "Weihnachten", "noun"),
    ("New Year", "das Neujahr", "noun"),
    ("the congratulations", "der Glückwunsch", "noun", "Pl. die Glückwünsche"),
    ("the surprise party", "die Überraschungsparty", "noun", "Pl. die Überraschungspartys"),
    ("the housewarming party", "die Einweihungsparty", "noun", "Pl. die Einweihungspartys"),
    ("the final exam", "die Abschlussprüfung", "noun", "Pl. die Abschlussprüfungen"),
    ("the acquaintance", "der Bekannte", "noun", "f. die Bekannte"),
    ("the relative", "der Verwandte", "noun", "f. die Verwandte"),
    ("the ticket", "das Ticket", "noun", "Pl. die Tickets"),
    ("the theme party", "die Mottoparty", "noun", "Pl. die Mottopartys"),
    ("to pass (an exam)", "bestehen", "verb", "hat bestanden"),
    ("to give (as a present)", "schenken", "verb"),
    ("to answer", "antworten", "verb"),
    ("to win", "gewinnen", "verb", "hat gewonnen"),
    ("to move (house)", "umziehen", "verb", "ist umgezogen"),
    ("to be happy / to look forward to", "freuen", "verb", "sich freuen auf"),
    ("would", "würden", "verb", "ich würde, du würdest"),
    ("satisfied", "zufrieden", "adjective"),
    ("outside", "draußen", "adverb"),
    ("together", "gemeinsam", "adverb"),
    ("back then", "damals", "adverb"),
    ("first", "erste", "adjective", "der erste Mai"),
    ("third", "dritte", "adjective"),
    ("seventh", "siebte", "adjective"),
    ("All the best!", "Alles Gute!", "phrase"),
    ("Merry Christmas!", "Frohe Weihnachten!", "phrase"),
    ("Happy New Year!", "Frohes neues Jahr!", "phrase"),
    ("Well done!", "Gut gemacht!", "phrase"),
    ("Congratulations!", "Herzlichen Glückwunsch!", "phrase"),
    ("We would be very pleased!", "Wir würden uns sehr freuen!", "phrase"),
]

L24_RULES = [
    rule(
        "würde + Infinitiv",
        "verbs",
        """
For wishes and "what if", use **würde** + infinitive at the end:

| ich | du | er / sie | wir | ihr | sie / Sie |
|---|---|---|---|---|---|
| würde | würdest | würde | würden | würdet | würden |

- *Ich **würde** gern um die Welt **reisen**.*
- ***Würdest** du mit mir ins Kino **gehen**?* (polite request)
""",
        [
            "Wir würden das gern mit dir feiern.",
            "Ich würde dich gern einladen.",
            "Würden Sie mir bitte helfen?",
        ],
    ),
    rule(
        "gern, lieber, am liebsten",
        "other",
        """
- **gern**: like to: *Ich würde **gern** feiern.*
- **lieber**: would rather: *Ich würde **lieber** zu Hause bleiben.*
- **am liebsten**: most of all: *Ich würde **am liebsten** jeden Tag feiern.*

The same works without *würde*: *Ich tanze gern, singe lieber und koche am liebsten.*
""",
        ["Am liebsten würde ich ans Meer fahren.", "Ich trinke lieber Tee als Kaffee."],
    ),
    rule(
        "Ordnungszahlen und Datum",
        "other",
        """
Dates use **ordinal numbers**:

- 1 to 19: number + **-te**: *zwei**te**, vier**te**, zehn**te***
  Irregular: **erste** (1.), **dritte** (3.), **siebte** (7.), **achte** (8.)
- 20 and up: number + **-ste**: *zwanzig**ste**, einundzwanzig**ste***

- *Heute ist **der** erst**e** Mai.* (der + -e)
- ***Am** erst**en** Mai* (am + -en) · *am 21. Juli = am einundzwanzig**sten** Juli*
- *vom achten **bis zum** achtzehnten Januar*

In writing, a dot after the number marks an ordinal: *der 3. Oktober*.
""",
        [
            "Mein Geburtstag ist am dritten März.",
            "Die Party ist am Freitag, den 16. Oktober.",
            "Heute ist der erste Januar.",
        ],
    ),
]

L24_LESSONS = [
    lesson(
        "Feste im Jahr",
        review("Weihnachten"),
        review("die Einladung"),
        match(
            [
                ("Frohe Weihnachten!", "24-26 December"),
                ("Frohes neues Jahr!", "1 January"),
                ("Herzlichen Glückwunsch!", "a birthday"),
                ("Gut gemacht!", "you passed an exam"),
            ],
            "When do you say it?",
        ),
        mc(
            "Your friend passed the final exam. You say:",
            "Herzlichen Glückwunsch! Gut gemacht!",
            "Gute Besserung!",
            "Frohe Weihnachten!",
        ),
        mc("Easter in German:", "Ostern", "Weihnachten", "Neujahr"),
        fill("Ich ___ dir ein Buch zum Geburtstag. (schenken)", "schenke"),
    ),
    lesson(
        "würde",
        grammar("würde + Infinitiv"),
        conj("würden", "ich", "würde"),
        conj("würden", "du", "würdest"),
        conj("würden", "wir", "würden"),
        conj("würden", "ihr", "würdet"),
        fill("Ich ___ gern eine Reise machen.", "würde"),
        fill("___ du mit mir tanzen?", "Würdest"),
        order("Wir würden das gern mit dir feiern."),
        tr("I would like to invite you. (informal)", "Ich würde dich gern einladen."),
    ),
    lesson(
        "gern, lieber, am liebsten",
        grammar("gern, lieber, am liebsten"),
        mc("Ich würde ___ zu Hause bleiben als ausgehen.", "lieber", "gern", "am liebsten"),
        mc(
            "Most of all I would celebrate every day:",
            "Ich würde am liebsten jeden Tag feiern.",
            "Ich würde lieber jeden Tag feiern.",
            "Ich würde gern jeden Tag feiern lieber.",
        ),
        fill("Ich tanze gern, aber ich singe ___. (rather)", "lieber"),
        fill("Am ___ würde ich ans Meer fahren. (most of all)", "liebsten"),
        order("Am liebsten würde ich draußen feiern."),
        tr("I'd rather drink tea.", "Ich würde lieber Tee trinken.|Ich trinke lieber Tee."),
    ),
    lesson(
        "Ordnungszahlen",
        grammar("Ordnungszahlen und Datum"),
        match(
            [
                ("1.", "erste"),
                ("3.", "dritte"),
                ("7.", "siebte"),
                ("8.", "achte"),
                ("20.", "zwanzigste"),
            ],
            "Match the ordinals.",
        ),
        mc("2. → der …", "zweite", "zweiste", "zwote"),
        mc("21. → der …", "einundzwanzigste", "einundzwanzigte", "einszwanzigste"),
        fill("Heute ist der ___ Mai. (1.)", "erste"),
        fill("Mein Geburtstag ist am ___ März. (3.)", "dritten"),
        fill("Die Party ist am ___ Juli. (21.)", "einundzwanzigsten"),
        tr("on the first of January", "am ersten Januar"),
    ),
    lesson(
        "Datum",
        mc(
            "Wann hast du Geburtstag? Answer:",
            "Am zehnten April.",
            "Der zehnte April.",
            "Um zehn April.",
        ),
        mc(
            "Welcher Tag ist heute? Answer:",
            "Heute ist der zweite Juni.",
            "Heute ist am zweiten Juni.",
            "Heute ist zweiten Juni.",
        ),
        fill("Der Kurs geht vom ersten ___ zum zehnten Mai. (until)", "bis"),
        fill("Wir haben Urlaub ___ achten bis zum achtzehnten Juli. (from the)", "vom"),
        order("Die Party ist am Samstag, den achten Juni."),
        tr("My birthday is on the seventh of August.", "Mein Geburtstag ist am siebten August."),
    ),
    lesson(
        "Eine Einladung",
        bank(
            "Liebe Freunde, ich bin ___ und feiere eine Einweihungsparty! Wann? Am Samstag, "
            "den 14. Mai, ab 19 Uhr. Bitte bringt ___ mit. Bitte ___ bis zum 10. Mai. "
            "Ich würde mich sehr ___! Eure Nina",
            ["umgezogen", "Getränke", "antwortet", "freuen"],
            "gewonnen",
            "schenkt",
        ),
        mc(
            "Bitte antworte bis zum 10. Mai. means:",
            "Please reply by 10 May.",
            "Please come on 10 May.",
            "Please bring 10 friends.",
        ),
        mc(
            "Wir würden uns sehr freuen! means:",
            "We'd be very pleased!",
            "We are very free!",
            "We'd like to be free!",
        ),
        fill("Er hat die Prüfung ___. (bestehen)", "bestanden"),
        fill("Sie hat ein Ticket für das Konzert ___. (gewinnen)", "gewonnen"),
        order("Kommst du zu meiner Party?", "Build the question."),
    ),
    lesson(
        "Lektion 24: Test",
        mc("___ Sie mir bitte helfen?", "Würden", "Würde", "Würdest"),
        fill("Am ___ trinke ich Kaffee. (most of all)", "liebsten"),
        fill("Heute ist der ___ Oktober. (3.)", "dritte"),
        mc("am 8. Mai =", "am achten Mai", "am achtzehnten Mai", "am acht Mai"),
        order("Ich würde gern um die Welt reisen."),
        tr("All the best!", "Alles Gute!"),
        mc("Merry Christmas!", "Frohe Weihnachten!", "Frohes neues Jahr!", "Frohe Ostern!"),
    ),
    lesson(
        "Modul 8: Wiederholung",
        fill("warm → ___", "wärmer"),
        fill("gut → besser → am ___", "besten"),
        mc("Die Hose ist billiger ___ der Rock.", "als", "wie"),
        mc("Wir bleiben zu Hause, ___ es regnet.", "denn", "als"),
        fill("Es ___ den ganzen Tag. (regnen)", "regnet"),
        fill("Ich ___ gern nach Spanien fahren. (would)", "würde"),
        fill("Mein Geburtstag ist am ___ Juni. (1.)", "ersten"),
        bank(
            "Am liebsten ___ ich im Sommer Urlaub machen, denn dann ___ die Sonne. "
            "Im Winter ist es mir zu ___.",
            ["würde", "scheint", "kalt"],
            "wird",
            "warm",
        ),
        tr("In summer it's warmer than in spring.", "Im Sommer ist es wärmer als im Frühling."),
        order("Am besten gefällt mir der rote Mantel."),
    ),
]

LEKTION_24 = unit(
    24,
    "Ich würde am liebsten jeden Tag feiern.",
    "Feste, würde, Datum",
    L24_WORDS,
    L24_RULES,
    interleave(L24_LESSONS, vocab_lessons(L24_WORDS, "Wörter")),
)


UNITS = [LEKTION_22, LEKTION_23, LEKTION_24]
