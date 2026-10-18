"""A1 Hören sets, after the Start Deutsch 1 listening paper, 5 questions per Teil:
Teil 1 one longer conversation (heard twice), Teil 2 five short announcements
(richtig/falsch, heard once), Teil 3 one longer phone call or voicemail (heard
twice). Recordings carry a quiet background `scene`, the thin `phone` sound or
a `gong`, mixed in by `manage.py make_hoeren_audio`.

All scripts are original and use the words taught up to the Modul's last
Lektion (plus names, places and numbers).
"""

from ..dsl import clip, hoeren_rf, hoeren_teil, mc

# The Moduls testers see in production; the rest stay local (DEBUG shows all).
LIVE = set(range(1, 9))

CONVERSATION = "Listen to the conversation. Choose a, b or c. (You hear it twice.)"
ANNOUNCEMENTS = "Listen to the announcements. Richtig oder falsch? (You hear each once.)"
PHONE = "Listen to the phone message. Choose a, b or c. (You hear it twice.)"


def _set(conversation, announcements, phone) -> list:
    """conversation / phone: (lines, scene or phone flags, questions);
    announcements: (text, clip options, (statement, is_true))."""
    talk, where, questions = conversation
    call, call_questions = phone
    return [
        hoeren_teil(
            1, CONVERSATION, *[mc(*q) for q in questions], recording=clip(*talk, scene=where)
        ),
        hoeren_teil(
            2,
            ANNOUNCEMENTS,
            *[hoeren_rf(clip(("Ansage", t), plays=1, **o), *q) for t, o, q in announcements],
        ),
        hoeren_teil(3, PHONE, *[mc(*q) for q in call_questions], recording=clip(*call, phone=True)),
    ]


GONG = {"gong": True}
STATION = {"gong": True, "scene": "bahnhof"}
SHOP = {"gong": True, "scene": "laden"}
OFFICE = {"gong": True, "scene": "buero"}
STREET = {"scene": "strasse"}
PARK = {"scene": "park"}
CAFE = {"scene": "cafe"}
NONE: dict = {}
RADIO = {"radio": True}

M1 = _set(
    (
        [
            ("Mann", "Hallo! Ist hier noch frei?"),
            ("Frau", "Ja, bitte. Bist du auch im Deutschkurs?"),
            ("Mann", "Ja. Ich heiße Pedro. Und du?"),
            ("Frau", "Ich bin Mariam. Woher kommst du, Pedro?"),
            ("Mann", "Aus Brasilien, aus Rio. Und du?"),
            ("Frau", "Ich komme aus Georgien. Ich wohne jetzt in Köln."),
            ("Mann", "Ich auch! Was machst du beruflich?"),
            ("Frau", "Ich bin Krankenschwester. Und du?"),
            ("Mann", "Ich bin Student. Ich studiere hier an der Universität."),
            ("Frau", "Sprichst du auch Englisch?"),
            ("Mann", "Ja, Englisch und Spanisch. Und ein bisschen Deutsch."),
            ("Frau", "Ich spreche Georgisch, Russisch und Englisch."),
            ("Mann", "Hast du Familie hier?"),
            ("Frau", "Ja, meine Schwester wohnt auch in Köln. Sie ist zweiundzwanzig."),
        ],
        "cafe",
        [
            ("Woher kommt Pedro?", "Aus Brasilien.", "Aus Spanien.", "Aus Georgien."),
            ("Wo wohnt Mariam?", "In Köln", "In Rio", "In Georgien"),
            ("Was ist Mariam von Beruf?", "Krankenschwester", "Studentin", "Lehrerin"),
            (
                "Welche Sprachen spricht Pedro?",
                "Englisch und Spanisch",
                "Georgisch und Russisch",
                "Nur Deutsch",
            ),
            ("Wie alt ist Mariams Schwester?", "22 Jahre", "20 Jahre", "12 Jahre"),
        ],
    ),
    [
        (
            "Liebe Studenten, der Deutschkurs A1 ist heute in Zimmer zwanzig.",
            GONG,
            ("Der Kurs ist heute in Zimmer 20.", True),
        ),
        (
            "Achtung, bitte! Frau Weber, bitte kommen Sie zur Information.",
            SHOP,
            ("Frau Weber soll zum Telefon kommen.", False),
        ),
        (
            "Guten Tag im Hotel Europa! Wir sprechen Deutsch, Englisch und Italienisch.",
            RADIO,
            ("Im Hotel sprechen sie Spanisch.", False),
        ),
        (
            "Achtung, bitte: Familie Yilmaz aus der Türkei, bitte kommen Sie zur Information.",
            STATION,
            ("Familie Yilmaz kommt aus der Türkei.", True),
        ),
        (
            "Liebe Eltern, die Telefonnummer von der Schule ist null – drei – null, vierundfünfzig, zweiundachtzig.",
            GONG,
            ("Die Telefonnummer ist 030 54 82.", True),
        ),
    ],
    (
        [
            (
                "Frau",
                "Hallo Tom, hier ist Anna. Wie geht's? Meine Freundin Sofia ist jetzt in Köln. "
                "Sie kommt aus Brasilien und ist Ärztin. Sie spricht ein bisschen Deutsch, aber "
                "sehr gut Englisch. Sie hat zwei Kinder, einen Sohn und eine Tochter. Der Sohn ist "
                "acht und die Tochter ist fünf. Meine Telefonnummer ist null – eins – sieben – null, "
                "dreiundsechzig, neunundzwanzig. Ruf mich bitte an! Tschüs!",
            )
        ],
        [
            ("Wo ist Sofia jetzt?", "In Köln", "In Brasilien", "In Berlin"),
            ("Was ist Sofia von Beruf?", "Ärztin", "Lehrerin", "Krankenschwester"),
            ("Welche Sprache spricht Sofia sehr gut?", "Englisch", "Deutsch", "Spanisch"),
            ("Wie alt ist Sofias Tochter?", "5 Jahre", "8 Jahre", "15 Jahre"),
            ("Wie ist Annas Telefonnummer?", "0170 63 29", "0170 36 29", "0170 63 92"),
        ],
    ),
)

HOEREN = {
    1: M1,
    # Modul 2 (Lektionen 4-6): furniture and prices, things and colours, the office.
    2: _set(
        (
            [
                ("Frau", "Entschuldigung, können Sie mir helfen? Ich suche einen Tisch."),
                ("Mann", "Gern. Für die Küche oder für das Zimmer?"),
                ("Frau", "Für mein Zimmer. Er soll nicht so groß sein."),
                ("Mann", "Hier, dieser Tisch ist klein und rund. Er ist aus Holz."),
                ("Frau", "Schön! Was kostet er?"),
                ("Mann", "Neunundachtzig Euro. Heute ist er im Angebot."),
                ("Frau", "Gut. Und ich brauche auch zwei Stühle."),
                ("Mann", "Die Stühle hier sind modern. Ein Stuhl kostet fünfundzwanzig Euro."),
                ("Frau", "Haben Sie die Stühle auch in Weiß?"),
                ("Mann", "Nein, leider nur in Schwarz und Grau."),
                ("Frau", "Dann zwei graue Stühle, bitte."),
                ("Mann", "Gern. Das macht zusammen hundertneununddreißig Euro."),
            ],
            "laden",
            [
                ("Was sucht die Frau zuerst?", "Einen Tisch", "Einen Stuhl", "Ein Bett"),
                ("Wie ist der Tisch?", "Klein und rund", "Groß und eckig", "Klein und eckig"),
                ("Was kostet der Tisch?", "89 Euro", "98 Euro", "25 Euro"),
                ("Welche Farbe haben die Stühle von der Frau?", "Grau", "Weiß", "Schwarz"),
                ("Was kostet alles zusammen?", "139 Euro", "114 Euro", "89 Euro"),
            ],
        ),
        [
            (
                "Liebe Kunden, heute im Sonderangebot: Sofas für nur dreihundertneunundneunzig Euro!",
                SHOP,
                ("Die Sofas kosten heute 399 Euro.", True),
            ),
            (
                "Liebe Kunden, alle Lampen kosten heute nur neunzehn Euro.",
                SHOP,
                ("Die Lampen kosten heute 90 Euro.", False),
            ),
            (
                "Liebe Kolleginnen und Kollegen, wir haben neue Computer. Haben Sie Fragen? Bitte fragen Sie Herrn Becker in Büro zwölf.",
                OFFICE,
                ("Herr Becker ist in Büro 12.", True),
            ),
            (
                "Achtung, bitte: Hier ist eine Tasche. Sie ist blau und klein. Bitte kommen Sie zur Information.",
                SHOP,
                ("Die Tasche ist schwarz.", False),
            ),
            (
                "Achtung: Im Drucker in Büro fünf ist kein Papier. Papier ist in Büro sieben.",
                OFFICE,
                ("Papier ist in Büro 7.", True),
            ),
        ],
        (
            [
                ("Mann", "Firma Hoffmann, guten Tag, hier ist Peter Novak."),
                (
                    "Frau",
                    "Guten Tag, Herr Novak, hier ist Lisa Klein. Ich brauche einen Laptop für die Arbeit.",
                ),
                (
                    "Mann",
                    "Einen Laptop? Kein Problem. Wir haben ein Sonderangebot: dreihundertneunundneunzig Euro.",
                ),
                ("Frau", "Gut. Und ich brauche auch einen Drucker."),
                ("Mann", "Der Drucker kostet neunundneunzig Euro. Brauchen Sie auch Papier?"),
                (
                    "Frau",
                    "Nein, Papier habe ich. Schreiben Sie mir bitte eine E-Mail mit der Rechnung?",
                ),
                ("Mann", "Ja, gern. Wie ist Ihre E-Mail?"),
                ("Frau", "Lisa Punkt Klein at web Punkt de."),
                ("Mann", "Danke, Frau Klein. Auf Wiederhören!"),
            ],
            [
                ("Was braucht Frau Klein zuerst?", "Einen Laptop", "Einen Drucker", "Papier"),
                ("Was kostet der Laptop?", "399 Euro", "99 Euro", "299 Euro"),
                ("Was kostet der Drucker?", "99 Euro", "399 Euro", "19 Euro"),
                (
                    "Braucht Frau Klein Papier?",
                    "Nein, sie hat Papier.",
                    "Ja, viel Papier.",
                    "Ja, ein bisschen.",
                ),
                (
                    "Was soll Herr Novak schreiben?",
                    "Eine E-Mail mit der Rechnung",
                    "Eine SMS",
                    "Einen Brief",
                ),
            ],
        ),
    ),
    # Modul 3 (Lektionen 7-9): hobbies, times and appointments, food and drink.
    3: _set(
        (
            [
                ("Mann", "Hallo Lea! Hast du am Wochenende Zeit?"),
                ("Frau", "Am Samstag nicht, da arbeite ich. Aber am Sonntag habe ich Zeit. Warum?"),
                ("Mann", "Ich gehe am Sonntag ins Kino. Hast du Lust?"),
                ("Frau", "Ja, gern! Wann ist der Film?"),
                ("Mann", "Um sieben Uhr. Wir treffen uns um halb sieben vor dem Kino."),
                ("Frau", "Gut. Und danach? Gehen wir noch etwas essen?"),
                ("Mann", "Klar! Ich kenne ein Restaurant. Dort gibt es super Fisch."),
                ("Frau", "Ach, ich esse keinen Fisch. Aber Salat und Kartoffeln mag ich."),
                ("Mann", "Kein Problem, es gibt auch Salat."),
                ("Frau", "Und was machst du am Samstag?"),
                ("Mann", "Am Samstag spiele ich Fußball. Und am Abend koche ich für meine Eltern."),
            ],
            "cafe",
            [
                ("Wann hat Lea Zeit?", "Am Sonntag", "Am Samstag", "Am Freitag"),
                ("Wann ist der Film?", "Um 19 Uhr", "Um 18:30 Uhr", "Um 17 Uhr"),
                ("Wo treffen sie sich?", "Vor dem Kino", "Im Restaurant", "Im Café"),
                ("Was isst Lea nicht?", "Fisch", "Salat", "Kartoffeln"),
                (
                    "Was macht der Mann am Samstagabend?",
                    "Er kocht für seine Eltern.",
                    "Er spielt Fußball.",
                    "Er geht ins Kino.",
                ),
            ],
        ),
        [
            (
                "Liebe Kunden, heute im Angebot: Äpfel, ein Kilo für nur ein Euro neunundneunzig.",
                SHOP,
                ("Ein Kilo Äpfel kostet heute 1,99 Euro.", True),
            ),
            (
                "Achtung, bitte: Heute kann man im Schwimmbad nur bis achtzehn Uhr schwimmen.",
                GONG,
                ("Man kann heute bis 20 Uhr schwimmen.", False),
            ),
            (
                "Liebe Gäste, das Konzert heute Abend ist nicht um acht Uhr. Es ist um neun Uhr.",
                GONG,
                ("Das Konzert ist um 21 Uhr.", True),
            ),
            (
                "Liebe Gäste, das Frühstück gibt es heute von sieben bis zehn Uhr im Restaurant.",
                CAFE,
                ("Das Frühstück ist im Café.", False),
            ),
            (
                "Liebe Besucher, Sie können das Museum heute bis siebzehn Uhr besuchen.",
                GONG,
                ("Man kann das Museum heute bis 17 Uhr besuchen.", True),
            ),
        ],
        (
            [
                (
                    "Mann",
                    "Hallo Eva, hier ist Ben. Ich mache am Freitag eine Party! Sie ist bei mir zu "
                    "Hause, um acht Uhr. Ich koche Suppe und mache einen Salat. Kannst du einen "
                    "Kuchen backen? Du kannst so gut backen! Wasser, Saft und Bier habe ich. Ich "
                    "habe auch Musik, wir tanzen! Ruf mich bitte an. Bis bald!",
                )
            ],
            [
                ("Wann ist die Party?", "Am Freitag", "Am Samstag", "Am Sonntag"),
                ("Um wie viel Uhr ist die Party?", "Um 8 Uhr", "Um 7 Uhr", "Um 9 Uhr"),
                ("Was macht Ben?", "Suppe und Salat", "Fisch und Salat", "Einen Kuchen"),
                ("Was soll Eva machen?", "Einen Kuchen backen", "Suppe kochen", "Musik mitbringen"),
                (
                    "Was gibt es zu trinken?",
                    "Wasser, Saft und Bier",
                    "Kaffee und Tee",
                    "Nur Wasser",
                ),
            ],
        ),
    ),
    # Modul 4 (Lektionen 10-12): transport, the Perfekt, months and celebrations.
    4: _set(
        (
            [
                ("Frau", "Entschuldigung, wann fährt der nächste Zug nach München?"),
                ("Mann", "Um zehn Uhr zwanzig, von Gleis vier."),
                ("Frau", "Muss ich umsteigen?"),
                ("Mann", "Ja, in Nürnberg. Da steigen Sie in den ICE um."),
                ("Frau", "Und wann komme ich in München an?"),
                ("Mann", "Um vierzehn Uhr fünfzehn."),
                ("Frau", "Gut. Wo kann ich eine Fahrkarte kaufen?"),
                ("Mann", "Dort hinten, links."),
                (
                    "Frau",
                    "Danke. Ich war schon am Wochenende in München. Meine Schwester hat Geburtstag gefeiert.",
                ),
                ("Mann", "Oh, schön! Gute Reise!"),
            ],
            "bahnhof",
            [
                ("Wann fährt der Zug?", "Um 10:20 Uhr", "Um 14:15 Uhr", "Um 10:40 Uhr"),
                ("Von welchem Gleis fährt der Zug?", "Gleis 4", "Gleis 10", "Gleis 14"),
                (
                    "Wo muss die Frau umsteigen?",
                    "In Nürnberg",
                    "In München",
                    "Sie muss nicht umsteigen.",
                ),
                ("Wann kommt sie in München an?", "Um 14:15 Uhr", "Um 10:20 Uhr", "Um 15:14 Uhr"),
                ("Was hat ihre Schwester gefeiert?", "Geburtstag", "Hochzeit", "Silvester"),
            ],
        ),
        [
            (
                "Achtung am Gleis drei: Der Zug nach Köln kommt heute zehn Minuten später.",
                STATION,
                ("Der Zug nach Köln kommt 10 Minuten später.", True),
            ),
            (
                "Liebe Fahrgäste, heute fahren keine Straßenbahnen. Bitte nehmen Sie den Bus.",
                {"gong": True, "scene": "strasse"},
                ("Heute fährt die Straßenbahn.", False),
            ),
            (
                "Achtung, bitte: Der Zug nach Hamburg fährt heute von Gleis sieben, nicht von Gleis zwei.",
                STATION,
                ("Der Zug nach Hamburg fährt von Gleis 2.", False),
            ),
            (
                "Liebe Kollegen, Herr Roth hat heute Geburtstag! Wir feiern um zwölf Uhr im Büro.",
                OFFICE,
                ("Die Feier ist am Mittag.", True),
            ),
            (
                "Liebe Kunden, wir haben vom ersten bis vierzehnten August Urlaub.",
                SHOP,
                ("Der Laden hat im Juli Urlaub.", False),
            ),
        ],
        (
            [
                ("Frau", "Hallo Papa, ich bin's, Lena!"),
                ("Mann", "Hallo Lena! Bist du gut angekommen?"),
                (
                    "Frau",
                    "Ja, ich bin in Hamburg! Ich bin um sechs Uhr aufgestanden und um sieben abgefahren.",
                ),
                ("Mann", "Bist du in Hannover umgestiegen?"),
                ("Frau", "Ja, in Hannover. Und Ben hat mich am Bahnhof abgeholt."),
                ("Mann", "Super. Was macht ihr heute?"),
                ("Frau", "Heute Abend gehen wir ins Kino. Und morgen besuchen wir Bens Eltern."),
                ("Mann", "Wann kommst du zurück?"),
                ("Frau", "Am Sonntag. Mein Zug kommt um sechzehn Uhr an. Holst du mich ab?"),
                ("Mann", "Klar! Bis Sonntag!"),
            ],
            [
                ("Wann ist Lena aufgestanden?", "Um 6 Uhr", "Um 7 Uhr", "Um 8 Uhr"),
                ("Wo ist sie umgestiegen?", "In Hannover", "In Hamburg", "In Berlin"),
                ("Wer hat Lena abgeholt?", "Ben", "Ihr Vater", "Bens Eltern"),
                (
                    "Was machen sie heute Abend?",
                    "Sie gehen ins Kino.",
                    "Sie besuchen Bens Eltern.",
                    "Sie fahren zurück.",
                ),
                ("Wann kommt Lenas Zug am Sonntag an?", "Um 16 Uhr", "Um 6 Uhr", "Um 14 Uhr"),
            ],
        ),
    ),
    # Modul 5 (Lektionen 13-15): directions, flats and houses, the city.
    5: _set(
        (
            [
                ("Frau", "Entschuldigung, ich bin nicht von hier. Wo ist das Hotel Maritim?"),
                (
                    "Mann",
                    "Das Hotel Maritim? Das ist nicht weit. Gehen Sie hier geradeaus bis zur Ampel.",
                ),
                ("Frau", "Bis zur Ampel, okay."),
                ("Mann", "An der Ampel gehen Sie links. Dann sehen Sie den Dom."),
                ("Frau", "Und das Hotel?"),
                ("Mann", "Das Hotel ist neben dem Dom, zwischen dem Dom und der Post."),
                ("Frau", "Gibt es hier in der Nähe auch eine Bank?"),
                ("Mann", "Ja, die Bank ist hinter dem Rathaus. Das ist rechts."),
                ("Frau", "Und wie weit ist es zum Hotel?"),
                ("Mann", "Nur fünfhundert Meter. Zehn Minuten zu Fuß."),
                ("Frau", "Vielen Dank!"),
            ],
            "strasse",
            [
                ("Was sucht die Frau?", "Ein Hotel", "Eine Bank", "Die Post"),
                ("Wo geht sie links?", "An der Ampel", "Am Dom", "An der Post"),
                (
                    "Wo ist das Hotel?",
                    "Zwischen dem Dom und der Post",
                    "Hinter dem Rathaus",
                    "Neben der Bank",
                ),
                ("Wo ist die Bank?", "Hinter dem Rathaus", "Neben dem Dom", "An der Ampel"),
                ("Wie weit ist das Hotel?", "500 Meter", "5 Kilometer", "50 Meter"),
            ],
        ),
        [
            (
                "Liebe Besucher, die Bibliothek ist heute im ersten Stock, nicht im Erdgeschoss.",
                GONG,
                ("Die Bibliothek ist heute im ersten Stock.", True),
            ),
            (
                "Achtung: Heute fährt der Aufzug nicht. Bitte nehmen Sie die Treppe.",
                GONG,
                ("Man soll heute den Aufzug nehmen.", False),
            ),
            (
                "Der Markt ist heute nicht vor dem Rathaus. Er ist im Park.",
                STREET,
                ("Der Markt ist heute im Park.", True),
            ),
            (
                "Liebe Nachbarn, am Samstag machen wir ein Fest im Garten. Es fängt um fünfzehn Uhr an.",
                NONE,
                ("Das Fest ist im Keller.", False),
            ),
            (
                "Liebe Kunden, unser Laden in der Bahnhofstraße ist ab Montag in der Marktstraße.",
                SHOP,
                ("Der Laden ist ab Montag in der Marktstraße.", True),
            ),
        ],
        (
            [
                (
                    "Frau",
                    "Guten Tag, Herr Nowak, hier ist Frau Lang, die Vermieterin. Sie suchen eine "
                    "Wohnung in der Gartenstraße. Die Wohnung ist im zweiten Stock. Sie hat zwei "
                    "Zimmer, eine Küche, ein Bad und einen Balkon. Die Miete ist fünfhundertachtzig "
                    "Euro, mit Nebenkosten sechshundertfünfzig. Die Wohnung ist ab ersten November "
                    "frei. Sie können sie am Samstag um elf Uhr sehen. Bitte rufen Sie mich an. "
                    "Auf Wiederhören!",
                )
            ],
            [
                (
                    "In welchem Stock ist die Wohnung?",
                    "Im zweiten Stock",
                    "Im Erdgeschoss",
                    "Im ersten Stock",
                ),
                ("Wie viele Zimmer hat die Wohnung?", "Zwei", "Drei", "Eins"),
                ("Was kostet die Wohnung mit Nebenkosten?", "650 Euro", "580 Euro", "560 Euro"),
                ("Ab wann ist die Wohnung frei?", "Ab 1. November", "Ab 1. Oktober", "Sofort"),
                (
                    "Wann kann Herr Nowak die Wohnung sehen?",
                    "Am Samstag um 11 Uhr",
                    "Am Sonntag um 11 Uhr",
                    "Am Samstag um 10 Uhr",
                ),
            ],
        ),
    ),
    # Modul 6 (Lektionen 16-18): hotel and appointments, plans, health.
    6: _set(
        (
            [
                ("Mann", "Guten Tag, Frau Berg. Was haben Sie denn?"),
                ("Frau", "Guten Tag, Herr Doktor. Ich habe seit Montag Kopfschmerzen und Fieber."),
                ("Mann", "Haben Sie auch Halsschmerzen?"),
                ("Frau", "Ja, ein bisschen. Und ich bin sehr müde."),
                ("Mann", "Das ist nicht schlimm. Sie müssen viel Tee trinken und im Bett bleiben."),
                ("Frau", "Muss ich auch Tabletten nehmen?"),
                ("Mann", "Ja. Nehmen Sie diese Tabletten dreimal am Tag, nach dem Essen."),
                ("Frau", "Ich arbeite in einem Hotel. Kann ich morgen arbeiten?"),
                (
                    "Mann",
                    "Nein, bleiben Sie drei Tage zu Hause. Kommen Sie am Freitag noch einmal.",
                ),
                ("Frau", "Gut. Danke, Herr Doktor."),
            ],
            "buero",
            [
                ("Seit wann ist die Frau krank?", "Seit Montag", "Seit Freitag", "Seit gestern"),
                ("Was soll sie trinken?", "Viel Tee", "Viel Wasser", "Saft"),
                (
                    "Wie oft soll sie die Tabletten nehmen?",
                    "Dreimal am Tag",
                    "Zweimal am Tag",
                    "Einmal am Tag",
                ),
                ("Wo arbeitet die Frau?", "In einem Hotel", "In einer Praxis", "In einem Büro"),
                ("Wann soll sie wieder kommen?", "Am Freitag", "Morgen", "Am Montag"),
            ],
        ),
        [
            (
                "Liebe Gäste, das Frühstück gibt es heute im Garten.",
                GONG,
                ("Das Frühstück ist heute im Garten.", True),
            ),
            (
                "Die Praxis Doktor Lehmann hat vom ersten bis vierzehnten August Urlaub.",
                NONE,
                ("Die Praxis hat im Juli Urlaub.", False),
            ),
            (
                "Der Deutschkurs ist heute nicht um achtzehn Uhr. Er ist um neunzehn Uhr.",
                GONG,
                ("Der Kurs ist heute um 18 Uhr.", False),
            ),
            (
                "In der Apotheke am Markt bekommen Sie heute bis zweiundzwanzig Uhr Medikamente.",
                SHOP,
                ("Sie bekommen heute bis 22 Uhr Medikamente.", True),
            ),
            (
                "Liebe Gäste, die Heizung funktioniert heute nicht. Der Techniker kommt um vierzehn Uhr.",
                GONG,
                ("Der Techniker kommt am Nachmittag.", True),
            ),
        ],
        (
            [
                ("Frau", "Hotel Sonne, guten Tag. Was kann ich für Sie tun?"),
                (
                    "Mann",
                    "Guten Tag, mein Name ist Kraus. Ich habe ein Zimmer vom dritten bis fünften Mai. Ich komme leider einen Tag später.",
                ),
                ("Frau", "Kein Problem. Dann kommen Sie am vierten Mai?"),
                ("Mann", "Ja, genau. Und ich bleibe bis zum sechsten Mai."),
                ("Frau", "Gut. Eine Nacht kostet neunzig Euro."),
                ("Mann", "Gibt es im Zimmer einen Fernseher?"),
                (
                    "Frau",
                    "Ja, einen Fernseher und eine Dusche. Das Frühstück ist von sieben bis zehn Uhr.",
                ),
                ("Mann", "Super. Ich komme mit dem Auto. Haben Sie eine Garage?"),
                ("Frau", "Ja, die Garage ist hinter dem Hotel."),
                ("Mann", "Vielen Dank! Auf Wiederhören."),
            ],
            [
                ("Wann kommt Herr Kraus jetzt?", "Am 4. Mai", "Am 3. Mai", "Am 5. Mai"),
                ("Bis wann bleibt er?", "Bis zum 6. Mai", "Bis zum 5. Mai", "Bis zum 4. Mai"),
                ("Was kostet eine Nacht?", "90 Euro", "19 Euro", "99 Euro"),
                (
                    "Wann gibt es Frühstück?",
                    "Von 7 bis 10 Uhr",
                    "Von 6 bis 9 Uhr",
                    "Von 7 bis 11 Uhr",
                ),
                ("Wo ist die Garage?", "Hinter dem Hotel", "Neben dem Hotel", "Vor dem Hotel"),
            ],
        ),
    ),
    # Modul 7 (Lektionen 19-21): looks and character, housework, rules.
    7: _set(
        (
            [
                ("Frau", "Jan, wir müssen reden. Die Küche ist schon wieder nicht sauber!"),
                ("Mann", "Oh, tut mir leid. Ich hatte gestern keine Zeit."),
                ("Frau", "Das sagst du immer. Wir brauchen einen Plan für den Haushalt."),
                ("Mann", "Okay. Was soll ich machen?"),
                (
                    "Frau",
                    "Du bringst jeden Montag und Donnerstag den Müll raus. Und am Samstag putzt du das Bad.",
                ),
                ("Mann", "Und was machst du?"),
                (
                    "Frau",
                    "Ich spüle das Geschirr und wische den Boden. Und Paul räumt die Küche auf.",
                ),
                ("Mann", "Paul? Der ist doch so faul!"),
                ("Frau", "Ja, aber jetzt muss er auch helfen. Ich spreche heute Abend mit ihm."),
                ("Mann", "Gut. Ach, und wer bügelt?"),
                ("Frau", "Bügeln? Das macht jeder selbst!"),
            ],
            "",
            [
                (
                    "Was ist das Problem?",
                    "Die Küche ist nicht sauber.",
                    "Das Bad ist kaputt.",
                    "Paul ist krank.",
                ),
                (
                    "Wann bringt Jan den Müll raus?",
                    "Montag und Donnerstag",
                    "Dienstag und Freitag",
                    "Jeden Tag",
                ),
                ("Was macht Jan am Samstag?", "Er putzt das Bad.", "Er spült.", "Er bügelt."),
                ("Wer räumt die Küche auf?", "Paul", "Jan", "Die Frau"),
                ("Wer bügelt?", "Jeder selbst", "Jan", "Paul"),
            ],
        ),
        [
            (
                "Achtung, bitte: Kinder unter zehn Jahren müssen mit den Eltern ins Schwimmbad kommen.",
                GONG,
                ("Kinder unter 10 Jahren dürfen allein ins Schwimmbad.", False),
            ),
            (
                "Liebe Mieter, bitte bringen Sie den Müll nur am Montag und am Donnerstag raus.",
                NONE,
                ("Man bringt den Müll am Montag raus.", True),
            ),
            (
                "Achtung: In diesem Zug darf man nicht rauchen. Und bitte sprechen Sie leise.",
                STATION,
                ("Im Zug darf man rauchen.", False),
            ),
            (
                "Liebe Fahrradfahrer, bitte schieben Sie im Park Ihr Fahrrad.",
                PARK,
                ("Im Park muss man das Fahrrad schieben.", True),
            ),
            (
                "Liebe Besucher, im Park müssen Hunde an der Leine bleiben.",
                PARK,
                ("Im Park dürfen Hunde frei laufen.", False),
            ),
        ],
        (
            [
                (
                    "Frau",
                    "Hallo Mia, hier ist Sophie. Kannst du bitte meinen Bruder am Bahnhof "
                    "abholen? Er heißt Leon und kommt um fünf Uhr an. Du kennst ihn nicht, also: "
                    "Er ist groß und schlank und hat kurze, blonde Haare. Er trägt eine Brille. "
                    "Er hat einen roten Koffer und eine schwarze Jacke. Er ist sehr nett, aber ein "
                    "bisschen ruhig. Danke! Tschüs!",
                )
            ],
            [
                ("Wen soll Mia abholen?", "Sophies Bruder", "Sophies Vater", "Sophies Freund"),
                ("Wann kommt Leon an?", "Um 5 Uhr", "Um 6 Uhr", "Um 4 Uhr"),
                ("Wie sind seine Haare?", "Kurz und blond", "Lang und blond", "Kurz und schwarz"),
                ("Welche Farbe hat sein Koffer?", "Rot", "Schwarz", "Blau"),
                ("Wie ist Leon?", "Nett und ruhig", "Laut und lustig", "Unfreundlich"),
            ],
        ),
    ),
    # Modul 8 (Lektionen 22-24): clothes, weather and holidays, celebrations.
    8: _set(
        (
            [
                ("Frau", "Entschuldigung, ich suche ein Kleid für eine Hochzeit."),
                ("Mann", "Gern. Welche Farbe möchten Sie?"),
                ("Frau", "Vielleicht Blau? Rot finde ich nicht so schön."),
                ("Mann", "Hier ist ein blaues Kleid. Es ist sehr elegant."),
                ("Frau", "Schön! Was kostet es?"),
                (
                    "Mann",
                    "Hundertzwanzig Euro. Das rosa Kleid hier ist billiger, nur neunundachtzig Euro.",
                ),
                ("Frau", "Das blaue Kleid gefällt mir besser. Kann ich es anziehen?"),
                ("Mann", "Natürlich, dort hinten rechts."),
                ("Frau", "Hm, es ist ein bisschen zu klein. Haben Sie es auch größer?"),
                ("Mann", "Ja, hier, eine Nummer größer. Wir haben auch schöne Schuhe dazu."),
                ("Frau", "Nein danke, Schuhe habe ich."),
            ],
            "laden",
            [
                (
                    "Wofür sucht die Frau ein Kleid?",
                    "Für eine Hochzeit",
                    "Für eine Party",
                    "Für die Arbeit",
                ),
                (
                    "Welches Kleid ist billiger?",
                    "Das rosa Kleid",
                    "Das blaue Kleid",
                    "Das rote Kleid",
                ),
                ("Was kostet das blaue Kleid?", "120 Euro", "89 Euro", "112 Euro"),
                (
                    "Was ist das Problem?",
                    "Das Kleid ist zu klein.",
                    "Das Kleid ist zu teuer.",
                    "Die Farbe ist hässlich.",
                ),
                (
                    "Kauft die Frau auch Schuhe?",
                    "Nein, sie hat Schuhe.",
                    "Ja, schwarze Schuhe.",
                    "Ja, blaue Schuhe.",
                ),
            ],
        ),
        [
            (
                "Und jetzt das Wetter: Morgen scheint im Süden die Sonne, im Norden regnet es.",
                RADIO,
                ("Im Norden regnet es morgen.", True),
            ),
            (
                "Liebe Kunden, heute sind alle Mäntel und Jacken zwanzig Prozent billiger!",
                SHOP,
                ("Heute sind die Hosen billiger.", False),
            ),
            (
                "Achtung: Heute ist Sturm. Bitte gehen Sie nicht an den Strand.",
                GONG,
                ("Man soll heute nicht an den Strand gehen.", True),
            ),
            (
                "Frohe Weihnachten! Am vierundzwanzigsten Dezember können Sie bei uns nur bis vierzehn Uhr einkaufen.",
                SHOP,
                ("Am 24. Dezember kann man bis 18 Uhr einkaufen.", False),
            ),
            (
                "Liebe Gäste, unsere Silvesterparty ist im Restaurant im ersten Stock. Sie fängt um einundzwanzig Uhr an.",
                GONG,
                ("Die Party ist im Erdgeschoss.", False),
            ),
        ],
        (
            [
                (
                    "Mann",
                    "Hallo Tina, hier ist Max. Viele Grüße aus Italien! Wir sind seit Montag am "
                    "Meer. Das Wetter ist super: Jeden Tag scheint die Sonne und es ist dreißig "
                    "Grad warm. Nur gestern hat es ein bisschen geregnet. Unsere Ferienwohnung ist "
                    "klein, aber wir sehen das Meer! Jeden Morgen gehe ich schwimmen. Am Samstag "
                    "fahren wir nach Rom. Am Sonntag in einer Woche sind wir wieder zu Hause. Tschüs!",
                )
            ],
            [
                ("Wo ist Max?", "Am Meer in Italien", "In den Bergen", "In Rom"),
                ("Wie warm ist es?", "30 Grad", "13 Grad", "20 Grad"),
                ("Wann hat es geregnet?", "Gestern", "Am Montag", "Jeden Tag"),
                (
                    "Was macht Max jeden Morgen?",
                    "Er geht schwimmen.",
                    "Er fährt nach Rom.",
                    "Er schläft lange.",
                ),
                ("Wohin fahren sie am Samstag?", "Nach Rom", "Nach Hause", "An den Strand"),
            ],
        ),
    ),
}

# Recorded by make_hoeren_audio but not seeded yet: Moduls waiting to replace HOEREN's.
NEXT: dict = {}
