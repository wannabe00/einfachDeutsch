"""B1 Schreiben sets, shaped like the Goethe-Zertifikat B1 writing paper: one set
per Modul. Teil 1: an e-mail to a friend (about 80 words). Teil 2: a forum post
giving your opinion (about 80 words, no greeting needed). Teil 3: a short
formal message (about 40 words). Three points each, graded with the A-E rubric.

All tasks and model answers are original, on the Modul's topics.
"""

from ..dsl import schreiben_text

INFORMAL = "Write an e-mail to a friend (about 80 words)."
FORUM_POST = "Write a forum post with your opinion (about 80 words)."
FORMAL = "Write a formal message (about 40 words)."


def _pair(informal, formal):
    """The two letters of a Modul; its forum post is in FORUM."""
    return informal, formal


FORUM = {
    1: (
        "Im Online-Forum einer Zeitschrift lesen Sie die Frage: „Sollen junge Leute "
        "nach der Schule sofort allein wohnen?“ Schreiben Sie Ihre Meinung.",
        [
            "Sagen Sie Ihre Meinung.",
            "Nennen Sie Vorteile oder Nachteile.",
            "Erzählen Sie von Ihrer Erfahrung.",
        ],
        """
        Ich finde, dass junge Leute nach der Schule nicht sofort allein wohnen müssen.
        Ein Vorteil ist natürlich, dass man selbstständig wird und lernt, einen Haushalt
        zu führen. Allerdings sind die Mieten in den Großstädten sehr hoch, und viele
        Auszubildende verdienen wenig. Ich selbst habe nach der Schule noch zwei Jahre bei
        meinen Eltern gewohnt und Geld gespart. Danach bin ich in eine WG gezogen. Das war
        für mich die beste Lösung, weil ich nie allein war.
        """,
    ),
    2: (
        "In einem Forum diskutieren Leute: „Werden Roboter bald unsere Hausarbeit machen? "
        "Ist das gut?“ Schreiben Sie Ihre Meinung.",
        [
            "Sagen Sie Ihre Meinung.",
            "Nennen Sie einen Vorteil und einen Nachteil.",
            "Was machen Sie selbst im Haushalt gern oder nicht gern?",
        ],
        """
        Ich glaube, dass in zwanzig Jahren in vielen Wohnungen Roboter arbeiten werden.
        Das finde ich eigentlich gut. Ein großer Vorteil ist, dass wir mehr Zeit für die
        Familie und für Hobbys haben werden. Ein Nachteil ist aber, dass solche Geräte
        teuer sind und nicht alle Menschen sie bezahlen können. Ich selbst putze nicht
        gern Fenster, deshalb würde ich mir sofort einen Fensterroboter kaufen. Kochen
        möchte ich aber immer selbst, das macht mir einfach zu viel Spaß.
        """,
    ),
    3: (
        "Im Forum einer Firmenzeitung lesen Sie die Frage: „Sollen Firmen Sportkurse "
        "während der Arbeitszeit anbieten?“ Schreiben Sie Ihre Meinung.",
        ["Sagen Sie Ihre Meinung.", "Begründen Sie Ihre Meinung.", "Machen Sie einen Vorschlag."],
        """
        Meiner Meinung nach sollten Firmen ihren Mitarbeitern Sportkurse während der
        Arbeitszeit anbieten. Viele Menschen sitzen acht Stunden am Schreibtisch und haben
        deshalb oft Rückenschmerzen. Wer sich regelmäßig bewegt, ist gesünder und arbeitet
        auch besser. Außerdem ist die Atmosphäre im Team besser, wenn man zusammen Sport
        macht. Ich schlage vor, dass jede Firma zweimal pro Woche eine kurze Gymnastik am
        Arbeitsplatz anbietet. Das kostet nicht viel Geld, aber es hilft allen.
        """,
    ),
    4: (
        "In einem Forum lesen Sie: „Betriebsfeiern sind Zeitverschwendung.“ Schreiben "
        "Sie Ihre Meinung.",
        [
            "Sagen Sie Ihre Meinung.",
            "Erzählen Sie von einer Feier, die Sie erlebt haben.",
            "Was macht eine gute Feier aus?",
        ],
        """
        Ich bin ganz anderer Meinung: Betriebsfeiern sind keine Zeitverschwendung. Bei der
        Arbeit hat man oft keine Zeit, die Kollegen richtig kennenzulernen. Letztes Jahr
        haben wir einen Betriebsausflug an einen See gemacht. Obwohl es geregnet hat,
        hatten alle viel Spaß, und ich habe mich zum ersten Mal lange mit meiner Chefin
        unterhalten. Eine gute Feier braucht nicht viel Geld. Wichtig sind gutes Essen,
        etwas Musik und vor allem Kollegen, die gern dabei sind.
        """,
    ),
    5: (
        "Im Forum einer Volkshochschule lesen Sie die Frage: „Lohnt sich eine "
        "Weiterbildung auch mit 50 noch?“ Schreiben Sie Ihre Meinung.",
        [
            "Sagen Sie Ihre Meinung.",
            "Begründen Sie Ihre Meinung.",
            "Welchen Kurs würden Sie gern machen?",
        ],
        """
        Ich bin davon überzeugt, dass man nie zu alt zum Lernen ist. Die Arbeitswelt
        verändert sich sehr schnell, deshalb muss man sowohl mit dreißig als auch mit
        fünfzig neue Dinge lernen. Ältere Menschen haben außerdem viel Erfahrung, und
        das hilft beim Lernen. Meine Mutter hat mit 55 einen Computerkurs gemacht und
        hat danach eine neue Stelle gefunden. Ich selbst würde gern einen Fotokurs
        besuchen, weil ich schon lange bessere Bilder von meinen Reisen machen möchte.
        """,
    ),
    6: (
        "In einem Forum diskutieren Leute: „Sollen Jugendliche schon mit 16 wählen dürfen?“ "
        "Schreiben Sie Ihre Meinung.",
        [
            "Sagen Sie Ihre Meinung.",
            "Nennen Sie ein Argument dafür und eins dagegen.",
            "Wie ist das in Ihrem Heimatland?",
        ],
        """
        Ich finde, dass Jugendliche schon mit 16 wählen dürfen sollten. Viele junge Menschen
        engagieren sich für den Klimaschutz und interessieren sich sehr für Politik. Die
        Entscheidungen von heute betreffen vor allem ihre Zukunft. Ein Argument dagegen
        ist zwar, dass manche Jugendliche noch nicht genug über Parteien wissen. Aber das
        gilt auch für viele Erwachsene. In meinem Heimatland darf man erst mit 18 wählen,
        und ich glaube, dass sich das bald ändern sollte.
        """,
    ),
    7: (
        "Im Forum einer Reisezeitschrift lesen Sie die Frage: „Sollen beliebte Regionen "
        "die Zahl der Touristen begrenzen?“ Schreiben Sie Ihre Meinung.",
        ["Sagen Sie Ihre Meinung.", "Begründen Sie Ihre Meinung.", "Wohin reisen Sie selbst gern?"],
        """
        Meiner Meinung nach ist es sinnvoll, die Zahl der Touristen in manchen Regionen zu
        begrenzen. Je mehr Menschen kommen, desto mehr Müll und Verkehr gibt es, sodass die
        Natur und die Einwohner leiden. Allerdings leben viele Familien vom Tourismus.
        Deshalb finde ich eine Lösung gut, bei der man vorher eine Karte kaufen muss. Ich
        selbst reise am liebsten in kleine Dörfer in den Bergen, wo es ruhig ist und
        man sich gut erholen kann.
        """,
    ),
    8: (
        "In einem Forum lesen Sie die Frage: „Soll unsere Innenstadt autofrei werden?“ "
        "Schreiben Sie Ihre Meinung.",
        [
            "Sagen Sie Ihre Meinung.",
            "Nennen Sie Vorteile oder Nachteile.",
            "Wie kommen Sie selbst in die Stadt?",
        ],
        """
        Ich bin dafür, dass die Innenstadt autofrei wird. Statt mit dem Auto zu fahren,
        könnten die Leute den Bus oder das Fahrrad nehmen. Dadurch wird die Luft sauberer,
        und es ist leiser und sicherer für Kinder. Ein Nachteil ist, dass ältere Menschen
        ohne Auto nicht so leicht zum Einkaufen kommen. Deshalb braucht man mehr Busse und
        vielleicht kleine Elektrobusse nur für die Altstadt. Ich selbst fahre jeden Tag mit
        dem Rad in die Stadt, um fit zu bleiben.
        """,
    ),
}


_LETTERS = {
    # Modul 1 (Lektionen 1-3): friendship, internships, housing.
    1: _pair(
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
    2: _pair(
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
    3: _pair(
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
    4: _pair(
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
    5: _pair(
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
    6: _pair(
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
    7: _pair(
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
    8: _pair(
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


SCHREIBEN = {
    modul: [
        schreiben_text(INFORMAL, *informal[:2], (65, 90), informal[2], teil=1),
        schreiben_text(
            FORUM_POST, *FORUM[modul][:2], (65, 90), FORUM[modul][2], teil=2, forum=True
        ),
        schreiben_text(FORMAL, *formal[:2], (35, 55), formal[2], formal=True, teil=3),
    ]
    for modul, (informal, formal) in _LETTERS.items()
}
