"""B1 Lesen sets: one per Modul, in the same four-Teil shape as A2 (Teil 1 a
newspaper text, Teil 2 an information board, Teil 3 an e-mail, Teil 4 people
and adverts; 20 questions), with longer B1 texts: subordinate clauses, the
Präteritum and more detail.

All texts are original (places and people are made up), on the Modul's topics.
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
    # Modul 1 (Lektionen 1-3): friendship, internships, housing.
    1: _set(
        (
            """
            Ein Hausmeister mit Herz

            Bremen. Seit 22 Jahren ist Georg Brandt (61) Hausmeister in einer großen
            Wohnanlage im Stadtteil Findorff. Er repariert Heizungen, wechselt Lampen
            und kümmert sich um den Innenhof. Doch für viele Bewohner ist er viel mehr:
            „Herr Brandt ist der Mensch, dem ich meinen Schlüssel gebe, wenn ich verreise“,
            sagt eine ältere Mieterin. Als im letzten Winter eine Familie aus Syrien
            einzog, half er ihr bei den Formularen und zeigte den Kindern den Weg zur
            Schule. Im Sommer organisiert er jedes Jahr ein Hoffest, zu dem fast alle
            kommen. Nächstes Jahr geht er in Rente. „Am meisten werde ich die Gespräche
            vermissen“, sagt er. Die Bewohner suchen schon jetzt ein Geschenk für ihn.
            """,
            [
                (
                    "Georg Brandt arbeitet …",
                    "seit 22 Jahren in der Wohnanlage.",
                    "seit 61 Jahren als Makler.",
                    "erst seit letztem Winter dort.",
                ),
                (
                    "Eine Mieterin gibt ihm ihren Schlüssel, …",
                    "wenn sie verreist.",
                    "weil sie ihn verloren hat.",
                    "wenn die Heizung kaputt ist.",
                ),
                (
                    "Der syrischen Familie …",
                    "half er bei den Formularen.",
                    "suchte er eine Wohnung.",
                    "gab er Deutschunterricht.",
                ),
                (
                    "Das Hoffest …",
                    "organisiert er jeden Sommer.",
                    "findet im Winter statt.",
                    "besuchen nur wenige Bewohner.",
                ),
                (
                    "Nach der Rente wird Herr Brandt vor allem …",
                    "die Gespräche vermissen.",
                    "die Reparaturen vermissen.",
                    "in eine andere Stadt ziehen.",
                ),
            ],
        ),
        (
            """
            Volkshochschule Seestadt · Haus der Bildung
            Erdgeschoss: Anmeldung · Information · Café
            1. Stock: Sprachen (Deutsch, Englisch, Spanisch) · Berufsberatung
            2. Stock: Computer und Medien · Bewerbungstraining
            3. Stock: Kunst: Malerei, Fotografie · Kreatives Schreiben
            Untergeschoss: Bewegung: Yoga, Tanz · Umkleideräume
            """,
            [
                (
                    "Sie möchten Hilfe bei Ihrem Lebenslauf und Bewerbungsschreiben.",
                    "2. Stock",
                    "1. Stock",
                    "Erdgeschoss",
                ),
                (
                    "Sie wollen sich für einen Kurs anmelden.",
                    "Erdgeschoss",
                    "3. Stock",
                    "Untergeschoss",
                ),
                (
                    "Sie möchten wissen, welcher Beruf zu Ihnen passt.",
                    "1. Stock",
                    "2. Stock",
                    "3. Stock",
                ),
                ("Sie suchen einen Fotokurs.", "3. Stock", "2. Stock", "Untergeschoss"),
                (
                    "Vor dem Yogakurs möchten Sie sich umziehen.",
                    "Untergeschoss",
                    "Erdgeschoss",
                    "1. Stock",
                ),
            ],
        ),
        (
            """
            Liebe Hanna,
            jetzt bin ich schon drei Wochen in Leipzig! Mein Praktikum bei der Zeitung
            gefällt mir sehr gut, obwohl die Tage lang sind. Am ersten Tag war ich
            ziemlich nervös, aber die Kollegen sind wirklich nett, und wir duzen uns
            alle. Gestern durfte ich sogar einen kurzen Artikel über ein Konzert
            schreiben. Das Problem ist die Wohnung: Ich wohne in einem kleinen Zimmer
            in einer WG am Stadtrand und brauche fast eine Stunde bis ins Büro. Ab
            nächstem Monat kann ich aber das Zimmer einer Kollegin übernehmen, die im
            Zentrum wohnt. Besuchst du mich im Mai? Dann zeige ich dir die Stadt.
            Liebe Grüße
            Tim
            """,
            [
                (
                    "Tim ist in Leipzig, …",
                    "weil er ein Praktikum macht.",
                    "weil er dort studiert.",
                    "weil er Urlaub macht.",
                ),
                ("Am ersten Tag war Tim …", "nervös.", "krank.", "allein im Büro."),
                (
                    "Gestern hat Tim …",
                    "einen Artikel geschrieben.",
                    "ein Konzert gegeben.",
                    "eine Wohnung besichtigt.",
                ),
                (
                    "Seine Wohnung jetzt …",
                    "ist weit vom Büro entfernt.",
                    "liegt im Zentrum.",
                    "gehört einer Kollegin.",
                ),
                (
                    "Im Mai möchte Tim …",
                    "Hanna die Stadt zeigen.",
                    "nach Hause fahren.",
                    "das Praktikum beenden.",
                ),
            ],
        ),
        (
            {
                "a": "Möbliertes Zimmer auf Zeit: 18 m², nahe Uni, 3–12 Monate, ideal für Praktikanten. Tel. 0176 445 21",
                "b": "Wer hilft mir im Garten? Rentner (80) sucht freundliche Person für zwei Stunden pro Woche.",
                "c": "Kindergarten Sonnenschein sucht Praktikantin oder Praktikanten für vier Wochen im Sommer.",
                "d": "Eigentumswohnung zu verkaufen: 4 Zimmer, Dachterrasse, beste Lage in der Innenstadt.",
                "e": "Alte Freunde wiederfinden: Klassentreffen der Goethe-Schule, Abschluss 2005. Bitte melden!",
                "f": "Reihenhaus im Vorort zu vermieten, mit Garten, ab 1. Juni, für Familien mit Kindern.",
            },
            [
                ("Lara studiert Pädagogik und möchte im Sommer mit Kindern arbeiten.", "c"),
                (
                    "Herr Kovač macht ein halbes Jahr ein Praktikum in der Stadt und braucht ein Zimmer.",
                    "a",
                ),
                ("Familie Weber mit drei Kindern sucht ein Haus mit Garten zur Miete.", "f"),
                ("Sabine hat 2005 Abitur gemacht und sucht ihre alten Mitschüler.", "e"),
                (
                    "Murat hat am Wochenende Zeit und möchte gern einem älteren Menschen helfen.",
                    "b",
                ),
            ],
        ),
    ),
    # Modul 2 (Lektionen 4-6): complaints, technology, invitations.
    2: _set(
        (
            """
            Wenn der Roboter den Rasen mäht

            Hannover. In immer mehr Gärten fahren kleine Roboter über den Rasen. Laut
            einer Umfrage hat schon jeder zehnte Haushalt mit Garten einen Mähroboter.
            „Früher habe ich jeden Samstag zwei Stunden gemäht“, erzählt Klaus Petersen
            (58). „Jetzt habe ich Zeit für meine Enkel.“ Doch nicht alle sind begeistert.
            Naturschützer warnen, dass die Geräte kleinen Tieren gefährlich werden
            können, besonders in der Nacht. Sie raten deshalb, die Roboter nur tagsüber
            fahren zu lassen. Experten vermuten, dass es in zehn Jahren auch Roboter
            geben wird, die Fenster putzen und Unkraut entfernen. Ob die Menschen das
            wirklich wollen, ist eine andere Frage.
            """,
            [
                (
                    "Mähroboter gibt es …",
                    "in jedem zehnten Haushalt mit Garten.",
                    "in fast allen Gärten.",
                    "nur in Hannover.",
                ),
                (
                    "Klaus Petersen hat jetzt mehr Zeit …",
                    "für seine Enkel.",
                    "für seinen Garten.",
                    "für die Arbeit.",
                ),
                (
                    "Naturschützer sagen, dass die Roboter …",
                    "für kleine Tiere gefährlich sind.",
                    "zu laut sind.",
                    "zu teuer sind.",
                ),
                (
                    "Man soll die Roboter …",
                    "nur am Tag fahren lassen.",
                    "nur in der Nacht fahren lassen.",
                    "nicht mehr kaufen.",
                ),
                (
                    "Experten glauben, dass Roboter in Zukunft …",
                    "auch Fenster putzen werden.",
                    "verboten werden.",
                    "keine Arbeit mehr machen.",
                ),
            ],
        ),
        (
            """
            Kundenservice Medienhaus Nordwind · Telefon 0800 123 456
            Taste 1: Neues Abonnement bestellen
            Taste 2: Abonnement kündigen oder ändern
            Taste 3: Lieferung fehlt oder kommt zu spät
            Taste 4: Rechnungen und Zahlungen
            Taste 5: Technische Hilfe für die App
            Taste 0: Persönliche Beratung
            """,
            [
                ("Ihre Zeitung ist heute nicht gekommen.", "Taste 3", "Taste 1", "Taste 4"),
                (
                    "Sie ziehen um und möchten Ihre neue Adresse für das Abo angeben.",
                    "Taste 2",
                    "Taste 3",
                    "Taste 0",
                ),
                ("Die App startet auf Ihrem Handy nicht.", "Taste 5", "Taste 4", "Taste 1"),
                ("Sie haben eine Rechnung zweimal bezahlt.", "Taste 4", "Taste 2", "Taste 5"),
                (
                    "Sie möchten die Zeitschrift für Ihre Mutter abonnieren.",
                    "Taste 1",
                    "Taste 2",
                    "Taste 3",
                ),
            ],
        ),
        (
            """
            Liebe Frau Albers,
            vielen Dank für die Einladung zu Ihrem Geburtstag am Samstag! Ich komme sehr
            gern. Mein Mann kann leider nicht mitkommen, weil er an diesem Wochenende
            beruflich in Zürich ist. Er lässt Sie herzlich grüßen. Darf ich etwas zum
            Essen mitbringen? Ich könnte zum Beispiel einen Kuchen backen. Ich muss
            Ihnen außerdem sagen, dass ich seit Kurzem allergisch gegen Nüsse bin. Falls
            es also Nüsse im Essen gibt, ist das kein Problem: Ich esse dann einfach
            etwas anderes. Ich freue mich schon sehr auf den Abend und darauf, Ihre
            Familie kennenzulernen.
            Herzliche Grüße
            Petra Lindner
            """,
            [
                ("Frau Lindner …", "kommt zum Geburtstag.", "kann nicht kommen.", "kommt später."),
                ("Ihr Mann …", "ist am Wochenende in Zürich.", "ist krank.", "kommt auch mit."),
                (
                    "Frau Lindner möchte …",
                    "vielleicht einen Kuchen mitbringen.",
                    "einen Salat machen.",
                    "Blumen kaufen.",
                ),
                ("Frau Lindner kann keine …", "Nüsse essen.", "Kuchen essen.", "Milch trinken."),
                (
                    "Frau Lindner kennt die Familie von Frau Albers …",
                    "noch nicht.",
                    "schon lange.",
                    "aus Zürich.",
                ),
            ],
        ),
        (
            {
                "a": "Computerhilfe zu Hause: Wir installieren Programme und retten verlorene Dateien. Auch abends.",
                "b": "Kochkurs „Gäste verwöhnen“: Menüs mit Vorspeise, Hauptspeise und Nachtisch für Ihre Einladung.",
                "c": "Partyservice Lecker: Buffets für Feste mit 20 bis 200 Gästen, auch vegetarisch.",
                "d": "Kurs „Gut telefonieren“: Professionell mit Kunden sprechen und Reklamationen lösen.",
                "e": "Gebrauchte Laptops und Monitore günstig: mit Garantie, Lieferung frei Haus.",
                "f": "Knigge-Seminar: richtig verhalten beim Geschäftsessen. Tischmanieren, Small Talk, Pünktlichkeit.",
            },
            [
                (
                    "Frau Yilmaz feiert ihre Hochzeit mit 80 Gästen und will nicht selbst kochen.",
                    "c",
                ),
                ("Herr Roth hat aus Versehen wichtige Dateien gelöscht.", "a"),
                ("Jan beginnt im Kundenservice und hat Angst vor schwierigen Anrufen.", "d"),
                ("Lena hat bald ein wichtiges Essen mit Geschäftspartnern und ist unsicher.", "f"),
                ("Tom möchte für seine Freunde ein Menü mit drei Gängen kochen lernen.", "b"),
            ],
        ),
    ),
    # Modul 3 (Lektionen 7-9): pets, careers, health at work.
    3: _set(
        (
            """
            Ein Büro für Hunde

            Köln. In der Werbeagentur „Blickfang“ arbeiten 14 Menschen und fünf Hunde.
            Seit zwei Jahren dürfen die Mitarbeiter ihre Hunde mit ins Büro bringen.
            „Am Anfang hatten einige Kollegen Angst“, erzählt die Chefin Mira Sanders.
            „Deshalb haben wir klare Regeln gemacht: Die Hunde dürfen nicht in die
            Küche, und wer allergisch ist, bekommt ein Büro ohne Tiere.“ Inzwischen
            sind alle zufrieden. Eine Studie zeigt, dass Hunde im Büro den Stress
            reduzieren können, weil die Mitarbeiter öfter Pausen machen und spazieren
            gehen. Frau Sanders sagt, dass die Atmosphäre viel besser geworden ist.
            Neue Bewerber fragen inzwischen oft zuerst nach den Hunden.
            """,
            [
                ("In der Agentur arbeiten …", "14 Menschen.", "fünf Menschen.", "zwei Menschen."),
                (
                    "Am Anfang …",
                    "hatten einige Kollegen Angst.",
                    "waren alle begeistert.",
                    "gab es keine Regeln.",
                ),
                (
                    "Wer allergisch ist, …",
                    "bekommt ein Büro ohne Tiere.",
                    "muss zu Hause arbeiten.",
                    "darf keinen Hund haben.",
                ),
                (
                    "Hunde im Büro reduzieren den Stress, weil …",
                    "die Mitarbeiter öfter Pausen machen.",
                    "sie leise sind.",
                    "die Mitarbeiter weniger arbeiten.",
                ),
                (
                    "Neue Bewerber …",
                    "fragen oft nach den Hunden.",
                    "dürfen keinen Hund mitbringen.",
                    "sind meistens allergisch.",
                ),
            ],
        ),
        (
            """
            Gesundheitstag bei der Firma Lindtec · Programm
            Halle A: Rückentraining und Gymnastik (9–12 Uhr)
            Halle B: Gesunde Ernährung: Vortrag und Kochvorführung (10 Uhr)
            Raum 101: Nichtraucher werden: Beratung (ganztags)
            Raum 102: Stress im Beruf: Entspannungsübungen (14 Uhr)
            Kantine: Obst- und Salatbuffet (12–14 Uhr)
            Foyer: Blutdruck messen · Informationen der Krankenkasse
            """,
            [
                ("Sie haben oft Rückenschmerzen.", "Halle A", "Raum 102", "Foyer"),
                ("Sie möchten mit dem Rauchen aufhören.", "Raum 101", "Halle B", "Kantine"),
                ("Sie wollen lernen, wie man gesund kocht.", "Halle B", "Halle A", "Raum 101"),
                ("Sie möchten Ihren Blutdruck prüfen lassen.", "Foyer", "Raum 102", "Halle A"),
                (
                    "Sie sind oft gestresst und möchten sich besser entspannen.",
                    "Raum 102",
                    "Raum 101",
                    "Kantine",
                ),
            ],
        ),
        (
            """
            Hallo Jakob,
            stell dir vor: Ich habe letzte Woche einen Berufstest gemacht! Bevor ich mich
            für eine Ausbildung bewerbe, wollte ich wissen, was wirklich zu mir passt.
            Das Ergebnis hat mich überrascht: Der Test sagt, dass ich ein sozialer Typ
            bin. Ich dachte immer, dass ich eher technisch begabt bin, weil ich gern
            Computer repariere. Meine Berufsberaterin meint aber, dass ich beides
            verbinden kann, zum Beispiel als Lehrerin für Informatik. Das kann ich mir
            gut vorstellen! Während ich die Ergebnisse gelesen habe, habe ich an dich
            gedacht: Du wolltest doch auch so einen Test machen. Ich schicke dir den Link.
            Viele Grüße
            Selin
            """,
            [
                (
                    "Selin hat den Test gemacht, …",
                    "bevor sie sich bewirbt.",
                    "nachdem sie eine Stelle hatte.",
                    "weil ihre Mutter es wollte.",
                ),
                (
                    "Das Ergebnis war für Selin …",
                    "eine Überraschung.",
                    "genau wie erwartet.",
                    "langweilig.",
                ),
                (
                    "Selin dachte, dass sie …",
                    "technisch begabt ist.",
                    "sozial begabt ist.",
                    "künstlerisch begabt ist.",
                ),
                (
                    "Die Berufsberaterin schlägt vor, …",
                    "beides zu verbinden.",
                    "Krankenschwester zu werden.",
                    "noch einen Test zu machen.",
                ),
                ("Selin schickt Jakob …", "den Link zum Test.", "ihr Ergebnis.", "eine Bewerbung."),
            ],
        ),
        (
            {
                "a": "Tierheim Pfötchen sucht Gassigeher: Gehen Sie am Wochenende mit unseren Hunden spazieren!",
                "b": "Meerschweinchen abzugeben: zwei junge Tiere mit Käfig, sehr zutraulich, ideal für Kinder.",
                "c": "Berufsberatung für Erwachsene: Wir helfen Ihnen, einen neuen Beruf zu finden. Kostenlos.",
                "d": "Fitnessstudio Aktiv: Rückenkurse für Menschen, die viel am Schreibtisch sitzen.",
                "e": "Tierarztpraxis Dr. Behr: auch samstags geöffnet, Notdienst rund um die Uhr.",
                "f": "Präsentieren lernen: Halten Sie Vorträge sicher und überzeugend. Abendkurs, 4 Termine.",
            },
            [
                (
                    "Herr Lange ist 45 und möchte nach 20 Jahren im Büro etwas ganz anderes machen.",
                    "c",
                ),
                ("Familie Becker sucht ein Haustier für ihre Tochter, aber keinen Hund.", "b"),
                ("Frau Wolf liebt Hunde, darf aber in ihrer Wohnung keine Tiere haben.", "a"),
                ("Ihre Katze ist am Sonntagabend plötzlich krank.", "e"),
                (
                    "Milan muss nächsten Monat seiner Firma ein Projekt vorstellen und ist nervös.",
                    "f",
                ),
            ],
        ),
    ),
    # Modul 4 (Lektionen 10-12): mishaps, happiness, company events.
    4: _set(
        (
            """
            Der verlorene Lottoschein

            Graz. Was für ein Pech – und dann doch noch Glück! Weil sie ihren Lottoschein
            im Bus liegen gelassen hatte, dachte Rentnerin Hilde M. (72) wochenlang, dass
            ihr Gewinn verloren war. „Ich habe mich so geärgert. Hätte ich ihn doch nur in
            die Tasche gesteckt!“, sagt sie. Der Busfahrer Daniel K. hatte den Schein
            jedoch gefunden und im Fundbüro abgegeben. Nachdem eine Zeitung über die
            Geschichte berichtet hatte, meldete sich Frau M. dort – und bekam den Schein
            zurück. Sie hatte 4.200 Euro gewonnen. Einen Teil des Geldes schenkte sie dem
            Busfahrer. „Ohne ihn wäre das Geld weg gewesen“, sagt sie.
            """,
            [
                (
                    "Frau M. hat ihren Lottoschein …",
                    "im Bus liegen gelassen.",
                    "zu Hause verloren.",
                    "nie gekauft.",
                ),
                (
                    "Sie dachte wochenlang, dass …",
                    "der Gewinn verloren war.",
                    "sie nichts gewonnen hatte.",
                    "der Busfahrer den Schein hatte.",
                ),
                (
                    "Der Busfahrer …",
                    "brachte den Schein ins Fundbüro.",
                    "behielt den Schein.",
                    "rief Frau M. an.",
                ),
                (
                    "Frau M. meldete sich, nachdem …",
                    "eine Zeitung berichtet hatte.",
                    "der Busfahrer sie besucht hatte.",
                    "sie den Bus gefunden hatte.",
                ),
                (
                    "Mit dem Geld …",
                    "beschenkte sie den Busfahrer.",
                    "kaufte sie einen Bus.",
                    "machte sie eine Reise.",
                ),
            ],
        ),
        (
            """
            Sommerfest der Papierfabrik Weber · Programm am Samstag
            14 Uhr: Begrüßung durch die Geschäftsführung (Festzelt)
            14.30 Uhr: Kinderprogramm mit Zauberer (Wiese)
            15 Uhr: Führung durch die neue Halle (Treffpunkt: Eingang)
            16 Uhr: Fußballturnier der Abteilungen (Sportplatz)
            18 Uhr: Buffet und Ehrung der Jubilare (Festzelt)
            20 Uhr: Musik und Tanz mit der Band „Papierflieger“ (Festzelt)
            """,
            [
                ("Ihre Kinder möchten einen Zauberer sehen.", "Wiese", "Festzelt", "Sportplatz"),
                (
                    "Sie wollen die neue Halle besichtigen. Wo treffen Sie sich?",
                    "Eingang",
                    "Wiese",
                    "Festzelt",
                ),
                (
                    "Ihr Kollege arbeitet seit 25 Jahren in der Firma und wird geehrt.",
                    "Festzelt",
                    "Sportplatz",
                    "Eingang",
                ),
                ("Ihre Abteilung spielt Fußball.", "Sportplatz", "Wiese", "Eingang"),
                ("Sie möchten am Abend tanzen.", "Festzelt", "Sportplatz", "Wiese"),
            ],
        ),
        (
            """
            Liebe Kolleginnen und Kollegen,
            nach 31 Jahren bei Weber gehe ich Ende Juni in Rente. Ich möchte mich
            deshalb bei euch verabschieden und lade euch herzlich zu meinem Ausstand ein:
            am Freitag, dem 27. Juni, ab 15 Uhr in der Kantine. Für Essen und Getränke
            ist gesorgt. Trotz der vielen Arbeit in den letzten Wochen hoffe ich, dass
            möglichst viele von euch kommen können. Bitte sagt mir bis Mittwoch Bescheid,
            damit ich genug Kuchen bestellen kann. Wer an diesem Tag Urlaub hat, ist
            natürlich auch herzlich willkommen. Ich freue mich auf einen schönen
            Nachmittag mit euch!
            Eure Renate
            """,
            [
                ("Renate …", "geht in Rente.", "wechselt die Firma.", "hat Geburtstag."),
                ("Der Ausstand ist …", "in der Kantine.", "im Restaurant.", "bei Renate zu Hause."),
                (
                    "Das Essen …",
                    "organisiert Renate.",
                    "müssen die Kollegen mitbringen.",
                    "gibt es nicht.",
                ),
                (
                    "Bis Mittwoch sollen die Kollegen …",
                    "Bescheid sagen.",
                    "Kuchen backen.",
                    "Urlaub nehmen.",
                ),
                (
                    "Kollegen im Urlaub …",
                    "dürfen auch kommen.",
                    "sollen nicht kommen.",
                    "bekommen eine E-Mail.",
                ),
            ],
        ),
        (
            {
                "a": "Schlüsseldienst Notfall: Tür zugefallen? Wir sind in 30 Minuten da, Tag und Nacht.",
                "b": "Glücksbringer aus Holz: handgemachte Geschenke für Hochzeiten, Geburten und Prüfungen.",
                "c": "Biergarten am See: Platz für Betriebsausflüge bis 150 Personen, mit Bootsfahrt.",
                "d": "Abschleppdienst Krause: Panne auf der Autobahn? Wir helfen schnell.",
                "e": "Fundbüro der Stadt: Haben Sie etwas verloren? Montag bis Freitag 8–16 Uhr.",
                "f": "Rednerkurs: Halten Sie die perfekte Rede auf Ihrer Feier oder Ihrem Jubiläum.",
            },
            [
                (
                    "Herr Sommer hat seinen Schlüssel in der Wohnung vergessen und kommt nicht hinein.",
                    "a",
                ),
                ("Frau Kaya organisiert einen Ausflug für 90 Kollegen.", "c"),
                ("Lukas hat seine Brieftasche in der Straßenbahn verloren.", "e"),
                ("Anna sucht ein Geschenk für ihre Schwester, die ein Baby bekommen hat.", "b"),
                ("Herr Wolf soll beim Firmenjubiläum sprechen und weiß nicht, wie.", "f"),
            ],
        ),
    ),
    # Modul 5 (Lektionen 13-15): misunderstandings, courses, applications.
    5: _set(
        (
            """
            Teekesselchen im Supermarkt

            Mainz. Missverständnisse wegen der Sprache sind oft lustig. Die Spanierin
            Lucía Gómez (29) lebt seit einem Jahr in Mainz und erzählt: „Im Supermarkt
            habe ich nach ‚Birnen‘ gefragt, weil ich Glühbirnen für meine Lampe brauchte.
            Der Verkäufer hat mir Obst gezeigt!“ Wörter mit zwei Bedeutungen heißen im
            Deutschen „Teekesselchen“. Deshalb rät eine Lehrerin der Volkshochschule, in
            solchen Situationen einfach nachzufragen: „Könnten Sie das bitte anders
            erklären?“ Lucía lacht heute über die Geschichte. Sie besucht jetzt einen
            Kurs, in dem die Teilnehmer jede Woche ein neues Teekesselchen lernen.
            Wegen ihrer Erfahrung hat sie sogar ein kleines Buch darüber geschrieben.
            """,
            [
                (
                    "Lucía wollte im Supermarkt …",
                    "Glühbirnen kaufen.",
                    "Obst kaufen.",
                    "eine Lampe kaufen.",
                ),
                (
                    "Der Verkäufer …",
                    "zeigte ihr Obst.",
                    "verstand sie sofort.",
                    "schickte sie weg.",
                ),
                (
                    "Ein Teekesselchen ist …",
                    "ein Wort mit zwei Bedeutungen.",
                    "ein Getränk.",
                    "ein Kurs an der VHS.",
                ),
                (
                    "Die Lehrerin rät, …",
                    "nachzufragen.",
                    "nichts zu sagen.",
                    "ein Wörterbuch zu kaufen.",
                ),
                (
                    "Wegen ihrer Erfahrung hat Lucía …",
                    "ein Buch geschrieben.",
                    "den Supermarkt gewechselt.",
                    "Mainz verlassen.",
                ),
            ],
        ),
        (
            """
            Stellenmarkt Online · Kategorien
            Büro und Verwaltung: Sachbearbeitung, Sekretariat, Empfang
            Gastronomie und Hotel: Küche, Service, Rezeption
            Handwerk: Elektriker, Schreiner, Mechaniker
            Gesundheit und Soziales: Pflege, Erziehung, Beratung
            Medien: Journalismus, Fotografie, Grafik
            Ausbildungsplätze für Schulabgänger
            """,
            [
                (
                    "Sie haben gerade die Schule beendet und suchen eine Ausbildung.",
                    "Ausbildungsplätze für Schulabgänger",
                    "Büro und Verwaltung",
                    "Handwerk",
                ),
                (
                    "Sie sind Krankenpflegerin und suchen eine neue Stelle.",
                    "Gesundheit und Soziales",
                    "Gastronomie und Hotel",
                    "Medien",
                ),
                ("Sie möchten als Reporter arbeiten.", "Medien", "Büro und Verwaltung", "Handwerk"),
                (
                    "Sie suchen eine Stelle an der Rezeption eines Hotels.",
                    "Gastronomie und Hotel",
                    "Büro und Verwaltung",
                    "Medien",
                ),
                ("Sie reparieren gern Autos.", "Handwerk", "Medien", "Gesundheit und Soziales"),
            ],
        ),
        (
            """
            Sehr geehrte Frau Doktor Kern,
            vielen Dank für das freundliche Gespräch am Dienstag. Ich habe mich sehr
            gefreut, Ihr Team kennenzulernen. Wie besprochen schicke ich Ihnen meine
            Zeugnisse noch einmal als Datei, weil die Kopien in meiner Bewerbung leider
            schlecht zu lesen waren. Ich möchte außerdem eine Frage klären: Im Gespräch
            habe ich verstanden, dass die Stelle ab 1. September frei ist. Meine
            Kollegin hat mir aber gesagt, dass es der 1. Oktober sein könnte. Könnten
            Sie mir das bitte bestätigen? Ich bin sowohl im September als auch im
            Oktober flexibel. Über eine positive Antwort würde ich mich sehr freuen.
            Mit freundlichen Grüßen
            Ana Petrović
            """,
            [
                (
                    "Frau Petrović hatte …",
                    "ein Vorstellungsgespräch.",
                    "einen Unfall.",
                    "einen Kurs bei Frau Kern.",
                ),
                (
                    "Sie schickt die Zeugnisse noch einmal, weil …",
                    "die Kopien schlecht zu lesen waren.",
                    "sie sie vergessen hatte.",
                    "Frau Kern sie verloren hat.",
                ),
                (
                    "Frau Petrović ist nicht sicher, …",
                    "wann die Stelle beginnt.",
                    "wie viel sie verdient.",
                    "wo das Büro ist.",
                ),
                (
                    "Sie kann anfangen …",
                    "im September oder im Oktober.",
                    "nur im September.",
                    "erst im nächsten Jahr.",
                ),
                (
                    "Der Ton der E-Mail ist …",
                    "höflich und formell.",
                    "unfreundlich.",
                    "sehr persönlich.",
                ),
            ],
        ),
        (
            {
                "a": "Bewerbungsfotos im Studio: professionell, schnell, mit Beratung zur Kleidung.",
                "b": "Klettern für Anfänger: Keine Vorkenntnisse nötig. Teilnahme auf eigene Gefahr.",
                "c": "Deutsch für den Beruf (B1/B2): Telefonieren, E-Mails, Besprechungen.",
                "d": "Übersetzungsbüro Klar: Wir übersetzen Zeugnisse und Dokumente in 30 Sprachen.",
                "e": "Nähkurs am Abend: Lernen Sie, Ihre Kleidung selbst zu nähen und zu reparieren.",
                "f": "Training Vorstellungsgespräch: Üben Sie mit echten Personalleitern.",
            },
            [
                ("Herr Ali hat seine Zeugnisse auf Arabisch und braucht sie auf Deutsch.", "d"),
                ("Frau Novak spricht gut Deutsch, hat aber im Büro Probleme am Telefon.", "c"),
                (
                    "Ben hat nächste Woche sein erstes Vorstellungsgespräch und ist sehr nervös.",
                    "f",
                ),
                ("Julia braucht für ihre Bewerbung ein gutes Foto.", "a"),
                (
                    "Paul möchte einen neuen Sport ausprobieren, auch wenn es ein bisschen gefährlich ist.",
                    "b",
                ),
            ],
        ),
    ),
    # Modul 6 (Lektionen 16-18): memories, art, politics.
    6: _set(
        (
            """
            Eine Malerin kehrt zurück

            Murnau. Das Schlossmuseum zeigt ab Samstag eine Ausstellung über die
            Malerin Elsa Hoff (1890–1962). Hoff wuchs in einer armen Familie auf und
            durfte als Frau zuerst nicht an der Kunstakademie studieren. Deshalb nahm
            sie privaten Unterricht. Ihre farbigen Bilder von Hügeln und kleinen Dörfern
            wurden in den Zwanzigerjahren bekannt. Im Krieg wurden viele ihrer Werke
            zerstört. Jahrzehntelang fand man ihre Bilder nur in wenigen Galerien. Erst
            als ihr Enkel vor drei Jahren 40 Gemälde auf einem Dachboden entdeckte,
            begann man, sich wieder für sie zu interessieren. „Es lohnt sich, sie neu
            zu entdecken“, sagt die Museumsleiterin.
            """,
            [
                (
                    "Elsa Hoff durfte zuerst nicht an der Akademie studieren, weil …",
                    "sie eine Frau war.",
                    "sie kein Geld hatte.",
                    "sie krank war.",
                ),
                (
                    "Ihre Bilder zeigen oft …",
                    "Hügel und Dörfer.",
                    "große Städte.",
                    "Menschen im Krieg.",
                ),
                (
                    "Im Krieg …",
                    "wurden viele Bilder zerstört.",
                    "malte sie besonders viel.",
                    "wurde sie berühmt.",
                ),
                (
                    "Ihr Enkel …",
                    "fand 40 Bilder auf einem Dachboden.",
                    "ist auch Maler.",
                    "leitet das Museum.",
                ),
                (
                    "Die Museumsleiterin findet, dass …",
                    "man Elsa Hoff neu entdecken sollte.",
                    "die Bilder zu teuer sind.",
                    "die Ausstellung zu klein ist.",
                ),
            ],
        ),
        (
            """
            Rathaus Altenburg · Wegweiser
            Erdgeschoss: Bürgerbüro (Pass, Personalausweis, Anmeldung) · Information
            1. Stock: Standesamt (Hochzeiten, Geburten) · Ratssaal
            2. Stock: Bauamt · Umweltamt (Bürgerinitiativen, Klimaschutz)
            3. Stock: Amt für Familie und Senioren · Kinderbetreuung
            Untergeschoss: Wahlbüro (Briefwahl) · Archiv
            """,
            [
                (
                    "Sie möchten vor der Wahl per Brief wählen.",
                    "Untergeschoss",
                    "Erdgeschoss",
                    "2. Stock",
                ),
                ("Sie möchten heiraten.", "1. Stock", "3. Stock", "Erdgeschoss"),
                (
                    "Ihre Bürgerinitiative möchte einen Park retten.",
                    "2. Stock",
                    "1. Stock",
                    "Untergeschoss",
                ),
                ("Sie brauchen einen neuen Pass.", "Erdgeschoss", "2. Stock", "3. Stock"),
                (
                    "Sie suchen einen Platz in einem Kindergarten.",
                    "3. Stock",
                    "1. Stock",
                    "Untergeschoss",
                ),
            ],
        ),
        (
            """
            Lieber Opa,
            für mein Schulprojekt „Früher und heute“ möchte ich dich interviewen. Meine
            Lehrerin hat gesagt, dass wir jemanden aus einer anderen Generation fragen
            sollen. Ich möchte wissen, wie deine Jugend war: Musstest du zu Hause viel
            helfen? Was durftest du nicht? Mama hat erzählt, dass du nie Taschengeld
            bekommen hast und schon mit 14 Jahren arbeiten musstest. Stimmt das? Du
            brauchst dich nicht vorzubereiten, wir reden einfach. Es dauert ungefähr
            eine Stunde. Passt dir Sonntagnachmittag? Ich bringe Kuchen mit!
            Dein Felix
            """,
            [
                (
                    "Felix schreibt, weil …",
                    "er ein Interview für die Schule machen will.",
                    "er Geld braucht.",
                    "sein Opa Geburtstag hat.",
                ),
                (
                    "Die Lehrerin möchte, dass die Schüler …",
                    "jemanden aus einer anderen Generation fragen.",
                    "einen Aufsatz über sich schreiben.",
                    "ein Museum besuchen.",
                ),
                (
                    "Laut Mama hat der Opa …",
                    "nie Taschengeld bekommen.",
                    "viel Taschengeld bekommen.",
                    "nie gearbeitet.",
                ),
                (
                    "Der Opa muss sich …",
                    "nicht vorbereiten.",
                    "gut vorbereiten.",
                    "Fragen aufschreiben.",
                ),
                (
                    "Felix möchte den Opa …",
                    "am Sonntagnachmittag besuchen.",
                    "am Samstagabend anrufen.",
                    "in der Schule treffen.",
                ),
            ],
        ),
        (
            {
                "a": "Erzählcafé: Senioren erzählen Jugendlichen von früher. Jeden ersten Dienstag im Monat.",
                "b": "Malkurs für Erwachsene: Landschaften in Öl, mit Pinsel und Spachtel.",
                "c": "Wahl-Info-Abend: Alle Parteien stellen ihre Programme vor. Diskutieren Sie mit!",
                "d": "Ehrenamt gesucht: Die Tafel braucht Helfer, die Lebensmittel an Bedürftige verteilen.",
                "e": "Kunstreise nach Wien: Museen und Galerien in vier Tagen, mit Führung.",
                "f": "Familienberatung: Hilfe bei Streit und Konflikten zwischen Eltern und Kindern.",
            },
            [
                ("Frau Berger ist Rentnerin und möchte etwas Sinnvolles für andere tun.", "d"),
                ("Herr Kim weiß noch nicht, welche Partei er wählen soll.", "c"),
                ("Familie Roth streitet oft mit ihrer Tochter und braucht Rat.", "f"),
                ("Mia möchte lernen, Berge und Seen zu malen.", "b"),
                ("Herr Lang ist 85 und erzählt gern von seiner Kindheit.", "a"),
            ],
        ),
    ),
    # Modul 7 (Lektionen 19-21): tourism, mountain huts, concerts and cities.
    7: _set(
        (
            """
            Je mehr Gäste, desto weniger Ruhe?

            Lüneburger Heide. Im August blüht die Heide lila, und dann kommen die meisten
            Touristen. Für die Region ist das gut, denn viele Hotels und Gaststätten leben
            vom Tourismus. Doch je mehr Menschen kommen, desto größer werden die
            Probleme: Manche Besucher verlassen die Wege, sodass Pflanzen und Tiere
            gestört werden. Der Naturschutzverein hat deshalb neue Regeln eingeführt. Man
            darf nur noch auf markierten Wegen wandern, und Hunde müssen an die Leine.
            Außerdem schützt man die Heide, indem man Schafe dort fressen lässt. Ein
            Schäfer erklärt: „Ohne die Schafe würde die Heide verschwinden.“
            """,
            [
                ("Die meisten Touristen kommen …", "im August.", "im Winter.", "im Frühling."),
                ("Der Tourismus ist für die Region …", "wichtig.", "unwichtig.", "verboten."),
                (
                    "Manche Besucher …",
                    "verlassen die Wege.",
                    "fahren mit dem Auto in die Heide.",
                    "füttern die Schafe.",
                ),
                (
                    "Hunde …",
                    "müssen an die Leine.",
                    "dürfen nicht in die Heide.",
                    "dürfen frei laufen.",
                ),
                (
                    "Die Schafe …",
                    "schützen die Heide.",
                    "sind ein Problem.",
                    "gehören den Touristen.",
                ),
            ],
        ),
        (
            """
            Stadthalle Kiel · Veranstaltungen im Mai
            Saal 1: Rockkonzert „Wonnetöne“ (Fr., 20 Uhr)
            Saal 2: Kindertheater „Die kleine Hexe“ (Sa., 15 Uhr)
            Studio: Jazzabend mit Lesung (Do., 19.30 Uhr)
            Foyer: Fotoausstellung „Leben an der Küste“ (täglich 10–18 Uhr)
            Kasse: Karten und Information · Garderobe im Untergeschoss
            """,
            [
                (
                    "Sie möchten mit Ihrer Tochter (6) ins Theater gehen.",
                    "Saal 2",
                    "Saal 1",
                    "Studio",
                ),
                ("Sie mögen Jazz und Literatur.", "Studio", "Saal 1", "Foyer"),
                ("Sie möchten am Nachmittag Fotos anschauen.", "Foyer", "Studio", "Saal 2"),
                ("Sie wollen Karten kaufen.", "Kasse", "Foyer", "Saal 1"),
                ("Sie möchten am Freitagabend laute Musik hören.", "Saal 1", "Studio", "Saal 2"),
            ],
        ),
        (
            """
            Hallo Mareike,
            wir sind zurück von der Hütte, und ich muss dir unbedingt erzählen, wie es
            war! Der Weg zum Gipfel war so steil, dass ich zweimal eine Pause machen
            musste. Oben war die Aussicht aber einmalig. Die Hütte war voll, sodass wir
            im Lager mit zwanzig anderen Leuten schlafen mussten. Zum Glück hatte ich
            Ohrstöpsel dabei! Der Hüttenwirt war sehr streng: Ab 22 Uhr war Nachtruhe,
            und jeder musste seinen Müll wieder mit ins Tal nehmen. Am Anfang fand ich
            das übertrieben, aber eigentlich sind die Regeln sinnvoll. Nächstes Jahr
            musst du mitkommen!
            Bis bald, Ina
            """,
            [
                ("Der Weg zum Gipfel war …", "sehr steil.", "ganz flach.", "zu kurz."),
                (
                    "Ina und ihre Freunde schliefen …",
                    "im Lager.",
                    "in einem Einzelzimmer.",
                    "im Zelt.",
                ),
                (
                    "Ina hatte Glück, weil sie …",
                    "Ohrstöpsel dabeihatte.",
                    "ein eigenes Zimmer hatte.",
                    "früh schlafen konnte.",
                ),
                (
                    "Den Müll musste man …",
                    "wieder mitnehmen.",
                    "in der Hütte lassen.",
                    "verbrennen.",
                ),
                ("Heute findet Ina die Regeln …", "sinnvoll.", "übertrieben.", "lustig."),
            ],
        ),
        (
            {
                "a": "Stadtführung „Geheime Ecken“: zwei Stunden durch die Altstadt, auch für Kinder.",
                "b": "Berghütte Edelweiß: Übernachtung im Lager, Halbpension, Reservierung nötig.",
                "c": "Fahrradtour am Fluss entlang: 40 km, Leihräder vorhanden, mit Picknick.",
                "d": "Musikschule: Gitarre und Schlagzeug für Anfänger und Fortgeschrittene.",
                "e": "Heidetour mit dem Schäfer: Erleben Sie die Schafe und lernen Sie alles über Honig.",
                "f": "Ticketservice: Karten für Konzerte, Theater und Sport in ganz Deutschland.",
            },
            [
                ("Familie Kaiser möchte am Wochenende die Stadt mit ihren Kindern entdecken.", "a"),
                ("Herr Ott sucht Karten für das Konzert seiner Lieblingsband in Berlin.", "f"),
                ("Lea und Nils wollen in den Bergen übernachten.", "b"),
                ("Tim möchte in einer Band spielen, kann aber noch kein Instrument.", "d"),
                ("Frau Brandt fährt gern Rad, hat aber kein eigenes Fahrrad.", "c"),
            ],
        ),
    ),
    # Modul 8 (Lektionen 22-24): history, environment, living together.
    8: _set(
        (
            """
            Ein Dorf für alle Generationen

            Bei Kassel. Vor fünf Jahren haben sich zwölf Familien und acht Rentner
            zusammengeschlossen, um gemeinsam auf einem alten Bauernhof zu wohnen. Jede
            Familie hat eine eigene Wohnung, aber Küche, Garten und Werkstatt teilen
            sich alle. Die Älteren kümmern sich um die Kinder, damit die Eltern arbeiten
            können. Die Jüngeren kaufen ein und helfen im Haushalt. Statt jeder ein
            eigenes Auto zu haben, nutzen alle drei gemeinsame Autos und viele Fahrräder.
            Anfangs gab es oft Streit, zum Beispiel über die Hausarbeit. Allmählich hat
            die Gruppe aber Kompromisse gefunden. „Es ist, als ob wir eine große Familie
            wären“, sagt eine Bewohnerin.
            """,
            [
                (
                    "Auf dem Bauernhof wohnen …",
                    "Familien und Rentner.",
                    "nur Rentner.",
                    "nur Studenten.",
                ),
                ("Die Küche …", "teilen sich alle.", "hat jede Familie selbst.", "gibt es nicht."),
                (
                    "Die Älteren kümmern sich um die Kinder, …",
                    "damit die Eltern arbeiten können.",
                    "weil sie Geld brauchen.",
                    "obwohl sie keine Zeit haben.",
                ),
                (
                    "Statt eigener Autos …",
                    "gibt es drei gemeinsame Autos.",
                    "fahren alle mit dem Bus.",
                    "hat niemand ein Auto.",
                ),
                (
                    "Am Anfang …",
                    "gab es oft Streit.",
                    "war alles perfekt.",
                    "wohnten dort nur zwei Familien.",
                ),
            ],
        ),
        (
            """
            Haus der Geschichte · Ausstellung „Deutschland nach 1945“
            Raum 1: Kriegsende und Besatzungszonen
            Raum 2: Die Luftbrücke nach Berlin (1948/49)
            Raum 3: Gründung von BRD und DDR (1949)
            Raum 4: Der Bau der Mauer (1961) und das Leben in der geteilten Stadt
            Raum 5: Die friedliche Revolution und die Maueröffnung (1989)
            Raum 6: Wiedervereinigung und Europa (ab 1990)
            """,
            [
                (
                    "Sie möchten mehr über die Flugzeuge wissen, die Berlin versorgten.",
                    "Raum 2",
                    "Raum 1",
                    "Raum 4",
                ),
                ("Sie interessieren sich für den 9. November 1989.", "Raum 5", "Raum 4", "Raum 6"),
                (
                    "Sie möchten sehen, wie 1949 zwei deutsche Staaten entstanden.",
                    "Raum 3",
                    "Raum 2",
                    "Raum 6",
                ),
                (
                    "Sie wollen wissen, wie die Menschen mit der Mauer lebten.",
                    "Raum 4",
                    "Raum 5",
                    "Raum 1",
                ),
                ("Sie interessieren sich für die Zeit nach 1990.", "Raum 6", "Raum 3", "Raum 5"),
            ],
        ),
        (
            """
            Liebe Nachbarinnen und Nachbarn,
            unsere Stadt plant, die Hauptstraße im nächsten Jahr für Autos zu sperren
            und dort einen breiten Radweg zu bauen. Viele von uns finden das gut, weil
            die Luft besser und die Straße ruhiger wird. Andere haben Sorgen: Wie kommen
            ältere Menschen ohne Auto zum Arzt? Wo sollen die Lieferwagen der Geschäfte
            parken? Damit alle ihre Meinung sagen können, laden wir zu einem
            Informationsabend ein: am Donnerstag um 19 Uhr in der Grundschule. Auch
            Vertreter der Stadt kommen. Bitte kommt zahlreich – je mehr Leute da sind,
            desto besser!
            Eure Bürgerinitiative „Saubere Luft“
            """,
            [
                (
                    "Die Stadt will …",
                    "die Hauptstraße für Autos sperren.",
                    "eine neue Autobahn bauen.",
                    "mehr Parkplätze bauen.",
                ),
                (
                    "Viele Nachbarn finden den Plan gut, weil …",
                    "die Luft besser wird.",
                    "sie kein Fahrrad haben.",
                    "es billiger ist.",
                ),
                (
                    "Manche haben Sorgen um …",
                    "ältere Menschen ohne Auto.",
                    "die Schulkinder.",
                    "die Touristen.",
                ),
                (
                    "Der Informationsabend ist …",
                    "in der Grundschule.",
                    "im Rathaus.",
                    "auf der Hauptstraße.",
                ),
                (
                    "Die Bürgerinitiative wünscht sich, dass …",
                    "viele Leute kommen.",
                    "nur Vertreter der Stadt kommen.",
                    "niemand diskutiert.",
                ),
            ],
        ),
        (
            {
                "a": "Repair-Café: Wir reparieren Fahrräder, Lampen und Kleidung, statt sie wegzuwerfen.",
                "b": "Zeitzeugen gesucht: Haben Sie den Mauerfall erlebt? Das Museum möchte Ihre Geschichte hören.",
                "c": "Mehrgenerationenhaus: Wohnungen frei für Familien, die mit Älteren zusammenleben möchten.",
                "d": "Lastenräder zu mieten: Transportieren Sie Ihren Einkauf ohne Auto.",
                "e": "Sprachcafé: Menschen aus aller Welt treffen sich, um Deutsch zu sprechen.",
                "f": "Kleidertausch: Bringen Sie Kleidung mit, die Sie nicht mehr tragen, und nehmen Sie andere mit.",
            },
            [
                ("Herr Schulz (70) hat 1989 in Berlin gewohnt und erzählt gern davon.", "b"),
                (
                    "Familie Yilmaz möchte gern mit anderen Generationen unter einem Dach wohnen.",
                    "c",
                ),
                ("Lisas Fahrrad ist kaputt, aber sie will kein neues kaufen.", "a"),
                ("Frau Berg hat kein Auto und muss einen großen Einkauf nach Hause bringen.", "d"),
                (
                    "Omar ist neu in der Stadt und möchte sein Deutsch üben und Leute kennenlernen.",
                    "e",
                ),
            ],
        ),
    ),
}
