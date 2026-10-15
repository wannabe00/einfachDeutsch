"""Modul 7 (A2.2): Lektion 19 (Wohin gehen wir heute?), 20 (Ich durfte
eigentlich keine Comics lesen.), 21 (Ja genau, den meine ich.)."""

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
# Lektion 19: Wohin gehen wir heute?
# ============================================================================

L19_WORDS = [
    ("the reading (by an author)", "die Lesung", "noun", "Pl. die Lesungen"),
    ("the performance", "die Aufführung", "noun", "Pl. die Aufführungen"),
    ("the show / screening", "die Vorstellung", "noun", "Pl. die Vorstellungen"),
    ("the admission", "der Eintritt", "noun", "Eintritt frei"),
    ("the ticket price", "der Eintrittspreis", "noun", "Pl. die Eintrittspreise"),
    ("the box office", "die Kasse", "noun", "an der Abendkasse"),
    ("the artist", "der Künstler", "noun", "f. die Künstlerin"),
    ("the venue", "der Veranstaltungsort", "noun", "Pl. die Veranstaltungsorte"),
    ("the events calendar", "der Veranstaltungskalender", "noun"),
    ("the programme booklet", "das Programmheft", "noun", "Pl. die Programmhefte"),
    ("the cabaret", "das Kabarett", "noun"),
    ("the circus", "der Zirkus", "noun", "Pl. die Zirkusse"),
    ("the comedy (show)", "die Comedy", "noun"),
    ("to take place", "stattfinden", "verb", "hat stattgefunden"),
    ("to convince", "überzeugen", "verb", "hat überzeugt"),
    ("to inspire / delight", "begeistern", "verb", "hat begeistert"),
    ("to decide", "sich entscheiden", "verb", "für + Akk., hat sich entschieden"),
    ("to take part", "teilnehmen", "verb", "an + Dat., hat teilgenommen"),
    ("sold out", "ausverkauft", "adjective"),
    ("enthusiastic", "begeistert", "adjective"),
    ("What's on today?", "Was läuft heute?", "phrase"),
    ("How about ...?", "Wie wäre es mit ...?", "phrase"),
    ("Count me in.", "Da bin ich dabei.", "phrase"),
    ("Come along!", "Komm doch mit!", "phrase"),
    ("I'm not so keen.", "Ich bin nicht so begeistert.", "phrase"),
]

L19_RULES = [
    rule(
        "Vorschläge machen und reagieren",
        "sentence_structure",
        """
Ways to **suggest** something:

- ***Wollen wir** ins Kabarett gehen?*
- ***Wie wäre es mit** einem Konzert?* (mit + Dativ)
- ***Wir könnten** zur Lesung gehen.*
- ***Ich schlage vor, dass** wir ins Theater **gehen**.* (verb at the end)
- ***Hast du Lust**, in den Zirkus **zu gehen**?*

Reacting:

| yes | not sure / no |
|---|---|
| *Gute Idee! · Da bin ich dabei. · Das klingt gut.* | *Na ja, ich weiß nicht ... · Ich würde lieber ...* |
| *Super, ich komme mit.* | *Vielleicht ein anderes Mal. · Ich habe leider keine Zeit.* |
""",
        [
            "Wie wäre es mit einer Lesung?",
            "Ich schlage vor, dass wir zuerst essen gehen.",
            "Na ja, ich würde lieber ins Kino gehen.",
        ],
    ),
    rule(
        "Wörter aus anderen Sprachen",
        "other",
        """
Many culture words come from English, French or Italian. They often keep their
**foreign plural -s** and their own **stress**:

| word | plural | stress |
|---|---|---|
| das Festival | die Festival**s** | FEStival |
| das Musical | die Musical**s** | MUsical |
| das Kabarett | (no plural) | kabaRETT |
| der Zirkus | die Zirkus**se** | ZIRkus |
| das Konzert | die Konzert**e** | konZERT |
| das Theater | die Theater | teAter |

Words ending in **-ion** are always feminine and stressed on the last
syllable: *die Informati**on**, die Präsentati**on***.
""",
        [
            "Im Sommer gibt es viele Festivals.",
            "Die Comedy gestern war sehr lustig.",
            "Das Kabarett findet im Theater statt.",
        ],
    ),
]

L19_LESSONS = [
    lesson(
        "Was läuft heute?",
        review("die Lesung"),
        review("die Aufführung"),
        match(
            [
                ("die Lesung", "an author reads from a book"),
                ("der Zirkus", "animals and acrobats"),
                ("das Kabarett", "funny, political show"),
                ("die Vorstellung", "a show at the cinema or theatre"),
                ("die Kasse", "where you buy tickets"),
            ],
            "What is it?",
        ),
        mc(
            "Es gibt keine Karten mehr. Das Konzert ist ...",
            "ausverkauft.",
            "begeistert.",
            "stattgefunden.",
        ),
        mc(
            "Eintritt frei! means:",
            "You don't have to pay.",
            "The entrance is closed.",
            "You can come in at any time.",
        ),
        fill("Das Festival ___ im Park statt. (stattfinden)", "findet"),
        tr("What's on today?", "Was läuft heute?"),
    ),
    lesson(
        "Wie wäre es mit ...?",
        grammar("Vorschläge machen und reagieren"),
        mc("Wie wäre es ___ einem Konzert?", "mit", "von", "für"),
        mc(
            "Which sentence is correct?",
            "Ich schlage vor, dass wir ins Theater gehen.",
            "Ich schlage vor, dass wir gehen ins Theater.",
            "Ich schlage vor, dass gehen wir ins Theater.",
        ),
        fill("___ wir ins Kabarett gehen? (shall we: wollen)", "Wollen"),
        fill("Wir ___ zur Lesung gehen. (could)", "könnten"),
        mc(
            "You like the idea:",
            "Da bin ich dabei!",
            "Na ja, ich weiß nicht.",
            "Vielleicht ein anderes Mal.",
        ),
        mc(
            "You're not sure:",
            "Na ja, ich würde lieber ins Kino gehen.",
            "Gute Idee!",
            "Super, ich komme mit.",
        ),
        order("Wie wäre es mit einer Lesung?", "Build the question."),
        tr("Come along!", "Komm doch mit!"),
    ),
    lesson(
        "Festivals und Musicals",
        grammar("Wörter aus anderen Sprachen"),
        mc("Plural: das Festival → die ...", "Festivals", "Festivale", "Festivalen"),
        mc("Plural: das Musical → die ...", "Musicals", "Musicale", "Musicalen"),
        mc("Plural: der Zirkus → die ...", "Zirkusse", "Zirkuss", "Zirkusen"),
        mc("Plural: das Konzert → die ...", "Konzerte", "Konzerts", "Konzerten"),
        fill("Im Sommer gibt es viele ___. (festivals)", "Festivals"),
        fill("Die ___ war sehr lustig. (comedy show)", "Comedy"),
        tr("The cabaret takes place in the theatre.", "Das Kabarett findet im Theater statt."),
    ),
    lesson(
        "Wir planen den Abend",
        bank(
            "Hast du heute Abend Zeit? Im ___ steht, dass es eine Lesung gibt. Na ja, ich weiß "
            "nicht. Wie ___ es mit dem Zirkus? Der ist leider ___. Dann schlage ich vor, ___ "
            "wir ins Kabarett gehen. Gute Idee, da bin ich ___!",
            ["Veranstaltungskalender", "wäre", "ausverkauft", "dass", "dabei"],
            "würde",
            "begeistert",
        ),
        mc(
            "Where do they go in the end?",
            "To the cabaret.",
            "To the circus.",
            "To the reading.",
        ),
        mc(
            "Why don't they go to the circus?",
            "It's sold out.",
            "It's too expensive.",
            "It's boring.",
        ),
        fill("Das Publikum war ___. (enthusiastic)", "begeistert"),
        fill("Du hast mich ___. Ich komme mit! (überzeugen)", "überzeugt"),
        fill("Wir haben uns für das Theater ___. (sich entscheiden)", "entschieden"),
        tr("I'm taking part in a dance course.", "Ich nehme an einem Tanzkurs teil."),
    ),
    lesson(
        "Lektion 19: Test",
        mc("Wie wäre es ___ dem Kino?", "mit", "zu"),
        fill("Ich schlage vor, dass wir zu Hause ___. (bleiben)", "bleiben"),
        fill("Das Konzert ist ___. Es gibt keine Karten mehr. (sold out)", "ausverkauft"),
        mc("Plural: das Musical", "die Musicals", "die Musicale"),
        fill("Wann ___ die Lesung statt? (finden)", "findet"),
        order("Ich schlage vor, dass wir ins Kabarett gehen."),
        tr("Count me in.", "Da bin ich dabei."),
    ),
]

LEKTION_19 = unit(
    19,
    "Wohin gehen wir heute?",
    "Kulturelle Veranstaltungen",
    L19_WORDS,
    L19_RULES,
    sections(L19_LESSONS, vocab_lessons(L19_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 20: Ich durfte eigentlich keine Comics lesen.
# ============================================================================

L20_WORDS = [
    ("the picture book", "das Bilderbuch", "noun", "Pl. die Bilderbücher"),
    ("the comic", "der Comic", "noun", "Pl. die Comics"),
    ("the novel", "der Roman", "noun", "Pl. die Romane"),
    ("the fairy tale", "das Märchen", "noun", "Pl. die Märchen"),
    ("the poem", "das Gedicht", "noun", "Pl. die Gedichte"),
    ("the paperback", "das Taschenbuch", "noun", "Pl. die Taschenbücher"),
    ("the article", "der Artikel", "noun", "Pl. die Artikel"),
    ("the report", "der Bericht", "noun", "Pl. die Berichte"),
    ("the press", "die Presse", "noun"),
    ("the author", "der Autor", "noun", "f. die Autorin"),
    ("the reader", "der Leser", "noun", "f. die Leserin"),
    ("the publisher", "der Verlag", "noun", "Pl. die Verlage"),
    ("the bookshop", "die Buchhandlung", "noun", "Pl. die Buchhandlungen"),
    ("the bookmark", "das Lesezeichen", "noun", "Pl. die Lesezeichen"),
    ("the page", "die Seite", "noun", "Pl. die Seiten"),
    ("the chapter (of a book)", "das Kapitel", "noun", "Pl. die Kapitel"),
    ("the title", "der Titel", "noun", "Pl. die Titel"),
    ("the hero", "der Held", "noun", "f. die Heldin"),
    ("the literature", "die Literatur", "noun"),
    ("to read aloud", "vorlesen", "verb", "liest vor, hat vorgelesen"),
    ("to publish", "veröffentlichen", "verb", "hat veröffentlicht"),
    ("to allow", "erlauben", "verb", "hat erlaubt"),
    ("to forbid", "verbieten", "verb", "hat verboten"),
    ("to stay up", "aufbleiben", "verb", "ist aufgeblieben"),
    ("That's not for me.", "Das ist nichts für mich.", "phrase"),
    ("I most like reading ...", "Ich lese am liebsten ...", "phrase"),
    (
        "I wasn't really allowed to read comics.",
        "Ich durfte eigentlich keine Comics lesen.",
        "phrase",
    ),
]

L20_RULES = [
    rule(
        "Präteritum: Modalverben",
        "verbs",
        """
For the past, modal verbs use the **Präteritum**: no umlaut, **-te** endings.

| | dürfen | können | müssen | wollen | sollen | mögen |
|---|---|---|---|---|---|---|
| ich | **durfte** | **konnte** | **musste** | **wollte** | **sollte** | **mochte** |
| du | durftest | konntest | musstest | wolltest | solltest | mochtest |
| er / sie | durfte | konnte | musste | wollte | sollte | mochte |
| wir | durften | konnten | mussten | wollten | sollten | mochten |
| ihr | durftet | konntet | musstet | wolltet | solltet | mochtet |
| sie / Sie | durften | konnten | mussten | wollten | sollten | mochten |

The second verb stays at the end: *Als Kind **durfte** ich keine Comics **lesen**.*
*ich* and *er/sie* have the same form, as with *war* and *hatte*.
""",
        [
            "Ich musste jeden Abend um acht ins Bett gehen.",
            "Mein Bruder konnte schon mit vier Jahren lesen.",
            "Wir wollten immer länger aufbleiben.",
        ],
    ),
    rule(
        "Modalverben ohne zweites Verb",
        "sentence_structure",
        """
When the meaning is clear, the **second verb can be left out**:

- *Ich **durfte** das nicht.* (= das nicht machen)
- *Er **konnte** gut Englisch.* (= sprechen)
- *Ich **mochte** keine Märchen.* (mögen usually stands alone)
- *Wir **wollten** nach Hause.* (= gehen / fahren)

*eigentlich* (actually) softens a statement or shows a contrast:
*Ich durfte **eigentlich** keine Comics lesen, aber ich habe sie heimlich gelesen.*
""",
        [
            "Ich mochte als Kind keine Gedichte.",
            "Durftest du das?",
            "Eigentlich wollte ich Autor werden.",
        ],
    ),
]

L20_LESSONS = [
    lesson(
        "Bücher und Presse",
        review("der Roman"),
        review("das Märchen"),
        match(
            [
                ("der Autor", "writes the book"),
                ("der Verlag", "publishes the book"),
                ("die Buchhandlung", "sells the book"),
                ("der Leser", "reads the book"),
                ("das Lesezeichen", "marks the page"),
            ],
            "Who or what?",
        ),
        mc(
            "Ein Buch mit vielen Bildern für kleine Kinder ist ein ...",
            "Bilderbuch.",
            "Roman.",
            "Bericht.",
        ),
        mc(
            "Zeitungen und Zeitschriften zusammen nennt man die ...",
            "Presse.",
            "Literatur.",
            "Seite.",
        ),
        fill("Meine Mutter hat mir jeden Abend ein Märchen ___. (vorlesen)", "vorgelesen"),
        fill("Das Buch hat 300 ___. (pages)", "Seiten"),
        tr("That's not for me.", "Das ist nichts für mich."),
    ),
    lesson(
        "Ich durfte ...",
        grammar("Präteritum: Modalverben"),
        conj("dürfen", "ich (Präteritum)", "durfte"),
        conj("können", "du (Präteritum)", "konntest"),
        conj("müssen", "wir (Präteritum)", "mussten"),
        conj("wollen", "ihr (Präteritum)", "wolltet"),
        conj("sollen", "er (Präteritum)", "sollte"),
        conj("mögen", "ich (Präteritum)", "mochte"),
        fill("Als Kind ___ ich keine Comics lesen. (dürfen)", "durfte"),
        fill("Wir ___ jeden Abend früh ins Bett gehen. (müssen)", "mussten"),
        fill("Mein Bruder ___ schon mit vier Jahren lesen. (können)", "konnte"),
        mc(
            "Ich muss jeden Tag lesen. → Past:",
            "Ich musste jeden Tag lesen.",
            "Ich müsste jeden Tag lesen.",
            "Ich habe jeden Tag lesen gemusst.",
        ),
        order("Wir wollten immer länger aufbleiben."),
        tr("As a child I wasn't allowed to watch TV.", "Als Kind durfte ich nicht fernsehen."),
    ),
    lesson(
        "Ich mochte keine Gedichte",
        grammar("Modalverben ohne zweites Verb"),
        mc("Ich ___ als Kind keine Gedichte. (didn't like)", "mochte", "möchte", "mag"),
        mc("___ du das? (were you allowed)", "Durftest", "Darfst", "Dürftest"),
        fill("Früher ___ er gut Englisch. (was able to)", "konnte"),
        fill("Wir ___ nach Hause. (wanted)", "wollten"),
        fill("Ich durfte ___ keine Comics lesen. (actually)", "eigentlich"),
        mc(
            "Eigentlich wollte ich Autor werden. means:",
            "Actually I wanted to become an author.",
            "I finally became an author.",
            "I never wanted to be an author.",
        ),
        tr("I didn't like fairy tales.", "Ich mochte keine Märchen."),
    ),
    lesson(
        "Lesen früher und heute",
        bank(
            "Als Kind ___ ich eigentlich keine Comics lesen. Meine Eltern haben sie ___. Ich "
            "___ aber viele Bilderbücher und Märchen lesen. Abends hat mir mein Vater oft "
            "___. Heute lese ich am liebsten ___, besonders Krimis. Und Comics? Die lese ich "
            "jetzt jeden Tag!",
            ["durfte", "verboten", "konnte", "vorgelesen", "Romane"],
            "musste",
            "erlaubt",
        ),
        mc(
            "What does the writer like reading most today?",
            "Novels, especially crime novels.",
            "Fairy tales.",
            "Poems.",
        ),
        mc(
            "Ich lese am liebsten Krimis. means:",
            "I like reading crime novels most.",
            "I read crime novels very rarely.",
            "I have to read crime novels.",
        ),
        fill("Der Verlag hat das Buch 2020 ___. (veröffentlichen)", "veröffentlicht"),
        fill("Meine Eltern haben mir alles ___. (erlauben)", "erlaubt"),
        tr(
            "Who is the hero of the novel?",
            "Wer ist der Held des Romans?|Wer ist der Held vom Roman?",
        ),
    ),
    lesson(
        "Lektion 20: Test",
        fill("Als Kind ___ ich nicht lange fernsehen. (dürfen)", "durfte"),
        fill("Früher ___ wir viel lesen. (sollen)", "sollten"),
        mc("Ich ___ als Kind keinen Fisch.", "mochte", "möchte"),
        fill("Gestern ___ ihr früh aufstehen. (müssen)", "musstet"),
        fill("Sie ___ Ärztin werden. (wanted)", "wollte"),
        order("Mein Vater hat mir jeden Abend vorgelesen."),
        tr("I wasn't really allowed to read comics.", "Ich durfte eigentlich keine Comics lesen."),
    ),
]

LEKTION_20 = unit(
    20,
    "Ich durfte eigentlich keine Comics lesen.",
    "Bücher und Presse",
    L20_WORDS,
    L20_RULES,
    sections(L20_LESSONS, vocab_lessons(L20_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 21: Ja genau, den meine ich.
# ============================================================================

L21_WORDS = [
    ("the ID card", "der Ausweis", "noun", "Pl. die Ausweise"),
    ("the passport", "der Reisepass", "noun", "Pl. die Reisepässe; also: der Pass"),
    ("the visa", "das Visum", "noun", "Pl. die Visa"),
    ("the residence permit", "die Aufenthaltsgenehmigung", "noun"),
    ("the health insurance card", "die Gesundheitskarte", "noun"),
    ("the customer card", "die Kundenkarte", "noun", "Pl. die Kundenkarten"),
    ("the bank card", "die EC-Karte", "noun", "Pl. die EC-Karten"),
    ("the cash", "das Bargeld", "noun"),
    ("the wallet", "die Geldbörse", "noun", "Pl. die Geldbörsen"),
    ("the application", "der Antrag", "noun", "Pl. die Anträge"),
    ("the authority", "die Behörde", "noun", "Pl. die Behörden"),
    ("the public office", "das Amt", "noun", "Pl. die Ämter"),
    ("the citizens' office", "das Bürgeramt", "noun", "Pl. die Bürgerämter"),
    ("the administration", "die Verwaltung", "noun"),
    ("the lost property office", "das Fundbüro", "noun", "Pl. die Fundbüros"),
    ("the crime", "das Verbrechen", "noun", "Pl. die Verbrechen"),
    ("the culprit", "der Täter", "noun", "f. die Täterin"),
    ("the witness", "der Zeuge", "noun", "f. die Zeugin"),
    ("the burglary", "der Einbruch", "noun", "Pl. die Einbrüche"),
    ("the theft", "der Diebstahl", "noun", "Pl. die Diebstähle"),
    ("the insurance", "die Versicherung", "noun", "Pl. die Versicherungen"),
    ("the police officer", "der Polizist", "noun", "f. die Polizistin"),
    ("to steal", "stehlen", "verb", "stiehlt, hat gestohlen"),
    ("to break in", "einbrechen", "verb", "bricht ein, ist eingebrochen"),
    ("to touch", "anfassen", "verb", "hat angefasst"),
    ("to report", "melden", "verb", "hat gemeldet"),
    ("to report (to the police)", "anzeigen", "verb", "hat angezeigt"),
    ("to secure / to cordon off", "absperren", "verb", "hat abgesperrt"),
    ("to let / to have done", "lassen", "verb", "lässt, hat gelassen"),
    ("Yes, exactly, that's the one I mean.", "Ja genau, den meine ich.", "phrase"),
    ("I've lost my ID card.", "Ich habe meinen Ausweis verloren.", "phrase"),
]

L21_RULES = [
    rule(
        "welcher? dieser! der hier!",
        "pronouns",
        """
To ask **which**, use *welch-* with the endings of *der, die, das*. To answer,
point with **der, die, das** (stressed) or *dieser*:

| | masculine | feminine | neuter | plural |
|---|---|---|---|---|
| Nominativ | **Welcher** Pass? **Der** hier. | **Welche** Karte? **Die** hier. | **Welches** Formular? **Das** hier. | **Welche** Ausweise? **Die** hier. |
| Akkusativ | **Welchen** Pass? **Den** hier. | **Welche** Karte? **Die**. | **Welches** Formular? **Das**. | **Welche**? **Die**. |
| Dativ | **Welchem**? **Dem**. | **Welcher**? **Der**. | **Welchem**? **Dem**. | **Welchen**? **Denen**. |

- *Meinen Sie diesen Ausweis? Ja genau, **den** meine ich.*
The pronoun takes the case of its **own** sentence.
""",
        [
            "Welchen Antrag muss ich ausfüllen? Den hier.",
            "Welche Karte brauchen Sie? Die blaue.",
            "Mit welchem Formular? Mit dem hier.",
        ],
    ),
    rule(
        "lassen",
        "verbs",
        """
**lassen** (lässt, ließ, hat gelassen) has three meanings:

| meaning | example |
|---|---|
| **leave** something | *Ich **lasse** den Pass zu Hause.* |
| **let / allow** | ***Lass** mich bitte ausreden!* |
| **have something done** | *Ich **lasse** mein Auto **reparieren**.* |

In "have something done", *lassen* is conjugated and the other verb is an
**infinitive at the end**: *Wir **lassen** das Schloss **wechseln**.*
du / er: *du **lässt**, er **lässt*** (with umlaut).
""",
        [
            "Ich lasse meinen Ausweis verlängern.",
            "Lass das bitte liegen, nicht anfassen!",
            "Sie lässt die Tür reparieren.",
        ],
    ),
]

L21_LESSONS = [
    lesson(
        "Dokumente",
        review("der Ausweis"),
        review("der Antrag"),
        match(
            [
                ("das Visum", "the visa"),
                ("das Bargeld", "the cash"),
                ("die Geldbörse", "the wallet"),
                ("die Behörde", "the authority"),
                ("das Fundbüro", "the lost property office"),
            ]
        ),
        mc(
            "Für eine Reise nach Amerika braucht man einen ...",
            "Reisepass.",
            "Antrag.",
            "Diebstahl.",
        ),
        mc(
            "Einen neuen Ausweis bekommt man im ...",
            "Bürgeramt.",
            "Fundbüro.",
            "Einbruch.",
        ),
        fill("Ich habe meinen Ausweis ___. (verlieren)", "verloren"),
        fill("Für ein Visum muss man einen ___ stellen. (application)", "Antrag"),
        tr("I've lost my wallet.", "Ich habe meine Geldbörse verloren."),
    ),
    lesson(
        "Welcher? Der hier!",
        grammar("welcher? dieser! der hier!"),
        mc("___ Formular muss ich ausfüllen?", "Welches", "Welcher", "Welchen"),
        mc("___ Pass ist deiner?", "Welcher", "Welchen", "Welches"),
        mc("___ Ausweis soll ich zeigen?", "Welchen", "Welcher", "Welchem"),
        mc("Meinen Sie diesen Antrag? Ja genau, ___ meine ich.", "den", "der", "dem"),
        fill("Welche Karte brauchen Sie? ___ hier. (die)", "Die"),
        fill("Welches Visum hast du? ___ hier. (das)", "Das"),
        fill("Mit ___ Formular? Mit dem hier. (welch-)", "welchem"),
        order("Welchen Ausweis meinen Sie?", "Build the question."),
        tr("Yes, exactly, that's the one I mean.", "Ja genau, den meine ich."),
    ),
    lesson(
        "Ich lasse das Auto reparieren",
        grammar("lassen"),
        conj("lassen", "du", "lässt"),
        conj("lassen", "er", "lässt"),
        conj("lassen", "wir", "lassen"),
        mc(
            "Ein Mechaniker repariert mein Auto. =",
            "Ich lasse mein Auto reparieren.",
            "Ich repariere mein Auto lassen.",
            "Ich lasse reparieren mein Auto.",
        ),
        fill("Ich ___ meinen Pass zu Hause. (leave)", "lasse"),
        fill("___ mich bitte ausreden! (let, du)", "Lass"),
        fill("Sie lässt die Tür ___. (reparieren)", "reparieren"),
        order("Wir lassen das Schloss wechseln."),
        tr("I'm having my car repaired.", "Ich lasse mein Auto reparieren."),
    ),
    lesson(
        "Bei der Polizei",
        bank(
            "Guten Tag, ich möchte einen ___ anzeigen. Jemand hat gestern meine Geldbörse "
            "___. Wo war das? Im Bus. Gibt es einen ___? Ja, eine Frau hat den ___ gesehen. "
            "Was war in der Geldbörse? Mein Ausweis, meine ___ und 50 Euro ___.",
            ["Diebstahl", "gestohlen", "Zeugen", "Täter", "EC-Karte", "Bargeld"],
            "Einbruch",
            "Versicherung",
        ),
        mc(
            "Where was the wallet stolen?",
            "On the bus.",
            "At home.",
            "At the citizens' office.",
        ),
        mc(
            "Bitte nichts anfassen! The police want ...",
            "nobody to touch anything.",
            "everyone to leave.",
            "a witness.",
        ),
        fill("Diebe sind in unser Haus ___. (einbrechen)", "eingebrochen"),
        fill("Die Polizei hat die Straße ___. (absperren)", "abgesperrt"),
        fill("Haben Sie den Diebstahl schon der Versicherung ___? (melden)", "gemeldet"),
        tr("Can you describe the culprit?", "Können Sie den Täter beschreiben?"),
    ),
    lesson(
        "Lektion 21: Test",
        mc("___ Karte brauchen Sie?", "Welche", "Welchen"),
        mc("Welchen Pass meinst du? ___ hier.", "Den", "Der"),
        fill("Ich ___ meine Uhr reparieren. (lassen)", "lasse"),
        fill("Er ___ sein Fahrrad im Keller. (lassen)", "lässt"),
        fill("Jemand hat mein Handy ___. (stehlen)", "gestohlen"),
        order("Ich habe meinen Ausweis im Bus verloren."),
        tr("Leave me alone! (du: lassen)", "Lass mich in Ruhe!"),
    ),
    lesson(
        "Modul 7: Wiederholung",
        mc("Wie wäre es ___ einem Kabarett?", "mit", "für"),
        fill("Ich schlage vor, dass wir ins Theater ___. (gehen)", "gehen"),
        fill("Als Kind ___ ich keine Comics lesen. (dürfen)", "durfte"),
        fill("Wir ___ jeden Tag Hausaufgaben machen. (müssen)", "mussten"),
        mc("Ich ___ keine Gedichte. (past of mögen)", "mochte", "möchte"),
        mc("___ Formular brauche ich?", "Welches", "Welchen"),
        fill("Meinst du den Ausweis? Ja, ___ meine ich.", "den"),
        fill("Ich ___ mein Fahrrad reparieren. (lassen)", "lasse"),
        bank(
            "Gestern ___ ich eigentlich zur Lesung gehen, aber ich ___ nicht: Jemand hat meine "
            "Geldbörse gestohlen und ich musste zur ___.",
            ["wollte", "konnte", "Polizei"],
            "durfte",
            "Behörde",
        ),
        tr("The concert is sold out.", "Das Konzert ist ausverkauft."),
        order("Ich lasse meinen Reisepass verlängern."),
    ),
]

LEKTION_21 = unit(
    21,
    "Ja genau, den meine ich.",
    "Staat und Verwaltung",
    L21_WORDS,
    L21_RULES,
    sections(L21_LESSONS, vocab_lessons(L21_WORDS, "Wörter")),
)


UNITS = [LEKTION_19, LEKTION_20, LEKTION_21]
