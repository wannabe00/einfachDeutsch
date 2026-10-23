"""Modul 5 (B1.2): Lektion 13 (Aus diesem Grund gab es ein Missverständnis.),
14 (Die Teilnahme ist auf eigene Gefahr.), 15 (Schön, dass Sie da sind.)."""

from ..dsl import (
    bank,
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
# Lektion 13: Aus diesem Grund gab es ein Missverständnis.
# ============================================================================

L13_WORDS = [
    ("the misunderstanding", "das Missverständnis", "noun", "Pl. die Missverständnisse"),
    ("the stress (on a syllable)", "die Betonung", "noun", "Pl. die Betonungen"),
    ("the translation", "die Übersetzung", "noun", "Pl. die Übersetzungen"),
    ("the translation error", "der Übersetzungsfehler", "noun", "Pl. die Übersetzungsfehler"),
    ("the meaning", "die Bedeutung", "noun", "Pl. die Bedeutungen"),
    ("the reason", "der Grund", "noun", "Pl. die Gründe"),
    ("the consequence", "die Folge", "noun", "Pl. die Folgen"),
    ("the cause", "die Ursache", "noun", "Pl. die Ursachen"),
    ("the announcement (loudspeaker)", "die Durchsage", "noun", "Pl. die Durchsagen"),
    ("the queue / snake", "die Schlange", "noun", "Schlange stehen"),
    ("the counter / switch", "der Schalter", "noun", "Pl. die Schalter"),
    ("the tap / rooster", "der Hahn", "noun", "Pl. die Hähne"),
    ("the ladder", "die Leiter", "noun", "der Leiter = the leader"),
    ("the nail", "der Nagel", "noun", "Pl. die Nägel"),
    ("the registry office", "das Standesamt", "noun", "Pl. die Standesämter"),
    ("the lawyer", "der Rechtsanwalt", "noun", "Pl. die Rechtsanwälte, f. die Rechtsanwältin"),
    ("the civil servant", "der Beamte", "noun", "ein Beamter, f. die Beamtin"),
    ("the course leader", "der Kursleiter", "noun", "f. die Kursleiterin"),
    ("to misunderstand", "missverstehen", "verb", "missverstand, hat missverstanden"),
    ("to ask again (to check)", "nachfragen", "verb", "hat nachgefragt"),
    ("to follow", "folgen", "verb", "folgen + Dat., ist gefolgt"),
    ("to get / to obtain", "besorgen", "verb", "hat besorgt"),
    ("to clear up / to explain", "klären", "verb", "hat geklärt"),
    ("to bite", "beißen", "verb", "biss, hat gebissen"),
    ("to be frightened", "erschrecken", "verb", "erschrickt, erschrak, ist erschrocken"),
    ("to fly off / to take off", "abfliegen", "verb", "flog ab, ist abgeflogen"),
    ("unclear (not clearly)", "undeutlich", "adjective"),
    ("mixed up", "durcheinander", "adverb", "durcheinander reden"),
    ("embarrassing", "peinlich", "adjective"),
    ("ambiguous", "mehrdeutig", "adjective"),
    ("angry / evil", "böse", "adjective"),
    ("instantly", "augenblicklich", "adverb"),
    ("therefore", "deshalb", "adverb"),
    ("that's why", "deswegen", "adverb"),
    ("for that reason", "darum", "adverb"),
    ("hence", "daher", "adverb"),
    ("for this reason", "aus diesem Grund", "phrase"),
    ("because of", "wegen", "other", "wegen + Genitiv"),
    ("That was so embarrassing!", "Das war so peinlich!", "phrase"),
    ("Could you say that more slowly?", "Könnten Sie das bitte langsamer sagen?", "phrase"),
]

L13_RULES = [
    rule(
        "deshalb, deswegen, darum, daher",
        "sentence_structure",
        """
These words point to a **consequence**: the sentence before gives the reason.
They belong to the **main clause**, so the verb comes **right after** them when
they stand first:

| reason | consequence |
|---|---|
| *Es war sehr laut.* | ***Deshalb** **konnte** ich die Durchsage nicht verstehen.* |
| *Er sprach Dialekt.* | ***Deswegen** **habe** ich ihn falsch verstanden.* |
| *Ich war unsicher.* | ***Darum** **fragte** ich noch einmal nach.* |
| *Der Zug hatte Verspätung.* | ***Aus diesem Grund** **kam** ich zu spät.* |

All four mean the same; *daher* sounds a bit more formal. They can also stand
later: *Ich habe **deshalb** noch einmal nachgefragt.*

Compare **weil** (reason, verb at the end): *Ich habe nachgefragt, **weil** ich
es nicht verstanden **habe**.*
""",
        [
            "Er sprach sehr schnell. Deshalb verstand ich ihn nicht.",
            "Es gab einen Übersetzungsfehler. Aus diesem Grund gab es ein Missverständnis.",
            "Ich habe es deswegen noch einmal erklärt.",
        ],
    ),
    rule(
        "wegen + Genitiv",
        "cases",
        """
**wegen** (because of) is a preposition with the **genitive** and is followed
by a noun, not a clause:

- ***Wegen des Lärms** konnte ich nichts hören.*
- ***Wegen der Betonung** gab es ein Missverständnis.*
- ***Wegen eines Fehlers** kam die Lieferung zu spät.*

| clause with *weil* | noun with *wegen* |
|---|---|
| *Weil es laut war, ...* | *Wegen des Lärms ...* |
| *Weil das Wetter schlecht war, ...* | *Wegen des schlechten Wetters ...* |

In everyday speech you will hear *wegen dem Lärm* (dative), but in writing use
the genitive.
""",
        [
            "Wegen des Dialekts habe ich die Frau nicht verstanden.",
            "Wegen der Verspätung haben wir den Anschluss verpasst.",
            "Wegen eines Missverständnisses bekam ich das falsche Essen.",
        ],
    ),
    rule(
        "Nachfragen und Missverständnisse klären",
        "other",
        """
**When you don't understand:**
- *Wie bitte? · Entschuldigung, ich habe Sie nicht verstanden.*
- *Könnten Sie das bitte wiederholen / langsamer sagen / lauter sprechen?*
- *Was bedeutet das Wort ...? · Könnten Sie das anders erklären?*
- *Habe ich Sie richtig verstanden: ...?*

**Telling about a misunderstanding:**
- *Mir ist Folgendes passiert: ... · Einmal habe ich ...*
- *Erst später habe ich bemerkt, dass ... · Das war mir so peinlich!*
""",
        [
            "Entschuldigung, könnten Sie das bitte wiederholen?",
            "Habe ich Sie richtig verstanden: Der Zug fällt aus?",
            "Mir ist Folgendes passiert: Ich habe im Restaurant das falsche Wort benutzt.",
        ],
    ),
]

L13_LESSONS = [
    lesson(
        "Wörter mit zwei Bedeutungen",
        review("das Missverständnis"),
        review("die Bedeutung"),
        match(
            [
                ("die Schlange", "ein Tier / viele Leute warten"),
                ("der Schalter", "am Bahnhof / für das Licht"),
                ("der Hahn", "ein Vogel / für das Wasser"),
                ("die Bank", "für das Geld / zum Sitzen"),
                ("das Schloss", "ein König wohnt dort / an der Tür"),
            ],
            "Which two meanings does each word have?",
        ),
        mc(
            "Ein Wort mit mehreren Bedeutungen ist ...",
            "mehrdeutig.",
            "peinlich.",
            "undeutlich.",
        ),
        mc(
            "Im Zug sagt eine Stimme etwas aus dem Lautsprecher. Das ist eine ...",
            "Durchsage.",
            "Übersetzung.",
            "Folge.",
        ),
        fill(
            "Er hat so ___ gesprochen, dass ich nichts verstanden habe. (unclearly)", "undeutlich"
        ),
        fill("Alle haben ___ geredet. (mixed up)", "durcheinander"),
        fill("Bitte ___ Sie mir! (folgen)", "folgen"),
        tr("That was so embarrassing!", "Das war so peinlich!"),
    ),
    lesson(
        "Deshalb verstand ich nichts",
        grammar("deshalb, deswegen, darum, daher"),
        mc(
            "Which sentence is correct?",
            "Es war laut. Deshalb konnte ich nichts hören.",
            "Es war laut. Deshalb ich konnte nichts hören.",
            "Es war laut. Deshalb nichts konnte ich hören.",
        ),
        mc(
            "Er sprach Dialekt. ___ habe ich ihn nicht verstanden.",
            "Deswegen",
            "Weil",
            "Obwohl",
        ),
        mc(
            "Ich habe nachgefragt, ___ ich unsicher war.",
            "weil",
            "deshalb",
            "darum",
        ),
        fill(
            "Der Zug hatte Verspätung. ___ kam ich zu spät. (therefore)",
            "Deshalb|Deswegen|Darum|Daher",
        ),
        fill("Aus diesem ___ gab es ein Missverständnis. (reason)", "Grund"),
        fill("Ich habe ___ noch einmal nachgefragt. (for that reason: darum)", "darum"),
        order("Darum fragte sie noch einmal nach."),
        order("Aus diesem Grund kam ich zu spät."),
        tr(
            "He spoke too fast. That's why I didn't understand him.",
            "Er sprach zu schnell. Deshalb verstand ich ihn nicht.|Er sprach zu schnell. Deswegen verstand ich ihn nicht.|Er hat zu schnell gesprochen. Deshalb habe ich ihn nicht verstanden.",
        ),
    ),
    lesson(
        "Wegen des Lärms",
        grammar("wegen + Genitiv"),
        mc("___ des Lärms konnte ich nichts hören.", "Wegen", "Weil", "Deshalb"),
        mc("Wegen ___ Betonung gab es ein Missverständnis.", "der", "die", "des"),
        mc("Wegen ___ Dialekts habe ich nichts verstanden.", "des", "dem", "der"),
        fill("Wegen ___ Fehlers kam die Lieferung zu spät. (ein)", "eines"),
        fill("Wegen des schlechten ___ blieben wir zu Hause. (Wetter)", "Wetters"),
        fill("Weil es regnete, ... = ___ des Regens ...", "Wegen"),
        order("Wegen der Verspätung haben wir den Zug verpasst."),
        tr(
            "Because of a translation error there was a misunderstanding.",
            "Wegen eines Übersetzungsfehlers gab es ein Missverständnis.",
        ),
    ),
    lesson(
        "Wie bitte?",
        grammar("Nachfragen und Missverständnisse klären"),
        match(
            [
                ("Sie sprechen zu leise.", "Könnten Sie bitte lauter sprechen?"),
                ("Sie sprechen zu schnell.", "Könnten Sie das bitte langsamer sagen?"),
                ("Sie kennen ein Wort nicht.", "Was bedeutet das Wort?"),
                ("Sie sind nicht sicher.", "Habe ich Sie richtig verstanden?"),
            ],
            "What do you say?",
        ),
        bank(
            "Mir ist Folgendes ___: Ich war am ___ und wollte ein Ticket kaufen. Der Mann sprach "
            "sehr ___. Deshalb habe ich ___. Erst später habe ich bemerkt, dass ich das "
            "falsche Ticket hatte. Das war so ___!",
            ["passiert", "Schalter", "undeutlich", "nachgefragt", "peinlich"],
            "Hahn",
            "deswegen",
        ),
        mc(
            "Beim Standesamt ...",
            "heiratet man.",
            "kauft man Brot.",
            "fliegt man ab.",
        ),
        fill("Ich bin furchtbar ___, als der Hund bellte. (erschrecken)", "erschrocken"),
        fill("Kannst du mir bitte Brot ___? (get)", "besorgen"),
        fill("Wir müssen das Missverständnis ___. (clear up)", "klären"),
        tr("Could you say that more slowly? (Sie)", "Könnten Sie das bitte langsamer sagen?"),
    ),
    lesson(
        "Lektion 13: Test",
        fill("Es war laut. ___ verstand ich nichts. (therefore)", "Deshalb|Deswegen|Darum|Daher"),
        mc("___ des Regens fahren wir nicht.", "Wegen", "Weil", "Darum"),
        fill("Wegen ___ Missverständnisses war sie böse. (das)", "des"),
        mc("Der Hahn in der Küche ist ...", "für das Wasser.", "ein Vogel.", "ein Schalter."),
        fill("Ich habe dich ___. (missverstehen)", "missverstanden"),
        order("Deswegen habe ich noch einmal nachgefragt."),
        tr("What does this word mean?", "Was bedeutet dieses Wort?"),
        tr("The plane took off on time.", "Das Flugzeug ist pünktlich abgeflogen."),
    ),
]

LEKTION_13 = unit(
    13,
    "Aus diesem Grund gab es ein Missverständnis.",
    "Sprache und Missverständnisse",
    L13_WORDS,
    L13_RULES,
    sections(L13_LESSONS, vocab_lessons(L13_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 14: Die Teilnahme ist auf eigene Gefahr.
# ============================================================================

L14_WORDS = [
    ("the adult education centre", "die Volkshochschule", "noun", "short: die VHS"),
    ("the adult education", "die Erwachsenenbildung", "noun"),
    ("the semester / term", "das Semester", "noun", "Pl. die Semester"),
    ("the participation", "die Teilnahme", "noun"),
    ("the participant", "der Teilnehmer", "noun", "f. die Teilnehmerin"),
    ("the danger", "die Gefahr", "noun", "auf eigene Gefahr"),
    ("the target group", "die Zielgruppe", "noun", "Pl. die Zielgruppen"),
    ("the previous knowledge", "die Vorkenntnisse", "noun", "only plural"),
    ("the requirement", "die Voraussetzung", "noun", "Pl. die Voraussetzungen"),
    ("the registration", "die Anmeldung", "noun", "Pl. die Anmeldungen"),
    ("the fee", "die Gebühr", "noun", "Pl. die Gebühren"),
    ("the skill", "die Fertigkeit", "noun", "Pl. die Fertigkeiten"),
    ("the photography", "die Fotografie", "noun"),
    ("the impression", "der Eindruck", "noun", "Pl. die Eindrücke"),
    ("the imagination", "die Fantasie", "noun", "Pl. die Fantasien"),
    ("the basis", "die Grundlage", "noun", "Pl. die Grundlagen"),
    ("the possibility", "die Möglichkeit", "noun", "Pl. die Möglichkeiten"),
    ("the needle", "die Nadel", "noun", "Pl. die Nadeln"),
    ("the rest / remainder", "der Rest", "noun", "Pl. die Reste"),
    ("the senior citizen", "der Senior", "noun", "den Senioren, f. die Seniorin"),
    ("the software", "die Software", "noun"),
    ("the voice", "die Stimme", "noun", "Pl. die Stimmen"),
    ("the talent", "das Talent", "noun", "Pl. die Talente"),
    ("the breath", "der Atem", "noun"),
    ("to acquire", "erwerben", "verb", "erwirbt, erwarb, hat erworben"),
    ("to listen", "zuhören", "verb", "zuhören + Dat., hat zugehört"),
    ("fascinating", "faszinierend", "adjective"),
    ("trained / qualified", "ausgebildet", "adjective"),
    ("necessary", "notwendig", "adjective"),
    ("current / up to date", "aktuell", "adjective"),
    ("rich", "reich", "adjective", "reich sein an + Dat."),
    ("state-run", "staatlich", "adjective"),
    ("backwards", "rückwärts", "adverb"),
    ("Participation is at your own risk.", "Die Teilnahme ist auf eigene Gefahr.", "phrase"),
    ("No previous knowledge is needed.", "Vorkenntnisse sind nicht nötig.", "phrase"),
]

L14_RULES = [
    rule(
        "Partizip I und II als Adjektiv",
        "adjectives",
        """
Participles can stand **before a noun** like adjectives, with the usual
adjective endings.

**Partizip I** = infinitive + **d**. It describes something that is **happening
now** (active):
*lachen → lachen**d** → ein lachend**es** Kind* (a child that is laughing)
*faszinieren → ein faszinierend**er** Kurs*

**Partizip II** describes something that **has been done** (a result, often
passive):
*ausbilden → ausgebildet → eine ausgebildet**e** Lehrerin* (a teacher who has
been trained)
*auswählen → ausgewählte Musikstücke*

| | Partizip I (-d) | Partizip II |
|---|---|---|
| *kochen* | *das kochend**e** Wasser* (is boiling) | *das gekocht**e** Wasser* (has been boiled) |
| *lernen* | *die lernend**en** Kinder* | *die gelernt**en** Wörter* |

Endings exactly like other adjectives: *der lachende Junge, ein lachender Junge,
mit dem lachenden Jungen*.
""",
        [
            "Der Kurs bietet faszinierende Einblicke in die Fotografie.",
            "Eine ausgebildete Expertin leitet den Kurs.",
            "Vorsicht, kochendes Wasser!",
            "Wir üben die gelernten Wörter.",
        ],
    ),
    rule(
        "Kurse beschreiben und empfehlen",
        "other",
        """
**Describing a course:**
- *In unserem Kurs lernen Sie ... · Sie haben die Möglichkeit, ... zu ...*
- *Der Kurs ist für alle geeignet, die ... · Zielgruppe: Senioren / Anfänger*
- *Vorkenntnisse sind (nicht) nötig / erforderlich.*
- *Die Teilnahme ist kostenlos / kostet 80 Euro. · Anmeldung bis ...*

**Recommending:**
- *Ich kann Ihnen diesen Kurs empfehlen. · Haben Sie schon einmal ...
  ausprobiert? · Das wäre etwas für Sie, weil ...*

**Registering:** *Ich möchte mich für den Kurs ... anmelden. · Gibt es noch freie
Plätze? · Der Kurs ist leider ausgebucht.*
""",
        [
            "Der Kurs ist für alle geeignet, die gern fotografieren.",
            "Vorkenntnisse sind nicht nötig.",
            "Ich möchte mich für den Kletterkurs anmelden.",
        ],
    ),
]

L14_LESSONS = [
    lesson(
        "Das neue Semester",
        review("die Volkshochschule"),
        review("die Teilnahme"),
        match(
            [
                ("die Zielgruppe", "für wen der Kurs ist"),
                ("die Vorkenntnisse", "was man schon wissen muss"),
                ("die Gebühr", "was der Kurs kostet"),
                ("die Anmeldung", "Man sagt: Ich möchte mitmachen."),
                ("auf eigene Gefahr", "Man ist selbst verantwortlich."),
            ],
            "Match the word to its meaning.",
        ),
        mc(
            "Eine Schule für Erwachsene mit vielen Kursen ist die ...",
            "Volkshochschule.",
            "Zielgruppe.",
            "Grundlage.",
        ),
        mc(
            "Für einen Nähkurs braucht man eine ...",
            "Nadel.",
            "Stimme.",
            "Software.",
        ),
        fill("Im Kurs können Sie neue Fertigkeiten ___. (acquire)", "erwerben"),
        fill("Bitte hören Sie gut ___! (zuhören)", "zu"),
        fill("Die Stadt ist ___ an Kultur. (rich)", "reich"),
        tr("Participation is at your own risk.", "Die Teilnahme ist auf eigene Gefahr."),
    ),
    lesson(
        "Ein faszinierender Kurs",
        grammar("Partizip I und II als Adjektiv"),
        mc("ein Kind, das lacht → ein ___ Kind", "lachendes", "gelachtes", "lachende"),
        mc(
            "eine Lehrerin, die ausgebildet wurde → eine ___ Lehrerin",
            "ausgebildete",
            "ausbildende",
            "ausgebildeter",
        ),
        mc("Vorsicht, ___ Wasser! (It is boiling.)", "kochendes", "gekochtes", "kochende"),
        fill("Das ist ein ___ Thema. (faszinieren, Partizip I)", "faszinierendes"),
        fill("Wir wiederholen die ___ Wörter. (lernen, Partizip II)", "gelernten"),
        fill("Die ___ Musikstücke sind toll. (auswählen, Partizip II)", "ausgewählten"),
        fill("Mit ___ Kursleiterinnen lernen Sie schnell. (erfahren)", "erfahrenen"),
        fill("Der ___ Junge winkt uns zu. (lachen, Partizip I)", "lachende"),
        order("Eine ausgebildete Expertin leitet den Kurs."),
        tr("We are looking for a suitable course.", "Wir suchen einen passenden Kurs."),
    ),
    lesson(
        "Welcher Kurs passt zu Ihnen?",
        grammar("Kurse beschreiben und empfehlen"),
        bank(
            "Fotografie für Senioren: In unserem Kurs lernen Sie die ___ der Fotografie. "
            "Vorkenntnisse sind nicht ___. Sie haben die ___, eigene Fotos zu machen. "
            "Die ___ beträgt 60 Euro. ___ bis zum 1. März.",
            ["Grundlagen", "nötig", "Möglichkeit", "Gebühr", "Anmeldung"],
            "Gefahr",
            "Atem",
        ),
        mc(
            "Der Kurs ist leider ausgebucht. means:",
            "There are no places left.",
            "The course has been cancelled.",
            "The course is free.",
        ),
        mc(
            "Ein Kurs, den der Staat bezahlt, ist ...",
            "staatlich.",
            "aktuell.",
            "rückwärts.",
        ),
        fill("Beim Yoga übt man den ___. (breath)", "Atem"),
        fill("Sie hat ein großes ___ für Musik. (talent)", "Talent"),
        fill("Der Kurs hat einen guten ___ auf mich gemacht. (impression)", "Eindruck"),
        tr("I'd like to sign up for the course.", "Ich möchte mich für den Kurs anmelden."),
    ),
    lesson(
        "Lektion 14: Test",
        fill("ein ___ Kurs (faszinieren, Partizip I)", "faszinierender"),
        fill("die ___ Fotos (machen, Partizip II)", "gemachten"),
        mc("Vorsicht, ___ Wasser! (It's boiling.)", "kochendes", "gekochtes", "kocht"),
        mc(
            "Was man vor dem Kurs schon wissen muss:", "die Vorkenntnisse", "die Gebühr", "der Rest"
        ),
        fill("Ein Pass ist eine ___ für die Reise. (requirement)", "Voraussetzung"),
        order("Vorkenntnisse sind nicht nötig."),
        tr("The course is fully booked.", "Der Kurs ist ausgebucht."),
        tr("She has a beautiful voice.", "Sie hat eine schöne Stimme."),
    ),
]

LEKTION_14 = unit(
    14,
    "Die Teilnahme ist auf eigene Gefahr.",
    "Weiterbildung und Kurse",
    L14_WORDS,
    L14_RULES,
    sections(L14_LESSONS, vocab_lessons(L14_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 15: Schön, dass Sie da sind.
# ============================================================================

L15_WORDS = [
    ("the cover letter", "das Bewerbungsschreiben", "noun", "Pl. die Bewerbungsschreiben"),
    ("the job advert", "die Stellenanzeige", "noun", "Pl. die Stellenanzeigen"),
    ("the applicant", "der Bewerber", "noun", "f. die Bewerberin"),
    ("the work experience", "die Berufserfahrung", "noun"),
    ("the requirement (for a job)", "die Anforderung", "noun", "Pl. die Anforderungen"),
    ("the language skills", "die Sprachkenntnisse", "noun", "only plural"),
    ("the computer skills", "die Computerkenntnisse", "noun", "only plural"),
    ("the customer contact", "der Kundenkontakt", "noun"),
    ("the HR manager", "der Personalleiter", "noun", "f. die Personalleiterin"),
    ("the correspondence", "die Korrespondenz", "noun"),
    ("the care / supervision", "die Betreuung", "noun"),
    ("the industry", "die Industrie", "noun", "Pl. die Industrien"),
    ("the means / remedy", "das Mittel", "noun", "das Kommunikationsmittel"),
    ("the physics", "die Physik", "noun"),
    ("the president", "der Präsident", "noun", "den Präsidenten, f. die Präsidentin"),
    ("the press release", "die Pressemeldung", "noun", "Pl. die Pressemeldungen"),
    ("the research (journalism)", "die Recherche", "noun", "Pl. die Recherchen"),
    ("the reporter", "der Reporter", "noun", "f. die Reporterin"),
    ("the writing / script", "die Schrift", "noun", "in Wort und Schrift"),
    ("the social worker", "der Sozialarbeiter", "noun", "f. die Sozialarbeiterin"),
    ("the entrepreneur", "der Unternehmer", "noun", "f. die Unternehmerin"),
    ("the scientist", "der Wissenschaftler", "noun", "f. die Wissenschaftlerin"),
    ("the poet", "der Dichter", "noun", "f. die Dichterin"),
    ("the section / paragraph", "der Abschnitt", "noun", "Pl. die Abschnitte"),
    ("the stain", "der Fleck", "noun", "Pl. die Flecken"),
    ("the account (bank)", "das Konto", "noun", "Pl. die Konten"),
    ("to hire (an employee)", "einstellen", "verb", "hat eingestellt"),
    ("to transfer / to broadcast", "übertragen", "verb", "überträgt, hat übertragen"),
    ("to have (skills) at your disposal", "verfügen", "verb", "verfügen über + Akk."),
    ("resilient (under pressure)", "belastbar", "adjective"),
    ("responsible", "verantwortlich", "adjective", "verantwortlich für + Akk."),
    ("committed", "engagiert", "adjective"),
    ("general", "allgemein", "adjective"),
    ("individual / single", "einzeln", "adjective"),
    ("usual", "üblich", "adjective"),
    ("both ... and", "sowohl ... als auch", "other"),
    ("not only ... but also", "nicht nur ... sondern auch", "other"),
    ("to pay attention", "Acht geben", "phrase", "Acht geben auf + Akk."),
    ("Nice that you're here.", "Schön, dass Sie da sind.", "phrase"),
    ("I am hereby applying for ...", "Hiermit bewerbe ich mich um ...", "phrase"),
]

L15_RULES = [
    rule(
        "sowohl ... als auch, nicht nur ... sondern auch",
        "sentence_structure",
        """
Two-part connectors join **two equal things** (two nouns, two adjectives, two
verbs):

**sowohl ... als auch** = both ... and
- *Ich spreche **sowohl** Deutsch **als auch** Spanisch.*
- *Sie ist **sowohl** zuverlässig **als auch** freundlich.*

**nicht nur ..., sondern auch** = not only ..., but also (stresses the second
part)
- *Ich habe **nicht nur** Berufserfahrung, **sondern auch** gute
  Computerkenntnisse.*
- *Er arbeitet **nicht nur** schnell, **sondern auch** genau.*

There is a **comma** before *sondern*, not before *als auch*. Both parts should
be the same kind of word: ~~sowohl Deutsch als auch sehr gut~~.
""",
        [
            "Sie spricht sowohl Italienisch als auch Französisch.",
            "Er ist nicht nur pünktlich, sondern auch sehr engagiert.",
            "Wir suchen sowohl Bewerber mit Erfahrung als auch Berufsanfänger.",
        ],
    ),
    rule(
        "Bewerbung und Vorstellungsgespräch",
        "other",
        """
**Cover letter (Bewerbungsschreiben):**
- *Sehr geehrte Frau ..., / Sehr geehrter Herr ...,*
- *mit großem Interesse habe ich Ihre Stellenanzeige gelesen.*
- *Hiermit bewerbe ich mich um die Stelle als ...*
- *Ich habe meine Ausbildung als ... abgeschlossen. · Ich verfüge über ...*
- *Ich habe bereits Erfahrung in ... gesammelt. · Zu meinen Aufgaben gehörten ...*
- *Über eine Einladung zu einem Vorstellungsgespräch würde ich mich sehr freuen.*
- *Mit freundlichen Grüßen*

**Interview:** *Schön, dass Sie da sind. · Erzählen Sie bitte etwas über sich. ·
Warum möchten Sie bei uns arbeiten? · Was sind Ihre Stärken? · Vielen Dank für
das Gespräch.*
""",
        [
            "Hiermit bewerbe ich mich um die Stelle als Sachbearbeiterin.",
            "Ich habe bereits Erfahrung im Kundenkontakt gesammelt.",
            "Über eine Einladung zu einem Vorstellungsgespräch würde ich mich freuen.",
        ],
    ),
]

L15_LESSONS = [
    lesson(
        "Stellenanzeigen",
        review("die Stellenanzeige"),
        review("der Bewerber"),
        match(
            [
                ("die Stellenanzeige", "Eine Firma sucht einen Mitarbeiter."),
                ("der Bewerber", "Er möchte die Stelle haben."),
                ("die Berufserfahrung", "Man hat schon in dem Beruf gearbeitet."),
                ("der Personalleiter", "Er stellt neue Mitarbeiter ein."),
                ("belastbar", "Man arbeitet auch unter Stress gut."),
            ],
            "Match the word to its meaning.",
        ),
        mc(
            "Eine Person, die für Zeitungen schreibt und Recherchen macht, ist ...",
            "ein Reporter.",
            "ein Dichter.",
            "ein Präsident.",
        ),
        mc(
            "Wer hilft Familien mit Problemen?",
            "der Sozialarbeiter",
            "der Wissenschaftler",
            "der Unternehmer",
        ),
        fill("Die Firma will zwei neue Mitarbeiter ___. (hire)", "einstellen"),
        fill("Sie ist ___ für die Korrespondenz. (responsible)", "verantwortlich"),
        fill("Das Spiel wird im Fernsehen ___. (übertragen)", "übertragen"),
        tr("Nice that you're here. (Sie)", "Schön, dass Sie da sind."),
    ),
    lesson(
        "Sowohl ... als auch",
        grammar("sowohl ... als auch, nicht nur ... sondern auch"),
        mc(
            "Ich spreche ___ Deutsch als auch Englisch.",
            "sowohl",
            "nicht nur",
            "entweder",
        ),
        mc(
            "Er ist nicht nur pünktlich, ___ auch freundlich.",
            "sondern",
            "als",
            "aber",
        ),
        fill("Sie hat ___ nur Erfahrung, sondern auch gute Ideen. (not)", "nicht"),
        fill("Wir suchen sowohl Anfänger ___ auch Profis. (as)", "als"),
        fill("Sie ist nicht nur engagiert, ___ auch belastbar. (but)", "sondern"),
        mc(
            "Where is the comma?",
            "Er arbeitet nicht nur schnell, sondern auch genau.",
            "Er arbeitet nicht nur, schnell sondern auch genau.",
            "Er arbeitet, nicht nur schnell sondern auch genau.",
        ),
        order("Sie spricht sowohl Italienisch als auch Französisch."),
        tr(
            "I have not only work experience but also good computer skills.",
            "Ich habe nicht nur Berufserfahrung, sondern auch gute Computerkenntnisse.",
        ),
    ),
    lesson(
        "Ein Bewerbungsschreiben",
        grammar("Bewerbung und Vorstellungsgespräch"),
        bank(
            "Sehr geehrte Frau Lang,\nmit großem ___ habe ich Ihre Stellenanzeige gelesen. "
            "___ bewerbe ich mich um die Stelle als Reiseverkehrskauffrau. Ich habe bereits "
            "Erfahrung im ___ gesammelt und spreche ___ Englisch als auch Spanisch. Über eine "
            "___ zu einem Vorstellungsgespräch würde ich mich sehr freuen.",
            ["Interesse", "Hiermit", "Kundenkontakt", "sowohl", "Einladung"],
            "sondern",
            "Fleck",
        ),
        mc(
            "Which question is typical in an interview?",
            "Warum möchten Sie bei uns arbeiten?",
            "Wie viel kostet die Wohnung?",
            "Kann ich die Jacke anprobieren?",
        ),
        mc(
            "in Wort und Schrift means:",
            "spoken and written",
            "only in writing",
            "in one word",
        ),
        fill("Sie hat mich im Gespräch völlig ___. (überzeugen)", "überzeugt"),
        fill("Auf meinem Hemd ist ein ___. (stain)", "Fleck"),
        fill("Das Gehalt wird auf Ihr ___ überwiesen. (account)", "Konto"),
        tr(
            "I am applying for the job as a nurse.",
            "Ich bewerbe mich um die Stelle als Krankenpflegerin.|Ich bewerbe mich um die Stelle als Krankenpfleger.",
        ),
    ),
    lesson(
        "Lektion 15: Test",
        fill("Ich spreche ___ Deutsch als auch Polnisch.", "sowohl"),
        fill("Er ist nicht nur nett, ___ auch klug.", "sondern"),
        mc("Hiermit bewerbe ich mich ___ die Stelle.", "um", "für", "auf"),
        mc("Erzählen Sie bitte etwas ___ sich.", "über", "von", "um"),
        fill("Das ist hier ___: Man duzt sich. (usual)", "üblich"),
        order("Ich habe nicht nur Erfahrung, sondern auch Ideen."),
        tr("Thank you for the conversation.", "Vielen Dank für das Gespräch."),
        tr("She is very committed.", "Sie ist sehr engagiert."),
    ),
    lesson(
        "Modul 5: Wiederholung",
        fill(
            "Es war laut. ___ konnte ich nichts hören. (therefore)", "Deshalb|Deswegen|Darum|Daher"
        ),
        fill("___ des Lärms konnte ich nicht schlafen. (because of)", "Wegen"),
        fill("Das ist ein ___ Buch. (faszinieren, Partizip I)", "faszinierendes"),
        fill("Wir lesen die ___ Texte noch einmal. (schreiben, Partizip II)", "geschriebenen"),
        mc("Sie spricht ___ Deutsch als auch Englisch.", "sowohl", "nicht nur", "weder"),
        mc("Sie ist nicht nur fleißig, ___ auch kreativ.", "sondern", "aber", "als"),
        bank(
            "___ eines Missverständnisses habe ich mich für den falschen Kurs angemeldet. "
            "Der Kurs war ___ teuer als auch langweilig. ___ habe ich mich am nächsten Tag "
            "wieder abgemeldet. Jetzt mache ich einen ___ Fotokurs.",
            ["Wegen", "sowohl", "Deshalb", "faszinierenden"],
            "Weil",
            "sondern",
        ),
        tr(
            "Because of a mistake, I came too late.",
            "Wegen eines Fehlers kam ich zu spät.|Wegen eines Fehlers bin ich zu spät gekommen.",
        ),
        order("Aus diesem Grund gab es ein Missverständnis."),
    ),
]

LEKTION_15 = unit(
    15,
    "Schön, dass Sie da sind.",
    "Bewerbung und Vorstellungsgespräch",
    L15_WORDS,
    L15_RULES,
    sections(L15_LESSONS, vocab_lessons(L15_WORDS, "Wörter")),
)


UNITS = [LEKTION_13, LEKTION_14, LEKTION_15]
