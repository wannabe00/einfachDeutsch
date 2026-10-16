"""A2 Lesen sets, shaped like the Goethe A2 reading paper: one set per Modul
(Teil 1 a newspaper text, Teil 2 a board or store directory, Teil 3 an e-mail,
Teil 4 people and adverts; 20 questions).

All texts are original (places and people are made up), on the Modul's topics,
and use A1 words plus the A2 words taught up to the Modul's last Lektion.
"""

from ..dsl import lesen_directory, lesen_people, lesen_text


def _set(article, board, email, people) -> list:
    return [
        lesen_text("newspaper article", *article, teil=1),
        lesen_directory(*board, teil=2),
        lesen_text("e-mail", *email, teil=3),
        lesen_people(*people, teil=4),
    ]


LESEN = {
    # Modul 1 (Lektionen 1-3): family and childhood, furniture, holidays in nature.
    1: _set(
        (
            """
            100 Jahre Bäckerei Hoffmann

            Lindau. Die Bäckerei Hoffmann in der Altstadt feiert in diesem Monat
            ihren 100. Geburtstag. Heute verkauft Jonas Hoffmann (34) dort Brot
            und Kuchen – wie früher sein Vater und sein Opa. „Als Kind habe ich
            nach der Schule immer in der Bäckerei geholfen“, erzählt er. „Damals
            fand ich das langweilig. Ich wollte Lehrer werden.“ Nach der Schule
            hat Jonas dann aber doch eine Ausbildung als Bäcker gemacht. Seine
            Schwester Lisa ist Lehrerin und arbeitet nicht in der Bäckerei. Am
            Samstag gibt es ein großes Fest: Alle Kinder bekommen ein Stück Kuchen.
            """,
            [
                (
                    "Die Bäckerei Hoffmann …",
                    "ist 100 Jahre alt.",
                    "ist neu in Lindau.",
                    "verkauft 100 Kuchen am Tag.",
                ),
                (
                    "Als Kind hat Jonas …",
                    "in der Bäckerei geholfen.",
                    "in einer Schule gearbeitet.",
                    "im Garten gespielt.",
                ),
                ("Früher wollte Jonas …", "Lehrer werden.", "Bäcker werden.", "in Lindau bleiben."),
                ("Lisa …", "ist Lehrerin.", "arbeitet in der Bäckerei.", "ist Bäckerin."),
                (
                    "Am Samstag …",
                    "bekommen Kinder Kuchen.",
                    "kostet das Brot nur einen Euro.",
                    "macht die Bäckerei eine Pause.",
                ),
            ],
        ),
        (
            """
            Möbelhaus Wohnfreude
            Untergeschoss: Werkzeug · Kissen und Vorhänge
            Erdgeschoss: Küchen · Lampen · Teppiche · Information · Café
            1. Stock: Sofas und Sessel · Tische und Stühle
            2. Stock: Schlafzimmer: Betten, Schränke, Kommoden · Spiegel
            3. Stock: Kinderzimmer: Betten, Regale, Spiele · Büro: Schreibtische
            """,
            [
                (
                    "Sie brauchen einen neuen Spiegel für Ihr Schlafzimmer.",
                    "2. Stock",
                    "Erdgeschoss",
                    "Untergeschoss",
                ),
                ("Sie möchten einen Kaffee trinken.", "Erdgeschoss", "1. Stock", "3. Stock"),
                ("Ihr Sohn braucht ein Regal für sein Zimmer.", "3. Stock", "2. Stock", "1. Stock"),
                (
                    "Sie suchen Vorhänge für das Wohnzimmer.",
                    "Untergeschoss",
                    "Erdgeschoss",
                    "1. Stock",
                ),
                ("Sie möchten einen Sessel kaufen.", "1. Stock", "2. Stock", "Erdgeschoss"),
            ],
        ),
        (
            """
            Liebe Oma,
            viele Grüße aus dem Schwarzwald! Wir wohnen in einer kleinen Pension
            in einem Dorf. Unser Zimmer ist einfach, aber die Aussicht ist toll:
            Wir sehen den See und die Berge. Gestern sind wir sechs Stunden
            gewandert – Mama war danach sehr müde! Morgen machen wir eine Fahrt
            mit dem Fahrrad um den See. Papa möchte lieber in der Pension bleiben
            und lesen. Die Luft ist hier so gut! Am Samstag fahren wir zurück.
            Wir besuchen dich dann am Sonntag.
            Deine Emma
            """,
            [
                (
                    "Emma und ihre Familie wohnen …",
                    "in einer Pension.",
                    "auf einem Campingplatz.",
                    "in einem Hotel in der Stadt.",
                ),
                (
                    "Vom Zimmer sieht man …",
                    "den See und die Berge.",
                    "nur das Dorf.",
                    "einen Wald.",
                ),
                (
                    "Gestern …",
                    "ist die Familie gewandert.",
                    "war Mama krank.",
                    "hat es geregnet.",
                ),
                (
                    "Morgen möchte Papa …",
                    "in der Pension lesen.",
                    "mit dem Fahrrad fahren.",
                    "wandern.",
                ),
                ("Emma besucht ihre Oma …", "am Sonntag.", "am Samstag.", "morgen."),
            ],
        ),
        (
            {
                "a": "Ferien im Dorf: Bei uns gibt es Katzen, Vögel und viele andere Tiere. Ideal für Familien mit Kindern.",
                "b": "Camping am See: Plätze für Zelte und Wohnmobile direkt am Ufer, günstige Preise.",
                "c": "Umzug? Wir helfen! Wir tragen Ihre Möbel und stellen alles an den richtigen Platz.",
                "d": "Alte Spiele und Puppen gesucht! Ich sammle Spielsachen aus den 70er-Jahren. Tel. 0151 228 40 17",
                "e": "Wohnung renovieren? Team Weiß: Wände, Türen und Decken – schnell und preiswert.",
                "f": "Hotel Seeblick: komfortable Zimmer mit Aussicht, Restaurant und guter Service.",
            },
            [
                ("Herr Kraus zieht nächste Woche um und hat viele schwere Möbel.", "c"),
                (
                    "Familie Schulz macht Urlaub mit zwei kleinen Kindern. Die Kinder lieben Tiere.",
                    "a",
                ),
                ("Frau Berger hat viele Puppen aus ihrer Kindheit und möchte sie verkaufen.", "d"),
                ("Tim und Max haben ein Zelt und wenig Geld.", "b"),
                ("Familie Öztürk hat eine alte Wohnung gekauft. Die Wände sind hässlich.", "e"),
            ],
        ),
    ),
    # Modul 2 (Lektionen 4-6): shopping and quantities, sightseeing, culture.
    2: _set(
        (
            """
            Die Altstadt für Kinder

            Lindenstein. Seit Mai bietet die Stadt Lindenstein eine neue Führung
            an: „Die Altstadt für Kinder“. Der Rundgang beginnt jeden Samstag um
            14 Uhr am Marktplatz und dauert 90 Minuten. Die Kinder hören alte
            Geschichten über die Burg und die Stadtmauer und dürfen auf einen
            Turm klettern. Die Führung kostet für Kinder 3 Euro, Eltern bezahlen
            nichts. „Viele Touristen kommen mit Kindern zu uns“, sagt
            Stadtführerin Petra Lang. „Eine normale Führung ist für Kinder oft
            langweilig.“ Tickets gibt es in der Touristen-Information gegenüber
            vom Rathaus.
            """,
            [
                ("Die neue Führung ist …", "für Kinder.", "für Studenten.", "nur im Winter."),
                ("Der Rundgang beginnt …", "am Marktplatz.", "am Rathaus.", "an der Burg."),
                (
                    "Die Kinder dürfen …",
                    "auf einen Turm klettern.",
                    "in der Burg schlafen.",
                    "im Museum Fotos machen.",
                ),
                ("Eltern …", "bezahlen nichts.", "bezahlen 3 Euro.", "dürfen nicht mitkommen."),
                (
                    "Tickets kauft man …",
                    "in der Touristen-Information.",
                    "im Rathaus.",
                    "bei Petra Lang.",
                ),
            ],
        ),
        (
            """
            Kaufhaus Merkur
            Untergeschoss: Lebensmittel · Obst und Gemüse · Getränke · Metzgerei
            Erdgeschoss: Taschen · Uhren · Brillen · Information
            1. Stock: Mode für Frauen · Schuhe
            2. Stock: Mode für Männer · Sportkleidung
            3. Stock: Für Kinder: Kleidung, Spiele, Puppen · Restaurant mit Aussicht
            """,
            [
                (
                    "Sie brauchen ein Kilo Bananen und zwei Flaschen Wasser.",
                    "Untergeschoss",
                    "Erdgeschoss",
                    "3. Stock",
                ),
                ("Ihr Mann braucht ein Hemd.", "2. Stock", "1. Stock", "Erdgeschoss"),
                (
                    "Sie möchten mittags essen und dabei die Stadt sehen.",
                    "3. Stock",
                    "Untergeschoss",
                    "Erdgeschoss",
                ),
                (
                    "Ihre Tochter hat Geburtstag. Sie möchten eine Puppe kaufen.",
                    "3. Stock",
                    "1. Stock",
                    "2. Stock",
                ),
                (
                    "Ihre Uhr ist kaputt. Sie brauchen eine neue.",
                    "Erdgeschoss",
                    "2. Stock",
                    "Untergeschoss",
                ),
            ],
        ),
        (
            """
            Hallo Sven,
            ich habe zwei Eintrittskarten für das Jazz-Festival am Samstag
            gewonnen! Hast du Lust mitzukommen? Die Band „Blue Notes“ spielt um
            20 Uhr auf der großen Bühne im Stadtpark. Ich war letztes Jahr schon
            da, das Publikum war super! Vorher essen wir bei mir, ich koche.
            Am Eingang treffen wir meine Kollegin Jana, sie kommt auch mit. Bitte
            sag mir bis Donnerstag Bescheid. Das Festival ist draußen – nimm eine
            warme Jacke mit!
            Liebe Grüße
            Mara
            """,
            [
                (
                    "Mara hat die Eintrittskarten …",
                    "gewonnen.",
                    "gekauft.",
                    "von Jana bekommen.",
                ),
                ("Die Band spielt …", "im Stadtpark.", "im Theater.", "in einer Disco."),
                (
                    "Vor dem Festival …",
                    "essen Mara und Sven bei Mara.",
                    "gehen sie ins Restaurant.",
                    "trinken sie Kaffee mit Jana.",
                ),
                (
                    "Sven soll …",
                    "bis Donnerstag antworten.",
                    "Jana anrufen.",
                    "die Karten bezahlen.",
                ),
                (
                    "Mara sagt, Sven soll …",
                    "eine Jacke mitnehmen.",
                    "früh kommen.",
                    "Essen mitbringen.",
                ),
            ],
        ),
        (
            {
                "a": "Theater am Fluss: Heute „Romeo und Julia“ – ein klassisches Theaterstück, 19:30 Uhr.",
                "b": "Wochenmarkt: frisches Obst und Gemüse vom Land, jeden Mittwoch am Rathaus.",
                "c": "Ballettschule Tanzwelt: Kurse für Kinder ab 4 Jahren.",
                "d": "Stadtführung mit Kamera: Wir zeigen Ihnen die besten Plätze für Fotos.",
                "e": "Metzgerei Huber: Wurst und Fleisch – heute Hähnchen im Angebot.",
                "f": "Rock-Festival am See: 3 Tage, 20 Bands, mit Campingplatz.",
            },
            [
                ("Frau Klein liebt klassische Kultur und geht gern ins Theater.", "a"),
                ("Herr Neumann fotografiert gern und möchte die Stadt kennenlernen.", "d"),
                ("Lisa ist sechs Jahre alt und tanzt gern.", "c"),
                ("Familie Roth isst gern frisches Gemüse vom Land.", "b"),
                ("Paul und seine Freunde lieben laute Musik und wollen draußen schlafen.", "f"),
            ],
        ),
    ),
    # Modul 3 (Lektionen 7-9): sport, health, work and companies.
    3: _set(
        (
            """
            Preis für Fahrräder aus Ulm

            Ulm. Das Unternehmen „Radwerk“ aus Ulm hat auf der Fahrrad-Messe in
            Frankfurt einen Preis gewonnen: Sein neues Modell „City 3“ ist das
            beste Fahrrad für die Stadt. Die kleine Firma hat 45 Mitarbeiter und
            stellt jedes Jahr 8.000 Fahrräder her. 60 Prozent gehen in den Export,
            vor allem nach Österreich und in die Schweiz. „Wir legen Wert auf
            Qualität“, sagt Chefin Anja Weber. „Unsere Fahrräder sind teurer als
            andere, aber sie sind sehr zuverlässig.“ Nächstes Jahr will Radwerk
            eine zweite Fabrik bauen und 20 neue Mitarbeiter suchen.
            """,
            [
                (
                    "„Radwerk“ hat …",
                    "einen Preis gewonnen.",
                    "eine Messe in Ulm gemacht.",
                    "eine Firma in Frankfurt gekauft.",
                ),
                (
                    "Das Modell „City 3“ ist …",
                    "ein Fahrrad für die Stadt.",
                    "ein Motorrad.",
                    "ein Fahrrad für die Berge.",
                ),
                (
                    "Die Firma …",
                    "hat 45 Mitarbeiter.",
                    "stellt 45.000 Fahrräder her.",
                    "hat 8.000 Mitarbeiter.",
                ),
                (
                    "Die meisten Fahrräder …",
                    "gehen ins Ausland.",
                    "sind billig.",
                    "bleiben in Ulm.",
                ),
                (
                    "Nächstes Jahr …",
                    "möchte Radwerk mehr Mitarbeiter haben.",
                    "zieht die Firma nach Österreich.",
                    "gibt es kein neues Modell.",
                ),
            ],
        ),
        (
            """
            Ärztehaus am Park
            Erdgeschoss: Apotheke · Fitnessstudio „Fit & Gesund“
            1. Stock: Dr. Wagner – Hausarzt · Dr. Sommer – Kinderärztin
            2. Stock: Dr. Yilmaz – Hautarzt und Allergien · Dr. Lenz – Zahnarzt
            3. Stock: Dr. Fischer – Herz und Blutdruck · Dr. Ott – Augenärztin
            """,
            [
                ("Ihr Sohn (5) hat Fieber und Husten.", "1. Stock", "2. Stock", "3. Stock"),
                (
                    "Sie haben im Frühling oft eine Allergie und Ihre Haut ist rot.",
                    "2. Stock",
                    "1. Stock",
                    "Erdgeschoss",
                ),
                ("Ihr Blutdruck ist zu hoch.", "3. Stock", "1. Stock", "2. Stock"),
                ("Sie möchten mehr Krafttraining machen.", "Erdgeschoss", "3. Stock", "1. Stock"),
                (
                    "Sie sehen nicht mehr gut und brauchen vielleicht eine Brille.",
                    "3. Stock",
                    "2. Stock",
                    "Erdgeschoss",
                ),
            ],
        ),
        (
            """
            Hallo Ben,
            danke für deine Nachricht! Toll, dass du mehr Sport machen willst. Ich
            gehe seit einem Jahr zweimal pro Woche ins Fitnessstudio „Kraftwerk“,
            montags und donnerstags nach der Arbeit. Das Training ist anstrengend,
            aber ich fühle mich viel besser. Der Trainer dort ist sehr nett und
            hilft allen. Am Anfang solltest du langsam trainieren. Joggen ist auch
            gut, aber beim Joggen tut mir das Knie weh. Wir könnten am Samstag
            zusammen schwimmen gehen – das Schwimmbad ist neben dem Studio. Was
            hältst du davon?
            Viele Grüße
            Felix
            """,
            [
                (
                    "Felix geht … ins Fitnessstudio.",
                    "zweimal pro Woche",
                    "jeden Tag",
                    "einmal im Monat",
                ),
                ("Felix trainiert …", "nach der Arbeit.", "am Morgen.", "am Wochenende."),
                ("Der Trainer …", "ist nett.", "ist sehr teuer.", "hat wenig Zeit."),
                (
                    "Beim Joggen …",
                    "tut Felix das Knie weh.",
                    "ist Felix schnell müde.",
                    "trifft Felix Ben.",
                ),
                (
                    "Felix möchte am Samstag …",
                    "mit Ben schwimmen.",
                    "ins Fitnessstudio gehen.",
                    "joggen.",
                ),
            ],
        ),
        (
            {
                "a": "Fußballverein SV Grün sucht Spieler für die Mannschaft. Training dienstags und freitags.",
                "b": "Yoga am Morgen: Entspannen vor der Arbeit, 7-8 Uhr im Park.",
                "c": "Firma Techno sucht Mitarbeiter für die Produktion – auch ohne Erfahrung.",
                "d": "Ski-Reise in die Alpen: eine Woche mit Skikurs.",
                "e": "Bewegung gegen Rückenschmerzen: montags 18 Uhr in der Sporthalle.",
                "f": "Fitnessstudio Max: Krafttraining mit Trainer – Tag und Nacht offen.",
            },
            [
                ("Herr Braun sitzt den ganzen Tag im Büro. Sein Rücken tut oft weh.", "e"),
                ("Sarah möchte im Winter Ski fahren lernen.", "d"),
                ("Jan spielt gern Fußball und sucht eine Mannschaft.", "a"),
                ("Frau Demir sucht Arbeit. Sie hat noch keine Erfahrung.", "c"),
                ("Herr Koch arbeitet abends lange und möchte um 3 Uhr nachts trainieren.", "f"),
            ],
        ),
    ),
    # Modul 4 (Lektionen 10-12): restaurant, family news and feelings, food.
    4: _set(
        (
            """
            Immer mehr Menschen essen kein Fleisch

            Immer mehr Menschen in Deutschland essen wenig oder kein Fleisch. Vor
            zehn Jahren haben nur drei Prozent vegetarisch gegessen, heute sind
            es fast zehn Prozent. Besonders junge Leute zwischen 18 und 29 Jahren
            essen gern vegetarisch oder vegan. Viele sagen, dass sie gesünder
            leben möchten. Andere essen kein Fleisch, weil sie die Tiere lieben.
            Auch viele Restaurants haben jetzt mehr vegetarische Gerichte auf der
            Speisekarte. Koch Martin Feld aus Köln sagt: „Früher wollten die
            Gäste immer Fleisch. Heute bestellt jeder dritte Gast ein Gericht
            ohne Fleisch.“
            """,
            [
                (
                    "Heute essen in Deutschland … vegetarisch.",
                    "fast zehn Prozent der Menschen",
                    "drei Prozent der Menschen",
                    "die meisten Menschen",
                ),
                ("Besonders … essen vegetarisch.", "junge Leute", "alte Leute", "Köche"),
                (
                    "Viele essen kein Fleisch, weil …",
                    "sie gesünder leben möchten.",
                    "Fleisch zu teuer ist.",
                    "es im Restaurant kein Fleisch gibt.",
                ),
                (
                    "Viele Restaurants …",
                    "haben mehr Gerichte ohne Fleisch.",
                    "verkaufen kein Fleisch mehr.",
                    "kochen nur vegan.",
                ),
                (
                    "Martin Feld sagt: Heute …",
                    "bestellt jeder dritte Gast kein Fleisch.",
                    "wollen alle Gäste Fleisch.",
                    "kochen die Gäste selbst.",
                ),
            ],
        ),
        (
            """
            Einkaufszentrum Rheinpark – Essen und Trinken
            Erdgeschoss: Supermarkt Frischmarkt · Bäckerei Korn · Eiscafé Venezia
            1. Stock: Restaurant Athen (griechische Küche) · Pizzeria Roma
            2. Stock: Vegetarisches Restaurant „Grünkern“ · Spielplatz für Kinder
            3. Stock: Kochschule „Topf & Pfanne“ · Alles für die Küche: Töpfe, Pfannen, Messer, Teller
            """,
            [
                ("Sie möchten ein Eis essen.", "Erdgeschoss", "1. Stock", "2. Stock"),
                (
                    "Sie essen kein Fleisch und möchten zu Mittag essen.",
                    "2. Stock",
                    "1. Stock",
                    "Erdgeschoss",
                ),
                (
                    "Sie möchten lernen, wie man Nudeln selbst macht.",
                    "3. Stock",
                    "2. Stock",
                    "1. Stock",
                ),
                (
                    "Ihre Pfanne ist alt. Sie brauchen eine neue.",
                    "3. Stock",
                    "Erdgeschoss",
                    "2. Stock",
                ),
                ("Sie möchten eine Pizza essen.", "1. Stock", "2. Stock", "3. Stock"),
            ],
        ),
        (
            """
            Liebe Tante Inge,
            ich habe tolle Nachrichten: Kemal und ich haben uns verlobt! Er hat
            mich am Wochenende in Paris gefragt, in einem Restaurant mit Blick
            auf den Eiffelturm. Ich war so überrascht und habe sofort ja gesagt.
            Die Hochzeit soll im nächsten Sommer sein, wahrscheinlich im Juli.
            Wir möchten in einem kleinen Hotel am See feiern. Mama freut sich
            sehr, aber Papa ist ein bisschen nervös, weil er auf der Feier etwas
            sagen muss. Ich weiß noch nicht, ob Kemals Familie aus der Türkei
            kommen kann. Ich hoffe es sehr!
            Ich freue mich auf dich!
            Deine Selin
            """,
            [
                (
                    "Selin und Kemal …",
                    "haben sich verlobt.",
                    "haben geheiratet.",
                    "haben sich getrennt.",
                ),
                ("Kemal hat Selin … gefragt.", "in Paris", "im Hotel am See", "zu Hause"),
                (
                    "Die Hochzeit ist …",
                    "wahrscheinlich im Juli.",
                    "am Wochenende.",
                    "im Winter.",
                ),
                (
                    "Selins Vater ist nervös, weil …",
                    "er auf der Feier etwas sagen muss.",
                    "er nicht kommen kann.",
                    "die Hochzeit in Paris ist.",
                ),
                (
                    "Selin weiß noch nicht, …",
                    "ob Kemals Familie kommen kann.",
                    "wo sie feiern.",
                    "ob ihre Mutter sich freut.",
                ),
            ],
        ),
        (
            {
                "a": "Kochkurs: Gesund und schnell kochen – Rezepte für die ganze Woche.",
                "b": "Restaurant Seeterrasse: Feiern Sie Ihre Hochzeit bei uns! Für bis zu 80 Gäste.",
                "c": "Diät-Gruppe: Gemeinsam abnehmen – jeden Dienstag, 19 Uhr.",
                "d": "Café Süß: Kuchen für jedes Fest – Geburt, Verlobung, Hochzeit.",
                "e": "Laden Natur: regionales Obst und Gemüse, vegane Produkte.",
                "f": "Imbiss Schnell: Pommes, Burger und Cola – bis 2 Uhr nachts.",
            },
            [
                ("Frau Weber möchte fünf Kilo abnehmen, aber nicht allein.", "c"),
                ("Tom isst vegan und kauft gern Gemüse aus der Region.", "e"),
                ("Herr und Frau Lang feiern ihre Hochzeit mit 60 Gästen.", "b"),
                ("Anna möchte gesund essen, aber das Kochen dauert für sie immer zu lange.", "a"),
                ("Max kommt um 1 Uhr nachts aus der Disco und hat Hunger.", "f"),
            ],
        ),
    ),
    # Modul 5 (Lektionen 13-15): learning languages, the post, media.
    5: _set(
        (
            """
            Fernsehen, Internet oder Zeitung?

            Wie informieren sich die Menschen? Das hat ein Radiosender aus Hamburg
            gefragt, und 1.000 Menschen haben geantwortet. Die meisten (45 Prozent)
            sehen die Nachrichten am Abend im Fernsehen. 30 Prozent lesen die
            Nachrichten im Internet, besonders auf dem Handy. Nur 15 Prozent lesen
            noch eine Zeitung. Junge Menschen sehen Serien und Sendungen fast nur
            in der Mediathek. „Ich habe gar keinen Fernseher“, sagt Lea (22).
            „Ich sehe alles auf dem Laptop – und ohne Werbung!“ Ältere Menschen
            hören dagegen morgens oft Radio.
            """,
            [
                (
                    "Die meisten Menschen …",
                    "sehen die Nachrichten im Fernsehen.",
                    "lesen eine Zeitung.",
                    "hören Radio.",
                ),
                (
                    "30 Prozent …",
                    "lesen die Nachrichten im Internet.",
                    "haben keinen Fernseher.",
                    "sehen Serien.",
                ),
                (
                    "Junge Menschen sehen Serien oft …",
                    "in der Mediathek.",
                    "im Kino.",
                    "bei Freunden.",
                ),
                (
                    "Lea …",
                    "hat keinen Fernseher.",
                    "sieht gern Werbung.",
                    "liest jeden Tag Zeitung.",
                ),
                (
                    "Ältere Menschen …",
                    "hören morgens oft Radio.",
                    "sehen keine Nachrichten.",
                    "laden Serien herunter.",
                ),
            ],
        ),
        (
            """
            Sprachschule Lingua
            Erdgeschoss: Anmeldung und Information · Bibliothek · Café
            1. Stock: Deutschkurse A1 und A2 · Prüfungen
            2. Stock: Deutschkurse B1 und B2 · Training für die Aussprache
            3. Stock: Englisch · Spanisch · Französisch · Computerraum
            """,
            [
                (
                    "Sie möchten sich für einen Deutschkurs anmelden.",
                    "Erdgeschoss",
                    "1. Stock",
                    "2. Stock",
                ),
                (
                    "Sie lernen seit drei Monaten Deutsch und sind im A1-Kurs.",
                    "1. Stock",
                    "2. Stock",
                    "3. Stock",
                ),
                (
                    "Sie möchten in Ruhe Bücher und Wörterbücher lesen.",
                    "Erdgeschoss",
                    "3. Stock",
                    "1. Stock",
                ),
                (
                    "Ihre Aussprache ist nicht gut. Sie möchten üben.",
                    "2. Stock",
                    "1. Stock",
                    "Erdgeschoss",
                ),
                ("Ihre Tochter möchte Spanisch lernen.", "3. Stock", "2. Stock", "Erdgeschoss"),
            ],
        ),
        (
            """
            Hallo Marco,
            vielen Dank für das Päckchen! Es ist gestern angekommen. Leider war ich
            nicht zu Hause, aber meine Nachbarin hat es für mich genommen. Die
            Bücher sind toll, danke! Aber der Pullover ist mir leider zu klein.
            Kann ich ihn zurückschicken? Im Karton war eine Rechnung, aber keine
            Adresse vom Geschäft. Kannst du sie mir schicken? Und noch etwas: Mein
            Handy ist kaputt. Ruf mich bitte am Abend zu Hause an, Telefon
            040 22 81 90.
            Liebe Grüße
            Hanna
            """,
            [
                (
                    "Das Päckchen …",
                    "hat die Nachbarin genommen.",
                    "ist noch nicht angekommen.",
                    "war kaputt.",
                ),
                ("Hanna findet die Bücher …", "toll.", "zu schwierig.", "langweilig."),
                (
                    "Der Pullover …",
                    "ist zu klein.",
                    "hat die falsche Farbe.",
                    "war nicht im Päckchen.",
                ),
                (
                    "Hanna braucht …",
                    "die Adresse vom Geschäft.",
                    "eine neue Rechnung.",
                    "einen Karton.",
                ),
                (
                    "Marco soll Hanna …",
                    "am Abend zu Hause anrufen.",
                    "eine E-Mail schreiben.",
                    "auf dem Handy anrufen.",
                ),
            ],
        ),
        (
            {
                "a": "Deutsch am Wochenende: Kurs am Samstag und Sonntag, 9-15 Uhr.",
                "b": "Tandem: Ich lerne Deutsch und spreche Italienisch. Wer möchte mit mir üben?",
                "c": "Paket-Service Express: Ihr Paket ist morgen da – in ganz Europa.",
                "d": "Krimi im Radio: Jeden Freitag um 21 Uhr eine spannende Geschichte.",
                "e": "Hilfe bei der Grammatik: Deutschlehrerin korrigiert Ihre Briefe und Texte.",
                "f": "Computerkurs für Leute ab 60: Videos herunterladen und hochladen.",
            },
            [
                (
                    "Herr Rossi kommt aus Italien und möchte mit einer Deutschen Deutsch sprechen.",
                    "b",
                ),
                (
                    "Frau Kim arbeitet von Montag bis Freitag und möchte schnell Deutsch lernen.",
                    "a",
                ),
                (
                    "Leon schickt ein Geschenk an seine Oma in Spanien. Es soll schnell da sein.",
                    "c",
                ),
                (
                    "Frau Peters schreibt einen wichtigen Brief auf Deutsch und macht oft Fehler.",
                    "e",
                ),
                ("Herr Wolf (65) möchte lernen, wie man Videos ins Internet stellt.", "f"),
            ],
        ),
    ),
    # Modul 6 (Lektionen 16-18): the hotel, travel and traffic, weather.
    6: _set(
        (
            """
            Stau und Hitze am ersten Ferientag

            München. Am ersten Tag der Sommerferien hatten viele Autofahrer in
            Bayern Pech: Auf der Autobahn von München nach Salzburg gab es am
            Samstag 40 Kilometer Stau. Viele Familien standen bei 35 Grad mehr als
            fünf Stunden im Auto. Auch an den Tankstellen mussten die Leute lange
            warten. Die Polizei sagt: „Fahren Sie lieber in der Nacht oder am
            Dienstag oder Mittwoch.“ Für Sonntag sagt die Wettervorhersage Gewitter
            und Regen. Dann wird es kühler, aber die Straßen sind auch gefährlich.
            """,
            [
                ("Der Stau war …", "am Samstag.", "am Dienstag.", "in der Nacht."),
                (
                    "Auf der Autobahn …",
                    "gab es 40 Kilometer Stau.",
                    "war es 40 Grad heiß.",
                    "fuhren keine Autos.",
                ),
                (
                    "Die Familien …",
                    "standen lange im Auto.",
                    "sind zu Hause geblieben.",
                    "haben im Hotel übernachtet.",
                ),
                (
                    "Die Polizei sagt, man soll …",
                    "in der Nacht fahren.",
                    "am Samstag fahren.",
                    "mit dem Zug fahren.",
                ),
                (
                    "Am Sonntag …",
                    "soll es regnen.",
                    "ist es 35 Grad warm.",
                    "gibt es keinen Stau.",
                ),
            ],
        ),
        (
            """
            Hotel Bergblick – Information
            Untergeschoss: Sauna · Fitnessraum · Garage
            Erdgeschoss: Rezeption · Frühstücksraum (7-10 Uhr) · Restaurant
            1. Stock: Konferenzraum „Alpen“ · Zimmer 101-120
            2. Stock: Zimmer 201-230 · Spielzimmer für Kinder
            """,
            [
                (
                    "Sie möchten nach dem Wandern in die Sauna.",
                    "Untergeschoss",
                    "Erdgeschoss",
                    "2. Stock",
                ),
                (
                    "Sie haben eine Sitzung mit Kollegen.",
                    "1. Stock",
                    "Erdgeschoss",
                    "Untergeschoss",
                ),
                ("Sie möchten um 8 Uhr frühstücken.", "Erdgeschoss", "1. Stock", "Untergeschoss"),
                ("Ihr Zimmer hat die Nummer 215.", "2. Stock", "1. Stock", "Erdgeschoss"),
                ("Sie suchen Ihr Auto.", "Untergeschoss", "Erdgeschoss", "1. Stock"),
            ],
        ),
        (
            """
            Sehr geehrte Damen und Herren,
            vom 10. bis 14. März war ich Gast in Ihrem Hotel. Ich hatte ein
            Nichtraucherzimmer mit Halbpension gebucht. Leider war das Zimmer
            nicht ruhig: Es lag direkt über dem Parkplatz, und schon um 5 Uhr
            morgens kamen die ersten Autos. Das WLAN hat nur in der Empfangshalle
            funktioniert. Das Frühstück war sehr gut, aber am Abend war das Essen
            oft kalt. An der Rezeption habe ich zweimal gefragt, ob ich ein
            anderes Zimmer bekommen kann, aber das Hotel war ausgebucht. Könnten
            Sie mir bitte 50 Euro zurückzahlen?
            Mit freundlichen Grüßen
            Karin Vogt
            """,
            [
                ("Frau Vogt hatte … gebucht.", "Halbpension", "Vollpension", "nur Frühstück"),
                (
                    "Das Zimmer war laut, weil …",
                    "es über dem Parkplatz lag.",
                    "die Nachbarn laut waren.",
                    "es neben der Sauna lag.",
                ),
                (
                    "Das WLAN …",
                    "hat nur in der Empfangshalle funktioniert.",
                    "hat im Zimmer gut funktioniert.",
                    "hat Geld gekostet.",
                ),
                (
                    "Frau Vogt fand …",
                    "das Frühstück gut.",
                    "das Abendessen gut.",
                    "die Rezeption unfreundlich.",
                ),
                (
                    "Frau Vogt möchte …",
                    "50 Euro zurück.",
                    "im Mai ein neues Zimmer.",
                    "mit dem Chef sprechen.",
                ),
            ],
        ),
        (
            {
                "a": "Fähre zur Insel: jede Stunde, auch mit dem Auto.",
                "b": "Werkstatt Rad & Reifen: Hilfe bei der Panne – 24 Stunden am Tag.",
                "c": "Rucksack-Reisen: Wandern an der Küste, Übernachtung im Zelt.",
                "d": "Hotel am Flughafen: Einzelzimmer ab 69 €, Parkplatz inklusive.",
                "e": "Wochenende im Wellnesshotel: Sauna, Massage und viel Ruhe.",
                "f": "Wetterdienst Sonne: die Wettervorhersage für Ihren Urlaub am Telefon.",
            },
            [
                ("Herr Kurz fliegt morgen um 6 Uhr und braucht heute ein Zimmer.", "d"),
                ("Familie Haas möchte mit ihrem Auto auf eine Insel fahren.", "a"),
                ("Frau Nowak hatte auf der Autobahn eine Reifenpanne.", "b"),
                ("Jonas und Lea wollen am Meer wandern und draußen schlafen.", "c"),
                ("Herr Jung hat viel Stress und möchte sich am Wochenende erholen.", "e"),
            ],
        ),
    ),
    # Modul 7 (Lektionen 19-21): culture, books and the press, offices and crime.
    7: _set(
        (
            """
            Einbruch im Stadtmuseum

            Sonnfeld. In der Nacht von Freitag auf Samstag sind Täter in das
            Stadtmuseum eingebrochen. Sie haben drei alte Bilder und eine goldene
            Uhr gestohlen. Ein Zeuge hat um 2 Uhr zwei Männer mit einem weißen
            Auto gesehen und die Polizei angerufen. Aber als die Polizei kam,
            waren die Täter schon weg. Das Museum bleibt bis Mittwoch geschlossen.
            Die Polizei sucht noch mehr Zeugen: „Haben Sie in der Nacht etwas
            gesehen? Bitte melden Sie sich!“
            """,
            [
                (
                    "Die Täter sind … ins Museum eingebrochen.",
                    "in der Nacht",
                    "am Mittwoch",
                    "am Nachmittag",
                ),
                ("Sie haben … gestohlen.", "Bilder und eine Uhr", "viel Geld", "ein Auto"),
                (
                    "Der Zeuge …",
                    "hat die Polizei angerufen.",
                    "arbeitet im Museum.",
                    "hat ein weißes Auto.",
                ),
                (
                    "Das Museum …",
                    "ist bis Mittwoch geschlossen.",
                    "ist schon wieder offen.",
                    "zeigt neue Bilder.",
                ),
                (
                    "Die Polizei …",
                    "sucht noch mehr Zeugen.",
                    "hat die Täter gefunden.",
                    "hat die Bilder zurück.",
                ),
            ],
        ),
        (
            """
            Rathaus Neustadt
            Erdgeschoss: Information · Bürgeramt: Ausweis, Reisepass, neue Adresse melden
            1. Stock: Ausländerbehörde: Visum, Aufenthaltsgenehmigung
            2. Stock: Fundbüro · Standesamt (Hochzeiten)
            3. Stock: Stadtbibliothek · Veranstaltungskalender und Eintrittskarten
            """,
            [
                (
                    "Ihr Reisepass ist alt. Sie brauchen einen neuen.",
                    "Erdgeschoss",
                    "1. Stock",
                    "2. Stock",
                ),
                (
                    "Sie haben Ihre Geldbörse im Bus verloren.",
                    "2. Stock",
                    "Erdgeschoss",
                    "3. Stock",
                ),
                (
                    "Sie kommen aus Brasilien und brauchen eine Aufenthaltsgenehmigung.",
                    "1. Stock",
                    "Erdgeschoss",
                    "2. Stock",
                ),
                (
                    "Sie möchten Eintrittskarten für eine Lesung kaufen.",
                    "3. Stock",
                    "2. Stock",
                    "Erdgeschoss",
                ),
                ("Sie wollen heiraten.", "2. Stock", "1. Stock", "3. Stock"),
            ],
        ),
        (
            """
            Liebe Paula,
            du hast mich gefragt, welches Buch ich dir empfehlen kann. Ich lese
            gerade einen tollen Roman: „Das Haus am Fluss“ von Marie Lenz. Er
            erzählt die Geschichte von drei Schwestern in einem kleinen Dorf. Am
            Anfang ist er ein bisschen langsam, aber nach dem dritten Kapitel
            konnte ich nicht mehr aufhören! Als Kind durfte ich abends nicht lange
            lesen. Ich habe dann oft unter der Decke weitergelesen. Am Freitag
            gibt es in der Buchhandlung Seitenwind eine Lesung mit Marie Lenz. Der
            Eintritt kostet 8 Euro. Willst du mitkommen?
            Viele Grüße
            Ines
            """,
            [
                (
                    "Der Roman erzählt von …",
                    "drei Schwestern.",
                    "einem Fluss in der Stadt.",
                    "einer Buchhandlung.",
                ),
                (
                    "Ines findet den Anfang …",
                    "ein bisschen langsam.",
                    "sehr spannend.",
                    "zu schwierig.",
                ),
                (
                    "Als Kind …",
                    "durfte Ines abends nicht lange lesen.",
                    "hat Ines keine Bücher gelesen.",
                    "hat Ines Gedichte geschrieben.",
                ),
                ("Die Lesung ist …", "in einer Buchhandlung.", "in der Bibliothek.", "im Theater."),
                ("Die Lesung …", "kostet 8 Euro.", "ist am Samstag.", "ist ausverkauft."),
            ],
        ),
        (
            {
                "a": "Zirkus Sonne: Clowns und Artisten für die ganze Familie.",
                "b": "Kabarett im Keller: Politik zum Lachen – jeden Donnerstag.",
                "c": "Alte Bücher: Romane, Comics und Kinderbücher – jedes Buch 1 Euro.",
                "d": "Gedichte und Geschichten schreiben: Kurs mit der Autorin Eva Brandt.",
                "e": "Versicherung Sicher: Hilfe bei Einbruch und Diebstahl.",
                "f": "Märchen in der Bibliothek: Wir lesen Kindern vor, samstags um 10 Uhr.",
            },
            [
                ("Herr Polat möchte selbst Gedichte schreiben.", "d"),
                ("Frau Huber sucht günstige Comics für ihren Sohn.", "c"),
                (
                    "Im Haus von Frau Grafs Nachbarn gab es einen Einbruch. Jetzt hat sie Angst.",
                    "e",
                ),
                (
                    "Opa Karl möchte mit seinen Enkeln (4 und 6) am Wochenende eine Geschichte hören.",
                    "f",
                ),
                ("Lena lacht gern und interessiert sich für Politik.", "b"),
            ],
        ),
    ),
    # Modul 8 (Lektionen 22-24): mobility and the environment, jobs, living abroad.
    8: _set(
        (
            """
            Ein Auto für viele

            Freiburg. Immer mehr Menschen in Freiburg haben kein eigenes Auto mehr.
            Sie teilen ein Auto mit anderen: Seit 2015 hat der Verein „Stadtauto“
            12.000 neue Mitglieder bekommen. Die Mitglieder buchen ein Auto im
            Internet oder mit dem Handy. Eine Stunde kostet 3 Euro, dazu kommen
            25 Cent pro Kilometer. Benzin, Steuer und Versicherung muss man nicht
            bezahlen. „Seit ich meinen Wagen verkauft habe, habe ich jeden Monat
            200 Euro mehr“, sagt Mitglied Tobias Mann (41). Viele Autos sind
            Elektroautos – das ist gut für die Umwelt.
            """,
            [
                (
                    "Viele Menschen in Freiburg …",
                    "haben kein eigenes Auto mehr.",
                    "kaufen ein Elektroauto.",
                    "fahren nur Fahrrad.",
                ),
                (
                    "Ein Auto bucht man …",
                    "im Internet oder mit dem Handy.",
                    "im Büro vom Verein.",
                    "an der Tankstelle.",
                ),
                ("Für eine Stunde bezahlt man …", "3 Euro.", "25 Cent.", "200 Euro."),
                (
                    "Das Benzin …",
                    "müssen die Mitglieder nicht bezahlen.",
                    "kostet 25 Cent pro Kilometer.",
                    "ist sehr teuer.",
                ),
                (
                    "Tobias Mann …",
                    "hat seinen Wagen verkauft.",
                    "arbeitet beim Verein.",
                    "hat ein Elektroauto gekauft.",
                ),
            ],
        ),
        (
            """
            Ausbildungsmesse Kassel
            Erdgeschoss: Information · Lebenslauf-Check: Wir lesen und korrigieren Ihre Bewerbung
            1. Stock: Handwerk: Bäcker, Koch, Friseur · Berufe mit Autos und Motoren
            2. Stock: Gesundheit: Ausbildung im Krankenhaus und in der Arztpraxis · Büro und Verwaltung
            3. Stock: Studium an der Universität · Arbeiten und Studieren im Ausland
            """,
            [
                (
                    "Jemand soll Ihren Lebenslauf lesen und korrigieren.",
                    "Erdgeschoss",
                    "2. Stock",
                    "3. Stock",
                ),
                ("Sie möchten Koch werden.", "1. Stock", "2. Stock", "Erdgeschoss"),
                (
                    "Sie möchten nach der Schule ein Jahr in Kanada arbeiten.",
                    "3. Stock",
                    "1. Stock",
                    "Erdgeschoss",
                ),
                (
                    "Sie interessieren sich für eine Ausbildung im Krankenhaus.",
                    "2. Stock",
                    "1. Stock",
                    "3. Stock",
                ),
                ("Sie reparieren gern Motoren.", "1. Stock", "2. Stock", "3. Stock"),
            ],
        ),
        (
            """
            Hallo Jana,
            jetzt bin ich schon drei Monate in Valencia! Am Anfang war es
            schwierig: Ich habe wenig Spanisch verstanden und hatte oft Heimweh.
            Meine Gastfamilie war aber sehr nett und hat mir viel geholfen. Jetzt
            fühle ich mich hier wohl. Mein Tagesablauf ist ganz anders als in
            Deutschland: Wir essen erst um 22 Uhr zu Abend! Im Büro arbeite ich an
            einem großen Auftrag für einen Kunden aus Mexiko. Nach Feierabend gehe
            ich oft mit Kollegen an den Strand. Im Juni komme ich zurück. Dann
            erzähle ich dir alles!
            Liebe Grüße
            Moritz
            """,
            [
                (
                    "Moritz ist … in Valencia.",
                    "seit drei Monaten",
                    "seit einem Jahr",
                    "seit einer Woche",
                ),
                (
                    "Am Anfang …",
                    "hatte Moritz Heimweh.",
                    "hat Moritz gut Spanisch gesprochen.",
                    "war die Gastfamilie unfreundlich.",
                ),
                (
                    "In Spanien isst Moritz …",
                    "spät zu Abend.",
                    "um 18 Uhr zu Abend.",
                    "nur mittags.",
                ),
                (
                    "Nach der Arbeit …",
                    "geht Moritz oft an den Strand.",
                    "lernt Moritz Spanisch.",
                    "kocht Moritz für die Gastfamilie.",
                ),
                ("Moritz kommt … zurück.", "im Juni", "im März", "nicht mehr"),
            ],
        ),
        (
            {
                "a": "Ausbildung zum Koch oder zur Köchin im Hotel Adler. Start: 1. September.",
                "b": "Job für Studenten: 10 Stunden pro Woche im Büro, 13 € pro Stunde.",
                "c": "Fahrrad-Werkstatt: Wir reparieren Ihr Rad – schnell und umweltfreundlich.",
                "d": "Weiterbildung am Abend: Computer im Büro – Kurse ab 18 Uhr.",
                "e": "Au-pair in Frankreich: ein Jahr in einer Gastfamilie leben.",
                "f": "Elektroauto zu verkaufen: drei Jahre alt, wenig Kilometer.",
            },
            [
                ("Sophie ist 19. Sie möchte ein Jahr im Ausland bei einer Familie wohnen.", "e"),
                (
                    "Herr Arslan arbeitet von 8 bis 17 Uhr und möchte mehr über Computer lernen.",
                    "d",
                ),
                ("Mia studiert und braucht ein bisschen Geld.", "b"),
                ("Familie Brenner möchte ein umweltfreundliches Auto kaufen.", "f"),
                ("Ali hat die Schule fertig und möchte in einer Küche arbeiten.", "a"),
            ],
        ),
    ),
}
