"""A2 Schreiben sets, shaped like the Goethe A2 writing paper: one set per Modul.
Teil 1: an informal SMS (20-30 words). Teil 2: a semi-formal e-mail
(30-40 words). Three points each.

All tasks and model answers are original, on the Modul's topics.
"""

from ..dsl import schreiben_text

SMS = "Write an SMS (20-30 words)."
EMAIL = "Write an e-mail (30-40 words)."


def _set(sms, email) -> list:
    """Each is (situation, points, model answer)."""
    (s1, p1, m1), (s2, p2, m2) = sms, email
    return [
        schreiben_text(SMS, s1, p1, (20, 30), m1, teil=1),
        schreiben_text(EMAIL, s2, p2, (30, 40), m2, formal=True, teil=2),
    ]


SCHREIBEN = {
    # Modul 1 (Lektionen 1-3): family and childhood, furniture, holidays in nature.
    1: _set(
        (
            "Sie sind im Urlaub in einer Pension am See. Schreiben Sie Ihrer "
            "Schwester Nina eine SMS.",
            [
                "Sagen Sie, wo Sie sind.",
                "Schreiben Sie, was Ihnen gefällt.",
                "Was machen Sie morgen?",
            ],
            """
            Hallo Nina,
            ich bin in einer kleinen Pension am Bodensee. Die Aussicht ist toll
            und es ist so ruhig! Morgen wandern wir auf einen Berg.
            Liebe Grüße, Eva
            """,
        ),
        (
            "Sie ziehen nächsten Monat um. Sie haben eine Anzeige von „Umzüge "
            "Becker“ gelesen. Schreiben Sie eine E-Mail an Herrn Becker.",
            [
                "Sagen Sie, wann Sie umziehen.",
                "Schreiben Sie, welche Möbel Sie haben.",
                "Fragen Sie nach dem Preis.",
            ],
            """
            Sehr geehrter Herr Becker,
            am 15. Mai ziehe ich von Bonn nach Köln um. Ich habe ein Sofa, ein
            Bett, einen großen Schrank und zehn Kartons. Was kostet das?
            Mit freundlichen Grüßen
            Paul Weber
            """,
        ),
    ),
    # Modul 2 (Lektionen 4-6): shopping and quantities, sightseeing, culture.
    2: _set(
        (
            "Sie sind im Supermarkt. Ihr Mitbewohner Ben kocht heute. Schreiben Sie Ben eine SMS.",
            [
                "Fragen Sie, was er braucht.",
                "Sagen Sie, was heute im Angebot ist.",
                "Sagen Sie, wann Sie nach Hause kommen.",
            ],
            """
            Hi Ben,
            ich bin im Supermarkt. Was brauchst du noch für das Essen? Hähnchen
            ist heute im Angebot! Ich bin um 18 Uhr zu Hause.
            Bis gleich, Tom
            """,
        ),
        (
            "Sie möchten mit Ihrer Familie eine Stadtführung machen. Schreiben Sie "
            "an die Touristen-Information.",
            [
                "Sagen Sie, wann Sie kommen möchten.",
                "Schreiben Sie, wie viele Personen kommen.",
                "Fragen Sie, ob es eine Führung für Kinder gibt.",
            ],
            """
            Sehr geehrte Damen und Herren,
            wir möchten am Samstag, den 12. Juli, eine Stadtführung machen. Wir
            sind vier Personen: zwei Erwachsene und zwei Kinder. Gibt es auch
            eine Führung für Kinder?
            Mit freundlichen Grüßen
            Anna Klein
            """,
        ),
    ),
    # Modul 3 (Lektionen 7-9): sport, health, work.
    3: _set(
        (
            "Sie sind krank und können heute nicht zum Fußballtraining kommen. "
            "Schreiben Sie Ihrem Trainer Martin eine SMS.",
            [
                "Sagen Sie, dass Sie nicht kommen.",
                "Erklären Sie, warum.",
                "Fragen Sie nach dem Spiel am Samstag.",
            ],
            """
            Hallo Martin,
            ich kann heute leider nicht zum Training kommen. Ich habe eine
            Erkältung und Fieber. Wann ist das Spiel am Samstag?
            Viele Grüße, Jonas
            """,
        ),
        (
            "Sie haben am Montag einen Termin bei Dr. Wagner. An dem Tag müssen Sie "
            "arbeiten. Schreiben Sie an die Praxis.",
            [
                "Erklären Sie, warum Sie schreiben.",
                "Sagen Sie, warum Sie nicht kommen können.",
                "Fragen Sie nach einem neuen Termin.",
            ],
            """
            Sehr geehrte Damen und Herren,
            ich habe am Montag um 9 Uhr einen Termin bei Dr. Wagner. Leider muss
            ich an diesem Tag arbeiten. Haben Sie am Mittwoch einen Termin frei?
            Mit freundlichen Grüßen
            Ali Yilmaz
            """,
        ),
    ),
    # Modul 4 (Lektionen 10-12): restaurant, family news and feelings, food.
    4: _set(
        (
            "Ihre Freundin Lisa hat ein Baby bekommen. Schreiben Sie Lisa eine SMS.",
            [
                "Gratulieren Sie.",
                "Fragen Sie, wie es ihr geht.",
                "Fragen Sie, wann Sie sie besuchen können.",
            ],
            """
            Liebe Lisa,
            herzlichen Glückwunsch zur Geburt! Ich freue mich so für euch. Wie
            geht es dir und dem Baby? Wann kann ich euch besuchen?
            Deine Sara
            """,
        ),
        (
            "Sie haben im Restaurant „Seeterrasse“ für Samstag einen Tisch für vier "
            "Personen reserviert. Jetzt kommen acht Personen. Schreiben Sie an das "
            "Restaurant.",
            [
                "Erklären Sie, warum Sie schreiben.",
                "Fragen Sie nach einem größeren Tisch.",
                "Sagen Sie, dass zwei Gäste vegetarisch essen.",
            ],
            """
            Sehr geehrte Damen und Herren,
            ich habe für Samstag um 19 Uhr einen Tisch für vier Personen
            reserviert. Jetzt kommen aber acht Personen. Haben Sie einen größeren
            Tisch? Zwei Gäste essen vegetarisch.
            Mit freundlichen Grüßen
            Maria Lopez
            """,
        ),
    ),
    # Modul 5 (Lektionen 13-15): learning languages, the post, media.
    5: _set(
        (
            "Heute kommt ein Paket für Sie, aber Sie sind nicht zu Hause. Schreiben "
            "Sie Ihrem Nachbarn Tim eine SMS.",
            [
                "Erklären Sie, warum Sie schreiben.",
                "Bitten Sie Tim, das Paket zu nehmen.",
                "Sagen Sie, wann Sie es holen.",
            ],
            """
            Hallo Tim,
            heute kommt ein Paket für mich, aber ich bin nicht zu Hause. Kannst du
            es bitte für mich nehmen? Ich hole es heute Abend.
            Danke! Lena
            """,
        ),
        (
            "Sie möchten an der Sprachschule Lingua einen Deutschkurs machen. "
            "Schreiben Sie eine E-Mail an Frau Hartmann.",
            [
                "Sagen Sie, welchen Kurs Sie suchen.",
                "Schreiben Sie, wann Sie Zeit haben.",
                "Fragen Sie nach dem Preis.",
            ],
            """
            Sehr geehrte Frau Hartmann,
            ich lerne seit einem Jahr Deutsch und suche einen A2-Kurs. Ich arbeite
            am Tag, darum habe ich nur am Abend Zeit. Was kostet der Kurs?
            Mit freundlichen Grüßen
            Daniel Costa
            """,
        ),
    ),
    # Modul 6 (Lektionen 16-18): the hotel, travel and traffic, weather.
    6: _set(
        (
            "Sie fahren mit dem Auto zu Ihrem Freund Mehmet und stehen im Stau. "
            "Schreiben Sie Mehmet eine SMS.",
            [
                "Sagen Sie, wo Sie sind.",
                "Schreiben Sie, warum Sie später kommen.",
                "Sagen Sie, wann Sie ankommen.",
            ],
            """
            Hallo Mehmet,
            ich bin auf der Autobahn bei Köln. Hier ist ein langer Stau, darum
            komme ich später. Ich bin um 20 Uhr bei dir.
            Bis später, Jan
            """,
        ),
        (
            "Sie haben im Hotel Bergblick ein Doppelzimmer vom 2. bis 5. Mai gebucht. "
            "Sie möchten einen Tag länger bleiben. Schreiben Sie an das Hotel.",
            [
                "Erklären Sie, warum Sie schreiben.",
                "Fragen Sie, ob das Zimmer noch frei ist.",
                "Fragen Sie nach einem Parkplatz.",
            ],
            """
            Sehr geehrte Damen und Herren,
            ich habe vom 2. bis 5. Mai ein Doppelzimmer gebucht. Wir möchten bis
            zum 6. Mai bleiben. Ist das Zimmer noch frei? Haben Sie auch einen
            Parkplatz für uns?
            Mit freundlichen Grüßen
            Eva Sommer
            """,
        ),
    ),
    # Modul 7 (Lektionen 19-21): culture, books and the press, offices.
    7: _set(
        (
            "Sie haben zwei Karten für das Kabarett am Freitag. Schreiben Sie Ihrer "
            "Freundin Julia eine SMS.",
            [
                "Laden Sie Julia ein.",
                "Sagen Sie, wann und wo es ist.",
                "Schlagen Sie einen Treffpunkt vor.",
            ],
            """
            Hi Julia,
            ich habe zwei Kabarett-Karten für Freitag, 20 Uhr, im Theater am
            Markt. Kommst du mit? Treffen wir uns um 19.30 Uhr am Eingang?
            LG Kathi
            """,
        ),
        (
            "Sie haben gestern im Bus Ihre Geldbörse verloren. Schreiben Sie an das Fundbüro.",
            [
                "Sagen Sie, wann und wo Sie sie verloren haben.",
                "Beschreiben Sie die Geldbörse.",
                "Fragen Sie, wann Sie kommen können.",
            ],
            """
            Sehr geehrte Damen und Herren,
            ich habe gestern im Bus 12 meine Geldbörse verloren. Sie ist braun und
            klein. Mein Ausweis und meine EC-Karte sind darin. Wann kann ich zu
            Ihnen kommen?
            Mit freundlichen Grüßen
            Olga Petrova
            """,
        ),
    ),
    # Modul 8 (Lektionen 22-24): mobility, jobs and training, living abroad.
    8: _set(
        (
            "Sie haben morgen ein Vorstellungsgespräch. Ihr Freund Leo hat ein Auto. "
            "Schreiben Sie Leo eine SMS.",
            [
                "Erzählen Sie von dem Vorstellungsgespräch.",
                "Fragen Sie, ob Sie sein Auto haben können.",
                "Sagen Sie, wann Sie es zurückbringen.",
            ],
            """
            Hallo Leo,
            ich habe morgen um 10 Uhr ein Vorstellungsgespräch in Kassel! Kann ich
            dein Auto haben? Ich bringe es um 14 Uhr zurück.
            Danke, Nora
            """,
        ),
        (
            "Das Hotel Adler sucht Mitarbeiter für die Rezeption. Sie haben die "
            "Anzeige gelesen. Schreiben Sie an Frau Schmidt.",
            [
                "Sagen Sie, warum Sie schreiben.",
                "Schreiben Sie etwas über Ihre Erfahrung.",
                "Fragen Sie nach der Arbeitszeit.",
            ],
            """
            Sehr geehrte Frau Schmidt,
            ich habe Ihre Anzeige gelesen und interessiere mich für die Stelle an
            der Rezeption. Ich habe zwei Jahre in einem Hotel in Spanien
            gearbeitet. Wie ist die Arbeitszeit?
            Mit freundlichen Grüßen
            Carlos Ruiz
            """,
        ),
    ),
}
