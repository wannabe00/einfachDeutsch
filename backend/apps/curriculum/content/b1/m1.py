"""Modul 1 (B1.1): Lektion 1 (Ihr seid einfach die Besten!), 2 (Er erledigte
seine Aufgaben zuverlässig.), 3 (Mein Beruf ist meine Leidenschaft.)."""

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
# Lektion 1: Ihr seid einfach die Besten!
# ============================================================================

L1_WORDS = [
    ("sensible", "vernünftig", "adjective"),
    ("generous", "großzügig", "adjective"),
    ("fair", "fair", "adjective"),
    ("intelligent", "intelligent", "adjective"),
    ("cheeky", "frech", "adjective"),
    ("thrifty", "sparsam", "adjective"),
    ("realistic", "realistisch", "adjective"),
    ("attentive", "aufmerksam", "adjective"),
    ("brave", "mutig", "adjective"),
    ("critical", "kritisch", "adjective"),
    ("loyal", "treu", "adjective"),
    ("honest", "ehrlich", "adjective"),
    ("modest", "bescheiden", "adjective"),
    ("humorous", "humorvoll", "adjective"),
    ("arrogant", "arrogant", "adjective"),
    ("witty", "witzig", "adjective"),
    ("lively", "lebendig", "adjective"),
    ("financial", "finanziell", "adjective"),
    ("as ... as possible", "möglichst", "adverb", "möglichst schnell"),
    ("the adult", "der Erwachsene", "noun", "ein Erwachsener, Pl. die Erwachsenen"),
    ("the role model", "das Vorbild", "noun", "Pl. die Vorbilder"),
    ("the respect", "der Respekt", "noun", "Respekt haben vor + Dat."),
    ("the quality / trait", "die Eigenschaft", "noun", "Pl. die Eigenschaften"),
    ("the courage", "der Mut", "noun"),
    ("the humour", "der Humor", "noun"),
    ("the decision", "die Entscheidung", "noun", "Pl. die Entscheidungen"),
    ("the adventure", "das Abenteuer", "noun", "Pl. die Abenteuer"),
    ("the lady", "die Dame", "noun", "Pl. die Damen"),
    ("the friendship", "die Freundschaft", "noun", "Pl. die Freundschaften"),
    ("the boy", "der Junge", "noun", "den Jungen, Pl. die Jungen"),
    ("to admire", "bewundern", "verb", "hat bewundert"),
    ("to support", "unterstützen", "verb", "hat unterstützt"),
    ("to trust", "vertrauen", "verb", "vertrauen + Dat."),
    ("to influence", "beeinflussen", "verb", "hat beeinflusst"),
    ("to fall asleep", "einschlafen", "verb", "schläft ein, ist eingeschlafen"),
    ("to say goodbye", "verabschieden", "verb", "sich verabschieden"),
    ("You're simply the best!", "Ihr seid einfach die Besten!", "phrase"),
    ("I have great respect for her.", "Ich habe großen Respekt vor ihr.", "phrase"),
]

L1_RULES = [
    rule(
        "Adjektive als Nomen",
        "adjectives",
        """
An adjective can stand for a **person**: *der Kluge* = the clever man. It is
written with a **capital letter** but keeps its **adjective ending**, exactly as
if the noun *Mann / Frau / Leute* still followed it:

| | masculine | feminine | plural |
|---|---|---|---|
| der / die | der Erwachsen**e** | die Erwachsen**e** | die Erwachsen**en** |
| ein / eine | ein Erwachsen**er** | eine Erwachsen**e** | Erwachsen**e** |
| Akkusativ | den / einen Erwachsen**en** | die / eine Erwachsen**e** | die Erwachsen**en** |
| Dativ | dem / einem Erwachsen**en** | der / einer Erwachsen**en** | den Erwachsen**en** |

So: *der Bekannte* but *ein Bekannt**er***; *die Kleinen* but *viele Klein**e***.

Common ones: *der/die Erwachsene, Bekannte, Deutsche, Jugendliche, Kranke,
Verwandte*, and the superlative *die Besten*.
""",
        [
            "Ihr seid einfach die Besten!",
            "Sie ist die Mutigste von uns.",
            "Ein Erwachsener muss das Formular unterschreiben.",
            "Ich habe gestern einen Bekannten getroffen.",
        ],
    ),
    rule(
        "n-Deklination",
        "cases",
        """
Some **masculine** nouns add **-n** or **-en** in every case except the
nominative singular:

| | singular | plural |
|---|---|---|
| Nominativ | der Kolleg**e** | die Kolleg**en** |
| Akkusativ | den Kolleg**en** | die Kolleg**en** |
| Dativ | dem Kolleg**en** | den Kolleg**en** |
| Genitiv | des Kolleg**en** | der Kolleg**en** |

Which nouns? Masculine nouns for people or animals ending in **-e** (*der Junge,
der Kunde, der Kollege, der Löwe*), most ending in **-ent / -ant / -ist**
(*der Student, der Praktikant, der Journalist*), and a few others: *der Mensch,
der Nachbar, der Herr (den Herrn), der Held*.

Not every masculine noun: *der Lehrer → den Lehrer*.
""",
        [
            "Später hat sie den Kollegen geheiratet.",
            "Ich helfe meinem Nachbarn im Garten.",
            "Kennst du den neuen Studenten?",
            "Wir sprechen mit dem Kunden.",
        ],
    ),
    rule(
        "Aussagen verstärken und abschwächen",
        "other",
        """
To make an opinion **stronger** or **weaker**, put a word before the adjective:

| | words | example |
|---|---|---|
| ++ | total, wahnsinnig, echt, richtig | *Der Vortrag war **total** spannend.* |
| + | sehr, wirklich, besonders, ziemlich | *Er ist **ziemlich** kreativ.* |
| − | nicht so, nicht besonders | *Das Essen war **nicht besonders** gut.* |
| −− | gar nicht, überhaupt nicht | *Sie ist **überhaupt nicht** arrogant.* |

*echt, total, wahnsinnig* are spoken and informal; in a letter use *sehr,
besonders, wirklich*.
""",
        [
            "Mein Mitbewohner ist echt witzig.",
            "Die Prüfung war nicht so schwer.",
            "Er ist überhaupt nicht großzügig.",
        ],
    ),
]

L1_LESSONS = [
    lesson(
        "Charaktereigenschaften",
        review("vernünftig"),
        review("großzügig"),
        match(
            [
                ("Sie teilt gern ihr Geld.", "großzügig"),
                ("Er gibt nur wenig Geld aus.", "sparsam"),
                ("Sie hat keine Angst.", "mutig"),
                ("Er hört immer genau zu.", "aufmerksam"),
                ("Sie bleibt bei ihren Freunden, auch wenn es schwer ist.", "treu"),
            ],
            "Which trait fits?",
        ),
        mc(
            "Er sagt immer die Wahrheit. Er ist ...",
            "ehrlich",
            "frech",
            "arrogant",
        ),
        mc(
            "Sie spricht nie über ihre Erfolge. Sie ist ...",
            "bescheiden",
            "kritisch",
            "realistisch",
        ),
        fill("Ein Kind, das nicht höflich ist, ist ___. (cheeky)", "frech"),
        fill("Sie erzählt die lustigsten Witze. Sie ist sehr ___. (witty)", "witzig"),
        tr("My flatmate is sensible and fair.", "Mein Mitbewohner ist vernünftig und fair."),
    ),
    lesson(
        "Die Klugen und die Mutigen",
        grammar("Adjektive als Nomen"),
        mc("Wir haben einen ___ getroffen. (bekannt)", "Bekannten", "Bekannter", "Bekannte"),
        fill("Ein ___ muss das Formular unterschreiben. (erwachsen)", "Erwachsener"),
        fill("Die ___ dürfen den Film nicht sehen. (jugendlich, Pl.)", "Jugendlichen"),
        fill("Ich habe gestern eine ___ von dir getroffen. (bekannt)", "Bekannte"),
        fill("Wir haben mit einem ___ gesprochen. (deutsch, m.)", "Deutschen"),
        fill("Ihr seid einfach die ___! (gut, Superlativ)", "Besten"),
        mc(
            "Which sentence is correct?",
            "Der Kluge hat die Antwort gewusst.",
            "Der Klugen hat die Antwort gewusst.",
            "Der Kluger hat die Antwort gewusst.",
        ),
        order("Die Erwachsenen sitzen im Garten."),
        tr("He is the bravest of us.", "Er ist der Mutigste von uns."),
    ),
    lesson(
        "Den Kollegen geheiratet",
        grammar("n-Deklination"),
        mc("Später hat sie ___ geheiratet.", "den Kollegen", "den Kollege", "dem Kollege"),
        mc("Ich helfe ___ im Garten.", "meinem Nachbarn", "meinem Nachbar", "meinen Nachbar"),
        fill("Kennst du den neuen ___? (Student)", "Studenten"),
        fill("Die Chefin spricht mit dem ___. (Kunde)", "Kunden"),
        fill("Wir haben einen ___ für den Sommer. (Praktikant)", "Praktikanten"),
        fill("Das Fahrrad gehört dem kleinen ___. (Junge)", "Jungen"),
        fill("Guten Tag, ___ Müller! (Herr, Akk.)", "Herrn"),
        mc(
            "Which noun does NOT take -n?",
            "der Lehrer",
            "der Mensch",
            "der Kollege",
            "der Student",
        ),
        order("Ich habe den Jungen im Park gesehen."),
        tr("I trust my neighbour.", "Ich vertraue meinem Nachbarn."),
    ),
    lesson(
        "Ein wichtiger Mensch in meinem Leben",
        review("das Vorbild"),
        mc(
            "Ein Vorbild ist ein Mensch, ...",
            "den man bewundert.",
            "den man nicht kennt.",
            "der immer frech ist.",
        ),
        fill("Ich habe großen ___ vor meiner Großmutter. (respect)", "Respekt"),
        fill("Meine Eltern haben mich immer ___. (unterstützen)", "unterstützt"),
        fill("Der Lehrer hat meine ___ für den Beruf beeinflusst. (decision)", "Entscheidung"),
        fill("Sie hat viel ___: Sie ist allein durch Afrika gereist. (courage)", "Mut"),
        mc("vertrauen + ...", "Dativ: Ich vertraue ihm.", "Akkusativ: Ich vertraue ihn."),
        bank(
            "Meine Tante ist mein ___. Sie ist sehr ___ und hat viel Humor. Als ich zwölf "
            "war, hat sie mich ___ unterstützt. Ich ___ sie sehr, weil sie so ___ ist.",
            ["Vorbild", "großzügig", "finanziell", "bewundere", "mutig"],
            "Abenteuer",
            "beeinflusst",
        ),
        tr("I met her five years ago.", "Ich habe sie vor fünf Jahren kennengelernt."),
    ),
    lesson(
        "In der Mensa: stärker oder schwächer",
        grammar("Aussagen verstärken und abschwächen"),
        mc(
            "Which is the strongest?",
            "Der Vortrag war wahnsinnig spannend.",
            "Der Vortrag war ziemlich spannend.",
            "Der Vortrag war nicht so spannend.",
        ),
        mc(
            "Which is the weakest (most negative)?",
            "Er ist überhaupt nicht nett.",
            "Er ist nicht besonders nett.",
            "Er ist ziemlich nett.",
        ),
        mc(
            "Which fits a formal letter?",
            "Die Zusammenarbeit war sehr angenehm.",
            "Die Zusammenarbeit war echt total super.",
            "Die Zusammenarbeit war wahnsinnig cool.",
        ),
        fill("Das Essen war ___ besonders gut. (not)", "nicht"),
        fill("Der Professor ist ___ nicht arrogant. (not at all: gar)", "gar"),
        order("Der neue Professor ist wirklich sympathisch."),
        tr("The exam was not that difficult.", "Die Prüfung war nicht so schwer."),
    ),
    lesson(
        "Lektion 1: Test",
        fill("Sie ist die ___ von uns allen. (klug, Superlativ)", "Klügste"),
        fill("Ich spreche oft mit meinem ___. (Kollege)", "Kollegen"),
        mc("Kennst du den ___?", "Jungen", "Junge", "Junges"),
        mc("Er gibt gern Geld für andere aus. Er ist ...", "großzügig", "sparsam", "frech"),
        fill("Sie hat sich am Bahnhof ___. (verabschieden)", "verabschiedet"),
        fill("Das Baby ist sofort ___. (einschlafen)", "eingeschlafen"),
        order("Ich habe großen Respekt vor meinem Vater."),
        tr("An adult has to sign.", "Ein Erwachsener muss unterschreiben."),
        tr("She is really honest.", "Sie ist wirklich ehrlich."),
    ),
]

LEKTION_1 = unit(
    1,
    "Ihr seid einfach die Besten!",
    "Freundschaft und Charakter",
    L1_WORDS,
    L1_RULES,
    sections(L1_LESSONS, vocab_lessons(L1_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 2: Er erledigte seine Aufgaben zuverlässig.
# ============================================================================

L2_WORDS = [
    ("the trainee", "der Auszubildende", "noun", "ein Auszubildender, short: der Azubi"),
    ("the educator / nursery teacher", "der Erzieher", "noun", "f. die Erzieherin"),
    ("the intern", "der Praktikant", "noun", "den Praktikanten, f. die Praktikantin"),
    ("the head / manager", "der Leiter", "noun", "f. die Leiterin"),
    ("the reference (from an employer)", "das Zeugnis", "noun", "Pl. die Zeugnisse"),
    ("the certificate", "die Bescheinigung", "noun", "Pl. die Bescheinigungen"),
    ("the performance / achievement", "die Leistung", "noun", "Pl. die Leistungen"),
    ("the theory", "die Theorie", "noun", "Pl. die Theorien"),
    ("the working atmosphere", "das Betriebsklima", "noun"),
    ("the knowledge", "die Kenntnis", "noun", "Pl. die Kenntnisse"),
    ("the opportunity", "die Gelegenheit", "noun", "Pl. die Gelegenheiten"),
    ("the noise", "der Lärm", "noun"),
    ("the overtime hour", "die Überstunde", "noun", "Pl. die Überstunden"),
    ("the full-time work", "die Vollzeit", "noun"),
    ("the part-time work", "die Teilzeit", "noun"),
    ("the feedback", "die Rückmeldung", "noun", "Pl. die Rückmeldungen"),
    ("the disappointment", "die Enttäuschung", "noun", "Pl. die Enttäuschungen"),
    ("the enthusiasm", "die Begeisterung", "noun"),
    ("to get done / to complete", "erledigen", "verb", "hat erledigt"),
    ("to take over", "übernehmen", "verb", "übernimmt, übernahm, hat übernommen"),
    ("to look after", "betreuen", "verb", "hat betreut"),
    ("to observe", "beobachten", "verb", "hat beobachtet"),
    ("to report", "berichten", "verb", "hat berichtet"),
    ("to train (someone)", "ausbilden", "verb", "hat ausgebildet"),
    ("to expect", "erwarten", "verb", "hat erwartet"),
    ("to lead / to guide", "führen", "verb", "hat geführt"),
    ("to think about / to consider", "überlegen", "verb", "sich etwas überlegen"),
    ("to decide (to do)", "entschließen", "verb", "sich entschließen, hat sich entschlossen"),
    ("to manage / to cope", "zurechtkommen", "verb", "kam zurecht, ist zurechtgekommen"),
    ("to be left over", "übrig bleiben", "verb", "ist übrig geblieben"),
    ("to say du to someone", "duzen", "verb", "hat geduzt"),
    ("gross (before tax)", "brutto", "adverb"),
    ("net (after tax)", "netto", "adverb"),
    ("low / small", "gering", "adjective"),
    ("strange", "merkwürdig", "adjective"),
    ("social", "sozial", "adjective"),
    (
        "Overall I liked the internship a lot.",
        "Insgesamt gefiel mir das Praktikum sehr gut.",
        "phrase",
    ),
    ("He did his tasks reliably.", "Er erledigte seine Aufgaben zuverlässig.", "phrase"),
]

L2_RULES = [
    rule(
        "Präteritum: gemischte Verben",
        "verbs",
        """
You know regular (*arbeitete*) and irregular (*ging*) Präteritum forms. A few
verbs are **mixed**: the stem changes **and** they take **-te**:

| Infinitiv | Präteritum | Perfekt |
|---|---|---|
| bringen | brach**te** | hat gebracht |
| denken | dach**te** | hat gedacht |
| kennen | kann**te** | hat gekannt |
| nennen | nann**te** | hat genannt |
| rennen | rann**te** | ist gerannt |
| wissen | wuss**te** | hat gewusst |

Endings as with all Präteritum forms: *ich brachte, du brachtest, er brachte,
wir brachten, ihr brachtet, sie brachten*. **ich** and **er/sie/es** never add
an ending.
""",
        [
            "Der Praktikant brachte mir einen Kaffee.",
            "Ich dachte, die Arbeit ist leicht.",
            "Niemand wusste die Antwort.",
            "Wir kannten die Kollegen noch nicht.",
        ],
    ),
    rule(
        "Präteritum in Berichten",
        "verbs",
        """
**Written** reports, references, stories and the news use the **Präteritum**.
Spoken German mostly uses the Perfekt, except for *sein, haben* and the modal
verbs.

| spoken (Perfekt) | written report (Präteritum) |
|---|---|
| *Ich habe im Kindergarten gearbeitet.* | *Ich arbeitete im Kindergarten.* |
| *Die Chefin hat mir alles gezeigt.* | *Die Chefin zeigte mir alles.* |
| *Er ist früh aufgestanden.* | *Er stand früh auf.* |

Separable verbs split in the Präteritum too: *Er **stand** um sechs **auf**.*
In a subordinate clause they join again: *..., weil er um sechs **aufstand**.*

Useful forms: *gefallen → gefiel, bekommen → bekam, halten → hielt, geben →
gab, helfen → half, finden → fand, schreiben → schrieb, werden → wurde*.
""",
        [
            "Insgesamt gefiel mir das Praktikum sehr gut.",
            "Am ersten Tag bekam ich eine eigene Gruppe.",
            "Er erledigte seine Aufgaben zuverlässig.",
        ],
    ),
    rule(
        "Einen Bericht gliedern",
        "other",
        """
A report tells events **in order** and ends with an **evaluation**.

**Order:** *Gleich am Morgen ... · Zuerst ... · Danach / Dann ... ·
Anschließend ... · Gegen Mittag ... · Am Nachmittag ... · Zum Schluss /
Schließlich ...* (the verb stays in position 2: *Danach **zeigte** sie mir ...*)

**Evaluation:** *Insgesamt gefiel mir ... · Besonders gut fand ich ... · Das
Betriebsklima war angenehm. · Der Tag war zwar anstrengend, aber ... · Ich war
von ... enttäuscht.*

**A reference (Zeugnis):** *Er erledigte seine Aufgaben stets zuverlässig. ·
Sie war immer freundlich und hilfsbereit. · Wir können ihn sehr empfehlen.*
""",
        [
            "Zuerst lernte ich die Kinder kennen.",
            "Anschließend half ich beim Mittagessen.",
            "Besonders gut fand ich die Teamsitzungen.",
        ],
    ),
]

L2_LESSONS = [
    lesson(
        "Beruf und Ausbildung",
        review("der Auszubildende"),
        review("das Zeugnis"),
        match(
            [
                ("der Erzieher", "arbeitet im Kindergarten"),
                ("der Auszubildende", "lernt einen Beruf im Betrieb"),
                ("der Praktikant", "arbeitet ein paar Wochen zur Probe"),
                ("die Leiterin", "führt die Abteilung"),
            ],
            "Who is it?",
        ),
        mc(
            "Das Gehalt ohne Steuern ist ...",
            "netto",
            "brutto",
            "gering",
        ),
        mc(
            "Nach dem Praktikum bekommt man oft ...",
            "eine Bescheinigung.",
            "eine Überstunde.",
            "einen Lärm.",
        ),
        fill("Sie arbeitet 20 Stunden pro Woche, also in ___. (part-time)", "Teilzeit"),
        fill("Wir müssen heute zwei ___ machen. (overtime hours)", "Überstunden"),
        tr("The working atmosphere was pleasant.", "Das Betriebsklima war angenehm."),
    ),
    lesson(
        "brachte, dachte, wusste",
        grammar("Präteritum: gemischte Verben"),
        conj("bringen (Präteritum)", "ich", "brachte"),
        conj("denken (Präteritum)", "wir", "dachten"),
        conj("wissen (Präteritum)", "du", "wusstest"),
        conj("kennen (Präteritum)", "sie (Pl.)", "kannten"),
        conj("nennen (Präteritum)", "er", "nannte"),
        fill("Am Anfang ___ ich die Kollegen noch nicht. (kennen)", "kannte"),
        fill("Niemand ___, wo der Schlüssel war. (wissen)", "wusste"),
        fill("Der Azubi ___ die Post ins Büro. (bringen)", "brachte"),
        mc("Ich ___, das ist eine einfache Arbeit.", "dachte", "denkte", "dacht"),
        order("Wir dachten an die Kinder."),
        tr("He brought the reference.", "Er brachte das Zeugnis."),
    ),
    lesson(
        "Mein Praktikum im Kindergarten",
        grammar("Präteritum in Berichten"),
        fill("Insgesamt ___ mir das Praktikum sehr gut. (gefallen)", "gefiel"),
        fill("Am ersten Tag ___ ich eine eigene Gruppe. (bekommen)", "bekam"),
        fill("Die Leiterin ___ mir den ganzen Betrieb. (zeigen)", "zeigte"),
        fill("Die Kinder ___ mir beim Aufräumen. (helfen)", "halfen"),
        fill("Er ___ jeden Tag um sechs Uhr auf. (aufstehen)", "stand"),
        mc(
            "Written report: Ich habe die Kinder betreut. →",
            "Ich betreute die Kinder.",
            "Ich betreut die Kinder.",
            "Ich betreutete die Kinder.",
        ),
        mc(
            "Which sentence is correct?",
            "Ich war müde, weil ich früh aufstand.",
            "Ich war müde, weil ich stand früh auf.",
            "Ich war müde, weil ich früh stand auf.",
        ),
        order("Danach beobachtete ich die Kinder beim Spielen."),
        tr("The children were very nice.", "Die Kinder waren sehr nett."),
        tr("I took over a group.", "Ich übernahm eine Gruppe."),
    ),
    lesson(
        "Mein erster Arbeitstag",
        grammar("Einen Bericht gliedern"),
        bank(
            "Mein erster Arbeitstag in der Werkstatt war spannend. ___ zeigte mir der Meister "
            "alle Maschinen. ___ bekam ich meine erste Aufgabe. Gegen ___ aßen wir zusammen. "
            "Am Nachmittag ___ ich allein ein Fahrrad. ___ war ich müde, aber zufrieden.",
            ["Zuerst", "Danach", "Mittag", "reparierte", "Zum Schluss"],
            "Gestern",
            "repariere",
        ),
        mc(
            "Which sentence is correct?",
            "Anschließend half ich in der Küche.",
            "Anschließend ich half in der Küche.",
            "Anschließend half in der Küche ich.",
        ),
        mc(
            "In a reference (Zeugnis) you read:",
            "Sie erledigte ihre Aufgaben stets zuverlässig.",
            "Sie war echt total nett.",
            "Sie hat immer Lärm gemacht.",
        ),
        fill("Der Tag war ___ anstrengend, aber schön. (admittedly)", "zwar"),
        fill("Ich war von der Arbeit ein bisschen ___. (disappointed)", "enttäuscht"),
        order("Besonders gut fand ich die Teamsitzungen."),
        tr("I can recommend the internship.", "Ich kann das Praktikum empfehlen."),
    ),
    lesson(
        "Im Betrieb",
        mc(
            "Wir duzen uns. means:",
            "We say du to each other.",
            "We work together.",
            "We don't know each other.",
        ),
        mc(
            "Nach dem Fest ist viel Kuchen ...",
            "übrig geblieben.",
            "zurechtgekommen.",
            "erledigt.",
        ),
        fill("Am Anfang bin ich mit der Arbeit gut ___. (zurechtkommen)", "zurechtgekommen"),
        fill("Ich habe mich ___, eine Ausbildung zu machen. (entschließen)", "entschlossen"),
        fill("Das war ein ___ Tag: Niemand war im Büro. (strange)", "merkwürdiger"),
        fill("Ich hatte die ___, mit dem Chef zu sprechen. (opportunity)", "Gelegenheit"),
        tr("I expected more.", "Ich habe mehr erwartet."),
    ),
    lesson(
        "Lektion 2: Test",
        fill("Gestern ___ ich keine Zeit. (haben)", "hatte"),
        fill("Der Praktikant ___ die Aufgabe sofort. (erledigen)", "erledigte"),
        mc("Sie ___ die Antwort nicht.", "wusste", "wisste", "weißte"),
        fill("Am Nachmittag ___ die Kinder im Garten. (spielen)", "spielten"),
        mc("Das Gehalt mit Steuern ist ...", "brutto", "netto", "sozial"),
        order("Sie erledigte ihre Aufgaben zuverlässig."),
        tr("Overall I liked the work a lot.", "Insgesamt gefiel mir die Arbeit sehr gut."),
        tr("He looked after the children.", "Er betreute die Kinder."),
    ),
]

LEKTION_2 = unit(
    2,
    "Er erledigte seine Aufgaben zuverlässig.",
    "Praktikum und Arbeitswelt",
    L2_WORDS,
    L2_RULES,
    sections(L2_LESSONS, vocab_lessons(L2_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 3: Mein Beruf ist meine Leidenschaft.
# ============================================================================

L3_WORDS = [
    ("the passion", "die Leidenschaft", "noun", "Pl. die Leidenschaften"),
    ("the estate agent", "der Makler", "noun", "f. die Maklerin"),
    ("the caretaker", "der Hausmeister", "noun", "f. die Hausmeisterin"),
    ("the resident", "der Bewohner", "noun", "f. die Bewohnerin"),
    ("the owner-occupied flat", "die Eigentumswohnung", "noun", "Pl. die Eigentumswohnungen"),
    ("the property / ownership", "das Eigentum", "noun"),
    ("the detached house", "das Einfamilienhaus", "noun", "Pl. die Einfamilienhäuser"),
    ("the terraced house", "das Reihenhaus", "noun", "Pl. die Reihenhäuser"),
    ("the block of flats", "der Wohnblock", "noun", "Pl. die Wohnblöcke"),
    ("the suburb", "der Vorort", "noun", "Pl. die Vororte"),
    ("the city centre", "die Innenstadt", "noun", "Pl. die Innenstädte"),
    ("the location", "die Lage", "noun", "in bester Lage"),
    ("the plot of land", "das Grundstück", "noun", "Pl. die Grundstücke"),
    ("the floor area", "die Wohnfläche", "noun", "Pl. die Wohnflächen"),
    ("the courtyard", "der Innenhof", "noun", "Pl. die Innenhöfe"),
    ("the terrace", "die Terrasse", "noun", "Pl. die Terrassen"),
    ("the stove / oven", "der Ofen", "noun", "Pl. die Öfen"),
    ("the lift", "der Lift", "noun", "Pl. die Lifts"),
    ("the bin", "der Mülleimer", "noun", "Pl. die Mülleimer"),
    ("the housing shortage", "der Wohnungsmangel", "noun"),
    ("the population", "die Bevölkerung", "noun"),
    ("the citizen", "der Bürger", "noun", "f. die Bürgerin"),
    ("the state", "der Staat", "noun", "Pl. die Staaten"),
    ("the nationality", "die Staatsangehörigkeit", "noun", "Pl. die Staatsangehörigkeiten"),
    ("the half", "die Hälfte", "noun", "Pl. die Hälften"),
    ("the third", "das Drittel", "noun", "Pl. die Drittel"),
    ("the quarter", "das Viertel", "noun", "Pl. die Viertel"),
    ("the photographer", "der Fotograf", "noun", "den Fotografen, f. die Fotografin"),
    ("to move in", "einziehen", "verb", "zog ein, ist eingezogen"),
    ("to throw", "werfen", "verb", "wirft, warf, hat geworfen"),
    ("to prevail / to rule", "herrschen", "verb", "hat geherrscht"),
    ("narrow / cramped", "eng", "adjective"),
    ("away / distant", "entfernt", "adjective", "zwei Kilometer entfernt"),
    ("dense / close", "dicht", "adjective"),
    ("lonely", "einsam", "adjective"),
    ("foreign", "ausländisch", "adjective"),
    ("about / roughly", "etwa", "adverb"),
    ("recently", "kürzlich", "adverb"),
    ("however", "allerdings", "adverb"),
    ("My job is my passion.", "Mein Beruf ist meine Leidenschaft.", "phrase"),
    ("Do you rent?", "Wohnen Sie zur Miete?", "phrase"),
]

L3_RULES = [
    rule(
        "Relativsätze im Dativ",
        "sentence_structure",
        """
You know relative clauses with *der, die, das* (Nominativ) and *den*
(Akkusativ). When the verb or preposition **in the relative clause** needs the
**dative**, the relative pronoun is dative:

| | masculine | feminine | neuter | plural |
|---|---|---|---|---|
| Dativ | **dem** | **der** | **dem** | **denen** |

- *Das ist der Mann, **dem** ich geholfen habe.* (helfen + Dativ)
- *Sie war eine Kundin, **der** keine Wohnung gefiel.* (gefallen + Dativ)
- *Das sind die Kunden, **denen** wir geschrieben haben.*

Gender and number come from the noun **before** the comma; the case comes from
the job the pronoun does **inside** the relative clause. The verb goes to the
end.
""",
        [
            "Das ist die Frau, der ich die Wohnung gezeigt habe.",
            "Der Hausmeister, dem wir vertrauen, hat einen Schlüssel.",
            "Die Bewohner, denen der Garten gehört, sind sehr nett.",
        ],
    ),
    rule(
        "Relativsätze mit Präposition",
        "sentence_structure",
        """
If the verb comes with a preposition, the preposition stands **directly before**
the relative pronoun. The preposition decides the case:

- *Das ist die Wohnung, **in der** ich wohne.* (in + Dativ: Wo?)
- *Das ist der Garten, **in dem** ich mich ausruhe.*
- *Das ist die Wohnung, **für die** ich mich interessiere.* (sich interessieren für + Akk.)
- *Das sind die Leute, **mit denen** ich zusammenwohne.* (mit + Dativ)
- *Das ist der Makler, **über den** ich mich geärgert habe.* (sich ärgern über + Akk.)

Never leave the preposition at the end, as in English (*the flat I live in*).
""",
        [
            "Das ist das Haus, in dem ich aufgewachsen bin.",
            "Das ist die Terrasse, auf der wir frühstücken.",
            "Die Nachbarn, mit denen ich spreche, sind freundlich.",
        ],
    ),
    rule(
        "Statistiken beschreiben",
        "other",
        """
To talk about numbers and surveys:

| fraction | | quantity words |
|---|---|---|
| die **Hälfte** (1/2) | *Die Hälfte von uns wohnt zur Miete.* | **fast alle** |
| ein **Drittel** (1/3) | *Ein Drittel wohnt im Vorort.* | **die meisten** |
| ein **Viertel** (1/4) | *Ein Viertel lebt allein.* | **viele / nur wenige** |
| drei **Viertel** (3/4) | | **keiner** |
| **jeder Zweite** | *Jeder Zweite hat einen Balkon.* | |

Approximate: ***etwa / rund / ungefähr** 40 Prozent, **fast** 80 Prozent,
**mehr als / knapp** die Hälfte*. With a fraction or *Prozent* the verb is
usually **singular**: *Ein Drittel **wohnt** ...; 20 Prozent **lebt** ...*
""",
        [
            "Mehr als die Hälfte der Bevölkerung wohnt zur Miete.",
            "Jeder Zweite im Kurs wohnt in der Innenstadt.",
            "Etwa ein Viertel der Haushalte hat einen Garten.",
        ],
    ),
]

L3_LESSONS = [
    lesson(
        "Rund ums Wohnen",
        review("das Reihenhaus"),
        review("der Vorort"),
        match(
            [
                ("das Einfamilienhaus", "ein Haus für eine Familie"),
                ("das Reihenhaus", "viele gleiche Häuser in einer Reihe"),
                ("der Wohnblock", "ein großes Haus mit vielen Wohnungen"),
                ("die Eigentumswohnung", "eine Wohnung, die einem gehört"),
                ("der Vorort", "ein Ort am Rand von einer Großstadt"),
            ],
            "Match the housing to its description.",
        ),
        mc(
            "Wer hilft, eine Wohnung zu finden?",
            "der Makler",
            "der Fotograf",
            "der Bürger",
        ),
        mc(
            "Wer repariert im Haus die Heizung und das Licht?",
            "der Hausmeister",
            "der Bewohner",
            "der Staat",
        ),
        fill("Die Wohnung hat 85 Quadratmeter ___. (floor area)", "Wohnfläche"),
        fill("In der Großstadt gibt es einen großen ___. (housing shortage)", "Wohnungsmangel"),
        tr("The flat is in the best location.", "Die Wohnung liegt in bester Lage."),
    ),
    lesson(
        "Ein Makler mit Leidenschaft",
        mc(
            "Mein Beruf ist meine Leidenschaft. means:",
            "I love my job.",
            "My job is very hard.",
            "I'm looking for a new job.",
        ),
        mc(
            "Die Küche ist sehr klein und ___.",
            "eng",
            "einsam",
            "ausländisch",
        ),
        fill("Wir sind letzte Woche in die neue Wohnung ___. (einziehen)", "eingezogen"),
        fill("Der Bahnhof ist nur zwei Kilometer ___. (away)", "entfernt"),
        fill("Bitte ___ den Müll in den Mülleimer! (werfen, du)", "wirf"),
        fill("Ohne Nachbarn fühlt sie sich sehr ___. (lonely)", "einsam"),
        fill("Die Wohnung ist schön, ___ ist sie teuer. (however)", "allerdings"),
        tr("Do you rent? (Sie)", "Wohnen Sie zur Miete?"),
    ),
    lesson(
        "Die Kundin, der nichts gefiel",
        grammar("Relativsätze im Dativ"),
        mc("Das ist der Mann, ___ ich geholfen habe.", "dem", "den", "der"),
        mc("Das ist die Frau, ___ ich die Wohnung gezeigt habe.", "der", "die", "dem"),
        mc("Das sind die Kunden, ___ wir geschrieben haben.", "denen", "den", "die"),
        fill("Das ist das Kind, ___ das Fahrrad gehört. (gehören + Dat.)", "dem"),
        fill("Sie war eine Kundin, ___ keine Wohnung gefiel.", "der"),
        fill("Die Bewohner, ___ wir vertrauen, haben einen Schlüssel.", "denen"),
        fill("Der Makler, ___ ich gestern begegnet bin, war sehr nett.", "dem"),
        order("Das ist die Nachbarin, der ich oft helfe."),
        tr(
            "That is the caretaker whom I thanked.",
            "Das ist der Hausmeister, dem ich gedankt habe.",
        ),
    ),
    lesson(
        "Der Garten, in dem ich mich ausruhe",
        grammar("Relativsätze mit Präposition"),
        mc("Das ist die Wohnung, ___ ich wohne.", "in der", "in die", "der in"),
        mc("Das ist die Wohnung, ___ ich mich interessiere.", "für die", "für der", "die für"),
        mc("Das sind die Leute, ___ ich zusammenwohne.", "mit denen", "mit den", "mit die"),
        fill("Das ist der Balkon, auf ___ die Blumen stehen.", "dem"),
        fill("Das ist der Makler, über ___ ich mich geärgert habe.", "den"),
        fill("Das ist das Haus, in ___ ich aufgewachsen bin.", "dem"),
        fill("Die Stadt, von ___ ich träume, liegt am Meer.", "der"),
        order("Das ist die Terrasse, auf der wir frühstücken."),
        tr(
            "That is the flat I am looking for.",
            "Das ist die Wohnung, die ich suche.",
        ),
        tr(
            "These are the neighbours I talk to.",
            "Das sind die Nachbarn, mit denen ich spreche.",
        ),
    ),
    lesson(
        "Wohnen in Deutschland",
        grammar("Statistiken beschreiben"),
        match(
            [
                ("die Hälfte", "50 Prozent"),
                ("ein Drittel", "etwa 33 Prozent"),
                ("ein Viertel", "25 Prozent"),
                ("drei Viertel", "75 Prozent"),
                ("jeder Zweite", "die Hälfte von allen"),
            ],
            "Match the numbers.",
        ),
        mc(
            "Mehr als ___ der Bevölkerung wohnt zur Miete.",
            "die Hälfte",
            "das Halbe",
            "die Halbe",
        ),
        mc(
            "Which sentence is correct?",
            "Ein Drittel der Haushalte hat einen Garten.",
            "Ein Drittel der Haushalte haben ein Garten.",
            "Ein Drittel von Haushalte hat Garten.",
        ),
        fill("___ Zweite im Kurs wohnt in der Innenstadt. (every)", "Jeder"),
        fill("Die ___ von uns haben einen Balkon. (most)", "meisten"),
        fill("___ 40 Prozent haben eine ausländische Staatsangehörigkeit. (about)", "Etwa|Rund"),
        order("Fast alle im Kurs wohnen zur Miete."),
        tr("A quarter of the people live alone.", "Ein Viertel der Menschen lebt allein."),
    ),
    lesson(
        "Lektion 3: Test",
        mc("Das ist die Nachbarin, ___ ich die Blumen gegeben habe.", "der", "die", "denen"),
        fill("Das sind die Kinder, mit ___ mein Sohn spielt.", "denen"),
        fill("Das ist das Zimmer, in ___ ich arbeite.", "dem"),
        mc(
            "Eine Wohnung, die einem gehört, ist eine ...",
            "Eigentumswohnung",
            "Mietwohnung",
            "Wohngemeinschaft",
        ),
        fill("Die ___ der Kursteilnehmer kommt aus Europa. (half)", "Hälfte"),
        order("Wir wohnen in einem Reihenhaus im Vorort."),
        tr("That is the man I helped.", "Das ist der Mann, dem ich geholfen habe."),
        tr("The street is very narrow.", "Die Straße ist sehr eng."),
    ),
    lesson(
        "Modul 1: Wiederholung",
        fill("Sie ist die ___ in der Familie. (mutig, Superlativ)", "Mutigste"),
        fill("Ich habe den neuen ___ kennengelernt. (Kollege)", "Kollegen"),
        fill("Gestern ___ ich lange im Büro. (bleiben)", "blieb"),
        fill("Er ___ mir einen Kaffee. (bringen, Präteritum)", "brachte"),
        mc("Das ist die Frau, ___ ich vertraue.", "der", "die", "dem"),
        mc("Das ist das Haus, ___ ich wohne.", "in dem", "in das", "dem in"),
        fill("Jeder ___ hat einen Balkon. (second)", "Zweite"),
        bank(
            "Mein Praktikum beim ___ war super. Am ersten Tag ___ ich eine Kundin, ___ "
            "eine Wohnung in bester Lage suchte. Wir besichtigten ein Haus, ___ dem ein großer "
            "Garten gehörte. Die Kundin war total ___!",
            ["Makler", "traf", "die", "zu", "begeistert"],
            "der",
            "treffe",
        ),
        tr("He is a sensible adult.", "Er ist ein vernünftiger Erwachsener."),
        order("Das ist die Wohnung, für die ich mich interessiere."),
    ),
]

LEKTION_3 = unit(
    3,
    "Mein Beruf ist meine Leidenschaft.",
    "Wohnen und Statistik",
    L3_WORDS,
    L3_RULES,
    sections(L3_LESSONS, vocab_lessons(L3_WORDS, "Wörter")),
)


UNITS = [LEKTION_1, LEKTION_2, LEKTION_3]
