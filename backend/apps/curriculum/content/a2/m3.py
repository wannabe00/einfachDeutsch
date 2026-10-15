"""Modul 3 (A2.1): Lektion 7 (Wir könnten montags joggen gehen.), 8
(Hoffentlich ist es nicht das Herz!), 9 (Bei guten Autos sind wir ganz vorn.)."""

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
# Lektion 7: Wir könnten montags joggen gehen.
# ============================================================================

L7_WORDS = [
    ("the fitness", "die Fitness", "noun"),
    ("the training", "das Training", "noun", "Pl. die Trainings"),
    ("the movement / exercise", "die Bewegung", "noun", "Pl. die Bewegungen"),
    ("the gym", "das Fitnessstudio", "noun", "Pl. die Fitnessstudios"),
    ("the strength training", "das Krafttraining", "noun"),
    ("the club / association", "der Verein", "noun", "Pl. die Vereine"),
    ("the coach / trainer", "der Trainer", "noun", "f. die Trainerin"),
    ("the team", "die Mannschaft", "noun", "Pl. die Mannschaften"),
    ("the kind of sport", "die Sportart", "noun", "Pl. die Sportarten"),
    ("the sports hall", "die Sporthalle", "noun", "Pl. die Sporthallen"),
    ("the stamina", "die Ausdauer", "noun"),
    ("the strength", "die Kraft", "noun", "Pl. die Kräfte"),
    ("the muscle", "der Muskel", "noun", "Pl. die Muskeln"),
    ("yoga", "Yoga", "noun", "Yoga machen"),
    ("to jog", "joggen", "verb", "ist gejoggt"),
    ("to train", "trainieren", "verb", "hat trainiert"),
    ("to move (oneself)", "bewegen", "verb", "sich bewegen"),
    ("to relax", "entspannen", "verb", "sich entspannen"),
    ("to lose", "verlieren", "verb", "hat verloren"),
    ("to suggest", "vorschlagen", "verb", "schlägt vor, hat vorgeschlagen"),
    ("to ski", "Ski fahren", "verb", "ist Ski gefahren"),
    ("fit", "fit", "adjective"),
    ("strenuous", "anstrengend", "adjective"),
    ("regularly", "regelmäßig", "adjective"),
    ("on Mondays", "montags", "adverb"),
    ("in the evenings", "abends", "adverb"),
    ("in the mornings", "morgens", "adverb"),
    ("twice a week", "zweimal pro Woche", "phrase"),
    ("What do you think of that?", "Was hältst du davon?", "phrase"),
    ("We could go jogging on Mondays.", "Wir könnten montags joggen gehen.", "phrase"),
]

L7_RULES = [
    rule(
        "Vorschläge: Wir könnten ...",
        "verbs",
        """
*könnte* (could) is the Konjunktiv II of *können*. It makes a **friendly
suggestion**; the other verb goes **to the end**:

| ich | du | er / sie | wir | ihr | sie / Sie |
|---|---|---|---|---|---|
| könnte | könntest | könnte | könnten | könntet | könnten |

- *Wir **könnten** montags joggen **gehen**.*
- ***Könntest** du mir den Ball **geben**?* (polite request)

Other ways to suggest: *Was hältst du davon, ... zu ...? · Wie wäre es mit ...?*
""",
        [
            "Wir könnten am Samstag Ski fahren.",
            "Ihr könntet in einen Verein gehen.",
            "Könnten Sie mir das Fitnessstudio zeigen?",
        ],
    ),
    rule(
        "Ratschläge: Du solltest ...",
        "verbs",
        """
*sollte* (should) is the Konjunktiv II of *sollen*. Use it for **advice**:

| ich | du | er / sie | wir | ihr | sie / Sie |
|---|---|---|---|---|---|
| sollte | solltest | sollte | sollten | solltet | sollten |

- *Du **solltest** dich mehr **bewegen**.*
- *Sie **sollten** regelmäßig **trainieren**.*

Compare: *Du **sollst** ...* passes on what someone else says; *Du **solltest** ...*
is your own advice.
""",
        [
            "Du solltest zweimal pro Woche schwimmen.",
            "Ihr solltet nicht so viel sitzen.",
            "Man sollte vor dem Training etwas trinken.",
        ],
    ),
    rule(
        "montags, abends: Zeitadverbien",
        "other",
        """
Add **-s** to a day or a time of day to say **every** (always lowercase):

| one time | every time |
|---|---|
| am Montag | **montags** (every Monday) |
| am Abend | **abends** (in the evenings) |
| am Morgen | **morgens** |
| am Wochenende | **am Wochenende** (no -s form) |

How often: *einmal / zweimal / dreimal pro Woche, jeden Tag, jeden Monat*.
""",
        [
            "Montags gehe ich ins Fitnessstudio.",
            "Abends mache ich Yoga.",
            "Wir trainieren dreimal pro Woche.",
        ],
    ),
]

L7_LESSONS = [
    lesson(
        "Sport und Fitness",
        review("die Mannschaft"),
        review("die Ausdauer"),
        match(
            [
                ("der Verein", "the club"),
                ("die Mannschaft", "the team"),
                ("die Kraft", "the strength"),
                ("die Bewegung", "the exercise"),
                ("die Sportart", "the kind of sport"),
            ]
        ),
        mc(
            "Joggen ist gut für ...",
            "die Ausdauer.",
            "die Mannschaft.",
            "die Sporthalle.",
        ),
        mc(
            "Im Fitnessstudio macht man ...",
            "Krafttraining.",
            "Ski fahren.",
            "eine Führung.",
        ),
        fill("Das Training war sehr ___. Ich bin müde. (strenuous)", "anstrengend"),
        fill("Unsere Mannschaft hat ___. (verlieren)", "verloren"),
        tr("I go jogging regularly.", "Ich gehe regelmäßig joggen."),
    ),
    lesson(
        "Wir könnten ...",
        grammar("Vorschläge: Wir könnten ..."),
        conj("könnten", "ich", "könnte"),
        conj("könnten", "du", "könntest"),
        conj("könnten", "wir", "könnten"),
        conj("könnten", "ihr", "könntet"),
        fill("Wir ___ am Samstag Ski fahren. (could)", "könnten"),
        fill("___ du mir helfen? (could)", "Könntest"),
        mc(
            "Which sentence is correct?",
            "Wir könnten montags joggen gehen.",
            "Wir könnten joggen gehen montags.",
            "Wir montags könnten joggen gehen.",
        ),
        order("Wir könnten zusammen ins Fitnessstudio gehen."),
        tr("We could play tennis.", "Wir könnten Tennis spielen."),
    ),
    lesson(
        "Du solltest ...",
        grammar("Ratschläge: Du solltest ..."),
        conj("sollten", "ich", "sollte"),
        conj("sollten", "du", "solltest"),
        conj("sollten", "ihr", "solltet"),
        fill("Du ___ dich mehr bewegen. (should)", "solltest"),
        fill("Sie ___ regelmäßig trainieren. (should, formal)", "sollten"),
        mc(
            "Your friend is always tired. Your advice:",
            "Du solltest früher schlafen gehen.",
            "Du könntest später schlafen.",
            "Du sollst nicht schlafen.",
        ),
        mc(
            "Which is advice?",
            "Du solltest mehr Wasser trinken.",
            "Du hast mehr Wasser getrunken.",
            "Du trinkst Wasser.",
        ),
        order("Ihr solltet nicht so viel sitzen."),
        tr("You should relax. (du)", "Du solltest dich entspannen."),
    ),
    lesson(
        "Montags und abends",
        grammar("montags, abends: Zeitadverbien"),
        mc("every Monday:", "montags", "am Montag", "Montags Tag"),
        mc("in the evenings:", "abends", "am Abends", "Abend"),
        fill("___ mache ich Yoga. (in the mornings)", "Morgens"),
        fill("Wir trainieren ___ pro Woche. (twice)", "zweimal"),
        fill("___ gehe ich ins Fitnessstudio. (on Mondays)", "Montags"),
        order("Abends spielen wir in der Sporthalle Fußball."),
        tr("We train three times a week.", "Wir trainieren dreimal pro Woche."),
    ),
    lesson(
        "Ein Plan für die Woche",
        bank(
            "Hallo Tom, du willst fit werden? Ich habe eine Idee: Wir ___ montags joggen gehen. "
            "Mittwochs könnten wir in den ___ gehen, da spielen sie Volleyball. Du ___ auch "
            "mehr trinken. Was ___ du davon? Und am Wochenende ___ wir uns!",
            ["könnten", "Verein", "solltest", "hältst", "entspannen"],
            "sollst",
            "Muskel",
        ),
        mc(
            "Was hältst du davon? asks ...",
            "for your opinion.",
            "for the time.",
            "for help.",
        ),
        mc(
            "Who could Tom play volleyball with?",
            "With a club.",
            "With his coach at home.",
            "With nobody.",
        ),
        fill("Ich ___ vor, dass wir schwimmen gehen. (vorschlagen)", "schlage"),
        fill("Der ___ sagt, ich soll langsam anfangen. (coach)", "Trainer"),
        tr("What do you think of that?", "Was hältst du davon?"),
    ),
    lesson(
        "Lektion 7: Test",
        fill("Wir ___ am Sonntag wandern. (could)", "könnten"),
        fill("Du ___ mehr schlafen. (should)", "solltest"),
        mc("every evening:", "abends", "am Abend"),
        fill("Ich ___ dreimal pro Woche. (trainieren)", "trainiere"),
        mc("Fitness, Yoga, Krafttraining: Das ist ...", "Sport.", "Kunst.", "Musik."),
        order("Ihr könntet in eine Mannschaft gehen."),
        tr("You should move more. (du)", "Du solltest dich mehr bewegen."),
    ),
]

LEKTION_7 = unit(
    7,
    "Wir könnten montags joggen gehen.",
    "Sport und Fitness",
    L7_WORDS,
    L7_RULES,
    sections(L7_LESSONS, vocab_lessons(L7_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 8: Hoffentlich ist es nicht das Herz!
# ============================================================================

L8_WORDS = [
    ("the health", "die Gesundheit", "noun"),
    ("the illness", "die Krankheit", "noun", "Pl. die Krankheiten"),
    ("the heart", "das Herz", "noun", "Pl. die Herzen"),
    ("the stomach", "der Magen", "noun", "Pl. die Mägen"),
    ("the skin", "die Haut", "noun"),
    ("the blood", "das Blut", "noun"),
    ("the blood pressure", "der Blutdruck", "noun"),
    ("the doctor's surgery", "die Arztpraxis", "noun", "Pl. die Arztpraxen"),
    ("the waiting room", "das Wartezimmer", "noun", "Pl. die Wartezimmer"),
    ("the patient", "der Patient", "noun", "f. die Patientin"),
    ("the examination", "die Untersuchung", "noun", "Pl. die Untersuchungen"),
    ("the injection", "die Spritze", "noun", "Pl. die Spritzen"),
    ("the cold (illness)", "die Erkältung", "noun", "Pl. die Erkältungen"),
    ("the backache", "die Rückenschmerzen", "noun", "plural"),
    ("the dizziness", "der Schwindel", "noun"),
    ("the allergy", "die Allergie", "noun", "Pl. die Allergien"),
    ("the injury", "die Verletzung", "noun", "Pl. die Verletzungen"),
    ("the emergency", "der Notfall", "noun", "Pl. die Notfälle"),
    ("to cough", "husten", "verb", "hat gehustet"),
    ("to sneeze", "niesen", "verb", "hat geniest"),
    ("to examine", "untersuchen", "verb", "hat untersucht"),
    ("to rest", "ausruhen", "verb", "sich ausruhen"),
    ("to injure", "verletzen", "verb", "sich verletzen"),
    ("dizzy", "schwindelig", "adjective", "Mir ist schwindelig."),
    ("sick / nauseous", "übel", "adjective", "Mir ist übel."),
    ("serious", "ernst", "adjective"),
    ("having a cold", "erkältet", "adjective", "Ich bin erkältet."),
    ("Hopefully it isn't the heart!", "Hoffentlich ist es nicht das Herz!", "phrase"),
    ("What's wrong with you? (formal)", "Was fehlt Ihnen?", "phrase"),
    ("I hope you get better soon.", "Ich hoffe, dass es dir bald besser geht.", "phrase"),
]

L8_RULES = [
    rule(
        "Ich hoffe, dass ...",
        "sentence_structure",
        """
**dass** (that) starts a subordinate clause. The conjugated verb goes **to the
end**, after a comma:

- *Ich hoffe, **dass** es nicht das Herz **ist**.*
- *Der Arzt sagt, **dass** ich mich ausruhen **soll**.*
- *Ich glaube, **dass** du erkältet **bist**.*

With a modal verb or the Perfekt, the conjugated verb is last:
*..., dass er zum Arzt gehen **muss**. · ..., dass sie krank gewesen **ist**.*

Shorter: ***Hoffentlich** ist es nichts Ernstes!* (verb in position 2)
""",
        [
            "Ich hoffe, dass es dir bald besser geht.",
            "Die Ärztin meint, dass es nur eine Erkältung ist.",
            "Ich weiß, dass du Rückenschmerzen hast.",
        ],
    ),
    rule(
        "Mir ist schlecht: Dativ bei Gefühlen",
        "cases",
        """
For how you **feel**, German often puts the person in the **dative** and has no
real subject:

| German | English |
|---|---|
| **Mir** ist schlecht / übel. | I feel sick. |
| **Mir** ist schwindelig. | I feel dizzy. |
| **Mir** ist kalt / warm. | I'm cold / warm. |
| Wie geht es **dir**? | How are you? |
| **Ihm** tut der Rücken weh. | His back hurts. |

The pronouns: *mir, dir, ihm, ihr, uns, euch, ihnen, Ihnen*.
""",
        [
            "Mir ist schwindelig, ich muss mich setzen.",
            "Ist dir kalt?",
            "Meinem Vater geht es schon besser.",
        ],
    ),
]

L8_LESSONS = [
    lesson(
        "Beim Arzt",
        review("die Erkältung"),
        review("die Untersuchung"),
        match(
            [
                ("das Herz", "the heart"),
                ("der Magen", "the stomach"),
                ("die Haut", "the skin"),
                ("das Blut", "the blood"),
                ("der Blutdruck", "the blood pressure"),
            ]
        ),
        mc(
            "Bevor der Arzt kommt, warten die Patienten im ...",
            "Wartezimmer.",
            "Notfall.",
            "Magen.",
        ),
        mc(
            "Was fehlt Ihnen? The doctor wants to know ...",
            "what's wrong with you.",
            "what you are missing at home.",
            "where you live.",
        ),
        fill("Ich bin ___ und habe Schnupfen. (have a cold)", "erkältet"),
        fill("Der Arzt hat mich gründlich ___. (untersuchen)", "untersucht"),
        tr("I have backache.", "Ich habe Rückenschmerzen."),
    ),
    lesson(
        "Ich hoffe, dass ...",
        grammar("Ich hoffe, dass ..."),
        mc(
            "Which sentence is correct?",
            "Ich hoffe, dass es nicht das Herz ist.",
            "Ich hoffe, dass es ist nicht das Herz.",
            "Ich hoffe, dass ist es nicht das Herz.",
        ),
        fill("Ich glaube, dass du erkältet ___. (sein)", "bist"),
        fill("Die Ärztin sagt, dass ich mich ausruhen ___. (sollen)", "soll"),
        fill("Ich weiß, dass er Fieber ___. (haben)", "hat"),
        mc(
            "Er sagt, dass er zum Arzt ___.",
            "gehen muss",
            "muss gehen",
            "geht muss",
        ),
        order("Ich hoffe, dass es nichts Ernstes ist."),
        tr(
            "I hope that you get better soon. (du)",
            "Ich hoffe, dass es dir bald besser geht.",
        ),
    ),
    lesson(
        "Mir ist schwindelig",
        grammar("Mir ist schlecht: Dativ bei Gefühlen"),
        mc("___ ist schwindelig.", "Mir", "Ich", "Mich"),
        mc("Ist ___ kalt? (du)", "dir", "du", "dich"),
        mc("Wie geht es ___? (er)", "ihm", "er", "ihn"),
        fill("Meiner Mutter ___ es schon besser. (gehen)", "geht"),
        fill("___ ist übel. (I feel sick)", "Mir"),
        fill("Uns ___ warm. (sein)", "ist"),
        tr("I'm cold.", "Mir ist kalt."),
    ),
    lesson(
        "Ein Notfall?",
        bank(
            "Herr Braun hat seit gestern Schmerzen in der Brust und ihm ist ___. Seine Frau ruft "
            "den Arzt: Ist das ein ___? Hoffentlich ist es nicht das ___! In der Praxis ___ der "
            "Arzt den Blutdruck. Es ist nichts ___, nur zu viel Stress.",
            ["schwindelig", "Notfall", "Herz", "misst", "Ernstes"],
            "erkältet",
            "Magen",
        ),
        mc(
            "What was the problem in the end?",
            "Too much stress.",
            "A heart attack.",
            "An allergy.",
        ),
        mc(
            "Gesundheit! (after someone sneezes) means:",
            "Bless you!",
            "Get well soon!",
            "Good luck!",
        ),
        fill("Er hat die ganze Nacht ___. (husten)", "gehustet"),
        fill("Ich habe mich beim Sport ___. (verletzen)", "verletzt"),
        tr("Hopefully it's nothing serious!", "Hoffentlich ist es nichts Ernstes!"),
    ),
    lesson(
        "Gesund bleiben",
        mc(
            "Ich habe eine ___: Ich darf keine Nüsse essen.",
            "Allergie",
            "Spritze",
            "Untersuchung",
        ),
        mc(
            "Bei einer Erkältung sollte man ...",
            "sich ausruhen und viel trinken.",
            "viel Sport machen.",
            "keinen Tee trinken.",
        ),
        fill("Nach dem Sport solltest du dich ___. (relax)", "entspannen"),
        fill("Die ___ ist das Wichtigste! (health)", "Gesundheit"),
        tr("The patient is waiting in the waiting room.", "Der Patient wartet im Wartezimmer."),
    ),
    lesson(
        "Lektion 8: Test",
        fill("Ich hoffe, dass du bald gesund ___. (sein)", "bist"),
        mc("___ ist übel.", "Mir", "Ich"),
        fill("Der Arzt ___ den Patienten. (untersuchen)", "untersucht"),
        mc("Ich glaube, dass sie eine Allergie ___.", "hat", "haben"),
        fill("Er muss sich ___. (rest)", "ausruhen"),
        order("Die Ärztin sagt, dass es nur eine Erkältung ist."),
        tr("What's wrong with you? (formal)", "Was fehlt Ihnen?"),
    ),
]

LEKTION_8 = unit(
    8,
    "Hoffentlich ist es nicht das Herz!",
    "Gesundheit und Krankheit",
    L8_WORDS,
    L8_RULES,
    sections(L8_LESSONS, vocab_lessons(L8_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 9: Bei guten Autos sind wir ganz vorn.
# ============================================================================

L9_WORDS = [
    ("the department", "die Abteilung", "noun", "Pl. die Abteilungen"),
    ("the company / enterprise", "das Unternehmen", "noun", "Pl. die Unternehmen"),
    ("the business / plant", "der Betrieb", "noun", "Pl. die Betriebe"),
    ("the factory", "die Fabrik", "noun", "Pl. die Fabriken"),
    ("the employee", "der Mitarbeiter", "noun", "f. die Mitarbeiterin"),
    ("the customer", "der Kunde", "noun", "f. die Kundin"),
    ("the product", "das Produkt", "noun", "Pl. die Produkte"),
    ("the model", "das Modell", "noun", "Pl. die Modelle"),
    ("the quality", "die Qualität", "noun"),
    ("the production", "die Produktion", "noun"),
    ("the export", "der Export", "noun"),
    ("the trade fair", "die Messe", "noun", "Pl. die Messen"),
    ("the strength", "die Stärke", "noun", "Pl. die Stärken"),
    ("the weakness", "die Schwäche", "noun", "Pl. die Schwächen"),
    ("to manufacture", "herstellen", "verb", "hat hergestellt"),
    ("to develop", "entwickeln", "verb", "hat entwickelt"),
    ("to deliver", "liefern", "verb", "hat geliefert"),
    ("reliable", "zuverlässig", "adjective"),
    ("high-quality", "hochwertig", "adjective"),
    ("successful", "erfolgreich", "adjective"),
    ("good at teamwork", "teamfähig", "adjective"),
    ("independent / self-employed", "selbstständig", "adjective"),
    ("responsible (for)", "zuständig", "adjective", "zuständig für + Akk."),
    ("worldwide", "weltweit", "adjective"),
    ("At good cars we're right at the front.", "Bei guten Autos sind wir ganz vorn.", "phrase"),
    ("We value quality.", "Wir legen Wert auf Qualität.", "phrase"),
    ("My tasks include ...", "Zu meinen Aufgaben gehört ...", "phrase"),
]

L9_RULES = [
    rule(
        "Adjektive ohne Artikel",
        "adjectives",
        """
With **no article**, the adjective itself takes the article's ending:

| | masculine | feminine | neuter | plural |
|---|---|---|---|---|
| Nominativ | gut**er** Service | gut**e** Qualität | gut**es** Produkt | gut**e** Autos |
| Akkusativ | gut**en** Service | gut**e** Qualität | gut**es** Produkt | gut**e** Autos |
| Dativ | mit gut**em** Service | mit gut**er** Qualität | mit gut**em** Produkt | bei gut**en** Autos |

You see this in adverts, menus and after numbers: *frischer Kaffee, zwei
neue Modelle, bei schlechtem Wetter*.
""",
        [
            "Bei guten Autos sind wir ganz vorn.",
            "Wir bieten hochwertige Produkte und schnellen Service.",
            "Mit frischem Brot schmeckt das Frühstück besser.",
        ],
    ),
    rule(
        "Superlativ vor dem Nomen: das beste Auto",
        "adjectives",
        """
Before a noun, the superlative takes **-st-** plus the normal adjective ending:

| am ... (after sein) | before a noun |
|---|---|
| Das Auto ist **am schnellsten**. | das schnell**ste** Auto |
| Die Firma ist **am größten**. | die größ**te** Firma |
| Der Service ist **am besten**. | der be**ste** Service |

- *Wir haben **die zuverlässigsten** Mitarbeiter.*
- *Das ist **unser erfolgreichstes** Modell.*

Irregular, as before: *gut, besser, best- · viel, mehr, meist- · hoch, höher, höchst-*.
""",
        [
            "Das ist das beste Auto auf der Messe.",
            "Unsere größte Fabrik steht in Bayern.",
            "Sie ist die erfolgreichste Mitarbeiterin der Abteilung.",
        ],
    ),
    rule(
        "Über die Arbeit sprechen",
        "other",
        """
Useful phrases for talking about your job and company:

- *Ich arbeite **bei** Siemens / **in der** Abteilung Export.*
- *Ich bin **zuständig für** den Kundenservice.* (+ Akkusativ)
- ***Zu meinen Aufgaben gehört** die Produktion.*
- *Ich habe **Erfahrung mit** ...* (+ Dativ)
- *Unsere Firma **stellt** Autos **her**. · Wir **legen** großen **Wert auf** Qualität.*
""",
        [
            "Ich bin für die neuen Kunden zuständig.",
            "Zu meinen Aufgaben gehört die Planung.",
            "Wir legen großen Wert auf Qualität.",
        ],
    ),
]

L9_LESSONS = [
    lesson(
        "In der Firma",
        review("die Abteilung"),
        review("der Kunde"),
        match(
            [
                ("herstellen", "to manufacture"),
                ("entwickeln", "to develop"),
                ("liefern", "to deliver"),
                ("die Messe", "the trade fair"),
                ("die Fabrik", "the factory"),
            ]
        ),
        mc(
            "Ein Mitarbeiter, der immer pünktlich ist und gut arbeitet, ist ...",
            "zuverlässig.",
            "selbstständig.",
            "weltweit.",
        ),
        mc(
            "Sie arbeitet gern mit anderen zusammen. Sie ist ...",
            "teamfähig.",
            "hochwertig.",
            "zuständig.",
        ),
        fill("Unsere Firma ___ Autos her. (herstellen)", "stellt"),
        tr("We deliver worldwide.", "Wir liefern weltweit."),
    ),
    lesson(
        "Bei guten Autos",
        grammar("Adjektive ohne Artikel"),
        fill("Wir bieten ___ Service. (schnell)", "schnellen"),
        fill("Hier gibt es ___ Kaffee. (frisch)", "frischen"),
        fill("Bei ___ Wetter fahren wir nicht. (schlecht)", "schlechtem"),
        fill("___ Qualität ist uns wichtig. (gut)", "Gute"),
        fill("Wir haben zwei ___ Modelle. (neu)", "neue"),
        mc("Bei ___ Autos sind wir ganz vorn.", "guten", "gute", "guter"),
        mc("___ Produkt kostet nur 20 Euro!", "Unser neues", "Unser neuer", "Unser neuen"),
        mc("mit ___ Mitarbeitern", "netten", "nette", "netter"),
        tr("We offer high-quality products.", "Wir bieten hochwertige Produkte."),
    ),
    lesson(
        "Das beste Auto",
        grammar("Superlativ vor dem Nomen: das beste Auto"),
        fill("Das ist das ___ Auto auf der Messe. (gut)", "beste"),
        fill("Unsere ___ Fabrik steht in Bayern. (groß)", "größte"),
        fill("Sie ist die ___ Mitarbeiterin. (erfolgreich)", "erfolgreichste"),
        fill("Das ist unser ___ Modell. (schnell)", "schnellstes"),
        mc("Der Service ist am ___.", "besten", "beste", "bester"),
        mc(
            "Which is correct?",
            "Das ist der zuverlässigste Mitarbeiter.",
            "Das ist der am zuverlässigsten Mitarbeiter.",
            "Das ist der zuverlässiger Mitarbeiter.",
        ),
        order("Wir haben die zuverlässigsten Produkte."),
        tr("This is the most expensive model.", "Das ist das teuerste Modell."),
    ),
    lesson(
        "Meine Arbeit",
        grammar("Über die Arbeit sprechen"),
        fill("Ich bin ___ den Export zuständig. (for)", "für"),
        fill("Zu meinen Aufgaben ___ die Planung. (gehören)", "gehört"),
        fill("Ich habe viel Erfahrung ___ Kunden. (with)", "mit"),
        fill("Wir legen großen ___ auf Qualität. (value)", "Wert"),
        mc(
            "Was sind Ihre Stärken? The interviewer asks about your ...",
            "strengths.",
            "weaknesses.",
            "salary.",
        ),
        order("Ich arbeite in der Abteilung Export."),
        tr("I am responsible for the new customers.", "Ich bin für die neuen Kunden zuständig."),
    ),
    lesson(
        "Ein Firmenporträt",
        bank(
            "Die Firma Autotec ___ seit 1960 Autos her. In der ___ arbeiten 800 Mitarbeiter. "
            "Wir legen großen Wert auf ___. Unsere Autos sind ___ und modern. Wir liefern "
            "___, auch nach Asien. Bei guten Autos sind wir ganz ___!",
            ["stellt", "Fabrik", "Qualität", "zuverlässig", "weltweit", "vorn"],
            "liefert",
            "Messe",
        ),
        mc(
            "Since when has Autotec been making cars?",
            "Since 1960.",
            "For 800 years.",
            "Since last year.",
        ),
        mc(
            "ganz vorn sein means:",
            "to be the best / leading",
            "to be at the entrance",
            "to be very early",
        ),
        fill("Wir haben ein neues Modell ___. (entwickeln)", "entwickelt"),
        fill("Sie arbeitet ___. Sie hat ihre eigene Firma. (self-employed)", "selbstständig"),
        tr("The company is very successful.", "Die Firma ist sehr erfolgreich."),
    ),
    lesson(
        "Lektion 9: Test",
        fill("Wir bieten ___ Service. (gut)", "guten"),
        fill("Das ist das ___ Produkt. (neu)", "neueste"),
        mc("Ich bin ___ die Produktion zuständig.", "für", "mit"),
        mc("bei ___ Wetter", "schönem", "schöne"),
        fill("Was ist Ihre größte ___? (weakness)", "Schwäche"),
        order("Bei guten Autos sind wir ganz vorn."),
        tr("We value quality.", "Wir legen Wert auf Qualität."),
    ),
    lesson(
        "Modul 3: Wiederholung",
        fill("Wir ___ montags schwimmen gehen. (could)", "könnten"),
        fill("Du ___ mehr Sport machen. (should)", "solltest"),
        mc("every Friday:", "freitags", "am Freitags"),
        fill("Ich hoffe, dass es dir gut ___. (gehen)", "geht"),
        mc("___ ist schwindelig.", "Mir", "Mich"),
        fill("Wir verkaufen ___ Brot. (frisch)", "frisches"),
        fill("Das ist der ___ Service. (schnell)", "schnellste"),
        fill("Ich bin für die Kunden ___. (responsible)", "zuständig"),
        bank(
            "Die Ärztin sagt, ___ ich mich mehr bewegen soll. Ich ___ zweimal pro Woche "
            "joggen gehen. Am besten trainiere ich ___.",
            ["dass", "könnte", "morgens"],
            "weil",
            "solltest",
        ),
        tr("Hopefully it isn't the heart!", "Hoffentlich ist es nicht das Herz!"),
        order("Du solltest zweimal pro Woche trainieren."),
    ),
]

LEKTION_9 = unit(
    9,
    "Bei guten Autos sind wir ganz vorn.",
    "Arbeitsleben und Firmen",
    L9_WORDS,
    L9_RULES,
    sections(L9_LESSONS, vocab_lessons(L9_WORDS, "Wörter")),
)


UNITS = [LEKTION_7, LEKTION_8, LEKTION_9]
