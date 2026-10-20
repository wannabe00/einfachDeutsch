"""B1 Lesen sets, shaped like the Goethe-Zertifikat B1 reading paper: one set per
Modul, 30 questions. Teil 1: a blog post, 6 richtig/falsch. Teil 2: two
newspaper texts, 3 questions each (a/b/c). Teil 3: 7 situations and 10 adverts
(one situation has no advert: 0). Teil 4: 7 readers' comments, is the person for
it? (ja/nein). Teil 5: rules or instructions, 4 questions (a/b/c).

All texts are original (places and people are made up), on the Modul's topics.
"""

from ..dsl import NO_AD, lesen_ads, lesen_opinions, lesen_rf, lesen_text


def _set(blog, article_a, article_b, ads, opinions, rules) -> list:
    return [
        lesen_rf("blog post", *blog, teil=1),
        lesen_text("newspaper article", *article_a, teil=2),
        lesen_text("newspaper article", *article_b, teil=2),
        lesen_ads(*ads, teil=3),
        lesen_opinions(*opinions, teil=4),
        lesen_text(*rules, teil=5),  # (what, text, rows)
    ]


LESEN = {
    # Modul 1 (Lektionen 1-3): friendship, internships, housing.
    1: _set(
        (
            """
            Mein Jahr in Hamburg

            Vor einem Jahr bin ich für ein Praktikum nach Hamburg gezogen. Am Anfang kannte
            ich niemanden, und mein Zimmer in der WG war so klein, dass nur ein Bett und ein
            Schreibtisch hineinpassten. Meine Mitbewohnerin Ronja hat mir aber sofort die
            Stadt gezeigt. Sie ist die Hilfsbereiteste, die ich kenne! Das Praktikum bei
            einer Zeitung war anstrengend, weil ich oft bis spät abends arbeiten musste.
            Trotzdem habe ich viel gelernt, und mein Chef hat mir am Ende ein sehr gutes
            Zeugnis geschrieben. Jetzt habe ich eine feste Stelle in derselben Redaktion.
            Nächsten Monat ziehe ich in eine eigene Wohnung mit Balkon, aber Ronja und ich
            treffen uns natürlich weiter jeden Sonntag zum Frühstück.
            """,
            [
                ("Am Anfang hatte die Autorin in Hamburg keine Bekannten.", True),
                ("Ihr Zimmer in der WG war sehr groß.", False),
                ("Ronja hat ihr die Stadt gezeigt.", True),
                ("Im Praktikum musste sie nie lange arbeiten.", False),
                ("Sie arbeitet jetzt bei einer anderen Zeitung.", False),
                ("Sie möchte Ronja auch nach dem Umzug weiter treffen.", True),
            ],
        ),
        (
            """
            Ein Hausmeister mit Herz

            Bremen. Seit 22 Jahren ist Georg Brandt (61) Hausmeister in einer großen
            Wohnanlage. Er repariert Heizungen und kümmert sich um den Innenhof. Für viele
            Bewohner ist er aber viel mehr: „Herr Brandt ist der Mensch, dem ich meinen
            Schlüssel gebe, wenn ich verreise“, sagt eine Mieterin. Als im letzten Winter eine
            Familie aus Syrien einzog, half er ihr bei den Formularen. Nächstes Jahr geht er in
            Rente. „Am meisten werde ich die Gespräche vermissen“, sagt er.
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
                    "Nach der Rente wird Herr Brandt vor allem …",
                    "die Gespräche vermissen.",
                    "die Reparaturen vermissen.",
                    "in eine andere Stadt ziehen.",
                ),
            ],
        ),
        (
            """
            Immer mehr Menschen leben allein

            Wiesbaden. Fast jeder zweite Haushalt in deutschen Großstädten ist ein
            Single-Haushalt. Das zeigt eine neue Statistik. Besonders viele ältere Menschen
            wohnen allein, weil ihre Kinder ausgezogen sind oder ihr Partner gestorben ist.
            Junge Leute ziehen dagegen oft in eine WG, weil die Mieten in den Innenstädten so
            hoch sind. Experten erwarten, dass in Zukunft mehr Wohnungen gebaut werden, in
            denen Menschen zwar allein wohnen, aber eine Küche und einen Garten teilen.
            """,
            [
                (
                    "Laut der Statistik ist in Großstädten …",
                    "fast jeder zweite Haushalt ein Single-Haushalt.",
                    "jeder zehnte Haushalt eine WG.",
                    "die Hälfte der Wohnungen leer.",
                ),
                (
                    "Junge Leute ziehen oft in eine WG, weil …",
                    "die Mieten hoch sind.",
                    "sie nicht allein sein wollen.",
                    "es keine Wohnungen gibt.",
                ),
                (
                    "Experten erwarten mehr Wohnungen, …",
                    "in denen man manche Räume teilt.",
                    "die sehr groß sind.",
                    "die am Stadtrand liegen.",
                ),
            ],
        ),
        (
            {
                "a": "Möbliertes Zimmer auf Zeit: 18 m², nahe Uni, 3–12 Monate, ideal für Praktikanten.",
                "b": "Wer hilft mir im Garten? Rentner (80) sucht freundliche Person für zwei Stunden pro Woche.",
                "c": "Kindergarten Sonnenschein sucht Praktikantin oder Praktikanten für vier Wochen im Sommer.",
                "d": "Eigentumswohnung zu verkaufen: 4 Zimmer, Dachterrasse, beste Lage in der Innenstadt.",
                "e": "Klassentreffen der Goethe-Schule, Abschluss 2005. Bitte meldet euch!",
                "f": "Reihenhaus im Vorort zu vermieten, mit Garten, ab 1. Juni, für Familien mit Kindern.",
                "g": "Umzugshelfer gesucht: Wir tragen Möbel und Kartons, auch am Wochenende. Günstige Preise.",
                "h": "Malkurs für Senioren: jeden Mittwoch im Gemeindehaus, Material wird gestellt.",
                "i": "Hausmeisterservice Klar: Reparaturen, Gartenpflege und Winterdienst für Wohnanlagen.",
                "j": "WG-Zimmer frei: nette Dreier-WG sucht Mitbewohnerin, Nichtraucherin, ab sofort.",
            },
            [
                ("Lara studiert Pädagogik und möchte im Sommer mit Kindern arbeiten.", "c"),
                ("Herr Kovač macht ein halbes Jahr ein Praktikum und braucht ein Zimmer.", "a"),
                ("Familie Weber mit drei Kindern sucht ein Haus mit Garten zur Miete.", "f"),
                ("Sabine hat 2005 Abitur gemacht und sucht ihre alten Mitschüler.", "e"),
                ("Murat hat Zeit und möchte einem älteren Menschen helfen.", "b"),
                ("Frau Lorenz zieht nächste Woche um und hat viele schwere Möbel.", "g"),
                ("Ben sucht einen Job als Fotograf in einer Werbeagentur.", NO_AD),
            ],
        ),
        (
            "Ist es eine gute Idee, mit Freunden zusammenzuwohnen?",
            [
                (
                    "Lisa (24)",
                    "Mit meiner besten Freundin wohne ich seit drei Jahren zusammen. Wir kochen zusammen, wir teilen die Kosten, und ich bin nie allein. Für mich gibt es nichts Besseres.",
                    True,
                ),
                (
                    "Jonas (31)",
                    "Ich habe es versucht, und unsere Freundschaft ist kaputtgegangen. Wer den ganzen Tag zusammen ist, streitet irgendwann über das schmutzige Geschirr. Nie wieder!",
                    False,
                ),
                (
                    "Ayşe (19)",
                    "Ich ziehe bald mit zwei Freundinnen in eine WG. Ich freue mich sehr darauf, weil wir uns schon seit der Schule kennen und gut verstehen.",
                    True,
                ),
                (
                    "Herr Pohl (58)",
                    "In meinem Alter brauche ich meine Ruhe. Freunde besuche ich gern, aber wohnen möchte ich allein. Jeder sollte seine eigenen vier Wände haben.",
                    False,
                ),
                (
                    "Mira (27)",
                    "Es kommt darauf an. Mit ordentlichen Freunden ja, mit chaotischen nein. Meine WG funktioniert super, weil wir klare Regeln haben.",
                    True,
                ),
                (
                    "Tobias (22)",
                    "Freunde sind Freunde, Mitbewohner sind etwas anderes. Ich wohne lieber mit Leuten zusammen, die ich vorher nicht kannte. Dann ist es einfacher, ehrlich zu sein.",
                    False,
                ),
                (
                    "Frau Haas (45)",
                    "Meine Tochter wohnt mit ihrer Schulfreundin zusammen, und die beiden sind sehr glücklich. Ich finde, man lernt dabei viel, zum Beispiel Kompromisse zu machen.",
                    True,
                ),
            ],
        ),
        (
            "house rules",
            """
            Hausordnung der Wohnanlage Findorff

            Ruhezeiten: Von 22 bis 7 Uhr und sonntags ist Ruhe. Bitte keine laute Musik.
            Müll: Der Müll wird in die Container im Innenhof geworfen. Glas bitte nur
            werktags zwischen 8 und 20 Uhr.
            Fahrräder: Fahrräder gehören in den Fahrradkeller, nicht in den Hausflur.
            Reparaturen: Melden Sie Schäden bitte sofort dem Hausmeister, Telefon 0421 55 81.
            Feiern: Wer eine Party plant, informiert seine Nachbarn bitte eine Woche vorher.
            """,
            [
                (
                    "Am Sonntag …",
                    "soll es im Haus ruhig sein.",
                    "darf man laut Musik hören.",
                    "wird der Müll abgeholt.",
                ),
                (
                    "Glas darf man wegwerfen …",
                    "an Werktagen von 8 bis 20 Uhr.",
                    "jeden Tag rund um die Uhr.",
                    "nur am Sonntag.",
                ),
                (
                    "Fahrräder …",
                    "stellt man in den Keller.",
                    "darf man in den Flur stellen.",
                    "sind im Haus verboten.",
                ),
                (
                    "Vor einer Party …",
                    "soll man die Nachbarn informieren.",
                    "muss man den Hausmeister fragen.",
                    "muss man eine Gebühr bezahlen.",
                ),
            ],
        ),
    ),
    # Modul 2 (Lektionen 4-6): complaints, technology, invitations.
    2: _set(
        (
            """
            Ärger mit der neuen Waschmaschine

            Vor sechs Wochen habe ich online eine Waschmaschine bestellt. Sie kam zwar
            pünktlich, aber schon nach drei Tagen lief Wasser in die Küche. Ich habe sofort
            beim Kundenservice angerufen und war eine halbe Stunde in der Warteschleife. Die
            Mitarbeiterin war freundlich und hat versprochen, dass ein Techniker kommt.
            Obwohl ich zwei Tage zu Hause gewartet habe, kam niemand. Erst nachdem ich eine
            schriftliche Reklamation geschickt hatte, bekam ich eine Antwort: Die Firma hat
            mir eine neue Maschine geliefert und mir sogar einen Gutschein geschenkt. Jetzt
            bin ich zufrieden, aber ich werde nächstes Mal im Geschäft kaufen.
            """,
            [
                ("Die Waschmaschine kam zu spät.", False),
                ("Nach drei Tagen hatte die Maschine ein Problem.", True),
                ("Der Autor musste am Telefon lange warten.", True),
                ("Der Techniker hat die Maschine repariert.", False),
                ("Nach der schriftlichen Reklamation bekam er eine neue Maschine.", True),
                ("Er will die nächste Maschine wieder online kaufen.", False),
            ],
        ),
        (
            """
            Wenn der Roboter den Rasen mäht

            Hannover. In immer mehr Gärten fahren kleine Roboter über den Rasen. Schon jeder
            zehnte Haushalt mit Garten hat einen. „Jetzt habe ich Zeit für meine Enkel“, sagt
            Klaus Petersen (58). Naturschützer warnen aber, dass die Geräte kleinen Tieren wie
            Igeln gefährlich werden, besonders in der Nacht. Sie raten deshalb, die Roboter nur
            tagsüber fahren zu lassen.
            """,
            [
                (
                    "Mähroboter gibt es …",
                    "in jedem zehnten Haushalt mit Garten.",
                    "in fast allen Gärten.",
                    "nur in Hannover.",
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
            ],
        ),
        (
            """
            Gäste aus aller Welt

            Leipzig. Was bringt man mit, wenn man eingeladen ist? Die Volkshochschule bietet
            seit Kurzem einen Kurs über Gastfreundschaft in verschiedenen Ländern an. „Viele
            Teilnehmer haben schon peinliche Situationen erlebt“, erzählt die Kursleiterin. In
            Deutschland bringt man oft Blumen oder Wein mit, in anderen Ländern ist ein
            Geschenk beim ersten Besuch unhöflich. Im Kurs kochen die Teilnehmer außerdem
            zusammen und probieren Gerichte aus vielen Ländern.
            """,
            [
                ("Der Kurs an der VHS ist …", "neu.", "schon sehr alt.", "nur für Köche."),
                (
                    "Viele Teilnehmer …",
                    "haben schon peinliche Situationen erlebt.",
                    "laden nie Gäste ein.",
                    "kommen aus Leipzig.",
                ),
                (
                    "Im Kurs …",
                    "kochen die Teilnehmer zusammen.",
                    "kauft man Geschenke.",
                    "lernt man nur Deutsch.",
                ),
            ],
        ),
        (
            {
                "a": "Computerhilfe zu Hause: Wir installieren Programme und retten verlorene Dateien. Auch abends.",
                "b": "Kochkurs „Gäste verwöhnen“: Menüs mit Vorspeise, Hauptspeise und Nachtisch.",
                "c": "Partyservice Lecker: Buffets für Feste mit 20 bis 200 Gästen, auch vegetarisch.",
                "d": "Kurs „Gut telefonieren“: Professionell mit Kunden sprechen und Reklamationen lösen.",
                "e": "Gebrauchte Laptops und Monitore günstig, mit Garantie und Lieferung frei Haus.",
                "f": "Knigge-Seminar: richtig verhalten beim Geschäftsessen. Tischmanieren und Small Talk.",
                "g": "Verbraucherberatung: Hilfe bei Problemen mit Verträgen, Abos und Kündigungen.",
                "h": "Blumen Rosi: Blumensträuße für jeden Anlass, Lieferung am selben Tag.",
                "i": "Handyreparatur in 30 Minuten: neue Batterie, neuer Bildschirm, faire Preise.",
                "j": "Restaurant Seeblick: Räume für Geburtstage und Hochzeiten bis 80 Personen.",
            },
            [
                (
                    "Frau Yilmaz feiert ihre Hochzeit mit 120 Gästen und will nicht selbst kochen.",
                    "c",
                ),
                ("Herr Roth hat aus Versehen wichtige Dateien gelöscht.", "a"),
                ("Jan beginnt im Kundenservice und hat Angst vor schwierigen Anrufen.", "d"),
                ("Lena hat bald ein wichtiges Essen mit Geschäftspartnern.", "f"),
                ("Ihr Handy geht nicht mehr, weil der Bildschirm kaputt ist.", "i"),
                ("Herr Krüger möchte ein Abo kündigen, aber die Firma reagiert nicht.", "g"),
                ("Tim sucht einen neuen Fernseher mit großem Bildschirm.", NO_AD),
            ],
        ),
        (
            "Sollte man Kinder schon früh mit Computern und Tablets lernen lassen?",
            [
                (
                    "Petra (42)",
                    "Meine Kinder lernen in der Schule mit Tablets, und sie sind begeistert. Die Welt wird immer digitaler, also müssen sie das früh lernen.",
                    True,
                ),
                (
                    "Herr Lang (66)",
                    "Kinder sollten draußen spielen und Bücher lesen. Bildschirme machen sie unruhig. Ich halte davon gar nichts.",
                    False,
                ),
                (
                    "Selma (35)",
                    "Eine Stunde am Tag finde ich in Ordnung. Es gibt sehr gute Lernprogramme, mit denen meine Tochter Mathematik übt.",
                    True,
                ),
                (
                    "Kai (29)",
                    "Ich arbeite als Programmierer und kann Ihnen sagen: Die Grundlagen lernt man auch mit zwölf noch schnell genug. Kleine Kinder brauchen keine Tablets.",
                    False,
                ),
                (
                    "Frau Becker (51)",
                    "Als Lehrerin sehe ich jeden Tag, wie Kinder mit Tablets schneller lesen lernen. Natürlich nur zusammen mit einem Erwachsenen.",
                    True,
                ),
                (
                    "Anton (17)",
                    "Ich habe mit vier mein erstes Tablet bekommen und war danach süchtig. Ich würde meinen Kindern lieber noch keins geben.",
                    False,
                ),
                (
                    "Nina (38)",
                    "Verbieten bringt nichts. Ich finde es besser, wenn Kinder früh lernen, vernünftig mit Technik umzugehen.",
                    True,
                ),
            ],
        ),
        (
            "instructions",
            """
            Rückgabe und Reklamation bei Technikwelt

            Sie können jedes Gerät innerhalb von 14 Tagen ohne Grund zurückgeben. Bitte
            bringen Sie dafür die Rechnung mit. Ist ein Gerät kaputt, haben Sie zwei Jahre
            Garantie. Rufen Sie in diesem Fall zuerst unseren Kundendienst an (Taste 3).
            Online gekaufte Geräte können Sie kostenlos per Post zurückschicken. Bei
            geöffneten Computerprogrammen ist eine Rückgabe leider nicht möglich.
            """,
            [
                (
                    "Innerhalb von 14 Tagen kann man ein Gerät …",
                    "ohne Grund zurückgeben.",
                    "nur mit Grund zurückgeben.",
                    "nicht zurückgeben.",
                ),
                (
                    "Für die Rückgabe braucht man …",
                    "die Rechnung.",
                    "die Garantie.",
                    "einen Termin.",
                ),
                (
                    "Wenn ein Gerät kaputt ist, soll man zuerst …",
                    "den Kundendienst anrufen.",
                    "das Gerät zurückschicken.",
                    "ins Geschäft kommen.",
                ),
                (
                    "Geöffnete Computerprogramme …",
                    "kann man nicht zurückgeben.",
                    "kann man immer zurückgeben.",
                    "kosten weniger.",
                ),
            ],
        ),
    ),
    # Modul 3 (Lektionen 7-9): pets, careers, health at work.
    3: _set(
        (
            """
            Wie Bello mein Leben verändert hat

            Lange habe ich überlegt, ob ich mir einen Hund anschaffen soll. Ich arbeite viel
            und wohne in einer kleinen Wohnung. Dann habe ich im Tierheim Bello kennengelernt,
            einen alten, sehr ruhigen Hund. Zum Glück darf ich ihn mit ins Büro bringen. Jetzt
            gehe ich jeden Mittag mit ihm spazieren, statt am Schreibtisch zu essen. Seitdem
            habe ich viel weniger Rückenschmerzen. Ein Problem gibt es aber: Bello frisst
            alles, was er findet, und der Tierarzt war schon dreimal teuer. Trotzdem bereue ich
            meine Entscheidung keinen einzigen Tag.
            """,
            [
                ("Die Autorin hat sich schnell für einen Hund entschieden.", False),
                ("Bello kommt aus dem Tierheim.", True),
                ("Bello darf mit ins Büro.", True),
                ("Mittags isst die Autorin am Schreibtisch.", False),
                ("Seit sie den Hund hat, hat sie weniger Rückenschmerzen.", True),
                ("Der Tierarzt war noch nie nötig.", False),
            ],
        ),
        (
            """
            Ein Büro für Hunde

            Köln. In der Agentur „Blickfang“ arbeiten 14 Menschen und fünf Hunde. „Am Anfang
            hatten einige Kollegen Angst“, erzählt die Chefin. „Deshalb haben wir Regeln
            gemacht: Die Hunde dürfen nicht in die Küche, und wer allergisch ist, bekommt ein
            Büro ohne Tiere.“ Eine Studie zeigt, dass Hunde im Büro den Stress reduzieren, weil
            die Mitarbeiter öfter Pausen machen.
            """,
            [
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
                    "Hunde reduzieren den Stress, weil …",
                    "die Mitarbeiter öfter Pausen machen.",
                    "sie leise sind.",
                    "die Mitarbeiter weniger arbeiten.",
                ),
            ],
        ),
        (
            """
            Der Test, der den Beruf verrät?

            Berlin. Jedes Jahr machen Tausende Schüler einen Berufstest im Internet. Die Tests
            fragen zum Beispiel, ob man lieber mit Menschen oder mit Maschinen arbeitet.
            Berufsberater finden die Tests nützlich, warnen aber: „Ein Test kann nur einen
            ersten Hinweis geben.“ Wichtiger sei ein Praktikum, weil man dort den Alltag in
            einem Beruf wirklich kennenlernt. Viele Schüler sind vom Ergebnis überrascht.
            """,
            [
                (
                    "Die Tests fragen zum Beispiel, …",
                    "ob man lieber mit Menschen oder Maschinen arbeitet.",
                    "wie viel man verdienen möchte.",
                    "welche Noten man hat.",
                ),
                (
                    "Berufsberater meinen, dass ein Test …",
                    "nur ein erster Hinweis ist.",
                    "immer richtig ist.",
                    "unnötig ist.",
                ),
                (
                    "Wichtiger als ein Test ist laut Beratern …",
                    "ein Praktikum.",
                    "ein Gespräch mit den Eltern.",
                    "ein gutes Zeugnis.",
                ),
            ],
        ),
        (
            {
                "a": "Tierheim Pfötchen sucht Gassigeher für das Wochenende.",
                "b": "Meerschweinchen abzugeben: zwei junge Tiere mit Käfig, sehr zutraulich.",
                "c": "Berufsberatung für Erwachsene: Wir helfen Ihnen, einen neuen Beruf zu finden.",
                "d": "Fitnessstudio Aktiv: Rückenkurse für Menschen, die viel sitzen.",
                "e": "Tierarztpraxis Dr. Behr: Notdienst rund um die Uhr.",
                "f": "Präsentieren lernen: Halten Sie Vorträge sicher. Abendkurs, 4 Termine.",
                "g": "Nichtraucher in 6 Wochen: Kurs der Krankenkasse, kostenlos für Mitglieder.",
                "h": "Hundeschule Fuchs: Ihr Hund lernt hören, auch für ältere Hunde.",
                "i": "Yoga in der Mittagspause: 30 Minuten Entspannung direkt neben Ihrem Büro.",
                "j": "Ausbildungsmesse am Samstag: über 80 Firmen stellen Berufe vor.",
            },
            [
                ("Herr Lange ist 45 und möchte etwas ganz anderes machen.", "c"),
                ("Familie Becker sucht ein Haustier für ihre Tochter, aber keinen Hund.", "b"),
                ("Frau Wolf liebt Hunde, darf aber in ihrer Wohnung keine Tiere haben.", "a"),
                ("Ihre Katze ist am Sonntagabend plötzlich krank.", "e"),
                ("Milan muss seiner Firma bald ein Projekt vorstellen und ist nervös.", "f"),
                ("Sandra raucht seit zehn Jahren und möchte aufhören.", "g"),
                ("Herr Ott sucht einen Kurs, in dem er Kochen für Diabetiker lernt.", NO_AD),
            ],
        ),
        (
            "Sollte jeder Arbeitgeber seinen Mitarbeitern Sport anbieten?",
            [
                (
                    "Clara (34)",
                    "In meiner Firma gibt es zweimal pro Woche Yoga. Seitdem fühle ich mich viel besser und bin seltener krank. Das sollte es überall geben.",
                    True,
                ),
                (
                    "Herr Brinkmann (59)",
                    "Sport ist Privatsache. Die Firma soll gute Gehälter zahlen, dann kann jeder selbst entscheiden, was er in seiner Freizeit macht.",
                    False,
                ),
                (
                    "Deniz (27)",
                    "Ich finde das super, weil ich nach der Arbeit keine Zeit mehr habe. So bewege ich mich wenigstens ein bisschen.",
                    True,
                ),
                (
                    "Frau Ullrich (48)",
                    "Ich arbeite in einem kleinen Betrieb mit fünf Leuten. Für uns ist so etwas viel zu teuer. Man kann das nicht von jeder Firma verlangen.",
                    False,
                ),
                (
                    "Paul (41)",
                    "Gesunde Mitarbeiter arbeiten besser. Am Ende spart die Firma also Geld. Ich bin klar dafür.",
                    True,
                ),
                (
                    "Lea (23)",
                    "Ich möchte nicht mit meinem Chef Gymnastik machen, das wäre mir peinlich. Ich gehe lieber allein ins Fitnessstudio.",
                    False,
                ),
                (
                    "Herr Kaya (52)",
                    "Seit wir eine Betriebssportgruppe haben, ist die Atmosphäre im Team viel besser. Ich kann es jeder Firma empfehlen.",
                    True,
                ),
            ],
        ),
        (
            "instructions",
            """
            Hinweise für Mitarbeiter: Gesundheitstag am 14. Mai

            Der Gesundheitstag findet von 9 bis 15 Uhr in der Kantine und in Halle A statt.
            Die Teilnahme ist freiwillig und zählt als Arbeitszeit. Für die Kurse am Vormittag
            melden Sie sich bitte bis zum 10. Mai bei Frau Hartmann an. Bringen Sie bequeme
            Kleidung mit. Das Mittagessen ist an diesem Tag kostenlos. Wer nicht kommen kann,
            findet alle Informationen danach im Intranet.
            """,
            [
                (
                    "Die Teilnahme am Gesundheitstag …",
                    "ist freiwillig.",
                    "ist Pflicht.",
                    "kostet Geld.",
                ),
                (
                    "Für die Kurse am Vormittag muss man sich …",
                    "bis zum 10. Mai anmelden.",
                    "nicht anmelden.",
                    "am 14. Mai anmelden.",
                ),
                (
                    "Man soll mitbringen: …",
                    "bequeme Kleidung.",
                    "ein Mittagessen.",
                    "einen Laptop.",
                ),
                (
                    "Wer nicht teilnimmt, …",
                    "findet die Informationen im Intranet.",
                    "muss einen Bericht schreiben.",
                    "bekommt kein Mittagessen.",
                ),
            ],
        ),
    ),
    # Modul 4 (Lektionen 10-12): mishaps, happiness, company events.
    4: _set(
        (
            """
            Der schlimmste und der schönste Tag

            Letzten Freitag ist bei mir alles schiefgegangen. Zuerst habe ich verschlafen,
            dann habe ich meinen Schlüssel in der Wohnung vergessen. Weil ich zu spät kam, habe
            ich den Zug zum Vorstellungsgespräch verpasst. Hätte ich doch nur den Wecker
            gestellt! Am Bahnhof habe ich mich furchtbar geärgert, bis eine Frau mich ansprach:
            Sie hatte denselben Zug verpasst und musste zum selben Termin. Wir haben zusammen
            ein Taxi genommen und sind gerade noch pünktlich angekommen. Jetzt sind wir beide
            Kolleginnen, und ich habe eine neue Freundin gefunden.
            """,
            [
                ("Die Autorin ist am Freitag zu spät aufgestanden.", True),
                ("Sie hat ihr Handy zu Hause vergessen.", False),
                ("Sie hat den Zug noch bekommen.", False),
                ("Die Frau am Bahnhof hatte das gleiche Problem.", True),
                ("Die beiden kamen zu spät zum Termin.", False),
                ("Heute arbeiten die beiden in derselben Firma.", True),
            ],
        ),
        (
            """
            Der verlorene Lottoschein

            Graz. Weil sie ihren Lottoschein im Bus liegen gelassen hatte, dachte Hilde M. (72)
            wochenlang, dass ihr Gewinn verloren war. Der Busfahrer hatte den Schein jedoch im
            Fundbüro abgegeben. Nachdem eine Zeitung darüber berichtet hatte, meldete sich Frau
            M. dort und bekam 4.200 Euro. Einen Teil schenkte sie dem Busfahrer.
            """,
            [
                (
                    "Frau M. hat ihren Lottoschein …",
                    "im Bus liegen gelassen.",
                    "zu Hause verloren.",
                    "nie gekauft.",
                ),
                (
                    "Frau M. meldete sich im Fundbüro, nachdem …",
                    "eine Zeitung berichtet hatte.",
                    "der Busfahrer sie angerufen hatte.",
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
            Wenn Kollegen feiern

            München. Fast jede zweite Firma in Deutschland organisiert jedes Jahr eine
            Weihnachtsfeier. Für viele Mitarbeiter ist das eine gute Gelegenheit, Kollegen aus
            anderen Abteilungen kennenzulernen. Experten raten aber, bei der Feier nicht zu viel
            Alkohol zu trinken und keine Witze über den Chef zu machen. Beliebte Themen für den
            Small Talk sind Urlaub, Sport und Essen.
            """,
            [
                (
                    "Eine Weihnachtsfeier organisiert …",
                    "fast jede zweite Firma.",
                    "jede Firma.",
                    "nur jede zehnte Firma.",
                ),
                (
                    "Auf der Feier lernt man oft …",
                    "Kollegen aus anderen Abteilungen kennen.",
                    "neue Kunden kennen.",
                    "den neuen Chef kennen.",
                ),
                (
                    "Experten raten, …",
                    "nicht zu viel Alkohol zu trinken.",
                    "über den Chef zu sprechen.",
                    "früh nach Hause zu gehen.",
                ),
            ],
        ),
        (
            {
                "a": "Schlüsseldienst Notfall: Tür zugefallen? Wir sind in 30 Minuten da, Tag und Nacht.",
                "b": "Glücksbringer aus Holz: Geschenke für Hochzeiten, Geburten und Prüfungen.",
                "c": "Biergarten am See: Platz für Betriebsausflüge bis 150 Personen, mit Bootsfahrt.",
                "d": "Abschleppdienst Krause: Panne auf der Autobahn? Wir helfen schnell.",
                "e": "Fundbüro der Stadt: Haben Sie etwas verloren? Montag bis Freitag 8–16 Uhr.",
                "f": "Rednerkurs: die perfekte Rede für Ihre Feier oder Ihr Jubiläum.",
                "g": "Fotostudio Moment: Fotos für Hochzeiten, Jubiläen und Firmenfeiern.",
                "h": "Partyzelt-Verleih: Zelte, Tische und Bänke für Sommerfeste.",
                "i": "Reinigung Blitz: Flecken auf Ihrem Anzug? Morgen ist er wie neu.",
                "j": "Tanzschule Schwung: Tanzkurse für Paare vor der Hochzeit.",
            },
            [
                ("Herr Sommer kommt nicht in seine Wohnung, weil der Schlüssel drinnen ist.", "a"),
                ("Frau Kaya organisiert einen Ausflug für 90 Kollegen.", "c"),
                ("Lukas hat seine Brieftasche in der Straßenbahn verloren.", "e"),
                ("Anna sucht ein Geschenk für ihre Schwester, die ein Baby bekommen hat.", "b"),
                ("Herr Wolf soll beim Firmenjubiläum sprechen.", "f"),
                ("Auf Pauls Hemd ist ein Rotweinfleck, und morgen ist eine Feier.", "i"),
                ("Familie Neumann sucht einen Koch für ein Fest zu Hause.", NO_AD),
            ],
        ),
        (
            "Sind Betriebsfeiern eine gute Idee?",
            [
                (
                    "Svenja (29)",
                    "Ich freue mich jedes Jahr auf unser Sommerfest. Man lernt die Kollegen ganz anders kennen, und das hilft später bei der Arbeit.",
                    True,
                ),
                (
                    "Herr Graf (55)",
                    "Nach acht Stunden im Büro möchte ich nach Hause zu meiner Familie, nicht noch mit Kollegen feiern. Darauf kann ich verzichten.",
                    False,
                ),
                (
                    "Mehmet (36)",
                    "Als ich neu in der Firma war, habe ich auf der Weihnachtsfeier meine besten Kollegen kennengelernt. Ohne die Feier wäre das nie passiert.",
                    True,
                ),
                (
                    "Julia (42)",
                    "Bei uns trinken immer einige zu viel, und am nächsten Tag ist die Stimmung schlecht. Ich gehe nicht mehr hin.",
                    False,
                ),
                (
                    "Frau Lenz (61)",
                    "Ein Betriebsausflug im Jahr ist eine schöne Tradition. Ich finde, eine Firma sollte das unbedingt weitermachen.",
                    True,
                ),
                (
                    "Tom (25)",
                    "Mich stört, dass man fast hingehen muss. Wer nicht kommt, gilt schnell als unfreundlich. Das ist keine echte Feier.",
                    False,
                ),
                (
                    "Herr Ahmadi (47)",
                    "Feiern ist gut für das Team. Wichtig ist nur, dass die Feier während der Arbeitszeit stattfindet. Dann kommen auch alle gern.",
                    True,
                ),
            ],
        ),
        (
            "rules",
            """
            Fundbüro der Stadt Seeburg: Informationen

            Gefundene Sachen können Sie in jedem Bürgerbüro abgeben. Wir bewahren sie sechs
            Monate auf. Wenn Sie etwas verloren haben, können Sie auch online suchen. Für die
            Abholung brauchen Sie Ihren Ausweis. Bei Sachen mit einem Wert über 50 Euro
            bezahlen Sie eine kleine Gebühr. Fundsachen aus Bussen und Bahnen sind die ersten
            drei Tage noch bei den Verkehrsbetrieben.
            """,
            [
                (
                    "Gefundene Sachen bleiben im Fundbüro …",
                    "sechs Monate.",
                    "drei Tage.",
                    "ein Jahr.",
                ),
                ("Zum Abholen braucht man …", "seinen Ausweis.", "eine Rechnung.", "einen Termin."),
                (
                    "Eine Gebühr bezahlt man, …",
                    "wenn die Sache mehr als 50 Euro wert ist.",
                    "immer.",
                    "nie.",
                ),
                (
                    "Wer etwas im Bus verloren hat, …",
                    "fragt zuerst bei den Verkehrsbetrieben.",
                    "muss sechs Monate warten.",
                    "bekommt es nicht zurück.",
                ),
            ],
        ),
    ),
    # Modul 5 (Lektionen 13-15): misunderstandings, courses, applications.
    5: _set(
        (
            """
            Mein Vorstellungsgespräch auf Deutsch

            Gestern hatte ich mein erstes Vorstellungsgespräch auf Deutsch. Ich hatte mich
            gut vorbereitet und sogar einen Kurs an der Volkshochschule gemacht. Trotzdem war
            ich sehr nervös. Als die Personalleiterin fragte, wo meine Stärken liegen, habe
            ich die Frage falsch verstanden und über meinen Wohnort erzählt! Sie hat gelacht,
            und ich habe noch einmal nachgefragt. Danach lief das Gespräch richtig gut. Ich
            konnte zeigen, dass ich sowohl Erfahrung im Verkauf als auch gute
            Computerkenntnisse habe. Heute Morgen kam die Zusage: Ich fange am ersten März an!
            """,
            [
                ("Die Autorin hatte sich auf das Gespräch vorbereitet.", True),
                ("Sie war im Gespräch ganz ruhig.", False),
                ("Sie hat eine Frage falsch verstanden.", True),
                ("Die Personalleiterin war unfreundlich.", False),
                ("Sie hat Erfahrung im Verkauf.", True),
                ("Sie hat die Stelle nicht bekommen.", False),
            ],
        ),
        (
            """
            Teekesselchen im Supermarkt

            Mainz. Die Spanierin Lucía Gómez (29) fragte im Supermarkt nach „Birnen“, weil sie
            Glühbirnen brauchte, und der Verkäufer zeigte ihr Obst. Wörter mit zwei Bedeutungen
            heißen im Deutschen „Teekesselchen“. Eine Lehrerin rät, in solchen Situationen
            einfach nachzufragen. Lucía hat über ihre Erfahrungen sogar ein kleines Buch
            geschrieben.
            """,
            [
                (
                    "Lucía wollte im Supermarkt …",
                    "Glühbirnen kaufen.",
                    "Obst kaufen.",
                    "eine Lampe kaufen.",
                ),
                (
                    "Ein Teekesselchen ist …",
                    "ein Wort mit zwei Bedeutungen.",
                    "ein Getränk.",
                    "ein Kurs.",
                ),
                (
                    "Die Lehrerin rät, …",
                    "nachzufragen.",
                    "nichts zu sagen.",
                    "ein Wörterbuch zu kaufen.",
                ),
            ],
        ),
        (
            """
            Lernen ein Leben lang

            Bonn. Die Volkshochschulen haben so viele Teilnehmer wie nie zuvor. Besonders
            beliebt sind Sprachkurse und Kurse für den Beruf, zum Beispiel Bewerbungstraining.
            Auch immer mehr Senioren melden sich an, viele für Computerkurse. „Vorkenntnisse
            braucht man bei uns nicht“, sagt eine Sprecherin. Die Kurse sind günstig, weil sie
            vom Staat unterstützt werden.
            """,
            [
                (
                    "Die Volkshochschulen haben …",
                    "mehr Teilnehmer als je zuvor.",
                    "weniger Teilnehmer als früher.",
                    "keine Sprachkurse mehr.",
                ),
                (
                    "Viele Senioren besuchen …",
                    "Computerkurse.",
                    "Bewerbungstraining.",
                    "Sportkurse.",
                ),
                (
                    "Die Kurse sind günstig, weil …",
                    "der Staat sie unterstützt.",
                    "die Lehrer kein Geld bekommen.",
                    "sie online sind.",
                ),
            ],
        ),
        (
            {
                "a": "Bewerbungsfotos im Studio: professionell und schnell.",
                "b": "Klettern für Anfänger: Keine Vorkenntnisse nötig. Teilnahme auf eigene Gefahr.",
                "c": "Deutsch für den Beruf (B1/B2): Telefonieren, E-Mails, Besprechungen.",
                "d": "Übersetzungsbüro Klar: Zeugnisse und Dokumente in 30 Sprachen.",
                "e": "Nähkurs am Abend: Kleidung selbst nähen und reparieren.",
                "f": "Training Vorstellungsgespräch: Üben Sie mit echten Personalleitern.",
                "g": "Stellenbörse Gastronomie: Jobs in Küche und Service, auch Teilzeit.",
                "h": "Lebenslauf-Check: Wir prüfen Ihre Bewerbung, bevor Sie sie abschicken.",
                "i": "Fotokurs für Senioren: Grundlagen der Fotografie mit dem Handy.",
                "j": "Sprachcafé: Deutsch sprechen mit Muttersprachlern, jeden Donnerstag.",
            },
            [
                ("Herr Ali hat seine Zeugnisse auf Arabisch und braucht sie auf Deutsch.", "d"),
                ("Frau Novak hat im Büro Probleme am Telefon.", "c"),
                ("Ben hat nächste Woche sein erstes Vorstellungsgespräch.", "f"),
                ("Julia braucht für ihre Bewerbung ein gutes Foto.", "a"),
                ("Paul möchte einen neuen, etwas gefährlichen Sport ausprobieren.", "b"),
                ("Herr Fischer (70) möchte lernen, mit seinem Handy schöne Bilder zu machen.", "i"),
                ("Mia sucht einen Kurs, in dem sie Gitarre spielen lernt.", NO_AD),
            ],
        ),
        (
            "Sollte jeder Arbeitnehmer regelmäßig eine Weiterbildung machen müssen?",
            [
                (
                    "Herr Stein (44)",
                    "In meinem Beruf ändert sich alles sehr schnell. Ohne Weiterbildung wäre ich nach ein paar Jahren nicht mehr gut. Ich finde das richtig.",
                    True,
                ),
                (
                    "Olga (38)",
                    "Ich lerne gern, aber ein Muss finde ich falsch. Jeder sollte selbst entscheiden, wann er einen Kurs macht.",
                    False,
                ),
                (
                    "Benni (26)",
                    "Weiterbildungen sind die beste Chance, mehr Geld zu verdienen. Ich wäre für eine Pflicht, wenn die Firma sie bezahlt.",
                    True,
                ),
                (
                    "Frau Möller (60)",
                    "Ich gehe in zwei Jahren in Rente. Warum sollte ich jetzt noch einen Kurs machen? Für ältere Leute ist das sinnlos.",
                    False,
                ),
                (
                    "Ali (33)",
                    "Wer sich weiterbildet, ist sicherer, wenn die Firma Personal abbaut. Deshalb sollten alle mitmachen.",
                    True,
                ),
                (
                    "Herr Wendt (51)",
                    "Viele Kurse sind langweilig und bringen nichts für die Praxis. Lieber lerne ich direkt bei der Arbeit.",
                    False,
                ),
                (
                    "Carla (29)",
                    "Bei uns gibt es eine Weiterbildung pro Jahr für alle, und die Stimmung im Team ist dadurch besser geworden. Ich bin dafür.",
                    True,
                ),
            ],
        ),
        (
            "rules",
            """
            Anmeldebedingungen der Volkshochschule

            Sie können sich online, per Post oder persönlich anmelden. Die Kursgebühr müssen
            Sie vor dem ersten Termin bezahlen. Wenn Sie sich bis zwei Wochen vor Kursbeginn
            abmelden, bekommen Sie das Geld zurück. Bei Kletter- und Sportkursen ist die
            Teilnahme auf eigene Gefahr. Fällt ein Kurs aus, informieren wir Sie per E-Mail.
            """,
            [
                (
                    "Die Kursgebühr bezahlt man …",
                    "vor dem ersten Termin.",
                    "nach dem Kurs.",
                    "am letzten Tag.",
                ),
                (
                    "Das Geld bekommt man zurück, wenn man sich …",
                    "zwei Wochen vor Kursbeginn abmeldet.",
                    "nach dem ersten Termin abmeldet.",
                    "nie abmeldet.",
                ),
                (
                    "Bei Sportkursen …",
                    "ist man selbst verantwortlich.",
                    "zahlt die VHS bei einem Unfall.",
                    "braucht man einen Arzttermin.",
                ),
                (
                    "Wenn ein Kurs ausfällt, …",
                    "bekommt man eine E-Mail.",
                    "ruft die VHS an.",
                    "steht es in der Zeitung.",
                ),
            ],
        ),
    ),
    # Modul 6 (Lektionen 16-18): memories, art, politics.
    6: _set(
        (
            """
            Das Tagebuch meiner Großmutter

            Beim Aufräumen habe ich auf dem Dachboden das alte Tagebuch meiner Großmutter
            gefunden. Sie hat es mit 15 Jahren geschrieben, kurz nach dem Krieg. Damals
            brauchte sie nicht in die Schule zu gehen, wenn auf dem Feld viel Arbeit war.
            Taschengeld bekam sie nie, aber sie schreibt, dass sie trotzdem sehr glücklich
            war. Besonders gern hat sie gemalt, am liebsten Hügel und Blumen. Es fällt mir
            schwer, mir ihr Leben damals vorzustellen. Ich habe das Tagebuch meiner Mutter
            gezeigt, und wir wollen es jetzt zusammen abschreiben, damit es nicht verloren geht.
            """,
            [
                ("Das Tagebuch lag auf dem Dachboden.", True),
                ("Die Großmutter schrieb es als Erwachsene.", False),
                ("Wenn es viel Arbeit gab, musste sie nicht zur Schule.", True),
                ("Sie bekam jede Woche Taschengeld.", False),
                ("Die Großmutter malte gern.", True),
                ("Die Autorin will das Tagebuch verkaufen.", False),
            ],
        ),
        (
            """
            Eine Malerin kehrt zurück

            Murnau. Das Schlossmuseum zeigt eine Ausstellung über die Malerin Elsa Hoff
            (1890–1962). Als Frau durfte sie zuerst nicht an der Kunstakademie studieren und
            nahm deshalb privaten Unterricht. Im Krieg wurden viele ihrer Werke zerstört. Erst
            als ihr Enkel vor drei Jahren 40 Gemälde auf einem Dachboden entdeckte, interessierte
            man sich wieder für sie.
            """,
            [
                (
                    "Elsa Hoff durfte zuerst nicht an der Akademie studieren, weil …",
                    "sie eine Frau war.",
                    "sie kein Geld hatte.",
                    "sie krank war.",
                ),
                (
                    "Im Krieg …",
                    "wurden viele Bilder zerstört.",
                    "wurde sie berühmt.",
                    "malte sie besonders viel.",
                ),
                (
                    "Ihr Enkel …",
                    "fand 40 Bilder auf einem Dachboden.",
                    "ist auch Maler.",
                    "leitet das Museum.",
                ),
            ],
        ),
        (
            """
            Junge Leute und die Politik

            Berlin. Jugendliche interessieren sich zwar wenig für Parteien, aber sehr für
            Themen wie Klimaschutz und Gerechtigkeit. Das zeigt eine neue Studie. Viele
            engagieren sich ehrenamtlich oder gehen auf Demonstrationen. Weder Zeitungen noch
            Fernsehen sind für sie wichtige Informationsquellen; sie informieren sich vor allem
            online. Fast zwei Drittel möchten schon mit 16 wählen dürfen.
            """,
            [
                (
                    "Jugendliche interessieren sich besonders für …",
                    "Themen wie Klimaschutz.",
                    "Parteien.",
                    "das Fernsehen.",
                ),
                (
                    "Informationen bekommen sie vor allem …",
                    "online.",
                    "aus der Zeitung.",
                    "im Fernsehen.",
                ),
                (
                    "Fast zwei Drittel der Jugendlichen …",
                    "möchten mit 16 wählen.",
                    "sind in einer Partei.",
                    "gehen nie wählen.",
                ),
            ],
        ),
        (
            {
                "a": "Erzählcafé: Senioren erzählen Jugendlichen von früher. Jeden ersten Dienstag.",
                "b": "Malkurs für Erwachsene: Landschaften in Öl, mit Pinsel und Spachtel.",
                "c": "Wahl-Info-Abend: Alle Parteien stellen ihre Programme vor.",
                "d": "Die Tafel sucht Helfer, die Lebensmittel an Bedürftige verteilen.",
                "e": "Kunstreise nach Wien: Museen und Galerien in vier Tagen.",
                "f": "Familienberatung: Hilfe bei Streit zwischen Eltern und Kindern.",
                "g": "Ahnenforschung: Wir helfen Ihnen, Ihre Familiengeschichte zu finden.",
                "h": "Bürgerinitiative „Grüner Park“ sucht Unterstützer gegen das neue Parkhaus.",
                "i": "Galerie am Markt: Ausstellung junger Künstler, Eintritt frei.",
                "j": "Klavierunterricht für Kinder und Erwachsene, auch zu Hause.",
            },
            [
                ("Frau Berger ist Rentnerin und möchte Menschen in Not helfen.", "d"),
                ("Herr Kim weiß noch nicht, welche Partei er wählen soll.", "c"),
                ("Familie Roth streitet oft mit ihrer Tochter.", "f"),
                ("Mia möchte lernen, Berge und Seen zu malen.", "b"),
                ("Herr Lang möchte wissen, woher seine Urgroßeltern kamen.", "g"),
                ("Tim will gegen den Bau eines Parkhauses in seinem Stadtteil kämpfen.", "h"),
                ("Sara möchte am Wochenende einen Theaterkurs besuchen.", NO_AD),
            ],
        ),
        (
            "Sollten Jugendliche schon mit 16 wählen dürfen?",
            [
                (
                    "Leonie (16)",
                    "Wir müssen mit den Entscheidungen von heute am längsten leben. Deshalb sollten wir auch mitbestimmen dürfen.",
                    True,
                ),
                (
                    "Herr Schulze (63)",
                    "Mit 16 weiß man noch zu wenig über Politik. Ich finde 18 genau richtig.",
                    False,
                ),
                (
                    "Aylin (19)",
                    "Ich hätte mit 16 sehr gern gewählt. Viele in meiner Klasse haben sich damals für Politik interessiert.",
                    True,
                ),
                (
                    "Frau Hofer (47)",
                    "Jugendliche lassen sich zu leicht von Eltern oder vom Internet beeinflussen. Davon halte ich nicht viel.",
                    False,
                ),
                (
                    "Max (17)",
                    "Ich darf mit 17 Auto fahren lernen, aber nicht wählen? Das kann ich nicht nachvollziehen. Ich bin dafür.",
                    True,
                ),
                (
                    "Herr Brandt (52)",
                    "Ich bin Lehrer und sehe, dass die meisten Schüler sich weder für Parteien noch für Wahlen interessieren. Das bringt nichts.",
                    False,
                ),
                (
                    "Nora (35)",
                    "In einigen Bundesländern dürfen 16-Jährige schon bei Kommunalwahlen wählen, und das funktioniert gut. Warum nicht überall?",
                    True,
                ),
            ],
        ),
        (
            "rules",
            """
            Museumsordnung des Schlossmuseums

            Bitte geben Sie Taschen und Rucksäcke an der Garderobe ab. Fotografieren ist
            erlaubt, aber ohne Blitz. Essen und Trinken sind nur im Café erlaubt. Kinder unter
            12 Jahren dürfen das Museum nur mit Erwachsenen besuchen. Der Eintritt ist für
            Schüler und Studenten frei.
            """,
            [
                (
                    "Taschen und Rucksäcke …",
                    "gibt man an der Garderobe ab.",
                    "darf man mitnehmen.",
                    "sind im Museum verboten.",
                ),
                ("Fotos darf man machen, …", "aber ohne Blitz.", "nur mit Blitz.", "gar nicht."),
                (
                    "Kinder unter 12 Jahren …",
                    "brauchen eine erwachsene Begleitung.",
                    "dürfen nicht ins Museum.",
                    "zahlen keinen Eintritt.",
                ),
                (
                    "Studenten …",
                    "zahlen keinen Eintritt.",
                    "zahlen den halben Preis.",
                    "dürfen nur am Sonntag kommen.",
                ),
            ],
        ),
    ),
    # Modul 7 (Lektionen 19-21): tourism, mountain huts, concerts and cities.
    7: _set(
        (
            """
            Drei Tage in den Bergen

            Letztes Wochenende war ich mit zwei Freundinnen auf der Berghütte Edelweiß. Der Weg
            zum Gipfel war so steil, dass wir oft Pausen machen mussten. Oben war die Aussicht
            aber einmalig. In der Hütte haben wir im Lager mit zwanzig anderen Wanderern
            geschlafen, sodass es nachts ziemlich laut war. Zum Glück hatte ich Ohrstöpsel
            dabei. Der Hüttenwirt war streng: Jeder musste seinen Müll wieder mit ins Tal nehmen.
            Je länger ich darüber nachdenke, desto sinnvoller finde ich diese Regel. Nächstes
            Jahr wollen wir wiederkommen, dann aber im Herbst.
            """,
            [
                ("Die Autorin war allein auf der Hütte.", False),
                ("Der Weg zum Gipfel war anstrengend.", True),
                ("Sie hatte ein Einzelzimmer.", False),
                ("In der Nacht war es laut.", True),
                ("Den Müll konnte man in der Hütte lassen.", False),
                ("Sie möchte im nächsten Jahr wieder auf die Hütte.", True),
            ],
        ),
        (
            """
            Je mehr Gäste, desto weniger Ruhe?

            Lüneburger Heide. Im August blüht die Heide, und dann kommen die meisten
            Touristen. Je mehr Menschen kommen, desto größer werden die Probleme: Manche
            Besucher verlassen die Wege, sodass Tiere gestört werden. Man darf deshalb nur noch
            auf markierten Wegen wandern, und Hunde müssen an die Leine. Außerdem schützt man
            die Heide, indem man Schafe dort fressen lässt.
            """,
            [
                ("Die meisten Touristen kommen …", "im August.", "im Winter.", "im Frühling."),
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
            Konzertkarten in Minuten weg

            Hamburg. Innerhalb von nur 20 Minuten waren alle 40.000 Karten für das Konzert der
            Band Wonnetöne verkauft. Viele Fans sind enttäuscht. Der Veranstalter plant
            deshalb ein zweites Konzert außerhalb der Stadt. Die Karten dafür sollen nur online
            verkauft werden, und jeder darf höchstens zwei Karten kaufen.
            """,
            [
                (
                    "Die Karten waren …",
                    "in 20 Minuten verkauft.",
                    "nach 20 Tagen verkauft.",
                    "noch nicht im Verkauf.",
                ),
                (
                    "Das zweite Konzert findet …",
                    "außerhalb der Stadt statt.",
                    "im Zentrum statt.",
                    "im Ausland statt.",
                ),
                (
                    "Für das zweite Konzert darf man …",
                    "höchstens zwei Karten kaufen.",
                    "beliebig viele Karten kaufen.",
                    "Karten nur an der Kasse kaufen.",
                ),
            ],
        ),
        (
            {
                "a": "Stadtführung „Geheime Ecken“: zwei Stunden durch die Altstadt, auch für Kinder.",
                "b": "Berghütte Edelweiß: Übernachtung im Lager, Reservierung nötig.",
                "c": "Fahrradtour am Fluss entlang: 40 km, Leihräder vorhanden.",
                "d": "Musikschule: Gitarre und Schlagzeug für Anfänger.",
                "e": "Heidetour mit dem Schäfer: Schafe erleben und alles über Honig lernen.",
                "f": "Ticketservice: Karten für Konzerte, Theater und Sport in ganz Deutschland.",
                "g": "Bergschule Alpin: Kletterkurse mit Bergführern, Ausrüstung inklusive.",
                "h": "Hotel am Hafen: Zimmer mit Blick aufs Meer, Frühstück inklusive.",
                "i": "Museumsnacht: Alle Museen der Stadt sind bis Mitternacht geöffnet.",
                "j": "Busreisen Weber: Tagesfahrten zu Weihnachtsmärkten.",
            },
            [
                ("Familie Kaiser möchte die Stadt mit ihren Kindern entdecken.", "a"),
                ("Herr Ott sucht Karten für das Konzert seiner Lieblingsband.", "f"),
                ("Lea und Nils wollen in den Bergen übernachten.", "b"),
                ("Tim möchte in einer Band spielen, kann aber noch kein Instrument.", "d"),
                ("Frau Brandt fährt gern Rad, hat aber kein eigenes Fahrrad.", "c"),
                ("Jonas will das Klettern lernen, hat aber keine Ausrüstung.", "g"),
                ("Herr Yilmaz sucht einen Campingplatz am See.", NO_AD),
            ],
        ),
        (
            "Sollten Berghütten strenge Regeln haben?",
            [
                (
                    "Bernd (58)",
                    "Ohne Regeln würde auf den Hütten Chaos herrschen. Wenn 30 Leute in einem Raum schlafen, braucht man eine Nachtruhe.",
                    True,
                ),
                (
                    "Kim (24)",
                    "Ich gehe in die Berge, um frei zu sein. Wenn mir jemand sagt, wann ich schlafen muss, ist das nicht mehr Urlaub.",
                    False,
                ),
                (
                    "Frau Maier (44)",
                    "Ich finde es richtig, dass man seinen Müll wieder mitnehmen muss. Die Natur dankt es uns.",
                    True,
                ),
                (
                    "Lukas (31)",
                    "Manche Hüttenwirte übertreiben. Bei uns durfte man nicht einmal leise reden. Das ist zu viel.",
                    False,
                ),
                (
                    "Anja (36)",
                    "Mit Kindern bin ich froh über klare Regeln. So können alle gut schlafen und am nächsten Morgen früh losgehen.",
                    True,
                ),
                (
                    "Herr Wenger (67)",
                    "Früher gab es fast keine Regeln, und es hat trotzdem funktioniert. Die Leute haben einfach Rücksicht genommen.",
                    False,
                ),
                (
                    "Jana (28)",
                    "Regeln sind sinnvoll, weil heute viel mehr Menschen in die Berge kommen als früher. Ich bin dafür.",
                    True,
                ),
            ],
        ),
        (
            "rules",
            """
            Hüttenordnung der Berghütte Edelweiß

            Die Nachtruhe beginnt um 22 Uhr. Im Lager benutzen Sie bitte einen eigenen
            Schlafsack. Bergschuhe bleiben im Schuhraum. Müll nehmen Sie bitte wieder mit ins
            Tal. Duschen ist wegen Wassermangels nur drei Minuten erlaubt. Bezahlen können Sie
            nur bar.
            """,
            [
                (
                    "Ab 22 Uhr …",
                    "soll es ruhig sein.",
                    "gibt es Abendessen.",
                    "schließt die Hütte.",
                ),
                (
                    "Im Lager braucht man …",
                    "einen eigenen Schlafsack.",
                    "eine eigene Matratze.",
                    "keine Decke.",
                ),
                (
                    "Die Duschzeit ist kurz, weil …",
                    "es wenig Wasser gibt.",
                    "viele Gäste da sind.",
                    "das Wasser teuer ist.",
                ),
                ("Bezahlen kann man …", "nur mit Bargeld.", "nur mit Karte.", "erst im Tal."),
            ],
        ),
    ),
    # Modul 8 (Lektionen 22-24): history, environment, living together.
    8: _set(
        (
            """
            Ein Jahr ohne Auto

            Vor einem Jahr haben mein Mann und ich unser Auto verkauft. Statt mit dem Auto zu
            fahren, nehmen wir jetzt das Fahrrad oder den Bus. Am Anfang war das schwierig,
            besonders beim Einkaufen. Inzwischen haben wir ein Lastenrad, mit dem wir sogar die
            Getränkekisten transportieren können. Wir sparen viel Geld und sind fitter als
            früher. Nur im Winter, wenn es schneit, vermissen wir das Auto manchmal. Für lange
            Reisen nehmen wir den Zug, und unsere Nachbarn leihen uns ihr Auto, wenn wir es
            wirklich brauchen. Damit sind wir sehr zufrieden.
            """,
            [
                ("Die Familie hat ihr Auto verkauft.", True),
                ("Das Einkaufen war am Anfang leicht.", False),
                ("Mit dem Lastenrad können sie schwere Sachen transportieren.", True),
                ("Seit sie kein Auto haben, geben sie mehr Geld aus.", False),
                ("Im Winter fehlt ihnen das Auto manchmal.", True),
                ("Für lange Reisen mieten sie ein Auto.", False),
            ],
        ),
        (
            """
            Ein Dorf für alle Generationen

            Bei Kassel. Vor fünf Jahren haben sich zwölf Familien und acht Rentner
            zusammengeschlossen, um auf einem alten Bauernhof zu wohnen. Die Älteren kümmern
            sich um die Kinder, damit die Eltern arbeiten können. Anfangs gab es oft Streit,
            aber allmählich hat die Gruppe Kompromisse gefunden. „Es ist, als ob wir eine große
            Familie wären“, sagt eine Bewohnerin.
            """,
            [
                (
                    "Auf dem Bauernhof wohnen …",
                    "Familien und Rentner.",
                    "nur Rentner.",
                    "nur Studenten.",
                ),
                (
                    "Die Älteren kümmern sich um die Kinder, …",
                    "damit die Eltern arbeiten können.",
                    "weil sie Geld brauchen.",
                    "obwohl sie keine Zeit haben.",
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
            Zeitzeugen erzählen

            Berlin. Im Haus der Geschichte erzählen jeden Monat Menschen, wie sie den Fall der
            Mauer 1989 erlebt haben. Die Veranstaltung ist besonders bei Schulklassen beliebt.
            „Viele Jugendliche wissen kaum etwas über die DDR“, sagt die Organisatorin. Die
            Gespräche werden aufgenommen und später im Internet veröffentlicht.
            """,
            [
                (
                    "Die Zeitzeugen erzählen vom …",
                    "Fall der Mauer.",
                    "Bau der Mauer.",
                    "Ende des Krieges.",
                ),
                (
                    "Die Veranstaltung besuchen besonders oft …",
                    "Schulklassen.",
                    "Touristen.",
                    "Politiker.",
                ),
                (
                    "Die Gespräche …",
                    "kann man später im Internet sehen.",
                    "sind geheim.",
                    "werden nicht aufgenommen.",
                ),
            ],
        ),
        (
            {
                "a": "Repair-Café: Wir reparieren Fahrräder, Lampen und Kleidung.",
                "b": "Zeitzeugen gesucht: Haben Sie den Mauerfall erlebt?",
                "c": "Mehrgenerationenhaus: Wohnungen frei für Familien, die mit Älteren leben möchten.",
                "d": "Lastenräder zu mieten: Transportieren Sie Ihren Einkauf ohne Auto.",
                "e": "Sprachcafé: Menschen aus aller Welt sprechen Deutsch zusammen.",
                "f": "Kleidertausch: Bringen Sie Kleidung mit und nehmen Sie andere mit.",
                "g": "Stadtführung „Geteiltes Berlin“: auf den Spuren der Mauer.",
                "h": "Solarberatung: Strom vom eigenen Dach. Kostenlose Erstberatung.",
                "i": "Carsharing Grün: Autos in Ihrer Nähe, nur bezahlen, wenn Sie fahren.",
                "j": "Gemeinschaftsgarten sucht Mitglieder: Gemüse anbauen mit Nachbarn.",
            },
            [
                ("Herr Schulz hat 1989 in Berlin gewohnt und erzählt gern davon.", "b"),
                ("Familie Yilmaz möchte mit anderen Generationen unter einem Dach wohnen.", "c"),
                ("Lisas Fahrrad ist kaputt, aber sie will kein neues kaufen.", "a"),
                ("Frau Berg hat kein Auto und muss einen großen Einkauf nach Hause bringen.", "d"),
                ("Herr Weiß möchte auf seinem Haus Energie aus der Sonne produzieren.", "h"),
                ("Mara möchte gern mit anderen zusammen Tomaten und Salat anbauen.", "j"),
                ("Herr Koch sucht einen günstigen Flug nach Spanien.", NO_AD),
            ],
        ),
        (
            "Sollte die Innenstadt autofrei werden?",
            [
                (
                    "Sophie (31)",
                    "Endlich könnten Kinder sicher auf der Straße spielen, und die Luft wäre sauberer. Ich bin sofort dafür.",
                    True,
                ),
                (
                    "Herr Koch (64)",
                    "Ich kann nicht mehr gut laufen und brauche mein Auto. Für ältere Menschen wäre das eine Katastrophe.",
                    False,
                ),
                (
                    "Emre (27)",
                    "Ich fahre sowieso nur Rad. Statt neue Parkhäuser zu bauen, sollte die Stadt mehr Radwege bauen.",
                    True,
                ),
                (
                    "Frau Seidel (52)",
                    "Mein Geschäft lebt von Kunden, die mit dem Auto kommen. Ohne Parkplätze muss ich vielleicht schließen.",
                    False,
                ),
                (
                    "Lars (40)",
                    "In Kopenhagen funktioniert es super. Wenn es genug Busse gibt, ist eine autofreie Stadt viel schöner.",
                    True,
                ),
                (
                    "Herr Albers (46)",
                    "Die Idee ist zwar gut, aber zu radikal. Man sollte die Autos langsam reduzieren, nicht sofort verbieten.",
                    False,
                ),
                (
                    "Marie (19)",
                    "Ich bin froh über jeden Platz, wo man ohne Autolärm sitzen kann. Das macht die Stadt lebendig.",
                    True,
                ),
            ],
        ),
        (
            "rules",
            """
            Regeln im Gemeinschaftsgarten „Grüne Mitte“

            Jedes Mitglied bekommt ein eigenes Beet und hilft einmal im Monat bei der
            Gartenarbeit für alle. Werkzeug finden Sie im Gartenhaus; bitte bringen Sie es
            sauber zurück. Chemische Mittel sind nicht erlaubt. Das Gemüse aus den gemeinsamen
            Beeten wird geteilt. Der Mitgliedsbeitrag beträgt 20 Euro im Jahr.
            """,
            [
                (
                    "Einmal im Monat …",
                    "hilft jedes Mitglied bei der Gartenarbeit für alle.",
                    "gibt es ein Fest.",
                    "bekommt man neues Werkzeug.",
                ),
                (
                    "Das Werkzeug …",
                    "liegt im Gartenhaus.",
                    "muss man selbst mitbringen.",
                    "kann man kaufen.",
                ),
                ("Chemische Mittel …", "sind verboten.", "sind erlaubt.", "gibt es im Gartenhaus."),
                (
                    "Der Mitgliedsbeitrag …",
                    "kostet 20 Euro pro Jahr.",
                    "kostet 20 Euro pro Monat.",
                    "ist kostenlos.",
                ),
            ],
        ),
    ),
}
