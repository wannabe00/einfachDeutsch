"""Modul 8 (A2.2): Lektion 22 (Seit ich meinen Wagen verkauft habe, ...), 23
(Der Beruf, der zu mir passt.), 24 (Wie sah dein Alltag aus?)."""

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
# Lektion 22: Seit ich meinen Wagen verkauft habe, ...
# ============================================================================

L22_WORDS = [
    ("the mobility", "die Mobilität", "noun"),
    ("the car (vehicle)", "der Wagen", "noun", "Pl. die Wagen"),
    ("the electric car", "das Elektroauto", "noun", "Pl. die Elektroautos"),
    ("the car sharing", "das Carsharing", "noun"),
    ("the petrol", "das Benzin", "noun"),
    ("the environmental protection", "der Umweltschutz", "noun"),
    ("the pollution", "die Umweltverschmutzung", "noun"),
    ("the exhaust fumes", "die Abgase", "noun", "plural"),
    ("the energy", "die Energie", "noun", "Pl. die Energien"),
    ("the electricity", "der Strom", "noun"),
    ("the member", "das Mitglied", "noun", "Pl. die Mitglieder"),
    ("the membership", "die Mitgliedschaft", "noun", "Pl. die Mitgliedschaften"),
    ("the tax", "die Steuer", "noun", "Pl. die Steuern"),
    ("the goal / destination", "das Ziel", "noun", "Pl. die Ziele"),
    ("the password", "das Passwort", "noun", "Pl. die Passwörter"),
    ("the data / details", "die Daten", "noun", "plural"),
    ("the booking", "die Buchung", "noun", "Pl. die Buchungen"),
    ("the instructions", "die Anleitung", "noun", "Pl. die Anleitungen"),
    ("to own", "besitzen", "verb", "hat besessen"),
    ("to share", "teilen", "verb", "hat geteilt"),
    ("to reach", "erreichen", "verb", "hat erreicht"),
    ("to log in", "einloggen", "verb", "sich einloggen"),
    ("to click (on)", "anklicken", "verb", "hat angeklickt"),
    ("to select", "auswählen", "verb", "hat ausgewählt"),
    ("to enter / type in", "eingeben", "verb", "gibt ein, hat eingegeben"),
    ("to confirm", "bestätigen", "verb", "hat bestätigt"),
    ("environmentally friendly", "umweltfreundlich", "adjective"),
    ("outside (of)", "außerhalb", "other", "außerhalb der Stadt"),
    ("at most", "höchstens", "adverb"),
    ("at least", "mindestens", "adverb"),
    ("Since I sold my car, ...", "Seit ich meinen Wagen verkauft habe, ...", "phrase"),
    ("How does that work?", "Wie geht das?", "phrase"),
]

L22_RULES = [
    rule(
        "Nebensätze mit seit und bis",
        "sentence_structure",
        """
**seit** (since): something started in the past and is **still true now**. The
main clause is usually in the **present**:

- ***Seit** ich meinen Wagen verkauft **habe**, **fahre** ich mehr Fahrrad.*
- *Sie benutzt oft die U-Bahn, **seit** sie in der Stadt **wohnt**.*

**bis** (until): the **end point**:

- *Ich warte hier, **bis** der Bus **kommt**.*
- ***Bis** das Auto repariert **ist**, **fahren** wir mit dem Zug.*

Both send the verb **to the end**. A clause at the start makes the main clause
begin with its verb.
""",
        [
            "Seit ich Carsharing benutze, spare ich viel Geld.",
            "Wir bleiben im Café, bis der Regen aufhört.",
            "Seit wir ein Elektroauto haben, brauchen wir kein Benzin mehr.",
        ],
    ),
    rule(
        "seit und bis als Präposition",
        "cases",
        """
*seit* and *bis* can also be **prepositions** in front of a time:

| | + | example |
|---|---|---|
| **seit** | Dativ | *seit einem Jahr · seit drei Wochen · seit gestern* |
| **bis** | (no article) | *bis Montag · bis morgen · bis 18 Uhr* |
| **bis zum / zur** | Dativ | *bis zum Wochenende · bis zur Grenze* |

German uses the **present** with *seit*, where English says "have been":
*Ich **wohne** seit zwei Jahren hier.* (I have been living here for two years.)
""",
        [
            "Ich bin seit einem Jahr Mitglied beim Carsharing.",
            "Die Buchung ist bis Freitag gültig.",
            "Wir fahren bis zur nächsten Tankstelle.",
        ],
    ),
]

L22_LESSONS = [
    lesson(
        "Mobilität und Umwelt",
        review("die Umweltverschmutzung"),
        review("das Carsharing"),
        match(
            [
                ("das Benzin", "the petrol"),
                ("die Abgase", "the exhaust fumes"),
                ("der Strom", "the electricity"),
                ("die Steuer", "the tax"),
                ("das Mitglied", "the member"),
            ]
        ),
        mc(
            "Ein Fahrrad macht keine Abgase. Es ist ...",
            "umweltfreundlich.",
            "außerhalb.",
            "höchstens.",
        ),
        mc(
            "Beim Carsharing ...",
            "teilen viele Leute ein Auto.",
            "hat jeder drei Autos.",
            "fährt man nur Fahrrad.",
        ),
        fill("Wir ___ kein Auto mehr. (own)", "besitzen"),
        fill("Ein Elektroauto fährt mit ___. (electricity)", "Strom"),
        tr("We live outside the city.", "Wir wohnen außerhalb der Stadt."),
    ),
    lesson(
        "Seit ich ...",
        grammar("Nebensätze mit seit und bis"),
        mc(
            "Which sentence is correct?",
            "Seit ich kein Auto habe, fahre ich mehr Fahrrad.",
            "Seit ich kein Auto habe, ich fahre mehr Fahrrad.",
            "Seit habe ich kein Auto, fahre ich mehr Fahrrad.",
        ),
        mc("___ ich kein Auto mehr habe, fahre ich mit dem Bus.", "Seit", "Bis", "Als"),
        mc("Warte hier, ___ ich zurückkomme.", "bis", "seit", "wenn"),
        fill("Seit ich meinen Wagen ___ habe, spare ich Geld. (verkaufen)", "verkauft"),
        fill("Wir bleiben hier, bis der Regen ___. (aufhören)", "aufhört"),
        fill("Seit sie in der Stadt ___, nimmt sie die U-Bahn. (wohnen)", "wohnt"),
        order("Ich warte, bis der Bus kommt."),
        tr(
            "Since I've been using car sharing, I save a lot of money.",
            "Seit ich Carsharing benutze, spare ich viel Geld.",
        ),
    ),
    lesson(
        "seit einem Jahr, bis Montag",
        grammar("seit und bis als Präposition"),
        mc("Ich wohne ___ zwei Jahren hier.", "seit", "bis", "vor"),
        mc("Die Buchung ist ___ Freitag gültig.", "bis", "seit", "um"),
        fill("Ich bin seit ___ Jahr Mitglied. (ein)", "einem"),
        fill("Wir fahren bis ___ Grenze. (zu der)", "zur"),
        fill("Er wartet ___ einer Stunde auf den Bus. (for: seit)", "seit"),
        mc(
            "I have been living here for two years:",
            "Ich wohne seit zwei Jahren hier.",
            "Ich habe seit zwei Jahren hier gewohnt.",
            "Ich wohne für zwei Jahre hier.",
        ),
        tr(
            "I have been waiting since 8 o'clock.", "Ich warte seit acht Uhr.|Ich warte seit 8 Uhr."
        ),
    ),
    lesson(
        "Online buchen",
        bank(
            "So buchst du ein Auto: Zuerst ___ du dich auf der Webseite ein. Dann gibst du "
            "dein ___ ein. Danach ___ du das Auto und die Zeit aus. Zuletzt ___ du die "
            "Buchung. Du bekommst eine E-Mail mit allen ___.",
            ["loggst", "Passwort", "wählst", "bestätigst", "Daten"],
            "klickst",
            "Steuer",
        ),
        mc(
            "What comes last?",
            "You confirm the booking.",
            "You log in.",
            "You enter the password.",
        ),
        mc(
            "Klicken Sie auf „Weiter“. means:",
            "Click on 'Next'.",
            "Wait for the next page.",
            "Close the website.",
        ),
        fill("Bitte ___ Sie Ihren Namen ein. (eingeben)", "geben"),
        fill("Hast du die E-Mail schon ___? (bestätigen)", "bestätigt"),
        tr("How does that work?", "Wie geht das?|Wie funktioniert das?"),
    ),
    lesson(
        "Unterwegs ohne Auto",
        mc(
            "Mit dem Bus ___ ich mein Ziel in 20 Minuten.",
            "erreiche",
            "besitze",
            "teile",
        ),
        mc(
            "Das Ticket kostet ___ 3 Euro, nicht mehr.",
            "höchstens",
            "mindestens",
            "außerhalb",
        ),
        fill("Man sollte ___ einmal pro Woche Rad fahren. (at least)", "mindestens"),
        fill("___ Sie bitte das Datum aus. (auswählen)", "Wählen"),
        tr("We share a car with our neighbours.", "Wir teilen ein Auto mit unseren Nachbarn."),
    ),
    lesson(
        "Lektion 22: Test",
        mc("___ ich in Berlin wohne, fahre ich Rad.", "Seit", "Bis"),
        fill("Ich bleibe, bis du ___. (kommen)", "kommst"),
        fill("Ich lerne ___ einem Jahr Deutsch. (since)", "seit"),
        fill("Bitte ___ Sie die Buchung. (confirm)", "bestätigen"),
        mc("Das Auto ist sehr ___: Es fährt mit Strom.", "umweltfreundlich", "teuer"),
        order("Seit ich meinen Wagen verkauft habe, fahre ich mehr Fahrrad."),
        tr("I'm waiting until the bus comes.", "Ich warte, bis der Bus kommt."),
    ),
]

LEKTION_22 = unit(
    22,
    "Seit ich meinen Wagen verkauft habe, ...",
    "Mobilität und Umwelt",
    L22_WORDS,
    L22_RULES,
    sections(L22_LESSONS, vocab_lessons(L22_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 23: Der Beruf, der zu mir passt.
# ============================================================================

L23_WORDS = [
    ("the vocational training", "die Berufsausbildung", "noun"),
    ("the vocational school", "die Berufsschule", "noun", "Pl. die Berufsschulen"),
    ("the trainee / apprentice", "der Azubi", "noun", "Pl. die Azubis"),
    ("the university studies", "das Studium", "noun", "Pl. die Studien"),
    ("the qualification / degree", "der Abschluss", "noun", "Pl. die Abschlüsse"),
    ("the further training", "die Weiterbildung", "noun", "Pl. die Weiterbildungen"),
    ("the application", "die Bewerbung", "noun", "Pl. die Bewerbungen"),
    ("the CV", "der Lebenslauf", "noun", "Pl. die Lebensläufe"),
    ("the job interview", "das Vorstellungsgespräch", "noun", "Pl. die Vorstellungsgespräche"),
    ("the ability", "die Fähigkeit", "noun", "Pl. die Fähigkeiten"),
    ("the qualification", "die Qualifikation", "noun", "Pl. die Qualifikationen"),
    ("the employee", "der Arbeitnehmer", "noun", "f. die Arbeitnehmerin"),
    ("the activity / duty", "die Tätigkeit", "noun", "Pl. die Tätigkeiten"),
    ("the working hours", "die Arbeitszeit", "noun", "Pl. die Arbeitszeiten"),
    ("the salary", "das Gehalt", "noun", "Pl. die Gehälter"),
    ("the wage", "der Lohn", "noun", "Pl. die Löhne"),
    ("the career", "die Karriere", "noun", "Pl. die Karrieren"),
    ("the responsibility", "die Verantwortung", "noun"),
    ("to apply (for)", "sich bewerben", "verb", "um + Akk., hat sich beworben"),
    ("to employ", "beschäftigen", "verb", "hat beschäftigt"),
    ("to quit / give notice", "kündigen", "verb", "hat gekündigt"),
    ("written", "schriftlich", "adjective"),
    ("oral", "mündlich", "adjective"),
    ("dissatisfied", "unzufrieden", "adjective"),
    ("creative", "kreativ", "adjective"),
    ("The job that suits me.", "Der Beruf, der zu mir passt.", "phrase"),
    ("I enjoy the work.", "Die Arbeit macht mir Spaß.", "phrase"),
]

L23_RULES = [
    rule(
        "Relativsätze im Nominativ",
        "sentence_structure",
        """
A **relative clause** describes a noun. It starts with a **relative pronoun**,
after a comma, and its verb goes **to the end**:

| | masculine | feminine | neuter | plural |
|---|---|---|---|---|
| Nominativ | **der** | **die** | **das** | **die** |

- *Das ist der Beruf, **der** zu mir **passt**.*
- *Ich suche eine Arbeit, **die** mir Spaß **macht**.*
- *Das ist ein Unternehmen, **das** viele Leute **beschäftigt**.*
- *Ich mag Kollegen, **die** hilfsbereit **sind**.*

The pronoun has the gender of the noun it describes.
""",
        [
            "Ich suche einen Job, der kreativ ist.",
            "Sie hat eine Stelle, die gut bezahlt ist.",
            "Das ist das Studium, das mich interessiert.",
        ],
    ),
    rule(
        "Relativsätze im Akkusativ",
        "sentence_structure",
        """
The relative pronoun takes the case of its role **inside the relative
clause**. If it's the **object**, use the **Akkusativ**; only the masculine
changes:

| | masculine | feminine | neuter | plural |
|---|---|---|---|---|
| Nominativ | der | die | das | die |
| Akkusativ | **den** | die | das | die |

- *Der Kollege, **der** hier arbeitet, ist nett.* (he works: subject)
- *Der Kollege, **den** ich kenne, ist nett.* (I know him: object)
- *Das ist die Kollegin, **die** ich gestern getroffen habe.*
""",
        [
            "Das ist der Beruf, den ich immer wollte.",
            "Die Bewerbung, die ich geschrieben habe, ist sehr gut.",
            "Der Chef, den wir jetzt haben, ist sehr fair.",
        ],
    ),
]

L23_LESSONS = [
    lesson(
        "Ausbildung und Beruf",
        review("die Bewerbung"),
        review("der Lebenslauf"),
        match(
            [
                ("der Azubi", "makes a vocational training"),
                ("das Vorstellungsgespräch", "you meet the company"),
                ("der Lebenslauf", "your school and jobs on paper"),
                ("das Gehalt", "the money you earn per month"),
                ("die Weiterbildung", "learning more for your job"),
            ],
            "What does it mean?",
        ),
        mc(
            "Die Prüfung war nicht schriftlich, sondern ...",
            "mündlich.",
            "kreativ.",
            "unzufrieden.",
        ),
        mc(
            "Nach der Schule macht Tom eine ___ als Koch.",
            "Ausbildung",
            "Karriere",
            "Verantwortung",
        ),
        fill("Ich habe mich bei einer Firma ___. (sich bewerben)", "beworben"),
        fill("Sie hat ihren Job ___. Sie sucht etwas Neues. (kündigen)", "gekündigt"),
        tr("I enjoy the work.", "Die Arbeit macht mir Spaß."),
    ),
    lesson(
        "Der Beruf, der zu mir passt",
        grammar("Relativsätze im Nominativ"),
        mc("Das ist der Beruf, ___ zu mir passt.", "der", "die", "das"),
        mc("Ich suche eine Arbeit, ___ mir Spaß macht.", "die", "der", "das"),
        mc("Das ist ein Unternehmen, ___ 500 Leute beschäftigt.", "das", "der", "die"),
        mc("Ich mag Kollegen, ___ hilfsbereit sind.", "die", "der", "den"),
        fill("Ich suche einen Job, der kreativ ___. (sein)", "ist"),
        fill("Sie hat eine Stelle, ___ gut bezahlt ist.", "die"),
        mc(
            "Which sentence is correct?",
            "Ich suche einen Beruf, der kreativ ist.",
            "Ich suche einen Beruf, der ist kreativ.",
            "Ich suche einen Beruf, ist der kreativ.",
        ),
        order("Das ist die Firma, die mein Vater gegründet hat."),
        tr(
            "I want a job that is interesting.",
            "Ich möchte einen Beruf, der interessant ist.|Ich will einen Beruf, der interessant ist.",
        ),
    ),
    lesson(
        "Der Kollege, den ich kenne",
        grammar("Relativsätze im Akkusativ"),
        mc("Der Kollege, ___ ich kenne, ist nett.", "den", "der", "dem"),
        mc("Der Kollege, ___ hier arbeitet, ist nett.", "der", "den", "dem"),
        mc("Das ist die Kollegin, ___ ich gestern getroffen habe.", "die", "der", "den"),
        mc("Das ist das Buch, ___ ich lese.", "das", "den", "der"),
        fill("Das ist der Beruf, ___ ich immer wollte.", "den"),
        fill("Der Chef, den wir jetzt ___, ist fair. (haben)", "haben"),
        fill("Die Bewerbung, die ich geschrieben ___, ist gut. (haben)", "habe"),
        order("Das ist der Lebenslauf, den ich geschrieben habe."),
        tr("The colleague that I know is nice.", "Der Kollege, den ich kenne, ist nett."),
    ),
    lesson(
        "Mein Traumberuf",
        bank(
            "Ich mache eine ___ als Mediengestalterin. Das ist ein Beruf, ___ sehr kreativ ist. "
            "Zweimal pro Woche gehe ich in die ___. Die Arbeitszeiten sind gut und das "
            "___ ist okay. Am meisten gefällt mir das Team, ___ ich jeden Tag sehe. Der Beruf "
            "passt wirklich zu ___!",
            ["Ausbildung", "der", "Berufsschule", "Gehalt", "das", "mir"],
            "den",
            "Karriere",
        ),
        mc(
            "What does she like most?",
            "The team.",
            "The salary.",
            "The vocational school.",
        ),
        mc(
            "Ich bin mit meinem Arbeitsplatz unzufrieden. means:",
            "I'm not happy with my workplace.",
            "I'm very happy with my workplace.",
            "I don't have a workplace.",
        ),
        fill("Das ist eine große ___. Ich habe 20 Mitarbeiter. (responsibility)", "Verantwortung"),
        fill("Die Firma ___ 300 Leute. (beschäftigen)", "beschäftigt"),
        tr("The job that suits me.", "Der Beruf, der zu mir passt."),
    ),
    lesson(
        "Lektion 23: Test",
        mc("Das ist die Stelle, ___ mich interessiert.", "die", "der"),
        mc("Der Mann, ___ ich angerufen habe, ist mein Chef.", "den", "der"),
        fill("Ich suche ein Team, ___ nett ist.", "das"),
        fill("Ich habe mich um die Stelle ___. (sich bewerben)", "beworben"),
        mc("Das Gespräch war ___, nicht schriftlich.", "mündlich", "kreativ"),
        order("Ich suche eine Arbeit, die mir Spaß macht."),
        tr("I have a job interview tomorrow.", "Ich habe morgen ein Vorstellungsgespräch."),
    ),
]

LEKTION_23 = unit(
    23,
    "Der Beruf, der zu mir passt.",
    "Ausbildung und Beruf",
    L23_WORDS,
    L23_RULES,
    sections(L23_LESSONS, vocab_lessons(L23_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 24: Wie sah dein Alltag aus?
# ============================================================================

L24_WORDS = [
    ("the stay abroad", "der Auslandsaufenthalt", "noun", "Pl. die Auslandsaufenthalte"),
    ("the semester abroad", "das Auslandssemester", "noun", "Pl. die Auslandssemester"),
    ("the exchange", "der Austausch", "noun"),
    ("the everyday life", "der Alltag", "noun"),
    ("the daily routine", "der Tagesablauf", "noun", "Pl. die Tagesabläufe"),
    ("the host family", "die Gastfamilie", "noun", "Pl. die Gastfamilien"),
    ("the culture", "die Kultur", "noun", "Pl. die Kulturen"),
    ("the challenge", "die Herausforderung", "noun", "Pl. die Herausforderungen"),
    ("the assignment / order", "der Auftrag", "noun", "Pl. die Aufträge"),
    ("the end of the working day", "der Feierabend", "noun", "Feierabend machen"),
    ("the homesickness", "das Heimweh", "noun"),
    ("to get used to", "sich gewöhnen", "verb", "an + Akk."),
    ("to feel comfortable", "sich wohlfühlen", "verb"),
    ("to find one's way / settle in", "sich zurechtfinden", "verb", "hat sich zurechtgefunden"),
    ("disappointed", "enttäuscht", "adjective"),
    ("unfamiliar / unusual", "ungewohnt", "adjective"),
    ("pleasant", "angenehm", "adjective"),
    ("finally / in the end", "schließlich", "adverb"),
    ("during", "während", "other", "während dieser Zeit"),
    ("What was your everyday life like?", "Wie sah dein Alltag aus?", "phrase"),
    ("At first it was difficult.", "Am Anfang war es schwierig.", "phrase"),
]

L24_RULES = [
    rule(
        "Präteritum: regelmäßige und unregelmäßige Verben",
        "verbs",
        """
Stories and reports use the **Präteritum**.

**Regular** verbs: stem + **-te**: *arbeiten → ich arbeit**ete**, wohnen → ich
wohn**te***.

**Irregular** verbs change the vowel and have **no ending** for *ich / er*:

| infinitive | ich / er / sie | wir / sie |
|---|---|---|
| sehen | **sah** | sahen |
| fahren | **fuhr** | fuhren |
| gehen | **ging** | gingen |
| kommen | **kam** | kamen |
| stehen (auf) | **stand** (auf) | standen |
| treffen | **traf** | trafen |
| essen | **aß** | aßen |
| finden | **fand** | fanden |

Endings: *ich sah, du sah**st**, er sah, wir sah**en**, ihr sah**t**, sie sah**en***.
Separable verbs split as usual: *Ich **stand** um sechs Uhr **auf**.*
""",
        [
            "Wie sah dein Alltag aus?",
            "Jeden Morgen fuhr ich mit dem Bus zur Arbeit.",
            "Am Abend traf ich oft Kollegen.",
        ],
    ),
    rule(
        "Präteritum oder Perfekt?",
        "other",
        """
Both talk about the past. The difference is mostly **style**:

| Perfekt | Präteritum |
|---|---|
| speaking, chats, e-mails to friends | written stories, reports, news |
| *Ich **bin** nach Wien **gefahren**.* | *Ich **fuhr** nach Wien.* |

In speaking, too, people almost always use the Präteritum of **sein, haben** and
the **modal verbs**: *Ich **war** müde. Ich **hatte** keine Zeit. Ich **musste**
arbeiten.*

To tell the story in order: *zuerst, dann, danach, später, **während** dieser Zeit,
am Anfang, **schließlich**, am Ende*.
""",
        [
            "Am Anfang war alles neu, schließlich fühlte ich mich wohl.",
            "Während dieser Zeit lernte ich viel über die Kultur.",
            "Ich habe in Spanien gearbeitet. Ich hatte dort eine schöne Wohnung.",
        ],
    ),
]

L24_LESSONS = [
    lesson(
        "Arbeiten im Ausland",
        review("der Alltag"),
        review("die Herausforderung"),
        match(
            [
                ("die Gastfamilie", "the host family"),
                ("das Heimweh", "the homesickness"),
                ("der Feierabend", "the end of the working day"),
                ("der Austausch", "the exchange"),
                ("der Tagesablauf", "the daily routine"),
            ]
        ),
        mc(
            "Ich vermisse meine Familie und meine Stadt. Ich habe ...",
            "Heimweh.",
            "Feierabend.",
            "einen Auftrag.",
        ),
        mc(
            "Das Essen war am Anfang ___ für mich. Ich kannte es nicht.",
            "ungewohnt",
            "angenehm",
            "enttäuscht",
        ),
        fill("Nach ein paar Wochen habe ich mich an das Wetter ___. (sich gewöhnen)", "gewöhnt"),
        fill("Ich habe mich in der Firma sehr ___. (sich wohlfühlen)", "wohlgefühlt"),
        tr("At first it was difficult.", "Am Anfang war es schwierig."),
    ),
    lesson(
        "Wie sah dein Alltag aus?",
        grammar("Präteritum: regelmäßige und unregelmäßige Verben"),
        match(
            [
                ("sehen", "sah"),
                ("fahren", "fuhr"),
                ("gehen", "ging"),
                ("treffen", "traf"),
                ("essen", "aß"),
            ],
            "Match the Präteritum.",
        ),
        conj("arbeiten", "ich (Präteritum)", "arbeitete"),
        conj("wohnen", "wir (Präteritum)", "wohnten"),
        conj("kommen", "er (Präteritum)", "kam"),
        conj("finden", "du (Präteritum)", "fandest|fandst"),
        fill("Jeden Morgen ___ ich um sechs Uhr auf. (aufstehen, Präteritum)", "stand"),
        fill("Am Abend ___ wir oft Kollegen. (treffen, Präteritum)", "trafen"),
        fill("Wie ___ dein Alltag aus? (aussehen, Präteritum)", "sah"),
        mc(
            "Ich fahre mit dem Bus. → Präteritum:",
            "Ich fuhr mit dem Bus.",
            "Ich fahrte mit dem Bus.",
            "Ich führ mit dem Bus.",
        ),
        order("Jeden Morgen fuhr ich mit dem Rad zur Arbeit."),
    ),
    lesson(
        "Erzählen",
        grammar("Präteritum oder Perfekt?"),
        mc(
            "In a chat with a friend, you'd usually write:",
            "Ich bin gestern nach Wien gefahren.",
            "Ich fuhr gestern nach Wien.",
        ),
        mc(
            "Even in speaking, people say:",
            "Ich war müde.",
            "Ich bin müde gewesen gehabt.",
            "Ich habe müde.",
        ),
        fill("Am Anfang war alles neu, ___ fühlte ich mich wohl. (finally)", "schließlich"),
        fill("___ dieser Zeit lernte ich viel. (during)", "Während"),
        fill("Zuerst ___ ich in einer Gastfamilie. (wohnen, Präteritum)", "wohnte"),
        order("Während dieser Zeit lernte ich viel über die Kultur."),
        tr("I had a nice flat there.", "Ich hatte dort eine schöne Wohnung."),
    ),
    lesson(
        "Ein Jahr in Kanada",
        bank(
            "2022 ___ ich ein Jahr in Toronto. Ich arbeitete für eine Firma, die Software "
            "entwickelt. Am Anfang ___ alles ungewohnt und ich hatte oft ___. Ich ___ jeden "
            "Morgen um sieben auf und ___ mit der U-Bahn ins Büro. Nach ein paar Monaten "
            "hatte ich mich an alles ___. Schließlich wollte ich gar nicht mehr nach Hause!",
            ["arbeitete", "war", "Heimweh", "stand", "fuhr", "gewöhnt"],
            "sah",
            "Feierabend",
        ),
        mc(
            "How did the writer feel at the end?",
            "They didn't want to go home.",
            "They were very homesick.",
            "They were disappointed.",
        ),
        mc(
            "What was hard at the beginning?",
            "Everything was unfamiliar.",
            "The work was boring.",
            "The flat was too small.",
        ),
        fill("Ich war ___, weil die Wohnung so klein war. (disappointed)", "enttäuscht"),
        fill("In einer neuen Stadt muss man sich erst ___. (find one's way)", "zurechtfinden"),
        tr("What was your everyday life like?", "Wie sah dein Alltag aus?"),
    ),
    lesson(
        "Lektion 24: Test",
        fill("Gestern ___ ich einen alten Freund. (treffen, Präteritum)", "traf"),
        fill("Wir ___ in einem kleinen Haus. (wohnen, Präteritum)", "wohnten"),
        mc("gehen → Präteritum (ich)", "ging", "gehte"),
        mc("Nach drei Monaten habe ich mich an die Arbeit ___.", "gewöhnt", "gewohnt"),
        fill("Das Wetter war sehr ___. (pleasant)", "angenehm"),
        order("Am Anfang hatte ich oft Heimweh."),
        tr(
            "I felt comfortable there.",
            "Ich fühlte mich dort wohl.|Ich habe mich dort wohlgefühlt.",
        ),
    ),
    lesson(
        "Modul 8: Wiederholung",
        mc("___ ich in der Stadt wohne, fahre ich kein Auto.", "Seit", "Bis"),
        fill("Ich warte, bis der Zug ___. (kommen)", "kommt"),
        fill("Ich lerne seit ___ Jahr Deutsch. (ein)", "einem"),
        fill("Das ist der Beruf, ___ zu mir passt.", "der"),
        fill("Das ist die Kollegin, ___ ich gestern getroffen habe.", "die"),
        mc("Der Chef, ___ ich kenne, ist nett.", "den", "der"),
        fill("Jeden Abend ___ ich mit Freunden. (essen, Präteritum)", "aß"),
        fill("Wie ___ dein Tagesablauf aus? (aussehen, Präteritum)", "sah"),
        bank(
            "Seit ich im Ausland ___, ist mein Alltag anders. Ich habe einen Job, ___ mir viel "
            "Spaß macht. Am Anfang ___ alles schwierig, aber jetzt fühle ich mich wohl.",
            ["arbeite", "der", "war"],
            "den",
            "bin",
        ),
        tr(
            "I'm looking for a job that suits me.",
            "Ich suche einen Beruf, der zu mir passt.|Ich suche einen Job, der zu mir passt.",
        ),
        order("Seit ich hier wohne, fahre ich jeden Tag Fahrrad."),
    ),
]

LEKTION_24 = unit(
    24,
    "Wie sah dein Alltag aus?",
    "Arbeiten im Ausland",
    L24_WORDS,
    L24_RULES,
    sections(L24_LESSONS, vocab_lessons(L24_WORDS, "Wörter")),
)


UNITS = [LEKTION_22, LEKTION_23, LEKTION_24]
