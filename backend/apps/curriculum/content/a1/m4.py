"""Modul 4: Lektion 10 (Ich steige jetzt in die U-Bahn ein), 11 (Was hast du
heute gemacht?), 12 (Was ist denn hier passiert?)."""

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
# Lektion 10: Ich steige jetzt in die U-Bahn ein.
# ============================================================================

L10_WORDS = [
    ("the means of transport", "das Verkehrsmittel", "noun", "Pl. die Verkehrsmittel"),
    ("the train", "der Zug", "noun", "Pl. die Züge"),
    ("the bus", "der Bus", "noun", "Pl. die Busse"),
    ("the underground / metro", "die U-Bahn", "noun", "Pl. die U-Bahnen"),
    ("the city train", "die S-Bahn", "noun", "Pl. die S-Bahnen"),
    ("the tram", "die Straßenbahn", "noun", "Pl. die Straßenbahnen"),
    ("the taxi", "das Taxi", "noun", "Pl. die Taxis"),
    ("the bicycle", "das Fahrrad", "noun", "Pl. die Fahrräder"),
    ("the plane", "das Flugzeug", "noun", "Pl. die Flugzeuge"),
    ("the train station", "der Bahnhof", "noun", "Pl. die Bahnhöfe"),
    ("the platform", "der Bahnsteig", "noun", "Pl. die Bahnsteige"),
    ("the track (platform number)", "das Gleis", "noun", "Pl. die Gleise"),
    ("the stop (bus, tram)", "die Haltestelle", "noun", "Pl. die Haltestellen"),
    ("the airport", "der Flughafen", "noun", "Pl. die Flughäfen"),
    ("the ticket", "die Fahrkarte", "noun", "Pl. die Fahrkarten"),
    ("the timetable", "der Fahrplan", "noun", "Pl. die Fahrpläne"),
    ("the suitcase", "der Koffer", "noun", "Pl. die Koffer"),
    ("the luggage", "das Gepäck", "noun"),
    ("the journey / trip", "die Reise", "noun", "Pl. die Reisen"),
    ("the caution", "die Vorsicht", "noun", "Vorsicht! = Careful!"),
    ("to depart", "abfahren", "verb", "Der Zug fährt ab. / ist abgefahren"),
    ("to arrive", "ankommen", "verb", "Er kommt an. / ist angekommen"),
    ("to get on", "einsteigen", "verb", "Ich steige ein."),
    ("to get off", "aussteigen", "verb", "Ich steige aus."),
    ("to change (trains, buses)", "umsteigen", "verb", "Ich steige um."),
    ("to pick up (someone)", "abholen", "verb", "Ich hole dich ab."),
    ("to phone", "anrufen", "verb", "Ich rufe dich an."),
    ("to go shopping", "einkaufen", "verb", "Ich kaufe ein."),
    ("to watch TV", "fernsehen", "verb", "Ich sehe fern."),
    ("to bring along", "mitbringen", "verb", "Ich bringe Wein mit."),
    ("to get up", "aufstehen", "verb", "Ich stehe auf."),
    ("to take", "nehmen", "verb", "du nimmst, er nimmt"),
    ("to fly", "fliegen", "verb"),
    ("to get / to receive", "bekommen", "verb"),
    ("at home", "zu Hause", "phrase"),
    ("right now / just", "gerade", "adverb"),
    ("next", "nächste", "adjective", "der nächste Zug"),
    ("so / well then", "also", "other"),
    ("See you soon!", "Bis bald!", "phrase"),
    ("When does the train leave?", "Wann fährt der Zug ab?", "phrase"),
]

L10_RULES = [
    rule(
        "Trennbare Verben",
        "verbs",
        """
Many verbs have a **prefix** (*ein-, aus-, um-, ab-, an-, auf-, mit-, fern-*). In a statement
the verb is in position 2 and the **prefix goes to the end**:

| infinitive | sentence |
|---|---|
| **ein**steigen | Ich steige jetzt in die U-Bahn **ein**. |
| **ab**fahren | Der Zug fährt um 8 Uhr **ab**. |
| **an**rufen | Ich rufe dich morgen **an**. |
| **auf**stehen | Wir stehen um sieben **auf**. |

With **können** the verb stays whole at the end: *Ich kann dich **abholen**.*
The prefix carries the stress: *EINsteigen, ANrufen*.
""",
        ["Wo steige ich um?", "Der Bus kommt um 9 Uhr an.", "Kannst du Brot mitbringen?"],
    ),
    rule(
        "nehmen",
        "verbs",
        """
**nehmen** (to take) changes its vowel and drops the **h**:

| ich | du | er / sie | wir | ihr | sie / Sie |
|---|---|---|---|---|---|
| nehme | **nimmst** | **nimmt** | nehmen | nehmt | nehmen |

*Ich nehme den Bus. Nimmst du ein Taxi?*
""",
        ["Wir nehmen die U-Bahn.", "Er nimmt den Zug um acht."],
    ),
    rule(
        "mit dem Bus, zu Fuß",
        "other",
        """
Say how you travel with **mit** + vehicle. Learn these as fixed phrases:

- **mit dem** Bus / Zug / Auto / Taxi / Fahrrad / Flugzeug (masculine and neuter)
- **mit der** U-Bahn / S-Bahn / Straßenbahn (feminine)
- on foot: **zu Fuß**

*Ich fahre **mit dem** Fahrrad zur Arbeit. Sie geht **zu Fuß**.*
""",
        ["Wir fahren mit der S-Bahn.", "Er fliegt mit dem Flugzeug nach Rom.", "Ich gehe zu Fuß."],
    ),
]

L10_LESSONS = [
    lesson(
        "Verkehrsmittel",
        review("der Zug"),
        review("die U-Bahn"),
        match(
            [
                ("das Flugzeug", "der Flughafen"),
                ("der Zug", "der Bahnhof"),
                ("der Bus", "die Haltestelle"),
                ("das Taxi", "the driver takes you to the door"),
            ],
            "Where do you get on?",
        ),
        mc("Which one flies?", "das Flugzeug", "die Straßenbahn", "der Bus"),
        mc("You put your clothes for a trip in a …", "Koffer", "Fahrplan", "Bahnsteig"),
        mc("You need it to travel by train:", "eine Fahrkarte", "einen Koffer", "eine Haltestelle"),
        fill("Der Zug fährt von ___ 5 ab. (track)", "Gleis"),
    ),
    lesson(
        "Trennbare Verben",
        grammar("Trennbare Verben"),
        mc(
            "einsteigen: Ich ___ jetzt in die U-Bahn ___.",
            "steige … ein",
            "einsteige … (nothing)",
            "steige … aus",
        ),
        fill("Der Zug fährt um 8:15 Uhr ___. (abfahren)", "ab"),
        fill("Ich rufe dich morgen ___. (anrufen)", "an"),
        fill("Wir ___ um sieben Uhr auf. (aufstehen)", "stehen"),
        fill("Wo ___ ich um? (umsteigen)", "steige"),
        order("Ich steige jetzt aus."),
        order("Der Bus kommt um zehn Uhr an."),
        order("Wann fährt der Zug ab?", "Build the question."),
        mc(
            "Which sentence is correct?",
            "Ich steige jetzt ein.",
            "Ich einsteige jetzt.",
            "Ich jetzt steige ein.",
        ),
    ),
    lesson(
        "Ich kaufe ein.",
        fill("Du ___ heute ein. (einkaufen)", "kaufst"),
        fill("Er ___ jeden Abend fern. (fernsehen)", "sieht"),
        fill("Ich ___ um sechs Uhr auf. (aufstehen)", "stehe"),
        fill("Am Samstag ___ ich im Supermarkt ein. (einkaufen)", "kaufe"),
        fill("Am Abend sieht Paul ___. (fernsehen)", "fern"),
        fill("Bringst du Wein ___? (mitbringen)", "mit"),
        order("Ich hole dich am Bahnhof ab."),
        tr("I'll call you tomorrow.", "Ich rufe dich morgen an.|Morgen rufe ich dich an."),
    ),
    lesson(
        "Mit können",
        order("Ich kann dich am Flughafen abholen."),
        order("Kannst du mich morgen anrufen?", "Build the question."),
        order("Wir können am Bahnhof umsteigen."),
        mc(
            "Which sentence is correct?",
            "Ich kann dich abholen.",
            "Ich kann dich holen ab.",
            "Ich abholen kann dich.",
        ),
        fill("Du musst in Köln ___. (change trains)", "umsteigen"),
        tr("Can you bring some bread? (informal)", "Kannst du Brot mitbringen?"),
    ),
    lesson(
        "Wie fährst du?",
        grammar("mit dem Bus, zu Fuß"),
        grammar("nehmen"),
        conj("nehmen", "du", "nimmst"),
        conj("nehmen", "er", "nimmt"),
        mc("Ich fahre ___ U-Bahn.", "mit der", "mit dem"),
        mc("Er fährt ___ Fahrrad.", "mit dem", "mit der"),
        fill("Wir gehen zu ___. Es ist nicht weit. (on foot)", "Fuß"),
        fill("___ du den Bus oder die S-Bahn? (nehmen)", "Nimmst"),
        tr("I take the train.", "Ich nehme den Zug."),
        tr("She goes by tram.", "Sie fährt mit der Straßenbahn."),
    ),
    lesson(
        "Am Bahnhof",
        review("Wann fährt der Zug ab?"),
        mc(
            "Durchsage: Der ICE nach Berlin fährt heute von Gleis 7 ab. Which track?",
            "Gleis 7",
            "Gleis 17",
            "Gleis 1",
        ),
        mc(
            "Durchsage: Vorsicht an Gleis 2! Der Zug fährt ab. What does Vorsicht mean?",
            "Careful!",
            "Welcome!",
            "Sorry!",
        ),
        bank(
            "Entschuldigung, wann ___ der nächste Zug nach Hamburg ab? Um 14:20 Uhr. "
            "Muss ich ___? Ja, in Hannover. Danke! Und wo ist ___ 4? Da vorne.",
            ["fährt", "umsteigen", "Gleis"],
            "ankommen",
            "Bahnsteig",
        ),
        order("Der nächste Zug kommt um neun Uhr an."),
        tr("Where is the bus stop?", "Wo ist die Haltestelle?"),
    ),
    lesson(
        "Am Telefon: Ich bin gerade …",
        bank(
            "Hallo Lisa, ich bin ___ am Bahnhof. Ich steige jetzt in die U-Bahn ___. "
            "Holst du mich ab? Ja, klar. ___ bald!",
            ["gerade", "ein", "Bis"],
            "aus",
            "Auf",
        ),
        mc(
            "Your train is late. You call: …",
            "Ich komme später an.",
            "Ich komme früher an.",
            "Ich steige ein.",
        ),
        mc("Bis bald! means:", "See you soon!", "Good night!", "Careful!"),
        fill("Ich bin ___ Hause. (at)", "zu"),
        order("Also dann, bis bald!"),
    ),
    lesson(
        "Lektion 10: Test",
        mc("Er ___ um sechs Uhr ___.", "steht … auf", "aufsteht … (nothing)", "steht … an"),
        fill("Der Zug ___ um 12 Uhr ab. (abfahren)", "fährt"),
        conj("nehmen", "sie (she)", "nimmt"),
        mc("Wir fahren ___ Auto.", "mit dem", "mit der"),
        order("Wo muss ich umsteigen?", "Build the question."),
        tr(
            "The plane arrives at eight o'clock.",
            "Das Flugzeug kommt um acht Uhr an.|Das Flugzeug kommt um 8 Uhr an.",
        ),
        mc("Gepäck means:", "luggage", "ticket", "platform"),
    ),
]

LEKTION_10 = unit(
    10,
    "Ich steige jetzt in die U-Bahn ein.",
    "Verkehrsmittel und trennbare Verben",
    L10_WORDS,
    L10_RULES,
    interleave(L10_LESSONS, vocab_lessons(L10_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 11: Was hast du heute gemacht?
# ============================================================================

L11_WORDS = [
    ("the work", "die Arbeit", "noun"),
    ("the task", "die Aufgabe", "noun", "Pl. die Aufgaben"),
    ("the homework", "die Hausaufgabe", "noun", "Pl. die Hausaufgaben"),
    ("the break", "die Pause", "noun", "Pl. die Pausen"),
    ("the baby", "das Baby", "noun", "Pl. die Babys"),
    ("the present / gift", "das Geschenk", "noun", "Pl. die Geschenke"),
    ("the couple", "das Paar", "noun", "Pl. die Paare"),
    ("the party", "die Party", "noun", "Pl. die Partys"),
    ("the sport", "der Sport", "noun"),
    ("the wine", "der Wein", "noun", "Pl. die Weine"),
    ("to tidy up", "aufräumen", "verb", "hat aufgeräumt"),
    ("to invite", "einladen", "verb", "du lädst ein; hat eingeladen"),
    ("to laugh", "lachen", "verb", "hat gelacht"),
    ("to learn / to study", "lernen", "verb", "hat gelernt"),
    ("to talk", "reden", "verb", "hat geredet"),
    ("to sleep", "schlafen", "verb", "du schläfst; hat geschlafen"),
    ("to phone (someone)", "telefonieren", "verb", "hat telefoniert"),
    ("to think / to mean", "meinen", "verb"),
    ("to buy", "kaufen", "verb", "hat gekauft"),
    ("to get to know", "kennenlernen", "verb", "hat kennengelernt"),
    ("yesterday", "gestern", "adverb"),
    ("the day before yesterday", "vorgestern", "adverb"),
    ("daily", "täglich", "adjective"),
    ("for a long time", "lange", "adverb"),
    ("boring", "langweilig", "adjective"),
    ("interesting", "interessant", "adjective"),
    ("finished / ready", "fertig", "adjective"),
    ("last week", "letzte Woche", "phrase"),
    ("last year", "letztes Jahr", "phrase"),
    ("last Friday", "letzten Freitag", "phrase"),
    ("from (a time on)", "ab", "other", "ab 9 Uhr"),
    ("from … until …", "von … bis …", "phrase", "von 9 bis 12 Uhr"),
    ("for", "für", "other"),
    ("twice", "zweimal", "adverb"),
    ("really?", "wirklich?", "phrase"),
    ("What did you do today?", "Was hast du heute gemacht?", "phrase"),
]

L11_RULES = [
    rule(
        "Perfekt mit haben",
        "verbs",
        """
To talk about the past in conversation, use the **Perfekt**:
**haben** (conjugated, position 2) + **Partizip II** (at the end).

| 1 | 2 | middle | end |
|---|---|---|---|
| Ich | **habe** | Tennis | **gespielt**. |
| Gestern | **haben** | wir | **gearbeitet**. |
| Was | **hast** | du heute | **gemacht**? |

Most verbs use *haben*. (Verbs of movement use *sein*: next Lektion.)
""",
        ["Ich habe Deutsch gelernt.", "Hast du Pizza gegessen?", "Am Abend haben wir ferngesehen."],
    ),
    rule(
        "Das Partizip II",
        "verbs",
        """
**Regular verbs**: **ge-** + stem + **-t**

- machen → **ge**mach**t**, spielen → **ge**spiel**t**, kaufen → **ge**kauf**t**
- stems in -t/-d add -et: arbeiten → **ge**arbeit**et**, reden → **ge**red**et**

**Irregular verbs**: **ge-** + (often changed) stem + **-en**. Learn them by heart:

| infinitive | Partizip II |
|---|---|
| essen | gegessen |
| trinken | getrunken |
| schreiben | geschrieben |
| lesen | gelesen |
| sehen | gesehen |
| schlafen | geschlafen |
| treffen | getroffen |
| sprechen | gesprochen |
| finden | gefunden |
| nehmen | genommen |
""",
        [
            "Ich habe ein Buch gelesen.",
            "Wir haben lange geschlafen.",
            "Er hat eine E-Mail geschrieben.",
        ],
    ),
    rule(
        "Perfekt: trennbar und -ieren",
        "verbs",
        """
- **Separable verbs**: *ge* goes **between** prefix and stem:
  ein**ge**kauft, auf**ge**räumt, an**ge**rufen, fern**ge**sehen, ein**ge**laden, mit**ge**bracht
- **Verbs ending in -ieren** get **no ge-**:
  telefonieren → telefonier**t**, fotografieren → fotografier**t**, studieren → studier**t**
""",
        [
            "Ich habe eingekauft.",
            "Hast du Oma angerufen?",
            "Wir haben im Urlaub viel fotografiert.",
        ],
    ),
    rule(
        "von … bis, ab, letzte Woche",
        "other",
        """
- **von … bis …**: a period: *von 9 **bis** 12 Uhr*
- **ab**: a starting point: ***ab** 8 Uhr, **ab** Montag*
- **gestern, vorgestern**: yesterday, the day before yesterday
- **letzt-** (last): *letzt**e** Woche, letzt**es** Jahr, letzt**en** Freitag*
- how many times: *einmal, zweimal, dreimal*
""",
        [
            "Von 9 bis 17 Uhr habe ich gearbeitet.",
            "Ab Montag habe ich Urlaub.",
            "Letzte Woche war ich krank.",
        ],
    ),
]

L11_LESSONS = [
    lesson(
        "Was hast du heute gemacht?",
        review("Was hast du heute gemacht?"),
        grammar("Perfekt mit haben"),
        conj("haben", "ich", "habe", hint="Perfekt helper: Ich ___ gespielt."),
        fill("Gestern ___ ich Fußball gespielt.", "habe"),
        fill("Was ___ du am Wochenende gemacht?", "hast"),
        fill("Wir ___ lange gearbeitet.", "haben"),
        fill("___ ihr Deutsch gelernt?", "Habt"),
        order("Ich habe heute viel gearbeitet."),
        order("Was hast du gestern gemacht?", "Build the question."),
    ),
    lesson(
        "Regelmäßige Partizipien",
        grammar("Das Partizip II"),
        fill("machen → ___", "gemacht"),
        fill("spielen → ___", "gespielt"),
        fill("kaufen → ___", "gekauft"),
        fill("lachen → ___", "gelacht"),
        fill("arbeiten → ___", "gearbeitet"),
        fill("reden → ___", "geredet"),
        mc("lernen → ?", "gelernt", "gelernen", "lernt"),
        mc("kochen → ?", "gekocht", "gekochen", "gekocht hat"),
        tr("I bought a present.", "Ich habe ein Geschenk gekauft."),
    ),
    lesson(
        "Unregelmäßige Partizipien",
        match(
            [
                ("essen", "gegessen"),
                ("trinken", "getrunken"),
                ("schreiben", "geschrieben"),
                ("schlafen", "geschlafen"),
                ("treffen", "getroffen"),
            ],
            "Match the infinitive and the Partizip II.",
        ),
        fill("lesen → ___", "gelesen"),
        fill("sehen → ___", "gesehen"),
        fill("sprechen → ___", "gesprochen"),
        fill("finden → ___", "gefunden"),
        fill("nehmen → ___", "genommen"),
        mc("Ich habe einen Kaffee ___.", "getrunken", "getrinkt", "trinken"),
        tr("We slept for a long time.", "Wir haben lange geschlafen."),
    ),
    lesson(
        "eingekauft, telefoniert",
        grammar("Perfekt: trennbar und -ieren"),
        fill("einkaufen → ___", "eingekauft"),
        fill("aufräumen → ___", "aufgeräumt"),
        fill("anrufen → ___", "angerufen"),
        fill("fernsehen → ___", "ferngesehen"),
        fill("einladen → ___", "eingeladen"),
        fill("telefonieren → ___", "telefoniert"),
        fill("fotografieren → ___", "fotografiert"),
        mc(
            "Which is correct?",
            "Ich habe eingekauft.",
            "Ich habe geeinkauft.",
            "Ich habe einkaufte.",
        ),
        mc(
            "Which is correct?",
            "Er hat telefoniert.",
            "Er hat getelefoniert.",
            "Er hat telefonieren.",
        ),
    ),
    lesson(
        "Mein Tag",
        grammar("von … bis, ab, letzte Woche"),
        order("Von neun bis zwölf habe ich gearbeitet."),
        order("Am Nachmittag habe ich eingekauft."),
        order("Am Abend haben wir ferngesehen."),
        fill("___ 8 Uhr bin ich im Büro. (from … on)", "Ab"),
        fill("Der Kurs ist von 18 ___ 20 Uhr.", "bis"),
        fill("Letzt___ Woche habe ich viel gelernt.", "e"),
        tr("Yesterday I tidied up.", "Gestern habe ich aufgeräumt.|Ich habe gestern aufgeräumt."),
    ),
    lesson(
        "Vom Präsens ins Perfekt",
        mc(
            "Ich kaufe ein. → Perfekt:",
            "Ich habe eingekauft.",
            "Ich habe gekauft ein.",
            "Ich bin eingekauft.",
        ),
        mc(
            "Er spielt Tennis. → Perfekt:",
            "Er hat Tennis gespielt.",
            "Er hat Tennis spielen.",
            "Er spielt Tennis gespielt.",
        ),
        mc(
            "Wir trinken Tee. → Perfekt:",
            "Wir haben Tee getrunken.",
            "Wir haben Tee getrinkt.",
            "Wir sind Tee getrunken.",
        ),
        mc(
            "Sie liest ein Buch. → Perfekt:",
            "Sie hat ein Buch gelesen.",
            "Sie hat ein Buch gelest.",
            "Sie hat ein Buch lesen.",
        ),
        tr("Did you call Anna? (informal)", "Hast du Anna angerufen?"),
        tr("We invited friends.", "Wir haben Freunde eingeladen."),
    ),
    lesson(
        "Eine E-Mail über gestern",
        bank(
            "Liebe Sara, gestern ___ ich lange geschlafen. Dann habe ich ___ und die Wohnung "
            "aufgeräumt. Am Abend ___ Tom und ich Freunde eingeladen. Wir haben viel ___. "
            "Liebe Grüße, Eva",
            ["habe", "eingekauft", "haben", "gelacht"],
            "bin",
            "gekauft",
        ),
        mc(
            "Gestern habe ich lange geschlafen. Dann habe ich eingekauft. What did Eva do first?",
            "She slept for a long time.",
            "She went shopping.",
            "She invited friends.",
        ),
        mc(
            "Wie war die Party? Sie war super! Was it boring?",
            "No, it was great.",
            "Yes, very boring.",
            "It didn't happen.",
        ),
        order("Die Party war wirklich interessant."),
    ),
    lesson(
        "Lektion 11: Test",
        mc("Ich ___ eine Pizza gegessen.", "habe", "bin", "hat"),
        fill("schreiben → ___", "geschrieben"),
        fill("mitbringen → ___", "mitgebracht"),
        mc("studieren → ?", "studiert", "gestudiert", "gestudieren"),
        order("Hast du die Hausaufgabe gemacht?", "Build the question."),
        tr(
            "Last week I worked a lot.",
            "Letzte Woche habe ich viel gearbeitet.|Ich habe letzte Woche viel gearbeitet.",
        ),
        fill("Ich habe ___ telefoniert. (twice)", "zweimal"),
    ),
]

LEKTION_11 = unit(
    11,
    "Was hast du heute gemacht?",
    "Perfekt mit haben",
    L11_WORDS,
    L11_RULES,
    interleave(L11_LESSONS, vocab_lessons(L11_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 12: Was ist denn hier passiert?
# ============================================================================

L12_WORDS = [
    ("the spring", "der Frühling", "noun"),
    ("the summer", "der Sommer", "noun"),
    ("the autumn", "der Herbst", "noun"),
    ("the winter", "der Winter", "noun"),
    ("the month", "der Monat", "noun", "Pl. die Monate"),
    ("January", "der Januar", "noun"),
    ("February", "der Februar", "noun"),
    ("March", "der März", "noun"),
    ("April", "der April", "noun"),
    ("May", "der Mai", "noun"),
    ("June", "der Juni", "noun"),
    ("July", "der Juli", "noun"),
    ("August", "der August", "noun"),
    ("September", "der September", "noun"),
    ("October", "der Oktober", "noun"),
    ("November", "der November", "noun"),
    ("December", "der Dezember", "noun"),
    ("the festival / party", "das Fest", "noun", "Pl. die Feste"),
    ("the celebration", "die Feier", "noun", "Pl. die Feiern"),
    ("the birthday", "der Geburtstag", "noun", "Pl. die Geburtstage"),
    ("the wedding", "die Hochzeit", "noun", "Pl. die Hochzeiten"),
    ("the carnival", "der Karneval", "noun"),
    ("New Year's Eve", "das Silvester", "noun"),
    ("the holiday / vacation", "der Urlaub", "noun", "Pl. die Urlaube"),
    ("the people", "die Leute", "noun", "plural only"),
    ("the person", "die Person", "noun", "Pl. die Personen"),
    ("the drinks", "die Getränke", "noun", "Sg. das Getränk"),
    ("to begin", "anfangen", "verb", "hat angefangen"),
    ("to stop / to end", "aufhören", "verb", "hat aufgehört"),
    ("to celebrate", "feiern", "verb", "hat gefeiert"),
    ("to last", "dauern", "verb", "hat gedauert"),
    ("to please (I like it)", "gefallen", "verb", "Das gefällt mir. / hat gefallen"),
    ("to give", "geben", "verb", "es gibt; hat gegeben"),
    ("to happen", "passieren", "verb", "ist passiert"),
    ("to jump", "springen", "verb", "ist gesprungen"),
    ("to stay", "bleiben", "verb", "ist geblieben"),
    ("happy", "glücklich", "adjective"),
    ("hard-working", "fleißig", "adjective"),
    ("fast", "schnell", "adjective"),
    ("comfortable", "bequem", "adjective"),
    ("clean", "sauber", "adjective"),
    ("little / few", "wenig", "adjective"),
    ("on the way / travelling", "unterwegs", "adverb"),
    ("Happy birthday!", "Herzlichen Glückwunsch zum Geburtstag!", "phrase"),
    ("What happened?", "Was ist passiert?", "phrase"),
]

L12_RULES = [
    rule(
        "Perfekt mit sein",
        "verbs",
        """
Verbs of **movement** (from A to B) and **change** use **sein** in the Perfekt:

| infinitive | Perfekt |
|---|---|
| gehen | ist gegangen |
| fahren | ist gefahren |
| fliegen | ist geflogen |
| kommen | ist gekommen |
| ankommen | ist angekommen |
| aufstehen | ist aufgestanden |
| springen | ist gesprungen |
| passieren | ist passiert |

Also with *sein*: **bleiben** (ist geblieben) and **sein** itself (ist gewesen).
""",
        ["Ich bin nach Wien gefahren.", "Wann bist du aufgestanden?", "Was ist passiert?"],
    ),
    rule(
        "haben oder sein?",
        "verbs",
        """
- **sein**: movement from one place to another (*gehen, fahren, fliegen, kommen*), a change
  (*aufstehen, passieren*), and *bleiben, sein*.
- **haben**: almost everything else, including verbs that don't move you anywhere
  (*essen, schlafen, arbeiten, feiern, gefallen*).

*Wir **sind** nach Berlin **gefahren** und **haben** dort **gefeiert**.*
""",
        [
            "Ich bin ins Kino gegangen. Der Film hat mir gefallen.",
            "Er ist zu Hause geblieben und hat geschlafen.",
        ],
    ),
    rule(
        "im Januar, im Sommer",
        "other",
        """
Months and seasons are all **masculine** (*der Mai, der Sommer*). Say when with **im**:

- ***im** Januar, **im** August*
- ***im** Frühling, **im** Sommer, **im** Herbst, **im** Winter*

Compare: ***am** Montag* (days), ***um** acht Uhr* (clock times).
""",
        ["Im Mai habe ich Geburtstag.", "Im Winter fahren wir Ski.", "Im Sommer ist es warm."],
    ),
    rule(
        "es gibt, gefallen",
        "other",
        """
- **es gibt** + accusative = *there is / there are*:
  *Es gibt **einen** Kuchen.* Perfekt: *Es **hat** einen Kuchen **gegeben**.*
- **gefallen** = *to please*. The thing you like is the subject; the person is *mir / dir*:
  *Das Fest **gefällt mir**.* (I like the party.) Perfekt: *Das Fest **hat mir gefallen**.*
""",
        [
            "Auf der Party hat es Musik gegeben.",
            "Gefällt dir das Geschenk?",
            "Die Hochzeit hat mir sehr gefallen.",
        ],
    ),
]

L12_LESSONS = [
    lesson(
        "Monate und Jahreszeiten",
        review("der Monat"),
        match(
            [
                ("der Frühling", "März, April, Mai"),
                ("der Sommer", "Juni, Juli, August"),
                ("der Herbst", "September, Oktober, November"),
                ("der Winter", "Dezember, Januar, Februar"),
            ],
            "Which months belong to which season?",
        ),
        fill("Januar, Februar, ___, April", "März"),
        fill("Oktober, November, ___", "Dezember"),
        mc("The month after Juni:", "Juli", "Juni", "August"),
        mc("Silvester is in …", "Dezember", "Januar", "Mai"),
    ),
    lesson(
        "im Januar, im Sommer",
        grammar("im Januar, im Sommer"),
        mc("___ Mai habe ich Geburtstag.", "Im", "Am", "Um"),
        mc("___ Montag fahre ich nach Hause.", "Am", "Im", "Um"),
        mc("Die Party fängt ___ acht Uhr an.", "um", "im", "am"),
        fill("___ Winter ist es kalt.", "Im"),
        fill("Wir machen ___ August Urlaub.", "im"),
        tr(
            "In summer we go to Italy.",
            "Im Sommer fahren wir nach Italien.|Wir fahren im Sommer nach Italien.",
        ),
    ),
    lesson(
        "Feste",
        review("der Geburtstag"),
        match(
            [
                ("der Geburtstag", "one more year"),
                ("die Hochzeit", "two people marry"),
                ("das Silvester", "31 December"),
                ("der Karneval", "costumes in February"),
            ]
        ),
        mc(
            "Your friend has a birthday. You say:",
            "Herzlichen Glückwunsch zum Geburtstag!",
            "Guten Appetit!",
            "Gute Reise!",
        ),
        conj("feiern", "wir", "feiern"),
        fill("Wann ___ die Party an? (anfangen)", "fängt"),
        fill("Wie lange ___ das Fest? (dauern)", "dauert"),
        order("Wir feiern am Samstag Geburtstag."),
    ),
    lesson(
        "Perfekt mit sein",
        grammar("Perfekt mit sein"),
        fill("Ich ___ nach Zürich gefahren.", "bin"),
        fill("Wann ___ du aufgestanden?", "bist"),
        fill("Der Zug ___ pünktlich angekommen.", "ist"),
        fill("Wir ___ nach Wien geflogen.", "sind"),
        fill("gehen → ist ___", "gegangen"),
        fill("fliegen → ist ___", "geflogen"),
        fill("bleiben → ist ___", "geblieben"),
        fill("sein → ist ___", "gewesen"),
        order("Was ist passiert?", "Build the question."),
    ),
    lesson(
        "haben oder sein?",
        grammar("haben oder sein?"),
        mc("Ich ___ ins Kino gegangen.", "bin", "habe"),
        mc("Wir ___ Pizza gegessen.", "haben", "sind"),
        mc("Er ___ nach Hause gefahren.", "ist", "hat"),
        mc("Sie ___ lange geschlafen.", "hat", "ist"),
        mc("Was ___ passiert?", "ist", "hat"),
        mc("Ihr ___ viel gefeiert.", "habt", "seid"),
        fill("Am Sonntag ___ ich zu Hause geblieben.", "bin"),
        fill("Der Film ___ mir gefallen.", "hat"),
        tr("We flew to Rome.", "Wir sind nach Rom geflogen."),
    ),
    lesson(
        "es gibt, gefallen",
        grammar("es gibt, gefallen"),
        mc("Auf dem Fest ___ es Musik und Getränke.", "gibt", "gefällt", "ist"),
        mc("Die Musik ___ mir.", "gefällt", "gibt", "magst"),
        fill("Gefällt ___ das Geschenk? (you, informal)", "dir"),
        fill("Es hat Kuchen ___. (geben)", "gegeben"),
        fill("Die Hochzeit hat mir sehr ___. (gefallen)", "gefallen"),
        tr("I like the city. (use gefallen)", "Die Stadt gefällt mir."),
    ),
    lesson(
        "Was ist denn hier passiert?",
        bank(
            "Im Juli ___ wir nach Hamburg gefahren. Wir haben eine Hochzeit ___. "
            "Die Party ___ bis drei Uhr gedauert. Es ___ mir sehr gefallen!",
            ["sind", "gefeiert", "hat", "hat"],
            "haben",
            "ist",
        ),
        mc(
            "Im Juli sind wir nach Hamburg gefahren. When did they travel?",
            "in July",
            "in June",
            "on Monday",
        ),
        mc(
            "Was ist passiert? Der Zug ist zu spät gekommen. What happened?",
            "The train was late.",
            "The train was early.",
            "There was no train.",
        ),
        order("Im Urlaub sind wir viel geschwommen."),
        tr("The party lasted three hours.", "Die Party hat drei Stunden gedauert."),
    ),
    lesson(
        "Lektion 12: Test",
        mc("Ich ___ um sieben aufgestanden.", "bin", "habe"),
        fill("kommen → ist ___", "gekommen"),
        mc("___ Herbst fahren wir nach Italien.", "Im", "Am", "Um"),
        mc("Das Fest ___ mir gefallen.", "hat", "ist"),
        tr("Happy birthday!", "Herzlichen Glückwunsch zum Geburtstag!|Alles Gute zum Geburtstag!"),
        order("Wann ist das Fest zu Ende?", "Build the question."),
        fill("Der Herbst kommt nach dem ___. (summer)", "Sommer"),
    ),
    lesson(
        "Modul 4: Wiederholung",
        fill("Ich steige in Köln ___. (umsteigen)", "um"),
        mc("Wir fahren ___ Straßenbahn.", "mit der", "mit dem"),
        conj("nehmen", "du", "nimmst"),
        mc("Gestern ___ ich eingekauft.", "habe", "bin"),
        mc("Gestern ___ ich nach Bonn gefahren.", "bin", "habe"),
        fill("telefonieren → ___", "telefoniert"),
        fill("trinken → ___", "getrunken"),
        bank(
            "Am Samstag ___ ich um neun aufgestanden. Dann habe ich ___. Am Abend ___ "
            "wir Geburtstag gefeiert. Das Fest hat mir ___!",
            ["bin", "eingekauft", "haben", "gefallen"],
            "habe",
            "gefällt",
        ),
        order("Im Dezember sind wir nach Wien geflogen."),
        tr("What did you do yesterday? (informal)", "Was hast du gestern gemacht?"),
    ),
]

LEKTION_12 = unit(
    12,
    "Was ist denn hier passiert?",
    "Perfekt mit sein, Monate, Feste",
    L12_WORDS,
    L12_RULES,
    interleave(L12_LESSONS, vocab_lessons(L12_WORDS, "Wörter")),
)


UNITS = [LEKTION_10, LEKTION_11, LEKTION_12]
