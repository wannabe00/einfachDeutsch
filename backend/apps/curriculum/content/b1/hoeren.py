"""B1 Hören sets, shaped like the Goethe-Zertifikat B1 listening paper: one set
per Modul, 30 questions. Teil 1: 5 short texts (radio, announcements, phone
messages), each with a richtig/falsch and an a/b/c question, heard twice.
Teil 2: a talk or guided tour, 5 questions a/b/c, heard once. Teil 3: a
conversation, 7 richtig/falsch, heard once. Teil 4: a radio discussion with a
host and two guests, 8 statements: who says it? Heard twice.

All scripts are original, on the Modul's topics. The audio is generated once
with `manage.py make_hoeren_audio --level B1`; a Modul goes live in production
when it is added to `LIVE` after its audio exists (DEBUG shows every set).
"""

from ..a2.hoeren import _sound
from ..dsl import clip, hoeren_teil, hoeren_tf, hoeren_who, mc

# Empty until the B1 audio is recorded (owner runs make_hoeren_audio locally).
LIVE: set[int] = set()

SHORT = "Listen to the text. Answer both questions. (You hear it twice.)"
TALK = "Listen to the talk. Choose a, b or c. (You hear it once.)"
CHAT = "Listen to the conversation. Richtig oder falsch? (You hear it once.)"
DEBATE = "Listen to the discussion. Who says what? (You hear it twice.)"

# Where each Modul's talk (Teil 2) and conversation (Teil 3) take place.
SCENES = {
    1: ("strasse", "cafe"),
    2: ("buero", "cafe"),
    3: ("buero", "park"),
    4: ("", "cafe"),
    5: ("buero", "cafe"),
    6: ("", "cafe"),
    7: ("park", "strasse"),
    8: ("strasse", "cafe"),
}


def _set(modul, short, talk, chat, debate) -> list:
    talk_scene, chat_scene = SCENES[modul]
    speaker, lines, questions = talk
    conversation, statements = chat
    guests, discussion, who = debate
    return [
        *[
            hoeren_teil(
                1,
                SHORT,
                hoeren_tf(*tf),
                mc(*q),
                recording=clip((who_, text), **_sound(who_, text)),
            )
            for who_, text, tf, q in short
        ],
        hoeren_teil(
            2,
            TALK,
            *[mc(*q) for q in questions],
            recording=clip(*[(speaker, line) for line in lines], plays=1, scene=talk_scene),
        ),
        hoeren_teil(
            3,
            CHAT,
            *[hoeren_tf(*s) for s in statements],
            recording=clip(*conversation, plays=1, scene=chat_scene),
        ),
        hoeren_teil(
            4,
            DEBATE,
            *[hoeren_who(s, guests[k], guests) for s, k in who],
            recording=clip(*discussion, plays=2, radio=True),
        ),
    ]


HOST = "Moderatorin"  # the host is always the "Ansage" voice


def _guests(frau: str, mann: str) -> list[str]:
    """The answer options for Teil 4: host, the woman guest, the man guest."""
    return [HOST, frau, mann]


HOEREN = {
    # Modul 1 (Lektionen 1-3): friendship, internships, housing.
    1: _set(
        1,
        [
            (
                "Ansage",
                "Und jetzt unser Wohnungstipp der Woche: In der Innenstadt ist eine helle Dreizimmerwohnung mit Dachterrasse frei. Die Miete beträgt neunhundert Euro, Besichtigung am Donnerstag um achtzehn Uhr.",
                ("Die Wohnung hat eine Dachterrasse.", True),
                (
                    "Wann kann man die Wohnung besichtigen?",
                    "Am Donnerstag",
                    "Am Dienstag",
                    "Am Wochenende",
                ),
            ),
            (
                "Frau",
                "Hallo Max, hier ist Sandra. Ich habe gehört, dass du ab Montag dein Praktikum bei uns machst. Toll! Bring bitte deinen Ausweis mit, weil du einen Schlüssel für das Büro bekommst. Bis Montag!",
                ("Max beginnt sein Praktikum am Dienstag.", False),
                ("Was soll Max mitbringen?", "Seinen Ausweis", "Einen Schlüssel", "Sein Zeugnis"),
            ),
            (
                "Ansage",
                "Liebe Kunden, unser Möbelhaus feiert Geburtstag. Heute bekommen alle, die ein Sofa kaufen, einen Sessel gratis dazu. Das Angebot gilt nur bis achtzehn Uhr.",
                ("Das Angebot gilt den ganzen Tag bis Mitternacht.", False),
                ("Was bekommt man heute gratis?", "Einen Sessel", "Ein Sofa", "Einen Tisch"),
            ),
            (
                "Mann",
                "Guten Tag, Frau Kraus, hier spricht Herr Weber, der Hausmeister. Die Heizung in Ihrer Wohnung wird morgen zwischen neun und elf repariert. Bitte seien Sie dann zu Hause oder geben Sie den Schlüssel bei Ihrer Nachbarin ab.",
                ("Der Hausmeister repariert morgen die Heizung.", True),
                (
                    "Was soll Frau Kraus tun?",
                    "Zu Hause sein oder den Schlüssel abgeben",
                    "Die Heizung reparieren",
                    "Den Hausmeister anrufen",
                ),
            ),
            (
                "Ansage",
                "Eine aktuelle Umfrage zeigt: Fast die Hälfte der jungen Erwachsenen wohnt noch bei den Eltern. Der wichtigste Grund ist die hohe Miete in den Großstädten.",
                ("Die meisten jungen Erwachsenen wohnen allein.", False),
                (
                    "Warum wohnen viele junge Leute bei den Eltern?",
                    "Die Miete ist hoch.",
                    "Sie mögen ihre Eltern.",
                    "Sie studieren nicht.",
                ),
            ),
        ],
        (
            "Frau",
            [
                "Herzlich willkommen in der Wohnanlage Sonnenhof! Ich bin Frau Albers, die Verwalterin, und zeige Ihnen heute die Anlage.",
                "Hier wohnen zweihundert Menschen in achtzig Wohnungen, Familien, Studenten und Rentner.",
                "Wir stehen jetzt im Innenhof. Im Sommer feiern wir hier jedes Jahr ein Hoffest, zu dem alle Bewohner kommen.",
                "Links sehen Sie den Gemeinschaftsraum. Den können Bewohner für Geburtstage mieten, er kostet nur zwanzig Euro.",
                "Die Fahrräder stehen im Keller, nicht im Hausflur. Das ist eine wichtige Regel.",
                "Unser Hausmeister, Herr Brandt, ist jeden Tag von sieben bis fünfzehn Uhr da. Danach rufen Sie bitte den Notdienst an.",
            ],
            [
                ("Wie viele Wohnungen hat die Anlage?", "Achtzig", "Zweihundert", "Zwanzig"),
                (
                    "Was passiert jeden Sommer im Innenhof?",
                    "Ein Hoffest",
                    "Ein Konzert",
                    "Ein Flohmarkt",
                ),
                ("Was kostet der Gemeinschaftsraum?", "Zwanzig Euro", "Nichts", "Achtzig Euro"),
                ("Wo stehen die Fahrräder?", "Im Keller", "Im Hausflur", "Im Innenhof"),
                (
                    "Bis wann ist der Hausmeister da?",
                    "Bis fünfzehn Uhr",
                    "Bis sieben Uhr",
                    "Bis siebzehn Uhr",
                ),
            ],
        ),
        (
            [
                ("Frau", "Und, wie war deine erste Woche im Praktikum?"),
                (
                    "Mann",
                    "Super! Am Montag habe ich alle Kollegen kennengelernt. Der Chef war sehr freundlich.",
                ),
                ("Frau", "Und musstest du schon richtig arbeiten?"),
                (
                    "Mann",
                    "Ja, am Dienstag habe ich zum ersten Mal Kunden am Telefon beraten. Das war schwer, weil manche sehr schnell sprechen.",
                ),
                ("Frau", "Und die Kollegen? Duzt ihr euch?"),
                (
                    "Mann",
                    "Ja, alle duzen sich, sogar der Chef. Am Mittwoch hatten wir eine große Teamsitzung, und ich durfte etwas präsentieren.",
                ),
                ("Frau", "Wow! Und wo wohnst du jetzt?"),
                (
                    "Mann",
                    "Noch in einem kleinen WG-Zimmer am Stadtrand. Ich brauche fast eine Stunde ins Büro. Ab nächstem Monat ziehe ich aber in die Innenstadt.",
                ),
            ],
            [
                ("Der Mann hat am Montag die Kollegen kennengelernt.", True),
                ("Der Chef war unfreundlich.", False),
                ("Am Telefon war es für ihn leicht.", False),
                ("In der Firma sagen alle du.", True),
                ("Am Mittwoch hat er etwas präsentiert.", True),
                ("Er wohnt im Moment in der Innenstadt.", False),
                ("Er braucht im Moment lange ins Büro.", True),
            ],
        ),
        (
            _guests("Frau Becker", "Herr Lindner"),
            [
                (
                    "Ansage",
                    "Willkommen zu unserer Sendung. Heute geht es um die Frage: Wohnen wir in Zukunft alle allein? Bei mir sind die Maklerin Frau Becker und der Student Herr Lindner.",
                ),
                (
                    "Frau",
                    "Ich sehe in meinem Beruf jeden Tag, dass immer mehr Menschen allein wohnen. Besonders ältere Leute suchen kleine Wohnungen.",
                ),
                (
                    "Mann",
                    "Bei jungen Leuten ist das anders. Wir können uns allein gar keine Wohnung leisten, deshalb wohnen fast alle meine Freunde in einer WG.",
                ),
                ("Ansage", "Ist das für Sie nur eine Frage des Geldes?"),
                (
                    "Mann",
                    "Nein, nicht nur. In einer WG ist man nie einsam. Ich finde das sogar schöner als allein zu wohnen.",
                ),
                (
                    "Frau",
                    "Das verstehe ich. Aber viele Menschen brauchen ab einem bestimmten Alter ihre Ruhe.",
                ),
                ("Ansage", "Was müsste sich denn ändern?"),
                (
                    "Frau",
                    "Die Städte müssen mehr Wohnungen bauen, in denen man allein wohnt, aber zum Beispiel einen Garten teilt.",
                ),
                (
                    "Mann",
                    "Und die Mieten müssen sinken. Sonst ziehen junge Leute bald alle aufs Land.",
                ),
                ("Ansage", "Vielen Dank Ihnen beiden für das Gespräch."),
            ],
            [
                ("Ich stelle meine Gäste vor.", 0),
                ("Immer mehr Menschen wohnen allein.", 1),
                ("Fast alle meine Freunde wohnen in einer WG.", 2),
                ("Ist es nur eine Frage des Geldes?", 0),
                ("In einer WG ist man nie einsam.", 2),
                ("Viele brauchen ab einem bestimmten Alter Ruhe.", 1),
                ("Man sollte Wohnungen mit einem gemeinsamen Garten bauen.", 1),
                ("Die Mieten müssen niedriger werden.", 2),
            ],
        ),
    ),
    # Modul 2 (Lektionen 4-6): complaints, technology, invitations.
    2: _set(
        2,
        [
            (
                "Ansage",
                "Herzlich willkommen beim Kundenservice von Telenet. Für Fragen zu Ihrer Rechnung drücken Sie bitte die Eins. Bei technischen Problemen drücken Sie die Zwei. Für eine persönliche Beratung bleiben Sie bitte am Apparat.",
                ("Für eine persönliche Beratung muss man eine Taste drücken.", False),
                (
                    "Was macht man bei technischen Problemen?",
                    "Die Zwei drücken",
                    "Die Eins drücken",
                    "Am Apparat bleiben",
                ),
            ),
            (
                "Mann",
                "Hallo Lisa, hier ist Paul. Danke für die Einladung zum Essen am Freitag! Ich komme gern. Ich bringe einen Nachtisch mit, falls du das möchtest. Ruf mich kurz zurück!",
                ("Paul kommt zum Essen.", True),
                ("Was will Paul mitbringen?", "Einen Nachtisch", "Blumen", "Wein"),
            ),
            (
                "Ansage",
                "Experten vermuten, dass in zwanzig Jahren in fast jedem Haushalt ein Roboter arbeiten wird. Die Roboter werden putzen, kochen und sogar mit älteren Menschen sprechen.",
                ("Experten glauben, dass Roboter bald im Haushalt helfen werden.", True),
                (
                    "Wann wird es laut Experten so weit sein?",
                    "In zwanzig Jahren",
                    "In zwei Jahren",
                    "In fünfzig Jahren",
                ),
            ),
            (
                "Frau",
                "Guten Tag, hier ist Frau Klein von der Firma Lexa. Wir haben Ihre Reklamation erhalten. Obwohl das Gerät noch neu ist, ist es leider kaputt. Wir schicken Ihnen diese Woche ein neues Gerät.",
                ("Das Gerät ist schon sehr alt.", False),
                (
                    "Was passiert mit der Reklamation?",
                    "Der Kunde bekommt ein neues Gerät.",
                    "Der Kunde bekommt sein Geld zurück.",
                    "Der Kunde muss das Gerät reparieren.",
                ),
            ),
            (
                "Ansage",
                "Liebe Gäste, unser Restaurant schließt heute schon um zweiundzwanzig Uhr. Falls Sie noch einen Nachtisch bestellen möchten, sagen Sie bitte jetzt Bescheid.",
                ("Man kann noch einen Nachtisch bestellen.", True),
                ("Wann schließt das Restaurant heute?", "Um 22 Uhr", "Um 20 Uhr", "Um Mitternacht"),
            ),
        ],
        (
            "Mann",
            [
                "Guten Tag und herzlich willkommen zu unserem Seminar „Gut telefonieren im Kundenservice“. Mein Name ist Herr Roth.",
                "Viele Kunden rufen an, weil sie sich ärgern. Das Wichtigste ist deshalb, ruhig und freundlich zu bleiben, auch wenn der Kunde laut wird.",
                "Nennen Sie am Anfang immer die Firma und Ihren Namen. So weiß der Kunde, mit wem er spricht.",
                "Wenn Sie nicht zuständig sind, verbinden Sie den Kunden mit der richtigen Abteilung. Sagen Sie ihm aber vorher, wohin Sie ihn verbinden.",
                "Versprechen Sie nichts, was Sie nicht halten können. Ein Rückruf, der nicht kommt, ist schlimmer als eine ehrliche Antwort.",
                "Heute Nachmittag üben wir das in kleinen Gruppen mit echten Situationen.",
            ],
            [
                (
                    "Warum rufen viele Kunden an?",
                    "Weil sie sich ärgern",
                    "Weil sie etwas kaufen wollen",
                    "Weil sie Herrn Roth kennen",
                ),
                (
                    "Was soll man am Anfang sagen?",
                    "Die Firma und seinen Namen",
                    "Die Telefonnummer",
                    "Den Preis",
                ),
                (
                    "Was soll man tun, wenn man nicht zuständig ist?",
                    "Den Kunden richtig verbinden",
                    "Auflegen",
                    "Später anrufen",
                ),
                (
                    "Was ist laut Herrn Roth schlimm?",
                    "Ein Rückruf, der nicht kommt",
                    "Eine ehrliche Antwort",
                    "Eine lange Warteschleife",
                ),
                (
                    "Was machen die Teilnehmer am Nachmittag?",
                    "Sie üben in Gruppen.",
                    "Sie haben frei.",
                    "Sie schreiben einen Test.",
                ),
            ],
        ),
        (
            [
                ("Frau", "Also, für das Fest am Samstag: Wer bringt was mit?"),
                (
                    "Mann",
                    "Klaus bringt den Salat, das hat er schon gesagt. Und Maria backt einen Kuchen.",
                ),
                ("Frau", "Gut. Und Jonas? Er kann doch nicht kochen."),
                ("Mann", "Jonas kümmert sich um die Getränke. Er bringt Wasser, Saft und Sekt."),
                (
                    "Frau",
                    "Tante Erna hat geschrieben, dass sie seit Kurzem keine Nüsse essen darf.",
                ),
                ("Mann", "Dann darf im Kuchen keine Nuss sein. Ich sage es Maria."),
                ("Frau", "Und wann sollen die Gäste kommen? Um sechs oder um sieben?"),
                ("Mann", "Um sieben. Vorher müssen wir noch die Wohnung aufräumen."),
            ],
            [
                ("Klaus bringt einen Salat mit.", True),
                ("Maria bringt die Getränke mit.", False),
                ("Jonas kann gut kochen.", False),
                ("Tante Erna ist allergisch gegen Nüsse.", True),
                ("Der Mann wird mit Maria sprechen.", True),
                ("Die Gäste kommen um sechs Uhr.", False),
                ("Vor dem Fest wollen sie aufräumen.", True),
            ],
        ),
        (
            _guests("Frau Doktor Kühn", "Herr Lang"),
            [
                (
                    "Ansage",
                    "In unserer Sendung diskutieren wir heute: Machen uns Computer das Leben leichter? Bei mir sind die Forscherin Frau Doktor Kühn und der Landwirt Herr Lang.",
                ),
                (
                    "Frau",
                    "Ich bin davon überzeugt, dass Computer uns in Zukunft viel Arbeit abnehmen werden, zum Beispiel im Haushalt.",
                ),
                (
                    "Mann",
                    "Auf meinem Bauernhof hilft mir der Computer schon heute. Er sagt mir, wann meine Kühe Futter brauchen.",
                ),
                ("Ansage", "Gibt es auch Nachteile?"),
                (
                    "Mann",
                    "Ja. Wenn das Internet nicht funktioniert, steht bei mir alles still. Dann fühle ich mich ganz abhängig.",
                ),
                (
                    "Frau",
                    "Viele Menschen haben außerdem Angst, dass Maschinen ihren Arbeitsplatz ersetzen werden.",
                ),
                ("Ansage", "Und was glauben Sie: Wird das passieren?"),
                ("Frau", "Manche Berufe werden verschwinden, aber es wird auch neue geben."),
                (
                    "Mann",
                    "Ich werde jedenfalls nie einen Roboter für meine Kühe kaufen. Das mache ich lieber selbst.",
                ),
            ],
            [
                ("Machen Computer das Leben leichter?", 0),
                ("Computer werden uns im Haushalt helfen.", 1),
                ("Der Computer sagt mir, wann die Tiere Futter brauchen.", 2),
                ("Gibt es auch Nachteile?", 0),
                ("Ohne Internet funktioniert bei mir nichts.", 2),
                ("Viele haben Angst um ihren Arbeitsplatz.", 1),
                ("Es wird neue Berufe geben.", 1),
                ("Ich möchte keinen Roboter für meine Tiere.", 2),
            ],
        ),
    ),
    # Modul 3 (Lektionen 7-9): pets, careers, health at work.
    3: _set(
        3,
        [
            (
                "Ansage",
                "Das Tierheim Pfötchen sucht ein neues Zuhause für drei junge Katzen. Die Tiere sind sehr zutraulich und schon geimpft. Besuchen Sie uns am Samstag zwischen zehn und vierzehn Uhr.",
                ("Die Katzen sind sehr ängstlich.", False),
                ("Wann kann man die Katzen besuchen?", "Am Samstag", "Am Sonntag", "Jeden Tag"),
            ),
            (
                "Frau",
                "Hallo Ben, hier ist Mama. Kannst du bitte morgen das Kaninchen füttern? Ich muss früh zur Arbeit. Das Futter steht im Keller, und vergiss nicht, frisches Wasser in den Napf zu tun.",
                ("Das Futter ist im Keller.", True),
                (
                    "Was soll Ben machen?",
                    "Das Kaninchen füttern",
                    "Futter kaufen",
                    "Zum Tierarzt gehen",
                ),
            ),
            (
                "Ansage",
                "Liebe Mitarbeiter, morgen ist Gesundheitstag. Von neun bis zwölf Uhr gibt es in Halle A Rückentraining. Bitte bringen Sie bequeme Kleidung mit.",
                ("Das Rückentraining ist am Nachmittag.", False),
                ("Was soll man mitbringen?", "Bequeme Kleidung", "Etwas zu essen", "Einen Ausweis"),
            ),
            (
                "Mann",
                "Guten Tag, Frau Neumann, hier ist die Berufsberatung. Ihr Termin am Montag muss leider ausfallen, weil die Beraterin krank ist. Könnten Sie stattdessen am Mittwoch um zehn kommen?",
                ("Die Beraterin ist krank.", True),
                (
                    "Wann ist der neue Termin?",
                    "Am Mittwoch um zehn",
                    "Am Montag um zehn",
                    "Am Mittwoch um zwölf",
                ),
            ),
            (
                "Ansage",
                "Eine neue Studie zeigt: Wer bei der Arbeit regelmäßig Pausen macht, ist nicht nur gesünder, sondern auch zufriedener. Schon zehn Minuten an der frischen Luft helfen gegen Stress.",
                ("Pausen machen Menschen zufriedener.", True),
                (
                    "Was hilft laut der Studie gegen Stress?",
                    "Zehn Minuten an der frischen Luft",
                    "Mehr Arbeit",
                    "Weniger Schlaf",
                ),
            ),
        ],
        (
            "Frau",
            [
                "Guten Morgen! Ich möchte Ihnen heute unser neues Gesundheitskonzept vorstellen. Mein Name ist Frau Wolff, ich leite die Personalabteilung.",
                "Zuerst einige Zahlen: Im letzten Jahr waren unsere Mitarbeiter im Durchschnitt zwölf Tage krank, meistens wegen Rückenschmerzen.",
                "Deshalb gibt es ab März jeden Dienstag und Donnerstag eine kurze Gymnastik direkt am Arbeitsplatz.",
                "In der Kantine bieten wir ab sofort jeden Tag ein vegetarisches Gericht und frisches Obst an.",
                "Außerdem bezahlt die Firma allen Mitarbeitern die Hälfte vom Fitnessstudio.",
                "Fragen beantworte ich gern am Schluss. Damit komme ich zum nächsten Punkt.",
            ],
            [
                (
                    "Wer ist Frau Wolff?",
                    "Die Leiterin der Personalabteilung",
                    "Eine Ärztin",
                    "Eine Trainerin",
                ),
                (
                    "Warum waren die Mitarbeiter oft krank?",
                    "Wegen Rückenschmerzen",
                    "Wegen Erkältungen",
                    "Wegen Stress",
                ),
                (
                    "Wann gibt es Gymnastik?",
                    "Dienstag und Donnerstag",
                    "Jeden Tag",
                    "Nur am Montag",
                ),
                (
                    "Was gibt es neu in der Kantine?",
                    "Ein vegetarisches Gericht",
                    "Kostenloses Essen",
                    "Fleisch jeden Tag",
                ),
                (
                    "Was bezahlt die Firma?",
                    "Die Hälfte vom Fitnessstudio",
                    "Das ganze Fitnessstudio",
                    "Neue Schreibtische",
                ),
            ],
        ),
        (
            [
                (
                    "Mann",
                    "Wir haben im Kurs den Berufstest gemacht. Rate mal, was bei mir rausgekommen ist!",
                ),
                ("Frau", "Erzähl! Bist du ein technischer Typ?"),
                (
                    "Mann",
                    "Nein, ein sozialer Typ. Der Test sagt, dass ich Lehrer werden soll. Das hätte ich nicht erwartet.",
                ),
                ("Frau", "Warum nicht? Du erklärst doch immer allen alles."),
                (
                    "Mann",
                    "Stimmt. Aber eigentlich wollte ich Mechaniker werden, weil ich gern Autos repariere.",
                ),
                (
                    "Frau",
                    "Du könntest ja beides verbinden: Lehrer an einer Berufsschule für Mechaniker.",
                ),
                (
                    "Mann",
                    "Gute Idee! Bevor ich mich entscheide, mache ich aber noch ein Praktikum.",
                ),
            ],
            [
                ("Der Mann hat den Test zu Hause gemacht.", False),
                ("Laut Test ist er ein sozialer Typ.", True),
                ("Er hat das Ergebnis erwartet.", False),
                ("Die Frau findet, dass er gut erklären kann.", True),
                ("Er wollte eigentlich Mechaniker werden.", True),
                ("Die Frau schlägt vor, an einer Berufsschule zu unterrichten.", True),
                ("Er entscheidet sich sofort.", False),
            ],
        ),
        (
            _guests("Frau Sanders", "Herr Doktor Behr"),
            [
                (
                    "Ansage",
                    "Heute fragen wir: Gehören Hunde ins Büro? Zu Gast sind die Chefin einer Agentur, Frau Sanders, und der Tierarzt Herr Doktor Behr.",
                ),
                (
                    "Frau",
                    "In unserer Agentur dürfen die Mitarbeiter ihre Hunde seit zwei Jahren mitbringen, und die Atmosphäre ist viel besser geworden.",
                ),
                (
                    "Mann",
                    "Für den Hund ist das oft gut, weil er nicht den ganzen Tag allein zu Hause bleibt.",
                ),
                ("Ansage", "Und was ist mit Kollegen, die Angst vor Hunden haben?"),
                (
                    "Frau",
                    "Dafür haben wir klare Regeln. Wer allergisch ist oder Angst hat, bekommt ein Büro ohne Tiere.",
                ),
                (
                    "Mann",
                    "Man muss aber auch sagen: Nicht jeder Hund ist für ein Büro geeignet. Manche sind zu nervös.",
                ),
                ("Ansage", "Was raten Sie Firmen, die das ausprobieren möchten?"),
                ("Mann", "Fangen Sie mit wenigen, ruhigen Hunden an."),
                ("Frau", "Und sprechen Sie vorher mit allen Mitarbeitern."),
            ],
            [
                ("Gehören Hunde ins Büro?", 0),
                ("Die Atmosphäre ist viel besser geworden.", 1),
                ("Der Hund ist dann nicht allein zu Hause.", 2),
                ("Was ist mit Kollegen, die Angst haben?", 0),
                ("Wer allergisch ist, bekommt ein anderes Büro.", 1),
                ("Nicht jeder Hund passt ins Büro.", 2),
                ("Man sollte mit ruhigen Hunden anfangen.", 2),
                ("Man sollte vorher mit allen sprechen.", 1),
            ],
        ),
    ),
    # Modul 4 (Lektionen 10-12): mishaps, happiness, company events.
    4: _set(
        4,
        [
            (
                "Ansage",
                "Liebe Fahrgäste, wegen einer technischen Störung fährt der Zug nach Hamburg heute von Gleis sieben statt von Gleis drei. Wir bitten um Entschuldigung.",
                ("Der Zug nach Hamburg fällt aus.", False),
                (
                    "Von welchem Gleis fährt der Zug?",
                    "Von Gleis sieben",
                    "Von Gleis drei",
                    "Von Gleis zehn",
                ),
            ),
            (
                "Frau",
                "Hallo Tom, hier ist Kerstin. Stell dir vor, ich habe die Festanstellung bekommen! Nachdem ich so lange gewartet hatte, kam heute endlich der Anruf. Wir müssen feiern! Ruf mich an!",
                ("Kerstin musste lange auf die Antwort warten.", True),
                (
                    "Warum ruft Kerstin an?",
                    "Sie hat eine feste Stelle bekommen.",
                    "Sie hat Geburtstag.",
                    "Sie hat ihren Job verloren.",
                ),
            ),
            (
                "Ansage",
                "Ein Glücksmoment für den FC Seestadt: Nachdem die Mannschaft jahrelang Pech gehabt hatte, hat sie gestern das Turnier gewonnen. Die Fans haben bis Mitternacht gefeiert.",
                ("Die Mannschaft hat in den letzten Jahren oft gewonnen.", False),
                (
                    "Was ist gestern passiert?",
                    "Die Mannschaft hat gewonnen.",
                    "Die Mannschaft hat verloren.",
                    "Das Turnier ist ausgefallen.",
                ),
            ),
            (
                "Mann",
                "Guten Tag, hier ist das Fundbüro der Stadt. Herr Petersen, wir haben Ihre Brieftasche gefunden. Sie können sie von Montag bis Freitag bis sechzehn Uhr abholen.",
                ("Herr Petersen hat seine Brieftasche verloren.", True),
                (
                    "Bis wann kann Herr Petersen die Brieftasche abholen?",
                    "Bis 16 Uhr",
                    "Bis 18 Uhr",
                    "Nur am Montag",
                ),
            ),
            (
                "Ansage",
                "Liebe Mitarbeiter, unser Betriebsausflug findet trotz des schlechten Wetterberichts statt. Wir treffen uns am Freitag um acht Uhr vor dem Haupteingang. Bitte denken Sie an eine Regenjacke.",
                ("Der Ausflug fällt wegen des Wetters aus.", False),
                (
                    "Was sollen die Mitarbeiter mitbringen?",
                    "Eine Regenjacke",
                    "Etwas zu essen",
                    "Ihren Ausweis",
                ),
            ),
        ],
        (
            "Mann",
            [
                "Liebe Kolleginnen und Kollegen, herzlich willkommen zu unserem Sommerfest! Ich bin Thomas Albers, der Geschäftsführer.",
                "Unsere Firma wird dieses Jahr fünfundzwanzig Jahre alt. Angefangen haben wir mit nur drei Mitarbeitern in einer Garage.",
                "Heute sind wir hundertzwanzig, und darauf bin ich sehr stolz.",
                "Besonders danken möchte ich Frau Lenz. Sie ist seit dem ersten Tag dabei und geht im Herbst in Rente.",
                "Nach dem Essen gibt es eine Bootsfahrt auf dem See. Die Boote fahren um sechzehn Uhr.",
                "Und jetzt: Das Buffet ist eröffnet. Viel Vergnügen!",
            ],
            [
                (
                    "Wie alt ist die Firma?",
                    "Fünfundzwanzig Jahre",
                    "Drei Jahre",
                    "Hundertzwanzig Jahre",
                ),
                (
                    "Wo hat die Firma angefangen?",
                    "In einer Garage",
                    "In einem Büro",
                    "Auf einem Boot",
                ),
                (
                    "Wie viele Mitarbeiter hat die Firma heute?",
                    "Hundertzwanzig",
                    "Drei",
                    "Fünfundzwanzig",
                ),
                (
                    "Was macht Frau Lenz im Herbst?",
                    "Sie geht in Rente.",
                    "Sie wird Chefin.",
                    "Sie macht eine Reise.",
                ),
                (
                    "Was passiert um sechzehn Uhr?",
                    "Die Boote fahren.",
                    "Das Buffet beginnt.",
                    "Das Fest endet.",
                ),
            ],
        ),
        (
            [
                ("Mann", "Warum bist du so spät? Der Film hat schon angefangen."),
                ("Frau", "Frag nicht! Zuerst habe ich meinen Schlüssel in der Wohnung vergessen."),
                ("Mann", "Oh je. Und wie bist du dann reingekommen?"),
                (
                    "Frau",
                    "Meine Nachbarin hat einen Ersatzschlüssel. Aber sie war nicht zu Hause, ich musste eine halbe Stunde warten.",
                ),
                ("Mann", "Das ist ja dumm gelaufen."),
                (
                    "Frau",
                    "Und dann habe ich den Bus verpasst. Wäre ich doch nur mit dem Fahrrad gefahren!",
                ),
                (
                    "Mann",
                    "Komm, wir sehen den Film einfach morgen noch einmal. Die Karten kann man umtauschen.",
                ),
            ],
            [
                ("Der Film hatte schon begonnen.", True),
                ("Die Frau hat ihr Handy vergessen.", False),
                ("Die Nachbarin hat einen Schlüssel für die Wohnung.", True),
                ("Die Nachbarin war sofort da.", False),
                ("Die Frau hat den Bus verpasst.", True),
                ("Die Frau ist mit dem Fahrrad gekommen.", False),
                ("Sie wollen den Film am nächsten Tag sehen.", True),
            ],
        ),
        (
            _guests("Frau Seidel", "Herr Brandl"),
            [
                (
                    "Ansage",
                    "Unser Thema heute: Pech im Alltag. Bei mir sind die Psychologin Frau Seidel und der Autor Herr Brandl, der ein Buch über Missgeschicke geschrieben hat.",
                ),
                (
                    "Mann",
                    "Mir passieren ständig dumme Dinge. Letzte Woche habe ich meinen Schlüssel in der Tür stecken lassen.",
                ),
                (
                    "Frau",
                    "Viele Menschen ärgern sich darüber sehr lange. Das ist aber nicht gesund.",
                ),
                ("Ansage", "Was kann man denn tun, wenn etwas schiefgeht?"),
                (
                    "Frau",
                    "Man sollte sich fragen: Ist das in einem Jahr noch wichtig? Meistens ist die Antwort nein.",
                ),
                (
                    "Mann",
                    "Ich lache heute darüber. Nachdem ich einmal einen Zug verpasst hatte, habe ich am Bahnhof meine Frau kennengelernt!",
                ),
                ("Ansage", "Also kann Pech auch Glück bringen?"),
                ("Mann", "Auf jeden Fall. Da kann man sowieso nichts machen."),
                ("Frau", "Wichtig ist nur, dass man aus seinen Fehlern lernt."),
            ],
            [
                ("Heute sprechen wir über Pech im Alltag.", 0),
                ("Ich habe den Schlüssel in der Tür vergessen.", 2),
                ("Langer Ärger ist nicht gesund.", 1),
                ("Was kann man tun, wenn etwas schiefgeht?", 0),
                ("Fragen Sie sich, ob es in einem Jahr noch wichtig ist.", 1),
                ("Ich habe meine Frau am Bahnhof kennengelernt.", 2),
                ("Kann Pech auch Glück bringen?", 0),
                ("Man sollte aus seinen Fehlern lernen.", 1),
            ],
        ),
    ),
    # Modul 5 (Lektionen 13-15): misunderstandings, courses, applications.
    5: _set(
        5,
        [
            (
                "Ansage",
                "Die Volkshochschule informiert: Das neue Semester beginnt am fünfzehnten September. Die Anmeldung ist ab sofort online möglich. Viele Kurse sind schnell ausgebucht, melden Sie sich deshalb früh an.",
                ("Man kann sich nur persönlich anmelden.", False),
                ("Wann beginnt das Semester?", "Am 15. September", "Am 5. September", "Heute"),
            ),
            (
                "Mann",
                "Guten Tag, Frau Novak, hier ist Herr Lorenz vom Hotel Bergblick. Vielen Dank für Ihre Bewerbung. Wir möchten Sie gern zu einem Vorstellungsgespräch einladen, am Dienstag um vierzehn Uhr. Bitte bestätigen Sie den Termin.",
                ("Frau Novak hat sich bei einem Hotel beworben.", True),
                (
                    "Was soll Frau Novak tun?",
                    "Den Termin bestätigen",
                    "Eine neue Bewerbung schicken",
                    "Sofort vorbeikommen",
                ),
            ),
            (
                "Ansage",
                "Achtung am Gleis vier: Wegen Bauarbeiten fällt der Regionalzug nach Bonn heute aus. Bitte nehmen Sie den Bus vor dem Bahnhof.",
                ("Der Zug fällt wegen eines Unfalls aus.", False),
                (
                    "Wie kommt man heute nach Bonn?",
                    "Mit dem Bus",
                    "Mit dem Regionalzug",
                    "Gar nicht",
                ),
            ),
            (
                "Frau",
                "Hallo Jan, hier ist Mia. Ich glaube, es gab ein Missverständnis: Das Treffen ist nicht heute, sondern morgen. Ich warte also nicht im Café. Bis morgen!",
                ("Mia wartet heute im Café.", False),
                ("Wann ist das Treffen?", "Morgen", "Heute", "Nächste Woche"),
            ),
            (
                "Ansage",
                "Neu im Programm: Klettern für Anfänger. Vorkenntnisse sind nicht nötig. Die Teilnahme ist auf eigene Gefahr. Der Kurs kostet achtzig Euro.",
                ("Für den Kurs braucht man keine Vorkenntnisse.", True),
                ("Was kostet der Kletterkurs?", "80 Euro", "18 Euro", "Er ist kostenlos."),
            ),
        ],
        (
            "Frau",
            [
                "Herzlich willkommen zum Infoabend der Volkshochschule. Ich bin Frau Engel und leite den Bereich Sprachen.",
                "Unsere Deutschkurse gibt es auf allen Niveaus, von A1 bis C1. Vor dem ersten Kurs machen Sie bei uns einen kurzen Einstufungstest.",
                "Neu ist der Kurs „Deutsch für den Beruf“. Dort üben Sie Telefonieren, E-Mails und Vorstellungsgespräche.",
                "Die Kurse finden abends oder samstags statt, damit auch Berufstätige teilnehmen können.",
                "Wenn Sie wenig Geld haben, können Sie eine Ermäßigung bekommen. Fragen Sie einfach an der Anmeldung.",
                "Am Ende jedes Kurses können Sie eine Prüfung machen und bekommen ein Zertifikat.",
            ],
            [
                (
                    "Was macht man vor dem ersten Kurs?",
                    "Einen Einstufungstest",
                    "Eine Prüfung",
                    "Ein Vorstellungsgespräch",
                ),
                (
                    "Was übt man im Kurs „Deutsch für den Beruf“?",
                    "Telefonieren und E-Mails",
                    "Kochen",
                    "Fotografieren",
                ),
                (
                    "Wann finden die Kurse statt?",
                    "Abends oder samstags",
                    "Nur vormittags",
                    "Nur sonntags",
                ),
                (
                    "Wer kann eine Ermäßigung bekommen?",
                    "Menschen mit wenig Geld",
                    "Alle Studenten",
                    "Nur Senioren",
                ),
                ("Was bekommt man nach der Prüfung?", "Ein Zertifikat", "Einen Job", "Geld zurück"),
            ],
        ),
        (
            [
                ("Frau", "Wie war dein Vorstellungsgespräch?"),
                (
                    "Mann",
                    "Gut, glaube ich. Am Anfang war ich sehr nervös, aber die Personalleiterin war nett.",
                ),
                ("Frau", "Was hat sie dich gefragt?"),
                (
                    "Mann",
                    "Warum ich bei ihnen arbeiten möchte. Und welche Sprachen ich spreche. Ich habe gesagt: sowohl Englisch als auch Spanisch.",
                ),
                ("Frau", "Und gab es keine schwierige Frage?"),
                (
                    "Mann",
                    "Doch. Ich habe eine Frage falsch verstanden und über meine Hobbys erzählt statt über meine Stärken. Das war mir peinlich.",
                ),
                ("Frau", "Ach, das passiert. Wann sagen sie dir Bescheid?"),
                ("Mann", "Bis Ende der Woche. Ich hoffe auf eine Zusage!"),
            ],
            [
                ("Der Mann war am Anfang ruhig.", False),
                ("Die Personalleiterin war freundlich.", True),
                ("Er spricht Englisch und Spanisch.", True),
                ("Es gab keine schwierigen Fragen.", False),
                ("Er hat über seine Hobbys gesprochen.", True),
                ("Er hat schon eine Antwort bekommen.", False),
                ("Er bekommt bis Ende der Woche eine Antwort.", True),
            ],
        ),
        (
            _guests("Frau Gómez", "Herr Fischer"),
            [
                (
                    "Ansage",
                    "Heute geht es um Missverständnisse beim Deutschlernen. Bei uns sind die Spanierin Frau Gómez und der Deutschlehrer Herr Fischer.",
                ),
                (
                    "Frau",
                    "Als ich neu in Deutschland war, habe ich im Supermarkt nach Birnen gefragt, weil ich Glühbirnen brauchte. Ich bekam Obst!",
                ),
                (
                    "Mann",
                    "Solche Wörter nennen wir Teekesselchen. Im Unterricht spielen wir oft Spiele damit.",
                ),
                ("Ansage", "Was raten Sie Lernenden in solchen Situationen?"),
                (
                    "Mann",
                    "Fragen Sie einfach nach. Kein Deutscher ist böse, wenn Sie sagen: Könnten Sie das bitte erklären?",
                ),
                ("Frau", "Am Anfang war mir das peinlich. Heute frage ich ohne Probleme nach."),
                ("Ansage", "Und welche Fehler machen Lernende am häufigsten?"),
                (
                    "Mann",
                    "Die Betonung. Wegen der falschen Betonung versteht man manche Wörter gar nicht.",
                ),
                ("Frau", "Deshalb höre ich jeden Tag deutsches Radio. Das hilft mir sehr."),
            ],
            [
                ("Heute geht es um Missverständnisse.", 0),
                ("Ich bekam im Supermarkt Obst.", 1),
                ("Im Unterricht spielen wir mit solchen Wörtern.", 2),
                ("Was raten Sie Lernenden?", 0),
                ("Niemand ist böse, wenn Sie nachfragen.", 2),
                ("Früher war mir das Nachfragen peinlich.", 1),
                ("Die Betonung ist oft falsch.", 2),
                ("Ich höre jeden Tag deutsches Radio.", 1),
            ],
        ),
    ),
    # Modul 6 (Lektionen 16-18): memories, art, politics.
    6: _set(
        6,
        [
            (
                "Ansage",
                "Das Kunstmuseum zeigt ab Sonntag Bilder der Malerin Gabi Roth. Es lohnt sich: Viele Gemälde werden zum ersten Mal ausgestellt. Der Eintritt ist am ersten Tag frei.",
                ("Alle Bilder waren schon oft in Ausstellungen.", False),
                (
                    "Was ist am ersten Tag besonders?",
                    "Der Eintritt ist frei.",
                    "Die Malerin ist da.",
                    "Das Museum ist länger offen.",
                ),
            ),
            (
                "Mann",
                "Hallo Oma, hier ist Felix. Ich mache doch das Interview für die Schule. Du brauchst nichts vorzubereiten, wir reden einfach. Passt dir Sonntag um drei?",
                ("Felix will die Oma für die Schule interviewen.", True),
                ("Was muss die Oma vorbereiten?", "Nichts", "Fotos", "Kuchen"),
            ),
            (
                "Ansage",
                "Am Sonntag ist Bundestagswahl. Die Wahllokale sind von acht bis achtzehn Uhr geöffnet. Wer nicht kommen kann, kann auch per Brief wählen.",
                ("Man kann auch per Brief wählen.", True),
                ("Bis wann sind die Wahllokale geöffnet?", "Bis 18 Uhr", "Bis 20 Uhr", "Bis 8 Uhr"),
            ),
            (
                "Frau",
                "Guten Tag, hier ist die Bürgerinitiative Grüner Park. Wir sammeln am Samstag Unterschriften gegen den Bau des Parkhauses. Wir brauchen noch ehrenamtliche Helfer. Haben Sie Zeit?",
                ("Die Bürgerinitiative ist für das Parkhaus.", False),
                ("Was sucht die Bürgerinitiative?", "Helfer", "Geld", "Ein Parkhaus"),
            ),
            (
                "Ansage",
                "Eine Umfrage zeigt: Jugendliche interessieren sich weder für Parteien noch für Wahlen, aber sehr für den Klimaschutz. Viele engagieren sich in Gruppen.",
                ("Jugendliche interessieren sich sehr für Parteien.", False),
                (
                    "Wofür interessieren sich Jugendliche laut Umfrage?",
                    "Für den Klimaschutz",
                    "Für Parteien",
                    "Für Wahlen",
                ),
            ),
        ],
        (
            "Ansage",
            [
                "Herzlich willkommen im Schlossmuseum. Ich führe Sie heute durch die Ausstellung über die Malerin Elsa Hoff.",
                "Elsa Hoff wurde achtzehnhundertneunzig in einem kleinen Dorf geboren. Als Frau durfte sie zuerst nicht an der Kunstakademie studieren.",
                "Deshalb nahm sie privaten Unterricht bei einem Maler in München.",
                "Hier sehen Sie eines ihrer bekanntesten Bilder: Hügel im Herbst. Sie hat es neunzehnhundertvierundzwanzig gemalt.",
                "Im Krieg wurden viele ihrer Werke zerstört. Die Bilder hier hat ihr Enkel vor drei Jahren auf einem Dachboden gefunden.",
                "Im nächsten Raum können Sie selbst malen. Pinsel und Farben liegen bereit.",
            ],
            [
                ("Wann wurde Elsa Hoff geboren?", "1890", "1924", "1980"),
                (
                    "Warum nahm sie privaten Unterricht?",
                    "Sie durfte nicht an der Akademie studieren.",
                    "Sie hatte kein Geld.",
                    "Sie wohnte zu weit weg.",
                ),
                (
                    "Was zeigt ihr bekanntes Bild?",
                    "Hügel im Herbst",
                    "Ein Dorf im Winter",
                    "Ihre Familie",
                ),
                ("Wer hat die Bilder gefunden?", "Ihr Enkel", "Ein Maler", "Das Museum"),
                (
                    "Was kann man im nächsten Raum machen?",
                    "Selbst malen",
                    "Bilder kaufen",
                    "Kaffee trinken",
                ),
            ],
        ),
        (
            [
                ("Frau", "Erzähl mal, wie war das früher bei euch zu Hause?"),
                ("Mann", "Meine Mutter war sehr streng. Sie hat immer auf Pünktlichkeit geachtet."),
                ("Frau", "Musstest du im Haushalt helfen?"),
                (
                    "Mann",
                    "Kaum. Ich brauchte nur mein Zimmer aufzuräumen. Meine große Schwester musste viel mehr machen.",
                ),
                ("Frau", "Das finde ich ungerecht."),
                (
                    "Mann",
                    "Ja, damals war das leider normal. Taschengeld bekam ich auch nur, wenn meine Noten gut waren.",
                ),
                ("Frau", "Und wie war dein Vater?"),
                (
                    "Mann",
                    "Viel lockerer. Er hat mir abends Geschichten vorgelesen, und wir sind oft zusammen wandern gegangen.",
                ),
            ],
            [
                ("Die Mutter des Mannes war streng.", True),
                ("Der Mann musste viel im Haushalt helfen.", False),
                ("Seine Schwester musste mehr helfen als er.", True),
                ("Die Frau findet das gerecht.", False),
                ("Taschengeld bekam er immer.", False),
                ("Der Vater hat ihm vorgelesen.", True),
                ("Mit dem Vater ging er oft wandern.", True),
            ],
        ),
        (
            _guests("Frau Maier", "Herr Kowalski"),
            [
                (
                    "Ansage",
                    "Heute diskutieren wir: Sollen schon Sechzehnjährige wählen dürfen? Bei mir sind die Politikerin Frau Maier und der Schüler Herr Kowalski.",
                ),
                (
                    "Mann",
                    "Ich bin siebzehn und finde: Wir müssen mit den Entscheidungen von heute am längsten leben. Also sollten wir mitbestimmen.",
                ),
                (
                    "Frau",
                    "Ich verstehe das. Aber viele Jugendliche interessieren sich weder für Parteien noch für Programme.",
                ),
                ("Ansage", "Ist das nicht bei vielen Erwachsenen genauso?"),
                ("Mann", "Genau das meine ich! Niemand fragt Erwachsene, ob sie genug wissen."),
                (
                    "Frau",
                    "Das ist zwar richtig, aber die Schulen müssten dann mehr über Politik unterrichten.",
                ),
                ("Ansage", "Wäre das eine Lösung?"),
                ("Frau", "Ja. Mit besserem Unterricht wäre ich dafür."),
                (
                    "Mann",
                    "Damit bin ich einverstanden. In meiner Schule gibt es fast keinen Politikunterricht.",
                ),
            ],
            [
                ("Sollen Sechzehnjährige wählen dürfen?", 0),
                ("Wir leben am längsten mit den Entscheidungen.", 2),
                ("Viele Jugendliche interessieren sich nicht für Parteien.", 1),
                ("Ist das bei Erwachsenen nicht genauso?", 0),
                ("Erwachsene fragt niemand, ob sie genug wissen.", 2),
                ("Die Schulen müssten mehr über Politik unterrichten.", 1),
                ("Mit besserem Unterricht bin ich dafür.", 1),
                ("An meiner Schule gibt es kaum Politikunterricht.", 2),
            ],
        ),
    ),
    # Modul 7 (Lektionen 19-21): tourism, mountain huts, concerts and cities.
    7: _set(
        7,
        [
            (
                "Ansage",
                "Der Wetterbericht für die Alpen: Morgen wird es am Vormittag sonnig, am Nachmittag gibt es Gewitter. Wanderer sollten deshalb früh losgehen und vor vierzehn Uhr auf einer Hütte sein.",
                ("Am Nachmittag gibt es Gewitter.", True),
                (
                    "Wann sollten Wanderer auf der Hütte sein?",
                    "Vor 14 Uhr",
                    "Vor 10 Uhr",
                    "Am Abend",
                ),
            ),
            (
                "Mann",
                "Hallo, hier ist Georg von der Berghütte Edelweiß. Ihre Reservierung für Samstag ist bestätigt: zwei Plätze im Lager. Bitte bringen Sie einen Schlafsack mit, Decken gibt es genug.",
                ("Die Reservierung ist für ein Doppelzimmer.", False),
                ("Was soll man mitbringen?", "Einen Schlafsack", "Decken", "Essen"),
            ),
            (
                "Ansage",
                "Liebe Besucher, das Konzert der Band Wonnetöne beginnt wegen technischer Probleme erst um einundzwanzig Uhr. Die Garderobe ist im Untergeschoss.",
                ("Das Konzert beginnt später.", True),
                ("Wann beginnt das Konzert?", "Um 21 Uhr", "Um 20 Uhr", "Um 22 Uhr"),
            ),
            (
                "Frau",
                "Hallo Kai, hier ist Jule. Die Karten für das Konzert waren innerhalb einer Stunde verkauft. Ich habe leider keine bekommen. Wollen wir stattdessen ins Kino gehen?",
                ("Jule hat zwei Karten gekauft.", False),
                (
                    "Was schlägt Jule vor?",
                    "Ins Kino zu gehen",
                    "Zu Hause zu bleiben",
                    "Ein anderes Konzert",
                ),
            ),
            (
                "Ansage",
                "Die Lüneburger Heide blüht! Je wärmer der August ist, desto mehr Touristen kommen. Bitte bleiben Sie auf den Wegen, damit die Natur geschützt wird.",
                ("Im warmen August kommen weniger Touristen.", False),
                (
                    "Was sollen die Besucher tun?",
                    "Auf den Wegen bleiben",
                    "Blumen pflücken",
                    "Mit dem Auto fahren",
                ),
            ),
        ],
        (
            "Mann",
            [
                "Guten Tag, ich bin Herr Jansen und zeige Ihnen heute die Lüneburger Heide.",
                "Die Heide ist keine wilde Natur. Sie entstand, weil die Menschen hier vor vielen hundert Jahren die Wälder abgeholzt haben.",
                "Damit die Heide bleibt, fressen jedes Jahr Tausende Schafe die jungen Bäume. Ohne die Schafe würde hier bald wieder Wald wachsen.",
                "Am schönsten ist die Heide im August, wenn sie lila blüht.",
                "Aus den Blüten machen die Bienen einen besonderen Honig, den Heidehonig. Sie können ihn später im Hofladen probieren.",
                "Bitte bleiben Sie auf den Wegen, und Hunde müssen an die Leine.",
            ],
            [
                (
                    "Wie ist die Heide entstanden?",
                    "Die Menschen haben die Wälder abgeholzt.",
                    "Durch einen großen Brand.",
                    "Sie war schon immer da.",
                ),
                (
                    "Was machen die Schafe?",
                    "Sie fressen junge Bäume.",
                    "Sie schützen die Bienen.",
                    "Sie geben Honig.",
                ),
                ("Wann blüht die Heide?", "Im August", "Im Mai", "Im Oktober"),
                ("Wo kann man Heidehonig probieren?", "Im Hofladen", "Im Hotel", "Am Bahnhof"),
                (
                    "Was gilt für Hunde?",
                    "Sie müssen an die Leine.",
                    "Sie dürfen nicht mit.",
                    "Sie dürfen frei laufen.",
                ),
            ],
        ),
        (
            [
                ("Frau", "Wir haben morgen die Stadtführung. Wo treffen wir uns?"),
                ("Mann", "Um neun Uhr vor dem Rathaus. Die Führung dauert bis zwölf."),
                ("Frau", "Und danach?"),
                (
                    "Mann",
                    "Danach essen wir in einer Gaststätte in der Altstadt. Ich habe schon einen Tisch reserviert.",
                ),
                (
                    "Frau",
                    "Super. Gehen wir am Nachmittag ins Stadion? Das liegt doch außerhalb der Stadt.",
                ),
                ("Mann", "Ja, wir fahren mit der Straßenbahn hin, das dauert zwanzig Minuten."),
                ("Frau", "Und am Abend ist das Konzert. Hast du die Karten?"),
                ("Mann", "Ja, die habe ich schon vor zwei Monaten online gekauft."),
            ],
            [
                ("Sie treffen sich vor dem Rathaus.", True),
                ("Die Führung dauert bis vierzehn Uhr.", False),
                ("Der Mann hat einen Tisch reserviert.", True),
                ("Das Stadion liegt im Zentrum.", False),
                ("Zum Stadion fahren sie mit der Straßenbahn.", True),
                ("Die Fahrt dauert eine Stunde.", False),
                ("Die Konzertkarten hat der Mann schon gekauft.", True),
            ],
        ),
        (
            _guests("Frau Albrecht", "Herr Gruber"),
            [
                (
                    "Ansage",
                    "Heute fragen wir: Wie viele Touristen verträgt eine Region? Bei mir sind die Naturschützerin Frau Albrecht und der Hüttenwirt Herr Gruber.",
                ),
                (
                    "Mann",
                    "Auf meiner Hütte kommen jedes Jahr mehr Gäste. Für mich als Wirt ist das natürlich gut.",
                ),
                (
                    "Frau",
                    "Aber je mehr Menschen kommen, desto mehr leidet die Natur. Viele verlassen die Wege.",
                ),
                ("Ansage", "Sollte man die Zahl der Besucher begrenzen?"),
                (
                    "Frau",
                    "Ja. In manchen Nationalparks muss man schon heute vorher eine Karte reservieren.",
                ),
                (
                    "Mann",
                    "Das halte ich für übertrieben. Besser ist es, die Gäste gut zu informieren, indem man die Regeln erklärt.",
                ),
                ("Ansage", "Was erklären Sie Ihren Gästen?"),
                ("Mann", "Dass jeder seinen Müll wieder mit ins Tal nimmt."),
                ("Frau", "Das ist ein guter Anfang, aber es reicht nicht."),
            ],
            [
                ("Wie viele Touristen verträgt eine Region?", 0),
                ("Für mich sind mehr Gäste gut.", 2),
                ("Viele Besucher verlassen die Wege.", 1),
                ("Sollte man die Besucher begrenzen?", 0),
                ("In manchen Parks muss man vorher reservieren.", 1),
                ("Eine Grenze finde ich übertrieben.", 2),
                ("Jeder nimmt seinen Müll mit ins Tal.", 2),
                ("Das reicht nicht.", 1),
            ],
        ),
    ),
    # Modul 8 (Lektionen 22-24): history, environment, living together.
    8: _set(
        8,
        [
            (
                "Ansage",
                "Heute vor fünfunddreißig Jahren wurde die Berliner Mauer geöffnet. Am Abend gibt es am Brandenburger Tor ein großes Fest mit Musik und Reden.",
                ("Das Fest ist am Brandenburger Tor.", True),
                (
                    "Was ist heute vor 35 Jahren passiert?",
                    "Die Mauer wurde geöffnet.",
                    "Die Mauer wurde gebaut.",
                    "Die BRD wurde gegründet.",
                ),
            ),
            (
                "Frau",
                "Hallo Tim, hier ist Anke. Ich fahre ab jetzt mit dem Rad zur Arbeit, statt das Auto zu nehmen. Willst du nicht mitkommen? Wir könnten uns um halb acht an der Kreuzung treffen.",
                ("Anke fährt jetzt mit dem Auto zur Arbeit.", False),
                ("Wo will Anke Tim treffen?", "An der Kreuzung", "Am Bahnhof", "Vor dem Büro"),
            ),
            (
                "Ansage",
                "Die Stadt informiert: Ab Juli ist die Innenstadt für Autos gesperrt. Damit die Luft sauberer wird, gibt es neue Radwege und mehr Busse.",
                ("Es wird mehr Busse geben.", True),
                (
                    "Warum wird die Innenstadt gesperrt?",
                    "Damit die Luft sauberer wird",
                    "Wegen Bauarbeiten",
                    "Wegen eines Festes",
                ),
            ),
            (
                "Mann",
                "Guten Tag, Frau Demir, hier ist Herr Kühn vom Mehrgenerationenhaus. Ab September ist eine Wohnung mit drei Zimmern frei. Wenn Sie Interesse haben, rufen Sie mich bitte bis Freitag zurück.",
                ("Die Wohnung hat zwei Zimmer.", False),
                (
                    "Bis wann soll Frau Demir zurückrufen?",
                    "Bis Freitag",
                    "Bis September",
                    "Bis morgen",
                ),
            ),
            (
                "Ansage",
                "Das Repair-Café im Gemeindehaus ist jeden Samstag geöffnet. Bringen Sie kaputte Geräte mit, statt sie wegzuwerfen. Die Reparatur ist kostenlos.",
                ("Das Repair-Café ist nur am Sonntag geöffnet.", False),
                ("Was kostet die Reparatur?", "Nichts", "Fünf Euro", "Es hängt vom Gerät ab."),
            ),
        ],
        (
            "Frau",
            [
                "Willkommen bei unserer Führung „Geteiltes Berlin“. Wir stehen hier an der Bernauer Straße.",
                "Am dreizehnten August neunzehnhunderteinundsechzig begann die DDR, eine Mauer durch Berlin zu bauen. Über Nacht waren Familien getrennt.",
                "Die Häuser auf dieser Straßenseite gehörten zum Osten, der Bürgersteig davor aber schon zum Westen. Manche Menschen sprangen deshalb aus den Fenstern in den Westen.",
                "Später wurden die Häuser abgerissen, und die Grenze wurde immer stärker gesichert.",
                "Am neunten November neunzehnhundertneunundachtzig wurde die Mauer geöffnet. Hier an der Bernauer Straße steht heute eine Gedenkstätte.",
                "Wenn Sie möchten, können Sie im Besucherzentrum Filme von damals sehen.",
            ],
            [
                (
                    "Wann begann der Bau der Mauer?",
                    "Im August 1961",
                    "Im November 1989",
                    "Im Mai 1949",
                ),
                (
                    "Was war das Besondere an den Häusern?",
                    "Der Bürgersteig gehörte schon zum Westen.",
                    "Sie waren sehr modern.",
                    "Dort wohnten Soldaten.",
                ),
                (
                    "Was passierte später mit den Häusern?",
                    "Sie wurden abgerissen.",
                    "Sie wurden Museen.",
                    "Sie wurden renoviert.",
                ),
                (
                    "Was steht heute an der Bernauer Straße?",
                    "Eine Gedenkstätte",
                    "Ein Einkaufszentrum",
                    "Ein Bahnhof",
                ),
                (
                    "Was kann man im Besucherzentrum machen?",
                    "Filme von damals sehen",
                    "Essen gehen",
                    "Fahrräder mieten",
                ),
            ],
        ),
        (
            [
                ("Frau", "Wie gefällt euch das Leben im Mehrgenerationenhaus?"),
                ("Mann", "Sehr gut. Es ist, als ob wir eine große Familie wären."),
                ("Frau", "Hilft man sich wirklich gegenseitig?"),
                (
                    "Mann",
                    "Ja. Frau Berg von nebenan passt zweimal pro Woche auf unsere Kinder auf, damit wir arbeiten können.",
                ),
                ("Frau", "Und was macht ihr für sie?"),
                ("Mann", "Wir kaufen für sie ein und fahren sie zum Arzt, weil sie kein Auto hat."),
                ("Frau", "Gibt es keinen Streit?"),
                (
                    "Mann",
                    "Am Anfang schon, zum Beispiel über die Hausarbeit. Aber allmählich haben wir Kompromisse gefunden.",
                ),
            ],
            [
                ("Der Mann ist mit dem Mehrgenerationenhaus zufrieden.", True),
                ("Frau Berg wohnt in einer anderen Stadt.", False),
                ("Frau Berg passt auf die Kinder auf.", True),
                ("Sie passt jeden Tag auf die Kinder auf.", False),
                ("Die Familie kauft für Frau Berg ein.", True),
                ("Frau Berg hat ein eigenes Auto.", False),
                ("Am Anfang gab es Streit.", True),
            ],
        ),
        (
            _guests("Frau Hartwig", "Herr Demir"),
            [
                (
                    "Ansage",
                    "Unser Thema heute: Brauchen wir Autos in der Stadt? Zu Gast sind die Radfahrerin Frau Hartwig und der Taxifahrer Herr Demir.",
                ),
                (
                    "Frau",
                    "Ich fahre seit zehn Jahren ohne Auto. Statt im Stau zu stehen, bin ich mit dem Rad schneller.",
                ),
                (
                    "Mann",
                    "Für Sie ist das leicht. Aber meine Fahrgäste sind oft alt oder krank. Die können nicht Rad fahren.",
                ),
                ("Ansage", "Was halten Sie von einer autofreien Innenstadt?"),
                (
                    "Frau",
                    "Ich bin dafür. Die Luft wäre sauberer, und Kinder könnten sicher spielen.",
                ),
                (
                    "Mann",
                    "Dann müsste es aber Ausnahmen geben, zum Beispiel für Taxis und Krankenwagen.",
                ),
                ("Ansage", "Wäre das ein Kompromiss für Sie beide?"),
                ("Mann", "Ja, damit könnte ich leben."),
                ("Frau", "Ich auch, solange es genug Radwege gibt."),
            ],
            [
                ("Brauchen wir Autos in der Stadt?", 0),
                ("Mit dem Rad bin ich schneller.", 1),
                ("Viele Fahrgäste können nicht Rad fahren.", 2),
                ("Was halten Sie von einer autofreien Innenstadt?", 0),
                ("Kinder könnten sicher spielen.", 1),
                ("Es braucht Ausnahmen für Taxis.", 2),
                ("Damit könnte ich leben.", 2),
                ("Es muss genug Radwege geben.", 1),
            ],
        ),
    ),
}
