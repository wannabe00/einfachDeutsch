"""B1 Schreiben sets: one per Modul, in the same two-Teil shape as A2 but longer,
as in the Goethe B1 writing paper. Teil 1: an informal e-mail to a friend
(60-80 words). Teil 2: a formal e-mail or letter (40-60 words). Three points
each, graded with the A2 rubric.

All tasks and model answers are original, on the Modul's topics.
"""

from ..dsl import schreiben_text

INFORMAL = "Write an e-mail to a friend (60-80 words)."
FORMAL = "Write a formal e-mail (40-60 words)."


def _set(informal, formal) -> list:
    """Each is (situation, points, model answer)."""
    (s1, p1, m1), (s2, p2, m2) = informal, formal
    return [
        schreiben_text(INFORMAL, s1, p1, (60, 80), m1, teil=1),
        schreiben_text(FORMAL, s2, p2, (40, 60), m2, formal=True, teil=2),
    ]


SCHREIBEN = {
    # Modul 1 (Lektionen 1-3): friendship, internships, housing.
    1: _set(
        (
            "Sie haben gerade ein Praktikum in einer anderen Stadt begonnen. Schreiben "
            "Sie Ihrer Freundin Lea eine E-Mail.",
            [
                "Wo machen Sie das Praktikum, und was sind Ihre Aufgaben?",
                "Wie sind die Kollegen?",
                "Laden Sie Lea zu einem Besuch ein.",
            ],
            """
            Liebe Lea,
            seit Montag mache ich mein Praktikum in einem Kindergarten in Freiburg.
            Ich betreue morgens eine Gruppe mit zwölf Kindern, und nachmittags helfe
            ich beim Basteln und Spielen. Am ersten Tag war ich ziemlich nervös, aber
            meine Kollegen sind wirklich nett und sehr geduldig mit mir. Wir duzen uns
            alle. Hast du Lust, mich im Juni zu besuchen? Dann zeige ich dir die Stadt.
            Liebe Grüße
            Jana
            """,
        ),
        (
            "Sie suchen eine Wohnung und haben eine Anzeige der Maklerin Frau Schuster "
            "gelesen. Schreiben Sie ihr eine E-Mail.",
            [
                "Sagen Sie, warum Sie schreiben.",
                "Beschreiben Sie, was für eine Wohnung Sie suchen.",
                "Bitten Sie um einen Termin für eine Besichtigung.",
            ],
            """
            Sehr geehrte Frau Schuster,
            ich habe Ihre Anzeige gelesen und interessiere mich für die Wohnung in der
            Innenstadt. Ich suche eine helle Wohnung mit zwei Zimmern und einem Balkon,
            in der ich auch arbeiten kann. Könnten wir einen Termin für eine
            Besichtigung vereinbaren? Ich habe nächste Woche jeden Nachmittag Zeit.
            Mit freundlichen Grüßen
            Paul Weber
            """,
        ),
    ),
    # Modul 2 (Lektionen 4-6): complaints, technology, invitations.
    2: _set(
        (
            "Ihr Freund Ben hat Sie zu seinem Geburtstagsessen eingeladen. Schreiben "
            "Sie ihm eine E-Mail.",
            [
                "Bedanken Sie sich für die Einladung und sagen Sie zu.",
                "Fragen Sie, was Sie mitbringen können.",
                "Erzählen Sie, dass Sie etwas nicht essen dürfen.",
            ],
            """
            Lieber Ben,
            vielen Dank für deine Einladung zu deinem Geburtstagsessen am Samstag! Ich
            komme sehr gern. Soll ich etwas mitbringen? Ich könnte zum Beispiel einen
            Salat machen oder einen Kuchen backen. Ich muss dir aber noch sagen, dass
            ich allergisch gegen Nüsse bin. Falls es Nüsse im Essen gibt, ist das kein
            Problem, dann esse ich einfach etwas anderes. Ich freue mich schon auf den
            Abend!
            Viele Grüße
            Mia
            """,
        ),
        (
            "Sie haben vor einem Monat eine Zeitschrift abonniert, aber noch keine "
            "Ausgabe bekommen. Schreiben Sie an den Kundenservice des Verlags.",
            [
                "Beschreiben Sie das Problem.",
                "Sagen Sie, was Sie schon gemacht haben.",
                "Sagen Sie, was Sie jetzt erwarten.",
            ],
            """
            Sehr geehrte Damen und Herren,
            vor einem Monat habe ich Ihre Zeitschrift abonniert. Obwohl ich schon
            bezahlt habe, habe ich noch keine Ausgabe erhalten. Ich habe bereits zweimal
            angerufen, aber niemand konnte mir helfen. Bitte schicken Sie mir die
            Hefte sofort, oder ich kündige das Abonnement.
            Mit freundlichen Grüßen
            Karin Vogel
            """,
        ),
    ),
    # Modul 3 (Lektionen 7-9): pets, careers, health at work.
    3: _set(
        (
            "Sie haben sich ein Haustier angeschafft. Schreiben Sie Ihrem Freund Max eine E-Mail.",
            [
                "Welches Tier haben Sie, und warum?",
                "Was macht Ihnen Spaß, was ist schwierig?",
                "Bitten Sie Max, sich im Urlaub um das Tier zu kümmern.",
            ],
            """
            Lieber Max,
            stell dir vor, ich habe jetzt eine Katze! Sie heißt Mimi und kommt aus dem
            Tierheim. Ich habe eine Katze genommen, weil ich tagsüber arbeite und keine
            Zeit für einen Hund habe. Es macht mir viel Spaß, mit ihr zu spielen.
            Schwierig ist nur, dass sie nachts sehr aktiv ist. Hättest du Zeit, sie im
            August zu füttern, während ich im Urlaub bin?
            Liebe Grüße
            Sara
            """,
        ),
        (
            "Ihre Firma bietet einen Kurs zum Thema „Gesund im Büro“ an. Schreiben Sie "
            "eine E-Mail an Frau Hartmann aus der Personalabteilung.",
            [
                "Sagen Sie, dass Sie teilnehmen möchten.",
                "Sagen Sie, warum der Kurs für Sie wichtig ist.",
                "Fragen Sie nach Ort und Zeit.",
            ],
            """
            Sehr geehrte Frau Hartmann,
            ich möchte gern am Kurs „Gesund im Büro“ teilnehmen. Da ich jeden Tag acht
            Stunden am Schreibtisch sitze, habe ich oft Rückenschmerzen. Ich hoffe,
            dass ich im Kurs gute Übungen lerne. Könnten Sie mir bitte sagen, wann und
            wo der Kurs stattfindet?
            Mit freundlichen Grüßen
            Thomas Brenner
            """,
        ),
    ),
    # Modul 4 (Lektionen 10-12): mishaps, happiness, company events.
    4: _set(
        (
            "Ihnen ist gestern etwas Dummes passiert. Schreiben Sie Ihrer Freundin Julia "
            "eine E-Mail.",
            [
                "Erzählen Sie, was passiert ist.",
                "Schreiben Sie, was Sie besser gemacht hätten.",
                "Fragen Sie Julia, ob ihr so etwas auch schon passiert ist.",
            ],
            """
            Liebe Julia,
            stell dir vor, was mir gestern passiert ist! Ich wollte zu einem wichtigen
            Vorstellungsgespräch fahren, aber ich habe den Zug verpasst, weil ich mein
            Handy zu Hause liegen gelassen hatte und noch einmal zurück musste. Ich bin
            eine halbe Stunde zu spät gekommen. Wäre ich doch nur früher losgegangen!
            Zum Glück war die Chefin nett. Ist dir so etwas auch schon passiert?
            Viele Grüße
            Nora
            """,
        ),
        (
            "Ihr Kollege Herr Sander hat Sie zu seinem Ausstand eingeladen, aber Sie "
            "können nicht kommen. Schreiben Sie ihm eine E-Mail.",
            [
                "Bedanken Sie sich für die Einladung.",
                "Sagen Sie, warum Sie nicht kommen können.",
                "Wünschen Sie ihm alles Gute für die Zukunft.",
            ],
            """
            Lieber Herr Sander,
            vielen Dank für die Einladung zu Ihrem Ausstand. Leider kann ich am Freitag
            nicht kommen, weil ich an diesem Tag eine Dienstreise nach Wien habe. Das
            tut mir sehr leid. Ich wünsche Ihnen alles Gute für die Zukunft und viel
            Freude in der Rente!
            Mit freundlichen Grüßen
            Eva Kraus
            """,
        ),
    ),
    # Modul 5 (Lektionen 13-15): misunderstandings, courses, applications.
    5: _set(
        (
            "Sie haben einen Kurs an der Volkshochschule angefangen. Schreiben Sie Ihrem "
            "Freund Leo eine E-Mail.",
            [
                "Welchen Kurs machen Sie, und warum?",
                "Beschreiben Sie die Kursleiterin und die Teilnehmer.",
                "Schlagen Sie vor, dass Leo auch einen Kurs macht.",
            ],
            """
            Lieber Leo,
            seit zwei Wochen mache ich einen Fotokurs an der Volkshochschule. Ich wollte
            schon lange lernen, wie man bessere Fotos macht. Die Kursleiterin ist eine
            ausgebildete Fotografin, und sie erklärt alles sehr gut. Die Teilnehmer sind
            sowohl jung als auch alt, und wir haben viel Spaß zusammen. Willst du nicht
            auch einen Kurs machen? Es gibt sogar einen Kletterkurs, das wäre doch etwas
            für dich!
            Viele Grüße
            Ben
            """,
        ),
        (
            "Sie haben eine Stellenanzeige für eine Stelle im Hotel Bergblick gelesen. "
            "Schreiben Sie eine kurze Bewerbung an Herrn Lorenz.",
            [
                "Sagen Sie, für welche Stelle Sie sich bewerben.",
                "Beschreiben Sie Ihre Erfahrung und Sprachkenntnisse.",
                "Bitten Sie um ein Vorstellungsgespräch.",
            ],
            """
            Sehr geehrter Herr Lorenz,
            hiermit bewerbe ich mich um die Stelle an der Rezeption. Ich habe bereits
            drei Jahre in einem Hotel in Salzburg gearbeitet und spreche sowohl Englisch
            als auch Italienisch. Über eine Einladung zu einem Vorstellungsgespräch
            würde ich mich sehr freuen.
            Mit freundlichen Grüßen
            Lucia Moretti
            """,
        ),
    ),
    # Modul 6 (Lektionen 16-18): memories, art, politics.
    6: _set(
        (
            "Sie haben eine interessante Ausstellung besucht. Schreiben Sie Ihrer "
            "Freundin Anna eine E-Mail.",
            [
                "Wo waren Sie, und was haben Sie gesehen?",
                "Was hat Ihnen besonders gefallen?",
                "Schlagen Sie vor, die Ausstellung zusammen noch einmal zu besuchen.",
            ],
            """
            Liebe Anna,
            am Sonntag war ich im Stadtmuseum in der Ausstellung über die Malerin Elsa
            Hoff. Sie hat vor hundert Jahren Landschaften und kleine Dörfer gemalt. Es
            war wirklich beeindruckend! Besonders gut haben mir die starken Farben
            gefallen. Es fällt mir schwer, das zu beschreiben, du musst es selbst sehen.
            Hast du Lust, nächsten Samstag mit mir hinzugehen? Es lohnt sich wirklich.
            Liebe Grüße
            Carla
            """,
        ),
        (
            "Ihre Stadt plant, einen Park zu schließen. Schreiben Sie eine E-Mail an "
            "Bürgermeisterin Frau Dr. Wendt.",
            [
                "Sagen Sie, warum Sie schreiben.",
                "Sagen Sie Ihre Meinung zu dem Plan.",
                "Machen Sie einen Vorschlag.",
            ],
            """
            Sehr geehrte Frau Dr. Wendt,
            ich habe gelesen, dass die Stadt den Stadtpark schließen möchte. Davon halte
            ich nicht viel, denn der Park ist weder teuer noch unwichtig: Viele Familien
            und Rentner treffen sich dort. Ich schlage vor, dass die Bürger den Park
            ehrenamtlich pflegen.
            Mit freundlichen Grüßen
            Jonas Albrecht
            """,
        ),
    ),
    # Modul 7 (Lektionen 19-21): tourism, mountain huts, concerts and cities.
    7: _set(
        (
            "Sie waren am Wochenende auf einem Konzert. Schreiben Sie Ihrem Freund Tom "
            "eine E-Mail.",
            [
                "Wo und wann war das Konzert?",
                "Wie war die Atmosphäre?",
                "Empfehlen Sie Tom die Band.",
            ],
            """
            Lieber Tom,
            am Samstag war ich auf dem Konzert der Band Wonnetöne im Stadion außerhalb
            der Stadt. Die Karten waren innerhalb einer Stunde verkauft, aber ich hatte
            zum Glück noch eine bekommen! Die Atmosphäre war einmalig: Je später es wurde,
            desto lauter haben die Fans gesungen. Die Band spielt im Herbst noch einmal
            in Hamburg. Das kann ich dir nur empfehlen, du musst unbedingt hingehen!
            Viele Grüße
            Lisa
            """,
        ),
        (
            "Sie haben zwei Nächte auf der Berghütte Edelweiß verbracht. Schreiben Sie "
            "eine E-Mail an den Hüttenwirt Herrn Gruber.",
            [
                "Bedanken Sie sich für den Aufenthalt.",
                "Sagen Sie, was Ihnen gefallen hat.",
                "Fragen Sie nach einem Termin im nächsten Sommer.",
            ],
            """
            Sehr geehrter Herr Gruber,
            vielen Dank für die zwei schönen Nächte auf Ihrer Hütte. Besonders gut
            haben uns das Essen und die Aussicht vom Gipfel gefallen. Wir möchten im
            nächsten Sommer gern wiederkommen. Haben Sie im Juli noch Plätze im Lager
            für vier Personen frei?
            Mit freundlichen Grüßen
            Familie Neumann
            """,
        ),
    ),
    # Modul 8 (Lektionen 22-24): history, environment, living together.
    8: _set(
        (
            "Sie fahren seit einem Monat nur noch mit dem Fahrrad zur Arbeit. Schreiben "
            "Sie Ihrer Freundin Sophie eine E-Mail.",
            [
                "Warum fahren Sie jetzt Rad?",
                "Was ist besser, was ist schwieriger als früher?",
                "Fragen Sie Sophie, ob sie mitmachen möchte.",
            ],
            """
            Liebe Sophie,
            seit einem Monat fahre ich jeden Tag mit dem Fahrrad zur Arbeit, statt das
            Auto zu nehmen. Ich mache das, um fit zu bleiben und um etwas für die Umwelt
            zu tun. Ich fühle mich viel besser und spare sogar Geld! Schwieriger ist es
            nur, wenn es regnet, aber dafür habe ich jetzt eine gute Regenjacke. Hast du
            Lust, mitzumachen? Wir könnten zusammen fahren, du wohnst ja ganz in der Nähe.
            Liebe Grüße
            Lena
            """,
        ),
        (
            "Sie möchten in ein Mehrgenerationenhaus ziehen. Schreiben Sie eine E-Mail an "
            "die Hausverwaltung, Frau Kühn.",
            [
                "Stellen Sie sich und Ihre Familie kurz vor.",
                "Sagen Sie, warum Sie dort wohnen möchten.",
                "Fragen Sie, ob eine Wohnung frei ist.",
            ],
            """
            Sehr geehrte Frau Kühn,
            wir sind eine Familie mit zwei kleinen Kindern und möchten gern in Ihr
            Mehrgenerationenhaus ziehen. Wir möchten mit älteren Menschen zusammenleben,
            damit unsere Kinder auch Großeltern in der Nähe haben. Ist im Moment eine
            Wohnung mit drei Zimmern frei?
            Mit freundlichen Grüßen
            Familie Demir
            """,
        ),
    ),
}
