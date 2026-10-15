"""Modul 5 (A2.2): Lektion 13 (Meine erste „Deutschlehrerin“), 14 (Es werden
fleißig Päckchen gepackt.), 15 (Gleich geht's los!)."""

from ..dsl import (
    bank,
    conj,
    fill,
    grammar,
    lesson,
    match,
    mc,
    order,
    review,
    rule,
    sections,
    tr,
    unit,
    vocab_lessons,
)

# ============================================================================
# Lektion 13: Meine erste „Deutschlehrerin“
# ============================================================================

L13_WORDS = [
    ("the German course", "der Deutschkurs", "noun", "Pl. die Deutschkurse"),
    ("the language course", "der Sprachkurs", "noun", "Pl. die Sprachkurse"),
    ("the language school", "die Sprachschule", "noun", "Pl. die Sprachschulen"),
    ("the lessons / teaching", "der Unterricht", "noun"),
    ("the grammar", "die Grammatik", "noun"),
    ("the pronunciation", "die Aussprache", "noun"),
    ("the mistake", "der Fehler", "noun", "Pl. die Fehler"),
    ("the exercise", "die Übung", "noun", "Pl. die Übungen"),
    ("the dictionary", "das Wörterbuch", "noun", "Pl. die Wörterbücher"),
    ("the word", "das Wort", "noun", "Pl. die Wörter"),
    ("the vocabulary word", "die Vokabel", "noun", "Pl. die Vokabeln"),
    ("the dialect", "der Dialekt", "noun", "Pl. die Dialekte"),
    ("the difference", "der Unterschied", "noun", "Pl. die Unterschiede"),
    ("the learner", "der Lernende", "noun", "Pl. die Lernenden"),
    ("to repeat", "wiederholen", "verb", "hat wiederholt"),
    ("to practise", "üben", "verb", "hat geübt"),
    ("to remember / memorise", "merken", "verb", "sich etwas merken"),
    ("to correct", "korrigieren", "verb", "hat korrigiert"),
    ("to translate", "übersetzen", "verb", "hat übersetzt"),
    ("to explain", "erklären", "verb", "hat erklärt"),
    ("patient", "geduldig", "adjective"),
    ("strict", "streng", "adjective"),
    ("helpful", "hilfreich", "adjective"),
    ("difficult", "schwierig", "adjective"),
    ("polite", "höflich", "adjective"),
    ("possible", "möglich", "adjective"),
    ("perfect", "perfekt", "adjective"),
    ("That helped me.", "Das hat mir geholfen.", "phrase"),
    ("I found the course ...", "Ich fand den Kurs ...", "phrase"),
]

L13_RULES = [
    rule(
        "als: einmal in der Vergangenheit",
        "sentence_structure",
        """
**als** (when) introduces **one** event or period in the past. The verb goes to
the end, and the main clause starts with its verb:

- ***Als** ich zehn Jahre alt **war**, **habe** ich Englisch gelernt.*
- ***Als** ich nach Berlin gezogen **bin**, **habe** ich kein Wort verstanden.*
- *Ich war sehr nervös, **als** ich meine erste Prüfung **hatte**.*

| als | wenn |
|---|---|
| one time in the past | every time, or present / future |
| *Als ich Kind war, ...* | *Wenn ich Zeit habe, lerne ich Vokabeln.* |
| | *Immer wenn ich einen Fehler gemacht habe, ...* (repeated, past) |
""",
        [
            "Als ich in die Schule kam, war meine Lehrerin sehr streng.",
            "Als wir in Wien waren, haben wir viel Dialekt gehört.",
            "Wenn ich einen Fehler mache, korrigiert mich die Lehrerin.",
        ],
    ),
    rule(
        "Adjektive auf -ig und -lich",
        "adjectives",
        """
Many adjectives are built from nouns with **-ig** or **-lich**:

| noun | adjective |
|---|---|
| die Geduld | geduld**ig** (patient) |
| die Lust | lust**ig** (funny) |
| die Schwierigkeit (difficulty) | schwier**ig** |
| der Freund | freund**lich** (friendly) |
| die Hilfe | hilf**reich** / hilf**sbereit** |
| der Tag | täg**lich** (daily) |

**-lich** often adds an umlaut: *der Tag → täglich*, *die Gefahr → gefährlich*.
Pronunciation: *-ig* at the end sounds like *-ich* in standard German.

Many have an opposite with **un-**: *freundlich → unfreundlich, möglich →
unmöglich, höflich → unhöflich*.
""",
        [
            "Meine erste Lehrerin war sehr geduldig.",
            "Wir haben täglich Vokabeln geübt.",
            "Das ist leider unmöglich.",
        ],
    ),
]

L13_LESSONS = [
    lesson(
        "Deutsch lernen",
        review("die Aussprache"),
        review("der Fehler"),
        match(
            [
                ("das Wörterbuch", "the dictionary"),
                ("die Übung", "the exercise"),
                ("die Grammatik", "the grammar"),
                ("der Unterschied", "the difference"),
                ("die Vokabel", "the vocabulary word"),
            ]
        ),
        mc(
            "Die Lehrerin erklärt alles dreimal und wird nie böse. Sie ist ...",
            "geduldig.",
            "streng.",
            "schwierig.",
        ),
        mc(
            "In Bayern spricht man oft ...",
            "Dialekt.",
            "Grammatik.",
            "Wörterbuch.",
        ),
        fill("Kannst du das bitte ___? Ich habe es nicht verstanden. (repeat)", "wiederholen"),
        fill("Die Lehrerin hat meine Fehler ___. (korrigieren)", "korrigiert"),
        tr("That helped me.", "Das hat mir geholfen."),
    ),
    lesson(
        "Als ich klein war ...",
        grammar("als: einmal in der Vergangenheit"),
        mc(
            "Which sentence is correct?",
            "Als ich zehn war, habe ich Englisch gelernt.",
            "Als ich zehn war, ich habe Englisch gelernt.",
            "Als war ich zehn, habe ich Englisch gelernt.",
        ),
        mc(
            "___ ich nach Deutschland gekommen bin, habe ich kein Deutsch verstanden.",
            "Als",
            "Wenn",
            "Wann",
        ),
        mc("___ ich Zeit habe, lerne ich Vokabeln.", "Wenn", "Als", "Wann"),
        mc("___ beginnt der Kurs?", "Wann", "Als", "Wenn"),
        fill("Als ich in der Schule ___, war ich sehr fleißig. (sein)", "war"),
        fill("Ich war nervös, als ich meine erste Prüfung ___. (haben)", "hatte"),
        order("Als wir in Wien waren, haben wir viel Dialekt gehört."),
        tr(
            "When I was young, I learned French.",
            "Als ich jung war, habe ich Französisch gelernt.",
        ),
    ),
    lesson(
        "geduldig und freundlich",
        grammar("Adjektive auf -ig und -lich"),
        match(
            [
                ("die Geduld", "geduldig"),
                ("der Tag", "täglich"),
                ("die Hilfe", "hilfreich"),
                ("die Lust", "lustig"),
                ("der Freund", "freundlich"),
            ],
            "Noun and adjective",
        ),
        mc("möglich ↔ ...", "unmöglich", "nichtmöglich", "möglos"),
        mc("Er sagt nie bitte und danke. Er ist ...", "unhöflich.", "höflich.", "geduldig."),
        fill("Wir haben ___ eine Stunde geübt. (daily)", "täglich"),
        fill("Diese Übung ist sehr ___. Ich verstehe sie nicht. (difficult)", "schwierig"),
        fill("Der Lehrer war ___, aber fair. (strict)", "streng"),
        tr(
            "My first teacher was very patient.",
            "Meine erste Lehrerin war sehr geduldig.|Mein erster Lehrer war sehr geduldig.",
        ),
    ),
    lesson(
        "Meine erste Deutschlehrerin",
        bank(
            "Als ich 2015 nach Hamburg gezogen ___, habe ich nur drei Wörter verstanden. Meine erste "
            "Lehrerin war meine Nachbarin, Frau Peters. Sie war sehr ___ und hat mir jeden "
            "Tag neue ___ erklärt. Wenn ich einen ___ gemacht habe, hat sie mich freundlich "
            "korrigiert. Am Anfang war die ___ schwierig, aber Frau Peters hat mir sehr ___.",
            ["bin", "geduldig", "Wörter", "Fehler", "Aussprache", "geholfen"],
            "streng",
            "Wörterbuch",
        ),
        mc(
            "Who was the writer's first German teacher?",
            "The neighbour.",
            "A teacher at a language school.",
            "A colleague.",
        ),
        mc(
            "What was difficult at the beginning?",
            "The pronunciation.",
            "The grammar.",
            "The neighbour.",
        ),
        fill("Ich ___ mir neue Wörter mit Karten. (merken)", "merke"),
        fill("Kannst du mir diesen Satz ___? (translate)", "übersetzen"),
        tr("I found the course very helpful.", "Ich fand den Kurs sehr hilfreich."),
    ),
    lesson(
        "Lerntipps",
        mc(
            "Was hilft beim Vokabellernen?",
            "Jeden Tag ein paar Wörter wiederholen.",
            "Nie ein Wörterbuch benutzen.",
            "Nur einmal im Monat üben.",
        ),
        mc(
            "Ich habe keinen Fehler gemacht. Mein Test war ...",
            "perfekt.",
            "unmöglich.",
            "schwierig.",
        ),
        fill("Die Lehrerin ___ die Grammatik sehr gut. (erklären)", "erklärt"),
        fill("Wir müssen mehr ___. (practise)", "üben"),
        order("Wenn ich einen Fehler mache, korrigiert mich die Lehrerin."),
        tr("We go to a language school.", "Wir gehen in eine Sprachschule."),
    ),
    lesson(
        "Lektion 13: Test",
        mc("___ ich Kind war, habe ich viel gelesen.", "Als", "Wenn"),
        fill("Als ich nach Berlin kam, ___ ich 20 Jahre alt. (sein)", "war"),
        mc("die Hilfe → ...", "hilfreich", "hilflich"),
        fill("Das ist leider ___. (impossible)", "unmöglich"),
        fill("Kannst du das bitte ___? (explain)", "erklären"),
        order("Meine Lehrerin hat mich oft korrigiert."),
        tr("The pronunciation is difficult.", "Die Aussprache ist schwierig."),
    ),
]

LEKTION_13 = unit(
    13,
    "Meine erste „Deutschlehrerin“",
    "Sprachen lernen",
    L13_WORDS,
    L13_RULES,
    sections(L13_LESSONS, vocab_lessons(L13_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 14: Es werden fleißig Päckchen gepackt.
# ============================================================================

L14_WORDS = [
    ("the small parcel", "das Päckchen", "noun", "Pl. die Päckchen"),
    ("the parcel", "das Paket", "noun", "Pl. die Pakete"),
    ("the postcard", "die Postkarte", "noun", "Pl. die Postkarten"),
    ("the letterbox", "der Briefkasten", "noun", "Pl. die Briefkästen"),
    ("the envelope", "der Umschlag", "noun", "Pl. die Umschläge"),
    ("the address", "die Adresse", "noun", "Pl. die Adressen"),
    ("the sender", "der Absender", "noun", "f. die Absenderin"),
    ("the recipient", "der Empfänger", "noun", "f. die Empfängerin"),
    ("the delivery", "die Lieferung", "noun", "Pl. die Lieferungen"),
    ("the wrapping paper", "das Geschenkpapier", "noun"),
    ("the sticky tape", "das Klebeband", "noun"),
    ("the scissors", "die Schere", "noun", "Pl. die Scheren"),
    ("the cardboard box", "der Karton", "noun", "Pl. die Kartons"),
    ("the contents", "der Inhalt", "noun"),
    ("the instructions for use", "die Gebrauchsanweisung", "noun", "Pl. die Gebrauchsanweisungen"),
    ("the news report", "die Meldung", "noun", "Pl. die Meldungen"),
    ("the phone call", "der Anruf", "noun", "Pl. die Anrufe"),
    ("the greeting (in a letter)", "die Anrede", "noun", "Liebe Anna, ..."),
    ("to pack", "packen", "verb", "hat gepackt"),
    ("to wrap", "einpacken", "verb", "hat eingepackt"),
    ("to send", "verschicken", "verb", "hat verschickt"),
    ("to send off", "abschicken", "verb", "hat abgeschickt"),
    ("to send back", "zurückschicken", "verb", "hat zurückgeschickt"),
    ("to open", "öffnen", "verb", "hat geöffnet"),
    ("to close", "schließen", "verb", "hat geschlossen"),
    ("to sign", "unterschreiben", "verb", "hat unterschrieben"),
    ("to fill in", "ausfüllen", "verb", "hat ausgefüllt"),
    ("to sort", "sortieren", "verb", "hat sortiert"),
    ("to call back", "zurückrufen", "verb", "hat zurückgerufen"),
    ("to connect / put through", "verbinden", "verb", "hat verbunden"),
    ("engaged (phone)", "besetzt", "adjective"),
    ("reachable", "erreichbar", "adjective"),
    ("It's nice that you thought of me.", "Schön, dass du an mich gedacht hast.", "phrase"),
    ("That's really kind of you.", "Das ist wirklich lieb von dir.", "phrase"),
]

L14_RULES = [
    rule(
        "Passiv Präsens: werden + Partizip",
        "verbs",
        """
The **passive** puts the **action** first, not the person doing it:
**werden** + Partizip II at the end.

| werden | example |
|---|---|
| ich werde | *Ich werde abgeholt.* |
| du wirst | *Du wirst angerufen.* |
| er / sie / es **wird** | *Das Päckchen **wird** gepackt.* |
| wir / sie **werden** | *Die Päckchen **werden** gepackt.* |
| ihr werdet | *Ihr werdet gefragt.* |

Active → passive: the accusative object becomes the subject.

- Aktiv: *Die Post **verschickt** die Briefe.*
- Passiv: *Die Briefe **werden** (von der Post) **verschickt**.*

Who does it, if needed: **von + Dativ**. Often it's left out.
""",
        [
            "Es werden fleißig Päckchen gepackt.",
            "Das Paket wird morgen geliefert.",
            "Die Briefe werden am Morgen sortiert.",
        ],
    ),
    rule(
        "Briefe schreiben: Anrede und Gruß",
        "other",
        """
A personal letter or e-mail:

| | to friends (du) | formal (Sie) |
|---|---|---|
| Anrede | *Liebe Anna, / Lieber Tim,* | *Sehr geehrte Frau Roth, / Sehr geehrter Herr Kaya,* |
| Dank | *Vielen Dank für das Päckchen!* | *Vielen Dank für Ihre Nachricht.* |
| Gruß | *Viele Grüße / Liebe Grüße, dein Paul* | *Mit freundlichen Grüßen, Paul Weber* |

- After the comma in the Anrede, the next line starts with a **small** letter.
- *Liebe* for women, *Lieber* for men, *Liebe* + plural.
""",
        [
            "Liebe Oma, vielen Dank für das schöne Päckchen!",
            "Ich habe mich sehr darüber gefreut.",
            "Liebe Grüße, deine Lena",
        ],
    ),
]

L14_LESSONS = [
    lesson(
        "Post und Pakete",
        review("das Päckchen"),
        review("der Umschlag"),
        match(
            [
                ("der Absender", "the sender"),
                ("der Empfänger", "the recipient"),
                ("die Schere", "the scissors"),
                ("das Klebeband", "the sticky tape"),
                ("der Karton", "the cardboard box"),
            ]
        ),
        mc(
            "Den Brief wirft man in den ...",
            "Briefkasten.",
            "Karton.",
            "Kühlschrank.",
        ),
        mc(
            "Das Telefon ist ___. Jemand spricht gerade.",
            "besetzt",
            "erreichbar",
            "geöffnet",
        ),
        fill("Bitte ___ Sie hier. (sign)", "unterschreiben"),
        fill("Ich habe das Formular schon ___. (ausfüllen)", "ausgefüllt"),
        tr("I'm sending the parcel tomorrow.", "Ich verschicke das Paket morgen."),
    ),
    lesson(
        "Das Päckchen wird gepackt",
        grammar("Passiv Präsens: werden + Partizip"),
        conj("werden", "es", "wird"),
        conj("werden", "sie (they)", "werden"),
        conj("werden", "du", "wirst"),
        fill("Das Paket ___ morgen geliefert.", "wird"),
        fill("Die Briefe ___ am Morgen sortiert.", "werden"),
        fill("Das Geschenk wird schön ___. (einpacken)", "eingepackt"),
        fill("Die Pakete werden heute ___. (verschicken)", "verschickt"),
        mc(
            "Aktiv: Die Post bringt das Paket. Passiv:",
            "Das Paket wird von der Post gebracht.",
            "Das Paket bringt die Post.",
            "Das Paket ist von der Post bringen.",
        ),
        mc(
            "Die Fenster ___ jede Woche geputzt.",
            "werden",
            "wird",
            "werdet",
        ),
        order("Es werden fleißig Päckchen gepackt."),
    ),
    lesson(
        "Aktiv und Passiv",
        mc(
            "Man verschickt die Briefe heute. Passiv:",
            "Die Briefe werden heute verschickt.",
            "Die Briefe verschicken heute.",
            "Die Briefe wird heute verschickt.",
        ),
        mc(
            "Der Briefträger bringt die Post. Passiv:",
            "Die Post wird vom Briefträger gebracht.",
            "Die Post werden vom Briefträger gebracht.",
            "Die Post wird den Briefträger gebracht.",
        ),
        fill("Die Pakete ___ in Kartons gepackt.", "werden"),
        fill("Der Brief wird ___. (öffnen)", "geöffnet"),
        fill("Die Päckchen werden ___ der Post geliefert. (by)", "von"),
        order("Das Paket wird morgen zurückgeschickt."),
        tr("The parcel is being delivered today.", "Das Paket wird heute geliefert."),
        tr("The letters are being sorted.", "Die Briefe werden sortiert."),
    ),
    lesson(
        "Ein Dankesbrief",
        grammar("Briefe schreiben: Anrede und Gruß"),
        bank(
            "___ Oma, vielen ___ für das schöne Päckchen! Ich habe mich sehr darüber ___. "
            "Der Pullover ist toll und passt perfekt. Schön, dass du an mich ___ hast. "
            "Liebe ___, deine Lena",
            ["Liebe", "Dank", "gefreut", "gedacht", "Grüße"],
            "Lieber",
            "Geschenk",
        ),
        mc(
            "A formal letter to Mr Kaya starts:",
            "Sehr geehrter Herr Kaya,",
            "Lieber Herr Kaya,",
            "Hallo Kaya,",
        ),
        mc(
            "A formal letter ends:",
            "Mit freundlichen Grüßen",
            "Liebe Grüße",
            "Tschüs",
        ),
        fill("___ Tim, wie geht es dir? (dear, to a man)", "Lieber"),
        tr("That's really kind of you.", "Das ist wirklich lieb von dir."),
    ),
    lesson(
        "Am Telefon",
        mc(
            "Kann ich Sie mit Frau Lang ___?",
            "verbinden",
            "verschicken",
            "sortieren",
        ),
        mc(
            "Herr Roth ist gerade nicht ___. Rufen Sie später an.",
            "erreichbar",
            "besetzt",
            "geschlossen",
        ),
        fill("Ich rufe Sie morgen ___. (back)", "zurück"),
        fill("Danke für deinen ___! (call)", "Anruf"),
        fill("Ich habe die ___ im Radio gehört. (news report)", "Meldung"),
        tr(
            "Please read the instructions.",
            "Bitte lies die Gebrauchsanweisung.|Bitte lesen Sie die Gebrauchsanweisung.",
        ),
    ),
    lesson(
        "Lektion 14: Test",
        fill("Das Paket ___ heute verschickt.", "wird"),
        fill("Die Pakete werden ___. (packen)", "gepackt"),
        mc("Die Briefe ___ sortiert.", "werden", "wird"),
        mc("Formal letter:", "Sehr geehrte Frau Lang,", "Liebe Frau Lang,"),
        fill("Wie ist Ihre ___? Ich schreibe sie auf das Paket. (address)", "Adresse"),
        order("Das Geschenk wird schön eingepackt."),
        tr("It's nice that you thought of me.", "Schön, dass du an mich gedacht hast."),
    ),
]

LEKTION_14 = unit(
    14,
    "Es werden fleißig Päckchen gepackt.",
    "Post und Passiv",
    L14_WORDS,
    L14_RULES,
    sections(L14_LESSONS, vocab_lessons(L14_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 15: Gleich geht's los!
# ============================================================================

L15_WORDS = [
    ("the media", "die Medien", "noun", "plural; Sg. das Medium"),
    ("the television (medium)", "das Fernsehen", "noun"),
    ("the radio", "das Radio", "noun", "Pl. die Radios"),
    ("the magazine", "die Zeitschrift", "noun", "Pl. die Zeitschriften"),
    ("the programme / broadcast", "die Sendung", "noun", "Pl. die Sendungen"),
    ("the favourite programme", "die Lieblingssendung", "noun"),
    ("the series", "die Serie", "noun", "Pl. die Serien"),
    ("the crime drama", "der Krimi", "noun", "Pl. die Krimis"),
    ("the documentary", "die Dokumentation", "noun", "Pl. die Dokumentationen"),
    ("the advertising", "die Werbung", "noun"),
    ("the remote control", "die Fernbedienung", "noun", "Pl. die Fernbedienungen"),
    ("the online media library", "die Mediathek", "noun", "Pl. die Mediatheken"),
    ("the website", "die Webseite", "noun", "Pl. die Webseiten"),
    ("the channel / broadcaster", "der Sender", "noun", "Pl. die Sender"),
    ("the TV schedule", "das Programm", "noun", "Pl. die Programme"),
    ("the habit", "die Gewohnheit", "noun", "Pl. die Gewohnheiten"),
    ("to switch on", "einschalten", "verb", "hat eingeschaltet"),
    ("to switch off", "ausschalten", "verb", "hat ausgeschaltet"),
    ("to change channels", "umschalten", "verb", "hat umgeschaltet"),
    ("to record", "aufnehmen", "verb", "nimmt auf, hat aufgenommen"),
    ("to download", "herunterladen", "verb", "lädt herunter, hat heruntergeladen"),
    ("to upload", "hochladen", "verb", "hat hochgeladen"),
    ("to miss", "verpassen", "verb", "hat verpasst"),
    ("to broadcast", "ausstrahlen", "verb", "hat ausgestrahlt"),
    ("to inform oneself", "informieren", "verb", "sich informieren"),
    ("to watch", "ansehen", "verb", "sich etwas ansehen"),
    ("informative", "informativ", "adjective"),
    ("several times", "mehrmals", "adverb"),
    ("It's about to start!", "Gleich geht's los!", "phrase"),
]

L15_RULES = [
    rule(
        "Vorsilben: trennbar oder nicht?",
        "verbs",
        """
Some prefixes **split off** and go to the end; others **never** do.

| separable (stressed) | inseparable (unstressed) |
|---|---|
| **ein**schalten: *Ich **schalte** den Fernseher **ein**.* | **ver**passen: *Ich **verpasse** die Sendung.* |
| **aus**schalten: *Schalt das Radio **aus**!* | **be**kommen: *Ich **bekomme** viele E-Mails.* |
| **auf**nehmen: *Ich **nehme** den Krimi **auf**.* | **er**klären: *Er **erklärt** die Fernbedienung.* |
| **um**schalten, **an**sehen, **herunter**laden | **ent**wickeln, **emp**fehlen, **ge**fallen |

Perfekt: separable verbs put **ge** in the middle (*ein**ge**schaltet*),
inseparable verbs have **no ge-** (*verpasst, bekommen, erklärt*).
""",
        [
            "Ich nehme die Serie auf, weil ich keine Zeit habe.",
            "Hast du den Film verpasst?",
            "Ich habe das Video heruntergeladen.",
        ],
    ),
    rule(
        "Wie oft? einmal pro Woche, mehrmals am Tag",
        "other",
        """
How often you use media:

- ***einmal / zweimal / mehrmals** pro Woche / am Tag / im Monat*
- ***jeden** Abend, **jede** Woche, **jedes** Wochenende* (Akkusativ, no preposition)
- *immer · meistens · oft · manchmal · selten · nie*

Word order: the time comes early in the middle of the sentence, before the place
and the object: *Ich sehe **jeden Abend** im Wohnzimmer die Nachrichten.*
""",
        [
            "Ich benutze das Internet mehrmals am Tag.",
            "Jeden Sonntag sehen wir einen Krimi.",
            "Ich lese nur einmal pro Woche eine Zeitschrift.",
        ],
    ),
]

L15_LESSONS = [
    lesson(
        "Medien",
        review("die Sendung"),
        review("die Fernbedienung"),
        match(
            [
                ("der Krimi", "the crime drama"),
                ("die Serie", "the series"),
                ("die Werbung", "the advertising"),
                ("die Dokumentation", "the documentary"),
                ("der Sender", "the channel"),
            ]
        ),
        mc(
            "Eine Sendung, die man später im Internet sieht, findet man in der ...",
            "Mediathek.",
            "Fernbedienung.",
            "Zeitschrift.",
        ),
        mc(
            "Die Dokumentation war sehr ___. Ich habe viel gelernt.",
            "informativ",
            "besetzt",
            "unhöflich",
        ),
        fill("Ich habe meine ___ verpasst! (favourite programme)", "Lieblingssendung"),
        tr("It's about to start!", "Gleich geht's los!|Gleich geht es los!"),
    ),
    lesson(
        "einschalten oder verpassen?",
        grammar("Vorsilben: trennbar oder nicht?"),
        mc("Ich ___ den Fernseher jetzt ein.", "schalte", "einschalte", "geschaltet"),
        fill("Schalt bitte das Radio ___! (off)", "aus"),
        fill("Ich nehme den Krimi ___. (record)", "auf"),
        fill("Hast du die Sendung ___? (verpassen)", "verpasst"),
        fill("Ich habe den Fernseher ___. (einschalten)", "eingeschaltet"),
        fill("Er hat das Video ___. (herunterladen)", "heruntergeladen"),
        mc(
            "Which Perfekt is correct?",
            "Ich habe die Sendung verpasst.",
            "Ich habe die Sendung geverpasst.",
            "Ich habe die Sendung vergepasst.",
        ),
        order("Ich schalte um, weil Werbung kommt."),
        tr(
            "Switch on the TV, please! (du)",
            "Schalt bitte den Fernseher ein!|Schalte bitte den Fernseher ein!",
        ),
    ),
    lesson(
        "Wie oft?",
        grammar("Wie oft? einmal pro Woche, mehrmals am Tag"),
        mc("Ich benutze das Internet ___ am Tag.", "mehrmals", "jeden", "nie mal"),
        fill("___ Abend sehe ich die Nachrichten. (every)", "Jeden"),
        fill("Ich lese ___ pro Woche eine Zeitschrift. (once)", "einmal"),
        fill("Wir hören ___ Woche diesen Podcast. (every)", "jede"),
        mc(
            "Which word order is best?",
            "Ich sehe jeden Abend im Wohnzimmer fern.",
            "Ich sehe im Wohnzimmer fern jeden Abend.",
            "Jeden Abend ich sehe im Wohnzimmer fern.",
        ),
        order("Jeden Sonntag sehen wir zusammen einen Krimi."),
        tr("I watch TV twice a week.", "Ich sehe zweimal pro Woche fern."),
    ),
    lesson(
        "Meine Mediengewohnheiten",
        bank(
            "Ich sehe nicht oft fern, nur ___ pro Woche. Meistens sehe ich mir die Sendungen "
            "später in der ___ an, dann gibt es keine ___. Morgens höre ich ___. Im Internet "
            "___ ich mich über Politik. Mein Bruder ___ jeden Tag Videos hoch.",
            ["zweimal", "Mediathek", "Werbung", "Radio", "informiere", "lädt"],
            "verpasse",
            "Sender",
        ),
        mc(
            "Why does the writer watch programmes in the media library?",
            "Because there are no adverts.",
            "Because the TV is broken.",
            "Because it's free.",
        ),
        mc(
            "Was läuft heute im Fernsehen? asks about ...",
            "today's TV programme.",
            "a race.",
            "the remote control.",
        ),
        fill("Der Sender ___ den Film um 20:15 Uhr aus. (broadcast)", "strahlt"),
        tr("I'll watch that later. (sich ansehen)", "Ich sehe mir das später an."),
    ),
    lesson(
        "Lektion 15: Test",
        fill("Ich schalte den Computer ___. (on)", "ein"),
        fill("Wir haben den Film ___. (verpassen)", "verpasst"),
        mc("Ich habe die Serie ___.", "aufgenommen", "geaufnommen"),
        fill("Ich höre ___ Morgen Radio. (every)", "jeden"),
        mc("Krimi, Serie, Dokumentation: Das sind ...", "Sendungen.", "Sender.", "Zeitschriften."),
        order("Ich benutze das Internet mehrmals am Tag."),
        tr(
            "Switch off the radio, please! (du)",
            "Schalt bitte das Radio aus!|Schalte bitte das Radio aus!",
        ),
    ),
    lesson(
        "Modul 5: Wiederholung",
        mc("___ ich zum ersten Mal in Deutschland war, war ich 18.", "Als", "Wenn"),
        fill("Die Lehrerin war sehr ___. (patient)", "geduldig"),
        fill("Das ist ___. Das geht nicht. (impossible)", "unmöglich"),
        fill("Das Paket ___ morgen geliefert.", "wird"),
        fill("Die Briefe werden ___. (verschicken)", "verschickt"),
        mc("Sehr geehrte ___ Weber,", "Frau", "Liebe"),
        fill("Ich nehme die Sendung ___. (record)", "auf"),
        fill("Hast du den Anfang ___? (verpassen)", "verpasst"),
        bank(
            "Als ich ein Kind ___, haben wir jeden Abend um acht den Fernseher ___. Heute ___ "
            "die Sendungen oft in der Mediathek angesehen.",
            ["war", "eingeschaltet", "werden"],
            "wird",
            "verpasst",
        ),
        tr(
            "The parcels are being packed.",
            "Die Pakete werden gepackt.|Die Päckchen werden gepackt.",
        ),
        order("Wenn ich Zeit habe, sehe ich mir eine Dokumentation an."),
    ),
]

LEKTION_15 = unit(
    15,
    "Gleich geht's los!",
    "Medien und Gewohnheiten",
    L15_WORDS,
    L15_RULES,
    sections(L15_LESSONS, vocab_lessons(L15_WORDS, "Wörter")),
)


UNITS = [LEKTION_13, LEKTION_14, LEKTION_15]
