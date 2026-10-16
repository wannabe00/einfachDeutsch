"""A1 Lesen sets, shaped like the Start Deutsch 1 reading paper: one set per
Modul (Teil 1 notes and e-mails, Teil 2 adverts, Teil 3 signs; 15 questions).

All texts are original, on the Modul's topics, and use the words taught up to
the Modul's last Lektion (plus names, places and numbers).
"""

from ..dsl import lesen_adverts, lesen_notes, lesen_signs


def _set(notes, adverts, signs) -> list:
    return [lesen_notes(*notes), lesen_adverts(adverts), lesen_signs(signs)]


LESEN = {
    # Modul 1 (Lektionen 1-3): greetings, jobs, numbers, family, languages.
    1: _set(
        (
            [
                """
                Hallo Lukas,
                ich bin Maria. Ich komme aus Spanien und wohne in Berlin.
                Ich bin Studentin. Ich arbeite auch, ich bin Kellnerin.
                Meine Familie lebt in Madrid.
                Tschüs, Maria
                """,
                """
                Guten Tag, Frau Weber,
                mein Name ist Paul Roth. Ich bin Lehrer und spreche Deutsch,
                Englisch und ein bisschen Französisch. Ich bin 35 Jahre alt,
                verheiratet und habe zwei Kinder.
                Auf Wiedersehen
                Paul Roth
                """,
            ],
            [
                ("Maria kommt aus Spanien.", True),
                ("Maria wohnt in Madrid.", False),
                ("Maria ist Studentin.", True),
                ("Paul Roth spricht ein bisschen Französisch.", True),
                ("Paul Roth hat drei Kinder.", False),
            ],
        ),
        [
            (
                "Ihr Sohn ist 8 Jahre alt. Er spricht Spanisch und ein bisschen Deutsch.",
                "Schule Sonnenberg, Berlin\nKinder: 6-10 Jahre\nWir sprechen Deutsch und Spanisch.",
                "Universität Hamburg\nStudenten aus Spanien: Deutsch für die Universität",
                "a",
            ),
            (
                "Sie sind Arzt aus Italien und wohnen in Wien.",
                "Hotel Alpenblick, Innsbruck\nKellner und Kellnerin\nTelefon 0512 33 81",
                "Praxis Dr. Huber, Wien\nArzt oder Ärztin, Italienisch und Deutsch\nTelefon 01 457 23",
                "b",
            ),
            (
                "Ihre Tochter studiert in Berlin. Sie spricht Englisch, aber nicht Deutsch.",
                "Deutsch für Studenten!\nUniversität Berlin – die Lehrer sprechen Englisch.",
                "Englisch für Kinder\nSchule Lindenhof, Berlin – Kinder: 5-9 Jahre",
                "a",
            ),
            (
                "Sie sind Kellnerin. Sie wohnen in Zürich und sprechen Italienisch.",
                "Restaurant Roma, Basel\nKellnerin mit Italienisch",
                "Café Bella, Zürich\nKellner oder Kellnerin, Italienisch und Deutsch",
                "b",
            ),
            (
                "Ihre Oma ist Rentnerin und spricht ein bisschen Englisch.",
                "Englisch für Schüler\n8-16 Jahre",
                "Englisch für Rentnerinnen und Rentner\nAuch für Großeltern mit ein bisschen Englisch!",
                "b",
            ),
        ],
        [
            (
                "Praxis Dr. Schmidt\nArzt – Englisch, Französisch",
                "Dr. Schmidt spricht Englisch.",
                True,
            ),
            (
                "Café Wien\nHier arbeiten Studenten aus Italien und Spanien.",
                "Im Café arbeiten Studenten aus Frankreich.",
                False,
            ),
            (
                "Schule Lindenhof\nSekretär: Telefon 030 77 45 12",
                "Die Telefonnummer ist 030 77 45 12.",
                True,
            ),
            (
                "Hier wohnen:\nFamilie Becker\nFamilie Yilmaz\nHerr Novak",
                "Herr Novak wohnt hier.",
                True,
            ),
            (
                "Hotel Europa\nWir sprechen Deutsch, Englisch und Russisch.",
                "Im Hotel Europa sprechen sie Italienisch.",
                False,
            ),
        ],
    ),
    # Modul 2 (Lektionen 4-6): furniture, prices, things, colours, the office.
    2: _set(
        (
            [
                """
                Hallo Sabine,
                ich habe ein Zimmer in Köln! Es ist klein, aber schön.
                Ein Bett habe ich. Ich brauche einen Tisch und einen Stuhl.
                Hast du einen Stuhl für mich?
                Gruß, Tim
                """,
                """
                Guten Tag, Herr Lang,
                hier ist die Rechnung für den Schreibtisch und die Lampe:
                289 Euro. Der Drucker ist ein Sonderangebot: 99 Euro.
                Schöne Grüße
                Büro Schmidt
                """,
            ],
            [
                ("Tims Zimmer ist groß.", False),
                ("Tim hat ein Bett.", True),
                ("Tim braucht einen Stuhl.", True),
                ("Der Schreibtisch und die Lampe kosten 289 Euro.", True),
                ("Der Drucker kostet 120 Euro.", False),
            ],
        ),
        [
            (
                "Sie brauchen einen Tisch für 50 Euro.",
                "Tisch aus Holz, 2 m lang\n450 €",
                "Kleiner Tisch, rund, Holz\n45 €",
                "b",
            ),
            (
                "Sie haben drei Kinder und suchen ein Sofa für die Familie.",
                "Großes Sofa, blau, für 5 Personen\n600 €",
                "Sofa, klein und modern, für 2 Personen\n250 €",
                "a",
            ),
            (
                "Sie brauchen Stifte und Papier für das Büro.",
                "Büro Becker\nComputer, Drucker, Bildschirme – günstig!",
                "Papier & Co.\nPapier, Kugelschreiber, Bleistifte, Notizbücher",
                "b",
            ),
            (
                "Sie suchen eine kleine Lampe. Sie soll rot sein.",
                "Kleine Lampe, rot, Plastik\n19 €",
                "Große Lampe, schwarz, Metall\n80 €",
                "a",
            ),
            (
                "Sie brauchen einen Laptop. 900 Euro ist zu teuer.",
                "Laptop, sehr modern\n1.200 €",
                "Sonderangebot: Laptop, neu\n399 €",
                "b",
            ),
        ],
        [
            (
                "Möbel Krause – Sonderangebot!\nStühle: 29 €\nTische: 99 €",
                "Ein Tisch kostet 99 Euro.",
                True,
            ),
            ("Achtung! Kein Papier im Drucker.\nPapier: Büro 12", "Papier ist im Büro 12.", True),
            (
                "Firma Meyer\nKein Termin am Telefon! Bitte E-Mail: info@meyer.de",
                "Sie machen den Termin am Telefon.",
                False,
            ),
            (
                "Wer hat hier eine Tasche? Farbe: schwarz.\nBitte im Büro fragen.",
                "Die Tasche ist braun.",
                False,
            ),
            ("Hier: Briefmarken und Zeitungen", "Hier sind Briefmarken.", True),
        ],
    ),
    # Modul 3 (Lektionen 7-9): hobbies, times and dates, food and drink.
    3: _set(
        (
            [
                """
                Hallo Jonas,
                hast du am Samstag Zeit? Ich gehe um acht Uhr ins Kino.
                Der Film ist mein Lieblingsfilm! Hast du Lust?
                Am Sonntag kann ich leider nicht, da spiele ich Fußball.
                Lea
                """,
                """
                Hallo zusammen,
                am Freitag um 12 Uhr gibt es Mittagessen im Büro: Suppe,
                Salat und Kuchen. Wasser und Saft haben wir.
                Wer möchte Kaffee? Bitte sagt es Frau Klein.
                Viele Grüße, Tom
                """,
            ],
            [
                ("Lea geht am Samstag ins Kino.", True),
                ("Der Film ist um zehn Uhr.", False),
                ("Lea spielt am Sonntag Fußball.", True),
                ("Das Mittagessen ist am Freitag.", True),
                ("Zum Mittagessen gibt es Fisch.", False),
            ],
        ),
        [
            (
                "Sie möchten am Sonntag frühstücken.",
                "Café Sonne\nFrühstück am Sonntag: 9-14 Uhr",
                "Café Mia\nFrühstück Montag bis Freitag: 7-11 Uhr",
                "a",
            ),
            (
                "Sie möchten am Abend um 20 Uhr schwimmen.",
                "Schwimmbad Nord\nMontag bis Sonntag: 6-18 Uhr",
                "Schwimmbad Mitte\nMontag bis Sonntag: 10-22 Uhr",
                "b",
            ),
            (
                "Sie können nicht tanzen. Wer hilft Ihnen?",
                "Disco Nachtflug\nFreitag und Samstag ab 22 Uhr: Musik und Tanzen",
                "Tanzschule Weiß\nTanzen? Wir helfen! Dienstag, 19 Uhr",
                "b",
            ),
            (
                "Sie essen kein Fleisch und möchten am Abend ins Restaurant.",
                "Restaurant Grün\nGemüse, Salat, Reis und Fisch – kein Fleisch!\n17-23 Uhr",
                "Restaurant Zur Post\nBraten, Schnitzel, Wurst – jeden Abend!",
                "a",
            ),
            (
                "Sie möchten am Montag Kuchen und Brot kaufen.",
                "Café Kranz – Kuchen und Brot\nDienstag bis Sonntag: 7-18 Uhr",
                "Brot & Kuchen Lange\nMontag bis Samstag: 6-19 Uhr",
                "b",
            ),
        ],
        [
            (
                "Kino Astor\nHeute: „Die Reise“ – 17:30 und 20:15 Uhr",
                "Der Film ist am Abend.",
                True,
            ),
            (
                "Museum für Musik\nDienstag bis Sonntag, 10-18 Uhr",
                "Sie können am Montag ins Museum gehen.",
                False,
            ),
            ("Achtung! Hier bitte nicht rauchen.", "Hier können Sie rauchen.", False),
            (
                "Heute:\nKartoffelsuppe 4,50 €\nFisch mit Reis 9,80 €",
                "Die Suppe kostet 4,50 Euro.",
                True,
            ),
            ("Konzert: Samstag, 19 Uhr\nim Theater am Markt", "Das Konzert ist am Sonntag.", False),
        ],
    ),
    # Modul 4 (Lektionen 10-12): transport, the Perfekt, months and celebrations.
    4: _set(
        (
            [
                """
                Hallo Mama,
                ich bin in Hamburg! Ich bin um sechs Uhr aufgestanden und um
                sieben Uhr abgefahren. In Hannover bin ich umgestiegen.
                Am Bahnhof hat mich Ben abgeholt. Morgen rufe ich dich an.
                Bis bald, Lena
                """,
                """
                Hallo Freunde,
                am 14. Mai ist mein Geburtstag und ich mache eine Party!
                Wir feiern am Samstag ab 19 Uhr bei mir zu Hause.
                Bitte bringt etwas zu essen mit. Getränke habe ich.
                Carlos
                """,
            ],
            [
                ("Lena ist in Hannover umgestiegen.", True),
                ("Lena hat Ben am Bahnhof abgeholt.", False),
                ("Lena ruft morgen an.", True),
                ("Die Party ist am Freitag.", False),
                ("Carlos hat die Getränke.", True),
            ],
        ),
        [
            (
                "Sie möchten am Samstag am Morgen von Berlin nach München fahren.",
                "Zug Berlin – München\nSamstag: ab 6:30 Uhr, an 10:45 Uhr",
                "Zug Berlin – München\nSamstag: ab 16:30 Uhr, an 20:45 Uhr",
                "a",
            ),
            (
                "Sie fliegen um sechs Uhr und brauchen um vier Uhr ein Taxi.",
                "Taxi Schnell\nMontag bis Sonntag: 6-22 Uhr",
                "City-Taxi\nTag und Nacht! Telefon 0800 22 33 44",
                "b",
            ),
            (
                "Sie fahren mit dem Zug in den Urlaub und nehmen Ihr Fahrrad mit.",
                "Bus nach Italien\nKoffer bis 20 kg, keine Fahrräder",
                "Zug nach Italien\nFahrräder? Kein Problem!",
                "b",
            ),
            (
                "Sie feiern im Juli Hochzeit. Es kommen 100 Leute.",
                "Restaurant Seeblick\nFeste und Feiern für 120 Personen",
                "Café Lotte\nKleine Feiern für 20 Personen",
                "a",
            ),
            (
                "Ihre Tochter hat im Dezember Geburtstag. Sie feiern zu Hause, mit Musik.",
                "DJ Max\nMusik für Partys – auch bei Ihnen zu Hause!",
                "Disco Blau\nParty jeden Samstag ab 22 Uhr",
                "a",
            ),
        ],
        [
            (
                "Gleis 4\nZug nach Köln – fährt um 10:12 Uhr ab",
                "Der Zug nach Köln fährt um 10:12 Uhr ab.",
                True,
            ),
            (
                "Achtung! Heute keine S-Bahn.\nBitte nehmen Sie den Bus.",
                "Heute fährt die S-Bahn.",
                False,
            ),
            (
                "Haltestelle Marktplatz\nBus 12: Montag bis Freitag",
                "Am Samstag fährt hier der Bus 12.",
                False,
            ),
            (
                "Friseur Locke\nUrlaub: 1. bis 21. August",
                "Der Friseur hat im August Urlaub.",
                True,
            ),
            (
                "Silvester-Party im Hotel Europa\n31. Dezember, ab 20 Uhr",
                "Die Party fängt am Abend an.",
                True,
            ),
        ],
    ),
    # Modul 5 (Lektionen 13-15): directions, flats and houses, the city.
    5: _set(
        (
            [
                """
                Hallo Nina,
                wir haben eine neue Wohnung! Sie hat drei Zimmer, eine Küche,
                ein Bad und einen Balkon. Sie ist im zweiten Stock, aber es gibt
                einen Aufzug. Die Miete ist nicht billig: 950 Euro mit
                Nebenkosten. Besuch uns bald!
                Anna und Max
                """,
                """
                Guten Tag, Herr Yilmaz,
                das Hotel ist in der Nähe vom Bahnhof. Gehen Sie vom Bahnhof
                geradeaus. An der Ampel gehen Sie links. Das Hotel ist neben
                der Post. Es sind nur 500 Meter.
                Ihr Hotel Maritim
                """,
            ],
            [
                ("Die Wohnung hat zwei Zimmer.", False),
                ("Die Wohnung hat einen Balkon.", True),
                ("Die Miete ist 950 Euro.", True),
                ("Herr Yilmaz geht an der Ampel rechts.", False),
                ("Das Hotel ist neben der Post.", True),
            ],
        ),
        [
            (
                "Sie suchen eine Wohnung mit Garten für Ihre Kinder.",
                "3-Zimmer-Wohnung, Altstadt\n4. Stock, mit Balkon",
                "Haus mit Garten, 4 Zimmer\nStadtteil Grünwald",
                "b",
            ),
            (
                "Sie haben ein Auto und brauchen eine Garage.",
                "2 Zimmer, Küche, Bad, mit Garage\n780 €",
                "2 Zimmer, Stadtmitte\nBus und U-Bahn um die Ecke",
                "a",
            ),
            (
                "Sie möchten Bücher lesen, aber nicht kaufen.",
                "Stadtbibliothek\nBücher, Zeitungen und Filme\nMontag bis Samstag: 9-19 Uhr",
                "Bücher-Laden am Markt\nNeue Bücher, günstige Preise",
                "a",
            ),
            (
                "Sie sind mit Ihren Kindern in der Stadt. Die Kinder möchten spielen.",
                "Rathaus\nInformation und Stadtpläne, Montag bis Freitag",
                "Spielplatz im Park am Schloss\nFür Kinder bis 12 Jahre",
                "b",
            ),
            (
                "Sie machen eine Reise und brauchen ein billiges Zimmer für eine Nacht.",
                "Jugendherberge am Hafen\nZimmer ab 25 € die Nacht",
                "Hotel Kaiserhof\nZimmer mit Blick auf den Dom, ab 180 €",
                "a",
            ),
        ],
        [
            (
                "Wohnung frei!\n2 Zimmer, 55 m², ab sofort\nTelefon 0170 445 21 98",
                "Die Wohnung ist sofort frei.",
                True,
            ),
            ("Müll bitte hinter das Haus!", "Der Müll kommt vor das Haus.", False),
            ("Aufzug kaputt!\nBitte die Treppe nehmen.", "Sie können den Aufzug nehmen.", False),
            ("Dom: 300 m geradeaus", "Der Dom ist 300 Meter geradeaus.", True),
            (
                "Markt am Rathaus\nDienstag und Freitag, 7-13 Uhr",
                "Am Freitag gibt es einen Markt.",
                True,
            ),
        ],
    ),
    # Modul 6 (Lektionen 16-18): hotel and appointments, plans, health.
    6: _set(
        (
            [
                """
                Sehr geehrte Damen und Herren,
                ich habe vom 3. bis 5. Mai ein Zimmer in Ihrem Hotel. Leider
                komme ich einen Tag später, am 4. Mai. Ich bleibe bis zum 5. Mai.
                Geht das?
                Mit freundlichen Grüßen
                Julia Brandt
                """,
                """
                Hallo Papa,
                ich bin krank. Ich habe Fieber und Halsschmerzen. Der Arzt sagt,
                ich soll drei Tage im Bett bleiben. Kannst du mir bitte das
                Medikament aus der Apotheke bringen?
                Danke! Tom
                """,
            ],
            [
                ("Frau Brandt kommt am 3. Mai.", False),
                ("Frau Brandt bleibt bis zum 5. Mai.", True),
                ("Tom hat Kopfschmerzen.", False),
                ("Tom soll im Bett bleiben.", True),
                ("Toms Vater soll in die Apotheke gehen.", True),
            ],
        ),
        [
            (
                "Ihre Heizung ist kaputt. Sie brauchen sofort Hilfe.",
                "Techniker Wolf\nHeizung und Klimaanlage – auch am Wochenende, sofort bei Ihnen!",
                "Elektro Wolf\nFernseher, Föhn, Wecker – wir reparieren in 2 Wochen",
                "a",
            ),
            (
                "Sie wollen den Führerschein machen.",
                "Fahrschule Tempo\nAuto und Motorrad – jeden Montag ein neuer Kurs",
                "Werkstatt Kraus\nWir reparieren alle Autos",
                "a",
            ),
            (
                "Sie wollen Gitarre spielen.",
                "Musikladen Ton\nGitarren und Instrumente günstig kaufen!",
                "Musikschule Klang\nGitarrenkurse: Montag und Mittwoch, 18 Uhr",
                "b",
            ),
            (
                "Ihr Sohn hat am Sonntag Zahnschmerzen.",
                "Zahnarzt Dr. Berg\nMontag bis Freitag: 8-18 Uhr",
                "Zahnärzte am Wochenende\nSamstag und Sonntag: 9-20 Uhr",
                "b",
            ),
            (
                "Sie machen eine Geschäftsreise nach Paris und sprechen kein Französisch.",
                "Französisch in Paris\n4 Wochen für Schüler",
                "Französisch für die Arbeit\nSchnell lernen für die Geschäftsreise – Kurse am Abend in Köln",
                "b",
            ),
        ],
        [
            (
                "Praxis Dr. Lehmann\nUrlaub vom 2. bis 13. Juni.\nBitte gehen Sie zu Dr. Klein, Marktstraße 4.",
                "Dr. Lehmann hat im Juni Urlaub.",
                True,
            ),
            (
                "Apotheke am Dom\nSamstag: 8-14 Uhr",
                "Am Samstag können Sie um 16 Uhr in die Apotheke gehen.",
                False,
            ),
            (
                "Achtung, Gäste!\nDas Internet funktioniert heute nicht. Der Techniker kommt morgen.",
                "Das Internet funktioniert heute.",
                False,
            ),
            (
                "Kurs „Englisch für die Reise“\nNeuer Termin: Donnerstag, 18 Uhr (nicht Dienstag)",
                "Der Kurs ist am Donnerstag.",
                True,
            ),
            ("Prüfung: 9:00 Uhr\nBitte pünktlich!", "Die Prüfung ist um neun Uhr.", True),
        ],
    ),
    # Modul 7 (Lektionen 19-21): looks and character, housework, rules.
    7: _set(
        (
            [
                """
                Hallo Clara,
                in der WG ist alles gut, aber Paul ist so faul! Er räumt nie die
                Küche auf und bringt nie den Müll raus. Gestern habe ich alles
                gespült und den Boden gewischt. Ich mache das nicht mehr allein!
                Deine Mia
                """,
                """
                Hallo Mama, hallo Papa,
                ich habe gestern Herrn Fuchs gesehen, meinen Lehrer von früher!
                Früher hatte er lange Haare und keinen Bart. Jetzt hat er einen
                Bart und keine Haare! Er war sehr freundlich und lustig.
                Euer Jan
                """,
            ],
            [
                ("Paul räumt oft die Küche auf.", False),
                ("Mia hat gestern den Boden gewischt.", True),
                ("Mia will den Haushalt nicht allein machen.", True),
                ("Herr Fuchs hatte früher einen Bart.", False),
                ("Herr Fuchs war freundlich.", True),
            ],
        ),
        [
            (
                "Sie suchen ein Zimmer in einer WG. Sie haben einen Hund.",
                "WG-Zimmer frei, 380 €\nKeine Hunde!",
                "Zimmer in netter WG, 400 €\nHunde? Kein Problem!",
                "b",
            ),
            (
                "Sie haben keine Zeit für den Haushalt.",
                "Putzhilfe Blitz\nWir putzen, waschen und bügeln für Sie!",
                "Haushalt-Laden\nSpülmaschinen günstig",
                "a",
            ),
            (
                "Sie fahren mit dem Fahrrad zur Arbeit und brauchen einen Helm.",
                "Motorrad-Laden\nHelme für Motorradfahrer",
                "Rad-Laden Speiche\nFahrräder, Helme, Licht",
                "b",
            ),
            (
                "Sie arbeiten den ganzen Tag. Ihr Hund soll nicht allein zu Hause sein.",
                "Hunde-Hotel Bello\nIhr Hund bleibt bei uns: Montag bis Freitag, 7-19 Uhr",
                "Hundeschule Pfote\nIhr Hund lernt die Regeln",
                "a",
            ),
            (
                "Sie suchen eine ruhige Wohnung. Laute Musik mögen Sie nicht.",
                "Wohnung über der Disco „Bass“\nGünstig!",
                "Ruhige 2-Zimmer-Wohnung am Park\nLeise Nachbarn",
                "b",
            ),
        ],
        [
            ("Hunde bitte an die Leine!", "Hier dürfen Hunde ohne Leine laufen.", False),
            (
                "Fahrrad fahren verboten!\nBitte schieben.",
                "Sie müssen hier Ihr Fahrrad schieben.",
                True,
            ),
            ("Bitte nicht auf die Wiese gehen!", "Sie dürfen auf der Wiese spielen.", False),
            ("Parken nur für das Krankenhaus!", "Hier dürfen alle Leute parken.", False),
            ("Bitte leise sein!\nHier schlafen Kinder.", "Sie müssen hier leise sein.", True),
        ],
    ),
    # Modul 8 (Lektionen 22-24): clothes, weather and holidays, celebrations.
    8: _set(
        (
            [
                """
                Hallo Tina,
                viele Grüße aus Italien! Das Wetter ist super: Die Sonne scheint
                jeden Tag und es ist 30 Grad warm. Gestern war ich am Strand.
                Nur heute regnet es – ein bisschen Pech. Unsere Ferienwohnung
                ist klein, aber sehr schön.
                Bis bald, Sophie
                """,
                """
                Liebe Freunde,
                wir sind umgezogen und machen eine Einweihungsparty! Wann? Am
                Samstag, 12. Oktober, ab 18 Uhr. Wir würden uns sehr freuen!
                Bitte antwortet bis Mittwoch. Ihr müsst nichts mitbringen.
                Laura und Ben
                """,
            ],
            [
                ("Sophie ist in Spanien.", False),
                ("Heute scheint in Italien die Sonne.", False),
                ("Die Ferienwohnung ist klein.", True),
                ("Die Party ist am 12. Oktober.", True),
                ("Die Gäste sollen etwas mitbringen.", False),
            ],
        ),
        [
            (
                "Sie brauchen für eine Hochzeit ein elegantes Kleid.",
                "Mode Chic\nElegante Kleider und Hüte für Feste",
                "Sport-Laden\nT-Shirts, Hosen und Schuhe für den Sport",
                "a",
            ),
            (
                "Sie fahren im Winter in die Berge und brauchen eine warme Jacke.",
                "Sommer-Angebot\nT-Shirts und Röcke: 50 % billiger",
                "Winterjacken, Mützen und warme Schuhe\nJetzt günstiger!",
                "b",
            ),
            (
                "Sie möchten im Urlaub am Meer wohnen.",
                "Ferienwohnung am Strand\nOstsee, für 4 Personen",
                "Ferienwohnung in den Bergen\nBlick auf die Alpen",
                "a",
            ),
            (
                "Sie machen eine Überraschungsparty für Ihre Mutter.",
                "Party-Service Fest\nEssen und Getränke für Ihre Party",
                "Tickets für das Konzert\n„Weihnachten in Wien“",
                "a",
            ),
            (
                "Sie wollen mit einem Wohnmobil in den Urlaub fahren. Sie haben keins.",
                "Camping-Laden\nZelte, Tische und Stühle",
                "Wohnmobil für den Urlaub?\nWir vermieten Wohnmobile ab 90 € am Tag.",
                "b",
            ),
        ],
        [
            ("Heute: Sonne, 25 Grad\nMorgen: Gewitter!", "Morgen ist das Wetter schön.", False),
            ("Alle Pullover 20 % billiger!", "Die Pullover sind jetzt günstiger.", True),
            (
                "Am 24. und 25. Dezember geschlossen.\nFrohe Weihnachten!",
                "Am 25. Dezember können Sie hier einkaufen.",
                False,
            ),
            ("Strand\nBei Sturm nicht schwimmen!", "Sie dürfen bei Sturm nicht schwimmen.", True),
            (
                "Großes Sommerfest am 3. Juli\nFür die ganze Familie!",
                "Das Fest ist im Juli.",
                True,
            ),
        ],
    ),
}
