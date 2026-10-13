"""Modul 3: Lektion 7 (Du kannst wirklich toll …!), 8 (Kein Problem. Ich habe
Zeit!), 9 (Ich möchte was essen)."""

from ..dsl import (
    art,
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
# Lektion 7: Du kannst wirklich toll …!
# ============================================================================

L7_WORDS = [
    ("the free time", "die Freizeit", "noun"),
    ("the hobby", "das Hobby", "noun", "Pl. die Hobbys"),
    ("the trip / outing", "der Ausflug", "noun", "Pl. die Ausflüge"),
    ("the film", "der Film", "noun", "Pl. die Filme"),
    ("the cinema", "das Kino", "noun", "Pl. die Kinos"),
    ("the music", "die Musik", "noun"),
    ("the car", "das Auto", "noun", "Pl. die Autos"),
    ("the nature", "die Natur", "noun"),
    ("the internet", "das Internet", "noun"),
    ("the conversation", "das Gespräch", "noun", "Pl. die Gespräche"),
    ("football", "Fußball", "noun"),
    ("favourite film", "der Lieblingsfilm", "noun", "Lieblings- = favourite"),
    ("to cook", "kochen", "verb"),
    ("to sing", "singen", "verb"),
    ("to dance", "tanzen", "verb"),
    ("to swim", "schwimmen", "verb"),
    ("to take photos", "fotografieren", "verb"),
    ("to play", "spielen", "verb"),
    ("to read", "lesen", "verb", "du liest, er liest"),
    ("to paint / to draw", "malen", "verb"),
    ("to bake", "backen", "verb"),
    ("to visit", "besuchen", "verb"),
    ("to meet", "treffen", "verb", "du triffst, er trifft"),
    ("to love", "lieben", "verb"),
    ("to drive / to ride / to go (by vehicle)", "fahren", "verb", "du fährst, er fährt"),
    ("to cycle", "Rad fahren", "verb", "Ich fahre Rad."),
    ("to go for a walk", "spazieren gehen", "verb"),
    ("to surf the internet", "im Internet surfen", "phrase"),
    ("to smoke", "rauchen", "verb"),
    ("can / to be able to", "können", "verb", "ich kann, du kannst, er kann"),
    ("gladly / like to", "gern", "adverb", "Ich koche gern."),
    ("often", "oft", "adverb"),
    ("sometimes", "manchmal", "adverb"),
    ("never", "nie", "adverb"),
    ("almost always", "fast immer", "phrase"),
    ("of course", "natürlich", "adverb"),
    ("sure / clear", "klar", "adjective"),
    ("unfortunately", "leider", "adverb"),
    ("I'm sorry.", "Es tut mir leid.", "phrase"),
    ("That's fun.", "Das macht Spaß.", "phrase"),
    ("Thank you very much!", "Herzlichen Dank!", "phrase"),
    ("Can you help me?", "Kannst du mir helfen?", "phrase"),
]

L7_RULES = [
    rule(
        "können",
        "verbs",
        """
**können** says what someone can do. It is irregular in the singular:

| ich | du | er / sie | wir | ihr | sie / Sie |
|---|---|---|---|---|---|
| kann | kannst | kann | können | könnt | können |

With *können* the sentence has **two verb parts**: *können* is conjugated in **position 2**,
the other verb goes to the **end** in the infinitive.

- *Ich **kann** sehr gut **kochen**.*
- *Du **kannst** wirklich toll **tanzen**!*
- *Wir **können** heute nicht **kommen**.*

In questions *können* comes first: ***Kannst** du Auto **fahren**?*
""",
        ["Ich kann nicht schwimmen.", "Kannst du gut singen?", "Paul kann toll fotografieren."],
    ),
    rule(
        "lesen, fahren, treffen",
        "verbs",
        """
These verbs change their vowel in the **du** and **er/sie** forms, like *sprechen*:

| | lesen (e → ie) | fahren (a → ä) | treffen (e → i) |
|---|---|---|---|
| ich | lese | fahre | treffe |
| du | l**ie**st | f**ä**hrst | tr**i**ffst |
| er / sie | l**ie**st | f**ä**hrt | tr**i**fft |
| wir | lesen | fahren | treffen |

*lesen* has the same form for *du* and *er*: *du liest, er liest*.
""",
        ["Liest du gern?", "Sie fährt Rad.", "Er trifft am Abend Freunde."],
    ),
    rule(
        "gern und wie oft?",
        "other",
        """
Put **gern** after the verb to say you like doing something; **nicht gern** for the opposite:
*Ich koche **gern**. Er tanzt **nicht gern**.*

How often, from most to least:
**immer** → **fast immer** → **oft** → **manchmal** → **nie**

*Ich fahre **oft** Rad. Ich schwimme **nie**.*
""",
        ["Ich lese sehr gern.", "Wir gehen manchmal ins Kino.", "Er raucht nie."],
    ),
]

L7_LESSONS = [
    lesson(
        "Hobbys",
        review("das Hobby"),
        review("die Freizeit"),
        match(
            [
                ("kochen", "in the kitchen"),
                ("schwimmen", "in the water"),
                ("lesen", "a book"),
                ("fotografieren", "a camera"),
                ("tanzen", "in a club"),
            ],
            "Where or with what?",
        ),
        mc(
            "Was ist dein Hobby? Which answer fits?",
            "Ich male gern.",
            "Ich bin Lehrer.",
            "Ich wohne in Ulm.",
        ),
        fill("Ich ___ gern Fußball. (spielen)", "spiele"),
        fill("Wir ___ gern Musik. (hören)", "hören"),
        tr("My hobby is cooking.", "Mein Hobby ist Kochen.|Mein Hobby ist kochen."),
    ),
    lesson(
        "können",
        grammar("können"),
        conj("können", "ich", "kann"),
        conj("können", "du", "kannst"),
        conj("können", "er", "kann"),
        conj("können", "wir", "können"),
        conj("können", "ihr", "könnt"),
        fill("Mia ___ sehr gut singen.", "kann"),
        fill("___ du Auto fahren?", "Kannst"),
        fill("Ihr ___ toll tanzen!", "könnt"),
    ),
    lesson(
        "Ich kann gut kochen.",
        order("Ich kann sehr gut kochen."),
        order("Kannst du schwimmen?", "Build the question."),
        order("Wir können heute nicht kommen."),
        order("Paul kann toll fotografieren."),
        mc(
            "Which sentence is correct?",
            "Ich kann gut tanzen.",
            "Ich kann tanzen gut.",
            "Ich tanzen kann gut.",
        ),
        mc("Where does the second verb go?", "to the end", "to position 1", "after können"),
        tr("I can't swim.", "Ich kann nicht schwimmen."),
        tr("Can you cook? (informal)", "Kannst du kochen?"),
    ),
    lesson(
        "Komplimente",
        review("Das macht Spaß."),
        mc(
            "Your friend dances really well. You say:",
            "Du kannst wirklich toll tanzen!",
            "Du kannst nicht tanzen.",
            "Tanzt du?",
        ),
        mc(
            "Someone says: Du kannst toll kochen! You answer:",
            "Oh, vielen Dank!",
            "Es tut mir leid.",
            "Nein, bitte.",
        ),
        bank(
            "Wow, du ___ wirklich toll malen! Danke! Malen ___ mir viel Spaß.",
            ["kannst", "macht"],
            "kann",
            "hat",
        ),
        fill("Du kannst wirklich ___ singen! (great)", "toll"),
        order("Das macht viel Spaß."),
    ),
    lesson(
        "lesen, fahren, treffen",
        grammar("lesen, fahren, treffen"),
        conj("lesen", "du", "liest"),
        conj("lesen", "er", "liest"),
        conj("fahren", "du", "fährst"),
        conj("fahren", "sie (she)", "fährt"),
        conj("treffen", "du", "triffst"),
        conj("treffen", "er", "trifft"),
        fill("___ du gern Bücher? (lesen)", "Liest"),
        fill("Anna ___ oft Rad. (fahren)", "fährt"),
        fill("Am Abend ___ er Freunde. (treffen)", "trifft"),
    ),
    lesson(
        "gern und wie oft?",
        grammar("gern und wie oft?"),
        mc("Most often:", "fast immer", "oft", "manchmal", "nie"),
        mc("Least often:", "nie", "manchmal", "oft"),
        fill("Ich koche ___. Das macht Spaß! (gladly)", "gern"),
        fill("Er raucht ___. Er findet Rauchen schlecht. (never)", "nie"),
        order("Ich fahre oft Rad."),
        order("Wir gehen manchmal ins Kino."),
        tr("I like reading.", "Ich lese gern."),
        tr("She doesn't like swimming.", "Sie schwimmt nicht gern."),
    ),
    lesson(
        "Kannst du mir helfen?",
        review("Kannst du mir helfen?"),
        mc(
            "Your friend asks for help. You say yes:",
            "Klar! Natürlich.",
            "Leider nicht.",
            "Es geht.",
        ),
        mc(
            "You can't help. You say:",
            "Es tut mir leid, das geht leider nicht.",
            "Klar, gern!",
            "Herzlichen Dank!",
        ),
        bank(
            "Kannst du mir ___? Ja, ___. Was brauchst du? ___ Dank!",
            ["helfen", "natürlich", "Herzlichen"],
            "leider",
            "kochen",
        ),
        order("Kannst du mir helfen?", "Build the question."),
        tr("Unfortunately I can't.", "Leider kann ich nicht.|Ich kann leider nicht."),
    ),
    lesson(
        "Lektion 7: Test",
        mc("Er ___ gut schwimmen.", "kann", "kannst", "können"),
        fill("___ ihr Fußball spielen? (können)", "Könnt"),
        conj("fahren", "er", "fährt"),
        mc("Which sentence is correct?", "Liest du gern?", "Lest du gern?", "Lesst du gern?"),
        order("Mein Bruder kann sehr gut backen."),
        tr("We often visit friends.", "Wir besuchen oft Freunde."),
        mc("I'm sorry.", "Es tut mir leid.", "Das macht Spaß.", "Herzlichen Dank."),
    ),
]

LEKTION_7 = unit(
    7,
    "Du kannst wirklich toll …!",
    "Hobbys und Fähigkeiten",
    L7_WORDS,
    L7_RULES,
    sections(L7_LESSONS, vocab_lessons(L7_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 8: Kein Problem. Ich habe Zeit!
# ============================================================================

L8_WORDS = [
    ("the time", "die Zeit", "noun"),
    ("the time of day", "die Tageszeit", "noun", "Pl. die Tageszeiten"),
    ("the morning", "der Morgen", "noun"),
    ("the late morning", "der Vormittag", "noun"),
    ("the midday / noon", "der Mittag", "noun"),
    ("the afternoon", "der Nachmittag", "noun"),
    ("the evening", "der Abend", "noun"),
    ("the night", "die Nacht", "noun", "Pl. die Nächte"),
    ("the day", "der Tag", "noun", "Pl. die Tage"),
    ("the week", "die Woche", "noun", "Pl. die Wochen"),
    ("the weekend", "das Wochenende", "noun", "Pl. die Wochenenden"),
    ("Monday", "der Montag", "noun"),
    ("Tuesday", "der Dienstag", "noun"),
    ("Wednesday", "der Mittwoch", "noun"),
    ("Thursday", "der Donnerstag", "noun"),
    ("Friday", "der Freitag", "noun"),
    ("Saturday", "der Samstag", "noun"),
    ("Sunday", "der Sonntag", "noun"),
    ("the hour", "die Stunde", "noun", "Pl. die Stunden"),
    ("the minute", "die Minute", "noun", "Pl. die Minuten"),
    ("the café", "das Café", "noun", "Pl. die Cafés"),
    ("the restaurant", "das Restaurant", "noun", "Pl. die Restaurants"),
    ("the pub", "die Kneipe", "noun", "Pl. die Kneipen"),
    ("the bar", "die Bar", "noun", "Pl. die Bars"),
    ("the club / disco", "die Disco", "noun", "Pl. die Discos"),
    ("the concert", "das Konzert", "noun", "Pl. die Konzerte"),
    ("the museum", "das Museum", "noun", "Pl. die Museen"),
    ("the theatre", "das Theater", "noun", "Pl. die Theater"),
    ("the swimming pool", "das Schwimmbad", "noun", "Pl. die Schwimmbäder"),
    ("the exhibition", "die Ausstellung", "noun", "Pl. die Ausstellungen"),
    ("the idea", "die Idee", "noun", "Pl. die Ideen"),
    ("the desire (to feel like)", "die Lust", "noun", "Lust haben"),
    ("to go (on foot)", "gehen", "verb"),
    ("to see / to watch", "sehen", "verb", "du siehst, er sieht"),
    ("tomorrow", "morgen", "adverb"),
    ("maybe", "vielleicht", "adverb"),
    ("late", "spät", "adjective"),
    ("soon", "bald", "adverb"),
    ("rather / preferably", "lieber", "adverb"),
    ("especially", "besonders", "adverb"),
    ("when", "wann", "other"),
    ("Do you have time?", "Hast du Zeit?", "phrase"),
    ("Do you feel like it?", "Hast du Lust?", "phrase"),
    ("Unfortunately that doesn't work.", "Das geht leider nicht.", "phrase"),
    ("Maybe another time.", "Vielleicht ein anderes Mal.", "phrase"),
    ("Excuse me / sorry", "Entschuldigung", "phrase"),
    ("Yes, I'd love to.", "Ja, gern.", "phrase"),
    ("What time is it?", "Wie spät ist es?", "phrase"),
]

L8_RULES = [
    rule(
        "Die Uhrzeit",
        "other",
        """
Ask: ***Wie spät ist es?*** or ***Wie viel Uhr ist es?***

**Formal** (timetables, radio): hours + *Uhr* + minutes: *8:15 = acht Uhr fünfzehn*, *20:30 = zwanzig Uhr dreißig*.

**Informal** (everyday), 12-hour:

| time | say |
|---|---|
| 8:00 | acht (Uhr) |
| 8:15 | Viertel **nach** acht |
| 8:30 | **halb neun** (half *to* nine!) |
| 8:45 | Viertel **vor** neun |
| 8:10 | zehn nach acht |
| 8:50 | zehn vor neun |

Careful: ***halb neun*** is 8:30, not 9:30.
""",
        ["Es ist halb acht.", "Es ist Viertel nach drei.", "Der Film beginnt um 20 Uhr."],
    ),
    rule(
        "am, um, in der",
        "other",
        """
- **am** + day or part of the day: *am Montag, am Wochenende, am Abend, am Nachmittag*
- **in der** + Nacht: *in der Nacht*
- **um** + clock time: *um 8 Uhr, um halb drei*
- Ask with **Wann?** (when?) or **Um wie viel Uhr?** (at what time?)
""",
        ["Am Freitag habe ich Zeit.", "Wir treffen uns um sieben.", "In der Nacht schlafe ich."],
    ),
    rule(
        "Das Verb an Position 2",
        "sentence_structure",
        """
In a statement the **conjugated verb is always in position 2**. If something else comes
first (a time, a place), the subject moves **after** the verb:

| 1 | 2 (verb) | 3 | rest |
|---|---|---|---|
| Ich | habe | am Samstag | Zeit. |
| Am Samstag | habe | ich | Zeit. |
| Heute | gehe | ich | ins Kino. |
""",
        [
            "Morgen kann ich nicht.",
            "Am Abend gehen wir ins Theater.",
            "Um acht Uhr frühstücke ich.",
        ],
    ),
]

L8_LESSONS = [
    lesson(
        "Tage und Tageszeiten",
        review("die Woche"),
        review("das Wochenende"),
        mc("The day after Montag:", "Dienstag", "Mittwoch", "Sonntag"),
        mc("The day before Samstag:", "Freitag", "Sonntag", "Donnerstag"),
        mc("Samstag and Sonntag are the …", "Wochenende", "Woche", "Tageszeit"),
        match(
            [
                ("der Morgen", "7:00"),
                ("der Mittag", "12:00"),
                ("der Nachmittag", "15:00"),
                ("der Abend", "19:00"),
                ("die Nacht", "2:00"),
            ],
            "Which part of the day?",
        ),
        fill("Montag, Dienstag, ___, Donnerstag", "Mittwoch"),
    ),
    lesson(
        "Wie spät ist es?",
        grammar("Die Uhrzeit"),
        match(
            [
                ("8:15", "Viertel nach acht"),
                ("8:30", "halb neun"),
                ("8:45", "Viertel vor neun"),
                ("8:50", "zehn vor neun"),
            ],
            "Match the times.",
        ),
        mc("halb drei is …", "2:30", "3:30", "3:00"),
        mc("Viertel vor sieben is …", "6:45", "7:15", "7:45"),
        mc(
            "Formal: 20:15 is …",
            "zwanzig Uhr fünfzehn",
            "Viertel nach zwanzig",
            "acht Uhr fünfzehn",
        ),
        fill("7:30 = halb ___", "acht"),
        fill("10:15 = Viertel ___ zehn", "nach"),
        fill("4:45 = Viertel ___ fünf", "vor"),
        order("Wie spät ist es?", "Build the question."),
    ),
    lesson(
        "am, um, in der",
        grammar("am, um, in der"),
        mc("___ Montag habe ich keine Zeit.", "Am", "Um", "In"),
        mc("Der Film beginnt ___ 20 Uhr.", "um", "am", "in"),
        mc("___ Nacht schlafe ich.", "In der", "Am", "Um"),
        fill("Wir treffen uns ___ Wochenende.", "am"),
        fill("Das Konzert ist ___ halb neun.", "um"),
        fill("___ Abend gehe ich ins Kino.", "Am"),
        mc(
            "Wann hast du Zeit? Which answer fits?", "Am Freitag um sechs.", "Im Kino.", "Ja, gern."
        ),
        tr("On Sunday at ten o'clock.", "Am Sonntag um zehn Uhr.|Am Sonntag um zehn."),
    ),
    lesson(
        "Das Verb an Position 2",
        grammar("Das Verb an Position 2"),
        order("Am Samstag habe ich Zeit."),
        order("Heute gehe ich ins Kino."),
        order("Morgen kann ich leider nicht."),
        order("Am Abend sehen wir einen Film."),
        mc(
            "Which sentence is correct?",
            "Am Freitag gehe ich ins Theater.",
            "Am Freitag ich gehe ins Theater.",
            "Am Freitag ins Theater gehe ich.",
        ),
        tr("Tomorrow I have time.", "Morgen habe ich Zeit."),
        tr("On Monday we go to the museum.", "Am Montag gehen wir ins Museum."),
    ),
    lesson(
        "Wohin gehen wir?",
        review("das Café"),
        match(
            [
                ("das Kino", "a film"),
                ("das Konzert", "music"),
                ("das Museum", "an exhibition"),
                ("das Schwimmbad", "swimming"),
                ("das Restaurant", "dinner"),
            ],
            "What do you do there?",
        ),
        mc("You want to watch a play. You go to the …", "Theater", "Schwimmbad", "Café"),
        mc("Gehen wir ins Kino? Wir ___ einen Film.", "sehen", "essen", "trinken"),
        conj("sehen", "du", "siehst"),
        conj("sehen", "er", "sieht"),
        fill("___ du heute Abend einen Film? (sehen)", "Siehst"),
        tr("Let's go to the café.", "Wir gehen ins Café.|Gehen wir ins Café."),
    ),
    lesson(
        "Hast du Zeit?",
        review("Hast du Zeit?"),
        mc(
            "Hast du am Freitag Zeit? You can:",
            "Ja, gern. Wann denn?",
            "Das geht leider nicht.",
            "Vielleicht ein anderes Mal.",
        ),
        mc(
            "Hast du Lust auf Kino? You can't:",
            "Das geht leider nicht. Vielleicht ein anderes Mal?",
            "Ja, gern!",
            "Klar, um acht.",
        ),
        bank(
            "Hallo Jana, hast du am Samstag ___? Wir gehen ins Konzert. Hast du ___? "
            "Ja, ___! Um wie viel ___? Um acht.",
            ["Zeit", "Lust", "gern", "Uhr"],
            "leider",
            "Idee",
        ),
        order("Hast du am Sonntag Zeit?", "Build the question."),
        order("Vielleicht ein anderes Mal."),
        fill("Am Montag geht es ___ nicht. Ich muss arbeiten. (unfortunately)", "leider"),
        tr("Do you feel like going to the cinema? (informal)", "Hast du Lust auf Kino?"),
    ),
    lesson(
        "Eine Nachricht",
        bank(
            "Hi Tom! Hast du ___ Abend Zeit? Wir gehen ___ 19 Uhr in die Kneipe. "
            "Kommst du ___? Liebe Grüße, Mia",
            ["am", "um", "mit"],
            "in",
            "im",
        ),
        mc(
            "Hi Tom! Hast du am Abend Zeit? Wir gehen um 19 Uhr in die Kneipe. When do they meet?",
            "at 7 p.m.",
            "at 9 p.m.",
            "tomorrow morning",
        ),
        mc(
            "Liebe Mia, heute kann ich leider nicht. Aber morgen habe ich Zeit! Tom. Does Tom come today?",
            "No, but tomorrow he has time.",
            "Yes, at 7.",
            "He doesn't answer.",
        ),
        tr("Sorry, I'm late.", "Entschuldigung, ich bin spät.|Entschuldigung, ich komme spät."),
        order("Ich gehe lieber ins Schwimmbad."),
    ),
    lesson(
        "Lektion 8: Test",
        mc("halb zehn is …", "9:30", "10:30", "10:00"),
        fill("Wir treffen uns ___ Dienstag um acht Uhr.", "am"),
        mc(
            "Which sentence is correct?",
            "Morgen habe ich Zeit.",
            "Morgen ich habe Zeit.",
            "Morgen Zeit habe ich.",
        ),
        conj("sehen", "sie (she)", "sieht"),
        tr("When do you have time? (informal)", "Wann hast du Zeit?"),
        order("Das Museum ist am Montag geschlossen."),
        mc("Excuse me!", "Entschuldigung!", "Kein Problem!", "Vielleicht!"),
    ),
]

LEKTION_8 = unit(
    8,
    "Kein Problem. Ich habe Zeit!",
    "Verabredungen und Uhrzeit",
    L8_WORDS,
    L8_RULES,
    sections(L8_LESSONS, vocab_lessons(L8_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 9: Ich möchte was essen.
# ============================================================================

L9_WORDS = [
    ("the groceries", "die Lebensmittel", "noun", "plural"),
    ("the apple", "der Apfel", "noun", "Pl. die Äpfel"),
    ("the bread", "das Brot", "noun", "Pl. die Brote"),
    ("the bread roll", "das Brötchen", "noun", "Pl. die Brötchen"),
    ("the butter", "die Butter", "noun"),
    ("the egg", "das Ei", "noun", "Pl. die Eier"),
    ("the ice cream", "das Eis", "noun"),
    ("the fish", "der Fisch", "noun", "Pl. die Fische"),
    ("the meat", "das Fleisch", "noun"),
    ("the roast", "der Braten", "noun", "Pl. die Braten"),
    ("the cheese", "der Käse", "noun"),
    ("the potato", "die Kartoffel", "noun", "Pl. die Kartoffeln"),
    ("the cake", "der Kuchen", "noun", "Pl. die Kuchen"),
    ("the milk", "die Milch", "noun"),
    ("the fruit", "das Obst", "noun"),
    ("the vegetables", "das Gemüse", "noun"),
    ("the orange", "die Orange", "noun", "Pl. die Orangen"),
    ("the rice", "der Reis", "noun"),
    ("the cream", "die Sahne", "noun"),
    ("the salad", "der Salat", "noun", "Pl. die Salate"),
    ("the ham", "der Schinken", "noun"),
    ("the chocolate", "die Schokolade", "noun"),
    ("the soup", "die Suppe", "noun", "Pl. die Suppen"),
    ("the tea", "der Tee", "noun"),
    ("the coffee", "der Kaffee", "noun"),
    ("the water", "das Wasser", "noun"),
    ("the juice", "der Saft", "noun", "Pl. die Säfte"),
    ("the beer", "das Bier", "noun"),
    ("the tomato", "die Tomate", "noun", "Pl. die Tomaten"),
    ("the sausage", "die Wurst", "noun", "Pl. die Würste"),
    ("the lemon", "die Zitrone", "noun", "Pl. die Zitronen"),
    ("the onion", "die Zwiebel", "noun", "Pl. die Zwiebeln"),
    ("the cucumber", "die Gurke", "noun", "Pl. die Gurken"),
    ("the breakfast", "das Frühstück", "noun"),
    ("the lunch", "das Mittagessen", "noun"),
    ("the dinner", "das Abendessen", "noun"),
    ("the hunger", "der Hunger", "noun", "Hunger haben"),
    ("the thirst", "der Durst", "noun", "Durst haben"),
    ("the fridge", "der Kühlschrank", "noun", "Pl. die Kühlschränke"),
    ("the menu", "die Speisekarte", "noun", "Pl. die Speisekarten"),
    ("the starter", "die Vorspeise", "noun", "Pl. die Vorspeisen"),
    ("the main course", "das Hauptgericht", "noun", "Pl. die Hauptgerichte"),
    ("to eat", "essen", "verb", "du isst, er isst"),
    ("to drink", "trinken", "verb"),
    ("to have breakfast", "frühstücken", "verb"),
    ("to taste", "schmecken", "verb"),
    ("to like", "mögen", "verb", "ich mag, du magst, er mag"),
    ("would like", "möchten", "verb", "ich möchte, du möchtest"),
    ("fresh", "frisch", "adjective"),
    ("something", "etwas", "other"),
    ("Enjoy your meal!", "Guten Appetit!", "phrase"),
    ("Same to you!", "Danke, gleichfalls!", "phrase"),
    ("That tastes good.", "Das schmeckt gut.", "phrase"),
]

L9_RULES = [
    rule(
        "möchten",
        "verbs",
        """
**möchte** (would like) is the polite way to say what you want, especially when ordering:

| ich | du | er / sie | wir | ihr | sie / Sie |
|---|---|---|---|---|---|
| möchte | möchtest | möchte | möchten | möchtet | möchten |

- With a noun (accusative): *Ich möchte **einen** Kaffee / **eine** Suppe / **ein** Wasser.*
- With a verb at the end: *Ich möchte etwas **essen**.*
- *ich* and *er/sie* have the same form: *ich möchte, sie möchte*.
""",
        ["Ich möchte einen Tee, bitte.", "Möchten Sie etwas trinken?", "Wir möchten bestellen."],
    ),
    rule(
        "mögen",
        "verbs",
        """
**mögen** means *to like* (in general). Don't confuse it with *möchten* (would like, now).

| ich | du | er / sie | wir | ihr | sie / Sie |
|---|---|---|---|---|---|
| mag | magst | mag | mögen | mögt | mögen |

- *Ich **mag** Käse.* (I like cheese, always.)
- *Ich **möchte** Käse.* (I'd like some cheese, now.)
- With an activity, use **gern**: *Ich esse **gern** Fisch.* / *Ich esse **nicht gern** Fleisch.*
- *Ich mag **keinen** Fisch.* (kein- + accusative)
""",
        ["Magst du Schokolade?", "Er mag keinen Kaffee.", "Wir essen gern Salat."],
    ),
    rule(
        "Komposita",
        "other",
        """
German joins nouns into one word. The **last** noun decides the meaning and the **article**:

- *die Kartoffel* + *die Suppe* → **die** Kartoffelsuppe
- *der Apfel* + *der Kuchen* → **der** Apfelkuchen
- *der Schinken* + *das Brot* → **das** Schinkenbrot
- *die Tomate* + *der Salat* → **der** Tomatensalat

The **first** part carries the main stress: *KARtoffelsuppe*.
""",
        [
            "Ich möchte eine Tomatensuppe.",
            "Der Apfelkuchen schmeckt gut.",
            "Das Käsebrötchen ist frisch.",
        ],
    ),
]

L9_LESSONS = [
    lesson(
        "Lebensmittel",
        review("die Lebensmittel"),
        review("das Obst"),
        mc("Which is Obst?", "der Apfel", "die Kartoffel", "die Zwiebel"),
        mc("Which is Gemüse?", "die Tomate", "die Orange", "die Zitrone"),
        mc("Which is a drink?", "der Saft", "der Käse", "das Brötchen"),
        mc("Which comes from a cow?", "die Milch", "das Ei", "der Reis"),
        fill("Ich trinke Tee mit ___. (lemon)", "Zitrone"),
        fill("Morgens esse ich ein Brötchen mit ___. (butter)", "Butter"),
    ),
    lesson(
        "Frühstück, Mittagessen, Abendessen",
        match(
            [
                ("das Frühstück", "in the morning"),
                ("das Mittagessen", "at midday"),
                ("das Abendessen", "in the evening"),
            ],
            "When do you eat it?",
        ),
        conj("essen", "du", "isst"),
        conj("essen", "er", "isst"),
        conj("trinken", "ihr", "trinkt"),
        fill("Was ___ du zum Frühstück? (essen)", "isst"),
        fill("Ich ___ jeden Tag um sieben. (frühstücken)", "frühstücke"),
        order("Zum Frühstück trinke ich Kaffee."),
        tr("I'm hungry.", "Ich habe Hunger."),
        tr("Are you thirsty? (informal)", "Hast du Durst?"),
    ),
    lesson(
        "möchten",
        grammar("möchten"),
        conj("möchten", "ich", "möchte"),
        conj("möchten", "du", "möchtest"),
        conj("möchten", "er", "möchte"),
        conj("möchten", "ihr", "möchtet"),
        fill("Ich ___ einen Kaffee, bitte.", "möchte"),
        fill("___ Sie etwas trinken?", "Möchten"),
        mc("Ich möchte ___ Tee.", "einen", "ein", "eine"),
        mc("Ich möchte ___ Suppe.", "eine", "einen", "ein"),
        mc("Ich möchte ___ Wasser.", "ein", "einen", "eine"),
    ),
    lesson(
        "mögen",
        grammar("mögen"),
        conj("mögen", "ich", "mag"),
        conj("mögen", "du", "magst"),
        conj("mögen", "wir", "mögen"),
        conj("mögen", "ihr", "mögt"),
        fill("___ du Schokolade? (mögen)", "Magst"),
        fill("Er ___ keinen Fisch. (mögen)", "mag"),
        mc("I like cheese (always):", "Ich mag Käse.", "Ich möchte Käse."),
        mc(
            "I'd like a coffee now, please:",
            "Ich möchte einen Kaffee, bitte.",
            "Ich mag einen Kaffee, bitte.",
        ),
        tr("I don't like meat.", "Ich mag kein Fleisch.|Ich esse nicht gern Fleisch."),
    ),
    lesson(
        "gern und nicht gern",
        order("Ich esse gern Fisch."),
        order("Sie trinkt nicht gern Milch."),
        order("Isst du gern Salat?", "Build the question."),
        mc("Ich esse ___ Gemüse. Es ist gesund!", "gern", "nie", "nicht gern"),
        fill("Wir essen nicht ___ Wurst. (like)", "gern"),
        bank(
            "Ich ___ Kuchen sehr gern. Aber ich ___ keine Sahne. Und du? Ich ___ lieber Eis.",
            ["esse", "mag", "esse"],
            "möchte",
            "isst",
        ),
        tr("Do you like coffee? (informal)", "Magst du Kaffee?|Trinkst du gern Kaffee?"),
    ),
    lesson(
        "Komposita",
        grammar("Komposita"),
        mc(
            "die Kartoffel + die Suppe =",
            "die Kartoffelsuppe",
            "der Kartoffelsuppe",
            "das Kartoffelsuppe",
        ),
        mc("der Apfel + der Kuchen =", "der Apfelkuchen", "die Apfelkuchen", "das Apfelkuchen"),
        mc("der Schinken + das Brot =", "das Schinkenbrot", "der Schinkenbrot", "die Schinkenbrot"),
        art("der Tomatensalat", hint="Tomate + Salat"),
        art("die Fischsuppe", hint="Fisch + Suppe"),
        art("das Käsebrötchen", hint="Käse + Brötchen"),
        art("der Orangensaft", hint="Orange + Saft"),
        fill("der Kaffee + die Milch = die ___", "Kaffeemilch"),
        match(
            [
                ("die Zwiebelsuppe", "onion soup"),
                ("der Schokoladenkuchen", "chocolate cake"),
                ("das Schinkenbrot", "ham sandwich"),
                ("der Apfelsaft", "apple juice"),
            ]
        ),
    ),
    lesson(
        "Im Café",
        review("die Speisekarte"),
        bank(
            "Guten Tag! Was ___ Sie? Ich möchte eine Gemüsesuppe und ein ___, bitte. "
            "Und zu trinken? Einen ___. Gern!",
            ["möchten", "Brötchen", "Saft"],
            "mögen",
            "Durst",
        ),
        mc(
            "The waiter asks: Was möchten Sie trinken? You say:",
            "Ein Wasser, bitte.",
            "Ich mag Wasser.",
            "Ich trinke Wasser gern.",
        ),
        mc(
            "Möchten Sie noch etwas? You don't want more:",
            "Nein, danke.",
            "Ja, gern.",
            "Guten Appetit!",
        ),
        mc("Before eating, you say:", "Guten Appetit!", "Danke, gleichfalls!", "Auf Wiedersehen!"),
        mc(
            "Someone says Guten Appetit! You answer:",
            "Danke, gleichfalls!",
            "Guten Appetit!",
            "Bitte schön!",
        ),
        order("Ich möchte etwas essen."),
        tr("The soup tastes good.", "Die Suppe schmeckt gut."),
    ),
    lesson(
        "Lektion 9: Test",
        mc("Ich ___ einen Apfelsaft, bitte.", "möchte", "mag", "möchtest"),
        fill("Was ___ du zum Mittagessen? (essen)", "isst"),
        conj("mögen", "er", "mag"),
        mc(
            "die Kartoffel + der Salat =",
            "der Kartoffelsalat",
            "die Kartoffelsalat",
            "das Kartoffelsalat",
        ),
        tr("We would like to order.", "Wir möchten bestellen."),
        order("Magst du keinen Käse?", "Build the question."),
        mc("Durst haben means:", "to be thirsty", "to be hungry", "to be tired"),
    ),
    lesson(
        "Modul 3: Wiederholung",
        fill("___ du schwimmen? (können)", "Kannst"),
        order("Ich kann nicht gut singen."),
        conj("lesen", "du", "liest"),
        mc("Viertel nach drei is …", "3:15", "2:45", "3:45"),
        mc("___ Samstag ___ 10 Uhr", "Am … um", "Um … am", "In … am"),
        order("Am Sonntag habe ich Zeit."),
        mc("Ich ___ Tee. (I like it in general)", "mag", "möchte"),
        bank(
            "Hast du ___ auf ein Eis? Ja, gern! Ich ___ ein Schokoladeneis. Und du? "
            "Ich ___ lieber Apfelkuchen.",
            ["Lust", "möchte", "esse"],
            "Zeit",
            "mag",
        ),
        tr("I often go to the cinema.", "Ich gehe oft ins Kino."),
        art("der Zitronenkuchen", hint="Zitrone + Kuchen"),
    ),
]

LEKTION_9 = unit(
    9,
    "Ich möchte was essen.",
    "Essen und Trinken",
    L9_WORDS,
    L9_RULES,
    sections(L9_LESSONS, vocab_lessons(L9_WORDS, "Wörter")),
)


UNITS = [LEKTION_7, LEKTION_8, LEKTION_9]
