"""A1 Schreiben sets, shaped like the Start Deutsch 1 writing paper: one set per
Modul. Teil 1: a short text about a person, then a form with five gaps.
Teil 2: a short message (about 30 words) on three points.

All texts and model answers are original, on the Modul's topics, using the
words taught up to the Modul's last Lektion.
"""

from ..dsl import schreiben_form, schreiben_text

MESSAGE = "Write a short message (about 30 words)."
WORDS = (20, 40)


def _set(form, message) -> list:
    situation, fields = form
    return [schreiben_form(situation, fields), schreiben_text(MESSAGE, *message)]


SCHREIBEN = {
    # Modul 1 (Lektionen 1-3): introducing yourself, jobs, family, languages.
    1: _set(
        (
            """
            Ihre Freundin Ana Costa ist 27 Jahre alt und kommt aus Brasilien.
            Sie wohnt jetzt in Köln. Sie ist Ärztin, aber in Deutschland
            arbeitet sie nicht. Sie ist verheiratet und hat einen Sohn.
            Sie geht in eine Sprachschule. Helfen Sie Ana mit dem Formular.
            """,
            [
                ("Familienname:", "Costa"),
                ("Alter:", "27|27 Jahre|siebenundzwanzig"),
                ("Land:", "Brasilien"),
                ("Beruf:", "Ärztin"),
                ("Familienstand:", "verheiratet"),
            ],
        ),
        (
            "Sie haben eine neue Kollegin, Frau Berg. Schreiben Sie Frau Berg eine "
            "kurze E-Mail und stellen Sie sich vor.",
            ["Name und Land?", "Wo wohnen Sie?", "Welche Sprachen sprechen Sie?"],
            WORDS,
            """
            Guten Tag, Frau Berg,
            ich heiße Marco Rossi und komme aus Italien. Ich wohne in Hamburg.
            Ich spreche Italienisch, Englisch und ein bisschen Deutsch.
            Viele Grüße
            Marco Rossi
            """,
            True,
        ),
    ),
    # Modul 2 (Lektionen 4-6): furniture and prices, things, the office.
    2: _set(
        (
            """
            Ihr Kollege Jonas Weber kauft im Möbelhaus Krause ein Sofa. Es kostet
            499 Euro. Jonas wohnt in der Gartenstraße 12 in Köln. Seine
            Telefonnummer ist 0221 48 39 20. Er braucht das Sofa am Samstag.
            """,
            [
                ("Name:", "Weber|Jonas Weber"),
                ("Straße:", "Gartenstraße 12|Gartenstr. 12|Gartenstraße"),
                ("Telefon:", "0221 48 39 20|0221483920|0221 483920"),
                ("Was kaufen Sie?", "Sofa|ein Sofa|das Sofa"),
                ("Wann brauchen Sie es?", "Samstag|am Samstag"),
            ],
        ),
        (
            "Sie haben ein Zimmer, aber keinen Tisch. Ihre Freundin Lisa hat einen "
            "alten Tisch. Schreiben Sie Lisa.",
            ["Warum schreiben Sie?", "Was kostet der Tisch?", "Wann kommen Sie?"],
            WORDS,
            """
            Hallo Lisa,
            ich habe ein Zimmer, aber keinen Tisch. Hast du deinen alten Tisch
            noch? Was kostet er? Ich komme am Samstag um 10 Uhr. Geht das?
            Liebe Grüße
            Tim
            """,
        ),
    ),
    # Modul 3 (Lektionen 7-9): hobbies, times and dates, food and drink.
    3: _set(
        (
            """
            Ihre Nachbarin Eva Schulz ist 45 Jahre alt. Sie kocht gern und
            möchte einen Kochkurs machen: Küche aus Italien. Sie hat am Dienstag
            und am Donnerstag am Abend Zeit. Sie isst kein Fleisch.
            """,
            [
                ("Name:", "Eva Schulz|Schulz"),
                ("Alter:", "45|45 Jahre|fünfundvierzig"),
                ("Kurs: Küche aus …", "Italien"),
                (
                    "Welche Tage?",
                    "Dienstag und Donnerstag|Dienstag, Donnerstag|Donnerstag und Dienstag|Di und Do",
                ),
                ("Essen Sie Fleisch? (ja / nein)", "nein"),
            ],
        ),
        (
            "Ihr Freund Paul hat Sie am Samstag zum Essen eingeladen. Sie können am "
            "Samstag nicht. Schreiben Sie Paul.",
            ["Danke für die Einladung", "Warum können Sie nicht?", "Ein anderer Tag?"],
            WORDS,
            """
            Hallo Paul,
            vielen Dank für die Einladung! Leider kann ich am Samstag nicht, ich
            arbeite. Hast du am Sonntag Zeit? Ich bringe einen Kuchen mit.
            Viele Grüße
            Anna
            """,
        ),
    ),
    # Modul 4 (Lektionen 10-12): transport, the Perfekt, months and celebrations.
    4: _set(
        (
            """
            Ihr Freund Ali Demir fährt am 15. Juni mit dem Zug von Hamburg nach
            München. Am 20. Juni fährt er zurück. Er nimmt sein Fahrrad mit.
            Er kauft die Fahrkarte im Internet.
            """,
            [
                ("Von:", "Hamburg"),
                ("Nach:", "München"),
                ("Hinfahrt am:", "15. Juni|15.6.|15.06.|15 Juni|am 15. Juni"),
                ("Rückfahrt am:", "20. Juni|20.6.|20.06.|20 Juni|am 20. Juni"),
                ("Fahrrad? (ja / nein)", "ja"),
            ],
        ),
        (
            "Sie haben am Samstag Geburtstag und machen eine Party. Schreiben Sie "
            "Ihrer Freundin Mia eine Einladung.",
            ["Wann und wo ist die Party?", "Was soll Mia mitbringen?", "Mia soll antworten."],
            WORDS,
            """
            Liebe Mia,
            am Samstag habe ich Geburtstag und mache eine Party! Wir feiern ab
            19 Uhr bei mir. Kannst du einen Salat mitbringen? Bitte antworte bis
            Donnerstag.
            Liebe Grüße
            Lena
            """,
        ),
    ),
    # Modul 5 (Lektionen 13-15): directions, flats and houses, the city.
    5: _set(
        (
            """
            Ihr Kollege Tomasz Nowak sucht eine Wohnung in Leipzig. Er möchte zwei
            Zimmer und einen Balkon. Die Miete darf 600 Euro kosten. Er hat einen
            Hund. Ab 1. Oktober möchte er in der Wohnung wohnen.
            """,
            [
                ("Stadt:", "Leipzig"),
                ("Zimmer:", "2|zwei|2 Zimmer|zwei Zimmer"),
                ("Miete bis:", "600|600 Euro|600 €|600€"),
                ("Tiere:", "Hund|ein Hund|einen Hund|ja, einen Hund|ja, ein Hund"),
                ("Ab wann?", "1. Oktober|1.10.|01.10.|ab 1. Oktober|Oktober"),
            ],
        ),
        (
            "Sie haben eine neue Wohnung. Schreiben Sie Ihrem Freund Max.",
            ["Wie ist die Wohnung?", "Wo ist die Wohnung?", "Wann soll Max kommen?"],
            WORDS,
            """
            Hallo Max,
            ich habe eine neue Wohnung! Sie hat drei Zimmer und einen Balkon. Sie
            ist in der Altstadt, neben dem Park. Komm doch am Samstag um 16 Uhr!
            Bis bald
            Sara
            """,
        ),
    ),
    # Modul 6 (Lektionen 16-18): hotel and appointments, plans, health.
    6: _set(
        (
            """
            Ihre Freundin Julia Brandt ist 31 Jahre alt. Sie ist krank: Sie hat
            seit Montag Fieber und Halsschmerzen. Heute geht sie zum ersten Mal zu
            Dr. Lehmann. Sie wohnt in der Bahnhofstraße 5 in Bonn.
            """,
            [
                ("Vorname:", "Julia"),
                ("Alter:", "31|31 Jahre|einunddreißig"),
                (
                    "Adresse:",
                    "Bahnhofstraße 5, Bonn|Bahnhofstraße 5|Bahnhofstr. 5|Bahnhofstraße 5 Bonn",
                ),
                (
                    "Was haben Sie?",
                    "Fieber und Halsschmerzen|Halsschmerzen und Fieber|Fieber, Halsschmerzen",
                ),
                ("Seit wann?", "Montag|seit Montag"),
            ],
        ),
        (
            "Sie haben am Freitag um 10 Uhr einen Termin bei Ihrer Friseurin, Frau "
            "Klein. Sie können nicht kommen. Schreiben Sie Frau Klein.",
            ["Warum schreiben Sie?", "Warum können Sie nicht kommen?", "Neuer Termin?"],
            WORDS,
            """
            Sehr geehrte Frau Klein,
            leider kann ich am Freitag um 10 Uhr nicht kommen. Ich bin krank.
            Haben Sie nächste Woche am Dienstag einen Termin für mich?
            Mit freundlichen Grüßen
            Lea Maier
            """,
            True,
        ),
    ),
    # Modul 7 (Lektionen 19-21): looks and character, housework, rules.
    7: _set(
        (
            """
            Ihr Freund Leon Fischer ist 23 Jahre alt und Student. Er sucht ein
            Zimmer in einer WG in Freiburg. Er ist ordentlich und kocht gern. Er
            raucht nicht. Seine Handynummer ist 0176 22 45 81.
            """,
            [
                ("Alter:", "23|23 Jahre|dreiundzwanzig"),
                ("Beruf:", "Student"),
                ("Rauchen Sie? (ja / nein)", "nein"),
                ("Hobby:", "kochen|Kochen|er kocht gern"),
                ("Handy:", "0176 22 45 81|0176224581|0176 224581"),
            ],
        ),
        (
            "Sie wohnen in einer WG. Ihr Mitbewohner Jan räumt nie auf. Schreiben Sie "
            "Jan eine Nachricht.",
            ["Was ist das Problem?", "Was soll Jan machen?", "Eine Regel für die WG?"],
            WORDS,
            """
            Hallo Jan,
            die Küche ist nicht sauber und der Müll ist noch da. Bitte spül heute
            das Geschirr und bring den Müll raus. Machen wir einen Plan für den
            Haushalt?
            Gruß
            Mia
            """,
        ),
    ),
    # Modul 8 (Lektionen 22-24): clothes, weather and holidays, celebrations.
    8: _set(
        (
            """
            Familie Schneider (zwei Erwachsene und zwei Kinder) macht im August
            Urlaub an der Ostsee. Sie möchten eine Ferienwohnung vom 3. bis
            17. August. Herr Schneider heißt Thomas. Die Familie kommt mit dem Auto.
            """,
            [
                ("Vorname:", "Thomas"),
                ("Personen:", "4|vier|4 Personen|vier Personen"),
                ("Von:", "3. August|3.8.|03.08.|3 August"),
                ("Bis:", "17. August|17.8.|17 August"),
                ("Sie kommen mit:", "Auto|dem Auto|mit dem Auto"),
            ],
        ),
        (
            "Sie sind im Urlaub in Spanien. Schreiben Sie Ihrer Kollegin Frau Lang eine Karte.",
            ["Wo sind Sie?", "Wie ist das Wetter?", "Was machen Sie jeden Tag?"],
            WORDS,
            """
            Liebe Frau Lang,
            viele Grüße aus Spanien! Ich bin eine Woche in Valencia. Die Sonne
            scheint und es ist 28 Grad warm. Jeden Tag gehe ich an den Strand.
            Herzliche Grüße
            Ihre Petra Wolf
            """,
            True,
        ),
    ),
}
