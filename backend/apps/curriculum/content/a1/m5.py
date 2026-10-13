"""Modul 5 (A1.2): Lektion 13 (Wir suchen das Hotel Maritim), 14 (Wie findest du
Ottos Haus?), 15 (In Giesing wohnt das Leben!)."""

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
# Lektion 13: Wir suchen das Hotel Maritim.
# ============================================================================

L13_WORDS = [
    ("the hotel", "das Hotel", "noun", "Pl. die Hotels"),
    ("the traffic light", "die Ampel", "noun", "Pl. die Ampeln"),
    ("the bank", "die Bank", "noun", "Pl. die Banken"),
    ("the bridge", "die Brücke", "noun", "Pl. die Brücken"),
    ("the cathedral", "der Dom", "noun", "Pl. die Dome"),
    ("the city centre", "die Stadtmitte", "noun"),
    ("the centre", "das Zentrum", "noun", "Pl. die Zentren"),
    ("the city map", "der Stadtplan", "noun", "Pl. die Stadtpläne"),
    ("the police", "die Polizei", "noun"),
    ("the post office", "die Post", "noun"),
    ("the street", "die Straße", "noun", "Pl. die Straßen"),
    ("the crossroads", "die Kreuzung", "noun", "Pl. die Kreuzungen"),
    ("the way / path", "der Weg", "noun", "Pl. die Wege"),
    ("the kilometre", "der Kilometer", "noun", "Pl. die Kilometer"),
    ("the metre", "der Meter", "noun", "Pl. die Meter"),
    ("the question", "die Frage", "noun", "Pl. die Fragen"),
    ("the moment", "der Moment", "noun", "Pl. die Momente"),
    ("to turn (left, right)", "abbiegen", "verb", "Sie biegen links ab."),
    ("to drive on / keep going", "weiterfahren", "verb"),
    ("to turn around", "wenden", "verb"),
    ("to drive back", "zurückfahren", "verb"),
    ("to describe", "beschreiben", "verb"),
    ("to help", "helfen", "verb", "du hilfst, er hilft (+ Dativ)"),
    ("to know (a person, a place)", "kennen", "verb"),
    ("to be right / correct", "stimmen", "verb", "Das stimmt."),
    ("left", "links", "adverb"),
    ("right", "rechts", "adverb"),
    ("straight on", "geradeaus", "adverb"),
    ("foreign / a stranger here", "fremd", "adjective"),
    ("nice / kind", "nett", "adjective"),
    ("both", "beide", "other"),
    ("in / inside", "in", "other", "Wo? in + Dativ: im Hotel"),
    ("at / on (a vertical surface)", "an", "other", "am Bahnhof"),
    ("on (top of)", "auf", "other"),
    ("next to", "neben", "other"),
    ("behind", "hinter", "other"),
    ("in front of / ago (time)", "vor", "other", "vor dem Haus; vor einer Stunde"),
    ("between", "zwischen", "other"),
    ("above / over", "über", "other"),
    ("under", "unter", "other"),
    ("near (nearby)", "in der Nähe", "phrase"),
    ("I'm not from here.", "Ich bin nicht von hier.", "phrase"),
    ("Oh, I see.", "Ach so.", "phrase"),
    ("What a pity!", "Schade!", "phrase"),
    ("One moment!", "Einen Moment!", "phrase"),
]

L13_RULES = [
    rule(
        "Wo? Präpositionen mit Dativ",
        "cases",
        """
To say **where** something is (*Wo?*), use one of these prepositions + **dative**:

**in, an, auf, neben, hinter, vor, zwischen, über, unter**

- Das Hotel ist **neben dem** Dom.
- Die Post ist **zwischen der** Bank **und dem** Café.
- Der Bus wartet **vor dem** Bahnhof.
- Die Lampe hängt **über dem** Tisch.
""",
        [
            "Das Café ist hinter der Kirche.",
            "Wir warten an der Ampel.",
            "Der Stadtplan liegt auf dem Tisch.",
        ],
    ),
    rule(
        "Dativ: dem, der, den",
        "cases",
        """
| | nominative | dative |
|---|---|---|
| masculine | der Dom | **dem** Dom |
| neuter | das Hotel | **dem** Hotel |
| feminine | die Bank | **der** Bank |
| plural | die Häuser | **den** Häuser**n** |

- **in dem → im**: *Das Hotel liegt **im** Zentrum.*
- **an dem → am**: *Wir treffen uns **am** Bahnhof.*
- Plural nouns add **-n** in the dative where they can.
""",
        ["Ich bin im Hotel.", "Er wartet am Dom.", "Die Bank ist neben der Post."],
    ),
    rule(
        "Den Weg beschreiben",
        "other",
        """
Ask politely:

- *Entschuldigung, können Sie mir helfen?*
- *Ich suche das Hotel Maritim.* / *Wo ist hier eine Bank?*

Give directions:

- *Gehen / Fahren Sie **geradeaus**.*
- *Biegen Sie an der Ampel **links** / **rechts ab**.*
- *Das ist **in der Nähe** vom Bahnhof.*

If you don't know: *Tut mir leid, **ich bin nicht von hier**.*
""",
        [
            "Fahren Sie geradeaus und dann rechts.",
            "Biegen Sie an der Kreuzung links ab.",
            "Das Hotel ist ganz in der Nähe.",
        ],
    ),
]

L13_LESSONS = [
    lesson(
        "In der Stadt",
        review("das Hotel"),
        review("die Ampel"),
        match(
            [
                ("die Bank", "you get money"),
                ("die Post", "you send letters"),
                ("die Polizei", "you call for help"),
                ("der Dom", "a big church"),
                ("die Brücke", "you cross the river"),
            ]
        ),
        mc("Red, yellow, green: it is the …", "Ampel", "Brücke", "Kreuzung"),
        mc("You look for streets on a …", "Stadtplan", "Fahrplan", "Kalender"),
        fill("Das Hotel ist im ___. (centre)", "Zentrum"),
    ),
    lesson(
        "Wo ist das Hotel?",
        grammar("Wo? Präpositionen mit Dativ"),
        match(
            [
                ("neben", "next to"),
                ("hinter", "behind"),
                ("vor", "in front of"),
                ("zwischen", "between"),
                ("über", "above"),
                ("unter", "under"),
            ]
        ),
        mc(
            "The bag is under the table:",
            "Die Tasche ist unter dem Tisch.",
            "Die Tasche ist über dem Tisch.",
            "Die Tasche ist auf dem Tisch.",
        ),
        mc(
            "The car is behind the house:",
            "Das Auto ist hinter dem Haus.",
            "Das Auto ist vor dem Haus.",
            "Das Auto ist neben dem Haus.",
        ),
        fill("Die Lampe hängt ___ dem Tisch. (above)", "über"),
        fill("Der Bus hält ___ dem Bahnhof. (in front of)", "vor"),
        order("Das Hotel ist neben dem Dom."),
    ),
    lesson(
        "dem, der, den",
        grammar("Dativ: dem, der, den"),
        mc("Das Café ist neben ___ Dom.", "dem", "der", "den"),
        mc("Die Post ist hinter ___ Bank.", "der", "dem", "die"),
        mc("Das Kino ist neben ___ Hotel.", "dem", "der", "das"),
        mc("Die Kinder spielen zwischen ___ Häusern.", "den", "dem", "der"),
        fill("Wir warten vor ___ Ampel.", "der"),
        fill("Der Park ist hinter ___ Rathaus.", "dem"),
        fill("Das Hotel liegt ___ Zentrum. (in dem)", "im"),
        fill("Wir treffen uns ___ Bahnhof. (an dem)", "am"),
        tr("The bank is next to the post office.", "Die Bank ist neben der Post."),
    ),
    lesson(
        "Den Weg beschreiben",
        grammar("Den Weg beschreiben"),
        mc("geradeaus means:", "straight on", "left", "turn around"),
        mc("Biegen Sie rechts ab. means:", "Turn right.", "Turn left.", "Go straight on."),
        fill("Biegen Sie an der Ampel links ___.", "ab"),
        fill("Fahren Sie ___ bis zur Brücke. (straight on)", "geradeaus"),
        order("Biegen Sie an der Kreuzung rechts ab."),
        order("Gehen Sie zuerst geradeaus."),
        tr("Turn left. (formal)", "Biegen Sie links ab."),
    ),
    lesson(
        "Entschuldigung, können Sie mir helfen?",
        bank(
            "Entschuldigung, können Sie mir ___? Ich suche das Hotel Maritim. Ja, ___. "
            "Gehen Sie hier geradeaus und dann an der Ampel ___. Das Hotel ist ___ dem Dom.",
            ["helfen", "gern", "rechts", "neben"],
            "fremd",
            "unter",
        ),
        mc(
            "Someone asks you the way. You don't know:",
            "Tut mir leid, ich bin nicht von hier.",
            "Biegen Sie links ab.",
            "Ach so, danke.",
        ),
        mc("You understand now. You say:", "Ach so!", "Schade!", "Einen Moment!"),
        mc("The museum is closed today. You say:", "Schade!", "Ach so!", "Geradeaus!"),
        conj("helfen", "du", "hilfst"),
        conj("helfen", "er", "hilft"),
        conj("kennen", "du", "kennst"),
        tr("Do you know the Hotel Maritim? (formal)", "Kennen Sie das Hotel Maritim?"),
    ),
    lesson(
        "Lektion 13: Test",
        mc("Die Bank ist zwischen ___ Post und ___ Hotel.", "der … dem", "dem … der", "die … das"),
        fill("Das Auto steht ___ Haus. (in front of the)", "vor dem"),
        fill("Ich warte ___ Bahnhof. (an dem)", "am"),
        mc("Turn around: …", "wenden", "abbiegen", "weiterfahren"),
        order("Ist die Post in der Nähe?", "Build the question."),
        tr("The hotel is behind the cathedral.", "Das Hotel ist hinter dem Dom."),
        mc("Das stimmt. means:", "That's right.", "That's a pity.", "That's far."),
    ),
]

LEKTION_13 = unit(
    13,
    "Wir suchen das Hotel Maritim.",
    "Wegbeschreibung und Dativ",
    L13_WORDS,
    L13_RULES,
    sections(L13_LESSONS, vocab_lessons(L13_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 14: Wie findest du Ottos Haus?
# ============================================================================

L14_WORDS = [
    ("the house", "das Haus", "noun", "Pl. die Häuser"),
    ("the flat / apartment", "die Wohnung", "noun", "Pl. die Wohnungen"),
    ("the living room", "das Wohnzimmer", "noun", "Pl. die Wohnzimmer"),
    ("the bedroom", "das Schlafzimmer", "noun", "Pl. die Schlafzimmer"),
    ("the children's room", "das Kinderzimmer", "noun", "Pl. die Kinderzimmer"),
    ("the study (room)", "das Arbeitszimmer", "noun", "Pl. die Arbeitszimmer"),
    ("the kitchen", "die Küche", "noun", "Pl. die Küchen"),
    ("the bathroom", "das Bad", "noun", "Pl. die Bäder"),
    ("the toilet", "die Toilette", "noun", "Pl. die Toiletten"),
    ("the hallway", "der Flur", "noun", "Pl. die Flure"),
    ("the balcony", "der Balkon", "noun", "Pl. die Balkone"),
    ("the garage", "die Garage", "noun", "Pl. die Garagen"),
    ("the garden", "der Garten", "noun", "Pl. die Gärten"),
    ("the window", "das Fenster", "noun", "Pl. die Fenster"),
    ("the ground floor", "das Erdgeschoss", "noun"),
    ("the floor (storey)", "der Stock", "noun", "im ersten Stock"),
    ("the basement / cellar", "der Keller", "noun", "Pl. die Keller"),
    ("the stairs", "die Treppe", "noun", "Pl. die Treppen"),
    ("the lift", "der Aufzug", "noun", "Pl. die Aufzüge"),
    ("the rent", "die Miete", "noun", "Pl. die Mieten"),
    ("the additional costs (utilities)", "die Nebenkosten", "noun", "plural only"),
    ("the landlord", "der Vermieter", "noun", "f. die Vermieterin"),
    ("the neighbour", "der Nachbar", "noun", "f. die Nachbarin"),
    ("the square metre", "der Quadratmeter", "noun", "Pl. die Quadratmeter (m²)"),
    ("the advert", "die Anzeige", "noun", "Pl. die Anzeigen"),
    ("the tree", "der Baum", "noun", "Pl. die Bäume"),
    ("the flower", "die Blume", "noun", "Pl. die Blumen"),
    ("the light", "das Licht", "noun"),
    ("the rubbish", "der Müll", "noun"),
    ("the cooker / stove", "der Herd", "noun", "Pl. die Herde"),
    ("the mountain", "der Berg", "noun", "Pl. die Berge"),
    ("the river", "der Fluss", "noun", "Pl. die Flüsse"),
    ("the sea", "das Meer", "noun", "Pl. die Meere"),
    ("the forest", "der Wald", "noun", "Pl. die Wälder"),
    ("the tent", "das Zelt", "noun", "Pl. die Zelte"),
    ("to rent out", "vermieten", "verb"),
    ("to pay", "bezahlen", "verb"),
    ("to look (appearance)", "aussehen", "verb", "Das Haus sieht schön aus."),
    ("to stand", "stehen", "verb"),
    ("cosy", "gemütlich", "adjective"),
    ("empty", "leer", "adjective"),
    ("furnished", "möbliert", "adjective"),
    ("free / available", "frei", "adjective"),
    ("immediately", "sofort", "adverb"),
    ("at the back", "hinten", "adverb"),
    ("at the front", "vorn", "adverb"),
    ("up / upstairs", "oben", "adverb"),
    ("down / downstairs", "unten", "adverb"),
    ("in the country (rural)", "auf dem Land", "phrase"),
]

L14_RULES = [
    rule(
        "sein und ihr",
        "pronouns",
        """
- **sein** = his (or its): the owner is masculine or neuter.
- **ihr** = her, or their: the owner is feminine or plural.

Like *mein*, they take an ending that matches the **thing owned**:

| owner | der Balkon | das Haus | die Garage | die Fenster (pl.) |
|---|---|---|---|---|
| Otto (he) | sein Balkon | sein Haus | sein**e** Garage | sein**e** Fenster |
| Eva (she) | ihr Balkon | ihr Haus | ihr**e** Garage | ihr**e** Fenster |
| Ottos Kinder (they) | ihr Balkon | ihr Haus | ihr**e** Garage | ihr**e** Fenster |
""",
        [
            "Das ist Otto. Sein Haus ist groß.",
            "Eva wohnt hier. Ihre Wohnung ist hell.",
            "Die Kinder spielen in ihrem Zimmer.",
        ],
    ),
    rule(
        "Possessivartikel im Akkusativ",
        "cases",
        """
As the **object** (accusative), only the **masculine** form changes: it adds **-en**,
just like *einen*:

| | masculine | neuter | feminine | plural |
|---|---|---|---|---|
| nominative | mein Garten | mein Bad | meine Küche | meine Fenster |
| accusative | mein**en** Garten | mein Bad | meine Küche | meine Fenster |

Same for *dein, sein, ihr*: *Ich mag **seinen** Balkon. Kennst du **ihren** Nachbarn?*
""",
        ["Ich finde deinen Garten schön.", "Er sucht seinen Schlüssel.", "Sie zeigt ihre Wohnung."],
    ),
    rule(
        "Ottos Haus",
        "other",
        """
With **names**, show who owns something with **-s** (no apostrophe):

- *das Haus von Otto* = **Ottos** Haus
- *der Garten von Vanilla* = **Vanillas** Garten

If the name already ends in an s-sound, add only an **apostrophe**: *Hans' Wohnung, Max' Auto*.
""",
        ["Wie findest du Ottos Haus?", "Annas Balkon ist sehr groß.", "Das ist Pauls Zimmer."],
    ),
]

L14_LESSONS = [
    lesson(
        "Die Wohnung",
        review("die Wohnung"),
        review("das Wohnzimmer"),
        match(
            [
                ("die Küche", "you cook"),
                ("das Schlafzimmer", "you sleep"),
                ("das Bad", "you shower"),
                ("das Wohnzimmer", "you watch TV"),
                ("das Arbeitszimmer", "you work at a desk"),
            ],
            "Which room?",
        ),
        mc("You park your car in the …", "Garage", "Küche", "Toilette"),
        mc("Flowers and trees grow in the …", "Garten", "Keller", "Flur"),
        fill("Die Wohnung ist im ersten ___. (floor)", "Stock"),
        tr("The flat has three rooms.", "Die Wohnung hat drei Zimmer."),
    ),
    lesson(
        "sein und ihr",
        grammar("sein und ihr"),
        mc("Das ist Otto. Das ist ___ Haus.", "sein", "ihr", "seine"),
        mc("Das ist Eva. Das ist ___ Garage.", "ihre", "seine", "ihr"),
        mc("Das ist Max. Das ist ___ Küche.", "seine", "sein", "ihre"),
        mc("Das sind Tom und Lea. Das ist ___ Garten.", "ihr", "sein", "ihre"),
        fill("Frau Weber hat einen Hund. ___ Hund heißt Bello. (her)", "Ihr"),
        fill("Herr Roth hat eine Wohnung. ___ Wohnung ist klein. (his)", "Seine"),
        fill("Das Kind spielt. ___ Zimmer ist bunt. (its)", "Sein"),
        tr("This is her balcony.", "Das ist ihr Balkon."),
    ),
    lesson(
        "meinen, seinen, ihren",
        grammar("Possessivartikel im Akkusativ"),
        mc("Ich mag ___ Garten. (his)", "seinen", "sein", "seine"),
        mc("Kennst du ___ Nachbarn? (her)", "ihren", "ihr", "ihre"),
        mc("Er sucht ___ Schlüssel. (his)", "seinen", "sein", "seine"),
        fill("Ich finde ___ Balkon toll. (your, informal)", "deinen"),
        fill("Sie bezahlt ___ Miete pünktlich. (her)", "ihre"),
        fill("Sie zeigt ___ Bad. (her)", "ihr"),
        order("Ich finde deinen Garten sehr schön."),
        tr("He is looking for his key.", "Er sucht seinen Schlüssel."),
    ),
    lesson(
        "Ottos Haus",
        grammar("Ottos Haus"),
        mc("das Haus von Otto =", "Ottos Haus", "Otto's Haus", "Haus Ottos"),
        mc("der Garten von Anna =", "Annas Garten", "Anna's Garten", "Garten von Annas"),
        fill("das Zimmer von Paul = ___ Zimmer", "Pauls"),
        fill("die Wohnung von Lisa = ___ Wohnung", "Lisas"),
        order("Wie findest du Ottos Haus?", "Build the question."),
        tr("Anna's flat is cosy.", "Annas Wohnung ist gemütlich."),
    ),
    lesson(
        "Eine Anzeige",
        review("die Miete"),
        mc(
            "Anzeige: 2-Zimmer-Wohnung, 60 m², möbliert, 650 € + 150 € Nebenkosten, sofort frei. How big is it?",
            "60 square metres",
            "650 square metres",
            "2 square metres",
        ),
        mc(
            "Anzeige: 2-Zimmer-Wohnung, 60 m², möbliert, 650 € + 150 € Nebenkosten, sofort frei. Is there furniture?",
            "Yes, it is furnished.",
            "No, it is empty.",
            "The advert doesn't say.",
        ),
        mc(
            "Anzeige: … 650 € + 150 € Nebenkosten … What do you pay each month in total?",
            "800 €",
            "650 €",
            "150 €",
        ),
        mc("sofort frei means:", "available immediately", "free of charge", "very small"),
        fill("Die Wohnung hat keine Möbel. Sie ist ___. (empty)", "leer"),
        fill("Wir ___ die Miete am Monatsanfang. (bezahlen)", "bezahlen"),
    ),
    lesson(
        "Meine neue Wohnung",
        bank(
            "Hallo Jan, ich bin umgezogen! Meine Wohnung ist 55 m² ___ und kostet 700 Euro. "
            "Sie ist im ___ Stock. Die Küche ist sehr ___. Leider hat das Bad kein ___.",
            ["groß", "dritten", "gemütlich", "Fenster"],
            "leer",
            "Garten",
        ),
        mc(
            "Das Haus sieht schön aus. means:",
            "The house looks nice.",
            "The house is outside.",
            "The house is for sale.",
        ),
        order("Oben ist das Schlafzimmer und unten die Küche."),
        order("Hinten ist ein kleiner Garten."),
        tr("I live in the country.", "Ich wohne auf dem Land."),
    ),
    lesson(
        "Lektion 14: Test",
        mc("Das ist Lea. ___ Fahrrad ist neu.", "Ihr", "Sein", "Ihre"),
        mc("Ich mag ___ Balkon. (your, informal)", "deinen", "dein", "deine"),
        mc("das Auto von Max =", "Max' Auto", "Maxs Auto", "Max's Auto"),
        mc(
            "die Nebenkosten are:",
            "additional costs (utilities)",
            "the next costs",
            "the neighbours",
        ),
        order("Ihre Wohnung hat einen Balkon."),
        tr("His kitchen is small.", "Seine Küche ist klein."),
        mc("The opposite of oben:", "unten", "hinten", "vorn"),
    ),
]

LEKTION_14 = unit(
    14,
    "Wie findest du Ottos Haus?",
    "Wohnen, sein und ihr",
    L14_WORDS,
    L14_RULES,
    sections(L14_LESSONS, vocab_lessons(L14_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 15: In Giesing wohnt das Leben!
# ============================================================================

L15_WORDS = [
    ("the neighbourhood", "das Stadtviertel", "noun", "Pl. die Stadtviertel"),
    ("the district", "der Stadtteil", "noun", "Pl. die Stadtteile"),
    ("the old town", "die Altstadt", "noun"),
    ("the library", "die Bibliothek", "noun", "Pl. die Bibliotheken"),
    ("the shop / business", "das Geschäft", "noun", "Pl. die Geschäfte"),
    ("the (small) shop", "der Laden", "noun", "Pl. die Läden"),
    ("the harbour", "der Hafen", "noun", "Pl. die Häfen"),
    ("the youth hostel", "die Jugendherberge", "noun", "Pl. die Jugendherbergen"),
    ("the kindergarten", "der Kindergarten", "noun", "Pl. die Kindergärten"),
    ("the church", "die Kirche", "noun", "Pl. die Kirchen"),
    ("the market", "der Markt", "noun", "Pl. die Märkte"),
    ("the park", "der Park", "noun", "Pl. die Parks"),
    ("the town hall", "das Rathaus", "noun", "Pl. die Rathäuser"),
    ("the castle / palace", "das Schloss", "noun", "Pl. die Schlösser"),
    ("the playground", "der Spielplatz", "noun", "Pl. die Spielplätze"),
    ("the tower", "der Turm", "noun", "Pl. die Türme"),
    ("the workshop", "die Werkstatt", "noun", "Pl. die Werkstätten"),
    ("the travel agency", "das Reisebüro", "noun", "Pl. die Reisebüros"),
    ("the foreigner", "der Ausländer", "noun", "f. die Ausländerin"),
    ("the view", "der Blick", "noun"),
    ("the human being / person", "der Mensch", "noun", "Pl. die Menschen"),
    ("the recipe / prescription", "das Rezept", "noun", "Pl. die Rezepte"),
    ("the weather", "das Wetter", "noun"),
    ("the home (where you belong)", "die Heimat", "noun"),
    ("the landscape", "die Landschaft", "noun", "Pl. die Landschaften"),
    ("to thank", "danken", "verb", "+ Dativ: Ich danke dir."),
    ("to be missing", "fehlen", "verb", "+ Dativ: Mir fehlt ein Kino."),
    ("to belong to", "gehören", "verb", "+ Dativ: Das gehört mir."),
    ("to congratulate", "gratulieren", "verb", "+ Dativ"),
    ("important", "wichtig", "adjective"),
    ("all / everyone", "alle", "other"),
    ("everywhere", "überall", "adverb"),
    ("actually", "eigentlich", "adverb"),
    ("other", "andere", "adjective"),
    ("high / tall", "hoch", "adjective"),
    ("just around the corner", "um die Ecke", "phrase"),
    ("for example", "zum Beispiel", "phrase"),
    ("me (dative)", "mir", "other"),
    ("you (dative, informal)", "dir", "other"),
    ("him (dative)", "ihm", "other"),
    ("us (dative)", "uns", "other"),
    ("you all (dative)", "euch", "other"),
]

L15_RULES = [
    rule(
        "Personalpronomen im Dativ",
        "pronouns",
        """
| nominative | ich | du | er | es | sie | wir | ihr | sie / Sie |
|---|---|---|---|---|---|---|---|---|
| dative | **mir** | **dir** | **ihm** | **ihm** | **ihr** | **uns** | **euch** | **ihnen / Ihnen** |

*Das Viertel gefällt **mir**. Ich helfe **dir**. Wir danken **Ihnen**.*
""",
        ["Kannst du mir helfen?", "Das Buch gehört ihm.", "Wie geht es euch?"],
    ),
    rule(
        "Verben mit Dativ",
        "verbs",
        """
These verbs take a **dative** person:

**gefallen, gehören, helfen, danken, schmecken, fehlen, gratulieren**

- *Giesing **gefällt mir**.* (I like Giesing.)
- *Die Tasche **gehört ihr**.* (The bag belongs to her.)
- *Ich **helfe dir**.* / *Wir **danken euch**.*
- *Ein Kino **fehlt uns**.* (We're missing a cinema.)

With *gefallen, gehören, schmecken, fehlen*, the **thing** is the subject, so the verb
agrees with it: *Das Café gefällt mir. Die Cafés gefall**en** mir.*
""",
        [
            "Der Kuchen schmeckt uns.",
            "Die Schlüssel gehören mir.",
            "Ich gratuliere dir zum Geburtstag!",
        ],
    ),
]

L15_LESSONS = [
    lesson(
        "Mein Stadtviertel",
        review("das Stadtviertel"),
        review("die Bibliothek"),
        match(
            [
                ("die Bibliothek", "books"),
                ("der Spielplatz", "children play"),
                ("das Rathaus", "the mayor works"),
                ("die Jugendherberge", "cheap beds for young travellers"),
                ("der Markt", "fresh fruit and vegetables"),
            ]
        ),
        mc("Ships arrive at the …", "Hafen", "Turm", "Park"),
        mc("A king lived in a …", "Schloss", "Laden", "Kindergarten"),
        fill("Der Supermarkt ist gleich um die ___. (corner)", "Ecke"),
    ),
    lesson(
        "mir, dir, ihm",
        grammar("Personalpronomen im Dativ"),
        match(
            [
                ("ich", "mir"),
                ("du", "dir"),
                ("er", "ihm"),
                ("sie (she)", "ihr"),
                ("wir", "uns"),
                ("ihr (you all)", "euch"),
            ],
            "Match nominative and dative.",
        ),
        mc("Kannst du ___ helfen? (me)", "mir", "mich", "ich"),
        mc("Ich danke ___. (you, informal)", "dir", "dich", "du"),
        fill("Das Fahrrad gehört ___. (him)", "ihm"),
        fill("Wie geht es ___? (you all)", "euch"),
        fill("Wir helfen ___ gern. (her)", "ihr"),
        tr("Can you help us? (informal)", "Kannst du uns helfen?"),
    ),
    lesson(
        "gefallen, gehören, helfen",
        grammar("Verben mit Dativ"),
        mc("Das Viertel gefällt ___.", "mir", "mich", "ich"),
        mc("Die Cafés ___ mir.", "gefallen", "gefällt"),
        mc("Der Schlüssel ___ mir.", "gehört", "gehören"),
        mc("Die Schlüssel ___ mir.", "gehören", "gehört"),
        conj("helfen", "ich", "helfe"),
        conj("gefallen", "es", "gefällt"),
        fill("Der Kuchen ___ uns gut. (schmecken)", "schmeckt"),
        fill("Was ___ dir in deinem Viertel? (fehlen)", "fehlt"),
        tr("The park pleases me. (I like the park.)", "Der Park gefällt mir."),
    ),
    lesson(
        "Was gibt es in Giesing?",
        mc("In Giesing ___ es viele Kneipen.", "gibt", "gehört", "gefällt"),
        fill("Es gibt leider ___ Kino. (no)", "kein"),
        fill("Es gibt einen ___ und eine Kirche. (market)", "Markt"),
        bank(
            "In meinem Viertel gibt es ___ Park und viele ___. Mir ___ die Ruhe. "
            "Leider ___ eine Bibliothek.",
            ["einen", "Geschäfte", "gefällt", "fehlt"],
            "gehört",
            "ein",
        ),
        order("Mir gefällt die Altstadt besonders."),
        tr(
            "There is a library around the corner.",
            "Es gibt eine Bibliothek um die Ecke.|Um die Ecke gibt es eine Bibliothek.",
        ),
    ),
    lesson(
        "Ein Blog über mein Viertel",
        mc(
            "Blog: Ich wohne seit drei Jahren in Giesing. Hier gibt es viele kleine Läden und "
            "nette Menschen. Nur ein Schwimmbad fehlt. What is missing?",
            "a swimming pool",
            "small shops",
            "nice people",
        ),
        mc(
            "Blog: Ich wohne seit drei Jahren in Giesing. How long has the writer lived there?",
            "three years",
            "three months",
            "since yesterday",
        ),
        mc("eigentlich means:", "actually", "everywhere", "important"),
        fill("Das Wetter ist ___ gut. Hier scheint oft die Sonne. (actually)", "eigentlich"),
        order("Hier gibt es überall nette Menschen."),
        tr("The view is beautiful.", "Der Blick ist schön."),
    ),
    lesson(
        "Lektion 15: Test",
        mc("Gefällt ___ das Viertel? (you, informal)", "dir", "dich", "du"),
        fill("Das Handy gehört ___. (us)", "uns"),
        mc("Die Blumen ___ mir.", "gefallen", "gefällt"),
        conj("helfen", "du", "hilfst"),
        tr("I thank you. (informal)", "Ich danke dir."),
        order("Was fehlt dir in deinem Viertel?", "Build the question."),
        mc("das Rathaus is the …", "town hall", "guest house", "library"),
    ),
    lesson(
        "Modul 5: Wiederholung",
        mc("Das Café ist neben ___ Post.", "der", "dem", "die"),
        fill("Das Hotel liegt ___ Zentrum. (in dem)", "im"),
        mc("Biegen Sie an der Ampel links ___.", "ab", "an", "auf"),
        mc("Das ist Ina. ___ Balkon ist groß.", "Ihr", "Sein", "Ihre"),
        fill("Ich mag ___ Garten. (his)", "seinen"),
        fill("die Küche von Tom = ___ Küche", "Toms"),
        mc("Das Viertel gefällt ___. (her)", "ihr", "sie", "ihm"),
        bank(
            "Wo ist die Bank? Sie ist ___ dem Rathaus. Gehen Sie ___ und dann rechts. "
            "Danke! Das ___ mir sehr.",
            ["neben", "geradeaus", "hilft"],
            "gefällt",
            "links ab",
        ),
        tr("The bag belongs to me.", "Die Tasche gehört mir."),
        order("Seine Wohnung ist im Erdgeschoss."),
    ),
]

LEKTION_15 = unit(
    15,
    "In Giesing wohnt das Leben!",
    "Stadtviertel und Dativ",
    L15_WORDS,
    L15_RULES,
    sections(L15_LESSONS, vocab_lessons(L15_WORDS, "Wörter")),
)


UNITS = [LEKTION_13, LEKTION_14, LEKTION_15]
