"""A2 Hören sets, shaped like the Goethe-Zertifikat A2 listening paper: one set
per Modul. Teil 1: 5 radio texts, announcements and phone messages, a/b/c,
heard twice. Teil 2: one conversation, 5 items matched to choices (letters
a-h, each used once), heard once. Teil 3: 5 short dialogues, a/b/c, heard once.
Teil 4: a radio interview, 5 statements ja/nein, heard twice.

All scripts are original, on the Modul's topics, using A1 words plus the A2
words taught up to the Modul's last Lektion. The audio is generated once with
`manage.py make_hoeren_audio`.
"""

from ..dsl import clip, hoeren_match, hoeren_mc, hoeren_teil, hoeren_yn

# The Moduls testers see in production; the rest stay local (DEBUG shows all).
LIVE = set(range(1, 9))

RADIO = "Listen to the texts. Choose a, b or c. (You hear each text twice.)"
CONVERSATION = (
    "Listen to the conversation. Choose the right letter for each item. (You hear it once.)"
)
DIALOGUES = "Listen to the dialogues. Choose a, b or c. (You hear each dialogue once.)"
INTERVIEW = "Listen to the interview. Ja oder nein? (You hear it twice.)"


# Where each Modul's conversation (Teil 2) and dialogues (Teil 3) take place;
# "" is a quiet room. The interviews (Teil 4) sound like the radio.
SCENES = {
    1: ("", ["cafe", "cafe", "park", "laden", ""]),
    2: ("cafe", ["laden", "strasse", "cafe", "laden", "strasse"]),
    3: ("cafe", ["buero", "park", "buero", "buero", "strasse"]),
    4: ("cafe", ["cafe", "cafe", "", "cafe", ""]),
    5: ("buero", ["laden", "", "cafe", "", ""]),
    6: ("cafe", ["", "bahnhof", "", "", "strasse"]),
    7: ("cafe", ["buero", "cafe", "strasse", "strasse", "bahnhof"]),
    8: ("buero", ["cafe", "cafe", "buero", "cafe", "buero"]),
}


def _sound(who: str, text: str) -> dict:
    """Teil 1: phone messages sound like a phone; announcements in a shop or a
    station start with a gong over their background; the rest is radio."""
    if who != "Ansage":
        return {"phone": True}
    if text.startswith("Liebe Kunden"):
        return {"gong": True, "scene": "laden"}
    if text.startswith(("Achtung am Gleis", "Liebe Fahrgäste")):
        return {"gong": True, "scene": "bahnhof"}
    if text.startswith("Liebe Mitarbeiter"):
        return {"gong": True, "scene": "buero"}
    if text.startswith(("Liebe Besucher", "Liebe Gäste")):
        return {"gong": True}
    return {"radio": True}


def _set(modul, radio, conversation, dialogues, interview) -> list:
    lines, choices, rows = conversation
    talk, statements = interview
    talk_scene, dialogue_scenes = SCENES[modul]
    return [
        hoeren_teil(
            1, RADIO, *[hoeren_mc(clip((who, t), **_sound(who, t)), *q) for who, t, q in radio]
        ),
        hoeren_match(2, CONVERSATION, clip(*lines, plays=1, scene=talk_scene), choices, rows),
        hoeren_teil(
            3,
            DIALOGUES,
            *[
                hoeren_mc(clip(*d, plays=1, scene=where), *q)
                for (d, q), where in zip(dialogues, dialogue_scenes, strict=True)
            ],
        ),
        hoeren_teil(
            4,
            INTERVIEW,
            *[hoeren_yn(s, ok) for s, ok in statements],
            recording=clip(*talk, plays=2, radio=True),  # Goethe A2: a radio interview
        ),
    ]


HOEREN = {
    # Modul 1 (Lektionen 1-3): family and childhood, furniture, holidays in nature.
    1: _set(
        1,
        [
            (
                "Ansage",
                "Und nun das Wetter für morgen: Am Vormittag ist es noch bewölkt, aber am "
                "Nachmittag scheint überall die Sonne. Es wird bis zu zweiundzwanzig Grad warm.",
                ("Wie ist das Wetter morgen am Nachmittag?", "Sonnig", "Bewölkt", "Regnerisch"),
            ),
            (
                "Frau",
                "Hallo Jonas, hier ist Tante Petra. Wir kommen am Samstag nicht um zehn, sondern "
                "erst um zwölf Uhr. Onkel Karl muss am Vormittag noch arbeiten. Bis Samstag!",
                ("Wann kommt Tante Petra?", "Um zwölf Uhr", "Um zehn Uhr", "Am Sonntag"),
            ),
            (
                "Ansage",
                "Liebe Kunden, heute nur bei uns: Alle Regale und Kommoden sind dreißig Prozent "
                "billiger. Sie finden sie im zweiten Stock.",
                (
                    "Wo findet man die Regale?",
                    "Im zweiten Stock",
                    "Im Erdgeschoss",
                    "Im dritten Stock",
                ),
            ),
            (
                "Mann",
                "Guten Tag, Frau Berger, hier ist die Firma Umzug Schnell. Unser Team kommt am "
                "Montag um acht Uhr. Bitte packen Sie bis dahin alle Bücher in Kartons.",
                (
                    "Was soll Frau Berger machen?",
                    "Die Bücher einpacken",
                    "Die Möbel tragen",
                    "Das Team anrufen",
                ),
            ),
            (
                "Ansage",
                "Sie suchen Ruhe und Erholung? Dann besuchen Sie das Dorf Seefeld am See. Hier "
                "gibt es schöne Wanderwege, eine Pension direkt am Ufer und einen Campingplatz "
                "für Familien.",
                ("Wo ist die Pension?", "Direkt am Ufer", "Im Wald", "Im Zentrum"),
            ),
        ],
        (
            [
                ("Mann", "So, wohin stellen wir das Sofa?"),
                ("Frau", "Das Sofa kommt ins Wohnzimmer, an die Wand gegenüber vom Fenster."),
                ("Mann", "Gut. Und der große Spiegel? Ins Bad?"),
                ("Frau", "Nein, der ist zu groß für das Bad. Den hängen wir in den Flur."),
                ("Mann", "Okay. Die Kommode ist so schwer! Wohin damit?"),
                ("Frau", "Ins Schlafzimmer, neben das Bett."),
                ("Mann", "Und das kleine Regal für die Bücher von Lena?"),
                ("Frau", "Genau, das stellen wir ins Kinderzimmer."),
                ("Mann", "Und die alte Lampe von deiner Oma?"),
                (
                    "Frau",
                    "Die finde ich so schön! Die kommt auf meinen Schreibtisch im Arbeitszimmer.",
                ),
            ],
            {
                "a": "das Wohnzimmer",
                "b": "das Schlafzimmer",
                "c": "der Flur",
                "d": "die Küche",
                "e": "das Kinderzimmer",
                "f": "das Bad",
                "g": "der Balkon",
                "h": "das Arbeitszimmer",
            },
            [
                ("das Sofa", "a"),
                ("der Spiegel", "c"),
                ("die Kommode", "b"),
                ("das Regal", "e"),
                ("die Lampe", "h"),
            ],
        ),
        [
            (
                [
                    ("Mann", "Was hast du als Kind gern gespielt?"),
                    (
                        "Frau",
                        "Ich habe immer mit meiner Puppe gespielt. Mein Bruder hat lieber Fußball gespielt.",
                    ),
                ],
                (
                    "Womit hat die Frau als Kind gespielt?",
                    "Mit einer Puppe",
                    "Mit einem Ball",
                    "Mit Autos",
                ),
            ),
            (
                [
                    ("Frau", "Wo bist du aufgewachsen?"),
                    (
                        "Mann",
                        "In einem kleinen Dorf in den Bergen. Mit sechzehn bin ich dann nach München gezogen.",
                    ),
                ],
                (
                    "Wo ist der Mann aufgewachsen?",
                    "In einem Dorf in den Bergen",
                    "In München",
                    "Am Meer",
                ),
            ),
            (
                [
                    ("Mann", "Wie war der Campingplatz?"),
                    (
                        "Frau",
                        "Sehr schön, direkt am See. Aber die Duschen waren leider nicht sauber.",
                    ),
                ],
                ("Was war nicht gut?", "Die Duschen", "Der See", "Der Platz"),
            ),
            (
                [
                    ("Frau", "Was hast du für das Wochenende gebucht?"),
                    (
                        "Mann",
                        "Ein Zimmer in einer Pension, mit Frühstück. Das ist preiswerter als ein Hotel.",
                    ),
                ],
                (
                    "Was hat der Mann gebucht?",
                    "Ein Zimmer in einer Pension",
                    "Ein Hotelzimmer",
                    "Einen Campingplatz",
                ),
            ),
            (
                [
                    ("Mann", "Wohin soll das Poster?"),
                    ("Frau", "Häng es bitte über das Sofa. Nicht über den Tisch."),
                ],
                ("Wohin soll das Poster?", "Über das Sofa", "Über den Tisch", "Neben die Tür"),
            ),
        ],
        (
            [
                (
                    "Ansage",
                    "Herr Hoffmann, Sie sind Bäcker, wie Ihr Vater und Ihr Opa. Wollten Sie das schon als Kind?",
                ),
                (
                    "Mann",
                    "Nein, gar nicht! Als Kind wollte ich Fußballspieler werden. Ich war jeden Tag auf dem Platz.",
                ),
                ("Ansage", "Und wann wollten Sie dann doch Bäcker werden?"),
                (
                    "Mann",
                    "Mit siebzehn. Ich habe in den Ferien in der Bäckerei geholfen, und das hat mir viel Spaß gemacht.",
                ),
                ("Ansage", "Wie sieht Ihr Tag heute aus?"),
                (
                    "Mann",
                    "Ich stehe um drei Uhr auf. Um vier bin ich in der Bäckerei. Am Nachmittag bin ich dann sehr müde.",
                ),
                ("Ansage", "Und was backen Sie am liebsten?"),
                ("Mann", "Brot! Den Kuchen backt meine Frau. Sie macht das viel besser als ich."),
                ("Ansage", "Arbeiten Ihre Kinder auch in der Bäckerei?"),
                ("Mann", "Meine Tochter hilft am Samstag. Mein Sohn studiert in Berlin."),
            ],
            [
                ("Herr Hoffmann wollte als Kind Bäcker werden.", False),
                ("Mit siebzehn hat er in der Bäckerei geholfen.", True),
                ("Er ist um drei Uhr in der Bäckerei.", False),
                ("Seine Frau backt die Kuchen.", True),
                ("Sein Sohn arbeitet in der Bäckerei.", False),
            ],
        ),
    ),
    # Modul 2 (Lektionen 4-6): shopping and quantities, sightseeing, culture.
    2: _set(
        2,
        [
            (
                "Ansage",
                "Liebe Kunden, heute im Angebot: ein Kilo Tomaten für nur einen Euro fünfzig "
                "und frische Bananen, das Kilo für einen Euro neunundneunzig.",
                ("Was kostet ein Kilo Tomaten?", "1,50 Euro", "1,99 Euro", "1,05 Euro"),
            ),
            (
                "Frau",
                "Hallo Marco, hier ist Silvia. Ich habe zwei Karten für das Musical am Freitag. "
                "Wir treffen uns um halb acht am Eingang vom Theater. Ruf mich bitte zurück!",
                ("Wo treffen sie sich?", "Am Eingang vom Theater", "Vor dem Kino", "Im Café"),
            ),
            (
                "Ansage",
                "Die nächste Führung durch die Altstadt beginnt um vierzehn Uhr am Marktplatz. "
                "Sie dauert neunzig Minuten und endet an der Burg.",
                ("Wo endet die Führung?", "An der Burg", "Am Marktplatz", "Am Dom"),
            ),
            (
                "Mann",
                "Guten Tag, hier ist die Metzgerei Huber. Ihre Bestellung ist fertig: zwei "
                "Hähnchen und ein Kilo Wurst. Sie können sie ab fünfzehn Uhr abholen.",
                ("Ab wann kann man die Bestellung abholen?", "Ab 15 Uhr", "Ab 13 Uhr", "Ab 12 Uhr"),
            ),
            (
                "Ansage",
                "Am Wochenende gibt es im Stadtpark das große Sommerfestival: Musik, Theater "
                "und Kunst für die ganze Familie. Und das Beste: Es kostet nichts!",
                ("Was kostet das Festival?", "Nichts", "5 Euro", "10 Euro"),
            ),
        ],
        (
            [
                ("Mann", "Na, Anna, wie war Wien?"),
                (
                    "Frau",
                    "Super! Am Freitag bin ich angekommen und habe gleich eine Stadtführung gemacht. So habe ich die Stadt gut kennengelernt.",
                ),
                ("Mann", "Und am Samstag?"),
                (
                    "Frau",
                    "Am Samstag hat es geregnet. Da war ich den ganzen Tag im Museum. Am Abend wollte ich in die Oper, aber es gab keine Karten mehr.",
                ),
                ("Mann", "Schade! Und am Sonntag?"),
                (
                    "Frau",
                    "Da habe ich das Schloss Schönbrunn besichtigt. Es ist wirklich beeindruckend.",
                ),
                ("Mann", "Und am Montag?"),
                ("Frau", "Am Montag war ich einkaufen. Ich habe ein Kleid und Schuhe gekauft."),
                ("Mann", "Und am Dienstag bist du zurückgefahren?"),
                (
                    "Frau",
                    "Ja, aber am Vormittag habe ich noch in einem Café gefrühstückt. Das Café war wunderschön.",
                ),
            ],
            {
                "a": "ins Museum gehen",
                "b": "in die Oper gehen",
                "c": "eine Stadtführung machen",
                "d": "einkaufen",
                "e": "ins Ballett gehen",
                "f": "ein Konzert im Park",
                "g": "ein Schloss besichtigen",
                "h": "im Café frühstücken",
            },
            [
                ("Freitag", "c"),
                ("Samstag", "a"),
                ("Sonntag", "g"),
                ("Montag", "d"),
                ("Dienstag", "h"),
            ],
        ),
        [
            (
                [
                    ("Frau", "Ich hätte gern zweihundert Gramm Käse."),
                    ("Mann", "Gern. Darf es sonst noch etwas sein?"),
                    ("Frau", "Ja, noch ein Stück Butter, bitte."),
                ],
                ("Was kauft die Frau noch?", "Butter", "Wurst", "Brot"),
            ),
            (
                [
                    ("Mann", "Welche Sehenswürdigkeit gefällt dir am besten?"),
                    ("Frau", "Der Dom! Die Burg ist auch schön, aber der Dom ist beeindruckend."),
                ],
                ("Was gefällt der Frau am besten?", "Der Dom", "Die Burg", "Das Rathaus"),
            ),
            (
                [
                    ("Frau", "Wie war das Konzert?"),
                    (
                        "Mann",
                        "Die Band war super, aber das Publikum war so laut. Ich habe fast nichts gehört.",
                    ),
                ],
                (
                    "Was war nicht gut?",
                    "Das Publikum war laut.",
                    "Die Band war schlecht.",
                    "Die Karten waren teuer.",
                ),
            ),
            (
                [
                    ("Mann", "Wie viele Flaschen Wasser brauchen wir?"),
                    ("Frau", "Sechs. Und zwei Flaschen Saft."),
                ],
                ("Wie viele Flaschen Wasser brauchen sie?", "Sechs", "Zwei", "Acht"),
            ),
            (
                [
                    ("Frau", "Fahren wir mit dem Bus zum Theater?"),
                    ("Mann", "Nein, lieber zu Fuß. Es ist nicht weit, nur über die Brücke."),
                ],
                ("Wie kommen sie zum Theater?", "Zu Fuß", "Mit dem Bus", "Mit dem Taxi"),
            ),
        ],
        (
            [
                (
                    "Ansage",
                    "Frau Lindner, Sie spielen Gitarre im Theater der Stadt. Seit wann machen Sie Musik?",
                ),
                (
                    "Frau",
                    "Seit ich sechs Jahre alt bin. Meine Mutter war Musiklehrerin. Bei uns gab es immer Musik.",
                ),
                ("Ansage", "Spielen Sie nur klassische Musik?"),
                (
                    "Frau",
                    "Im Theater ja. Aber am Wochenende spiele ich mit Freunden in einer kleinen Band.",
                ),
                ("Ansage", "Was ist Ihre Lieblingsveranstaltung?"),
                (
                    "Frau",
                    "Das Sommerfestival im Park. Da kommen viele Familien und Kinder. Viele von ihnen gehen sonst nie in ein Konzert.",
                ),
                ("Ansage", "Haben Sie vor einem Konzert noch Angst?"),
                ("Frau", "Ein bisschen Stress habe ich immer. Aber Angst habe ich nicht mehr."),
            ],
            [
                ("Frau Lindner macht seit ihrer Kindheit Musik.", True),
                ("Ihr Vater war Musiklehrer.", False),
                ("Am Wochenende spielt sie in einer Band.", True),
                ("Zum Sommerfestival kommen keine Kinder.", False),
                ("Sie hat vor Konzerten große Angst.", False),
            ],
        ),
    ),
    # Modul 3 (Lektionen 7-9): sport, health, work.
    3: _set(
        3,
        [
            (
                "Ansage",
                "Und jetzt der Sport: Der FC Lindau hat am Samstag zwei zu eins gegen Ulm "
                "gewonnen. Das nächste Spiel ist am Sonntag in einer Woche.",
                ("Wer hat das Spiel gewonnen?", "Lindau", "Ulm", "Keine Mannschaft"),
            ),
            (
                "Frau",
                "Guten Tag, hier ist die Praxis Doktor Sommer. Ihre Untersuchung war gut, alles "
                "ist in Ordnung. Sie müssen keine Tabletten mehr nehmen. Auf Wiederhören!",
                (
                    "Was sagt die Praxis?",
                    "Alles ist in Ordnung.",
                    "Er braucht neue Tabletten.",
                    "Er soll noch einmal kommen.",
                ),
            ),
            (
                "Mann",
                "Hallo, hier ist Tim vom Fitnessstudio Kraftwerk. Ihr erstes Training ist am "
                "Mittwoch um achtzehn Uhr. Bitte bringen Sie Sportschuhe und ein Handtuch mit.",
                (
                    "Was soll man mitbringen?",
                    "Sportschuhe und ein Handtuch",
                    "Eine Flasche Wasser",
                    "Sportkleidung und Geld",
                ),
            ),
            (
                "Ansage",
                "Liebe Mitarbeiterinnen und Mitarbeiter, die Sitzung der Abteilung Export ist "
                "heute nicht um zehn Uhr, sondern um vierzehn Uhr in Raum zweihundertdrei.",
                ("Wann ist die Sitzung?", "Um 14 Uhr", "Um 10 Uhr", "Um 12 Uhr"),
            ),
            (
                "Ansage",
                "Im Herbst haben viele Menschen eine Erkältung. Unser Tipp: Trinken Sie viel "
                "Tee, schlafen Sie genug und gehen Sie jeden Tag eine halbe Stunde spazieren.",
                (
                    "Was soll man jeden Tag machen?",
                    "Spazieren gehen",
                    "Im Studio trainieren",
                    "Viel Obst essen",
                ),
            ),
        ],
        (
            [
                ("Frau", "Sag mal, Paul, ist bei euch in der Familie jeder so sportlich?"),
                ("Mann", "Fast! Mein Bruder Jonas spielt dreimal pro Woche Fußball im Verein."),
                ("Frau", "Und deine Schwester Lisa?"),
                (
                    "Mann",
                    "Lisa geht ins Fitnessstudio und macht Krafttraining. Joggen findet sie langweilig.",
                ),
                ("Frau", "Und dein Opa? Er ist doch schon achtzig!"),
                ("Mann", "Ja, aber er schwimmt jeden Morgen eine halbe Stunde."),
                ("Frau", "Toll! Und deine Mutter?"),
                (
                    "Mann",
                    "Meine Mutter macht Yoga, montags und donnerstags. Das ist gut für ihren Rücken.",
                ),
                ("Frau", "Und was machst du?"),
                ("Mann", "Ich fahre jeden Tag mit dem Fahrrad zur Arbeit. Das ist mein Sport!"),
            ],
            {
                "a": "joggen",
                "b": "schwimmen",
                "c": "Yoga",
                "d": "Fußball",
                "e": "Ski fahren",
                "f": "Krafttraining",
                "g": "Rad fahren",
                "h": "Tennis",
            },
            [
                ("Jonas", "d"),
                ("Lisa", "f"),
                ("der Opa", "b"),
                ("die Mutter", "c"),
                ("Paul", "g"),
            ],
        ),
        [
            (
                [
                    ("Mann", "Was fehlt Ihnen denn?"),
                    ("Frau", "Mir ist schwindelig und ich habe Kopfschmerzen."),
                ],
                ("Was hat die Frau?", "Schwindel und Kopfschmerzen", "Fieber", "Bauchschmerzen"),
            ),
            (
                [
                    ("Frau", "Wie oft trainierst du?"),
                    ("Mann", "Zweimal pro Woche, dienstags und freitags."),
                ],
                (
                    "Wann trainiert der Mann?",
                    "Dienstags und freitags",
                    "Montags und donnerstags",
                    "Jeden Tag",
                ),
            ),
            (
                [
                    ("Mann", "In welcher Abteilung arbeiten Sie?"),
                    ("Frau", "In der Produktion. Vorher war ich im Export."),
                ],
                (
                    "Wo arbeitet die Frau jetzt?",
                    "In der Produktion",
                    "Im Export",
                    "Im Büro vom Chef",
                ),
            ),
            (
                [
                    ("Frau", "Müssen Sie zur Untersuchung ins Krankenhaus?"),
                    ("Mann", "Nein, das macht Doktor Wagner hier in der Praxis."),
                ],
                ("Wo ist die Untersuchung?", "In der Praxis", "Im Krankenhaus", "Zu Hause"),
            ),
            (
                [
                    ("Mann", "Wie kommst du zur Fabrik?"),
                    (
                        "Frau",
                        "Mit dem Bus. Früher bin ich mit dem Auto gefahren, aber das war zu teuer.",
                    ),
                ],
                (
                    "Wie fährt die Frau jetzt zur Fabrik?",
                    "Mit dem Bus",
                    "Mit dem Auto",
                    "Mit dem Fahrrad",
                ),
            ),
        ],
        (
            [
                (
                    "Ansage",
                    "Herr Demir, Sie haben vor fünf Jahren ein kleines Fitnessstudio aufgemacht. Wie geht es dem Studio heute?",
                ),
                (
                    "Mann",
                    "Sehr gut! Bei uns trainieren jetzt dreihundert Leute, und wir haben vier Trainer.",
                ),
                ("Ansage", "Wer kommt zu Ihnen?"),
                (
                    "Mann",
                    "Viele junge Leute, aber auch ältere. Die älteste Frau bei uns ist achtundsiebzig!",
                ),
                ("Ansage", "Was ist Ihr Tipp für alle, die neu anfangen?"),
                (
                    "Mann",
                    "Nicht zu viel am Anfang! Lieber zweimal pro Woche eine Stunde als einmal drei Stunden.",
                ),
                ("Ansage", "Und machen Sie selbst noch Sport?"),
                (
                    "Mann",
                    "Leider wenig. Ich arbeite zu viel. Aber am Sonntag gehe ich immer joggen.",
                ),
            ],
            [
                ("Im Studio trainieren dreihundert Leute.", True),
                ("Nur junge Leute trainieren dort.", False),
                ("Am Anfang soll man sehr viel trainieren.", False),
                ("Herr Demir hat wenig Zeit für Sport.", True),
                ("Er joggt am Samstag.", False),
            ],
        ),
    ),
    # Modul 4 (Lektionen 10-12): restaurant, family news and feelings, food.
    4: _set(
        4,
        [
            (
                "Frau",
                "Guten Tag, hier ist das Restaurant Seeterrasse. Sie haben einen Tisch für "
                "Samstag reserviert. Leider ist der Garten an diesem Abend geschlossen. Wir "
                "haben einen Tisch im Restaurant für Sie.",
                ("Wo ist der Tisch jetzt?", "Im Restaurant", "Im Garten", "Auf dem Balkon"),
            ),
            (
                "Ansage",
                "Heute kochen wir eine schnelle Gemüsesuppe. Sie brauchen Kartoffeln, Zwiebeln, "
                "eine Tomate und etwas Salz. Die Suppe ist in zwanzig Minuten fertig.",
                ("Wie lange braucht die Suppe?", "20 Minuten", "30 Minuten", "40 Minuten"),
            ),
            (
                "Mann",
                "Hallo Oma, hier ist Felix. Ich habe tolle Nachrichten: Lara und ich haben uns "
                "verlobt! Die Hochzeit ist im nächsten Sommer. Ruf mich an!",
                (
                    "Was ist passiert?",
                    "Felix hat sich verlobt.",
                    "Felix hat geheiratet.",
                    "Felix hat ein Baby.",
                ),
            ),
            (
                "Ansage",
                "Liebe Gäste, unser Gericht heute: Hähnchen mit Reis und Salat für neun Euro "
                "fünfzig. Für Vegetarier gibt es Nudeln mit Gemüse.",
                (
                    "Was gibt es für Vegetarier?",
                    "Nudeln mit Gemüse",
                    "Hähnchen mit Reis",
                    "Nur Salat",
                ),
            ),
            (
                "Frau",
                "Hallo Tom, hier ist Mama. Ich freue mich so auf Sonntag! Bringst du die Kinder "
                "schon um zwölf? Dann können wir zusammen kochen.",
                ("Wann sollen die Kinder kommen?", "Um 12 Uhr", "Um 14 Uhr", "Am Abend"),
            ),
        ],
        (
            [
                ("Mann", "Hallo Sara, wer bringt denn was zur Party mit?"),
                ("Frau", "Also, Anna macht ihren berühmten Kartoffelsalat."),
                ("Mann", "Super. Und Ben?"),
                (
                    "Frau",
                    "Ben wollte zuerst einen Kuchen backen, aber er hat keine Zeit. Er bringt die Getränke.",
                ),
                ("Mann", "Und Lukas?"),
                ("Frau", "Lukas kauft das Brot beim Bäcker."),
                ("Mann", "Und Maria?"),
                ("Frau", "Maria backt den Kuchen! Mit Schokolade, natürlich."),
                ("Mann", "Lecker. Und Kemal?"),
                ("Frau", "Kemal macht die Musik. Er bringt seine Gitarre mit."),
            ],
            {
                "a": "den Salat",
                "b": "den Kuchen",
                "c": "die Getränke",
                "d": "die Nudeln",
                "e": "das Brot",
                "f": "das Obst",
                "g": "die Musik",
                "h": "die Teller und Gläser",
            },
            [
                ("Anna", "a"),
                ("Ben", "c"),
                ("Lukas", "e"),
                ("Maria", "b"),
                ("Kemal", "g"),
            ],
        ),
        [
            (
                [
                    ("Mann", "Zahlen, bitte!"),
                    ("Frau", "Zusammen oder getrennt?"),
                    ("Mann", "Getrennt, bitte."),
                ],
                ("Wie bezahlen sie?", "Getrennt", "Zusammen", "Mit Karte"),
            ),
            (
                [
                    ("Frau", "Wie war das Essen?"),
                    ("Mann", "Lecker, aber die Soße war ein bisschen zu salzig."),
                ],
                ("Was war nicht gut?", "Die Soße", "Das Fleisch", "Die Nachspeise"),
            ),
            (
                [
                    ("Mann", "Warum bist du so nervös?"),
                    ("Frau", "Morgen lerne ich die Eltern von meinem Freund kennen."),
                ],
                (
                    "Warum ist die Frau nervös?",
                    "Sie lernt die Eltern von ihrem Freund kennen.",
                    "Sie hat eine Prüfung.",
                    "Sie heiratet.",
                ),
            ),
            (
                [
                    ("Frau", "Was nimmst du als Vorspeise?"),
                    ("Mann", "Eine Suppe. Und als Hauptspeise den Fisch."),
                ],
                ("Was isst der Mann als Hauptspeise?", "Fisch", "Suppe", "Hähnchen"),
            ),
            (
                [
                    ("Mann", "Isst du morgens Müsli?"),
                    (
                        "Frau",
                        "Nein, meistens esse ich ein Brötchen mit Marmelade. Und ich trinke Kaffee.",
                    ),
                ],
                (
                    "Was isst die Frau meistens zum Frühstück?",
                    "Ein Brötchen mit Marmelade",
                    "Müsli",
                    "Joghurt",
                ),
            ),
        ],
        (
            [
                (
                    "Ansage",
                    "Frau Berger, Sie sind Köchin und haben ein kleines Restaurant in Köln. Was kochen Sie?",
                ),
                (
                    "Frau",
                    "Regionale Gerichte, aber modern. Das Gemüse kaufe ich jeden Morgen auf dem Markt.",
                ),
                ("Ansage", "Gibt es bei Ihnen auch vegetarische Gerichte?"),
                ("Frau", "Ja, natürlich. Heute bestellt fast jeder zweite Gast vegetarisch."),
                ("Ansage", "Kochen Sie zu Hause auch?"),
                (
                    "Frau",
                    "Nein, fast nie! Zu Hause kocht mein Mann. Ich esse dann einfach, was er macht.",
                ),
                ("Ansage", "Was ist Ihr Lieblingsessen?"),
                (
                    "Frau",
                    "Die Kartoffelsuppe von meiner Oma. Die kann ich bis heute nicht so gut kochen wie sie.",
                ),
            ],
            [
                ("Frau Berger kauft das Gemüse im Supermarkt.", False),
                ("Viele Gäste essen vegetarisch.", True),
                ("Zu Hause kocht sie jeden Tag.", False),
                ("Ihr Mann kocht zu Hause.", True),
                ("Ihr Lieblingsessen ist die Suppe von ihrer Oma.", True),
            ],
        ),
    ),
    # Modul 5 (Lektionen 13-15): learning languages, the post, media.
    5: _set(
        5,
        [
            (
                "Ansage",
                "Heute Abend um zwanzig Uhr fünfzehn: der Krimi „Tod am See“. Danach, um "
                "einundzwanzig Uhr fünfundvierzig, kommen die Nachrichten.",
                ("Wann beginnt der Krimi?", "Um 20:15 Uhr", "Um 21:45 Uhr", "Um 20:45 Uhr"),
            ),
            (
                "Mann",
                "Guten Tag, hier ist der Paketdienst. Wir hatten heute ein Paket für Sie, aber "
                "Sie waren nicht zu Hause. Sie können es ab morgen in der Post in der "
                "Bahnhofstraße abholen.",
                (
                    "Wo ist das Paket?",
                    "In der Post in der Bahnhofstraße",
                    "Beim Nachbarn",
                    "Vor der Tür",
                ),
            ),
            (
                "Frau",
                "Hallo, hier ist Frau Hartmann von der Sprachschule Lingua. Ihr A2-Kurs beginnt "
                "nicht am Montag, sondern erst am Mittwoch, den zehnten.",
                (
                    "Wann beginnt der Kurs?",
                    "Am Mittwoch, den 10.",
                    "Am Montag, den 8.",
                    "Am Mittwoch, den 3.",
                ),
            ),
            (
                "Ansage",
                "Liebe Kunden, ab Montag ist unsere Post auch am Samstag von neun bis vierzehn Uhr offen.",
                (
                    "Was ist neu?",
                    "Die Post ist auch am Samstag offen.",
                    "Die Post ist am Montag geschlossen.",
                    "Briefe kosten mehr.",
                ),
            ),
            (
                "Ansage",
                "Sie lernen Deutsch? Hören Sie jeden Tag zehn Minuten Radio oder sehen Sie "
                "Serien auf Deutsch. So lernen Sie viele neue Wörter.",
                (
                    "Was empfiehlt das Radio?",
                    "Jeden Tag Radio hören",
                    "Viel Grammatik üben",
                    "Einen Kurs machen",
                ),
            ),
        ],
        (
            [
                ("Frau", "Mehmet, wie lernst du zu Hause?"),
                (
                    "Mann",
                    "Ich habe einen Plan! Am Montag lerne ich immer Vokabeln, zwanzig neue Wörter.",
                ),
                ("Frau", "Gut. Und am Dienstag?"),
                (
                    "Mann",
                    "Am Dienstag treffe ich meine Freundin Julia. Wir sprechen eine Stunde Deutsch und eine Stunde Türkisch.",
                ),
                ("Frau", "Toll. Und am Mittwoch?"),
                (
                    "Mann",
                    "Am Mittwoch habe ich den Kurs hier bei Ihnen. Da mache ich sonst nichts.",
                ),
                ("Frau", "Und am Donnerstag?"),
                ("Mann", "Donnerstag ist mein Grammatiktag. Ich mache die Übungen aus dem Buch."),
                ("Frau", "Und am Freitag?"),
                (
                    "Mann",
                    "Am Freitag sehe ich eine deutsche Serie. Bücher lesen ist mir noch zu schwer.",
                ),
            ],
            {
                "a": "Vokabeln lernen",
                "b": "Grammatik üben",
                "c": "Radio hören",
                "d": "eine Serie sehen",
                "e": "mit einer Freundin sprechen",
                "f": "Briefe schreiben",
                "g": "Bücher lesen",
                "h": "in den Kurs gehen",
            },
            [
                ("Montag", "a"),
                ("Dienstag", "e"),
                ("Mittwoch", "h"),
                ("Donnerstag", "b"),
                ("Freitag", "d"),
            ],
        ),
        [
            (
                [
                    ("Frau", "Was kostet ein Brief nach Spanien?"),
                    ("Mann", "Ein Euro zehn."),
                ],
                ("Was kostet der Brief?", "1,10 Euro", "1,00 Euro", "0,95 Euro"),
            ),
            (
                [
                    ("Mann", "Hast du gestern den Film gesehen?"),
                    (
                        "Frau",
                        "Nein, ich habe ihn verpasst. Aber ich sehe ihn heute in der Mediathek.",
                    ),
                ],
                ("Wann sieht die Frau den Film?", "Heute", "Gestern", "Am Wochenende"),
            ),
            (
                [
                    ("Frau", "Wie hast du so gut Deutsch gelernt?"),
                    ("Mann", "Mit Musik! Ich habe viele deutsche Lieder gehört und mitgesungen."),
                ],
                (
                    "Wie hat der Mann Deutsch gelernt?",
                    "Mit Liedern",
                    "Mit einem Kurs",
                    "Mit Büchern",
                ),
            ),
            (
                [
                    ("Mann", "Ist das Paket für mich?"),
                    ("Frau", "Nein, für Frau Kraus im dritten Stock. Ich bringe es ihr."),
                ],
                ("Für wen ist das Paket?", "Für Frau Kraus", "Für den Mann", "Für die Frau selbst"),
            ),
            (
                [
                    ("Frau", "Kannst du den Fernseher leiser machen?"),
                    ("Mann", "Klar. Wo ist denn die Fernbedienung?"),
                    ("Frau", "Auf dem Sofa, unter dem Kissen."),
                ],
                (
                    "Wo ist die Fernbedienung?",
                    "Unter dem Kissen",
                    "Auf dem Tisch",
                    "Neben dem Fernseher",
                ),
            ),
        ],
        (
            [
                (
                    "Ansage",
                    "Frau Novak, Sie unterrichten seit zwanzig Jahren Deutsch. Was ist für Ihre Schüler am schwierigsten?",
                ),
                (
                    "Frau",
                    "Die Aussprache, besonders die Wörter mit „ch“. Und natürlich die Artikel: der, die, das!",
                ),
                ("Ansage", "Wie lernt man die Artikel am besten?"),
                (
                    "Frau",
                    "Immer das Wort mit dem Artikel lernen. Und mit Farben: blau für der, rot für die, grün für das.",
                ),
                ("Ansage", "Sind Ihre Schüler heute anders als früher?"),
                (
                    "Frau",
                    "Ja! Früher hatten alle Wörterbücher aus Papier. Heute haben alle ein Handy.",
                ),
                ("Ansage", "Ist das gut oder schlecht?"),
                (
                    "Frau",
                    "Beides. Das Handy hilft, aber man muss die Wörter auch im Kopf haben.",
                ),
            ],
            [
                ("Frau Novak unterrichtet seit zehn Jahren.", False),
                ("Für viele Schüler ist die Aussprache schwierig.", True),
                ("Sie empfiehlt, die Artikel mit Farben zu lernen.", True),
                ("Früher hatten die Schüler Handys.", False),
                ("Sie findet das Handy nur schlecht.", False),
            ],
        ),
    ),
    # Modul 6 (Lektionen 16-18): the hotel, travel and traffic, weather.
    6: _set(
        6,
        [
            (
                "Ansage",
                "Und jetzt der Verkehr: Auf der A3 zwischen Köln und Frankfurt gibt es zwanzig "
                "Kilometer Stau. Fahren Sie lieber über die A61.",
                (
                    "Wo gibt es Stau?",
                    "Zwischen Köln und Frankfurt",
                    "Zwischen Bonn und Köln",
                    "Auf der A61",
                ),
            ),
            (
                "Frau",
                "Guten Tag, Herr Berg, hier ist das Hotel Bergblick. Ihr Zimmer ist ab vierzehn "
                "Uhr frei. Das Frühstück gibt es von sieben bis zehn Uhr. Parken können Sie in "
                "unserer Garage.",
                ("Ab wann ist das Zimmer frei?", "Ab 14 Uhr", "Ab 10 Uhr", "Ab 12 Uhr"),
            ),
            (
                "Ansage",
                "Achtung am Gleis sieben: Der Zug nach Hamburg, Abfahrt zehn Uhr zwölf, fährt "
                "heute von Gleis neun.",
                ("Von welchem Gleis fährt der Zug heute?", "Gleis 9", "Gleis 7", "Gleis 12"),
            ),
            (
                "Ansage",
                "Die Wettervorhersage für das Wochenende: Am Samstag regnet es fast überall. Am "
                "Sonntag scheint wieder die Sonne, und es wird bis zu fünfundzwanzig Grad warm.",
                ("Wie ist das Wetter am Sonntag?", "Sonnig", "Regnerisch", "Stürmisch"),
            ),
            (
                "Mann",
                "Hallo Jana, hier ist Mehmet. Wir hatten eine Reifenpanne auf der Autobahn! Wir "
                "kommen erst um neun Uhr an. Wartet nicht mit dem Essen!",
                (
                    "Warum kommt Mehmet später?",
                    "Er hatte eine Reifenpanne.",
                    "Er steht im Stau.",
                    "Sein Zug ist zu spät.",
                ),
            ),
        ],
        (
            [
                ("Frau", "Und, wie war eure Reise an die Ostsee?"),
                ("Mann", "Toll! Am Montag sind wir mit der Fähre auf eine kleine Insel gefahren."),
                ("Frau", "Schön! Und am Dienstag?"),
                (
                    "Mann",
                    "Am Dienstag hat es den ganzen Tag geregnet. Wir waren im Hotel in der Sauna.",
                ),
                ("Frau", "Und am Mittwoch?"),
                (
                    "Mann",
                    "Am Mittwoch sind wir an der Küste gewandert. Zwanzig Kilometer! Die Kinder waren sehr müde.",
                ),
                ("Frau", "Und am Donnerstag wart ihr am Strand?"),
                (
                    "Mann",
                    "Nein, am Strand waren wir erst am Freitag. Am Donnerstag haben wir Rostock besichtigt.",
                ),
            ],
            {
                "a": "ins Museum gehen",
                "b": "an der Küste wandern",
                "c": "in die Sauna gehen",
                "d": "eine Stadt besichtigen",
                "e": "mit der Fähre fahren",
                "f": "am Strand liegen",
                "g": "Fahrrad fahren",
                "h": "in die Berge fahren",
            },
            [
                ("Montag", "e"),
                ("Dienstag", "c"),
                ("Mittwoch", "b"),
                ("Donnerstag", "d"),
                ("Freitag", "f"),
            ],
        ),
        [
            (
                [
                    ("Mann", "Haben Sie noch ein Doppelzimmer frei?"),
                    (
                        "Frau",
                        "Leider nein, wir sind ausgebucht. Aber wir haben noch ein Einzelzimmer.",
                    ),
                ],
                ("Was ist noch frei?", "Ein Einzelzimmer", "Ein Doppelzimmer", "Nichts"),
            ),
            (
                [
                    ("Frau", "Wie lange dauert die Fahrt nach Prag?"),
                    ("Mann", "Mit dem Auto fünf Stunden, mit dem Zug sechs."),
                ],
                (
                    "Wie lange dauert die Fahrt mit dem Zug?",
                    "Sechs Stunden",
                    "Fünf Stunden",
                    "Vier Stunden",
                ),
            ),
            (
                [
                    ("Mann", "Wie ist das Wetter bei euch?"),
                    ("Frau", "Furchtbar! Seit drei Tagen regnet es, und es ist total kalt."),
                ],
                ("Wie ist das Wetter bei der Frau?", "Es regnet.", "Es schneit.", "Es ist heiß."),
            ),
            (
                [
                    ("Frau", "Ist das WLAN im Zimmer inklusive?"),
                    ("Mann", "Ja. Das Passwort steht auf Ihrer Zimmerkarte."),
                ],
                (
                    "Wo steht das Passwort?",
                    "Auf der Zimmerkarte",
                    "An der Rezeption",
                    "An der Zimmertür",
                ),
            ),
            (
                [
                    ("Mann", "Wo können wir tanken?"),
                    (
                        "Frau",
                        "Die nächste Tankstelle ist in zehn Kilometern, an der Autobahn bei Ulm.",
                    ),
                ],
                (
                    "Wo ist die nächste Tankstelle?",
                    "In zehn Kilometern",
                    "In zwei Kilometern",
                    "In Ulm im Zentrum",
                ),
            ),
        ],
        (
            [
                (
                    "Ansage",
                    "Herr Wolf, Sie machen jeden Abend die Wettervorhersage im Fernsehen. Wann fängt Ihr Tag an?",
                ),
                ("Mann", "Um sechs Uhr. Zuerst sehe ich mir die Wetterkarten von der Nacht an."),
                ("Ansage", "Ist Ihre Vorhersage oft falsch?"),
                (
                    "Mann",
                    "Für morgen fast nie. Aber eine Vorhersage für zehn Tage ist sehr schwierig.",
                ),
                ("Ansage", "Was ist Ihr Lieblingswetter?"),
                (
                    "Mann",
                    "Ich liebe Gewitter! Viele Menschen haben Angst davor, aber ich finde sie spannend.",
                ),
                ("Ansage", "Und wohin fahren Sie im Urlaub?"),
                (
                    "Mann",
                    "Nach Norwegen. Da ist es auch im Sommer kühl, und das Wetter ist jede Stunde anders.",
                ),
            ],
            [
                ("Herr Wolf beginnt um sechs Uhr mit der Arbeit.", True),
                ("Die Vorhersage für morgen ist oft falsch.", False),
                ("Er findet Gewitter spannend.", True),
                ("Er hat Angst vor Gewittern.", False),
                ("Im Urlaub fährt er in ein warmes Land.", False),
            ],
        ),
    ),
    # Modul 7 (Lektionen 19-21): culture, books and the press, offices and crime.
    7: _set(
        7,
        [
            (
                "Ansage",
                "Am Samstag liest die Autorin Marie Lenz in der Stadtbibliothek aus ihrem neuen "
                "Roman. Beginn ist um neunzehn Uhr, der Eintritt kostet fünf Euro.",
                ("Was kostet der Eintritt?", "5 Euro", "9 Euro", "Nichts"),
            ),
            (
                "Frau",
                "Guten Tag, hier ist das Fundbüro der Stadt. Wir haben Ihre Geldbörse. Bitte "
                "bringen Sie Ihren Ausweis mit, wenn Sie sie abholen.",
                ("Was muss man mitbringen?", "Den Ausweis", "Die EC-Karte", "Geld"),
            ),
            (
                "Ansage",
                "Liebe Besucher, die Vorstellung beginnt in fünf Minuten. Bitte schalten Sie "
                "jetzt Ihre Handys aus.",
                (
                    "Was sollen die Besucher machen?",
                    "Die Handys ausschalten",
                    "Die Karten zeigen",
                    "Pünktlich kommen",
                ),
            ),
            (
                "Mann",
                "Guten Tag, Frau Petrova, hier ist das Bürgeramt. Ihr neuer Reisepass ist "
                "fertig. Sie können ihn von Montag bis Freitag zwischen acht und zwölf Uhr abholen.",
                (
                    "Wann kann man den Pass abholen?",
                    "Montag bis Freitag am Vormittag",
                    "Jeden Tag bis 18 Uhr",
                    "Nur am Samstag",
                ),
            ),
            (
                "Ansage",
                "Die Polizei sucht Zeugen: Gestern Abend gab es in der Goethestraße einen "
                "Einbruch in ein Geschäft. Haben Sie etwas gesehen? Bitte rufen Sie die Polizei an.",
                (
                    "Wo war der Einbruch?",
                    "In der Goethestraße",
                    "In der Bahnhofstraße",
                    "Im Museum",
                ),
            ),
        ],
        (
            [
                (
                    "Mann",
                    "Lisa, was machen wir nächste Woche? Ich habe den Veranstaltungskalender hier.",
                ),
                (
                    "Frau",
                    "Zeig mal! Am Montag gibt es eine Lesung in der Buchhandlung. Da möchte ich gern hin.",
                ),
                ("Mann", "Okay. Am Dienstag ist Kabarett im Keller. Hast du Lust?"),
                ("Frau", "Ja, gern! Am Mittwoch kann ich nicht, da arbeite ich lange."),
                (
                    "Mann",
                    "Dann Donnerstag: Da kommt der Zirkus in die Stadt! Gehen wir mit deinen Kindern hin?",
                ),
                ("Frau", "Super Idee! Und am Freitag?"),
                (
                    "Mann",
                    "Am Freitag wollte ich zum Konzert im Park, aber das ist schon ausverkauft. Gehen wir ins Kino?",
                ),
                ("Frau", "Gern. Und am Samstag gehe ich mit meinem Vater ins Museum."),
            ],
            {
                "a": "in den Zirkus",
                "b": "ins Kabarett",
                "c": "zu einer Lesung",
                "d": "in die Oper",
                "e": "ins Kino",
                "f": "zu einer Comedy-Show",
                "g": "ins Museum",
                "h": "zu einem Konzert",
            },
            [
                ("Montag", "c"),
                ("Dienstag", "b"),
                ("Donnerstag", "a"),
                ("Freitag", "e"),
                ("Samstag", "g"),
            ],
        ),
        [
            (
                [
                    ("Frau", "Ich habe meinen Ausweis verloren. Was muss ich machen?"),
                    ("Mann", "Gehen Sie zum Bürgeramt. Dort bekommen Sie einen neuen."),
                ],
                ("Wohin soll die Frau gehen?", "Zum Bürgeramt", "Zur Polizei", "Zum Fundbüro"),
            ),
            (
                [
                    ("Mann", "Liest du lieber Romane oder Zeitungen?"),
                    (
                        "Frau",
                        "Zeitungen lese ich nur im Internet. Aber abends lese ich gern einen Krimi.",
                    ),
                ],
                ("Was liest die Frau abends?", "Einen Krimi", "Die Zeitung", "Gedichte"),
            ),
            (
                [
                    ("Frau", "Wie war die Aufführung?"),
                    (
                        "Mann",
                        "Die Schauspieler waren toll, aber das Stück war viel zu lang. Drei Stunden!",
                    ),
                ],
                (
                    "Was hat dem Mann nicht gefallen?",
                    "Das Stück war zu lang.",
                    "Die Schauspieler waren schlecht.",
                    "Sein Platz war schlecht.",
                ),
            ),
            (
                [
                    ("Mann", "Hast du schon Karten für den Zirkus?"),
                    ("Frau", "Nein. An der Kasse gibt es nur noch Karten für Sonntag."),
                ],
                ("Für wann gibt es noch Karten?", "Für Sonntag", "Für Samstag", "Für heute"),
            ),
            (
                [
                    ("Frau", "Was ist denn passiert?"),
                    ("Mann", "Jemand hat mein Fahrrad gestohlen! Es stand direkt vor dem Bahnhof."),
                ],
                ("Wo war das Fahrrad?", "Vor dem Bahnhof", "Vor dem Haus", "Im Keller"),
            ),
        ],
        (
            [
                (
                    "Ansage",
                    "Frau Schulz, Sie haben seit dreißig Jahren eine Buchhandlung. Lesen die Leute heute weniger?",
                ),
                (
                    "Frau",
                    "Nein, das glaube ich nicht. Aber sie lesen anders. Viele lesen auch auf dem Handy.",
                ),
                ("Ansage", "Was verkaufen Sie am meisten?"),
                (
                    "Frau",
                    "Krimis! Und Kinderbücher. Bilderbücher für die Kleinen verkaufe ich sehr viel.",
                ),
                ("Ansage", "Gibt es bei Ihnen auch Veranstaltungen?"),
                (
                    "Frau",
                    "Ja, einmal im Monat gibt es eine Lesung. Dann kommen bis zu sechzig Leute.",
                ),
                ("Ansage", "Und welches Buch lesen Sie gerade?"),
                (
                    "Frau",
                    "Einen Roman aus Italien. Ich lese ihn auf Italienisch, das ist mein Hobby.",
                ),
            ],
            [
                ("Die Buchhandlung gibt es seit dreißig Jahren.", True),
                ("Frau Schulz glaubt, die Leute lesen heute weniger.", False),
                ("Sie verkauft viele Krimis.", True),
                ("Jede Woche gibt es eine Lesung.", False),
                ("Sie liest gerade einen Roman auf Deutsch.", False),
            ],
        ),
    ),
    # Modul 8 (Lektionen 22-24): mobility and the environment, jobs, living abroad.
    8: _set(
        8,
        [
            (
                "Ansage",
                "Ab Montag gibt es in der Innenstadt zwanzig neue Elektroautos für Carsharing. "
                "Die Mitglieder können sie ganz einfach mit dem Handy buchen.",
                ("Wie bucht man die Autos?", "Mit dem Handy", "Im Büro", "Am Telefon"),
            ),
            (
                "Frau",
                "Guten Tag, Herr Arslan, hier ist Frau Schmidt vom Hotel Adler. Vielen Dank für "
                "Ihre Bewerbung. Wir möchten Sie gern zu einem Vorstellungsgespräch einladen: am "
                "Dienstag um zehn Uhr.",
                (
                    "Wann ist das Vorstellungsgespräch?",
                    "Am Dienstag um 10 Uhr",
                    "Am Donnerstag um 10 Uhr",
                    "Am Dienstag um 12 Uhr",
                ),
            ),
            (
                "Ansage",
                "Liebe Fahrgäste, heute fährt die S-Bahn nur bis zum Hauptbahnhof. Dort steigen "
                "Sie bitte in den Bus um.",
                (
                    "Was müssen die Fahrgäste machen?",
                    "Am Hauptbahnhof in den Bus umsteigen",
                    "Ein Taxi nehmen",
                    "Zu Fuß gehen",
                ),
            ),
            (
                "Mann",
                "Hallo Mama, hier ist Lukas aus Lissabon. Mir geht es gut! Die Gastfamilie ist "
                "super nett. Nur das Essen ist ungewohnt: Es gibt jeden Tag Fisch. Ich rufe am "
                "Wochenende wieder an.",
                ("Was ist für Lukas ungewohnt?", "Das Essen", "Die Gastfamilie", "Die Sprache"),
            ),
            (
                "Ansage",
                "Die Berufsschule informiert: Der Infotag für Azubis ist am Samstag von zehn bis "
                "vierzehn Uhr. Bitte bringen Sie Ihren Lebenslauf mit.",
                ("Was soll man mitbringen?", "Den Lebenslauf", "Ein Foto", "Den Ausweis"),
            ),
        ],
        (
            [
                (
                    "Frau",
                    "Wir schreiben einen Artikel für die Firmenzeitung: Wie kommen unsere Kollegen zur Arbeit?",
                ),
                ("Mann", "Herr Klein hat seinen Wagen verkauft. Er nimmt jetzt das Carsharing."),
                ("Frau", "Interessant! Und Frau Yilmaz?"),
                ("Mann", "Sie wohnt in Bonn und kommt jeden Tag mit dem Zug."),
                ("Frau", "Und Tim aus der Produktion?"),
                ("Mann", "Tim fährt Fahrrad, auch im Winter! Früher ist er Motorrad gefahren."),
                ("Frau", "Und Sabine?"),
                ("Mann", "Sabine wohnt gleich um die Ecke. Sie geht zu Fuß."),
                ("Frau", "Und der Chef, Herr Roth?"),
                ("Mann", "Der hat seit Mai ein Elektroauto. Er ist sehr stolz darauf."),
            ],
            {
                "a": "mit dem Elektroauto",
                "b": "mit dem Fahrrad",
                "c": "mit dem Carsharing",
                "d": "mit dem Bus",
                "e": "mit dem Zug",
                "f": "zu Fuß",
                "g": "mit dem Motorrad",
                "h": "mit dem Taxi",
            },
            [
                ("Herr Klein", "c"),
                ("Frau Yilmaz", "e"),
                ("Tim", "b"),
                ("Sabine", "f"),
                ("Herr Roth", "a"),
            ],
        ),
        [
            (
                [
                    ("Mann", "Was machst du nach der Schule?"),
                    ("Frau", "Ich mache eine Ausbildung als Köchin. Studieren möchte ich nicht."),
                ],
                (
                    "Was macht die Frau nach der Schule?",
                    "Eine Ausbildung",
                    "Ein Studium",
                    "Ein Jahr im Ausland",
                ),
            ),
            (
                [
                    ("Frau", "Wie war dein Auslandssemester?"),
                    (
                        "Mann",
                        "Super! Am Anfang hatte ich Heimweh, aber dann habe ich viele Freunde gefunden.",
                    ),
                ],
                ("Was war am Anfang schwierig?", "Er hatte Heimweh.", "Die Sprache", "Das Wetter"),
            ),
            (
                [
                    ("Mann", "Wie lange arbeitest du am Tag?"),
                    ("Frau", "Acht Stunden, von acht bis siebzehn Uhr, mit einer Stunde Pause."),
                ],
                ("Wann hat die Frau Feierabend?", "Um 17 Uhr", "Um 16 Uhr", "Um 18 Uhr"),
            ),
            (
                [
                    ("Frau", "Warum hast du gekündigt?"),
                    ("Mann", "Das Gehalt war okay, aber ich hatte keine Zeit für meine Familie."),
                ],
                (
                    "Warum hat der Mann gekündigt?",
                    "Er hatte keine Zeit für die Familie.",
                    "Er hat zu wenig verdient.",
                    "Der Chef war unfreundlich.",
                ),
            ),
            (
                [
                    ("Mann", "Hast du dich schon eingeloggt?"),
                    ("Frau", "Nein, ich habe mein Passwort vergessen!"),
                ],
                (
                    "Was ist das Problem?",
                    "Die Frau hat ihr Passwort vergessen.",
                    "Der Computer ist kaputt.",
                    "Das Internet funktioniert nicht.",
                ),
            ),
        ],
        (
            [
                (
                    "Ansage",
                    "Herr Becker, Sie haben zwei Jahre in Japan gearbeitet. Wie war der Anfang?",
                ),
                (
                    "Mann",
                    "Schwierig! Ich konnte kein Wort Japanisch. In den ersten Wochen habe ich mich oft verirrt.",
                ),
                ("Ansage", "Was war im Alltag anders?"),
                (
                    "Mann",
                    "Alles ist sehr pünktlich. Die Züge kommen auf die Minute genau. Und im Büro arbeiten alle sehr lange.",
                ),
                ("Ansage", "Haben Sie sich dort wohlgefühlt?"),
                ("Mann", "Nach einem halben Jahr ja. Meine Kollegen haben mir viel geholfen."),
                ("Ansage", "Und jetzt sind Sie wieder in Deutschland?"),
                ("Mann", "Ja, seit März. Aber das japanische Essen fehlt mir sehr!"),
            ],
            [
                ("Herr Becker konnte am Anfang gut Japanisch.", False),
                ("In Japan sind die Züge pünktlich.", True),
                ("Im Büro arbeiten die Kollegen nur kurz.", False),
                ("Nach einem halben Jahr hat er sich wohlgefühlt.", True),
                ("Er ist seit März wieder in Deutschland.", True),
            ],
        ),
    ),
}
