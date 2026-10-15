"""A2 check content: what the review of each Lektion and each Modul test asks
beyond the generated word batches (see apps.curriculum.checks and
content/a1/checks.py for the format).

A2 is stage 4 of the ramp throughout: gaps and translations are typed (gaps
carry a hint), and every extra format is used. Translations list the common
word-order variants, since typing is graded exactly. All sentences are original.
"""

from ..dsl import lektion_check, modul_check

LEVEL = "A2"


def _l(n, gaps, translations):
    return n, lektion_check(LEVEL, n, gaps, translations)


LEKTION_CHECKS = dict(
    [
        _l(
            1,
            [
                ("Als Kind [hatte] ich einen Hund.", "haben"),
                ("Mein Opa [war] Bäcker.", "sein"),
                ("Ich wohne bei [meiner] Tante.", "mein"),
                ("Wir sind auf dem Land [aufgewachsen].", "aufwachsen"),
                ("[Damals] hatten wir kein Auto.", "back then"),
            ],
            [
                ("My grandpa was a baker too.", "Mein Opa war auch Bäcker."),
                ("We had a big garden.", "Wir hatten einen großen Garten."),
                ("I often talk to my cousin (male).", "Ich spreche oft mit meinem Cousin."),
                ("As a child I collected stamps.", "Als Kind habe ich Briefmarken gesammelt."),
            ],
        ),
        _l(
            2,
            [
                ("Das Bild hängt an [der] Wand.", "die Wand"),
                ("Stell die Lampe auf [den] Tisch!", "der Tisch"),
                ("Das Buch [liegt] auf dem Regal.", "liegen"),
                ("Ich [hänge] den Spiegel an die Tür.", "hängen"),
                ("Wir gehen [ins] Wohnzimmer.", "in das"),
            ],
            [
                ("The mirror is hanging on the wall.", "Der Spiegel hängt an der Wand."),
                (
                    "Put the chest of drawers next to the bed! (du)",
                    "Stell die Kommode neben das Bett!",
                    "Stelle die Kommode neben das Bett!",
                ),
                ("The cushion is lying on the sofa.", "Das Kissen liegt auf dem Sofa."),
                ("We need more space.", "Wir brauchen mehr Platz."),
            ],
        ),
        _l(
            3,
            [
                ("Der [ruhige] See ist sehr schön.", "ruhig"),
                ("Wir fahren im Sommer [ans] Meer.", "an das"),
                ("Im Urlaub waren wir in den [Bergen].", "mountains"),
                ("Ich [empfehle] Ihnen die Pension.", "empfehlen"),
                ("Hier finden Sie Ruhe und [Erholung].", "relaxation"),
            ],
            [
                ("The village is very quiet.", "Das Dorf ist sehr ruhig."),
                ("We are going to the mountains.", "Wir fahren in die Berge."),
                (
                    "The small guesthouse is by the lake.",
                    "Die kleine Pension ist am See.",
                    "Die kleine Pension liegt am See.",
                ),
                ("What can you recommend?", "Was können Sie empfehlen?"),
            ],
        ),
        _l(
            4,
            [
                ("Ich [hätte] gern 300 Gramm Käse.", "haben"),
                ("Eine [Flasche] Wasser, bitte.", "bottle"),
                ("Wir brauchen noch ein [paar] Eier.", "a few"),
                ("Darf es sonst noch [etwas] sein?", "something"),
                ("Die Bananen sind noch nicht [reif].", "ripe"),
            ],
            [
                ("I'd like a kilo of pears.", "Ich hätte gern ein Kilo Birnen."),
                ("That's all, thank you.", "Das ist alles, danke."),
                ("We need two bottles of juice.", "Wir brauchen zwei Flaschen Saft."),
                ("The lemon is sour.", "Die Zitrone ist sauer."),
            ],
        ),
        _l(
            5,
            [
                ("Schaut mal, der [schöne] Dom!", "schön"),
                ("Gehen Sie [durch] den Park.", "through"),
                ("Das Café ist gegenüber [vom] Rathaus.", "von dem"),
                ("Wir [besichtigen] heute die Burg.", "besichtigen"),
                ("Welche [alte] Kirche meinst du?", "alt"),
            ],
            [
                ("How do I get to the cathedral?", "Wie komme ich zum Dom?"),
                (
                    "Go straight on as far as the traffic light.",
                    "Gehen Sie geradeaus bis zur Ampel.",
                ),
                ("The castle is worth seeing.", "Die Burg ist sehenswert."),
                (
                    "The museum is closed today.",
                    "Das Museum ist heute geschlossen.",
                    "Heute ist das Museum geschlossen.",
                ),
            ],
        ),
        _l(
            6,
            [
                ("Das war ein [spannender] Film.", "spannend"),
                ("Hast du Lust, ins Konzert [zu] gehen?", "to"),
                ("Ich habe eine [klassische] Oper gesehen.", "klassisch"),
                ("Hast du Zeit [mitzukommen]?", "mitkommen"),
                ("Das Publikum hat laut [geklatscht].", "klatschen"),
            ],
            [
                ("That sounds interesting.", "Das klingt interessant."),
                ("Thanks for the invitation.", "Danke für die Einladung."),
                (
                    "It was an entertaining musical.",
                    "Es war ein unterhaltsames Musical.",
                    "Das war ein unterhaltsames Musical.",
                ),
                ("Do you feel like going to the theatre?", "Hast du Lust, ins Theater zu gehen?"),
            ],
        ),
        _l(
            7,
            [
                ("Wir [könnten] montags joggen gehen.", "could"),
                ("Du [solltest] dich mehr bewegen.", "should"),
                ("[Abends] mache ich Yoga.", "in the evenings"),
                ("Wir trainieren [zweimal] pro Woche.", "twice"),
                ("Unsere Mannschaft hat leider [verloren].", "verlieren"),
            ],
            [
                ("We could go swimming.", "Wir könnten schwimmen gehen."),
                ("You should sleep more. (du)", "Du solltest mehr schlafen."),
                (
                    "On Mondays I go to the gym.",
                    "Montags gehe ich ins Fitnessstudio.",
                    "Ich gehe montags ins Fitnessstudio.",
                ),
                ("What do you think of that?", "Was hältst du davon?"),
            ],
        ),
        _l(
            8,
            [
                ("Ich hoffe, dass es nichts Ernstes [ist].", "sein"),
                ("[Mir] ist schwindelig.", "ich"),
                ("Der Arzt hat mich [untersucht].", "untersuchen"),
                ("Ich bin [erkältet] und habe Fieber.", "have a cold"),
                ("Du solltest dich [ausruhen].", "rest"),
            ],
            [
                ("Hopefully it isn't the heart!", "Hoffentlich ist es nicht das Herz!"),
                ("I feel sick.", "Mir ist übel.", "Mir ist schlecht."),
                (
                    "I hope that you get better soon. (du)",
                    "Ich hoffe, dass es dir bald besser geht.",
                ),
                ("I have backache.", "Ich habe Rückenschmerzen."),
            ],
        ),
        _l(
            9,
            [
                ("Bei [guten] Autos sind wir ganz vorn.", "gut"),
                ("Das ist das [beste] Modell.", "gut"),
                ("Ich bin [für] den Export zuständig.", "for"),
                ("Unsere Firma stellt Autos [her].", "herstellen"),
                ("Wir bieten [schnellen] Service.", "schnell"),
            ],
            [
                ("We value quality.", "Wir legen Wert auf Qualität."),
                ("The company is very successful.", "Die Firma ist sehr erfolgreich."),
                ("We deliver worldwide.", "Wir liefern weltweit."),
                (
                    "She is the most successful employee.",
                    "Sie ist die erfolgreichste Mitarbeiterin.",
                ),
            ],
        ),
        _l(
            10,
            [
                ("Gut, dass du reserviert [hast].", "haben"),
                ("Ich nehme die Suppe, [weil] ich wenig Hunger habe.", "because"),
                ("Schade, dass das Restaurant geschlossen [ist].", "sein"),
                ("Die Soße ist zu [salzig].", "salty"),
                ("Ich bin [satt], danke.", "full"),
            ],
            [
                ("Good that you booked.", "Gut, dass du reserviert hast."),
                ("The bill, please!", "Zahlen, bitte!", "Die Rechnung, bitte!"),
                (
                    "We'd like to pay separately.",
                    "Wir möchten getrennt zahlen.",
                    "Wir möchten getrennt bezahlen.",
                ),
                (
                    "I'm ordering water because I have to drive.",
                    "Ich bestelle Wasser, weil ich fahren muss.",
                    "Ich bestelle Wasser, weil ich Auto fahren muss.",
                ),
            ],
        ),
        _l(
            11,
            [
                ("Wir freuen [uns] auf die Hochzeit.", "wir"),
                ("Ich freue mich [über] deine Nachricht.", "about"),
                ("Weißt du, [ob] Anna auch kommt?", "whether"),
                ("Meine Eltern sind stolz [auf] mich.", "of"),
                ("Er hat sich in Maria [verliebt].", "sich verlieben"),
            ],
            [
                ("I'm happy for you.", "Ich freue mich für dich."),
                ("I'm looking forward to the holiday.", "Ich freue mich auf den Urlaub."),
                ("I don't know if she is engaged.", "Ich weiß nicht, ob sie verlobt ist."),
                (
                    "We are meeting on Sunday.",
                    "Wir treffen uns am Sonntag.",
                    "Am Sonntag treffen wir uns.",
                ),
            ],
        ),
        _l(
            12,
            [
                ("Wenn es warm [ist], essen wir Salat.", "sein"),
                ("Wenn ich Zeit habe, [koche] ich selbst.", "kochen"),
                ("Zuerst [schälst] du die Kartoffeln.", "schälen"),
                ("Ich esse [selten] Fleisch.", "rarely"),
                ("Zum [Schluss] würzt du alles.", "finally"),
            ],
            [
                (
                    "When it's warm, we mostly eat salad.",
                    "Wenn es warm ist, essen wir meist Salat.",
                    "Wenn es warm ist, essen wir meistens Salat.",
                ),
                ("Cut the onions. (Sie)", "Schneiden Sie die Zwiebeln."),
                ("I rarely eat pasta.", "Ich esse selten Nudeln."),
                ("When I'm hungry, I eat an apple.", "Wenn ich Hunger habe, esse ich einen Apfel."),
            ],
        ),
        _l(
            13,
            [
                ("[Als] ich zehn war, habe ich Englisch gelernt.", "when (once, past)"),
                ("Meine erste Lehrerin war sehr [geduldig].", "patient"),
                ("Kannst du das bitte [wiederholen]?", "repeat"),
                ("Die Lehrerin hat meine Fehler [korrigiert].", "korrigieren"),
                ("Das ist leider [unmöglich].", "impossible"),
            ],
            [
                ("That helped me.", "Das hat mir geholfen."),
                ("The pronunciation is difficult.", "Die Aussprache ist schwierig."),
                (
                    "When I was young, I learned French.",
                    "Als ich jung war, habe ich Französisch gelernt.",
                ),
                ("I found the course very helpful.", "Ich fand den Kurs sehr hilfreich."),
            ],
        ),
        _l(
            14,
            [
                ("Das Paket [wird] morgen geliefert.", "werden"),
                ("Die Briefe werden [sortiert].", "sortieren"),
                ("Die Pakete werden heute [verschickt].", "verschicken"),
                ("Bitte [unterschreiben] Sie hier.", "sign"),
                ("[Lieber] Tim, vielen Dank für das Päckchen!", "dear"),
            ],
            [
                (
                    "The parcel is being delivered today.",
                    "Das Paket wird heute geliefert.",
                    "Heute wird das Paket geliefert.",
                ),
                ("The letters are being sorted.", "Die Briefe werden sortiert."),
                ("That's really kind of you.", "Das ist wirklich lieb von dir."),
                ("It's nice that you thought of me.", "Schön, dass du an mich gedacht hast."),
            ],
        ),
        _l(
            15,
            [
                ("Ich schalte den Fernseher [ein].", "on"),
                ("Hast du die Sendung [verpasst]?", "verpassen"),
                ("Ich nehme den Krimi [auf].", "record"),
                ("[Jeden] Abend sehe ich die Nachrichten.", "every"),
                ("Ich benutze das Internet [mehrmals] am Tag.", "several times"),
            ],
            [
                ("It's about to start!", "Gleich geht's los!", "Gleich geht es los!"),
                ("I watch TV twice a week.", "Ich sehe zweimal pro Woche fern."),
                (
                    "Switch off the radio, please! (du)",
                    "Schalt bitte das Radio aus!",
                    "Schalte bitte das Radio aus!",
                ),
                ("The documentary was very informative.", "Die Dokumentation war sehr informativ."),
            ],
        ),
        _l(
            16,
            [
                ("Können Sie mir sagen, wo die Rezeption [ist]?", "sein"),
                ("Darf ich fragen, [ob] das Frühstück inklusive ist?", "whether"),
                ("[Könnten] Sie mir bitte helfen?", "could"),
                ("Das Hotel ist leider [ausgebucht].", "fully booked"),
                ("Ich möchte wissen, wie viel das Zimmer [kostet].", "kosten"),
            ],
            [
                ("Do you still have a room free?", "Haben Sie noch ein Zimmer frei?"),
                ("Is breakfast included?", "Ist das Frühstück inklusive?"),
                (
                    "Could you tell me where the sauna is?",
                    "Könnten Sie mir sagen, wo die Sauna ist?",
                    "Können Sie mir sagen, wo die Sauna ist?",
                ),
                (
                    "I'd like a single room.",
                    "Ich hätte gern ein Einzelzimmer.",
                    "Ich möchte ein Einzelzimmer.",
                ),
            ],
        ),
        _l(
            17,
            [
                ("Wir kommen gerade [aus] dem Urlaub.", "from"),
                ("Er kommt [vom] Strand zurück.", "von dem"),
                ("Ich [wäre] jetzt gern am Meer.", "would be"),
                ("Wir müssen noch [tanken].", "fill up"),
                ("Wir hatten eine [Reifenpanne].", "flat tyre"),
            ],
            [
                (
                    "We want to go to Romania.",
                    "Wir wollen nach Rumänien.",
                    "Wir wollen nach Rumänien fahren.",
                ),
                ("How long does the journey take?", "Wie lange dauert die Fahrt?"),
                (
                    "I would like to travel by ferry.",
                    "Ich würde gern mit der Fähre fahren.",
                    "Ich würde gern mit der Fähre reisen.",
                ),
                ("We are coming back from the sea.", "Wir kommen vom Meer zurück."),
            ],
        ),
        _l(
            18,
            [
                ("Ich freue mich [auf] Sonne und Wärme.", "auf / über"),
                ("Ich ärgere mich [über] den Regen.", "about"),
                ("[Worauf] freust du dich?", "wo + auf"),
                ("Ja, [darauf] freue ich mich.", "da + auf"),
                ("Morgen [steigen] die Temperaturen.", "steigen"),
            ],
            [
                ("What are you looking forward to?", "Worauf freust du dich?"),
                ("I'm annoyed about the cold.", "Ich ärgere mich über die Kälte."),
                ("We are dreaming of a holiday.", "Wir träumen von einem Urlaub."),
                ("Are you satisfied with the hotel?", "Bist du mit dem Hotel zufrieden?"),
            ],
        ),
        _l(
            19,
            [
                ("Wie wäre es [mit] einem Konzert?", "with"),
                ("Ich schlage vor, dass wir ins Kino [gehen].", "gehen"),
                ("Das Konzert ist [ausverkauft].", "sold out"),
                ("Das Festival findet im Park [statt].", "stattfinden"),
                ("Du hast mich [überzeugt].", "überzeugen"),
            ],
            [
                ("Count me in.", "Da bin ich dabei."),
                ("What's on today?", "Was läuft heute?"),
                ("Come along!", "Komm doch mit!", "Komm mit!"),
                ("How about a reading?", "Wie wäre es mit einer Lesung?"),
            ],
        ),
        _l(
            20,
            [
                ("Als Kind [durfte] ich keine Comics lesen.", "dürfen"),
                ("Wir [mussten] früh ins Bett gehen.", "müssen"),
                ("Mein Bruder [konnte] schon mit vier lesen.", "können"),
                ("Ich [mochte] keine Gedichte.", "mögen"),
                ("Mein Vater hat mir oft [vorgelesen].", "vorlesen"),
            ],
            [
                ("I wasn't allowed to watch TV.", "Ich durfte nicht fernsehen."),
                ("We wanted to stay up longer.", "Wir wollten länger aufbleiben."),
                ("That's not for me.", "Das ist nichts für mich."),
                ("I had to read every day.", "Ich musste jeden Tag lesen."),
            ],
        ),
        _l(
            21,
            [
                ("[Welchen] Ausweis meinen Sie?", "which"),
                ("Ja genau, [den] meine ich.", "der Ausweis"),
                ("Ich [lasse] mein Auto reparieren.", "lassen"),
                ("Jemand hat meine Geldbörse [gestohlen].", "stehlen"),
                ("Ich habe meinen Pass [verloren].", "verlieren"),
            ],
            [
                ("I'm having my bike repaired.", "Ich lasse mein Fahrrad reparieren."),
                ("Which card do you need? (Sie)", "Welche Karte brauchen Sie?"),
                ("Can you describe the culprit?", "Können Sie den Täter beschreiben?"),
                ("I've lost my ID card.", "Ich habe meinen Ausweis verloren."),
            ],
        ),
        _l(
            22,
            [
                ("[Seit] ich kein Auto habe, fahre ich Rad.", "since"),
                ("Ich warte, [bis] der Bus kommt.", "until"),
                ("Ich wohne seit [einem] Jahr hier.", "ein"),
                ("Bitte [bestätigen] Sie die Buchung.", "confirm"),
                ("Ein Fahrrad ist [umweltfreundlich].", "environmentally friendly"),
            ],
            [
                (
                    "Since I sold my car, I cycle more.",
                    "Seit ich meinen Wagen verkauft habe, fahre ich mehr Fahrrad.",
                    "Seit ich mein Auto verkauft habe, fahre ich mehr Fahrrad.",
                ),
                ("I have been living here for two years.", "Ich wohne seit zwei Jahren hier."),
                ("We share a car.", "Wir teilen ein Auto."),
                ("How does that work?", "Wie geht das?", "Wie funktioniert das?"),
            ],
        ),
        _l(
            23,
            [
                ("Das ist der Beruf, [der] zu mir passt.", "relative pronoun"),
                ("Der Kollege, [den] ich kenne, ist nett.", "relative pronoun"),
                ("Ich suche eine Arbeit, [die] mir Spaß macht.", "relative pronoun"),
                ("Ich habe mich um die Stelle [beworben].", "sich bewerben"),
                ("Die Prüfung war [mündlich].", "oral"),
            ],
            [
                ("The job that suits me.", "Der Beruf, der zu mir passt."),
                ("I enjoy the work.", "Die Arbeit macht mir Spaß."),
                (
                    "I have a job interview tomorrow.",
                    "Ich habe morgen ein Vorstellungsgespräch.",
                    "Morgen habe ich ein Vorstellungsgespräch.",
                ),
                (
                    "This is the colleague that I met yesterday.",
                    "Das ist die Kollegin, die ich gestern getroffen habe.",
                    "Das ist der Kollege, den ich gestern getroffen habe.",
                ),
            ],
        ),
        _l(
            24,
            [
                ("Jeden Morgen [stand] ich um sechs auf.", "aufstehen"),
                ("Am Abend [traf] ich oft Freunde.", "treffen"),
                ("Wie [sah] dein Alltag aus?", "aussehen"),
                ("Am Anfang hatte ich oft [Heimweh].", "homesickness"),
                ("Ich habe mich schnell [gewöhnt].", "sich gewöhnen"),
            ],
            [
                ("What was your everyday life like?", "Wie sah dein Alltag aus?"),
                ("At first it was difficult.", "Am Anfang war es schwierig."),
                (
                    "I went to work by bus.",
                    "Ich fuhr mit dem Bus zur Arbeit.",
                    "Ich bin mit dem Bus zur Arbeit gefahren.",
                ),
                (
                    "I felt comfortable there.",
                    "Ich fühlte mich dort wohl.",
                    "Ich habe mich dort wohlgefühlt.",
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
                "A: Wohin soll die Kommode?",
                "B: ___",
                "A: Und das Regal?",
                "B: Das kommt in die Ecke.",
            ],
            "Stell sie bitte neben das Bett.",
            "Sie steht neben dem Bett geblieben.",
            "Mein Opa war Bäcker.",
        ),
        qa=[
            ("Was war dein Opa von Beruf?", "Er war Bäcker."),
            ("Wo hängt der Spiegel?", "An der Wand."),
            ("Wohin fahrt ihr im Sommer?", "Ans Meer."),
            ("Wie war das früher bei dir?", "Wir hatten einen großen Garten."),
            ("Was können Sie empfehlen?", "Die Pension am See."),
        ],
        odd=[
            ("der Spiegel", "die Tante", "der Onkel", "die Cousine"),
            ("die Kommode", "der Vogel", "die Katze", "das Tier"),
            ("zeichnen", "stellen", "legen", "hängen"),
            ("kompliziert", "das Dorf", "der See", "das Ufer"),
        ],
        reading=(
            """
Lisa ist auf einem Bauernhof aufgewachsen. Ihre Großeltern hatten viele Tiere,
und Lisa war jeden Tag draußen. Heute wohnt sie in Berlin, in einer kleinen
Wohnung im dritten Stock. Im Urlaub fährt sie aber immer aufs Land, weil sie
dort Ruhe und Erholung findet.
""",
            [
                ("Lisa ist in der Stadt aufgewachsen.", False),
                ("Ihre Großeltern hatten viele Tiere.", True),
                ("Lisa wohnt heute in einem großen Haus.", False),
                ("Im Urlaub fährt Lisa gern aufs Land.", True),
            ],
        ),
        form=[
            ("Als Kind ___ ich einen Hund. (haben, Präteritum)", "hatte"),
            ("Ich wohne bei ___ Onkel. (mein)", "meinem"),
            ("Das Bild hängt an ___ Wand. (die)", "der"),
            ("Ich lege das Buch auf ___ Tisch. (der)", "den"),
            ("Die ___ Pension ist am See. (klein)", "kleine"),
        ],
        mistake=[
            ("Mein Opa *waren* Bäcker.", "Mein Opa war Bäcker."),
            ("Ich wohne bei *meine* Tante.", "Ich wohne bei meiner Tante."),
            ("Das Bild hängt an *die* Wand.", "Das Bild hängt an der Wand."),
            ("Wir fahren im Sommer *am* Meer.", "Wir fahren im Sommer ans Meer."),
        ],
        dictation=[
            "Mein Opa war auch schon Bäcker.",
            "Stell die Lampe bitte auf den Tisch.",
            "Wir fahren im Sommer ans Meer.",
            "Hier finden Sie Ruhe und Erholung.",
        ],
    ),
    2: modul_check(
        LEVEL,
        6,
        dialogue=(
            [
                "A: Guten Tag, was darf es sein?",
                "B: Ich hätte gern ein Kilo Birnen.",
                "A: ___",
                "B: Nein, danke. Das ist alles.",
            ],
            "Darf es sonst noch etwas sein?",
            "Das macht zusammen drei Kilo.",
            "Gehen Sie geradeaus.",
        ),
        qa=[
            ("Was darf es sein?", "Ein Stück Kuchen, bitte."),
            ("Wie komme ich zum Dom?", "Gehen Sie durch den Park."),
            ("Hast du Lust mitzukommen?", "Gern, das klingt gut."),
            ("Was macht das zusammen?", "Sieben Euro zwanzig."),
            ("Welche Musik hörst du gern?", "Am liebsten klassische Musik."),
        ],
        odd=[
            ("die Oper", "die Birne", "die Banane", "die Traube"),
            ("die Flasche", "die Burg", "das Denkmal", "der Marktplatz"),
            ("süß", "das Musical", "das Festival", "das Ballett"),
            ("besichtigen", "das Gramm", "das Kilo", "der Liter"),
        ],
        reading=(
            """
Am Samstag war Paul in Köln. Zuerst hat er den berühmten Dom besichtigt. Dann
ist er über die Brücke gegangen und hat auf dem Markt frische Trauben und ein
Stück Käse gekauft. Am Abend war er in einem tollen Konzert. Die Eintrittskarte
war teuer, aber das Konzert war super.
""",
            [
                ("Paul hat zuerst den Dom besichtigt.", True),
                ("Er hat auf dem Markt Bananen gekauft.", False),
                ("Am Abend war Paul im Theater.", False),
                ("Paul fand das Konzert super.", True),
            ],
        ),
        form=[
            ("Ich ___ gern 200 Gramm Käse. (haben, Konjunktiv)", "hätte"),
            ("zwei ___ Wasser (die Flasche)", "Flaschen"),
            ("Schaut mal, die ___ Burg! (alt)", "alte"),
            ("Das ist ein ___ Film. (spannend)", "spannender"),
            ("Hast du Lust, ___? (mitkommen)", "mitzukommen"),
        ],
        mistake=[
            ("Ich hätte gern ein Kilo *von* Äpfel.", "Ich hätte gern ein Kilo Äpfel."),
            ("Schaut mal, der *schönen* Dom!", "Schaut mal, der schöne Dom!"),
            ("Das ist ein *spannende* Film.", "Das ist ein spannender Film."),
            ("Hast du Lust, ins Kino *gehen*?", "Hast du Lust, ins Kino zu gehen?"),
        ],
        dictation=[
            "Ich hätte gern ein Kilo Birnen.",
            "Gehen Sie geradeaus bis zur Ampel.",
            "Das war ein spannender Film.",
            "Danke für die Einladung.",
        ],
    ),
    3: modul_check(
        LEVEL,
        9,
        dialogue=(
            [
                "A: Ich bin immer so müde.",
                "B: ___",
                "A: Gute Idee! Wann denn?",
                "B: Montags und donnerstags.",
            ],
            "Wir könnten zusammen joggen gehen.",
            "Hoffentlich ist es nicht das Herz!",
            "Wir legen Wert auf Qualität.",
        ),
        qa=[
            ("Was fehlt Ihnen?", "Ich habe Rückenschmerzen."),
            ("Was soll ich tun?", "Du solltest dich ausruhen."),
            ("Wofür sind Sie zuständig?", "Für den Export."),
            ("Wie oft trainierst du?", "Dreimal pro Woche."),
            ("Was stellt Ihre Firma her?", "Hochwertige Autos."),
        ],
        odd=[
            ("die Fabrik", "der Magen", "das Herz", "die Haut"),
            ("husten", "joggen", "trainieren", "Ski fahren"),
            ("zuverlässig", "die Mannschaft", "der Verein", "der Trainer"),
            ("die Spritze", "die Abteilung", "der Kunde", "das Produkt"),
        ],
        reading=(
            """
Frau Yilmaz arbeitet in der Exportabteilung einer großen Firma. Sie sitzt jeden
Tag acht Stunden am Computer, und seit ein paar Wochen hat sie Rückenschmerzen.
Ihr Arzt sagt, dass sie sich mehr bewegen sollte. Jetzt geht sie montags und
mittwochs ins Fitnessstudio. Es geht ihr schon viel besser.
""",
            [
                ("Frau Yilmaz arbeitet im Export.", True),
                ("Sie hat Bauchschmerzen.", False),
                ("Der Arzt sagt, dass sie mehr Sport machen sollte.", True),
                ("Sie geht jeden Tag ins Fitnessstudio.", False),
            ],
        ),
        form=[
            ("Wir ___ montags schwimmen gehen. (können, Konjunktiv)", "könnten"),
            ("Du ___ mehr trinken. (sollen, Konjunktiv)", "solltest"),
            ("Ich hoffe, dass es dir besser ___. (gehen)", "geht"),
            ("Bei ___ Wetter fahren wir nicht. (schlecht)", "schlechtem"),
            ("Das ist das ___ Auto. (gut, Superlativ)", "beste"),
        ],
        mistake=[
            ("Ich *haben* Rückenschmerzen.", "Ich habe Rückenschmerzen."),
            ("Ich hoffe, dass es *ist* nichts Ernstes.", "Ich hoffe, dass es nichts Ernstes ist."),
            ("*Ich* ist schwindelig.", "Mir ist schwindelig."),
            ("Bei *gute* Autos sind wir ganz vorn.", "Bei guten Autos sind wir ganz vorn."),
        ],
        dictation=[
            "Wir könnten montags joggen gehen.",
            "Du solltest dich mehr bewegen.",
            "Hoffentlich ist es nicht das Herz.",
            "Wir legen großen Wert auf Qualität.",
        ],
    ),
    4: modul_check(
        LEVEL,
        12,
        dialogue=(
            [
                "A: Ich habe einen Tisch für vier Personen reserviert.",
                "B: ___",
                "A: Super, danke!",
                "B: Möchten Sie schon etwas trinken?",
            ],
            "Gut, dass Sie reserviert haben. Wir sind heute voll.",
            "Ich freue mich so für dich!",
            "Zuerst schälen Sie die Kartoffeln.",
        ),
        qa=[
            ("Warum nimmst du die Suppe?", "Weil ich wenig Hunger habe."),
            ("Weißt du, ob Anna kommt?", "Nein, das weiß ich nicht."),
            ("Worauf freust du dich?", "Auf die Hochzeit."),
            ("Was isst du, wenn es warm ist?", "Meistens Salat."),
            ("Zahlen Sie zusammen oder getrennt?", "Getrennt, bitte."),
        ],
        odd=[
            ("die Hochzeit", "die Gabel", "der Löffel", "der Teller"),
            ("nervös", "schälen", "schneiden", "rühren"),
            ("die Pfanne", "die Geburt", "die Verlobung", "die Trennung"),
            ("salzig", "die Nachspeise", "die Hauptspeise", "die Beilage"),
        ],
        reading=(
            """
Liebe Clara, ich habe eine tolle Nachricht: Jonas und ich haben uns verlobt!
Wir feiern im Juni in einem kleinen Restaurant am See. Gut, dass ich schon
reserviert habe, denn im Juni ist dort immer viel los. Es gibt vegetarisches
Essen, weil Jonas kein Fleisch isst. Weißt du schon, ob du kommen kannst?
Ich freue mich auf dich! Deine Mia
""",
            [
                ("Mia und Jonas haben sich verlobt.", True),
                ("Sie feiern im Juli.", False),
                ("Mia hat schon einen Tisch reserviert.", True),
                ("Jonas isst gern Fleisch.", False),
            ],
        ),
        form=[
            ("Gut, dass du gekommen ___. (sein)", "bist"),
            ("Ich bleibe hier, weil ich müde ___. (sein)", "bin"),
            ("Wir freuen ___ auf die Party. (wir)", "uns"),
            ("Weißt du, ___ er heute kommt? (whether)", "ob"),
            ("Wenn es kalt ___, trinke ich Tee. (sein)", "ist"),
        ],
        mistake=[
            ("Gut, dass du *hast* reserviert.", "Gut, dass du reserviert hast."),
            ("Ich freue *dich* auf den Urlaub.", "Ich freue mich auf den Urlaub."),
            ("Weißt du, *wenn* Anna heute kommt?", "Weißt du, ob Anna heute kommt?"),
            ("Wenn es warm *sind*, essen wir Salat.", "Wenn es warm ist, essen wir Salat."),
        ],
        dictation=[
            "Gut, dass du reserviert hast.",
            "Ich freue mich so für dich.",
            "Wenn es warm ist, essen wir meist Salat.",
            "Zum Schluss würzt du alles mit Salz.",
        ],
    ),
    5: modul_check(
        LEVEL,
        15,
        dialogue=(
            [
                "A: Was machst du heute Abend?",
                "B: Ich sehe meine Lieblingsserie. ___",
                "A: Schon? Dann schnell, schalt den Fernseher ein!",
                "B: Wo ist denn die Fernbedienung?",
            ],
            "Gleich geht's los!",
            "Das Paket wird morgen geliefert.",
            "Als ich zehn war, habe ich Englisch gelernt.",
        ),
        qa=[
            ("Wann wird das Paket geliefert?", "Morgen Vormittag."),
            ("Wie oft siehst du fern?", "Zweimal pro Woche."),
            ("Wie war deine erste Lehrerin?", "Sehr geduldig."),
            ("Hast du die Sendung gesehen?", "Nein, ich habe sie verpasst."),
            ("Wie beginnt ein formeller Brief?", "Sehr geehrte Damen und Herren,"),
        ],
        odd=[
            ("der Krimi", "der Absender", "der Empfänger", "die Adresse"),
            ("üben", "einschalten", "ausschalten", "umschalten"),
            ("das Wörterbuch", "die Serie", "die Werbung", "die Dokumentation"),
            ("die Schere", "die Grammatik", "die Aussprache", "die Vokabel"),
        ],
        reading=(
            """
Herr Kim lernt seit zwei Jahren Deutsch. Als er nach Deutschland gekommen ist, war die
Aussprache für ihn sehr schwierig. Jeden Abend sieht er die Nachrichten im
Fernsehen, und sonntags sieht er einen Krimi. Die Sendungen nimmt er oft auf,
weil er abends lange arbeitet. Neue Wörter schreibt er in ein Heft.
""",
            [
                ("Herr Kim lernt seit zwei Jahren Deutsch.", True),
                ("Die Grammatik war am Anfang am schwierigsten.", False),
                ("Sonntags sieht er einen Krimi.", True),
                ("Er sieht die Sendungen nie später.", False),
            ],
        ),
        form=[
            ("___ ich klein war, habe ich viel gelesen. (when, once)", "Als"),
            ("Das Paket ___ heute verschickt. (werden)", "wird"),
            ("Die Briefe werden ___. (sortieren)", "sortiert"),
            ("Ich habe die Sendung ___. (verpassen)", "verpasst"),
            ("Ich schalte das Radio ___. (off)", "aus"),
        ],
        mistake=[
            (
                "*Wenn* ich zehn war, habe ich Englisch gelernt.",
                "Als ich zehn war, habe ich Englisch gelernt.",
            ),
            ("Das Paket *werden* morgen geliefert.", "Das Paket wird morgen geliefert."),
            ("Hast du die Sendung *geverpasst*?", "Hast du die Sendung verpasst?"),
            ("Ich *einschalte* den Fernseher.", "Ich schalte den Fernseher ein."),
        ],
        dictation=[
            "Meine erste Lehrerin war sehr geduldig.",
            "Es werden fleißig Päckchen gepackt.",
            "Gleich geht es los.",
            "Ich habe die Sendung leider verpasst.",
        ],
    ),
    6: modul_check(
        LEVEL,
        18,
        dialogue=(
            [
                "A: Hotel Seeblick, guten Tag.",
                "B: Guten Tag. ___",
                "A: Ja, wir haben noch ein Doppelzimmer.",
                "B: Super, dann reserviere ich es.",
            ],
            "Darf ich fragen, ob Sie noch ein Zimmer frei haben?",
            "Ich freue mich auf Sonne und Wärme.",
            "Wir hatten eine Reifenpanne.",
        ),
        qa=[
            ("Wann beginnt das Frühstück?", "Um sieben Uhr."),
            ("Woher kommt ihr gerade?", "Vom Strand."),
            ("Worauf freust du dich?", "Auf den Sommer."),
            ("Worüber ärgerst du dich?", "Über den Regen."),
            ("Wie lange dauert die Fahrt?", "Etwa drei Stunden."),
        ],
        odd=[
            ("die Sauna", "der Hagel", "der Schnee", "der Regen"),
            ("tanken", "trocken", "feucht", "regnerisch"),
            ("die Insel", "die Rezeption", "das Einzelzimmer", "die Halbpension"),
            ("das Klima", "die Fähre", "die Autobahn", "die Tankstelle"),
        ],
        reading=(
            """
Familie Popescu fährt jedes Jahr mit dem Auto nach Rumänien. Die Strecke ist
lang, deshalb übernachten sie in einem Hotel in Ungarn. Dieses Jahr hatten sie auf
der Autobahn viel Stau, und es hat stark geregnet. Aber in Rumänien war das
Wetter super: viel Sonnenschein und 30 Grad. Darauf hatten sich alle gefreut.
""",
            [
                ("Die Familie fährt mit dem Zug nach Rumänien.", False),
                ("Sie übernachten in Ungarn.", True),
                ("Auf der Autobahn war kein Stau.", False),
                ("In Rumänien war das Wetter schön.", True),
            ],
        ),
        form=[
            ("Können Sie mir sagen, wo die Sauna ___? (sein)", "ist"),
            ("Wir kommen gerade ___ dem Urlaub. (from)", "aus"),
            ("Ich ___ jetzt gern am Meer. (sein, Konjunktiv)", "wäre"),
            ("Ich ärgere mich ___ das Wetter. (about)", "über"),
            ("___ freust du dich? (wo + auf)", "Worauf"),
        ],
        mistake=[
            (
                "Ich möchte wissen, wann das Frühstück *beginnen*.",
                "Ich möchte wissen, wann das Frühstück beginnt.",
            ),
            ("Wir kommen gerade *von* der Schweiz.", "Wir kommen gerade aus der Schweiz."),
            ("Ich freue mich *für* den Sommer.", "Ich freue mich auf den Sommer."),
            (
                "Freust du dich auf das Fest? Ja, *dafür* freue ich mich.",
                "Freust du dich auf das Fest? Ja, darauf freue ich mich.",
            ),
        ],
        dictation=[
            "Darf ich fragen, ob das Frühstück inklusive ist?",
            "Wir wollen nach Rumänien fahren.",
            "Ich freue mich auf Sonne und Wärme.",
            "Morgen steigen die Temperaturen.",
        ],
    ),
    7: modul_check(
        LEVEL,
        21,
        dialogue=(
            [
                "A: Was machen wir heute Abend?",
                "B: ___",
                "A: Na ja, ich weiß nicht. Ich würde lieber ins Kino gehen.",
                "B: Okay, dann gehen wir ins Kino.",
            ],
            "Wie wäre es mit einer Lesung?",
            "Ja genau, den meine ich.",
            "Ich durfte keine Comics lesen.",
        ),
        qa=[
            ("Welchen Ausweis meinen Sie?", "Den hier."),
            ("Was durftest du als Kind nicht?", "Lange fernsehen."),
            ("Wie wäre es mit dem Zirkus?", "Gute Idee, da bin ich dabei!"),
            ("Wo bekomme ich einen neuen Pass?", "Im Bürgeramt."),
            ("Was liest du am liebsten?", "Romane, besonders Krimis."),
        ],
        odd=[
            ("der Täter", "der Roman", "das Gedicht", "das Märchen"),
            ("stehlen", "die Lesung", "die Aufführung", "das Kabarett"),
            ("der Verlag", "der Ausweis", "der Reisepass", "das Visum"),
            ("vorlesen", "der Einbruch", "der Diebstahl", "das Verbrechen"),
        ],
        reading=(
            """
Als Kind durfte Sara keine Comics lesen. Ihre Eltern wollten, dass sie Romane
liest. Heute ist Sara Autorin und schreibt Comics für Kinder! Nächste Woche gibt
sie eine Lesung in der Stadtbibliothek. Der Eintritt ist frei, aber man sollte
früh kommen, denn die letzte Lesung war schnell voll.
""",
            [
                ("Sara durfte als Kind Comics lesen.", False),
                ("Heute schreibt Sara Comics.", True),
                ("Der Eintritt zur Lesung kostet zehn Euro.", False),
                ("Man sollte früh zur Lesung kommen.", True),
            ],
        ),
        form=[
            ("Ich schlage vor, dass wir ins Theater ___. (gehen)", "gehen"),
            ("Als Kind ___ ich nicht lange aufbleiben. (dürfen, Präteritum)", "durfte"),
            ("Wir ___ jeden Tag lesen. (müssen, Präteritum)", "mussten"),
            ("___ Formular brauche ich? (which)", "Welches"),
            ("Ich ___ meine Uhr reparieren. (lassen)", "lasse"),
        ],
        mistake=[
            (
                "Ich schlage vor, *ob* wir ins Kino gehen.",
                "Ich schlage vor, dass wir ins Kino gehen.",
            ),
            (
                "Als Kind *dürfte* ich keine Comics lesen.",
                "Als Kind durfte ich keine Comics lesen.",
            ),
            ("*Welcher* Ausweis meinen Sie?", "Welchen Ausweis meinen Sie?"),
            ("Ich lasse mein Auto *repariert*.", "Ich lasse mein Auto reparieren."),
        ],
        dictation=[
            "Wie wäre es mit einem Konzert?",
            "Ich durfte eigentlich keine Comics lesen.",
            "Ja genau, den meine ich.",
            "Ich lasse mein Auto reparieren.",
        ],
    ),
    8: modul_check(
        LEVEL,
        24,
        dialogue=(
            [
                "A: Du warst doch ein Jahr in Kanada. ___",
                "B: Ich stand um sieben auf und fuhr mit der U-Bahn ins Büro.",
                "A: Und hattest du Heimweh?",
                "B: Am Anfang schon, aber später nicht mehr.",
            ],
            "Wie sah dein Alltag aus?",
            "Seit wann wohnst du hier?",
            "Welchen Beruf suchst du?",
        ),
        qa=[
            ("Seit wann wohnst du hier?", "Seit zwei Jahren."),
            ("Wie lange wartest du noch?", "Bis der Bus kommt."),
            ("Was für einen Beruf suchst du?", "Einen, der kreativ ist."),
            ("Wann hast du das Vorstellungsgespräch?", "Morgen um zehn."),
            ("Hattest du im Ausland Heimweh?", "Am Anfang schon."),
        ],
        odd=[
            ("das Heimweh", "das Benzin", "der Strom", "die Energie"),
            ("der Lebenslauf", "die Gastfamilie", "der Austausch", "das Auslandssemester"),
            ("teilen", "das Gehalt", "der Lohn", "die Karriere"),
            ("angenehm", "anklicken", "auswählen", "eingeben"),
        ],
        reading=(
            """
Seit Tim seinen Wagen verkauft hat, fährt er jeden Tag mit dem Fahrrad zur
Arbeit. Er arbeitet als Azubi in einer Firma, die Elektroautos herstellt. Die
Arbeit macht ihm viel Spaß. Letztes Jahr war er drei Monate in Schweden. Am
Anfang war alles ungewohnt, aber schließlich fühlte er sich dort sehr wohl.
""",
            [
                ("Tim fährt mit dem Auto zur Arbeit.", False),
                ("Seine Firma stellt Elektroautos her.", True),
                ("Tim war ein Jahr in Schweden.", False),
                ("In Schweden fühlte er sich am Ende wohl.", True),
            ],
        ),
        form=[
            ("___ ich in Berlin wohne, fahre ich Rad. (since)", "Seit"),
            ("Ich warte, ___ du kommst. (until)", "bis"),
            ("Das ist der Beruf, ___ zu mir passt. (relative pronoun)", "der"),
            ("Der Kollege, ___ ich kenne, ist nett. (relative pronoun)", "den"),
            ("Jeden Morgen ___ ich um sechs auf. (aufstehen, Präteritum)", "stand"),
        ],
        mistake=[
            ("Ich wohne seit zwei *Jahre* hier.", "Ich wohne seit zwei Jahren hier."),
            ("Das ist der Beruf, *den* zu mir passt.", "Das ist der Beruf, der zu mir passt."),
            ("Der Kollege, *der* ich kenne, ist nett.", "Der Kollege, den ich kenne, ist nett."),
            ("Jeden Morgen *stehte* ich um sechs auf.", "Jeden Morgen stand ich um sechs auf."),
        ],
        dictation=[
            "Seit ich meinen Wagen verkauft habe, fahre ich mehr Fahrrad.",
            "Das ist der Beruf, der zu mir passt.",
            "Wie sah dein Alltag aus?",
            "Am Anfang war es schwierig.",
        ],
    ),
}
