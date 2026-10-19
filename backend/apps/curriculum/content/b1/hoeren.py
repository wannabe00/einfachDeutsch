"""B1 Hören sets: one per Modul, in the same four-Teil shape as A2 (Teil 1: 5
radio texts, announcements and phone messages, a/b/c, heard twice. Teil 2: one
conversation, 5 items matched to choices, heard once. Teil 3: 5 short
dialogues, a/b/c, heard once. Teil 4: a radio interview, 5 statements ja/nein,
heard twice), with longer B1 scripts.

All scripts are original, on the Modul's topics. The audio is generated once
with `manage.py make_hoeren_audio`; a Modul goes live in production when it is
added to `LIVE` after its audio is recorded (DEBUG shows every set).
"""

from ..a2.hoeren import CONVERSATION, DIALOGUES, INTERVIEW, RADIO, _sound
from ..dsl import clip, hoeren_match, hoeren_mc, hoeren_teil, hoeren_yn

# Empty until the B1 audio is recorded (owner runs make_hoeren_audio locally).
LIVE: set[int] = set()

# Where each Modul's conversation (Teil 2) and dialogues (Teil 3) take place.
SCENES = {
    1: ("cafe", ["buero", "cafe", "", "strasse", ""]),
    2: ("", ["laden", "cafe", "buero", "", "cafe"]),
    3: ("buero", ["laden", "park", "buero", "", "cafe"]),
    4: ("cafe", ["bahnhof", "", "buero", "cafe", ""]),
    5: ("buero", ["", "laden", "cafe", "buero", ""]),
    6: ("cafe", ["", "cafe", "strasse", "", "buero"]),
    7: ("cafe", ["park", "", "strasse", "cafe", "bahnhof"]),
    8: ("", ["strasse", "cafe", "", "park", "buero"]),
}


def _set(modul, radio, conversation, dialogues, interview) -> list:
    lines, choices, rows = conversation
    talk, statements = interview
    talk_scene, dialogue_scenes = SCENES[modul]
    return [
        hoeren_teil(
            1, RADIO, *[hoeren_mc(clip((who, t), **_sound(who, t)), *q) for who, t, q in radio]
        ),
        hoeren_match(2, CONVERSATION, clip(*lines, plays=1, scene=talk_scene), choices, rows),
        hoeren_teil(
            3,
            DIALOGUES,
            *[
                hoeren_mc(clip(*d, plays=1, scene=where), *q)
                for (d, q), where in zip(dialogues, dialogue_scenes, strict=True)
            ],
        ),
        hoeren_teil(
            4,
            INTERVIEW,
            *[hoeren_yn(s, ok) for s, ok in statements],
            recording=clip(*talk, plays=2, radio=True),
        ),
    ]


HOEREN = {
    # Modul 1 (Lektionen 1-3): friendship, internships, housing.
    1: _set(
        1,
        [
            (
                "Ansage",
                "Und jetzt unser Wohnungstipp der Woche: In der Innenstadt ist eine helle "
                "Dreizimmerwohnung mit Dachterrasse frei. Die Miete beträgt neunhundert Euro, "
                "Besichtigung am Donnerstag um achtzehn Uhr.",
                (
                    "Wann kann man die Wohnung besichtigen?",
                    "Am Donnerstag",
                    "Am Dienstag",
                    "Am Wochenende",
                ),
            ),
            (
                "Frau",
                "Hallo Max, hier ist Sandra. Ich habe gehört, dass du ab Montag dein Praktikum bei "
                "uns machst. Toll! Bring bitte deinen Ausweis mit, weil du einen Schlüssel für "
                "das Büro bekommst. Bis Montag!",
                ("Was soll Max mitbringen?", "Seinen Ausweis", "Einen Schlüssel", "Sein Zeugnis"),
            ),
            (
                "Ansage",
                "Liebe Kunden, unser Möbelhaus feiert Geburtstag. Heute bekommen alle, die ein "
                "Sofa kaufen, einen Sessel gratis dazu. Das Angebot gilt nur bis achtzehn Uhr.",
                ("Was bekommt man heute gratis?", "Einen Sessel", "Ein Sofa", "Einen Tisch"),
            ),
            (
                "Mann",
                "Guten Tag, Frau Kraus, hier spricht Herr Weber, der Hausmeister. Die Heizung in "
                "Ihrer Wohnung wird morgen zwischen neun und elf repariert. Bitte seien Sie dann "
                "zu Hause oder geben Sie den Schlüssel bei Ihrer Nachbarin ab.",
                (
                    "Was soll Frau Kraus tun?",
                    "Zu Hause sein oder den Schlüssel abgeben",
                    "Die Heizung reparieren",
                    "Den Hausmeister anrufen",
                ),
            ),
            (
                "Ansage",
                "Eine aktuelle Umfrage zeigt: Fast die Hälfte der jungen Erwachsenen wohnt noch "
                "bei den Eltern. Der wichtigste Grund ist die hohe Miete in den Großstädten.",
                (
                    "Warum wohnen viele junge Leute bei den Eltern?",
                    "Die Miete ist hoch.",
                    "Sie mögen ihre Eltern.",
                    "Sie studieren nicht.",
                ),
            ),
        ],
        (
            [
                ("Frau", "Und, wie war deine erste Woche im Praktikum?"),
                (
                    "Mann",
                    "Super! Am Montag habe ich alle Kollegen kennengelernt. Der Chef war sehr freundlich.",
                ),
                ("Frau", "Und was hast du am Dienstag gemacht?"),
                ("Mann", "Da habe ich zum ersten Mal Kunden am Telefon beraten. Das war schwer!"),
                ("Frau", "Am Mittwoch hattest du doch frei, oder?"),
                (
                    "Mann",
                    "Nein, am Mittwoch war die große Teamsitzung. Ich musste sogar etwas präsentieren.",
                ),
                ("Frau", "Wow. Und am Donnerstag?"),
                (
                    "Mann",
                    "Da war ich mit einer Kollegin bei einer Besichtigung, in einem neuen Wohnblock.",
                ),
                ("Frau", "Und Freitag?"),
                (
                    "Mann",
                    "Am Freitag habe ich meinen ersten Bericht geschrieben. Den liest der Chef jetzt.",
                ),
            ],
            {
                "a": "Kollegen kennenlernen",
                "b": "Kunden am Telefon beraten",
                "c": "frei haben",
                "d": "an einer Sitzung teilnehmen",
                "e": "eine Wohnung besichtigen",
                "f": "einen Bericht schreiben",
                "g": "eine Prüfung machen",
                "h": "Möbel kaufen",
            },
            [
                ("Montag", "a"),
                ("Dienstag", "b"),
                ("Mittwoch", "d"),
                ("Donnerstag", "e"),
                ("Freitag", "f"),
            ],
        ),
        [
            (
                [
                    ("Frau", "Wer ist denn dein Vorbild?"),
                    (
                        "Mann",
                        "Meine Großmutter. Sie war so mutig und hat allein vier Kinder großgezogen.",
                    ),
                ],
                (
                    "Warum ist die Großmutter ein Vorbild?",
                    "Sie war mutig.",
                    "Sie war reich.",
                    "Sie war streng.",
                ),
            ),
            (
                [
                    ("Mann", "Wie findest du deinen neuen Mitbewohner?"),
                    (
                        "Frau",
                        "Er ist nett, aber überhaupt nicht ordentlich. Die Küche ist immer schmutzig.",
                    ),
                ],
                (
                    "Was stört die Frau?",
                    "Der Mitbewohner ist nicht ordentlich.",
                    "Der Mitbewohner ist unfreundlich.",
                    "Die Küche ist zu klein.",
                ),
            ),
            (
                [
                    ("Frau", "Wohnen Sie zur Miete?"),
                    ("Mann", "Nein, wir haben vor zwei Jahren ein Reihenhaus im Vorort gekauft."),
                ],
                (
                    "Wo wohnt der Mann?",
                    "In einem Reihenhaus",
                    "In einer Mietwohnung",
                    "In der Innenstadt",
                ),
            ),
            (
                [
                    ("Mann", "Hast du das Zeugnis von deinem Praktikum bekommen?"),
                    (
                        "Frau",
                        "Ja, gestern. Da steht, dass ich meine Aufgaben immer zuverlässig erledigt habe.",
                    ),
                ],
                (
                    "Was steht im Zeugnis?",
                    "Sie war zuverlässig.",
                    "Sie war oft zu spät.",
                    "Sie war kreativ.",
                ),
            ),
            (
                [
                    ("Frau", "Wie groß ist eure neue Wohnung?"),
                    ("Mann", "Achtzig Quadratmeter, drei Zimmer und ein kleiner Balkon."),
                ],
                (
                    "Wie groß ist die Wohnung?",
                    "80 Quadratmeter",
                    "30 Quadratmeter",
                    "180 Quadratmeter",
                ),
            ),
        ],
        (
            [
                (
                    "Ansage",
                    "Frau Becker, Sie sind seit dreißig Jahren Maklerin. Ist der Beruf immer noch Ihre Leidenschaft?",
                ),
                (
                    "Frau",
                    "Ja, absolut. Ich finde es schön, wenn Menschen ein neues Zuhause finden, in dem sie glücklich sind.",
                ),
                ("Ansage", "Was war Ihr ungewöhnlichster Kunde?"),
                (
                    "Frau",
                    "Ein Mann, der unbedingt eine Wohnung mit Blick auf den Bahnhof wollte. Er liebt Züge!",
                ),
                ("Ansage", "Ist es heute schwieriger, eine Wohnung zu finden?"),
                (
                    "Frau",
                    "Ja, leider. In der Innenstadt gibt es einen großen Wohnungsmangel. Viele ziehen deshalb in die Vororte.",
                ),
                ("Ansage", "Und wie wohnen Sie selbst?"),
                (
                    "Frau",
                    "Ganz einfach: in einer kleinen Wohnung mit Garten am Stadtrand. Mehr brauche ich nicht.",
                ),
            ],
            [
                ("Frau Becker arbeitet seit dreißig Jahren als Maklerin.", True),
                ("Sie mag ihren Beruf nicht mehr.", False),
                ("Ein Kunde wollte eine Wohnung mit Blick auf den Bahnhof.", True),
                ("In der Innenstadt gibt es viele freie Wohnungen.", False),
                ("Frau Becker wohnt in einem großen Haus in der Innenstadt.", False),
            ],
        ),
    ),
    # Modul 2 (Lektionen 4-6): complaints, technology, invitations.
    2: _set(
        2,
        [
            (
                "Ansage",
                "Herzlich willkommen beim Kundenservice von Telenet. Für Fragen zu Ihrer Rechnung "
                "drücken Sie bitte die Eins. Bei technischen Problemen drücken Sie die Zwei. Für "
                "eine persönliche Beratung bleiben Sie bitte am Apparat.",
                (
                    "Was macht man bei technischen Problemen?",
                    "Die Zwei drücken",
                    "Die Eins drücken",
                    "Am Apparat bleiben",
                ),
            ),
            (
                "Mann",
                "Hallo Lisa, hier ist Paul. Danke für die Einladung zum Essen am Freitag! Ich komme "
                "gern. Ich bringe einen Nachtisch mit, falls du das möchtest. Ruf mich kurz zurück!",
                ("Was will Paul mitbringen?", "Einen Nachtisch", "Blumen", "Wein"),
            ),
            (
                "Ansage",
                "Experten vermuten, dass in zwanzig Jahren in fast jedem Haushalt ein Roboter "
                "arbeiten wird. Die Roboter werden putzen, kochen und sogar mit älteren Menschen "
                "sprechen.",
                (
                    "Was werden Roboter laut Experten tun?",
                    "Im Haushalt helfen",
                    "Autos fahren",
                    "In Schulen unterrichten",
                ),
            ),
            (
                "Frau",
                "Guten Tag, hier ist Frau Klein von der Firma Lexa. Wir haben Ihre Reklamation "
                "erhalten. Obwohl das Gerät noch neu ist, ist es leider kaputt. Wir schicken Ihnen "
                "diese Woche ein neues Gerät.",
                (
                    "Was passiert mit der Reklamation?",
                    "Der Kunde bekommt ein neues Gerät.",
                    "Der Kunde bekommt sein Geld zurück.",
                    "Der Kunde muss das Gerät reparieren.",
                ),
            ),
            (
                "Ansage",
                "Liebe Gäste, unser Restaurant schließt heute schon um zweiundzwanzig Uhr. Falls "
                "Sie noch einen Nachtisch bestellen möchten, sagen Sie bitte jetzt Bescheid.",
                ("Wann schließt das Restaurant heute?", "Um 22 Uhr", "Um 20 Uhr", "Um Mitternacht"),
            ),
        ],
        (
            [
                ("Frau", "Also, für das Fest am Samstag: Wer bringt was mit?"),
                ("Mann", "Klaus bringt den Salat, das hat er schon gesagt."),
                ("Frau", "Gut. Und Maria?"),
                ("Mann", "Maria backt einen Kuchen als Nachtisch. Sie backt so gern."),
                ("Frau", "Und was macht Jonas? Er kann doch nicht kochen."),
                ("Mann", "Jonas kümmert sich um die Getränke. Er bringt Wasser, Saft und Sekt."),
                ("Frau", "Und Tante Erna? Sie ist ja schon achtzig."),
                ("Mann", "Sie braucht nichts mitzubringen. Sie ist unser Ehrengast!"),
                ("Frau", "Und Peter?"),
                ("Mann", "Peter macht die Musik. Er hat eine tolle Anlage."),
            ],
            {
                "a": "Salat",
                "b": "Kuchen",
                "c": "Getränke",
                "d": "nichts",
                "e": "Musik",
                "f": "Blumen",
                "g": "Braten",
                "h": "Brot",
            },
            [("Klaus", "a"), ("Maria", "b"), ("Jonas", "c"), ("Tante Erna", "d"), ("Peter", "e")],
        ),
        [
            (
                [
                    ("Mann", "Hast du die Datei gespeichert?"),
                    (
                        "Frau",
                        "Nein! Der Computer ist abgestürzt, bevor ich speichern konnte. Alles ist weg.",
                    ),
                ],
                (
                    "Was ist das Problem?",
                    "Die Datei ist weg.",
                    "Der Drucker ist kaputt.",
                    "Das Internet geht nicht.",
                ),
            ),
            (
                [
                    ("Frau", "Darf ich Ihnen noch etwas Braten anbieten?"),
                    (
                        "Mann",
                        "Nein danke, es hat ausgezeichnet geschmeckt, aber ich bin schon satt.",
                    ),
                ],
                (
                    "Warum möchte der Mann nichts mehr?",
                    "Er ist satt.",
                    "Es schmeckt nicht.",
                    "Er ist Vegetarier.",
                ),
            ),
            (
                [
                    ("Mann", "Ist Frau Sommer zu sprechen?"),
                    (
                        "Frau",
                        "Leider nicht, sie ist heute außer Haus. Soll ich ihr etwas ausrichten?",
                    ),
                ],
                ("Wo ist Frau Sommer?", "Nicht im Büro", "In einer Sitzung", "Am Telefon"),
            ),
            (
                [
                    ("Frau", "Wie wird das Leben in fünfzig Jahren sein?"),
                    ("Mann", "Ich glaube, dass wir viel weniger Auto fahren werden."),
                ],
                (
                    "Was glaubt der Mann?",
                    "Man wird weniger Auto fahren.",
                    "Man wird mehr Auto fahren.",
                    "Es wird keine Autos mehr geben.",
                ),
            ),
            (
                [
                    ("Mann", "Kommst du zur Party am Samstag?"),
                    (
                        "Frau",
                        "Ich würde gern, aber ich habe eine Erkältung. Falls es mir besser geht, komme ich.",
                    ),
                ],
                (
                    "Kommt die Frau zur Party?",
                    "Vielleicht, wenn sie gesund ist",
                    "Ja, ganz sicher",
                    "Nein, sie hat keine Lust",
                ),
            ),
        ],
        (
            [
                (
                    "Ansage",
                    "Herr Doktor Lang, Sie forschen über die Zukunft der Technik. Werden Computer uns bald ersetzen?",
                ),
                (
                    "Mann",
                    "Nein, das glaube ich nicht. Computer werden uns helfen, aber sie werden die Menschen nicht ersetzen.",
                ),
                ("Ansage", "Viele Menschen haben trotzdem Angst um ihren Arbeitsplatz."),
                (
                    "Mann",
                    "Das verstehe ich. Manche Berufe werden verschwinden, aber es wird auch viele neue Berufe geben.",
                ),
                ("Ansage", "Benutzen Sie selbst viel Technik?"),
                (
                    "Mann",
                    "Im Büro schon. Aber zu Hause habe ich keinen Fernseher, und am Wochenende schalte ich das Handy aus.",
                ),
                ("Ansage", "Was ist Ihr Vorsatz für das nächste Jahr?"),
                ("Mann", "Ich werde mehr Bücher lesen, und zwar auf Papier!"),
            ],
            [
                ("Doktor Lang glaubt, dass Computer die Menschen ersetzen werden.", False),
                ("Er meint, dass es neue Berufe geben wird.", True),
                ("Zu Hause hat er einen Fernseher.", False),
                ("Am Wochenende schaltet er das Handy aus.", True),
                ("Er möchte nächstes Jahr mehr Bücher lesen.", True),
            ],
        ),
    ),
    # Modul 3 (Lektionen 7-9): pets, careers, health at work.
    3: _set(
        3,
        [
            (
                "Ansage",
                "Das Tierheim Pfötchen sucht ein neues Zuhause für drei junge Katzen. Die Tiere "
                "sind sehr zutraulich und schon geimpft. Besuchen Sie uns am Samstag zwischen "
                "zehn und vierzehn Uhr.",
                ("Wann kann man die Katzen besuchen?", "Am Samstag", "Am Sonntag", "Jeden Tag"),
            ),
            (
                "Frau",
                "Hallo Ben, hier ist Mama. Kannst du bitte morgen das Kaninchen füttern? Ich muss "
                "früh zur Arbeit. Das Futter steht im Keller, und vergiss nicht, frisches Wasser "
                "in den Napf zu tun.",
                (
                    "Was soll Ben machen?",
                    "Das Kaninchen füttern",
                    "Futter kaufen",
                    "Zum Tierarzt gehen",
                ),
            ),
            (
                "Ansage",
                "Liebe Mitarbeiter, morgen ist Gesundheitstag. Von neun bis zwölf Uhr gibt es in "
                "Halle A Rückentraining. Bitte bringen Sie bequeme Kleidung mit.",
                ("Was soll man mitbringen?", "Bequeme Kleidung", "Etwas zu essen", "Einen Ausweis"),
            ),
            (
                "Mann",
                "Guten Tag, Frau Neumann, hier ist die Berufsberatung. Ihr Termin am Montag muss "
                "leider ausfallen, weil die Beraterin krank ist. Könnten Sie stattdessen am "
                "Mittwoch um zehn kommen?",
                (
                    "Wann ist der neue Termin?",
                    "Am Mittwoch um zehn",
                    "Am Montag um zehn",
                    "Am Mittwoch um zwölf",
                ),
            ),
            (
                "Ansage",
                "Eine neue Studie zeigt: Wer bei der Arbeit regelmäßig Pausen macht, ist nicht nur "
                "gesünder, sondern auch zufriedener. Schon zehn Minuten an der frischen Luft "
                "helfen gegen Stress.",
                (
                    "Was hilft laut der Studie gegen Stress?",
                    "Pausen an der frischen Luft",
                    "Mehr Arbeit",
                    "Weniger Schlaf",
                ),
            ),
        ],
        (
            [
                (
                    "Mann",
                    "Wir haben den Berufstest im Kurs gemacht. Rate mal, was rausgekommen ist!",
                ),
                ("Frau", "Erzähl! Was ist mit Anna?"),
                ("Mann", "Anna ist ein kreativer Typ. Sie soll Designerin werden."),
                ("Frau", "Das passt. Und Lukas?"),
                ("Mann", "Lukas ist ein technischer Typ. Er repariert ja auch immer alles."),
                ("Frau", "Und Mehmet?"),
                ("Mann", "Mehmet ist ein sozialer Typ. Er möchte Krankenpfleger werden."),
                ("Frau", "Und Clara? Sie arbeitet so gern mit den Händen."),
                ("Mann", "Genau, Clara ist ein handwerklicher Typ. Sie wird Schreinerin."),
                ("Frau", "Und du?"),
                (
                    "Mann",
                    "Ich? Der Test sagt, dass ich Lehrer werden soll. Das hätte ich nicht erwartet!",
                ),
            ],
            {
                "a": "Designerin",
                "b": "Mechaniker",
                "c": "Krankenpfleger",
                "d": "Schreinerin",
                "e": "Lehrer",
                "f": "Psychologe",
                "g": "Tierärztin",
                "h": "Schriftsteller",
            },
            [("Anna", "a"), ("Lukas", "b"), ("Mehmet", "c"), ("Clara", "d"), ("der Mann", "e")],
        ),
        [
            (
                [
                    ("Frau", "Können Sie mir einen Hund empfehlen?"),
                    (
                        "Mann",
                        "Da Sie tagsüber arbeiten, würde ich Ihnen eher eine Katze empfehlen.",
                    ),
                ],
                ("Was empfiehlt der Mann?", "Eine Katze", "Einen kleinen Hund", "Ein Kaninchen"),
            ),
            (
                [
                    ("Mann", "Was machst du, bevor du zur Arbeit fährst?"),
                    ("Frau", "Ich gehe mit dem Hund spazieren und frühstücke dann."),
                ],
                (
                    "Was macht die Frau zuerst?",
                    "Sie geht mit dem Hund spazieren.",
                    "Sie frühstückt.",
                    "Sie fährt zur Arbeit.",
                ),
            ),
            (
                [
                    ("Frau", "Wie war deine Präsentation?"),
                    ("Mann", "Gut! Ich war zwar nervös, aber am Ende haben alle geklatscht."),
                ],
                ("Wie war die Präsentation?", "Gut", "Schlecht", "Langweilig"),
            ),
            (
                [
                    ("Mann", "Darf man hier rauchen?"),
                    (
                        "Frau",
                        "Nein, im ganzen Gebäude gilt ein Rauchverbot. Sie können aber draußen im Hof rauchen.",
                    ),
                ],
                ("Wo darf man rauchen?", "Im Hof", "Im Büro", "Nirgends"),
            ),
            (
                [
                    ("Frau", "Was frisst dein Meerschweinchen am liebsten?"),
                    ("Mann", "Möhren! Aber es bekommt jeden Tag auch frisches Heu."),
                ],
                ("Was frisst das Meerschweinchen am liebsten?", "Möhren", "Heu", "Äpfel"),
            ),
        ],
        (
            [
                (
                    "Ansage",
                    "Frau Wolff, Sie leiten ein Fitnessstudio für Firmen. Was machen Sie genau?",
                ),
                (
                    "Frau",
                    "Wir kommen in die Firmen und machen mit den Mitarbeitern Übungen, direkt am Arbeitsplatz.",
                ),
                ("Ansage", "Wie lange dauert so eine Übung?"),
                (
                    "Frau",
                    "Nur zehn Minuten. Je öfter man sie macht, desto besser ist es für den Rücken.",
                ),
                ("Ansage", "Machen alle Mitarbeiter gern mit?"),
                (
                    "Frau",
                    "Am Anfang nicht. Viele finden es peinlich, im Büro Gymnastik zu machen. Aber nach ein paar Wochen sind die meisten begeistert.",
                ),
                ("Ansage", "Und was raten Sie Menschen, die zu Hause arbeiten?"),
                (
                    "Frau",
                    "Stehen Sie jede Stunde einmal auf und atmen Sie tief durch. Das kostet nichts und hilft sehr.",
                ),
            ],
            [
                ("Frau Wolff macht Übungen mit Mitarbeitern in den Firmen.", True),
                ("Eine Übung dauert eine Stunde.", False),
                ("Am Anfang wollten nicht alle mitmachen.", True),
                ("Später finden die meisten Mitarbeiter die Übungen gut.", True),
                ("Sie rät, zu Hause teure Geräte zu kaufen.", False),
            ],
        ),
    ),
    # Modul 4 (Lektionen 10-12): mishaps, happiness, company events.
    4: _set(
        4,
        [
            (
                "Ansage",
                "Liebe Fahrgäste, wegen einer technischen Störung fährt der Zug nach Hamburg heute "
                "von Gleis sieben statt von Gleis drei. Wir bitten um Entschuldigung.",
                (
                    "Von welchem Gleis fährt der Zug?",
                    "Von Gleis sieben",
                    "Von Gleis drei",
                    "Von Gleis zehn",
                ),
            ),
            (
                "Frau",
                "Hallo Tom, hier ist Kerstin. Stell dir vor, ich habe die Festanstellung bekommen! "
                "Nachdem ich so lange gewartet hatte, kam heute endlich der Anruf. Wir müssen "
                "feiern! Ruf mich an!",
                (
                    "Warum ruft Kerstin an?",
                    "Sie hat eine feste Stelle bekommen.",
                    "Sie hat Geburtstag.",
                    "Sie hat ihren Job verloren.",
                ),
            ),
            (
                "Ansage",
                "Ein Glücksmoment für den FC Seestadt: Nachdem die Mannschaft jahrelang Pech gehabt "
                "hatte, hat sie gestern das Turnier gewonnen. Die Fans haben bis Mitternacht "
                "gefeiert.",
                (
                    "Was ist gestern passiert?",
                    "Die Mannschaft hat gewonnen.",
                    "Die Mannschaft hat verloren.",
                    "Das Turnier ist ausgefallen.",
                ),
            ),
            (
                "Mann",
                "Guten Tag, hier ist das Fundbüro der Stadt. Herr Petersen, wir haben Ihre "
                "Brieftasche gefunden. Sie können sie von Montag bis Freitag bis sechzehn Uhr "
                "abholen.",
                (
                    "Bis wann kann Herr Petersen die Brieftasche abholen?",
                    "Bis 16 Uhr",
                    "Bis 18 Uhr",
                    "Nur am Montag",
                ),
            ),
            (
                "Ansage",
                "Liebe Mitarbeiter, unser Betriebsausflug findet trotz des schlechten Wetterberichts "
                "statt. Wir treffen uns am Freitag um acht Uhr vor dem Haupteingang. Bitte denken "
                "Sie an eine Regenjacke.",
                (
                    "Was sollen die Mitarbeiter mitbringen?",
                    "Eine Regenjacke",
                    "Etwas zu essen",
                    "Ihren Ausweis",
                ),
            ),
        ],
        (
            [
                ("Frau", "Wir müssen die Weihnachtsfeier planen. Wer macht was?"),
                (
                    "Mann",
                    "Herr Kaya kümmert sich um das Buffet. Er kennt einen guten Partyservice.",
                ),
                ("Frau", "Sehr gut. Und die Einladungen?"),
                ("Mann", "Die schreibt Frau Lenz. Sie schickt sie diese Woche per E-Mail."),
                ("Frau", "Und wer hält die Rede?"),
                ("Mann", "Die Rede hält natürlich der Chef, Herr Dr. Albers."),
                ("Frau", "Gibt es auch Musik?"),
                ("Mann", "Ja, Frau Schmidt organisiert eine Band."),
                ("Frau", "Und das Geschenk für Herrn Weber? Er hat ja sein Jubiläum."),
                ("Mann", "Das kauft Herr Roth. Er hat schon eine Idee."),
            ],
            {
                "a": "das Buffet",
                "b": "die Einladungen",
                "c": "die Rede",
                "d": "die Musik",
                "e": "das Geschenk",
                "f": "die Fotos",
                "g": "der Raum",
                "h": "das Protokoll",
            },
            [
                ("Herr Kaya", "a"),
                ("Frau Lenz", "b"),
                ("Herr Dr. Albers", "c"),
                ("Frau Schmidt", "d"),
                ("Herr Roth", "e"),
            ],
        ),
        [
            (
                [
                    ("Mann", "Warum bist du so spät?"),
                    (
                        "Frau",
                        "Ich habe den Bus verpasst. Wäre ich doch nur fünf Minuten früher losgegangen!",
                    ),
                ],
                (
                    "Warum ist die Frau zu spät?",
                    "Sie hat den Bus verpasst.",
                    "Sie hat verschlafen.",
                    "Sie war krank.",
                ),
            ),
            (
                [
                    ("Frau", "Kommst du zum Sommerfest?"),
                    ("Mann", "Leider nicht. Ich habe an dem Tag schon einen Termin beim Arzt."),
                ],
                (
                    "Warum kommt der Mann nicht?",
                    "Er hat einen Arzttermin.",
                    "Er hat keine Lust.",
                    "Er ist im Urlaub.",
                ),
            ),
            (
                [
                    ("Mann", "Was war dein schönster Glücksmoment?"),
                    ("Frau", "Als mein Sohn geboren wurde. Ich habe vor Freude geweint."),
                ],
                (
                    "Was war der schönste Moment der Frau?",
                    "Die Geburt ihres Sohnes",
                    "Ihre Hochzeit",
                    "Ein Lottogewinn",
                ),
            ),
            (
                [
                    ("Frau", "Wann ist die Betriebsversammlung?"),
                    ("Mann", "Am Donnerstag um neun Uhr im großen Saal. Der Betriebsrat lädt ein."),
                ],
                (
                    "Wer lädt zur Versammlung ein?",
                    "Der Betriebsrat",
                    "Der Chef",
                    "Die Gewerkschaft",
                ),
            ),
            (
                [
                    ("Mann", "Oh je, dein Pullover ist ja ganz klein!"),
                    (
                        "Frau",
                        "Ja, ich habe ihn zu heiß gewaschen. Hätte ich bloß das Etikett gelesen!",
                    ),
                ],
                (
                    "Was ist mit dem Pullover passiert?",
                    "Er ist zu klein geworden.",
                    "Er ist kaputt gegangen.",
                    "Er hat einen Fleck.",
                ),
            ),
        ],
        (
            [
                (
                    "Ansage",
                    "Herr Brandl, Sie haben ein Buch über Pech im Alltag geschrieben. Wie kamen Sie auf die Idee?",
                ),
                (
                    "Mann",
                    "Mir passieren ständig dumme Dinge! Letzte Woche habe ich meinen Schlüssel in der Tür stecken lassen.",
                ),
                ("Ansage", "Ärgern Sie sich dann sehr?"),
                (
                    "Mann",
                    "Früher schon. Heute lache ich darüber. Oft ist es sogar gut, weil man interessante Menschen trifft.",
                ),
                ("Ansage", "Haben Sie ein Beispiel?"),
                (
                    "Mann",
                    "Ja. Nachdem ich einmal den Zug verpasst hatte, habe ich am Bahnhof meine heutige Frau kennengelernt.",
                ),
                ("Ansage", "Was raten Sie Ihren Lesern?"),
                ("Mann", "Nicht zu viel ärgern. Da kann man ja sowieso nichts machen."),
            ],
            [
                ("Herr Brandl hat ein Buch über Pech geschrieben.", True),
                ("Letzte Woche hat er seinen Schlüssel verloren.", False),
                ("Heute lacht er über seine Missgeschicke.", True),
                ("Er hat seine Frau im Zug kennengelernt.", False),
                ("Er rät, sich nicht zu sehr zu ärgern.", True),
            ],
        ),
    ),
    # Modul 5 (Lektionen 13-15): misunderstandings, courses, applications.
    5: _set(
        5,
        [
            (
                "Ansage",
                "Die Volkshochschule informiert: Das neue Semester beginnt am fünfzehnten "
                "September. Die Anmeldung ist ab sofort online möglich. Viele Kurse sind schnell "
                "ausgebucht, melden Sie sich deshalb früh an.",
                ("Wann beginnt das Semester?", "Am 15. September", "Am 5. September", "Heute"),
            ),
            (
                "Mann",
                "Guten Tag, Frau Novak, hier ist Herr Lorenz vom Hotel Bergblick. Vielen Dank für "
                "Ihre Bewerbung. Wir möchten Sie gern zu einem Vorstellungsgespräch einladen, am "
                "Dienstag um vierzehn Uhr. Bitte bestätigen Sie den Termin.",
                (
                    "Was soll Frau Novak tun?",
                    "Den Termin bestätigen",
                    "Eine neue Bewerbung schicken",
                    "Sofort vorbeikommen",
                ),
            ),
            (
                "Ansage",
                "Achtung am Gleis vier: Wegen Bauarbeiten fällt der Regionalzug nach Bonn heute "
                "aus. Bitte nehmen Sie den Bus vor dem Bahnhof.",
                (
                    "Wie kommt man heute nach Bonn?",
                    "Mit dem Bus",
                    "Mit dem Regionalzug",
                    "Gar nicht",
                ),
            ),
            (
                "Frau",
                "Hallo Jan, hier ist Mia. Ich glaube, es gab ein Missverständnis: Das Treffen ist "
                "nicht heute, sondern morgen. Wegen der Verwechslung warte ich nicht im Café. Bis "
                "morgen!",
                ("Wann ist das Treffen?", "Morgen", "Heute", "Nächste Woche"),
            ),
            (
                "Ansage",
                "Neu im Programm: Klettern für Anfänger. Vorkenntnisse sind nicht nötig. Die "
                "Teilnahme ist auf eigene Gefahr. Der Kurs kostet achtzig Euro.",
                ("Was kostet der Kletterkurs?", "80 Euro", "18 Euro", "Er ist kostenlos."),
            ),
        ],
        (
            [
                ("Frau", "Ich möchte im Herbst einen Kurs machen, aber ich weiß nicht, welchen."),
                ("Mann", "Was interessiert dich denn? Am Montag gibt es einen Fotokurs."),
                ("Frau", "Fotografieren mache ich schon. Was ist am Dienstag?"),
                ("Mann", "Am Dienstag gibt es Spanisch für Anfänger."),
                ("Frau", "Hm. Und am Mittwoch?"),
                ("Mann", "Am Mittwoch ist der Nähkurs. Den hat meine Schwester gemacht."),
                ("Frau", "Und Donnerstag?"),
                ("Mann", "Donnerstag ist Bewerbungstraining. Das wäre doch was für dich!"),
                ("Frau", "Stimmt. Und was ist am Freitag?"),
                ("Mann", "Am Freitag ist Yoga. Da gehe ich hin."),
            ],
            {
                "a": "Fotografie",
                "b": "Spanisch",
                "c": "Nähen",
                "d": "Bewerbungstraining",
                "e": "Yoga",
                "f": "Kochen",
                "g": "Klettern",
                "h": "Malen",
            },
            [
                ("Montag", "a"),
                ("Dienstag", "b"),
                ("Mittwoch", "c"),
                ("Donnerstag", "d"),
                ("Freitag", "e"),
            ],
        ),
        [
            (
                [
                    (
                        "Mann",
                        "Entschuldigung, könnten Sie das bitte wiederholen? Ich habe Sie nicht verstanden.",
                    ),
                    ("Frau", "Natürlich. Der Zug fährt um zehn nach acht, nicht um acht."),
                ],
                ("Wann fährt der Zug?", "Um 8.10 Uhr", "Um 8 Uhr", "Um 10 Uhr"),
            ),
            (
                [
                    ("Frau", "Welche Sprachen sprechen Sie?"),
                    ("Mann", "Sowohl Englisch als auch Französisch, und ein bisschen Italienisch."),
                ],
                (
                    "Welche Sprache spricht der Mann nur ein bisschen?",
                    "Italienisch",
                    "Englisch",
                    "Französisch",
                ),
            ),
            (
                [
                    ("Mann", "Brauche ich für den Kurs Vorkenntnisse?"),
                    (
                        "Frau",
                        "Nein, der Kurs ist für alle geeignet, die noch nie fotografiert haben.",
                    ),
                ],
                ("Für wen ist der Kurs?", "Für Anfänger", "Für Profis", "Für Kinder"),
            ),
            (
                [
                    ("Frau", "Warum möchten Sie bei uns arbeiten?"),
                    (
                        "Mann",
                        "Weil Ihre Firma nicht nur bekannt ist, sondern auch viele Weiterbildungen anbietet.",
                    ),
                ],
                (
                    "Was gefällt dem Mann an der Firma?",
                    "Die Weiterbildungen",
                    "Das Gehalt",
                    "Der Arbeitsweg",
                ),
            ),
            (
                [
                    ("Mann", "Was ist denn passiert? Du bist ja ganz rot."),
                    (
                        "Frau",
                        "Ich habe den Kellner falsch verstanden und eine riesige Portion bestellt. Das war so peinlich!",
                    ),
                ],
                (
                    "Warum war es der Frau peinlich?",
                    "Sie hat zu viel bestellt.",
                    "Sie hat nicht bezahlt.",
                    "Sie ist gestolpert.",
                ),
            ),
        ],
        (
            [
                (
                    "Ansage",
                    "Frau Engel, Sie sind Personalleiterin. Was ist im Vorstellungsgespräch besonders wichtig?",
                ),
                (
                    "Frau",
                    "Dass die Bewerber ehrlich sind. Ich merke sofort, wenn jemand nur auswendig gelernte Sätze sagt.",
                ),
                ("Ansage", "Und welche Fehler sehen Sie oft?"),
                (
                    "Frau",
                    "Viele Bewerber wissen nichts über unsere Firma. Man sollte sich vorher gut informieren.",
                ),
                ("Ansage", "Wie wichtig ist die Kleidung?"),
                (
                    "Frau",
                    "Sie muss nicht teuer sein, aber ordentlich. Wichtiger ist die Pünktlichkeit.",
                ),
                ("Ansage", "Haben Sie einen Tipp für nervöse Bewerber?"),
                (
                    "Frau",
                    "Ja: Fragen Sie nach, wenn Sie etwas nicht verstehen. Das zeigt Interesse.",
                ),
            ],
            [
                ("Frau Engel findet Ehrlichkeit besonders wichtig.", True),
                ("Die meisten Bewerber wissen viel über die Firma.", False),
                ("Die Kleidung muss teuer sein.", False),
                ("Pünktlichkeit ist für sie sehr wichtig.", True),
                ("Sie findet es gut, wenn Bewerber nachfragen.", True),
            ],
        ),
    ),
    # Modul 6 (Lektionen 16-18): memories, art, politics.
    6: _set(
        6,
        [
            (
                "Ansage",
                "Das Kunstmuseum zeigt ab Sonntag Bilder der Malerin Gabi Roth. Es lohnt sich: "
                "Viele Gemälde werden zum ersten Mal ausgestellt. Der Eintritt ist am ersten Tag "
                "frei.",
                (
                    "Was ist am ersten Tag besonders?",
                    "Der Eintritt ist frei.",
                    "Die Malerin ist da.",
                    "Das Museum ist länger offen.",
                ),
            ),
            (
                "Mann",
                "Hallo Oma, hier ist Felix. Ich mache doch das Interview für die Schule. Du brauchst "
                "nichts vorzubereiten, wir reden einfach. Passt dir Sonntag um drei?",
                ("Was muss die Oma vorbereiten?", "Nichts", "Fotos", "Kuchen"),
            ),
            (
                "Ansage",
                "Am Sonntag ist Bundestagswahl. Die Wahllokale sind von acht bis achtzehn Uhr "
                "geöffnet. Wer nicht kommen kann, kann auch per Brief wählen.",
                ("Bis wann sind die Wahllokale geöffnet?", "Bis 18 Uhr", "Bis 20 Uhr", "Bis 8 Uhr"),
            ),
            (
                "Frau",
                "Guten Tag, hier ist die Bürgerinitiative Grüner Park. Wir sammeln am Samstag "
                "Unterschriften gegen den Bau des Parkhauses. Wir brauchen noch ehrenamtliche "
                "Helfer. Haben Sie Zeit?",
                ("Was sucht die Bürgerinitiative?", "Helfer", "Geld", "Ein Parkhaus"),
            ),
            (
                "Ansage",
                "Eine Umfrage zeigt: Jugendliche interessieren sich weder für Parteien noch für "
                "Wahlen, aber sehr für den Klimaschutz. Viele engagieren sich in Gruppen.",
                (
                    "Wofür interessieren sich Jugendliche laut Umfrage?",
                    "Für den Klimaschutz",
                    "Für Parteien",
                    "Für Wahlen",
                ),
            ),
        ],
        (
            [
                ("Frau", "Erzähl mal, wie war das früher bei euch zu Hause?"),
                ("Mann", "Meine Mutter war sehr streng. Sie hat immer auf Pünktlichkeit geachtet."),
                ("Frau", "Und dein Vater?"),
                ("Mann", "Mein Vater war viel lockerer. Er hat mir abends Geschichten vorgelesen."),
                ("Frau", "Hattest du Geschwister?"),
                ("Mann", "Ja, meine große Schwester. Sie musste immer auf mich aufpassen."),
                ("Frau", "Und deine Großeltern?"),
                ("Mann", "Mein Opa hatte einen Bauernhof. Dort habe ich bei der Ernte geholfen."),
                ("Frau", "Und deine Tante?"),
                ("Mann", "Tante Inge hat mir Klavier beigebracht. Sie war Musiklehrerin."),
            ],
            {
                "a": "war sehr streng",
                "b": "hat Geschichten vorgelesen",
                "c": "musste aufpassen",
                "d": "hatte einen Bauernhof",
                "e": "hat Klavier unterrichtet",
                "f": "hat viel gemalt",
                "g": "war Politiker",
                "h": "hat Taschengeld gegeben",
            },
            [
                ("die Mutter", "a"),
                ("der Vater", "b"),
                ("die Schwester", "c"),
                ("der Opa", "d"),
                ("Tante Inge", "e"),
            ],
        ),
        [
            (
                [
                    ("Frau", "Musstest du als Kind im Haushalt helfen?"),
                    (
                        "Mann",
                        "Nein, ich brauchte nur mein Zimmer aufzuräumen. Alles andere hat meine Mutter gemacht.",
                    ),
                ],
                ("Was musste der Mann als Kind tun?", "Sein Zimmer aufräumen", "Kochen", "Nichts"),
            ),
            (
                [
                    ("Mann", "Wie findest du das Bild?"),
                    (
                        "Frau",
                        "Es fällt mir schwer, das zu sagen. Die Farben gefallen mir, aber die Form nicht.",
                    ),
                ],
                ("Was gefällt der Frau an dem Bild?", "Die Farben", "Die Form", "Gar nichts"),
            ),
            (
                [
                    ("Frau", "Wen wählst du am Sonntag?"),
                    ("Mann", "Ich weiß es noch nicht. Entweder die Grünen oder die SPD."),
                ],
                (
                    "Hat der Mann schon entschieden?",
                    "Nein, noch nicht.",
                    "Ja, die Grünen.",
                    "Ja, er wählt nicht.",
                ),
            ),
            (
                [
                    ("Mann", "Was hältst du von dem neuen Gesetz?"),
                    (
                        "Frau",
                        "Davon halte ich nicht viel. Es ist zwar gut gemeint, aber viel zu teuer.",
                    ),
                ],
                (
                    "Was denkt die Frau über das Gesetz?",
                    "Es ist zu teuer.",
                    "Es ist perfekt.",
                    "Es ist unwichtig.",
                ),
            ),
            (
                [
                    ("Frau", "Wann wurde die Malerin geboren?"),
                    ("Mann", "Im Jahr achtzehnhundertneunzig, in einem kleinen Dorf bei München."),
                ],
                ("Wann wurde die Malerin geboren?", "1890", "1980", "1819"),
            ),
        ],
        (
            [
                ("Ansage", "Frau Maier, Sie sind seit vierzig Jahren ehrenamtlich aktiv. Warum?"),
                (
                    "Frau",
                    "Weil ich etwas zurückgeben möchte. Als ich jung war, haben mir auch viele Menschen geholfen.",
                ),
                ("Ansage", "Was machen Sie genau?"),
                (
                    "Frau",
                    "Ich lese im Krankenhaus Kindern vor, und ich helfe bei der Tafel, wo Lebensmittel verteilt werden.",
                ),
                ("Ansage", "Interessieren sich junge Leute auch für das Ehrenamt?"),
                (
                    "Frau",
                    "Ja, mehr als man denkt. Aber sie wollen weder feste Termine noch lange Sitzungen. Sie helfen lieber bei einzelnen Projekten.",
                ),
                ("Ansage", "Was wünschen Sie sich von der Politik?"),
                ("Frau", "Mehr Anerkennung für die Menschen, die ohne Geld für andere arbeiten."),
            ],
            [
                ("Frau Maier arbeitet seit vierzig Jahren ehrenamtlich.", True),
                ("Als sie jung war, hat ihr niemand geholfen.", False),
                ("Sie liest Kindern im Krankenhaus vor.", True),
                ("Junge Leute mögen feste Termine und lange Sitzungen.", False),
                ("Sie wünscht sich mehr Anerkennung für Ehrenamtliche.", True),
            ],
        ),
    ),
    # Modul 7 (Lektionen 19-21): tourism, mountain huts, concerts and cities.
    7: _set(
        7,
        [
            (
                "Ansage",
                "Der Wetterbericht für die Alpen: Morgen wird es am Vormittag sonnig, am Nachmittag "
                "gibt es Gewitter. Wanderer sollten deshalb früh losgehen und vor vierzehn Uhr "
                "auf einer Hütte sein.",
                (
                    "Wann sollten Wanderer auf der Hütte sein?",
                    "Vor 14 Uhr",
                    "Vor 10 Uhr",
                    "Am Abend",
                ),
            ),
            (
                "Mann",
                "Hallo, hier ist Georg von der Berghütte Edelweiß. Ihre Reservierung für Samstag "
                "ist bestätigt: zwei Plätze im Lager. Bitte bringen Sie einen Schlafsack mit, "
                "Decken gibt es genug.",
                ("Was soll man mitbringen?", "Einen Schlafsack", "Decken", "Essen"),
            ),
            (
                "Ansage",
                "Liebe Besucher, das Konzert der Band Wonnetöne beginnt wegen technischer Probleme "
                "erst um einundzwanzig Uhr. Die Garderobe ist im Untergeschoss.",
                ("Wann beginnt das Konzert?", "Um 21 Uhr", "Um 20 Uhr", "Um 22 Uhr"),
            ),
            (
                "Frau",
                "Hallo Kai, hier ist Jule. Die Karten für das Konzert waren innerhalb einer Stunde "
                "verkauft. Ich habe leider keine bekommen. Wollen wir stattdessen ins Kino gehen?",
                (
                    "Warum geht Jule nicht zum Konzert?",
                    "Es gab keine Karten mehr.",
                    "Sie ist krank.",
                    "Das Konzert fällt aus.",
                ),
            ),
            (
                "Ansage",
                "Die Lüneburger Heide blüht! Je wärmer der August ist, desto mehr Touristen kommen. "
                "Bitte bleiben Sie auf den Wegen, damit die Natur geschützt wird.",
                (
                    "Was sollen die Besucher tun?",
                    "Auf den Wegen bleiben",
                    "Blumen pflücken",
                    "Mit dem Auto fahren",
                ),
            ),
        ],
        (
            [
                ("Frau", "Wir haben die Stadtführung morgen. Was sehen wir zuerst?"),
                ("Mann", "Um neun Uhr beginnen wir am Rathaus."),
                ("Frau", "Und dann?"),
                ("Mann", "Um zehn gehen wir am Fluss entlang zur alten Brücke."),
                ("Frau", "Wann machen wir Mittagspause?"),
                ("Mann", "Um zwölf essen wir in einer Gaststätte in der Altstadt."),
                ("Frau", "Und am Nachmittag?"),
                ("Mann", "Um zwei besichtigen wir das Stadion, das liegt außerhalb der Stadt."),
                ("Frau", "Und am Abend?"),
                ("Mann", "Um acht gehen wir alle zusammen ins Konzert."),
            ],
            {
                "a": "das Rathaus",
                "b": "die alte Brücke",
                "c": "die Gaststätte",
                "d": "das Stadion",
                "e": "das Konzert",
                "f": "das Hallenbad",
                "g": "der Bahnhof",
                "h": "das Museum",
            },
            [("9 Uhr", "a"), ("10 Uhr", "b"), ("12 Uhr", "c"), ("14 Uhr", "d"), ("20 Uhr", "e")],
        ),
        [
            (
                [
                    ("Mann", "Wie spart ihr auf der Hütte Wasser?"),
                    (
                        "Frau",
                        "Indem alle nur kurz duschen. Mehr als drei Minuten ist nicht erlaubt.",
                    ),
                ],
                (
                    "Wie spart man auf der Hütte Wasser?",
                    "Man duscht kurz.",
                    "Man duscht nicht.",
                    "Man trinkt weniger.",
                ),
            ),
            (
                [
                    (
                        "Frau",
                        "Ich hätte noch eine Frage zu Ihrem Vortrag: Wie viele Schafe gibt es in der Heide?",
                    ),
                    ("Mann", "Gute Frage! Ungefähr zehntausend."),
                ],
                ("Wie viele Schafe gibt es?", "Etwa 10 000", "Etwa 1 000", "Etwa 100"),
            ),
            (
                [
                    ("Mann", "Warum wart ihr nicht auf dem Gipfel?"),
                    (
                        "Frau",
                        "Es war so neblig, dass wir nichts sehen konnten. Deshalb sind wir umgekehrt.",
                    ),
                ],
                (
                    "Warum sind sie umgekehrt?",
                    "Wegen des Nebels",
                    "Wegen der Kälte",
                    "Weil sie müde waren",
                ),
            ),
            (
                [
                    ("Frau", "Was muss vor dem Konzert noch gemacht werden?"),
                    (
                        "Mann",
                        "Die Lautsprecher müssen noch aufgebaut werden. Alles andere ist fertig.",
                    ),
                ],
                ("Was ist noch nicht fertig?", "Die Lautsprecher", "Die Bühne", "Die Karten"),
            ),
            (
                [
                    ("Mann", "Wo ist denn das Parkhaus?"),
                    (
                        "Frau",
                        "Gleich um die Ecke, hinter dem Kaufhaus. Die Einfahrt ist auf der linken Seite.",
                    ),
                ],
                (
                    "Wo ist das Parkhaus?",
                    "Hinter dem Kaufhaus",
                    "Neben dem Bahnhof",
                    "Vor dem Rathaus",
                ),
            ),
        ],
        (
            [
                (
                    "Ansage",
                    "Herr Gruber, Sie sind seit zwanzig Jahren Hüttenwirt. Was hat sich verändert?",
                ),
                (
                    "Mann",
                    "Es kommen viel mehr Gäste. Je bekannter die Region wird, desto voller ist die Hütte.",
                ),
                ("Ansage", "Ist das ein Problem?"),
                (
                    "Mann",
                    "Manchmal. Viele Gäste kennen die Regeln nicht. Sie lassen ihren Müll liegen oder sind nachts laut.",
                ),
                ("Ansage", "Was tun Sie dagegen?"),
                (
                    "Mann",
                    "Ich erkläre die Regeln beim Abendessen. Die meisten verstehen dann, dass die Regeln sinnvoll sind.",
                ),
                ("Ansage", "Was gefällt Ihnen an Ihrer Arbeit am besten?"),
                (
                    "Mann",
                    "Der Sonnenaufgang am Morgen. Den sehe ich jeden Tag, und er ist immer wieder einmalig.",
                ),
            ],
            [
                ("Herr Gruber ist seit zwanzig Jahren Hüttenwirt.", True),
                ("Heute kommen weniger Gäste als früher.", False),
                ("Manche Gäste lassen ihren Müll liegen.", True),
                ("Er erklärt die Regeln beim Frühstück.", False),
                ("Am besten gefällt ihm der Sonnenaufgang.", True),
            ],
        ),
    ),
    # Modul 8 (Lektionen 22-24): history, environment, living together.
    8: _set(
        8,
        [
            (
                "Ansage",
                "Heute vor fünfunddreißig Jahren wurde die Berliner Mauer geöffnet. Am Abend gibt "
                "es am Brandenburger Tor ein großes Fest mit Musik und Reden.",
                (
                    "Was ist heute vor 35 Jahren passiert?",
                    "Die Mauer wurde geöffnet.",
                    "Die Mauer wurde gebaut.",
                    "Die BRD wurde gegründet.",
                ),
            ),
            (
                "Frau",
                "Hallo Tim, hier ist Anke. Ich fahre ab jetzt mit dem Rad zur Arbeit, statt das "
                "Auto zu nehmen. Willst du nicht mitkommen? Wir könnten uns um halb acht an der "
                "Kreuzung treffen.",
                ("Wo will Anke Tim treffen?", "An der Kreuzung", "Am Bahnhof", "Vor dem Büro"),
            ),
            (
                "Ansage",
                "Die Stadt informiert: Ab Juli ist die Innenstadt für Autos gesperrt. Damit die "
                "Luft sauberer wird, gibt es neue Radwege und mehr Busse.",
                (
                    "Warum wird die Innenstadt gesperrt?",
                    "Damit die Luft sauberer wird",
                    "Wegen Bauarbeiten",
                    "Wegen eines Festes",
                ),
            ),
            (
                "Mann",
                "Guten Tag, Frau Demir, hier ist Herr Kühn vom Mehrgenerationenhaus. Ab September "
                "ist eine Wohnung mit drei Zimmern frei. Wenn Sie Interesse haben, rufen Sie mich "
                "bitte bis Freitag zurück.",
                (
                    "Bis wann soll Frau Demir zurückrufen?",
                    "Bis Freitag",
                    "Bis September",
                    "Bis morgen",
                ),
            ),
            (
                "Ansage",
                "Das Repair-Café im Gemeindehaus ist jeden Samstag geöffnet. Bringen Sie kaputte "
                "Geräte mit, statt sie wegzuwerfen. Die Reparatur ist kostenlos.",
                ("Was kostet die Reparatur?", "Nichts", "Fünf Euro", "Es hängt vom Gerät ab."),
            ),
        ],
        (
            [
                (
                    "Mann",
                    "Wir machen im Kurs ein Geschichtsquiz. Hilfst du mir mit den Jahreszahlen?",
                ),
                ("Frau", "Klar. Wann endete der Zweite Weltkrieg?"),
                ("Mann", "Neunzehnhundertfünfundvierzig."),
                ("Frau", "Richtig. Und die Luftbrücke nach Berlin?"),
                ("Mann", "Die war neunzehnhundertachtundvierzig."),
                ("Frau", "Gut. Wann wurde die Mauer gebaut?"),
                ("Mann", "Neunzehnhunderteinundsechzig."),
                ("Frau", "Und wann wurde sie geöffnet?"),
                ("Mann", "Neunzehnhundertneunundachtzig, im November."),
                ("Frau", "Und die Wiedervereinigung?"),
                ("Mann", "Ein Jahr später, neunzehnhundertneunzig."),
            ],
            {
                "a": "1945",
                "b": "1948",
                "c": "1961",
                "d": "1989",
                "e": "1990",
                "f": "1949",
                "g": "2002",
                "h": "1953",
            },
            [
                ("Ende des Krieges", "a"),
                ("Luftbrücke", "b"),
                ("Bau der Mauer", "c"),
                ("Öffnung der Mauer", "d"),
                ("Wiedervereinigung", "e"),
            ],
        ),
        [
            (
                [
                    ("Frau", "Warum fährst du jetzt immer mit dem Rad?"),
                    ("Mann", "Um fit zu bleiben. Und ich spare viel Geld für Benzin."),
                ],
                (
                    "Warum fährt der Mann Rad?",
                    "Um fit zu bleiben",
                    "Weil sein Auto kaputt ist",
                    "Weil er keinen Führerschein hat",
                ),
            ),
            (
                [
                    ("Mann", "Wie gefällt dir das Wohnen mit den älteren Nachbarn?"),
                    (
                        "Frau",
                        "Super! Es ist, als ob wir eine große Familie wären. Sie passen oft auf die Kinder auf.",
                    ),
                ],
                (
                    "Was machen die älteren Nachbarn?",
                    "Sie passen auf die Kinder auf.",
                    "Sie kochen für alle.",
                    "Sie putzen das Haus.",
                ),
            ),
            (
                [
                    ("Frau", "Wissen Sie, wann der Euro eingeführt wurde?"),
                    ("Mann", "Meines Wissens im Jahr zweitausendzwei."),
                ],
                ("Wann wurde der Euro eingeführt?", "2002", "1992", "2012"),
            ),
            (
                [
                    ("Mann", "Hast du dich von Paul verabschiedet?"),
                    (
                        "Frau",
                        "Nein, er ist gegangen, ohne etwas zu sagen. Das finde ich unhöflich.",
                    ),
                ],
                (
                    "Was hat Paul gemacht?",
                    "Er ist ohne Abschied gegangen.",
                    "Er hat lange geredet.",
                    "Er hat ein Geschenk gebracht.",
                ),
            ),
            (
                [
                    ("Frau", "Was können wir gegen den Müll im Büro tun?"),
                    (
                        "Mann",
                        "Wir könnten Kaffeetassen benutzen, statt Becher aus Papier zu kaufen.",
                    ),
                ],
                (
                    "Was schlägt der Mann vor?",
                    "Tassen statt Papierbecher",
                    "Weniger Kaffee trinken",
                    "Den Müll trennen",
                ),
            ),
        ],
        (
            [
                (
                    "Ansage",
                    "Frau Hartwig, Sie haben die Maueröffnung neunzehnhundertneunundachtzig in Berlin erlebt. Wie war das?",
                ),
                (
                    "Frau",
                    "Unglaublich. Ich war damals zwanzig und wohnte in Ost-Berlin. Am Abend hörten wir im Radio, dass die Grenze offen ist.",
                ),
                ("Ansage", "Was haben Sie dann gemacht?"),
                (
                    "Frau",
                    "Ich bin mit meinem Bruder sofort zur Grenze gelaufen. Wir waren um Mitternacht im Westen.",
                ),
                ("Ansage", "Wie haben die Menschen reagiert?"),
                (
                    "Frau",
                    "Alle haben gefeiert, gelacht und geweint. Fremde Menschen haben sich umarmt.",
                ),
                ("Ansage", "Und wie sehen Sie das heute?"),
                (
                    "Frau",
                    "Ich bin sehr dankbar. Aber ich finde, dass wir den jungen Menschen mehr über diese Zeit erzählen müssen.",
                ),
            ],
            [
                ("Frau Hartwig wohnte 1989 in Ost-Berlin.", True),
                ("Sie hat die Nachricht im Fernsehen gesehen.", False),
                ("Sie ist allein zur Grenze gegangen.", False),
                ("Viele Menschen haben vor Freude geweint.", True),
                ("Sie möchte, dass junge Menschen mehr über die Zeit erfahren.", True),
            ],
        ),
    ),
}
