"""A1 Hören sets, shaped like the Start Deutsch 1 listening paper: one set per
Modul. Teil 1: 6 short dialogues, a/b/c, heard twice. Teil 2: 4 announcements,
richtig/falsch, heard once. Teil 3: 5 phone messages, a/b/c, heard twice.

All scripts are original and use the words taught up to the Modul's last
Lektion. The audio is generated once with `manage.py make_hoeren_audio`.
Moduls 1-2 for now; more follow the same pattern.
"""

from ..dsl import clip, hoeren_mc, hoeren_rf, hoeren_teil

# The Moduls testers see in production; the rest stay local (DEBUG shows all).
LIVE = {1}

DIALOGUES = "Listen to the dialogue. Choose a, b or c. (You hear it twice.)"
ANNOUNCEMENTS = "Listen to the announcement. Richtig oder falsch? (You hear it once.)"
MESSAGES = "Listen to the message. Choose a, b or c. (You hear it twice.)"


def _set(dialogues, announcements, messages=None) -> list:
    """Teil 3 is left out when `messages` is None (Modul 1 for now)."""
    teile = [
        hoeren_teil(1, DIALOGUES, *[hoeren_mc(clip(*s), *q) for s, q in dialogues]),
        hoeren_teil(
            2,
            ANNOUNCEMENTS,
            *[hoeren_rf(clip(("Ansage", s), plays=1), *q) for s, q in announcements],
        ),
    ]
    if messages is not None:
        teile.append(
            hoeren_teil(3, MESSAGES, *[hoeren_mc(clip((who, s)), *q) for who, s, q in messages])
        )
    return teile


# Modul 1's Teil 3 (phone messages), set aside until its audio is recorded:
# pass it as `_set(..., M1_MESSAGES)` below to add it back.
M1_MESSAGES = [
    (
        "Frau",
        "Hallo Tom, hier ist Anna. Meine Freundin Sofia ist da, sie kommt aus "
        "Brasilien. Sie spricht ein bisschen Deutsch. Bis bald!",
        ("Woher kommt Sofia?", "Aus Brasilien.", "Aus Spanien.", "Aus Georgien."),
    ),
    (
        "Mann",
        "Guten Tag, Frau Klein. Hier ist Peter Novak von der Firma Hoffmann. "
        "Meine Telefonnummer ist null – sechs – neun, achtunddreißig, "
        "einundfünfzig. Danke und auf Wiederhören!",
        (
            "Wie ist die Nummer von Herrn Novak?",
            "069 38 51",
            "069 83 51",
            "069 38 15",
        ),
    ),
    (
        "Frau",
        "Hallo Papa, hier ist Lena. Oma und Opa sind heute bei uns. Kommst du auch? Tschüs!",
        ("Wer ist heute bei Lena?", "Oma und Opa", "Mama und Papa", "Ihr Bruder"),
    ),
    (
        "Mann",
        "Hallo Maria, hier ist Jonas. Mein Kollege Ben sucht eine Lehrerin für "
        "Spanisch. Du bist doch Spanischlehrerin! Bis bald.",
        ("Was sucht Ben?", "Eine Spanischlehrerin", "Einen Job", "Eine Kollegin"),
    ),
    (
        "Frau",
        "Guten Tag, hier ist die Sprachschule Lingua. Ihr Englischkurs ist in "
        "Zimmer fünfzehn, nicht in Zimmer fünf. Auf Wiederhören!",
        ("In welchem Zimmer ist der Kurs?", "Zimmer 15", "Zimmer 5", "Zimmer 50"),
    ),
]


HOEREN = {
    # Modul 1 (Lektionen 1-3): names, countries, jobs, numbers, family, languages.
    1: _set(
        [
            (
                [
                    ("Frau", "Guten Tag! Wie ist Ihr Name, bitte?"),
                    ("Mann", "Mein Name ist Schneider."),
                    ("Frau", "Wie schreibt man das?"),
                    ("Mann", "S – C – H – N – E – I – D – E – R."),
                ],
                ("Wie heißt der Mann?", "Schneider", "Schreiner", "Schröder"),
            ),
            (
                [
                    ("Mann", "Woher kommst du, Lucia?"),
                    ("Frau", "Ich komme aus Spanien, aus Madrid. Und du?"),
                    ("Mann", "Ich komme aus Italien."),
                ],
                ("Woher kommt Lucia?", "Aus Spanien.", "Aus Italien.", "Aus Brasilien."),
            ),
            (
                [
                    ("Frau", "Was sind Sie von Beruf?"),
                    ("Mann", "Ich bin Lehrer. Und meine Frau ist Ärztin."),
                ],
                ("Was ist der Mann von Beruf?", "Lehrer", "Arzt", "Kellner"),
            ),
            (
                [
                    ("Mann", "Wie alt ist deine Tochter?"),
                    ("Frau", "Sie ist zwölf. Und mein Sohn ist acht."),
                ],
                ("Wie alt ist die Tochter?", "12 Jahre", "8 Jahre", "20 Jahre"),
            ),
            (
                [
                    ("Frau", "Wie ist deine Telefonnummer?"),
                    (
                        "Mann",
                        "Null – eins – sieben – null, fünfundvierzig, dreiundsechzig, neunundzwanzig.",
                    ),
                ],
                ("Wie ist die Telefonnummer?", "0170 45 63 29", "0170 54 63 29", "0170 45 36 29"),
            ),
            (
                [
                    ("Mann", "Sprechen Sie Englisch?"),
                    (
                        "Frau",
                        "Ja. Und ich spreche auch ein bisschen Französisch. Aber kein Russisch.",
                    ),
                ],
                (
                    "Welche Sprachen spricht die Frau?",
                    "Englisch und Französisch",
                    "Englisch und Russisch",
                    "Französisch und Russisch",
                ),
            ),
        ],
        [
            (
                "Liebe Studenten, der Deutschkurs ist heute nicht in Zimmer zwölf. "
                "Er ist in Zimmer zwanzig.",
                ("Der Kurs ist heute in Zimmer 20.", True),
            ),
            (
                "Achtung, bitte! Frau Weber, bitte kommen Sie zur Information. "
                "Frau Weber, bitte zur Information.",
                ("Frau Weber soll zum Telefon kommen.", False),
            ),
            (
                "Guten Tag im Hotel Europa! Wir sprechen Deutsch, Englisch und Italienisch.",
                ("Im Hotel sprechen sie Spanisch.", False),
            ),
            (
                "Liebe Eltern, die Lehrerin von Klasse drei ist Frau Yilmaz. Ihre "
                "Telefonnummer ist null – drei – null, vierundfünfzig, zweiundachtzig.",
                ("Frau Yilmaz ist Lehrerin.", True),
            ),
        ],
    ),
    # Modul 2 (Lektionen 4-6): furniture and prices, things and colours, the office.
    2: _set(
        [
            (
                [
                    ("Frau", "Entschuldigung, was kostet der Tisch?"),
                    ("Mann", "Der Tisch kostet zweihundertneunzig Euro."),
                    ("Frau", "Oh, das ist zu teuer!"),
                ],
                ("Was kostet der Tisch?", "290 Euro", "219 Euro", "209 Euro"),
            ),
            (
                [
                    ("Mann", "Wie findest du die Lampe?"),
                    (
                        "Frau",
                        "Die rote? Die finde ich schön. Aber die schwarze Lampe ist hässlich.",
                    ),
                ],
                ("Welche Lampe findet die Frau schön?", "Die rote", "Die schwarze", "Die weiße"),
            ),
            (
                [
                    ("Frau", "Hast du einen Kugelschreiber für mich?"),
                    ("Mann", "Nein, aber hier ist ein Bleistift."),
                    ("Frau", "Danke!"),
                ],
                (
                    "Was bekommt die Frau?",
                    "Einen Bleistift",
                    "Einen Kugelschreiber",
                    "Ein Notizbuch",
                ),
            ),
            (
                [
                    ("Mann", "Ist das deine Tasche?"),
                    ("Frau", "Nein, meine Tasche ist braun. Die Tasche hier ist schwarz."),
                ],
                ("Welche Farbe hat die Tasche von der Frau?", "Braun", "Schwarz", "Grau"),
            ),
            (
                [
                    ("Frau", "Herr Lang, wo ist der Drucker?"),
                    ("Mann", "Der Drucker ist im Büro von Frau Schmidt. Das ist Büro elf."),
                ],
                ("Wo ist der Drucker?", "In Büro 11", "In Büro 7", "Im Büro von Herrn Lang"),
            ),
            (
                [
                    ("Mann", "Brauchen Sie einen Schreibtisch?"),
                    ("Frau", "Nein, einen Schreibtisch habe ich. Ich brauche einen Stuhl."),
                ],
                ("Was braucht die Frau?", "Einen Stuhl", "Einen Schreibtisch", "Einen Schrank"),
            ),
        ],
        [
            (
                "Liebe Kunden, heute im Sonderangebot: Sofas für nur "
                "dreihundertneunundneunzig Euro!",
                ("Die Sofas kosten heute 399 Euro.", True),
            ),
            (
                "Liebe Kunden, im Möbelhaus Krause kosten alle Stühle heute nur "
                "neunundzwanzig Euro.",
                ("Die Stühle kosten heute 39 Euro.", False),
            ),
            (
                "Liebe Kolleginnen und Kollegen, wir haben neue Computer. Haben Sie "
                "Fragen? Bitte fragen Sie Herrn Becker in Büro zwölf.",
                ("Herr Becker ist in Büro 12.", True),
            ),
            (
                "Achtung, bitte: Hier ist eine Tasche. Sie ist blau und klein. "
                "Bitte kommen Sie zur Information.",
                ("Die Tasche ist schwarz.", False),
            ),
        ],
        [
            (
                "Mann",
                "Hallo Sabine, hier ist Tim. Ich habe einen Tisch, aber ich brauche "
                "noch zwei Stühle. Hast du Stühle für mich? Bis bald!",
                ("Was braucht Tim?", "Zwei Stühle", "Einen Tisch", "Ein Bett"),
            ),
            (
                "Frau",
                "Guten Tag, Herr Weber, hier ist Möbel Krause. Ihr Sofa ist da. Es kostet "
                "vierhundertneunundneunzig Euro. Auf Wiederhören!",
                ("Was kostet das Sofa?", "499 Euro", "449 Euro", "994 Euro"),
            ),
            (
                "Mann",
                "Hallo, hier ist Paul aus dem Büro. Frau Schmidt hat eine Frage zur "
                "Rechnung. Bitte schreiben Sie ihr eine E-Mail. Danke!",
                (
                    "Was sollen Sie machen?",
                    "Frau Schmidt eine E-Mail schreiben",
                    "Frau Schmidt anrufen",
                    "Ins Büro kommen",
                ),
            ),
            (
                "Frau",
                "Hallo Jan, hier ist Mia. Ich habe deinen Schlüssel! Er ist bei mir im Büro. Tschüs!",
                ("Was hat Mia?", "Jans Schlüssel", "Jans Brille", "Jans Handy"),
            ),
            (
                "Mann",
                "Guten Tag, hier ist die Firma Meyer. Wir brauchen von Ihnen noch das "
                "Formular. Bitte schreiben Sie uns eine E-Mail. Auf Wiederhören!",
                ("Was braucht die Firma Meyer?", "Das Formular", "Eine Rechnung", "Einen Termin"),
            ),
        ],
    ),
    # Modul 3 (Lektionen 7-9): hobbies, times and appointments, food and drink.
    3: _set(
        [
            (
                [
                    ("Mann", "Was machst du gern in der Freizeit?"),
                    ("Frau", "Ich fotografiere gern. Und am Wochenende spiele ich Fußball."),
                ],
                (
                    "Was macht die Frau am Wochenende?",
                    "Sie spielt Fußball.",
                    "Sie fotografiert.",
                    "Sie schwimmt.",
                ),
            ),
            (
                [
                    ("Frau", "Entschuldigung, wie spät ist es?"),
                    ("Mann", "Es ist Viertel nach drei."),
                ],
                ("Wie spät ist es?", "3:15 Uhr", "3:45 Uhr", "2:45 Uhr"),
            ),
            (
                [
                    ("Mann", "Hast du am Freitag Zeit? Wir gehen ins Kino."),
                    ("Frau", "Am Freitag kann ich leider nicht. Aber am Samstag geht es."),
                ],
                ("Wann hat die Frau Zeit?", "Am Samstag", "Am Freitag", "Am Sonntag"),
            ),
            (
                [
                    ("Frau", "Was möchten Sie trinken?"),
                    ("Mann", "Einen Kaffee, bitte. Und ein Stück Kuchen."),
                ],
                ("Was möchte der Mann trinken?", "Kaffee", "Tee", "Saft"),
            ),
            (
                [
                    ("Mann", "Wann ist der Film?"),
                    ("Frau", "Um acht Uhr. Wir treffen uns um halb acht vor dem Kino."),
                ],
                ("Wann treffen sie sich?", "Um 7:30 Uhr", "Um 8:00 Uhr", "Um 8:30 Uhr"),
            ),
            (
                [
                    ("Frau", "Kannst du gut schwimmen?"),
                    ("Mann", "Nein, nicht so gut. Aber ich kann gut tanzen!"),
                ],
                ("Was kann der Mann gut?", "Tanzen", "Schwimmen", "Kochen"),
            ),
        ],
        [
            (
                "Liebe Kunden, heute im Angebot: Äpfel, ein Kilo für nur ein Euro neunundneunzig.",
                ("Ein Kilo Äpfel kostet heute 1,99 Euro.", True),
            ),
            (
                "Achtung, bitte: Heute kann man im Schwimmbad nur bis achtzehn Uhr schwimmen.",
                ("Man kann heute bis 20 Uhr schwimmen.", False),
            ),
            (
                "Das Konzert heute Abend ist nicht um acht Uhr. Es ist um neun Uhr.",
                ("Das Konzert ist um 21 Uhr.", True),
            ),
            (
                "Liebe Gäste, das Frühstück gibt es heute von sieben bis zehn Uhr im Restaurant.",
                ("Das Frühstück ist im Café.", False),
            ),
        ],
        [
            (
                "Frau",
                "Hallo Max, hier ist Julia. Ich habe zwei Karten für das Konzert am Samstag. "
                "Hast du Lust? Ruf mich bitte an!",
                ("Wann ist das Konzert?", "Am Samstag", "Am Sonntag", "Am Freitag"),
            ),
            (
                "Mann",
                "Hallo Eva, hier ist Ben. Ich koche heute Abend Suppe. Aber ich habe kein Brot. "
                "Hast du Brot für mich? Bis später!",
                ("Was braucht Ben?", "Brot", "Käse", "Milch"),
            ),
            (
                "Frau",
                "Guten Tag, hier ist das Restaurant Roma. Ihr Tisch für heute Abend ist um "
                "halb acht frei, nicht um sieben. Bis heute Abend!",
                ("Wann ist der Tisch frei?", "Um 19:30 Uhr", "Um 19:00 Uhr", "Um 20:30 Uhr"),
            ),
            (
                "Mann",
                "Hallo Anna, hier ist Paul. Das Fußballspiel morgen ist nicht um zehn, es ist "
                "um elf Uhr. Tschüs!",
                ("Wann ist das Fußballspiel?", "Um 11 Uhr", "Um 10 Uhr", "Um 12 Uhr"),
            ),
            (
                "Frau",
                "Hallo Lukas, hier ist Mama. Wir essen heute um sechs Uhr zu Abend. Es gibt "
                "Fisch mit Kartoffeln. Bis dann!",
                (
                    "Was gibt es zum Abendessen?",
                    "Fisch mit Kartoffeln",
                    "Fleisch mit Reis",
                    "Suppe mit Brot",
                ),
            ),
        ],
    ),
    # Modul 4 (Lektionen 10-12): transport, the Perfekt, months and celebrations.
    4: _set(
        [
            (
                [
                    ("Frau", "Entschuldigung, wann fährt der Zug nach Berlin ab?"),
                    ("Mann", "Um zehn Uhr zwanzig, von Gleis vier."),
                ],
                ("Von welchem Gleis fährt der Zug?", "Gleis 4", "Gleis 10", "Gleis 20"),
            ),
            (
                [
                    ("Mann", "Wie kommst du zur Arbeit?"),
                    ("Frau", "Mit dem Fahrrad. Aber im Winter nehme ich den Bus."),
                ],
                ("Wie fährt die Frau im Winter?", "Mit dem Bus", "Mit dem Fahrrad", "Mit dem Auto"),
            ),
            (
                [
                    ("Frau", "Was hast du am Wochenende gemacht?"),
                    (
                        "Mann",
                        "Ich habe meine Eltern besucht. Und am Sonntag habe ich lange geschlafen.",
                    ),
                ],
                (
                    "Was hat der Mann am Sonntag gemacht?",
                    "Er hat lange geschlafen.",
                    "Er hat seine Eltern besucht.",
                    "Er hat gearbeitet.",
                ),
            ),
            (
                [("Mann", "Wann hast du Geburtstag?"), ("Frau", "Im Mai. Am zwölften Mai.")],
                ("Wann hat die Frau Geburtstag?", "Am 12. Mai", "Am 2. Mai", "Am 12. März"),
            ),
            (
                [
                    ("Frau", "Wo muss ich umsteigen?"),
                    ("Mann", "Sie steigen am Bahnhof in die U-Bahn um."),
                ],
                ("Wo steigt die Frau um?", "Am Bahnhof", "Am Flughafen", "An der Haltestelle"),
            ),
            (
                [
                    ("Mann", "Bist du mit dem Auto gekommen?"),
                    ("Frau", "Nein, ich bin zu Fuß gegangen. Das ist ganz nah."),
                ],
                ("Wie ist die Frau gekommen?", "Zu Fuß", "Mit dem Auto", "Mit dem Taxi"),
            ),
        ],
        [
            (
                "Achtung am Gleis drei: Der Zug nach München kommt heute zehn Minuten später.",
                ("Der Zug nach München kommt zehn Minuten später.", True),
            ),
            (
                "Liebe Fahrgäste, heute fahren keine Straßenbahnen. Bitte nehmen Sie den Bus.",
                ("Heute fährt die Straßenbahn.", False),
            ),
            (
                "Das Sommerfest im Kindergarten ist am fünften Juli um fünfzehn Uhr.",
                ("Das Fest ist im Juni.", False),
            ),
            (
                "Unser Kollege Herr Roth hat heute Geburtstag! Wir feiern um zwölf Uhr im Büro.",
                ("Die Feier ist am Mittag.", True),
            ),
        ],
        [
            (
                "Mann",
                "Hallo Lisa, hier ist Tom. Ich bin gerade in Hamburg angekommen. Ich rufe dich "
                "heute Abend an. Tschüs!",
                ("Wo ist Tom?", "In Hamburg", "In Berlin", "Am Flughafen"),
            ),
            (
                "Frau",
                "Hallo, hier ist Sara. Holst du mich bitte am Bahnhof ab? Mein Zug kommt um "
                "sechzehn Uhr dreißig an. Danke!",
                ("Wann kommt Saras Zug an?", "Um 16:30 Uhr", "Um 16:13 Uhr", "Um 18:30 Uhr"),
            ),
            (
                "Mann",
                "Hallo Anna, hier ist Jan. Am Samstag feiere ich Geburtstag. Die Party fängt "
                "um acht Uhr an. Bring bitte Musik mit! Bis Samstag!",
                ("Was soll Anna mitbringen?", "Musik", "Getränke", "Einen Kuchen"),
            ),
            (
                "Frau",
                "Guten Tag, Herr Weber, hier ist Frau Klein. Ich habe Ihre Fahrkarte gekauft. "
                "Sie fahren am Montag um neun Uhr. Auf Wiederhören!",
                (
                    "Wann fährt Herr Weber?",
                    "Am Montag um 9 Uhr",
                    "Am Montag um 19 Uhr",
                    "Am Dienstag um 9 Uhr",
                ),
            ),
            (
                "Mann",
                "Hallo Mia, hier ist Papa. Hast du deine Hausaufgaben gemacht? Ich komme um "
                "sieben Uhr nach Hause. Tschüs!",
                ("Wann kommt Papa nach Hause?", "Um 7 Uhr", "Um 6 Uhr", "Um 8 Uhr"),
            ),
        ],
    ),
    # Modul 5 (Lektionen 13-15): directions, flats and houses, the city.
    5: _set(
        [
            (
                [
                    ("Frau", "Entschuldigung, wo ist die Post?"),
                    ("Mann", "Gehen Sie hier geradeaus und dann die zweite Straße links."),
                ],
                (
                    "Wie kommt die Frau zur Post?",
                    "Geradeaus und dann links",
                    "Geradeaus und dann rechts",
                    "Zurück und dann links",
                ),
            ),
            (
                [
                    ("Mann", "Wie ist deine neue Wohnung?"),
                    ("Frau", "Sie hat drei Zimmer, eine Küche und einen Balkon."),
                ],
                ("Wie viele Zimmer hat die Wohnung?", "Drei", "Zwei", "Vier"),
            ),
            (
                [
                    ("Frau", "Wo ist das Bad?"),
                    ("Mann", "Das Bad ist oben, neben dem Schlafzimmer."),
                ],
                (
                    "Wo ist das Bad?",
                    "Oben neben dem Schlafzimmer",
                    "Unten neben der Küche",
                    "Oben neben dem Kinderzimmer",
                ),
            ),
            (
                [("Mann", "Ist hier eine Bank in der Nähe?"), ("Frau", "Ja, hinter dem Rathaus.")],
                ("Wo ist die Bank?", "Hinter dem Rathaus", "Neben dem Rathaus", "Vor dem Rathaus"),
            ),
            (
                [
                    ("Frau", "Was kostet die Wohnung?"),
                    (
                        "Mann",
                        "Die Miete ist sechshundert Euro. Mit Nebenkosten siebenhundertzwanzig.",
                    ),
                ],
                ("Was kostet die Wohnung mit Nebenkosten?", "720 Euro", "600 Euro", "620 Euro"),
            ),
            (
                [("Mann", "Wo treffen wir uns?"), ("Frau", "Am Markt, vor der Kirche.")],
                ("Wo treffen sie sich?", "Vor der Kirche", "Vor dem Rathaus", "Im Park"),
            ),
        ],
        [
            (
                "Liebe Besucher, die Bibliothek ist heute im ersten Stock, nicht im Erdgeschoss.",
                ("Die Bibliothek ist heute im ersten Stock.", True),
            ),
            (
                "Achtung: Heute fährt der Aufzug nicht. Bitte nehmen Sie die Treppe.",
                ("Man soll heute den Aufzug nehmen.", False),
            ),
            (
                "Der Markt ist heute nicht vor dem Rathaus. Er ist im Park.",
                ("Der Markt ist heute im Park.", True),
            ),
            (
                "Liebe Nachbarn, am Samstag machen wir ein Fest im Garten. Es fängt um fünfzehn Uhr an.",
                ("Das Fest ist im Keller.", False),
            ),
        ],
        [
            (
                "Frau",
                "Hallo Tim, hier ist Nina. Ich habe eine Wohnung gefunden! Sie ist in der "
                "Altstadt, neben dem Park. Ruf mich an!",
                ("Wo ist Ninas Wohnung?", "In der Altstadt", "Am Hafen", "Im Zentrum"),
            ),
            (
                "Mann",
                "Guten Tag, hier ist Herr Lang, Ihr Vermieter. Die Miete für Oktober fehlt "
                "noch. Bitte bezahlen Sie bis Freitag. Auf Wiederhören!",
                (
                    "Was soll man bis Freitag machen?",
                    "Die Miete bezahlen",
                    "Den Vermieter anrufen",
                    "Die Wohnung sauber machen",
                ),
            ),
            (
                "Frau",
                "Hallo, hier ist Lisa. Ich finde das Café nicht! Ich bin an der Brücke. Wo bist du?",
                ("Wo ist Lisa?", "An der Brücke", "Im Café", "Am Bahnhof"),
            ),
            (
                "Mann",
                "Hallo Sara, hier ist Jonas. Das Hotel ist ganz in der Nähe vom Dom, in der "
                "Domstraße zwei. Bis später!",
                ("Wo ist das Hotel?", "In der Domstraße 2", "In der Domstraße 12", "Am Bahnhof"),
            ),
            (
                "Frau",
                "Hallo Paul, hier ist Oma. Danke für die Blumen! Sie sind sehr schön. Bis Sonntag!",
                ("Wofür dankt Oma?", "Für die Blumen", "Für den Kuchen", "Für das Buch"),
            ),
        ],
    ),
    # Modul 6 (Lektionen 16-18): hotel and appointments, plans, health.
    6: _set(
        [
            (
                [
                    ("Frau", "Guten Tag, die Heizung in Zimmer zwölf funktioniert nicht."),
                    ("Mann", "Oh, das tut mir leid. Der Techniker kommt sofort."),
                ],
                ("Was funktioniert nicht?", "Die Heizung", "Die Dusche", "Der Fernseher"),
            ),
            (
                [
                    ("Frau", "Guten Tag, ich brauche einen Termin. Geht es am Dienstag?"),
                    ("Mann", "Am Dienstag leider nicht. Aber am Mittwoch um neun Uhr."),
                ],
                (
                    "Wann hat die Frau einen Termin?",
                    "Am Mittwoch um 9 Uhr",
                    "Am Dienstag um 9 Uhr",
                    "Am Mittwoch um 10 Uhr",
                ),
            ),
            (
                [("Frau", "Was haben Sie denn?"), ("Mann", "Ich habe Kopfschmerzen und Fieber.")],
                (
                    "Was hat der Mann?",
                    "Kopfschmerzen und Fieber",
                    "Halsschmerzen und Fieber",
                    "Bauchschmerzen",
                ),
            ),
            (
                [
                    ("Mann", "Was willst du später werden?"),
                    ("Frau", "Ich will Ärztin werden. Mein Bruder will Politiker werden."),
                ],
                ("Was will die Frau werden?", "Ärztin", "Politikerin", "Lehrerin"),
            ),
            (
                [
                    ("Frau", "Wie oft soll ich die Tabletten nehmen?"),
                    ("Mann", "Dreimal am Tag, nach dem Essen."),
                ],
                (
                    "Wie oft soll die Frau die Tabletten nehmen?",
                    "Dreimal am Tag",
                    "Zweimal am Tag",
                    "Einmal am Tag",
                ),
            ),
            (
                [
                    ("Mann", "Wir müssen die Sitzung verschieben. Geht Donnerstag?"),
                    ("Frau", "Ja, Donnerstag passt gut."),
                ],
                ("Wann ist die Sitzung jetzt?", "Am Donnerstag", "Am Dienstag", "Am Freitag"),
            ),
        ],
        [
            (
                "Liebe Gäste, das Frühstück gibt es heute im Garten.",
                ("Das Frühstück ist heute im Garten.", True),
            ),
            (
                "Die Praxis Doktor Lehmann hat vom ersten bis vierzehnten August Urlaub.",
                ("Die Praxis hat im Juli Urlaub.", False),
            ),
            (
                "Der Deutschkurs ist heute nicht um achtzehn Uhr. Er ist um neunzehn Uhr.",
                ("Der Kurs ist heute um 18 Uhr.", False),
            ),
            (
                "In der Apotheke am Markt bekommen Sie heute bis zweiundzwanzig Uhr Medikamente.",
                ("Sie bekommen heute bis 22 Uhr Medikamente.", True),
            ),
        ],
        [
            (
                "Frau",
                "Guten Tag, hier ist die Praxis Doktor Wagner. Ihr Termin am Freitag um zehn "
                "Uhr geht leider nicht. Können Sie am Montag um elf Uhr kommen?",
                (
                    "Wann ist der neue Termin?",
                    "Am Montag um 11 Uhr",
                    "Am Freitag um 10 Uhr",
                    "Am Montag um 10 Uhr",
                ),
            ),
            (
                "Mann",
                "Hallo Anna, hier ist Ben. Ich bin krank und kann heute nicht zur Arbeit "
                "kommen. Sag bitte dem Chef Bescheid. Danke!",
                (
                    "Was soll Anna machen?",
                    "Dem Chef Bescheid sagen",
                    "Zum Arzt gehen",
                    "Ben Tabletten bringen",
                ),
            ),
            (
                "Frau",
                "Guten Tag, Herr Kraus, hier ist das Hotel Sonne. Ihr Zimmer ist ab vierzehn "
                "Uhr fertig. Auf Wiederhören!",
                ("Ab wann ist das Zimmer fertig?", "Ab 14 Uhr", "Ab 12 Uhr", "Ab 16 Uhr"),
            ),
            (
                "Mann",
                "Hallo Lisa, hier ist Tim. Ich will den Führerschein machen! Die Prüfung ist im Mai. Bis bald!",
                ("Wann ist Tims Prüfung?", "Im Mai", "Im März", "Im Juni"),
            ),
            (
                "Frau",
                "Hallo Papa, hier ist Mia. Ich habe Halsschmerzen. Bringst du mir bitte Tee "
                "und Tabletten aus der Apotheke mit? Danke!",
                (
                    "Was soll Papa mitbringen?",
                    "Tee und Tabletten",
                    "Saft und Tabletten",
                    "Tee und eine Salbe",
                ),
            ),
        ],
    ),
    # Modul 7 (Lektionen 19-21): looks and character, housework, rules.
    7: _set(
        [
            (
                [
                    ("Frau", "Wie sieht dein Bruder aus?"),
                    ("Mann", "Er ist groß und schlank und hat blonde Haare."),
                ],
                ("Welche Haare hat der Bruder?", "Blonde Haare", "Schwarze Haare", "Keine Haare"),
            ),
            (
                [
                    ("Mann", "Wer bringt heute den Müll raus?"),
                    ("Frau", "Du! Ich habe gestern gespült und den Boden gewischt."),
                ],
                (
                    "Was hat die Frau gestern gemacht?",
                    "Gespült und den Boden gewischt",
                    "Den Müll rausgebracht",
                    "Die Wäsche gebügelt",
                ),
            ),
            (
                [
                    ("Frau", "Darf man hier parken?"),
                    ("Mann", "Nein, hier ist Parken verboten. Aber dort hinten dürfen Sie parken."),
                ],
                ("Wo darf die Frau parken?", "Dort hinten", "Hier", "Vor dem Haus"),
            ),
            (
                [
                    ("Mann", "Wie war dein Lehrer früher?"),
                    ("Frau", "Er war sehr ruhig und freundlich."),
                ],
                ("Wie war der Lehrer?", "Ruhig und freundlich", "Laut und lustig", "Unfreundlich"),
            ),
            (
                [
                    ("Frau", "Räum bitte dein Zimmer auf!"),
                    ("Mann", "Jetzt? Ich mache gerade Hausaufgaben."),
                    ("Frau", "Okay, dann nach dem Essen."),
                ],
                ("Wann soll er sein Zimmer aufräumen?", "Nach dem Essen", "Jetzt", "Morgen"),
            ),
            (
                [
                    ("Mann", "Muss der Hund im Park an die Leine?"),
                    (
                        "Frau",
                        "Ja, im Park schon. Aber auf der Wiese dort hinten darf er frei laufen.",
                    ),
                ],
                ("Wo darf der Hund frei laufen?", "Auf der Wiese", "Im Park", "Auf der Straße"),
            ),
        ],
        [
            (
                "Achtung, bitte: Kinder unter zehn Jahren müssen mit den Eltern ins Schwimmbad kommen.",
                ("Kinder unter 10 Jahren dürfen allein ins Schwimmbad.", False),
            ),
            (
                "Liebe Mieter, bitte bringen Sie den Müll nur am Montag und am Donnerstag raus.",
                ("Man bringt den Müll am Montag raus.", True),
            ),
            (
                "Achtung: In diesem Zug darf man nicht rauchen. Und bitte sprechen Sie leise.",
                ("Im Zug darf man rauchen.", False),
            ),
            (
                "Liebe Fahrradfahrer, bitte schieben Sie im Park Ihr Fahrrad.",
                ("Im Park muss man das Fahrrad schieben.", True),
            ),
        ],
        [
            (
                "Mann",
                "Hallo Lena, hier ist Jan. Wir machen am Samstag die Wohnung sauber. Kannst du "
                "die Küche putzen? Ich mache das Bad. Bis dann!",
                ("Was soll Lena putzen?", "Die Küche", "Das Bad", "Den Flur"),
            ),
            (
                "Frau",
                "Hallo Herr Fischer, hier ist Ihre Nachbarin, Frau Roth. Ihr Hund ist bei mir "
                "im Garten! Er ist ganz ruhig. Bitte kommen Sie.",
                (
                    "Wo ist der Hund?",
                    "Im Garten von Frau Roth",
                    "Im Park",
                    "Bei Herrn Fischer zu Hause",
                ),
            ),
            (
                "Mann",
                "Hallo Mama, hier ist Paul. Ich habe meinen Schlüssel vergessen! Bist du um fünf Uhr zu Hause?",
                ("Was hat Paul vergessen?", "Seinen Schlüssel", "Sein Handy", "Seine Tasche"),
            ),
            (
                "Frau",
                "Hallo Anna, hier ist Sophie. Ich habe gestern deinen Bruder gesehen. Er hat "
                "jetzt einen Bart! Er sieht so komisch aus! Tschüs!",
                ("Was hat Annas Bruder jetzt?", "Einen Bart", "Lange Haare", "Eine Brille"),
            ),
            (
                "Mann",
                "Guten Tag, hier ist die Fahrschule Tempo. Bitte bringen Sie morgen Ihren Helm "
                "mit. Die Fahrstunde ist um acht Uhr.",
                ("Was muss man mitbringen?", "Den Helm", "Den Führerschein", "Das Fahrrad"),
            ),
        ],
    ),
    # Modul 8 (Lektionen 22-24): clothes, weather and holidays, celebrations.
    8: _set(
        [
            (
                [
                    ("Frau", "Wie findest du die Jacke?"),
                    ("Mann", "Die rote? Schön. Aber die blaue ist billiger."),
                ],
                ("Welche Jacke ist billiger?", "Die blaue", "Die rote", "Die schwarze"),
            ),
            (
                [
                    ("Mann", "Wie ist das Wetter in Hamburg?"),
                    ("Frau", "Es regnet und es ist kalt. Nur zehn Grad."),
                ],
                (
                    "Wie ist das Wetter in Hamburg?",
                    "Es regnet.",
                    "Die Sonne scheint.",
                    "Es schneit.",
                ),
            ),
            (
                [
                    ("Frau", "Was ziehst du zur Hochzeit an?"),
                    ("Mann", "Ein weißes Hemd und eine schwarze Hose."),
                ],
                (
                    "Was zieht der Mann an?",
                    "Ein Hemd und eine schwarze Hose",
                    "Einen Pullover und eine Hose",
                    "Ein T-Shirt",
                ),
            ),
            (
                [
                    ("Mann", "Wohin fährst du im Urlaub?"),
                    ("Frau", "Ich fahre an die Ostsee. Ich liebe den Strand!"),
                ],
                ("Wohin fährt die Frau?", "An die Ostsee", "In die Berge", "Nach Italien"),
            ),
            (
                [("Frau", "Wann ist die Party?"), ("Mann", "Am dritten Oktober, am Samstag.")],
                ("Wann ist die Party?", "Am 3. Oktober", "Am 13. Oktober", "Am 3. November"),
            ),
            (
                [
                    ("Mann", "Was würdest du im Urlaub am liebsten machen?"),
                    ("Frau", "Am liebsten würde ich jeden Tag schwimmen."),
                ],
                (
                    "Was würde die Frau am liebsten machen?",
                    "Jeden Tag schwimmen",
                    "Jeden Tag wandern",
                    "Lange schlafen",
                ),
            ),
        ],
        [
            (
                "Und jetzt das Wetter: Morgen scheint im Süden die Sonne, im Norden regnet es.",
                ("Im Norden regnet es morgen.", True),
            ),
            (
                "Liebe Kunden, heute sind alle Mäntel und Jacken zwanzig Prozent billiger!",
                ("Heute sind die Hosen billiger.", False),
            ),
            (
                "Achtung: Heute ist Sturm. Bitte gehen Sie nicht an den Strand.",
                ("Man soll heute nicht an den Strand gehen.", True),
            ),
            (
                "Frohe Weihnachten! Am vierundzwanzigsten Dezember können Sie bei uns nur bis vierzehn Uhr einkaufen.",
                ("Am 24. Dezember kann man bis 18 Uhr einkaufen.", False),
            ),
        ],
        [
            (
                "Frau",
                "Hallo Tina, hier ist Sophie. Viele Grüße aus Spanien! Hier sind es dreißig "
                "Grad und die Sonne scheint. Bis bald!",
                ("Wie warm ist es in Spanien?", "30 Grad", "13 Grad", "20 Grad"),
            ),
            (
                "Mann",
                "Hallo Laura, hier ist Ben. Danke für die Einladung! Ich komme gern zu deiner "
                "Party. Ich bringe einen Kuchen mit.",
                ("Was bringt Ben mit?", "Einen Kuchen", "Einen Salat", "Getränke"),
            ),
            (
                "Frau",
                "Guten Tag, hier ist Mode Chic. Ihr Kleid ist fertig. Sie können es ab Dienstag abholen.",
                (
                    "Ab wann kann man das Kleid abholen?",
                    "Ab Dienstag",
                    "Ab Montag",
                    "Ab Donnerstag",
                ),
            ),
            (
                "Mann",
                "Hallo Opa, hier ist Max. Herzlichen Glückwunsch zum Geburtstag! Wir besuchen dich am Sonntag.",
                ("Wann besucht Max seinen Opa?", "Am Sonntag", "Am Samstag", "Heute"),
            ),
            (
                "Frau",
                "Hallo, hier ist Eva. Es schneit so schön! Fahren wir morgen in die Berge? Ruf mich an!",
                (
                    "Wohin möchte Eva morgen fahren?",
                    "In die Berge",
                    "An den Strand",
                    "In die Stadt",
                ),
            ),
        ],
    ),
}
