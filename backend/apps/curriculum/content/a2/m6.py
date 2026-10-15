"""Modul 6 (A2.2): Lektion 16 (Darf ich fragen, ob ...?), 17 (Wir wollen nach
Rumänien.), 18 (Ich freue mich auf Sonne und Wärme.)."""

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
# Lektion 16: Darf ich fragen, ob ...?
# ============================================================================

L16_WORDS = [
    ("the reception (desk)", "die Rezeption", "noun", "Pl. die Rezeptionen"),
    ("the lobby", "die Empfangshalle", "noun", "Pl. die Empfangshallen"),
    ("the stay", "der Aufenthalt", "noun", "Pl. die Aufenthalte"),
    ("the single room", "das Einzelzimmer", "noun", "Pl. die Einzelzimmer"),
    ("the double room", "das Doppelzimmer", "noun", "Pl. die Doppelzimmer"),
    ("the non-smoking room", "das Nichtraucherzimmer", "noun", "Pl. die Nichtraucherzimmer"),
    ("the overnight stay", "die Übernachtung", "noun", "Pl. die Übernachtungen"),
    ("the half board", "die Halbpension", "noun"),
    ("the full board", "die Vollpension", "noun"),
    ("the breakfast room", "der Frühstücksraum", "noun", "Pl. die Frühstücksräume"),
    ("the fitness room", "der Fitnessraum", "noun", "Pl. die Fitnessräume"),
    ("the conference room", "der Konferenzraum", "noun", "Pl. die Konferenzräume"),
    ("the sauna", "die Sauna", "noun", "Pl. die Saunen"),
    ("the car park / parking space", "der Parkplatz", "noun", "Pl. die Parkplätze"),
    ("the glass door", "die Glastür", "noun", "Pl. die Glastüren"),
    ("the signature", "die Unterschrift", "noun", "Pl. die Unterschriften"),
    ("the complaint", "die Beschwerde", "noun", "Pl. die Beschwerden"),
    ("the arrival (at a hotel)", "die Anreise", "noun"),
    ("the departure (from a hotel)", "die Abreise", "noun"),
    ("the Wi-Fi", "das WLAN", "noun"),
    ("to check in", "einchecken", "verb", "hat eingecheckt"),
    ("to check out", "auschecken", "verb", "hat ausgecheckt"),
    ("fully booked", "ausgebucht", "adjective"),
    ("included", "inklusive", "adverb"),
    ("May I ask whether ...?", "Darf ich fragen, ob ...?", "phrase"),
    ("Could you tell me ...?", "Könnten Sie mir sagen, ...?", "phrase"),
    ("Do you still have a room free?", "Haben Sie noch ein Zimmer frei?", "phrase"),
]

L16_RULES = [
    rule(
        "Indirekte Fragen mit Fragewort",
        "sentence_structure",
        """
Polite questions often start with a phrase and put the real question inside.
The **question word stays**, and the **verb goes to the end**:

| Direct | Indirect |
|---|---|
| *Wann beginnt das Frühstück?* | *Können Sie mir sagen, **wann** das Frühstück **beginnt**?* |
| *Wo ist die Sauna?* | *Wissen Sie, **wo** die Sauna **ist**?* |
| *Wie lange bleiben Sie?* | *Darf ich fragen, **wie lange** Sie **bleiben**?* |

Yes/no questions use **ob** (Lektion 11): *Darf ich fragen, **ob** Sie noch ein
Zimmer frei **haben**?*

Start phrases: *Darf ich fragen, ... · Könnten Sie mir sagen, ... · Wissen Sie,
... · Ich möchte wissen, ...*
""",
        [
            "Könnten Sie mir sagen, wo der Frühstücksraum ist?",
            "Ich möchte wissen, wie viel das Doppelzimmer kostet.",
            "Darf ich fragen, ob das Frühstück inklusive ist?",
        ],
    ),
    rule(
        "Höflich bitten: Könnten Sie ...? Würden Sie ...?",
        "verbs",
        """
The Konjunktiv II forms make requests **polite**:

| very direct | polite |
|---|---|
| *Bringen Sie mir ein Handtuch!* | ***Könnten** Sie mir bitte ein Handtuch **bringen**?* |
| *Rufen Sie ein Taxi.* | ***Würden** Sie mir bitte ein Taxi **rufen**?* |
| *Ich will ein Zimmer.* | *Ich **hätte gern** ein Zimmer. / Ich **möchte** ein Zimmer.* |

Complaints stay polite too: *Entschuldigung, aber das Zimmer ist leider nicht
sauber. Ich möchte mich über den Lärm **beschweren**.*
""",
        [
            "Könnten Sie mir bitte helfen?",
            "Würden Sie mich um sieben Uhr wecken?",
            "Ich hätte gern ein Nichtraucherzimmer.",
        ],
    ),
]

L16_LESSONS = [
    lesson(
        "Im Hotel",
        review("die Rezeption"),
        review("die Übernachtung"),
        match(
            [
                ("das Einzelzimmer", "a room for one person"),
                ("das Doppelzimmer", "a room for two people"),
                ("die Halbpension", "breakfast and dinner"),
                ("die Vollpension", "all three meals"),
                ("ausgebucht", "no rooms free"),
            ],
            "What does it mean?",
        ),
        mc(
            "Am Ende des Aufenthalts bekommt man ...",
            "die Rechnung.",
            "die Sauna.",
            "die Anreise.",
        ),
        mc(
            "Wo bekommt man den Schlüssel?",
            "an der Rezeption",
            "im Fitnessraum",
            "in der Sauna",
        ),
        fill("Das Hotel ist leider ___. Wir haben kein Zimmer mehr. (fully booked)", "ausgebucht"),
        fill("Ist das Frühstück ___? (included)", "inklusive"),
        tr("Do you still have a room free?", "Haben Sie noch ein Zimmer frei?"),
    ),
    lesson(
        "Darf ich fragen, ...?",
        grammar("Indirekte Fragen mit Fragewort"),
        mc(
            "Wann beginnt das Frühstück? → Können Sie mir sagen, ...",
            "wann das Frühstück beginnt?",
            "wann beginnt das Frühstück?",
            "ob das Frühstück wann beginnt?",
        ),
        mc(
            "Haben Sie ein Zimmer frei? → Darf ich fragen, ...",
            "ob Sie ein Zimmer frei haben?",
            "wann Sie ein Zimmer frei haben?",
            "ob haben Sie ein Zimmer frei?",
        ),
        fill("Wissen Sie, ___ die Sauna ist? (where)", "wo"),
        fill("Ich möchte wissen, wie viel das Zimmer ___. (kosten)", "kostet"),
        fill("Darf ich fragen, wie lange Sie ___? (bleiben)", "bleiben"),
        fill("Könnten Sie mir sagen, ___ es WLAN gibt? (whether)", "ob"),
        order("Können Sie mir sagen, wo der Parkplatz ist?", "Build the question."),
        tr(
            "Could you tell me where the breakfast room is?",
            "Könnten Sie mir sagen, wo der Frühstücksraum ist?",
        ),
    ),
    lesson(
        "Könnten Sie ...?",
        grammar("Höflich bitten: Könnten Sie ...? Würden Sie ...?"),
        conj("würden", "Sie", "würden"),
        conj("könnten", "Sie", "könnten"),
        mc(
            "Which request is the most polite?",
            "Könnten Sie mir bitte ein Handtuch bringen?",
            "Bring mir ein Handtuch!",
            "Ich will ein Handtuch.",
        ),
        fill("___ Sie mich bitte um sieben Uhr wecken? (would)", "Würden"),
        fill("___ Sie mir bitte helfen? (could)", "Könnten"),
        fill("Ich ___ gern ein Nichtraucherzimmer. (would like: haben)", "hätte"),
        fill("Ich möchte mich über den Lärm ___. (complain)", "beschweren"),
        tr(
            "Could you call me a taxi, please?",
            "Könnten Sie mir bitte ein Taxi rufen?|Würden Sie mir bitte ein Taxi rufen?",
        ),
    ),
    lesson(
        "Der Weg im Hotel",
        mc(
            "Die Sauna ist gegenüber ___ Fitnessraum.",
            "vom",
            "den",
            "durch",
        ),
        mc(
            "Gehen Sie ___ die Glastür.",
            "durch",
            "gegenüber",
            "vorbei",
        ),
        fill("Gehen Sie am Frühstücksraum ___. (past)", "vorbei"),
        fill("Der Konferenzraum ist ___ ersten Stock. (in dem)", "im"),
        bank(
            "Entschuldigung, wo ist der Fitnessraum? Gehen Sie ___ die Empfangshalle und dann "
            "am Frühstücksraum ___. Der Fitnessraum ist ___ von der Sauna.",
            ["durch", "vorbei", "gegenüber"],
            "über",
            "entlang",
        ),
        tr("Go through the lobby.", "Gehen Sie durch die Empfangshalle."),
    ),
    lesson(
        "Eine Beschwerde",
        bank(
            "Guten Morgen, ich möchte mich ___. Das ___ funktioniert nicht und im Zimmer ist "
            "es sehr laut. Darf ich fragen, ___ Sie ein anderes Zimmer frei haben? Es tut mir "
            "___, wir sind heute ___. Aber morgen bekommen Sie ein ruhiges Zimmer.",
            ["beschweren", "WLAN", "ob", "leid", "ausgebucht"],
            "wann",
            "inklusive",
        ),
        mc(
            "What's the problem?",
            "The Wi-Fi doesn't work and it's noisy.",
            "The room is too expensive.",
            "Breakfast is not included.",
        ),
        mc(
            "When does the guest get a quiet room?",
            "Tomorrow.",
            "Today.",
            "Never.",
        ),
        fill("Wann müssen wir ___? (check out)", "auschecken"),
        fill("Hier brauche ich Ihre ___. (signature)", "Unterschrift"),
        order("Ich möchte mich über das Zimmer beschweren."),
    ),
    lesson(
        "Lektion 16: Test",
        fill("Können Sie mir sagen, wo die Rezeption ___?", "ist"),
        fill("Darf ich fragen, ___ das Zimmer frei ist?", "ob"),
        mc("Wissen Sie, ___ das Frühstück beginnt?", "wann", "ob wann"),
        fill("___ Sie mir bitte den Weg zeigen? (could)", "Könnten"),
        mc("Breakfast and dinner:", "Halbpension", "Vollpension"),
        order("Ich möchte wissen, wie viel das Doppelzimmer kostet."),
        tr("Is breakfast included?", "Ist das Frühstück inklusive?"),
    ),
]

LEKTION_16 = unit(
    16,
    "Darf ich fragen, ob ...?",
    "Im Hotel",
    L16_WORDS,
    L16_RULES,
    sections(L16_LESSONS, vocab_lessons(L16_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 17: Wir wollen nach Rumänien.
# ============================================================================

L17_WORDS = [
    ("the ferry", "die Fähre", "noun", "Pl. die Fähren"),
    ("the motorway", "die Autobahn", "noun", "Pl. die Autobahnen"),
    ("the petrol station", "die Tankstelle", "noun", "Pl. die Tankstellen"),
    ("the engine", "der Motor", "noun", "Pl. die Motoren"),
    ("the breakdown", "die Panne", "noun", "Pl. die Pannen"),
    ("the flat tyre", "die Reifenpanne", "noun", "Pl. die Reifenpannen"),
    ("the traffic jam", "der Stau", "noun", "Pl. die Staus"),
    ("the departure", "die Abfahrt", "noun", "Pl. die Abfahrten"),
    ("the arrival", "die Ankunft", "noun", "Pl. die Ankünfte"),
    ("the border", "die Grenze", "noun", "Pl. die Grenzen"),
    ("the island", "die Insel", "noun", "Pl. die Inseln"),
    ("the coast", "die Küste", "noun", "Pl. die Küsten"),
    ("the region", "die Region", "noun", "Pl. die Regionen"),
    ("the cemetery", "der Friedhof", "noun", "Pl. die Friedhöfe"),
    ("the route / distance", "die Strecke", "noun", "Pl. die Strecken"),
    ("the direction", "die Richtung", "noun", "Pl. die Richtungen"),
    ("the backpack", "der Rucksack", "noun", "Pl. die Rucksäcke"),
    ("the map", "die Landkarte", "noun", "Pl. die Landkarten"),
    ("the sat nav", "das Navi", "noun", "Pl. die Navis"),
    ("to go away (on a trip)", "verreisen", "verb", "ist verreist"),
    ("to fill up (fuel)", "tanken", "verb", "hat getankt"),
    ("to get lost", "sich verirren", "verb", "hat sich verirrt"),
    ("Romania", "Rumänien", "noun"),
    ("Take care!", "Pass auf dich auf!", "phrase"),
    ("How long does the journey take?", "Wie lange dauert die Fahrt?", "phrase"),
    ("We had a flat tyre.", "Wir hatten eine Reifenpanne.", "phrase"),
]

L17_RULES = [
    rule(
        "Woher? aus, von, vom",
        "cases",
        """
**Woher?** (where from) mirrors **Wohin?**, always with the **Dativ**:

| Wohin? | Wo? | Woher? |
|---|---|---|
| **nach** Rumänien | **in** Rumänien | **aus** Rumänien |
| **in die** Schweiz | **in der** Schweiz | **aus der** Schweiz |
| **ans** Meer | **am** Meer | **vom** Meer |
| **zum** Bahnhof | **am** Bahnhof | **vom** Bahnhof |
| **zu** Freunden | **bei** Freunden | **von** Freunden |

Rule of thumb: *in → aus*, *an / zu / bei → von*.
""",
        [
            "Wir kommen gerade aus dem Urlaub.",
            "Mein Freund ist vom Strand zurück.",
            "Ich komme von meiner Tante.",
        ],
    ),
    rule(
        "Reisewünsche: Ich wäre gern ...",
        "verbs",
        """
To dream about a trip, use the Konjunktiv II:

| | sein | haben | other verbs |
|---|---|---|---|
| ich | **wäre** | **hätte** | **würde** ... fahren |
| du | wärst | hättest | würdest ... fahren |
| er / sie | wäre | hätte | würde ... fahren |
| wir | wären | hätten | würden ... fahren |

- *Ich **wäre** jetzt gern am Meer.* (I'd love to be at the sea now.)
- *Ich **hätte** gern mehr Urlaub.*
- *Wir **würden** gern mit der Fähre **fahren**.*
- Plans: *Wir **wollen** nach Rumänien (fahren).* The verb of movement is often left out.
""",
        [
            "Wir wollen im Sommer nach Rumänien.",
            "Ich wäre jetzt gern auf einer Insel.",
            "Wir würden gern an der Küste entlang fahren.",
        ],
    ),
]

L17_LESSONS = [
    lesson(
        "Unterwegs",
        review("die Panne"),
        review("die Grenze"),
        match(
            [
                ("die Fähre", "the ferry"),
                ("die Tankstelle", "the petrol station"),
                ("der Stau", "the traffic jam"),
                ("die Insel", "the island"),
                ("die Küste", "the coast"),
            ]
        ),
        mc(
            "Das Auto fährt nicht mehr. Wir haben eine ...",
            "Panne.",
            "Ankunft.",
            "Region.",
        ),
        mc(
            "Auf der Autobahn stehen alle Autos. Es gibt einen ...",
            "Stau.",
            "Friedhof.",
            "Motor.",
        ),
        fill("Wir müssen noch ___. Das Benzin ist fast leer. (fill up)", "tanken"),
        fill("Ohne Navi haben wir uns ___. (verirren)", "verirrt"),
        tr("We had a flat tyre.", "Wir hatten eine Reifenpanne."),
    ),
    lesson(
        "Woher kommst du?",
        grammar("Woher? aus, von, vom"),
        mc("Wir kommen gerade ___ dem Urlaub.", "aus", "von", "nach"),
        mc("Er kommt ___ Strand zurück.", "vom", "aus dem", "zum"),
        mc("Ich komme ___ meiner Tante.", "von", "aus", "zu"),
        fill("Sie kommt ___ der Schweiz. (from)", "aus"),
        fill("Wann kommst du ___ Bahnhof zurück? (von dem)", "vom"),
        fill("Wir fahren ___ Rumänien. (to)", "nach"),
        fill("Wir waren zwei Wochen ___ Rumänien. (in)", "in"),
        order("Mein Bruder kommt morgen aus Rumänien zurück."),
        tr("We are coming back from the sea.", "Wir kommen vom Meer zurück."),
    ),
    lesson(
        "Ich wäre gern ...",
        grammar("Reisewünsche: Ich wäre gern ..."),
        conj("wären", "ich", "wäre"),
        conj("wären", "du", "wärst"),
        conj("wären", "wir", "wären"),
        fill("Ich ___ jetzt gern am Meer. (would be)", "wäre"),
        fill("Wir ___ gern mehr Urlaub. (would have)", "hätten"),
        fill("Ich ___ gern mit der Fähre fahren. (would)", "würde"),
        mc(
            "We want to go to Romania:",
            "Wir wollen nach Rumänien.",
            "Wir wollen in Rumänien.",
            "Wir wollen aus Rumänien.",
        ),
        order("Ich wäre jetzt gern auf einer Insel."),
        tr(
            "I would like to travel along the coast.",
            "Ich würde gern an der Küste entlang fahren.|Ich würde gern an der Küste entlangfahren.",
        ),
    ),
    lesson(
        "Eine Reise nach Rumänien",
        bank(
            "Im Sommer sind wir nach Rumänien ___. Die ___ war lang: 1500 Kilometer! Auf der "
            "Autobahn hatten wir viel ___. In Ungarn hatten wir eine ___, aber an der Tankstelle "
            "hat uns ein Mann geholfen. An der ___ haben wir unsere Pässe gezeigt. Zum Glück "
            "sind wir gut ___.",
            ["gefahren", "Strecke", "Stau", "Reifenpanne", "Grenze", "angekommen"],
            "verreist",
            "Fähre",
        ),
        mc(
            "Where did they have the flat tyre?",
            "In Hungary.",
            "In Romania.",
            "At the border.",
        ),
        mc(
            "Pass auf dich auf! means:",
            "Take care!",
            "Pass me the map!",
            "Wait for me!",
        ),
        fill("Wie lange ___ die Fahrt? (dauern)", "dauert"),
        fill("Wir fahren in ___ Süden. (direction)", "Richtung"),
        tr("When is the departure?", "Wann ist die Abfahrt?"),
    ),
    lesson(
        "Lektion 17: Test",
        mc("Wir kommen ___ Italien.", "aus", "von"),
        fill("Ich komme gerade ___ Arzt. (von dem)", "vom"),
        fill("Ich ___ jetzt gern im Urlaub. (would be)", "wäre"),
        mc("Wir ___ nach Rumänien.", "wollen", "wollt"),
        fill("Wir haben uns im Wald ___. (verirren)", "verirrt"),
        order("Wir müssen an der Tankstelle tanken."),
        tr("How long does the journey take?", "Wie lange dauert die Fahrt?"),
    ),
]

LEKTION_17 = unit(
    17,
    "Wir wollen nach Rumänien.",
    "Reisen und Verkehr",
    L17_WORDS,
    L17_RULES,
    sections(L17_LESSONS, vocab_lessons(L17_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 18: Ich freue mich auf Sonne und Wärme.
# ============================================================================

L18_WORDS = [
    ("the climate", "das Klima", "noun"),
    ("the sunshine", "der Sonnenschein", "noun"),
    ("the hail", "der Hagel", "noun"),
    ("the shower (rain)", "der Schauer", "noun", "Pl. die Schauer"),
    ("the precipitation", "der Niederschlag", "noun", "Pl. die Niederschläge"),
    ("the frost", "der Frost", "noun"),
    ("the raindrop", "der Regentropfen", "noun", "Pl. die Regentropfen"),
    ("the rainbow", "der Regenbogen", "noun", "Pl. die Regenbögen"),
    ("the temperature", "die Temperatur", "noun", "Pl. die Temperaturen"),
    ("the heat", "die Hitze", "noun"),
    ("the warmth", "die Wärme", "noun"),
    ("the cold", "die Kälte", "noun"),
    ("the drought / dryness", "die Trockenheit", "noun"),
    ("the humidity", "die Feuchtigkeit", "noun"),
    ("the high-pressure area", "das Hochdruckgebiet", "noun", "Pl. die Hochdruckgebiete"),
    ("the low-pressure area", "das Tiefdruckgebiet", "noun", "Pl. die Tiefdruckgebiete"),
    ("the season", "die Jahreszeit", "noun", "Pl. die Jahreszeiten"),
    ("the weather forecast", "die Wettervorhersage", "noun", "Pl. die Wettervorhersagen"),
    ("to hail", "hageln", "verb", "es hagelt"),
    ("to rise", "steigen", "verb", "ist gestiegen"),
    ("to fall / sink", "sinken", "verb", "ist gesunken"),
    ("to be annoyed", "sich ärgern", "verb", "über + Akk."),
    ("to dream", "träumen", "verb", "von + Dat."),
    ("to feel like", "Lust haben auf", "verb", "+ Akk."),
    ("dry", "trocken", "adjective"),
    ("damp / humid", "feucht", "adjective"),
    ("icy", "eisig", "adjective"),
    ("stormy", "stürmisch", "adjective"),
    ("rainy", "regnerisch", "adjective"),
    ("What are you looking forward to?", "Worauf freust du dich?", "phrase"),
    ("I'm looking forward to that.", "Darauf freue ich mich.", "phrase"),
]

L18_RULES = [
    rule(
        "Verben mit Präpositionen",
        "verbs",
        """
Many verbs come with a **fixed preposition**. Learn them together, with the case:

| + Akkusativ | + Dativ |
|---|---|
| sich freuen **auf** / **über** | zufrieden sein **mit** |
| sich ärgern **über** | sprechen **mit** |
| sich interessieren **für** | träumen **von** |
| Lust haben **auf** | erzählen **von** |
| sprechen **über** | Angst haben **vor** |
| warten **auf** · sich beschweren **über** | |

- *Ich ärgere mich **über den** Regen.*
- *Wir träumen **von einem** Urlaub am Meer.*
""",
        [
            "Ich freue mich auf Sonne und Wärme.",
            "Bist du mit dem Wetter zufrieden?",
            "Ich habe Lust auf einen Spaziergang.",
        ],
    ),
    rule(
        "worauf? darauf: wo- und da-",
        "pronouns",
        """
For **things and ideas**, combine the preposition with **wo-** (question) or
**da-** (answer). Add **r** before a vowel:

| preposition | question | answer |
|---|---|---|
| auf | **worauf**? | **darauf** |
| über | **worüber**? | **darüber** |
| für | **wofür**? | **dafür** |
| mit | **womit**? | **damit** |
| von | **wovon**? | **davon** |

- ***Worauf** freust du dich? Auf den Sommer. **Darauf** freue ich mich auch.*

For **people**, keep preposition + pronoun: ***Auf wen** wartest du? **Auf** meinen Bruder.
Ich warte **auf ihn**.*
""",
        [
            "Worüber ärgerst du dich? Über die Hitze.",
            "Wofür interessierst du dich? Für das Klima.",
            "Mit wem sprichst du? Mit meiner Kollegin.",
        ],
    ),
]

L18_LESSONS = [
    lesson(
        "Wetter und Klima",
        review("die Wettervorhersage"),
        review("die Jahreszeit"),
        match(
            [
                ("die Hitze", "the heat"),
                ("die Kälte", "the cold"),
                ("der Hagel", "the hail"),
                ("der Regenbogen", "the rainbow"),
                ("der Schauer", "the shower"),
            ]
        ),
        mc(
            "Nach dem Regen scheint die Sonne. Am Himmel sieht man einen ...",
            "Regenbogen.",
            "Niederschlag.",
            "Frost.",
        ),
        mc(
            "Ein Hochdruckgebiet bringt meistens ...",
            "Sonnenschein.",
            "Sturm.",
            "Hagel.",
        ),
        mc(
            "Es regnet seit Monaten nicht. Es gibt eine große ...",
            "Trockenheit.",
            "Feuchtigkeit.",
            "Wärme.",
        ),
        fill("Morgen ___ die Temperaturen auf 30 Grad. (steigen)", "steigen"),
        fill("In der Nacht ist die Temperatur unter null ___. (sinken)", "gesunken"),
        tr("The weather is rainy and cold.", "Das Wetter ist regnerisch und kalt."),
    ),
    lesson(
        "Ich freue mich auf ...",
        grammar("Verben mit Präpositionen"),
        fill("Ich freue mich ___ den Sommer.", "auf"),
        fill("Ich ärgere mich ___ den Regen.", "über"),
        fill("Sie interessiert sich ___ das Klima.", "für"),
        fill("Wir träumen ___ einem Urlaub am Meer.", "von"),
        fill("Bist du ___ dem Hotel zufrieden?", "mit"),
        fill("Ich habe Lust ___ ein Eis.", "auf"),
        mc("Hast du Angst ___ dem Gewitter?", "vor", "auf", "über"),
        mc("Wir warten ___ den Bus.", "auf", "für", "mit"),
        tr("I'm looking forward to sun and warmth.", "Ich freue mich auf Sonne und Wärme."),
    ),
    lesson(
        "Worauf? Darauf!",
        grammar("worauf? darauf: wo- und da-"),
        mc("___ freust du dich? Auf den Urlaub.", "Worauf", "Wofür", "Auf was für"),
        mc("___ ärgerst du dich? Über die Hitze.", "Worüber", "Worauf", "Womit"),
        mc("___ wartest du? Auf meine Schwester.", "Auf wen", "Worauf", "Wen"),
        fill("Freust du dich auf den Sommer? Ja, ___ freue ich mich. (on it)", "darauf"),
        fill("Interessierst du dich für Politik? Nein, ___ interessiere ich mich nicht.", "dafür"),
        fill("Bist du mit dem Zimmer zufrieden? Ja, ___ bin ich zufrieden.", "damit"),
        fill("___ träumst du? Von einem Haus am Meer. (wo + von)", "Wovon"),
        order("Worüber sprecht ihr gerade?", "Build the question."),
        tr("What are you looking forward to?", "Worauf freust du dich?"),
    ),
    lesson(
        "Die Wettervorhersage",
        bank(
            "Und nun das Wetter: Ein ___ aus dem Westen bringt morgen viel Regen. Im Norden "
            "gibt es ___ und Gewitter, in den Bergen sogar ___. Die Temperaturen ___ auf 10 "
            "Grad. Am Wochenende kommt ein Hoch: Dann gibt es wieder viel ___.",
            ["Tiefdruckgebiet", "Schauer", "Hagel", "sinken", "Sonnenschein"],
            "steigen",
            "Hitze",
        ),
        mc(
            "What will the weekend be like?",
            "Sunny.",
            "Stormy.",
            "Very cold.",
        ),
        mc(
            "Where could it hail?",
            "In the mountains.",
            "In the north.",
            "At the coast.",
        ),
        fill("Im Winter ist es oft ___ und neblig. (icy)", "eisig"),
        fill("Gestern hat es ___. Die Autos haben jetzt Löcher! (hageln)", "gehagelt"),
        tr("I'm annoyed about the cold.", "Ich ärgere mich über die Kälte."),
    ),
    lesson(
        "Lektion 18: Test",
        fill("Ich freue mich ___ die Ferien.", "auf"),
        fill("Er ärgert sich ___ den Stau.", "über"),
        mc("___ interessierst du dich? Für Sport.", "Wofür", "Worauf"),
        fill("Freust du dich auf das Fest? Ja, ___ freue ich mich.", "darauf"),
        mc("Mit ___ sprichst du? Mit Anna.", "wem", "wen"),
        order("Ich habe Lust auf einen Spaziergang."),
        tr("We are dreaming of a holiday.", "Wir träumen von einem Urlaub."),
    ),
    lesson(
        "Modul 6: Wiederholung",
        fill("Können Sie mir sagen, wann der Bus ___? (kommen)", "kommt"),
        fill("Darf ich fragen, ___ das Zimmer frei ist?", "ob"),
        fill("___ Sie mir bitte helfen? (could)", "Könnten"),
        mc("Wir kommen gerade ___ Meer.", "vom", "aus"),
        fill("Ich ___ jetzt gern auf einer Insel. (would be)", "wäre"),
        fill("Ich freue mich ___ den Urlaub.", "auf"),
        mc("___ ärgerst du dich?", "Worüber", "Über was für"),
        fill("Bist du mit dem Wetter zufrieden? Ja, ___ bin ich zufrieden.", "damit"),
        bank(
            "Ich möchte wissen, ___ das Wetter morgen wird. Ich freue mich nämlich ___ "
            "unseren Ausflug ans Meer. Hoffentlich gibt es keine ___!",
            ["wie", "auf", "Schauer"],
            "ob",
            "über",
        ),
        tr("Could you tell me where the station is?", "Könnten Sie mir sagen, wo der Bahnhof ist?"),
        order("Wir wollen im Sommer nach Rumänien fahren."),
    ),
]

LEKTION_18 = unit(
    18,
    "Ich freue mich auf Sonne und Wärme.",
    "Wetter und Klima",
    L18_WORDS,
    L18_RULES,
    sections(L18_LESSONS, vocab_lessons(L18_WORDS, "Wörter")),
)


UNITS = [LEKTION_16, LEKTION_17, LEKTION_18]
