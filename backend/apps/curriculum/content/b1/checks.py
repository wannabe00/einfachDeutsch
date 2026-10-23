"""B1 check content: what the review of each Lektion and each Modul test asks
beyond the generated word batches (see apps.curriculum.checks and
content/a1/checks.py for the format).

B1 is stage 4 of the ramp throughout, like A2: gaps and translations are typed
(gaps carry a hint), and every extra format is used. Translations list the
common word-order variants, since typing is graded exactly. All sentences are
original. Each Modul adds its Lektionen here as it is written.
"""

from ..dsl import lektion_check, modul_check

LEVEL = "B1"


def _l(n, gaps, translations):
    return n, lektion_check(LEVEL, n, gaps, translations)


LEKTION_CHECKS = dict(
    [
        _l(
            1,
            [
                ("Ihr seid einfach die [Besten]!", "gut, Superlativ"),
                ("Ein [Erwachsener] muss unterschreiben.", "erwachsen"),
                ("Ich helfe meinem [Nachbarn].", "Nachbar"),
                ("Kennst du den neuen [Kollegen]?", "Kollege"),
                ("Sie hat viel [Mut].", "courage"),
            ],
            [
                ("She is really honest.", "Sie ist wirklich ehrlich."),
                ("I trust my neighbour.", "Ich vertraue meinem Nachbarn."),
                ("He is the bravest of us.", "Er ist der Mutigste von uns."),
                (
                    "I have great respect for her.",
                    "Ich habe großen Respekt vor ihr.",
                ),
            ],
        ),
        _l(
            2,
            [
                ("Insgesamt [gefiel] mir das Praktikum gut.", "gefallen"),
                ("Er [erledigte] seine Aufgaben zuverlässig.", "erledigen"),
                ("Der Azubi [brachte] die Post.", "bringen"),
                ("Niemand [wusste] die Antwort.", "wissen"),
                ("Sie arbeitet in [Teilzeit].", "part-time"),
            ],
            [
                ("He looked after the children.", "Er betreute die Kinder."),
                ("I took over a group.", "Ich übernahm eine Gruppe."),
                (
                    "The working atmosphere was pleasant.",
                    "Das Betriebsklima war angenehm.",
                ),
                ("We didn't know the colleagues yet.", "Wir kannten die Kollegen noch nicht."),
            ],
        ),
        _l(
            3,
            [
                ("Das ist der Mann, [dem] ich geholfen habe.", "relative pronoun"),
                ("Das sind die Kunden, [denen] wir schreiben.", "relative pronoun"),
                ("Das ist die Wohnung, in [der] ich wohne.", "relative pronoun"),
                ("Wir wohnen in einem [Vorort].", "suburb"),
                ("Die [Hälfte] von uns wohnt zur Miete.", "half"),
            ],
            [
                ("Do you rent? (Sie)", "Wohnen Sie zur Miete?"),
                (
                    "That is the house I grew up in.",
                    "Das ist das Haus, in dem ich aufgewachsen bin.",
                ),
                ("The street is very narrow.", "Die Straße ist sehr eng."),
                (
                    "A quarter of the people live alone.",
                    "Ein Viertel der Menschen lebt allein.",
                ),
            ],
        ),
        _l(
            4,
            [
                ("[Obwohl] ich angerufen habe, kam keine Antwort.", "although"),
                ("Es regnet. [Trotzdem] gehen wir spazieren.", "nevertheless"),
                ("Ich habe das Heft nicht [erhalten].", "erhalten"),
                ("Könnten Sie mich bitte [verbinden]?", "put through"),
                ("Bitte halten Sie Ihre Nummer [bereit].", "ready"),
            ],
            [
                (
                    "I'm not satisfied with your service.",
                    "Ich bin mit Ihrem Service nicht zufrieden.",
                ),
                ("I'm calling about a complaint.", "Ich rufe wegen einer Reklamation an."),
                (
                    "She went to work although she was ill.",
                    "Sie ging zur Arbeit, obwohl sie krank war.",
                    "Sie ist zur Arbeit gegangen, obwohl sie krank war.",
                ),
                ("Shall I pass on a message?", "Soll ich etwas ausrichten?"),
            ],
        ),
        _l(
            5,
            [
                ("Bald [wird] jeder einen Roboter haben.", "werden"),
                ("Ich [werde] ab morgen mehr Sport machen.", "werden"),
                ("Hast du die Datei [gespeichert]?", "speichern"),
                ("Er ist nicht da. Er wird [wohl] krank sein.", "probably"),
                ("Die Technik macht große [Fortschritte].", "progress"),
            ],
            [
                (
                    "I believe that robots will help us.",
                    "Ich glaube, dass Roboter uns helfen werden.",
                ),
                ("I promise you that.", "Das verspreche ich dir.", "Ich verspreche dir das."),
                ("Who invented the telephone?", "Wer hat das Telefon erfunden?"),
                ("You will tidy your room now!", "Du wirst jetzt dein Zimmer aufräumen!"),
            ],
        ),
        _l(
            6,
            [
                ("[Falls] du Zeit hast, komm vorbei.", "in case"),
                ("Fühlen Sie sich wie zu [Hause].", "home"),
                ("Danke! Gern [geschehen].", "geschehen"),
                ("Ich bin [allergisch] gegen Nüsse.", "allergic"),
                ("Ich [bedanke] mich für die Einladung.", "bedanken"),
            ],
            [
                ("Make yourself at home. (Sie)", "Fühlen Sie sich wie zu Hause."),
                (
                    "In case it rains, we'll eat inside.",
                    "Falls es regnet, essen wir drinnen.",
                ),
                (
                    "Thank you, that tasted excellent.",
                    "Danke, das hat ausgezeichnet geschmeckt.",
                ),
                ("I have to decline the invitation.", "Ich muss die Einladung ablehnen."),
            ],
        ),
        _l(
            7,
            [
                ("Hast du Lust, die Katze [zu] füttern?", "zu"),
                ("Ich rate dir, gut darüber [nachzudenken].", "nachdenken"),
                ("Der Hund [frisst] viel Fleisch.", "fressen"),
                ("Ein Hamster wohnt im [Käfig].", "cage"),
                ("Danke, das ist ein guter [Hinweis].", "tip"),
            ],
            [
                ("Can I help you? (Sie)", "Kann ich Ihnen helfen?"),
                (
                    "It is important to inform yourself first.",
                    "Es ist wichtig, sich vorher zu informieren.",
                ),
                ("A guinea pig is easy to look after.", "Ein Meerschweinchen ist pflegeleicht."),
                ("I'd like to get a dog.", "Ich möchte mir einen Hund anschaffen."),
            ],
        ),
        _l(
            8,
            [
                ("Ich frühstücke, [bevor] ich zur Arbeit fahre.", "before"),
                ("Ich höre Musik, [während] ich koche.", "while"),
                ("[Da] ich gern helfe, werde ich Krankenpfleger.", "since"),
                ("Das [entspricht] meinen Fähigkeiten.", "entsprechen"),
                ("Er spricht nicht gern mit Fremden. Er ist [schüchtern].", "shy"),
            ],
            [
                ("That suits me very well.", "Das passt sehr gut zu mir."),
                ("I wouldn't have expected that.", "Das hätte ich nicht erwartet."),
                ("She is suitable for the job.", "Sie ist für den Beruf geeignet."),
                (
                    "Before I sleep, I read a book.",
                    "Bevor ich schlafe, lese ich ein Buch.",
                ),
            ],
        ),
        _l(
            9,
            [
                ("Sport trägt zu einem [größeren] Wohlbefinden bei.", "groß"),
                ("Das ist die [wichtigste] Regel.", "wichtig"),
                ("Rauchen [schadet] der Gesundheit.", "schaden"),
                ("[Atmen] Sie tief ein!", "atmen"),
                ("Im [Durchschnitt] schlafen wir sieben Stunden.", "average"),
            ],
            [
                ("Thank you for listening.", "Vielen Dank fürs Zuhören."),
                ("Close your eyes. (Sie)", "Schließen Sie die Augen."),
                (
                    "We are looking for a quieter workplace.",
                    "Wir suchen einen ruhigeren Arbeitsplatz.",
                ),
                ("We want to reduce stress.", "Wir wollen den Stress reduzieren."),
            ],
        ),
        _l(
            10,
            [
                ("[Hätte] ich doch den Schirm mitgenommen!", "haben"),
                ("[Wäre] ich bloß früher losgegangen!", "sein"),
                ("Ich habe den Schlüssel stecken [lassen].", "lassen"),
                ("Leider ist alles [schiefgegangen].", "schiefgehen"),
                ("Oh je, das ist dumm [gelaufen].", "laufen"),
            ],
            [
                ("That's my fault.", "Das ist meine Schuld."),
                ("There's nothing you can do.", "Da kann man nichts machen."),
                (
                    "If only I had done that differently!",
                    "Hätte ich das bloß anders gemacht!",
                    "Hätte ich das doch anders gemacht!",
                ),
                ("I got lost.", "Ich habe mich verlaufen."),
            ],
        ),
        _l(
            11,
            [
                ("Als ich kam, [hatte] der Film schon begonnen.", "haben"),
                ("Sie [war] schon nach Hause gegangen.", "sein"),
                ("[Nachdem] ich gegessen hatte, ging ich spazieren.", "after"),
                ("Die Fans haben laut [gejubelt].", "jubeln"),
                ("Wir haben den Urlaub sehr [genossen].", "genießen"),
            ],
            [
                ("I was overjoyed!", "Ich war überglücklich!"),
                ("The train had already left.", "Der Zug war schon abgefahren."),
                (
                    "We cheered after we had won.",
                    "Wir jubelten, nachdem wir gewonnen hatten.",
                ),
                ("We never gave up hope.", "Wir haben die Hoffnung nie aufgegeben."),
            ],
        ),
        _l(
            12,
            [
                ("Das ist der Ausflug [des] Jahres.", "article"),
                ("Das Büro [der] Chefin ist oben.", "article"),
                ("[Trotz] des Regens fahren wir los.", "despite"),
                ("Trotz des [schlechten] Wetters war es schön.", "schlecht"),
                ("Vielen Dank im [Voraus]!", "in advance"),
            ],
            [
                ("That is the party of the year.", "Das ist die Feier des Jahres."),
                ("Thank you for the invitation.", "Vielen Dank für die Einladung."),
                (
                    "Unfortunately I can't come.",
                    "Leider kann ich nicht kommen.",
                ),
                ("That is my brother's car.", "Das ist das Auto meines Bruders."),
            ],
        ),
        _l(
            13,
            [
                ("Es war laut. [Deshalb] verstand ich nichts.", "therefore"),
                ("[Wegen] des Lärms konnte ich nicht schlafen.", "because of"),
                ("Aus diesem [Grund] gab es ein Missverständnis.", "reason"),
                ("Ich habe noch einmal [nachgefragt].", "nachfragen"),
                ("Das war so [peinlich]!", "embarrassing"),
            ],
            [
                (
                    "What does this word mean?",
                    "Was bedeutet dieses Wort?",
                    "Was bedeutet das Wort?",
                ),
                (
                    "Could you say that more slowly? (Sie)",
                    "Könnten Sie das bitte langsamer sagen?",
                    "Könnten Sie das langsamer sagen?",
                ),
                (
                    "Because of the dialect I didn't understand her.",
                    "Wegen des Dialekts habe ich sie nicht verstanden.",
                    "Wegen des Dialekts verstand ich sie nicht.",
                ),
                ("I misunderstood you. (dich)", "Ich habe dich missverstanden."),
            ],
        ),
        _l(
            14,
            [
                ("Das ist ein [faszinierender] Kurs.", "faszinieren"),
                ("Eine [ausgebildete] Expertin leitet den Kurs.", "ausbilden"),
                ("Vorsicht, [kochendes] Wasser!", "kochen"),
                ("Die [Teilnahme] ist auf eigene Gefahr.", "participation"),
                ("[Vorkenntnisse] sind nicht nötig.", "previous knowledge"),
            ],
            [
                ("The course is fully booked.", "Der Kurs ist ausgebucht."),
                ("I'd like to sign up for the course.", "Ich möchte mich für den Kurs anmelden."),
                ("We are repeating the learned words.", "Wir wiederholen die gelernten Wörter."),
                ("She has a beautiful voice.", "Sie hat eine schöne Stimme."),
            ],
        ),
        _l(
            15,
            [
                ("Ich spreche [sowohl] Deutsch als auch Englisch.", "both"),
                ("Er ist nicht nur nett, [sondern] auch klug.", "but"),
                ("[Hiermit] bewerbe ich mich um die Stelle.", "hereby"),
                ("Sie ist sehr [belastbar].", "resilient"),
                ("Die Firma will neue Mitarbeiter [einstellen].", "hire"),
            ],
            [
                ("Nice that you're here. (Sie)", "Schön, dass Sie da sind."),
                ("Thank you for the conversation.", "Vielen Dank für das Gespräch."),
                (
                    "She speaks both Italian and French.",
                    "Sie spricht sowohl Italienisch als auch Französisch.",
                ),
                (
                    "Tell me something about yourself. (Sie)",
                    "Erzählen Sie etwas über sich.",
                    "Erzählen Sie bitte etwas über sich.",
                ),
            ],
        ),
        _l(
            16,
            [
                ("Du brauchst nicht [zu] kochen.", "zu"),
                ("Sie brauchen nur [anzurufen].", "anrufen"),
                ("Wir [brauchten] uns um nichts zu kümmern.", "brauchen"),
                ("Im Zug bin ich ihr [begegnet].", "begegnen"),
                ("Meine Oma hat sich um uns [gekümmert].", "kümmern"),
            ],
            [
                ("Ah, that was a wonderful time!", "Ach, das war eine herrliche Zeit!"),
                (
                    "You don't need to get up early tomorrow. (du)",
                    "Du brauchst morgen nicht früh aufzustehen.",
                ),
                ("That was out of the question for us.", "Bei uns kam das nicht infrage."),
                ("It was completely different for me.", "Bei mir war das ganz anders."),
            ],
        ),
        _l(
            17,
            [
                ("[Es] fällt mir schwer, Nein zu sagen.", "es"),
                ("Im Museum [gibt] es eine Ausstellung.", "geben"),
                ("Es [lohnt] sich, die Galerie zu besuchen.", "lohnen"),
                ("Die Malerin wurde 1877 [geboren].", "born"),
                ("Die Bilder haben mich [beeindruckt].", "beeindrucken"),
            ],
            [
                ("Look! That's beautiful!", "Guck mal! Das ist schön!"),
                ("It depends.", "Es kommt darauf an."),
                (
                    "It is worth visiting the museum.",
                    "Es lohnt sich, das Museum zu besuchen.",
                ),
                ("The painting was made in 1911.", "Das Gemälde ist 1911 entstanden."),
            ],
        ),
        _l(
            18,
            [
                ("Ich habe [weder] Zeit noch Geld.", "neither"),
                ("[Entweder] wir fahren Rad oder wir gehen.", "either"),
                ("Die Idee ist [zwar] gut, aber teuer.", "admittedly"),
                ("Sie [engagiert] sich für die Umwelt.", "engagieren"),
                ("frei → die [Freiheit]", "noun"),
            ],
            [
                ("I don't think much of that.", "Davon halte ich nicht viel."),
                ("I agree with you. (dir)", "Ich stimme dir zu."),
                ("She works voluntarily.", "Sie arbeitet ehrenamtlich."),
                ("I have to contradict you. (Ihnen)", "Ich muss Ihnen widersprechen."),
            ],
        ),
        _l(
            19,
            [
                ("Je länger ich übe, [desto] sicherer spreche ich.", "the more"),
                ("Je [älter] ich wurde, desto mehr reiste ich.", "alt"),
                ("Was ist [denn] passiert?", "particle"),
                ("Bienen machen [Honig].", "honey"),
                ("Der Eintritt ist [umsonst].", "free"),
            ],
            [
                ("I'd have one more question about that.", "Ich hätte dazu noch eine Frage."),
                ("That is interesting!", "Das ist ja interessant!"),
                (
                    "The more I learn, the better I understand.",
                    "Je mehr ich lerne, desto besser verstehe ich.",
                    "Je mehr ich lerne, umso besser verstehe ich.",
                ),
                ("We can't afford a hotel.", "Wir können uns kein Hotel leisten."),
            ],
        ),
        _l(
            20,
            [
                ("Man spart Energie, [indem] man das Licht ausschaltet.", "by"),
                ("Es schneite, [sodass] wir bleiben mussten.", "so that"),
                ("Der Weg war [so] steil, dass wir langsam gingen.", "so"),
                ("Bitte nehmt [Rücksicht] auf die anderen.", "consideration"),
                ("Die Regeln [gelten] für alle.", "gelten"),
            ],
            [
                ("The others will thank you for it! (dir)", "Die anderen werden es dir danken!"),
                ("I don't agree with that.", "Damit bin ich nicht einverstanden."),
                ("The path is very steep.", "Der Weg ist sehr steil."),
                ("We'll gladly come again.", "Wir kommen gern wieder."),
            ],
        ),
        _l(
            21,
            [
                ("Die Bühne muss [aufgebaut] werden.", "aufbauen"),
                ("Vorher muss fleißig geübt [werden].", "passive"),
                ("Wir wandern den Fluss [entlang].", "along"),
                ("Das Stadion liegt [außerhalb] der Stadt.", "outside"),
                ("Um den See [herum] gibt es einen Weg.", "around"),
            ],
            [
                (
                    "The tickets can be bought online.",
                    "Die Karten können online gekauft werden.",
                    "Die Tickets können online gekauft werden.",
                ),
                (
                    "The old town is always worth a visit.",
                    "Die Altstadt ist immer einen Besuch wert.",
                ),
                ("The band is rehearsing in the studio.", "Die Band probt im Studio."),
                (
                    "Within an hour everything was sold.",
                    "Innerhalb einer Stunde war alles verkauft.",
                ),
            ],
        ),
        _l(
            22,
            [
                ("Die Mauer [wurde] 1961 gebaut.", "passive"),
                ("Der Euro ist 2002 eingeführt [worden].", "passive"),
                ("Berlin wurde in vier Sektoren [aufgeteilt].", "aufteilen"),
                ("Die Stadt wurde [von] den Soldaten besetzt.", "by"),
                ("1990 kam die [Wiedervereinigung].", "reunification"),
            ],
            [
                ("I'd have liked to be there.", "Ich wäre gern dabei gewesen."),
                (
                    "The wall was opened in 1989.",
                    "Die Mauer wurde 1989 geöffnet.",
                    "1989 wurde die Mauer geöffnet.",
                ),
                (
                    "In the FRG democracy was introduced.",
                    "In der BRD wurde die Demokratie eingeführt.",
                ),
                (
                    "Do you know when the GDR was founded? (Sie)",
                    "Wissen Sie, wann die DDR gegründet wurde?",
                ),
            ],
        ),
        _l(
            23,
            [
                ("Ich fahre Rad, statt das Auto [zu] nehmen.", "zu"),
                ("Er ging, [ohne] sich zu verabschieden.", "without"),
                ("Vor der Kreuzung musst du [bremsen].", "brake"),
                ("Wir sollten auf das Auto [verzichten].", "do without"),
                ("Das [hängt] vom Wetter ab.", "abhängen"),
            ],
            [
                ("Cycling is in.", "Fahrradfahren ist in."),
                ("We should avoid waste.", "Wir sollten Abfall vermeiden."),
                (
                    "She left without saying goodbye.",
                    "Sie ging, ohne sich zu verabschieden.",
                    "Sie ist gegangen, ohne sich zu verabschieden.",
                ),
                ("Cycling is sustainable.", "Fahrradfahren ist nachhaltig."),
            ],
        ),
        _l(
            24,
            [
                ("Ich lerne Deutsch, [um] in Wien zu studieren.", "in order to"),
                ("Sie spricht langsam, [damit] die Kinder sie verstehen.", "so that"),
                ("Er tut so, als ob er alles [wüsste].", "wissen"),
                ("Wir haben uns auf einen Plan [geeinigt].", "einigen"),
                ("Die Nachbarin wohnt [nebenan].", "next door"),
            ],
            [
                ("That solves several problems at once.", "Das löst mehrere Probleme auf einmal."),
                ("It was nice to meet you. (euch)", "Es war schön, euch kennenzulernen."),
                ("She acts as if she were ill.", "Sie tut so, als ob sie krank wäre."),
                (
                    "All the best for the future!",
                    "Alles Gute für die Zukunft!",
                    "Viel Erfolg für die Zukunft!",
                ),
            ],
        ),
    ]
)


MODUL_CHECKS = {
    1: modul_check(
        LEVEL,
        3,
        dialogue=(
            [
                "A: Wie war dein erster Tag im Praktikum?",
                "B: ___",
                "A: Und die Kollegen?",
                "B: Die sind total nett. Wir duzen uns sogar.",
            ],
            "Insgesamt gefiel er mir sehr gut.",
            "Ich wohne in einem Reihenhaus.",
            "Das ist der Mann, dem ich geholfen habe.",
        ),
        qa=[
            ("Wer ist dein Vorbild?", "Meine Großmutter, weil sie so mutig ist."),
            ("Wo hast du dein Praktikum gemacht?", "In einem Kindergarten."),
            ("Wohnen Sie zur Miete?", "Nein, wir haben eine Eigentumswohnung."),
            ("Wie viel verdienst du netto?", "Das sage ich nicht!"),
            ("Wie ist das Betriebsklima?", "Sehr angenehm."),
        ],
        odd=[
            ("der Ofen", "großzügig", "sparsam", "vernünftig"),
            ("der Vorort", "der Erzieher", "der Praktikant", "der Auszubildende"),
            ("bewundern", "das Reihenhaus", "der Wohnblock", "das Einfamilienhaus"),
            ("einsam", "die Hälfte", "das Drittel", "das Viertel"),
        ],
        reading=(
            """
Jonas hat nach der Schule ein Praktikum bei einem Makler gemacht. Am ersten
Tag war er sehr nervös, aber seine Chefin war geduldig und erklärte ihm alles.
Er begleitete sie zu Besichtigungen und lernte viele Kunden kennen. Eine Kundin
suchte drei Wochen lang eine Wohnung in bester Lage, und am Ende fanden sie eine
Dachwohnung mit Terrasse. Heute macht Jonas eine Ausbildung als Immobilienkaufmann.
""",
            [
                ("Jonas war am ersten Tag ganz ruhig.", False),
                ("Die Chefin hat ihm viel erklärt.", True),
                ("Die Kundin hat keine Wohnung gefunden.", False),
                ("Jonas macht jetzt eine Ausbildung.", True),
            ],
        ),
        form=[
            ("Ich habe mit dem ___ gesprochen. (Kunde)", "Kunden"),
            ("Ein ___ muss das unterschreiben. (erwachsen)", "Erwachsener"),
            ("Sie ___ die Antwort nicht. (wissen, Präteritum)", "wusste"),
            ("Das ist die Frau, ___ ich danke. (relative pronoun)", "der"),
            ("Die Kinder, mit ___ ich spiele, sind fünf. (relative pronoun)", "denen"),
        ],
        mistake=[
            ("Ich kenne den *Student* aus Polen.", "Ich kenne den Studenten aus Polen."),
            ("Er *bringte* mir einen Kaffee.", "Er brachte mir einen Kaffee."),
            (
                "Das ist der Mann, *den* ich geholfen habe.",
                "Das ist der Mann, dem ich geholfen habe.",
            ),
            ("Das ist die Wohnung, in *die* ich wohne.", "Das ist die Wohnung, in der ich wohne."),
        ],
        dictation=[
            "Ihr seid einfach die Besten!",
            "Er erledigte seine Aufgaben zuverlässig.",
            "Mein Beruf ist meine Leidenschaft.",
            "Die Hälfte von uns wohnt zur Miete.",
        ],
    ),
    2: modul_check(
        LEVEL,
        6,
        dialogue=(
            [
                "A: Firma Lexa, was kann ich für Sie tun?",
                "B: ___",
                "A: Einen Moment bitte, ich verbinde Sie.",
            ],
            "Könnten Sie mich bitte mit dem Kundendienst verbinden?",
            "Das hat ausgezeichnet geschmeckt.",
            "Falls es regnet, essen wir drinnen.",
        ),
        qa=[
            ("Ist Frau Kühn da?", "Nein, sie ist heute außer Haus."),
            ("Wie wird das Leben in 50 Jahren sein?", "Roboter werden viel Arbeit machen."),
            ("Möchten Sie noch etwas Nachtisch?", "Nein danke, ich bin schon satt."),
            ("Warum schreiben Sie uns?", "Ich habe meine Zeitschrift nicht erhalten."),
            ("Kann sie mich zurückrufen?", "Ja, wie ist Ihre Nummer?"),
        ],
        odd=[
            ("der Nachtisch", "die Festplatte", "der Monitor", "das Laufwerk"),
            ("der Roboter", "der Aperitif", "der Sekt", "der Nachtisch"),
            ("speichern", "die Durchwahl", "die Warteschleife", "der Anrufbeantworter"),
            ("falls", "die Reklamation", "die Bestellung", "die Bestätigung"),
        ],
        reading=(
            """
Herr Brandt hat vor zwei Monaten eine Kaffeemaschine bestellt. Obwohl er schon
bezahlt hat, ist die Maschine noch nicht gekommen. Er hat dreimal beim
Kundendienst angerufen, aber er war immer lange in der Warteschleife. Jetzt
schreibt er eine Reklamation. Falls die Firma nicht bis Freitag antwortet, will
er sein Geld zurück.
""",
            [
                ("Herr Brandt hat die Maschine noch nicht bezahlt.", False),
                ("Er hat mehrmals angerufen.", True),
                ("Am Telefon kam er sofort zur richtigen Person.", False),
                ("Er möchte bis Freitag eine Antwort.", True),
            ],
        ),
        form=[
            ("___ ich gewartet habe, kam niemand. (although)", "Obwohl"),
            ("Morgen ___ es regnen. (werden)", "wird"),
            ("Ihr ___ das schaffen. (werden)", "werdet"),
            ("___ Sie Fragen haben, rufen Sie an. (in case)", "Falls"),
            ("Sie hat die Einladung ___. (annehmen)", "angenommen"),
        ],
        mistake=[
            (
                "Obwohl ich *habe* angerufen, kam niemand.",
                "Obwohl ich angerufen habe, kam niemand.",
            ),
            ("Er war krank. *Obwohl* ist er gekommen.", "Er war krank. Trotzdem ist er gekommen."),
            (
                "Ich glaube, dass es morgen *wird* regnen.",
                "Ich glaube, dass es morgen regnen wird.",
            ),
            ("Ich *werden* dir morgen helfen.", "Ich werde dir morgen helfen."),
        ],
        dictation=[
            "Obwohl ich Ihnen das erklärt habe, ist nichts passiert.",
            "Bald wird in fast jedem Haushalt ein PC stehen.",
            "Fühlen Sie sich wie zu Hause.",
            "Falls Sie später kommen, rufen Sie bitte an.",
        ],
    ),
    3: modul_check(
        LEVEL,
        9,
        dialogue=(
            [
                "A: Kann ich Ihnen helfen?",
                "B: ___",
                "A: Dann würde ich Ihnen eine Katze empfehlen.",
            ],
            "Ja, ich möchte ein Haustier, aber ich arbeite tagsüber.",
            "Vielen Dank fürs Zuhören.",
            "Das ist die wichtigste Regel.",
        ),
        qa=[
            ("Was frisst ein Kaninchen?", "Heu und Möhren."),
            ("Was sagt der Test?", "Dass ich ein kreativer Typ bin."),
            ("Warum soll man Sport treiben?", "Weil er zur Gesundheit beiträgt."),
            ("Wann putzt du die Zähne?", "Bevor ich ins Bett gehe."),
            ("Haben Sie noch Fragen?", "Nein, danke für den Vortrag."),
        ],
        odd=[
            ("der Vortrag", "das Kaninchen", "der Hamster", "das Meerschweinchen"),
            ("das Heu", "schüchtern", "ehrgeizig", "kontaktfreudig"),
            ("füttern", "die Folie", "der Vortrag", "die Präsentation"),
            ("zutraulich", "der Raucher", "das Rauchverbot", "die Sucht"),
        ],
        reading=(
            """
Die Firma Holtz hat neue Regeln für die Gesundheit ihrer Mitarbeiter. Jeden
Mittag gibt es eine kurze Entspannungsübung im Freien. In der Kantine kann man
gesünderes Essen kaufen, und Raucher dürfen nur noch draußen rauchen. Die
Unternehmensleitung glaubt, dass diese Regeln zu einem größeren Wohlbefinden
beitragen. Viele Mitarbeiter sind zufrieden, aber einige Raucher ärgern sich.
""",
            [
                ("Die Entspannungsübung ist am Morgen.", False),
                ("In der Kantine gibt es jetzt gesünderes Essen.", True),
                ("Man darf im Büro rauchen.", False),
                ("Nicht alle Mitarbeiter finden die Regeln gut.", True),
            ],
        ),
        form=[
            ("Ich habe vergessen, die Tür ___. (abschließen)", "abzuschließen"),
            ("Hast du Zeit, mir ___ helfen?", "zu"),
            ("___ ich koche, höre ich Radio. (while)", "Während"),
            ("Das ist der ___ Weg. (kurz, Superlativ)", "kürzeste"),
            ("Wir suchen eine ___ Lösung. (gut, Komparativ)", "bessere"),
        ],
        mistake=[
            ("Ich muss den Käfig *zu* putzen.", "Ich muss den Käfig putzen."),
            ("Ich rate dir, *zu nachdenken*.", "Ich rate dir, nachzudenken."),
            ("Bevor ich schlafe, ich *lese* ein Buch.", "Bevor ich schlafe, lese ich ein Buch."),
            ("Das ist die *wichtigeste* Regel.", "Das ist die wichtigste Regel."),
        ],
        dictation=[
            "Hast du Lust, die Kaninchen zu füttern?",
            "Während andere lange nachdenken, entscheidet sie sofort.",
            "Sport trägt zu einem größeren Wohlbefinden bei.",
            "Vielen Dank für Ihre Aufmerksamkeit.",
        ],
    ),
    4: modul_check(
        LEVEL,
        12,
        dialogue=(
            [
                "A: Stell dir vor, ich habe den Zug verpasst!",
                "B: ___",
                "A: Ja, wäre ich doch bloß früher losgegangen.",
            ],
            "Oh je, das ist wirklich ärgerlich.",
            "Herzlichen Glückwunsch!",
            "Hiermit lade ich dich zum Sommerfest ein.",
        ),
        qa=[
            ("Kommst du zur Weihnachtsfeier?", "Leider nicht, ich bin verreist."),
            ("Was war dein schönster Glücksmoment?", "Als ich die Festanstellung bekam."),
            ("Was ist passiert?", "Ich habe meine Brieftasche liegen lassen."),
            ("Wann beginnt die Sitzung des Betriebsrats?", "Um zehn Uhr."),
            ("Findet der Ausflug statt?", "Ja, trotz des Regens."),
        ],
        odd=[
            ("die Tagesordnung", "der Glücksmoment", "die Freude", "die Erleichterung"),
            ("jubeln", "der Lottoschein", "die Batterie", "das Portemonnaie"),
            ("das Turnier", "die Zusage", "die Absage", "die Einladung"),
            ("plaudern", "zornig", "ärgerlich", "blöd"),
        ],
        reading=(
            """
Lieber Herr Peters,
vielen Dank für die Einladung zum Jubiläum der Firma. Ich habe mich sehr gefreut.
Leider kann ich am Freitag nicht kommen, weil ich an diesem Tag beruflich in
Hamburg bin. Das tut mir wirklich leid. Ich wünsche Ihnen und allen Kollegen eine
schöne Feier. Vielleicht können wir uns nächste Woche zum Mittagessen treffen?
Mit freundlichen Grüßen
Sabine Roth
""",
            [
                ("Frau Roth kommt zum Jubiläum.", False),
                ("Sie ist am Freitag in Hamburg.", True),
                ("Sie hat sich über die Einladung geärgert.", False),
                ("Sie schlägt ein Treffen vor.", True),
            ],
        ),
        form=[
            ("___ ich doch nur aufgepasst! (haben)", "Hätte"),
            ("Nachdem er angekommen ___, rief er an. (sein)", "war"),
            ("Das ist die Tasche ___ Mutter. (meine)", "meiner"),
            ("Trotz des ___ Wetters fahren wir. (kalt)", "kalten"),
            ("Er hatte die Arbeit schon ___. (abgeben)", "abgegeben"),
        ],
        mistake=[
            ("*Hatte* ich doch den Bus genommen!", "Hätte ich doch den Bus genommen!"),
            (
                "Nachdem ich gegessen *habe*, ging ich spazieren.",
                "Nachdem ich gegessen hatte, ging ich spazieren.",
            ),
            ("Das ist der Ausflug *dem* Jahres.", "Das ist der Ausflug des Jahres."),
            (
                "Trotz des schlechten *Wetter* fahren wir.",
                "Trotz des schlechten Wetters fahren wir.",
            ),
        ],
        dictation=[
            "Hätte ich das bloß anders gemacht!",
            "Nachdem wir jahrelang Pech gehabt hatten, gewannen wir.",
            "Das ist der Ausflug des Jahres.",
            "Vielen Dank für Ihre Einladung.",
        ],
    ),
    5: modul_check(
        LEVEL,
        15,
        dialogue=(
            [
                "A: Schön, dass Sie da sind. Erzählen Sie bitte etwas über sich.",
                "B: ___",
                "A: Und warum möchten Sie bei uns arbeiten?",
            ],
            "Ich habe meine Ausbildung 2020 abgeschlossen und spreche sowohl Englisch als auch Spanisch.",
            "Wegen des Lärms konnte ich nichts hören.",
            "Vorsicht, kochendes Wasser!",
        ),
        qa=[
            ("Warum bist du zu spät?", "Wegen eines Staus."),
            ("Braucht man Vorkenntnisse?", "Nein, der Kurs ist für Anfänger."),
            ("Welche Sprachen sprechen Sie?", "Sowohl Deutsch als auch Polnisch."),
            ("Was bedeutet das Wort?", "Es hat zwei Bedeutungen."),
            ("Gibt es noch freie Plätze?", "Nein, der Kurs ist ausgebucht."),
        ],
        odd=[
            ("die Gebühr", "der Hahn", "die Schlange", "der Schalter"),
            ("die Durchsage", "der Bewerber", "die Stellenanzeige", "das Bewerbungsschreiben"),
            ("peinlich", "die Zielgruppe", "die Anmeldung", "die Teilnahme"),
            ("einstellen", "deshalb", "deswegen", "darum"),
        ],
        reading=(
            """
Marta hat im Frühling einen Kletterkurs an der Volkshochschule gemacht. Für den
Kurs brauchte sie keine Vorkenntnisse, aber die Teilnahme war auf eigene Gefahr.
Der Kursleiter war ein ausgebildeter Bergführer. Wegen des schlechten Wetters
fiel ein Termin aus. Trotzdem hat Marta viel gelernt, und deshalb macht sie im
Herbst den Kurs für Fortgeschrittene.
""",
            [
                ("Marta brauchte für den Kurs Vorkenntnisse.", False),
                ("Der Kursleiter hatte eine Ausbildung.", True),
                ("Alle Termine haben stattgefunden.", False),
                ("Marta macht im Herbst noch einen Kurs.", True),
            ],
        ),
        form=[
            ("___ des Regens blieben wir zu Hause. (because of)", "Wegen"),
            ("ein ___ Kind (lachen, Partizip I)", "lachendes"),
            ("die ___ Fotos (machen, Partizip II)", "gemachten"),
            ("Ich spreche ___ Deutsch als auch Englisch.", "sowohl"),
            ("Er ist nicht nur klug, ___ auch fleißig.", "sondern"),
        ],
        mistake=[
            (
                "Es war laut. Deshalb ich *konnte* nichts hören.",
                "Es war laut. Deshalb konnte ich nichts hören.",
            ),
            (
                "Wegen *dem* Lärms konnte ich nicht schlafen.",
                "Wegen des Lärms konnte ich nicht schlafen.",
            ),
            ("Das ist ein *faszinierte* Kurs.", "Das ist ein faszinierender Kurs."),
            (
                "Er ist nicht nur nett, *aber* auch klug.",
                "Er ist nicht nur nett, sondern auch klug.",
            ),
        ],
        dictation=[
            "Aus diesem Grund gab es ein Missverständnis.",
            "Die Teilnahme ist auf eigene Gefahr.",
            "Schön, dass Sie da sind.",
            "Ich spreche sowohl Deutsch als auch Englisch.",
        ],
    ),
    6: modul_check(
        LEVEL,
        18,
        dialogue=(
            [
                "A: Ich finde, man sollte das Auto in der Innenstadt verbieten.",
                "B: ___",
                "A: Warum? Es gibt doch Busse und Fahrräder.",
            ],
            "Davon halte ich nicht viel.",
            "Es lohnt sich, die Galerie zu besuchen.",
            "Wir brauchten uns um nichts zu kümmern.",
        ),
        qa=[
            ("Musstest du als Kind im Haushalt helfen?", "Nein, ich brauchte nichts zu tun."),
            ("Wann wurde die Malerin geboren?", "Im Jahr 1877."),
            ("Wen wählst du?", "Weder Partei A noch Partei B."),
            ("Wie geht es dir?", "Danke, es geht mir gut."),
            ("Was hältst du von der Idee?", "Sie ist zwar gut, aber teuer."),
        ],
        odd=[
            ("der Pinsel", "die Regierung", "das Parlament", "die Partei"),
            ("die Ernte", "das Gemälde", "die Zeichnung", "die Galerie"),
            ("regieren", "die Träne", "der Kuss", "die Lüge"),
            ("farbig", "die Freiheit", "die Sicherheit", "die Möglichkeit"),
        ],
        reading=(
            """
Herr Wagner ist 78 Jahre alt. Als Kind wohnte er auf einem Bauernhof. Er
brauchte nicht jeden Tag in die Schule zu gehen, aber er musste bei der Ernte
helfen. Taschengeld bekam er nie. Heute engagiert er sich ehrenamtlich in einer
Bürgerinitiative für einen Park. Er sagt: Es fällt mir zwar manchmal schwer, aber
es lohnt sich.
""",
            [
                ("Herr Wagner ist in der Stadt aufgewachsen.", False),
                ("Er musste bei der Ernte helfen.", True),
                ("Er bekam jede Woche Taschengeld.", False),
                ("Er arbeitet heute ohne Geld für einen Park.", True),
            ],
        ),
        form=[
            ("Du brauchst nicht ___. (aufstehen)", "aufzustehen"),
            ("___ regnet seit Stunden.", "Es"),
            ("Ich habe ___ Hunger noch Durst. (neither)", "weder"),
            ("möglich → die ___", "Möglichkeit"),
            ("Das Bild ist 1911 ___. (entstehen)", "entstanden"),
        ],
        mistake=[
            ("Du brauchst nicht *kommen*.", "Du brauchst nicht zu kommen."),
            ("Ich muss *zu* arbeiten.", "Ich muss arbeiten."),
            ("Ich habe weder *keine* Zeit noch Geld.", "Ich habe weder Zeit noch Geld."),
            ("Die Malerin wurde *in* 1877 geboren.", "Die Malerin wurde 1877 geboren."),
        ],
        dictation=[
            "Wir brauchten uns um nichts zu kümmern.",
            "Es fällt mir schwer, Nein zu sagen.",
            "Davon halte ich nicht viel.",
            "Ich wähle weder Partei A noch Partei B.",
        ],
    ),
    7: modul_check(
        LEVEL,
        21,
        dialogue=(
            [
                "A: Vielen Dank für Ihren Vortrag über die Heide.",
                "B: Gern. Haben Sie noch Fragen?",
                "A: ___",
            ],
            "Ja, ich hätte dazu noch eine Frage: Wie viele Schafe gibt es dort?",
            "Die Bühne muss aufgebaut werden.",
            "Es schneite, sodass wir bleiben mussten.",
        ),
        qa=[
            ("Wie spart man Energie?", "Indem man das Licht ausschaltet."),
            ("Wo liegt das Stadion?", "Außerhalb der Stadt."),
            ("Was muss vor dem Konzert passieren?", "Es muss geprobt werden."),
            (
                "Warum seid ihr auf der Hütte geblieben?",
                "Es schneite, sodass wir nicht weiterkonnten.",
            ),
            ("Wie war das Konzert?", "Ein einmaliges Erlebnis!"),
        ],
        odd=[
            ("der Lautsprecher", "das Schaf", "die Biene", "die Herde"),
            ("der Gipfel", "die Probe", "der Auftritt", "die Tournee"),
            ("steil", "das Hallenbad", "das Parkhaus", "das Stadion"),
            ("proben", "der Schlafsack", "die Stirnlampe", "der Ohrstöpsel"),
        ],
        reading=(
            """
Die Band Nordlicht ist im Sommer auf Tournee. Vor jedem Auftritt muss die
Bühne aufgebaut und die Technik geprüft werden. Je größer die Halle ist, desto
länger dauert das. In München spielte die Band in einem Stadion außerhalb der
Stadt. Die Karten waren innerhalb einer Stunde verkauft, sodass viele Fans keine
mehr bekamen.
""",
            [
                ("Vor dem Konzert muss die Technik geprüft werden.", True),
                ("In kleinen Hallen dauert der Aufbau länger.", False),
                ("Das Stadion in München liegt im Zentrum.", False),
                ("Nicht alle Fans bekamen Karten.", True),
            ],
        ),
        form=[
            ("Je mehr ich lese, ___ mehr weiß ich.", "desto"),
            ("Man schützt die Natur, ___ man Müll vermeidet. (by)", "indem"),
            ("Die Plakate müssen ___ werden. (verteilen)", "verteilt"),
            ("außerhalb ___ Zentrums (das)", "des"),
            ("Was ist ___ passiert? (interested question)", "denn"),
        ],
        mistake=[
            (
                "Je länger ich übe, desto ich *spreche* sicherer.",
                "Je länger ich übe, desto sicherer spreche ich.",
            ),
            (
                "Man spart Strom, indem man *schaltet* das Licht aus.",
                "Man spart Strom, indem man das Licht ausschaltet.",
            ),
            ("Die Bühne muss aufgebaut *wird*.", "Die Bühne muss aufgebaut werden."),
            (
                "Das Stadion liegt außerhalb *dem* Zentrum.",
                "Das Stadion liegt außerhalb des Zentrums.",
            ),
        ],
        dictation=[
            "Je älter ich wurde, desto mehr reiste ich.",
            "Die anderen werden es dir danken!",
            "Vorher muss natürlich fleißig geübt werden.",
            "Die Altstadt ist immer einen Besuch wert.",
        ],
    ),
    8: modul_check(
        LEVEL,
        24,
        dialogue=(
            [
                "A: Wissen Sie, wann die Mauer geöffnet wurde?",
                "B: ___",
                "A: Danke! Da wäre ich gern dabei gewesen.",
            ],
            "Ja, am 9. November 1989.",
            "Ich fahre Rad, statt das Auto zu nehmen.",
            "Er tut so, als ob er alles wüsste.",
        ),
        qa=[
            ("Wann wurde die BRD gegründet?", "Im Jahr 1949."),
            ("Warum fährst du Rad?", "Um fit zu bleiben."),
            ("Warum sprichst du so langsam?", "Damit alle mich verstehen."),
            ("Wie war der Abend?", "Es war, als ob wir eine große Familie wären."),
            ("Was kann jeder für das Klima tun?", "Abfall vermeiden und Rad fahren."),
        ],
        odd=[
            ("die Bremse", "die Diktatur", "die Republik", "die Revolution"),
            ("die Luftbrücke", "die Klingel", "der Radweg", "das Ersatzteil"),
            ("nachhaltig", "die Einsamkeit", "die Gemeinschaft", "das Zusammenleben"),
            ("bremsen", "um ... zu", "damit", "als ob"),
        ],
        reading=(
            """
In einem Dorf bei Kassel haben sich junge und alte Menschen zusammengeschlossen.
Sie wohnen in einem großen Haus, um sich gegenseitig zu helfen. Die Älteren
kümmern sich um die Kinder, damit die Eltern arbeiten können. Die Jüngeren
kaufen ein und fahren die Älteren mit dem Auto zum Arzt. Anfangs gab es viel
Streit, aber allmählich hat die Gruppe Kompromisse gefunden. Eine Bewohnerin
sagt: Es ist, als ob wir eine große Familie wären.
""",
            [
                ("Im Haus wohnen nur alte Menschen.", False),
                ("Die Älteren passen auf die Kinder auf.", True),
                ("Von Anfang an gab es keine Probleme.", False),
                ("Die Bewohner fühlen sich wie eine Familie.", True),
            ],
        ),
        form=[
            ("Die Mauer ___ 1961 gebaut. (Präteritum)", "wurde"),
            ("Er fuhr weiter, ohne eine Pause ___ machen.", "zu"),
            ("Ich spare, ___ ein Rad zu kaufen.", "um"),
            ("Ich erkläre es, ___ du es verstehst.", "damit"),
            ("Er tut so, als ob er der Chef ___. (sein)", "wäre"),
        ],
        mistake=[
            ("Der Euro ist 2002 eingeführt *geworden*.", "Der Euro ist 2002 eingeführt worden."),
            ("Sie fährt Rad, statt das Auto *nehmen*.", "Sie fährt Rad, statt das Auto zu nehmen."),
            (
                "Ich lerne, *damit* die Prüfung zu bestehen.",
                "Ich lerne, um die Prüfung zu bestehen.",
            ),
            ("Er tut so, als ob er alles *weiß*.", "Er tut so, als ob er alles wüsste."),
        ],
        dictation=[
            "In der BRD wurde die Demokratie eingeführt.",
            "Fahrradfahren ist in.",
            "Das löst mehrere Probleme auf einmal.",
            "Er tut so, als ob er alles wüsste.",
        ],
    ),
}
